from datetime import datetime
from ..utils.background_tasks.tasks import upload_image_task
from ..repositories.order_repository import OrderRepository
from ..api.schemas.order import OrderRequestDTO, OrderResponseDTO
from typing import List, Optional
from fastapi.exceptions import HTTPException
from ..models.order import OrderAssignment, OrderAssignmentStatus, OrderStatus
from ..models.order import OrderAssignmentPolicy
from fastapi import UploadFile
import json, httpx
from ..core.conifg import settings
from ..services.image_service import ImageService
from ..services.messaging_service import MessagingService

class OrderService:
    def __init__(
            self, 
            order_repository: OrderRepository,
            image_service: ImageService,
            messaging_service: MessagingService
            ):
        self.order_repository = order_repository
        self.image_service = image_service
        self.messaging_service = messaging_service

    async def create_order(self, order: OrderRequestDTO, user: dict, image: Optional[UploadFile] = None) -> OrderResponseDTO:
        try:
            scheduled_date_naive = datetime.now().replace(tzinfo=None)

            image_url = None 
            order_data = {
                "user_id": user["id"],
                "description": order.description,
                "service_type_name": order.service_type_name,
                "scheduled_date": scheduled_date_naive,
                "status": OrderStatus.NEW.value,
                "assignment_policy": order.assignment_policy.value,
                "image_url": image_url, 
            }

            if image:
                if not image.filename:
                    raise ValueError("Uploaded file must have a name")
                image_url = await self.image_service.upload_image(image)
                order_data["image_url"] = image_url 

            new_order = await self.order_repository.create_order(order_data)

            response = OrderResponseDTO(
                id=new_order.id,
                description=new_order.description,
                service_type_name=new_order.service_type_name,
                scheduled_date=new_order.scheduled_date,
                status=new_order.status.value,
                image_url=image_url if image_url else None
            )

            response.model_validate(response.model_dump())
            return response
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Error uploading image: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while creating order: {str(e)}")

    async def update_order(self, order_id: int, order_data: dict, user: dict) -> OrderResponseDTO:
        try:
            order = await self.order_repository.get_order_by_id(order_id)
            if not order or order.user_id != user['id']:
                raise HTTPException(status_code=403, detail="You don't have permission to update this order.")

            if 'status' in order_data:
                order.status = order_data['status']
            if 'scheduled_date' in order_data:
                order.scheduled_date = order_data['scheduled_date']

            await self.order_repository.update_order(order_id, order_data)
            return OrderResponseDTO(
                id=order.id,
                description=order.description,
                service_type_name=order.service_type_name,
                scheduled_date=order.scheduled_date,
                status=order.status.value
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while updating order: {str(e)}")
    
    async def delete_order(self, order_id: int, user: dict) -> None:
        try:
            order = await self.order_repository.get_order_by_id(order_id)
            if not order or order.user_id != user["id"]:
                raise HTTPException(status_code=403, detail="You don't have permission to delete this order.")

            await self.order_repository.delete_order(order_id)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while deleting order: {str(e)}")

    async def assign_order(self, order_id: int, provider_id: int) -> OrderAssignment:
        try:
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
            return assignment
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while assigning order: {str(e)}")
        
    async def get_user_orders(self, user: dict) -> List[OrderResponseDTO]:
        try:
            orders = await self.order_repository.get_user_orders(user["id"])

            return [
                OrderResponseDTO(
                    id=order.id,
                    description=order.description,
                    service_type_name=order.service_type_name,
                    scheduled_date=order.scheduled_date,
                    status=order.status.value,
                    image_url=order.image_url
                )
                for order in orders
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user orders: {str(e)}")
        
    async def get_all_orders(self) -> List[OrderResponseDTO]:
        try:
            orders = await self.order_repository.get_all_orders()

            return [
                OrderResponseDTO(
                    id=order.id,
                    description=order.description,
                    service_type_name=order.service_type_name,
                    scheduled_date=order.scheduled_date,
                    status=order.status.value,
                    image_url=order.image_url
                )
                for order in orders
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching all orders: {str(e)}")
        
    async def get_order_by_id(self, order_id: int, user: dict) -> OrderResponseDTO:
        try:
            order = await self.order_repository.get_order_by_id(order_id)
            if not order or order.user_id != user["id"]:
                raise HTTPException(status_code=404, detail="Order not found or access denied.")

            return OrderResponseDTO(
                id=order.id,
                description=order.description,
                service_type_name=order.service_type_name,
                scheduled_date=order.scheduled_date,
                status=order.status.value,
                image_url=order.image_url
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching order by ID: {str(e)}")
        
    async def process_order(self, order_id: int, user: dict) -> OrderResponseDTO:
        try:
            order = await self.order_repository.get_order_by_id(order_id)

            if not order:
                raise HTTPException(status_code=404, detail="Order not found or access denied.")

            if order.user_id == user["id"]:
                raise HTTPException(status_code=403, detail="You cannot process your own order.")

            assignments = await self.order_repository.get_assignments_for_order(order_id)

            if all(assignment.status == OrderAssignmentStatus.COMPLETED for assignment in assignments):
                order.status = OrderStatus.IN_PROGRESS
                await self.order_repository.update_order(order_id, {"status": order.status})

                notification_message = {
                    "order_id": order_id,
                    "creator_id": order.user_id,
                    "executor_id": user["id"], 
                    "message": f"User {user['id']} started processing order {order_id}."
                }

                await self.messaging_service.send_message(json.dumps(notification_message), "notifications")

            else:
                raise HTTPException(status_code=400, detail="Order is not yet fully completed by all providers.")

            return OrderResponseDTO(
                id=order.id,
                description=order.description,
                service_type_name=order.service_type_name,
                scheduled_date=order.scheduled_date,
                status=order.status.value,
                image_url=order.image_url
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing order: {str(e)}")

    async def confirm_order_completion(self, order_id: int, user: dict) -> dict:
        try:
            order = await self.order_repository.get_order_by_id(order_id)

            if not order or order.user_id != user["id"]:
                raise HTTPException(status_code=403, detail="You don't have permission to confirm completion of this order.")

            assignments = await self.order_repository.get_assignments_for_order(order_id)
            if not all(assignment.status == OrderAssignmentStatus.COMPLETED for assignment in assignments):
                raise HTTPException(status_code=400, detail="Order cannot be confirmed as completed until providers complete it.")

            await self.order_repository.update_order(order_id, {"status": OrderStatus.COMPLETED.value})

            return {"id": order_id, "status": "COMPLETED"}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error confirming order completion: {str(e)}")
    
    async def get_user_notifications(self, user_id: int) -> list:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{settings().NOTIFICATION_SERVICE_URL}/notifications/{user_id}")
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Notification Service is unavailable: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch notifications: {str(e)}")
