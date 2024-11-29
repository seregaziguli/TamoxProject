from src.repositories.order_management_repository import OrderManagementRepository
from src.utils.logger import logger

class OrderManagementService:
    def __init__(self, order_management_repository: OrderManagementRepository):
        self.order_management_repository = order_management_repository

    async def get_order_by_id(self, order_id: int) -> dict:
        return await self.order_management_repository.get_order_by_id(order_id)

    async def update_order(self, order_id: int, order_data: dict) -> None:
        await self.order_management_repository.update_order(order_id, order_data)

    async def process_order_update(self, order_id: int, order_data: dict) -> None:
        order = await self.get_order_by_id(order_id)
        user_id = order.get("user_id")

        if user_id == order_data.get("user_id"):
            logger.error(f"User {order_data.get('user_id')} is trying to process their own order {order_id}")
            return

        update_data = {
            "status": order_data.get("new_status"),
            "scheduled_date": order_data.get("scheduled_date"),
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if update_data:
            await self.update_order(order_id, update_data)
            logger.info(f"Order {order_id} updated successfully with data {update_data}")

        check_data = await self.order_management_repository.process_order(order_id)
        if check_data.get("status") == "COMPLETED":
            logger.info(f"Order {order_id} marked as COMPLETED")
