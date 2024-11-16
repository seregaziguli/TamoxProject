from datetime import datetime, timezone
import fastapi
from src.repositories.order_repository import OrderRepository
from src.api.schemas.order import OrderRequest, OrderResponse
import src.models.order
from typing import List, Optional
from fastapi.exceptions import HTTPException
from src.utils.logger import logger
from src.models.order import OrderAssignment, OrderAssignmentStatus, OrderStatus
from src.models.order import OrderAssignmentPolicy
from fastapi import UploadFile
from src.services.s3_service import S3Client

class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        self.s3_client = S3Client

    async def create_order(self, order: OrderRequest, user: dict, image: Optional[UploadFile] = None) -> OrderResponse:
        try:
            scheduled_date_with_tz = datetime.now(timezone.utc)
            scheduled_date_naive = scheduled_date_with_tz.replace(tzinfo=None)

            image_url = None
            if image:
                object_name = self.s3_client.generate_object_name("orders", image.filename)
                image_content = await image.read()
                image_url = await self.s3_client.upload_image_bytes(image_content, object_name)

            order_data = {
                "user_id": user["id"],
                "description": order.description,
                "service_type_name": order.service_type_name,
                "scheduled_date": scheduled_date_naive,
                "status": OrderStatus.NEW.value,
                "assignment_policy": order.assignment_policy.value,
                "image_url": image_url
            }
            new_order = await self.order_repository.create_order(order_data)
            
            logger.info(f"Order {new_order.id} successfully created for user {user['id']}.")

            return OrderResponse(
                id=new_order.id,
                description=new_order.description,
                service_type_name=new_order.service_type_name,
                scheduled_date=new_order.scheduled_date,
                status=new_order.status.value
            )
            
        except Exception as e:
            logger.error("Failed to create order: %s", e)
            raise HTTPException(status_code=500, detail="An error occurred while creating the order.")
        
    async def update_order(self, order_id: int, order_data: dict, user: dict) -> OrderResponse:
        order = await self.order_repository.get_order_by_id(order_id)
        if not order or order.user_id != user['id']:
            raise HTTPException(status_code=403, detail="You don't have permission to update this order.")

        if 'status' in order_data:
            order.status = order_data['status']
        if 'scheduled_date' in order_data:
            order.scheduled_date = order_data['scheduled_date']

        await self.order_repository.update_order(order_id, order_data)
        return OrderResponse(
            id=order.id,
            description=order.description,
            service_type_name=order.service_type_name,
            scheduled_date=order.scheduled_date,
            status=order.status.value
        )
    
    async def assign_order(self, order_id: int, provider_id: int) -> OrderAssignment:
        order = await self.order_repository.get_order_by_id(order_id)

        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")
        
        if order.status == OrderStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Order is already completed and cannot be reassigned.")
    
        if order.assignment_policy == OrderAssignmentPolicy.EXCLUSIVE:
            existing_assignments = await self.order_repository.get_assignments_for_order(order_id)
            if existing_assignments:
                raise HTTPException(status_code=400, detail="Exclusive order can only have one assignment")
        
        assignment_data = {
            "order_id": order.id,
            "provider_id": provider_id,
            "status": OrderAssignmentStatus.PENDIND,
            "completion_date": None
        }

        assignment = await self.order_repository.create_assignment(assignment_data)
        logger.debug(f"Creating assignment {assignment} with data {assignment_data}")
        return assignment
        
    async def get_user_orders(self, user: dict) -> List[OrderResponse]:
        orders = await self.order_repository.get_user_orders(user["id"])
        
        return [
            OrderResponse(
                id=order.id,
                description=order.description,
                service_type_name=order.service_type_name,
                scheduled_date=order.scheduled_date,
                status=order.status.value
            )
            for order in orders
        ]
        
    async def get_all_orders(self) -> List[OrderResponse]:
        orders = await self.order_repository.get_all_orders()
        
        return [
            OrderResponse(
                id=order.id,
                description=order.description,
                service_type_name=order.service_type_name,
                scheduled_date=order.scheduled_date,
                status=order.status.value
            )
            for order in orders
        ]
        
    async def get_order_by_id(self, order_id: int, user: dict) -> OrderResponse:
        order = await self.order_repository.get_order_by_id(order_id)
        if not order or order.user_id != user["id"]:
            raise HTTPException(status_code=404, detail="Order not found or access denied.")
        
        return OrderResponse(
            id=order.id,
            description=order.description,
            service_type_name=order.service_type_name,
            scheduled_date=order.scheduled_date,
            status=order.status.value
        )
        
    async def process_order(self, order_id: int, user: dict) -> OrderResponse:
        order = await self.order_repository.get_order_by_id(order_id)
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found or access denied.")

        assignments = await self.order_repository.get_assignments_for_order(order_id)
        
        if all(assignment.status == OrderAssignmentStatus.COMPLETED for assignment in assignments):
            order.status = OrderStatus.IN_PROGRESS
            await self.order_repository.update_order(order_id, {"status": order.status})
        else:
            raise HTTPException(status_code=400, detail="Order is not yet fully completed by all providers.")
        
        return OrderResponse(
            id=order.id,
            description=order.description,
            service_type_name=order.service_type_name,
            scheduled_date=order.scheduled_date,
            status=order.status.value
        )
    
    async def confirm_order_completion(self, order_id: int, user: dict) -> dict:
        order = await self.order_repository.get_order_by_id(order_id)
        
        if not order or order.user_id != user["id"]:
            raise HTTPException(status_code=403, detail="You don't have permission to confirm completion of this order.")
        
        assignments = await self.order_repository.get_assignments_for_order(order_id)
        if not all(assignment.status == OrderAssignmentStatus.COMPLETED for assignment in assignments):
            raise HTTPException(status_code=400, detail="Order cannot be confirmed as completed until providers complete it.")
        
        await self.order_repository.update_order(order_id, {"status": OrderStatus.COMPLETED.value})
        return {"id": order_id, "status": "COMPLETED"}
