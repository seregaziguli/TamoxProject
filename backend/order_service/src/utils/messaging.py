import aio_pika
from aio_pika import Message, Connection
from fastapi import HTTPException

async def get_rabbitmq_connection(rabbitmq_url: str) -> Connection:
    try:
        connection: Connection = await aio_pika.connect_robust(rabbitmq_url)
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while connecting to RabbitMQ: {e}")

async def send_message(message: str, queue_name: str, rabbitmq_url: str) -> None:
    try:
        connection: Connection = await get_rabbitmq_connection(rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(queue_name, durable=True)
            await channel.default_exchange.publish(
                Message(message.encode()),
                routing_key=queue.name
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while sending message: {e}")
