from sqlalchemy.future import select
from ..models.message import Message
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.logger import logger
from fastapi import HTTPException

class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, from_user_id: int, to_user_id: int, content: str) -> Message:
        try:
            message = Message(from_user_id=from_user_id, to_user_id=to_user_id, content=content)
            self.db.add(message)
            await self.db.commit()
            await self.db.refresh(message)
            logger.info(f"Message created: {message.id}")
            return message
        except Exception as e:
            logger.error(f"Error creating message: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create message.")

    async def get_messages_for_user(self, user_id: int):
        try:
            stmt = select(Message).where(Message.to_user_id == user_id)
            result = await self.db.execute(stmt)
            messages = result.scalars().all()
            logger.info(f"Messages retrieved for user {user_id}: {len(messages)} messages found.")
            return messages
        except Exception as e:
            logger.error(f"Error retrieving messages for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to retrieve messages.")
