from fastapi import APIRouter
from fastapi import Depends, HTTPException
from ...api.deps.notification_deps import get_notification_service
from ...api.schemas.notification import NotificationResponseDTO
from ...services.notification_service import NotificationService
from typing import List
from ...utils.logger import logger

notification_router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    responses={404: {"description": "Not found"}}
)

@notification_router.get("/{user_id}", response_model=List[NotificationResponseDTO])
async def get_notifications_by_user_id(
    user_id: int, 
    notification_service: NotificationService = Depends(get_notification_service)
):
    try:
        return await notification_service.get_user_notifications(user_id)
    except Exception as e:
        logger.error(f"Error fetching notifications for user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch notifications")