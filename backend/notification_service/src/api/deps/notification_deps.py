from sqlalchemy.ext.asyncio import AsyncSession
from .session_deps import get_async_session
from fastapi import Depends
from ...services.notification_service import NotificationService
from ...utils.user import verify_user
from ...repositories.notification_repository import NotificationRepository
from ...utils.logger import logger
from fastapi import HTTPException

async def get_notification_service(
    session: AsyncSession = Depends(get_async_session)
) -> NotificationService:
    try:
        repository = NotificationRepository(session)
        return NotificationService(repository)
    except Exception as e:
        logger.error(f"Error initializing notification service: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not initialize notification service")

async def get_current_user(user: dict = Depends(verify_user)) -> dict:
    try:
        return user
    except Exception as e:
        logger.error(f"Error verifying user: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid user verification")

