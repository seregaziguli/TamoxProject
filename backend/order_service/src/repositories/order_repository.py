from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.order import Order
from typing import List
from ..models.order import OrderAssignment
from ..models.order import OrderAssignmentStatus
from fastapi.exceptions import HTTPException

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def create_order(self, order_data: dict) -> Order:
        try:
            new_order = Order(**order_data)
            self.db.add(new_order)
            await self.db.commit()
            await self.db.refresh(new_order)
            return new_order
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")
    
    async def delete_order(self, order_id: int) -> None:
        try:
            stmt = delete(Order).where(Order.id == order_id)
            await self.db.execute(stmt)
            await self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting order: {str(e)}")

    async def get_order_by_id(self, order_id: int) -> Order:
        try:
            stmt = select(Order).where(Order.id == order_id)
            result = await self.db.execute(stmt)
            order = result.scalar_one_or_none()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found.")
            return order
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving order by ID: {str(e)}")
    
    async def update_order(self, order_id: int, order_data: dict) -> None:
        try:
            stmt = (
                update(Order)
                .where(Order.id == order_id)
                .values(**order_data)
                .execution_options(synchronize_session="fetch")
            )
            await self.db.execute(stmt)
            await self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating order: {str(e)}")

    async def create_assignment(self, assignment_data: dict) -> OrderAssignment:
        try:
            new_assignment = OrderAssignment(**assignment_data)
            self.db.add(new_assignment)
            await self.db.commit()
            await self.db.refresh(new_assignment)
            return new_assignment
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating assignment: {str(e)}")

    async def get_assignment_for_order(self, order_id: int) -> OrderAssignment:
        try:
            stmt = select(OrderAssignment).where(OrderAssignment.order_id == order_id)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving assignment for order: {str(e)}")
    
    async def get_assignments_for_order(self, order_id: int) -> List[OrderAssignment]:
        try:
            stmt = select(OrderAssignment).where(OrderAssignment.order_id == order_id)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving assignments for order: {str(e)}")
    
    async def get_user_orders(self, user_id: int) -> List[Order]:
        try:
            stmt = select(Order).filter_by(user_id=user_id)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving user orders: {str(e)}")
    
    async def get_all_orders(self) -> List[Order]:
        try:
            stmt = select(Order)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving all orders: {str(e)}")
    
    async def complete_assignment(self, assignment_id: int) -> None:
        try:
            stmt = (
                update(OrderAssignment)
                .where(OrderAssignment.id == assignment_id)
                .values(status=OrderAssignmentStatus.COMPLETED)
            )
            await self.db.execute(stmt)
            await self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error completing assignment: {str(e)}")
