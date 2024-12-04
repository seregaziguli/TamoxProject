import asyncio
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
import os
from src.services.s3_service import s3_client
from src.utils.logger import logger
import base64

redis_async_result = RedisAsyncResultBackend(
    redis_url="redis://redis_app:6379",  # redis://redis_app:6379
)

broker = ListQueueBroker(url="redis://redis_app:6379")

broker = broker.with_result_backend(redis_async_result)

@broker.task
async def upload_image_task(encoded_file_content: str, object_name: str) -> str:
    try:
        file_content = base64.b64decode(encoded_file_content)
        uploaded_object_name = await s3_client.upload_image_bytes(file_content, object_name)
        return uploaded_object_name
    except Exception as e:
        raise e
