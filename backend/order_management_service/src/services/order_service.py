from src.repositories.order_repository import OrderRepository

class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def get_order_by_id(self, order_id: int) -> dict:
        return await self.order_repository.get_order_by_id(order_id)

    async def update_order(self, order_id: int, order_data: dict) -> None:
        await self.order_repository.update_order(order_id, order_data)