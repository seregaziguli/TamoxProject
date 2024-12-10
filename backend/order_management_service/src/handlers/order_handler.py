import json
from src.core.messaging import get_rabbitmq_connection
from src.utils.logger import logger
from src.services.order_management_service import OrderManagementService

class RabbitMQConsumer:
    def __init__(self, rabbitmq_url: str, queue_name: str, order_management_service: OrderManagementService):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.order_management_service = order_management_service

    async def start(self):
        connection = await get_rabbitmq_connection(self.rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.queue_name, durable=True)

            async for message in queue:
                async with message.process():
                    await self.handle_message(message.body.decode())

    async def handle_message(self, order_info: str) -> None:
        try:
            order_data = json.loads(order_info)
            order_id = order_data.get("order_id")
            
            if not order_id:
                logger.error("Order id not found in message. Message: %s", order_data)
                return
            
            await self.order_management_service.process_order_update(order_id, order_data)
        except json.JSONDecodeError as e:
            logger.error("Incorrect format JSON in message. Error: %s. Message: %s", e, order_info)
        except Exception as e:
            logger.error(f"Error while processing order: {str(e)}, {order_info}")