from ..db.session import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, nullable=False)
    creator_id = Column(Integer, nullable=False)
    executor_id = Column(Integer, nullable=False)
    message = Column(String(255), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)