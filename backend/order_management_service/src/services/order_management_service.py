from ..repositories.order_management_repository import OrderManagementRepository
from fastapi import HTTPException

class OrderManagementService:
    def __init__(self, order_management_repository: OrderManagementRepository):
        self.order_management_repository = order_management_repository

    async def get_order_by_id(self, order_id: int) -> dict:
        try:
            return await self.order_management_repository.get_order_by_id(order_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching order with ID {order_id}: {str(e)}")

    async def update_order(self, order_id: int, order_data: dict) -> None:
        try:
            await self.order_management_repository.update_order(order_id, order_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating order with ID {order_id}: {str(e)}")

    async def process_order_update(self, order_id: int, order_data: dict) -> None:
        try:
            order = await self.get_order_by_id(order_id)
            user_id = order.get("user_id")

            if user_id == order_data.get("user_id"):
                raise HTTPException(status_code=400, detail=f"User {order_data.get('user_id')} is trying to process their own order {order_id}")

            update_data = {
                "status": order_data.get("new_status"),
                "scheduled_date": order_data.get("scheduled_date"),
            }
            update_data = {k: v for k, v in update_data.items() if v is not None}

            if update_data:
                await self.update_order(order_id, update_data)

            check_data = await self.order_management_repository.process_order(order_id)
            if check_data.get("status") == "COMPLETED":
                return {"message": f"Order {order_id} marked as COMPLETED"}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing order update for order ID {order_id}: {str(e)}")
