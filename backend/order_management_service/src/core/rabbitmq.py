import asyncio
from src.handlers.order_handler import handle_order_message
from src.config_env import RABBITMQ_URL, QUEUE_NAME
from aio_pika import connect, IncomingMessage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_message(message: IncomingMessage):
    async with message.process():
        order_info = message.body.decode()
        logging.info(f"Got message: {order_info}")
        await handle_order_message(order_info)

async def consume():
    connection = await connect(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(handle_message)