from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ...repositories.order_repository import OrderRepository
from ...services.order_service import OrderService
from .session_deps import get_async_session
from ...utils.user import verify_user
from ...services.s3_service import S3Client
from ...core.conifg import settings
from ...services.messaging_service import MessagingService
from ...services.image_service import ImageService

async def get_order_repository(session: AsyncSession = Depends(get_async_session)) -> OrderRepository:
    try:
        return OrderRepository(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing OrderRepository: {str(e)}")

async def get_current_user(user: dict = Depends(verify_user)) -> dict:
    try:
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error verifying user: {str(e)}")

async def get_s3_client() -> S3Client:
    try:
        return S3Client(
            access_key=settings().ACCESS_KEY,
            secret_key=settings().SECRET_KEY,
            endpoint_url=settings().ENDPOINT_URL,
            bucket_name=settings().BUCKET_NAME,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing S3Client: {str(e)}")

async def get_messaging_service() -> MessagingService:
    try:
        return MessagingService(rabbitmq_url=settings().RABBITMQ_URL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing MessagingService: {str(e)}")

async def get_image_service(s3_client: S3Client = Depends(get_s3_client)) -> ImageService:
    try:
        return ImageService(s3_client=s3_client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing ImageService: {str(e)}")

async def get_order_service(
        order_repository: OrderRepository = Depends(get_order_repository),
        messaging_service: MessagingService = Depends(get_messaging_service),
        image_service: ImageService = Depends(get_image_service)
        ) -> OrderService:
    try:
        return OrderService(order_repository=order_repository, messaging_service=messaging_service, image_service=image_service)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing OrderService: {str(e)}")
