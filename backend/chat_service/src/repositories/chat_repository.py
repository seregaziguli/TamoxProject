from sqlalchemy.future import select
from ..models.message import Message
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.logger import logger

class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, from_user_id: int, to_user_id: int, content: str) -> Message:
        message = Message(from_user_id=from_user_id, to_user_id=to_user_id, content=content)
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        logger.info("here repo 1")
        return message
    
    async def get_messages_for_user(self, user_id: int):
        stmt = select(Message).where(Message.to_user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()