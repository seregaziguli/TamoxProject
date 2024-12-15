from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .session_deps import get_async_session
from ...repositories.user_repository import UserRepository
from ...services.user_service import UserService
from ...api.deps.auth_service_deps import get_auth_service_client

async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    try:
        return UserRepository(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing UserRepository: {e}")

async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service_client = Depends(get_auth_service_client)
        ) -> UserService:
    try:
        return UserService(user_repository, auth_service_client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing UserService: {e}")