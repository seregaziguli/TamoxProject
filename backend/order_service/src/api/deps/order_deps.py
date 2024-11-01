from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.order_repository import OrderRepository
from src.services.order_service import OrderService
from src.db.session import get_async_session
from src.utils.user import verify_user

async def get_order_repository(session: AsyncSession = Depends(get_async_session)) -> OrderRepository:
    return OrderRepository(session)

async def get_order_service(order_repository: OrderRepository = Depends(get_order_repository)) -> OrderService:
    return OrderService(order_repository)

async def get_current_user(user: dict = Depends(verify_user)) -> dict:
    return user
