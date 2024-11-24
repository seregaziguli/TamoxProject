import aio_pika
from aio_pika import Message, Connection


async def get_rabbitmq_connection(rabbitmq_url: str) -> Connection:
    connection: Connection = await aio_pika.connect_robust(rabbitmq_url)
    return connection


async def send_message(queue_name: str, message: str, rabbitmq_url: str) -> None:
    connection = await get_rabbitmq_connection(rabbitmq_url)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            Message(body=message.encode()),
            routing_key=queue_name
        )
