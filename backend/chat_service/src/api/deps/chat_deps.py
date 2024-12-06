from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps.session import get_async_session
from src.repositories.chat_repository import ChatRepository
from src.services.chat_service import ChatService
from fastapi import Depends
from src.utils.user import verify_user

async def get_current_user(user: dict = Depends(verify_user)) -> dict:
    return user

async def get_chat_reporitory(session: AsyncSession = Depends(get_async_session)) -> ChatRepository:
    return ChatRepository(session)

async def get_chat_service(chat_repository: ChatRepository = Depends(get_chat_reporitory)) -> ChatService:
    return ChatService(chat_repository=chat_repository)