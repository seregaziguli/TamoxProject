from sqlalchemy.ext.asyncio import AsyncSession
from ..models.notification import Notification
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import List
from fastapi import HTTPException

class NotificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notification(self, notification_data: dict) -> Notification:
        try:
            notification = Notification(**notification_data)
            self.db.add(notification)
            await self.db.commit()
            await self.db.refresh(notification)
            return notification
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating notification: {str(e)}")

    async def get_user_notifications(self, user_id: int) -> List[Notification]:
        try:
            stmt = (
                select(Notification)
                .where(or_(Notification.creator_id == user_id, Notification.executor_id == user_id))
                .order_by(Notification.created_at.desc())
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching notifications for user_id={user_id}: {str(e)}")
