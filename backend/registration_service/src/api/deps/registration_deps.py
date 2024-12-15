from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...api.deps.session import get_async_session
from ...repositories.user_repository import UserRepository
from ...services.user_service import UserService
from ...api.deps.auth_service_deps import get_auth_service_client

async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)

async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service_client = Depends(get_auth_service_client)
        ) -> UserService:
    return UserService(user_repository, auth_service_client)