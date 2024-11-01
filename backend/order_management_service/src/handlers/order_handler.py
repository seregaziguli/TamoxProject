import json
import logging
import httpx
from src.core.messaging import get_rabbitmq_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_order_message(order_info: str) -> None:
    try:
        order_data = json.loads(order_info)
        order_id = order_data.get("order_id")
        new_status = order_data.get("new_status")
        assigned_provider = order_data.get("assigned_provider")
        new_scheduled_date = order_data.get("scheduled_date")

        if not order_id:
            logger.error("Order id not found in message. Message: %s", order_data)
            return
      
        async with httpx.AsyncClient() as client:
            update_data = {
                "status": new_status,
                "assigned_provider": assigned_provider,
                "scheduled_date": new_scheduled_date
            }
            update_data = {k: v for k, v in update_data.items() if v is not None}  

            if update_data:
                response = await client.put(f"http://order_service:8002/orders/{order_id}", json=update_data)
                if response.status_code == 200:
                    logger.info("Order update with ID %s completed successfully.", order_id)
                else:
                    logger.error("Failed to update order with ID %s. Response status: %s", order_id, response.status_code)

    except json.JSONDecodeError:
        logger.error("Incorrect format JSON: %s", order_info)
    except Exception as e:
        logger.error(f"Error while parsing order: {str(e)}, {order_info}")

class RabbitMQConsumer:
    def __init__(self, rabbitmq_url: str, queue_name: str):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name

    async def start(self):
        connection = await get_rabbitmq_connection(self.rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.queue_name, durable=True)

            async for message in queue:
                async with message.process():
                    await handle_order_message(message.body.decode())