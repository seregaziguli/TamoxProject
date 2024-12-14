from ...src.repositories.chat_repository import ChatRepository

class ChatService:
    def __init__(
            self, 
            chat_repository: ChatRepository,
    ):
        self.chat_repository = chat_repository

    async def send_message(self, from_user_id: int, to_user_id: int, content: str):
        return await self.chat_repository.create_message(from_user_id, to_user_id, content)
    
    async def fetch_messages_for_user(self, user_id: int):
        return await self.chat_repository.get_messages_for_user(user_id)