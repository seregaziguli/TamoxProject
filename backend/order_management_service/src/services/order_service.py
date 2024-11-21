from src.repositories.order_repository import OrderManagementRepository

class OrderManagementService:
    def __init__(self, order_management_repository: OrderManagementRepository):
        self.order_management_repository = order_management_repository

    async def get_order_by_id(self, order_id: int) -> dict:
        return await self.order_management_repository.get_order_by_id(order_id)

    async def update_order(self, order_id: int, order_data: dict) -> None:
        await self.order_management_repository.update_order(order_id, order_data)