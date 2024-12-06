from sqlalchemy import Column, Integer, Text, DateTime, func
from src.db.session import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    from_user_id = Column(Integer, nullable=False)
    to_user_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    edited_at = Column(DateTime, server_default=func.now(), nullable=False)