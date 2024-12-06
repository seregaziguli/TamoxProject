from src.repositories.chat_repository import ChatRepository

class ChatService:
    def __init__(
            self, 
            chat_reporitory: ChatRepository,
    ):
        self.chat_reporitory = chat_reporitory

    async def send_message(self, from_user_id: int, to_user_id: int, content: str):
        return await self.chat_reporitory.create_message(from_user_id, to_user_id, content)
    
    async def fetch_messages_for_user(self, user_id: int):
        return await self.chat_reporitory.get_messages_for_user(user_id)