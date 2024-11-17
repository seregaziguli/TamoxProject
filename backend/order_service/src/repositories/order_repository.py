from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.order import Order
from typing import List
from src.models.order import OrderAssignment
from src.utils.logger import logger
from src.models.order import OrderAssignmentStatus

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order_data: dict) -> Order:
        new_order = Order(**order_data)
        self.db.add(new_order)
        await self.db.commit()
        await self.db.refresh(new_order)

        logger.info(f"Order created: {new_order}")
        return new_order

    async def get_order_by_id(self, order_id: int) -> Order:
        stmt = select(Order).where(Order.id == order_id)
        result = await self.db.execute(stmt)
        order = result.scalar_one_or_none()
        return order
    
    async def update_order(self, order_id: int, order_data: dict) -> None:
        stmt = (
            update(Order)
            .where(Order.id == order_id)
            .values(**order_data)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def create_assignment(self, assignment_data: dict) -> OrderAssignment:
        new_assignment = OrderAssignment(**assignment_data)
        self.db.add(new_assignment)
        await self.db.commit()
        await self.db.refresh(new_assignment)

        logger.debug(f"Added {new_assignment} to database")

        return new_assignment

    async def get_assignment_for_order(self, order_id: int) -> List[OrderAssignment]:
        stmt = select(OrderAssignment).where(OrderAssignment.order_id == order_id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()
    
    async def get_assignments_for_order(self, order_id: int) -> List[OrderAssignment]:
        stmt = select(OrderAssignment).where(OrderAssignment.order_id == order_id)
        result = await self.db.execute(stmt)

        return result.scalars().all()
    
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
    
    async def complete_assignment(self, assignment_id: int) -> None:
        stmt = (
            update(OrderAssignment)
            .where(OrderAssignment.id == assignment_id)
            .values(status=OrderAssignmentStatus.COMPLETED)
        )
        await self.db.execute(stmt)
        await self.db.commit()