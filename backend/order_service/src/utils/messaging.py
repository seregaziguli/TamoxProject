import aio_pika
from aio_pika import Message, Connection

async def get_rabbitmq_connection(rabbitmq_url: str) -> Connection:
    connection: Connection = await aio_pika.connect_robust(rabbitmq_url)
    return connection

async def send_message(message: str, queue_name: str, rabbitmq_url: str) -> None:
    connection: Connection = await get_rabbitmq_connection(rabbitmq_url)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        await channel.default_exchange.publish(
            Message(message.encode()),
            routing_key=queue.name
        )