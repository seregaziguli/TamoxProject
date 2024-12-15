from sqlalchemy.ext.asyncio import AsyncSession
from ...api.deps.session import get_async_session
from ...repositories.chat_repository import ChatRepository
from ...services.chat_service import ChatService
from fastapi import Depends
from ...utils.user import verify_user
from fastapi import Depends, HTTPException
from ...services.chat_service import ChatService

async def get_current_user(user: dict = Depends(verify_user)) -> dict:
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated.")
    return user

async def get_chat_repository(session: AsyncSession = Depends(get_async_session)) -> ChatRepository:
    try:
        return ChatRepository(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error initializing chat repository.") from e

async def get_chat_service(chat_repository: ChatRepository = Depends(get_chat_repository)) -> ChatService:
    try:
        return ChatService(chat_repository=chat_repository)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error initializing chat service.") from e
