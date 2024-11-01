from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.user import User, UserToken
from src.api.schemas.token import UserToken as UserTokenPydantic
from src.core.security import hash_password, verify_password, generate_token, get_token_payload, str_encode, str_decode
from src.repositories.user_repository import UserRepository
from src.repositories.token_repository import TokenRepository
from src.core.config import settings
from src.utils.string.string_utils import unique_string
from src.utils.logger import logger

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.token_repo = TokenRepository(session)

    async def authenticate_user(self, email: str, password: str) -> Optional[UserTokenPydantic]:
        logger.info("Authenticating user with email: %s", email)
        user = await self.user_repo.get_user_by_email(email)
        if user and verify_password(password, user.password):
            logger.info("User authenticated successfully: %s", email)
            tokens = await self._generate_tokens(user)
            
            user_token = await self.token_repo.get_token_by_user_id(user.id)
            
            if not user_token:
                logger.error("Token generation failer for user: %s", email)
                raise HTTPException(status_code=400, detail="Token generation failed.")
            
            return UserTokenPydantic(
                id=user_token.id,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                expires_at=user_token.expires_at
            )
        logger.warning("Invalid login attempt for email: %s", email)
        raise HTTPException(status_code=400, detail="Invalid email or password.")
    
    async def refresh_tokens(self, refresh_token: str) -> dict:
        token_payload = get_token_payload(refresh_token, settings().SECRET_KEY, settings().JWT_ALGORITHM)
        if not token_payload:
            raise HTTPException(status_code=400, detail="Invalid refresh token.")
        
        refresh_token = token_payload.get('t')
        access_token = token_payload.get('a')
        user_id = str_decode(token_payload.get('sub'))

        user_token = await self.token_repo.get_user_token(refresh_token, access_token, user_id)
        
        if not user_token or user_token.expires_at <= datetime.utcnow():
            raise HTTPException(status_code=400, detail="Expired or invalid refresh token.")
        
        user_token.expires_at = datetime.utcnow()
        await self.token_repo.update_token(user_token)

        return await self._generate_tokens(user_token.user)

    async def _generate_tokens(self, user: User) -> dict:
        refresh_token = unique_string(100)
        access_token = unique_string(50)

        rt_expires = timedelta(minutes=settings().REFRESH_TOKEN_EXPIRE_MINUTES)
        at_expires = timedelta(minutes=settings().ACCESS_TOKEN_EXPIRE_MINUTES)

        user_token = UserToken(
            user_id=user.id,
            refresh_token=refresh_token,
            access_token=access_token,
            expires_at=datetime.utcnow() + rt_expires,
        )

        await self.token_repo.add_token(user_token)

        access_payload = {
            "sub": str_encode(str(user.id)),
            'a': access_token,
            'r': str_encode(str(user_token.id))
        }
        refresh_payload = {"sub": str_encode(str(user.id)), "t": refresh_token, 'a': access_token}

        access_token = generate_token(access_payload, settings().JWT_SECRET, settings().JWT_ALGORITHM, at_expires)
        refresh_token = generate_token(refresh_payload, settings().SECRET_KEY, settings().JWT_ALGORITHM, rt_expires)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": at_expires.seconds
        }