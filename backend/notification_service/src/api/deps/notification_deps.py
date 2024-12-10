from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import async_session_maker
from typing import AsyncGenerator
from fastapi import Depends
from src.services.notification_service import NotificationService
from src.utils.user import verify_user
from src.repositories.notification_repository import NotificationRepository

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_notification_service(
    session: AsyncSession = Depends(get_async_session)
) -> NotificationService:
    repository = NotificationRepository(session)
    return NotificationService(repository)

async def get_current_user(user: dict = Depends(verify_user)) -> dict:
    return user