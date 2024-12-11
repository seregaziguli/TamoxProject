from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.order_repository import OrderRepository
from src.services.order_service import OrderService
from src.api.deps.session import get_async_session
from src.utils.user import verify_user
from src.services.s3_service import S3Client
from src.core.conifg import settings
from src.services.messaging_service import MessagingService
from src.services.image_service import ImageService

async def get_order_repository(session: AsyncSession = Depends(get_async_session)) -> OrderRepository:
    return OrderRepository(session)

async def get_current_user(user: dict = Depends(verify_user)) -> dict:
    return user

async def get_s3_client() -> S3Client:
    return S3Client(
    access_key=settings().ACCESS_KEY,
    secret_key=settings().SECRET_KEY,
    endpoint_url=settings().ENDPOINT_URL,
    bucket_name=settings().BUCKET_NAME,
    )

async def get_messaging_service() -> MessagingService:
    return MessagingService(rabbitmq_url=settings().RABBITMQ_URL)

async def get_image_service(s3_client: S3Client = Depends(get_s3_client)) -> ImageService:
    return ImageService(s3_client=s3_client)

async def get_order_service(
        order_repository: OrderRepository = Depends(get_order_repository),
        messaging_service: MessagingService = Depends(get_messaging_service),
        image_service: ImageService = Depends(get_image_service)
        ) -> OrderService:
    return OrderService(order_repository=order_repository, messaging_service=messaging_service, image_service=image_service)