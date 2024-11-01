from datetime import datetime, timezone
from src.repositories.order_repository import OrderRepository
from src.api.schemas.order import OrderRequest, OrderResponse
from src.models.order import OrderStatus
from typing import List
import logging
from fastapi.exceptions import HTTPException
from src.utils.logger import logger

class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def create_order(self, order: OrderRequest, user: dict) -> OrderResponse:
        try:
            scheduled_date_with_tz = datetime.now(timezone.utc)
            scheduled_date_naive = scheduled_date_with_tz.replace(tzinfo=None)

            order_data = {
                "user_id": user["id"],
                "description": order.description,
                "service_type_name": order.service_type_name,
                "scheduled_date": scheduled_date_naive,
                "status": OrderStatus.NEW.value
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
            raise HTTPException(status_code=500, detail="An error occurred while creating the order")
        
    async def update_order(self, order_id: int, order_data: dict, user: dict) -> dict:
        order = await self.order_repository.get_order_by_id(order_id)
        if not order or order.user_id != user['id']:
            raise HTTPException(status_code=403, detail="You don't have permission to update this order.")

        if 'status' in order_data:
            order.status = order_data['status']
        if 'assigned_provider' in order_data:
            order.assigned_provider = order_data['assigned_provider']
        if 'scheduled_date' in order_data:
            order.scheduled_date = order_data['scheduled_date']

        await self.order_repository.update_order(order_id, order_data)
        return order
        
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
            return None
        
        return OrderResponse(
            id=order.id,
            description=order.description,
            service_type_name=order.service_type_name,
            scheduled_date=order.scheduled_date,
            status=order.status.value
        )
        
    async def process_order(self, order_id: int, user: dict) -> OrderResponse:
        order = await self.order_repository.get_order_by_id(order_id)

        if not order or order.user_id != user["id"]:
            return None

        logger.info(f"Processing order {order.id} with status {order.status}")

        if order.status != OrderStatus.NEW:
            raise ValueError(f"Order cannot be processed. Current status: {order.status}")

        order.status = OrderStatus.COMPLETED

        await self.order_repository.update_order(order_id, {"status": order.status})

        return OrderResponse(
            id=order.id,
            description=order.description,
            service_type_name=order.service_type_name,
            scheduled_date=order.scheduled_date,
            status=order.status.value
        )