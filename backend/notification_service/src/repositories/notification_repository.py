from sqlalchemy.ext.asyncio import AsyncSession
from src.models.notification import Notification
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import List

class NotificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notification(self, notification_data: dict) -> Notification:
        notification = Notification(**notification_data)
        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification
    
    async def get_user_notifications(self, user_id: int) -> List[Notification]:
        stmt = (
            select(Notification)
            .where(or_(Notification.creator_id == user_id, Notification.executor_id == user_id))
            .order_by(Notification.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()