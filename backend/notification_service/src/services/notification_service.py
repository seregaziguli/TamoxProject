from ..utils.messaging import get_rabbitmq_connection
from ..repositories.notification_repository import NotificationRepository
from ..models.notification import Notification
from typing import List
from ..api.schemas.notification import NotificationResponseDTO
from fastapi import HTTPException
import json

class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    async def create_notification(self, order_id: int, creator_id: int, executor_id: int, message: str) -> Notification:
        notification_data = {
            "order_id": order_id,
            "creator_id": creator_id,
            "executor_id": executor_id,
            "message": message,
        }
        try:
            return await self.notification_repository.create_notification(notification_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating notification: {str(e)}")

    async def get_user_notifications(self, user_id: int) -> List[NotificationResponseDTO]:
        try:
            notifications = await self.notification_repository.get_user_notifications(user_id)
            return [
                NotificationResponseDTO(
                    id=notification.id,
                    user_id=user_id, 
                    message=notification.message,
                    created_at=notification.created_at
                )
                for notification in notifications
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching notifications for user_id={user_id}: {str(e)}")

    async def process_notifications(self, rabbitmq_url: str):
        try:
            connection = await get_rabbitmq_connection(rabbitmq_url)
            async with connection:
                channel = await connection.channel()
                queue = await channel.declare_queue("notifications", durable=True)

                async for message in queue:
                    async with message.process():
                        try:
                            notification_data = json.loads(message.body)
                            await self.notification_repository.create_notification(notification_data)
                        except Exception as e:
                            raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to RabbitMQ: {str(e)}")
