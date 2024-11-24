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
            logger.info("In authenticate_user function.")
            user = await self.user_repo.get_user_by_email(email)
            logger.info("After get_user_by_email function.")
            if user and verify_password(password, user.password):
                logger.info(f"In verify_password function")
                tokens = await self._generate_tokens(user)
                user_token = await self.token_repo.get_token_by_user_id(user.id)
                
                if not user_token:
                    logger.info(f"In if not user_token: condition")
                    raise HTTPException(status_code=400, detail="Token generation failed.")
                
                return UserTokenPydantic(
                    id=user_token.id,
                    access_token=tokens["access_token"],
                    refresh_token=tokens["refresh_token"],
                    expires_at=user_token.expires_at
                )
            logger.info(f"Just here 1")
            raise HTTPException(status_code=400, detail="Invalid email or password.")
    
    async def refresh_tokens(self, refresh_token: str) -> dict:
        logger.info(f"In refresh_tokens function")
        token_payload = get_token_payload(refresh_token, settings().SECRET_KEY, settings().JWT_ALGORITHM)
        if not token_payload:
            logger.info(f"In if not token_payload: condition")
            raise HTTPException(status_code=400, detail="Invalid refresh token.")
        
        refresh_token = token_payload.get('t')
        access_token = token_payload.get('a')
        user_id = str_decode(token_payload.get('sub'))

        user_token = await self.token_repo.get_user_token(refresh_token, access_token, user_id)

        logger.info(f"user_token: {user_token}, refresh_token: {refresh_token}, access_token: {access_token}, user_id: {user_id}")
        
        if not user_token or user_token.expires_at <= datetime.utcnow():
            logger.info(f"In if not user_token or user_token.expires_at <= datetime.utcnow(): condition")
            raise HTTPException(status_code=400, detail="Expired or invalid refresh token.")
        
        user_token.expires_at = datetime.utcnow()
        await self.token_repo.update_token(user_token)
        logger.info(f"Just here 2")
        return await self._generate_tokens(user_token.user)

    async def _generate_tokens(self, user: User) -> dict:
        logger.info(f"In _generate_tokens function")
        
        await self.token_repo.delete_tokens_by_user_id(user.id)

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
        logger.info(f"user_token: {user_token}")
        await self.token_repo.add_token(user_token)

        access_payload = {
            "sub": str_encode(str(user.id)),
            'a': access_token,
            'r': str_encode(str(user_token.id))
        }
        refresh_payload = {"sub": str_encode(str(user.id)), "t": refresh_token, 'a': access_token}

        access_token = generate_token(access_payload, settings().JWT_SECRET, settings().JWT_ALGORITHM, at_expires)
        refresh_token = generate_token(refresh_payload, settings().SECRET_KEY, settings().JWT_ALGORITHM, rt_expires)

        logger.info(f"access_payload: {access_payload} refresh_payload: {refresh_payload} access_token: {access_token} refresh_token: {refresh_token}")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": at_expires.seconds
        }

    
    async def get_token_user(self, token: str):
        logger.info(f"In get_token_user function")
        payload = get_token_payload(token, settings().JWT_SECRET, settings().JWT_ALGORITHM)
        logger.info(f"After payload: {payload}")
        if not payload:
            logger.info(f"In if not payload: condition")
            return None
        
        try:
            user_token_id = str_decode(payload.get('r'))
            user_id = str_decode(payload.get('sub'))
            access_token = payload.get('a')

            user_token = await self.token_repo.get_token_user_by_access(user_token_id, user_id, access_token)
            logger.info(f"user_token_id: {user_token_id} user_id: {user_id} access_token: {access_token} user_token: {user_token}")
            if not user_token:
            #if user_token: # это неправильное условие, должно быть if not user_token
                logger.info(f"In if not user_token: condition")
                return await self.user_repo.get_user_with_tokens(user_token.user_id)
            else:
                logger.info(f"In else: condition")
                return await self.user_repo.get_user_with_tokens(user_token.user_id)
            logger.info(f"Just here 3")
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail=f"Error decoding token: {e}", exc_info=True)
        logger.info(f"Just here 4")
        return None
