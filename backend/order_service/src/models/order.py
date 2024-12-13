from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from ..db.session import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
import enum

class OrderStatus(enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class OrderAssignmentStatus(enum.Enum):
    PENDIND = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class OrderAssignment(Base):
    __tablename__ = "order_assignments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    provider_id = Column(Integer, nullable=False)
    status = Column(Enum(OrderAssignmentStatus), default=OrderAssignmentStatus.PENDIND, nullable=False)
    completion_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_confirmed = Column(Boolean, default=False)

    order = relationship("Order", back_populates="assignments")

class OrderAssignmentPolicy(enum.Enum):
    EXCLUSIVE = "EXCLUSIVE"
    MULTIPLE = "MULTIPLE"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    description = Column(Text, nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW, nullable=False, index=True)
    service_type_name = Column(String, nullable=True)
    assignment_policy = Column(Enum(OrderAssignmentPolicy), default=OrderAssignmentPolicy.MULTIPLE, nullable=False, index=True)
    image_url = Column(String, nullable=True)

    assignments = relationship("OrderAssignment", back_populates="order")

    @classmethod
    async def get_order(cls, session: AsyncSession, order_id: int):
        query = select(cls).where(cls.id == order_id)
        result = await session.execute(query)
        return result.scalars().first()