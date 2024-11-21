from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import oauth2_scheme
from src.models.user import User
from src.db.session import async_session_maker
from typing import AsyncGenerator
from src.services.auth_service import AuthService

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_auth_service(session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(session)

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(session)
    user = await auth_service.get_token_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return user


