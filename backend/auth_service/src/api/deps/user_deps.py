from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import oauth2_scheme
from src.models.user import User
from src.db.session import async_session_maker
from typing import AsyncGenerator
from src.services.auth_service import AuthService
from src.repositories.user_repository import UserRepository
from src.services.token_service import TokenService
from src.repositories.token_repository import TokenRepository

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_token_repository(session: AsyncSession = Depends(get_async_session)) -> TokenRepository:
    return TokenRepository(session)

async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)

async def get_token_service(
    session: AsyncSession = Depends(get_async_session),
    token_repo: TokenRepository = Depends(get_token_repository),
    user_repo: UserRepository = Depends(get_user_repository)
) -> TokenService:
    return TokenService(session, token_repo, user_repo)

async def get_auth_service(
    session: AsyncSession = Depends(get_async_session),
    user_repo: UserRepository = Depends(get_user_repository),
    token_service: TokenService = Depends(get_token_service)
) -> AuthService:
    return AuthService(session, user_repo, token_service)

async def get_current_user(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.get_token_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return user




