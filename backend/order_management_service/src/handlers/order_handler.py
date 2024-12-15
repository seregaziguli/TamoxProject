import json
from ..core.messaging import get_rabbitmq_connection
from fastapi import HTTPException
from ..services.order_management_service import OrderManagementService

class RabbitMQConsumer:
    def __init__(self, rabbitmq_url: str, queue_name: str, order_management_service: OrderManagementService):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.order_management_service = order_management_service

    async def start(self):
        try:
            connection = await get_rabbitmq_connection(self.rabbitmq_url)
            async with connection:
                channel = await connection.channel()
                queue = await channel.declare_queue(self.queue_name, durable=True)

                async for message in queue:
                    async with message.process():
                        await self.handle_message(message.body.decode())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error starting RabbitMQ consumer: {str(e)}")

    async def handle_message(self, order_info: str) -> None:
        try:
            order_data = json.loads(order_info)
            order_id = order_data.get("order_id")
            
            if not order_id:
                raise HTTPException(status_code=400, detail="Order id not found in message")

            await self.order_management_service.process_order_update(order_id, order_data)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Incorrect format JSON in message: {str(e)}")
        except HTTPException as e:
            raise e  
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while processing order: {str(e)}")
