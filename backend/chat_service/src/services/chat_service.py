from ...src.repositories.chat_repository import ChatRepository
from fastapi import HTTPException

class ChatService:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    async def send_message(self, from_user_id: int, to_user_id: int, content: str):
        try:
            message = await self.chat_repository.create_message(from_user_id, to_user_id, content)
            return message
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to send message.")

    async def fetch_messages_for_user(self, user_id: int):
        try:
            messages = await self.chat_repository.get_messages_for_user(user_id)
            return messages
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to fetch messages.")
