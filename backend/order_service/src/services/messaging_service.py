from ..utils.messaging import get_rabbitmq_connection
from aio_pika import Message
from fastapi import HTTPException

class MessagingService:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url

    async def send_message(self, message: str, queue_name: str) -> None:
        try:
            connection = await get_rabbitmq_connection(self.rabbitmq_url)
            async with connection:
                channel = await connection.channel()
                await channel.default_exchange.publish(
                    Message(message.encode()),
                    routing_key=queue_name,
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error sending message: {str(e)}")
