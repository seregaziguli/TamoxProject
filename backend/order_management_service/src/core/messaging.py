import aio_pika
from aio_pika import Message, Connection
from fastapi import HTTPException

async def get_rabbitmq_connection(rabbitmq_url: str) -> Connection:
    try:
        connection: Connection = await aio_pika.connect_robust(rabbitmq_url)
        return connection
    except aio_pika.AMQPError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to RabbitMQ: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while connecting to RabbitMQ: {str(e)}")


async def send_message(queue_name: str, message: str, rabbitmq_url: str) -> None:
    try:
        connection = await get_rabbitmq_connection(rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                Message(body=message.encode()),
                routing_key=queue_name
            )
    except aio_pika.AMQPError as e:
        raise HTTPException(status_code=500, detail=f"Error sending message to RabbitMQ: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while sending message: {str(e)}")
