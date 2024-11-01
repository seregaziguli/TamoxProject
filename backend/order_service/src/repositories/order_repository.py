from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.order import Order
from src.models.order import OrderStatus
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('socketio')

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order_data: dict) -> Order:
        new_order = Order(**order_data)
        self.db.add(new_order)
        await self.db.commit()
        await self.db.refresh(new_order)

        return new_order
    
    async def get_order(self, order_id: int) -> Order:
        return await Order.get_order(self.db, order_id)
    
    async def update_order(self, order_id: int, order_data: dict) -> None:
        stmt = (
            update(Order)
            .where(Order.id == order_id)
            .values(**order_data)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        await self.db.commit()
    
    async def get_user_orders(self, user_id: int) -> List[Order]:
        stmt = select(Order).filter_by(user_id=user_id)
        result = await self.db.execute(stmt)
        orders = result.scalars().all()
        return orders
    
    async def get_all_orders(self) -> List[Order]:
        stmt = select(Order)
        result = await self.db.execute(stmt)
        orders = result.scalars().all()
        
        return orders