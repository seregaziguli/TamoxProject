from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from src.db.session import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
import enum

class OrderStatus(enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW, nullable=False)
    assigned_provider_id = Column(Integer, nullable=True)
    service_type_name = Column(String, nullable=True)

    @classmethod
    async def get_order(cls, session: AsyncSession, order_id: int):
        query = select(cls).where(cls.id == order_id)
        result = await session.execute(query)
        return result.scalars().first()