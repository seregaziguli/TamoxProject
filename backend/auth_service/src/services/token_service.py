from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from ..models.user import User, UserToken
from ..core.security import generate_token, get_token_payload, str_encode, str_decode
from ..repositories.user_repository import UserRepository
from ..repositories.token_repository import TokenRepository
from ..core.config import settings
from ..utils.string_utils import unique_string

class TokenService:
    def __init__(
            self,
            token_repo: TokenRepository,
            user_repo: UserRepository,
            ):
        self.token_repo = token_repo
        self.user_repo = user_repo
    
    async def generate_tokens(self, user: User) -> dict:
        try:
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
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error generating tokens.") from e

    async def refresh_tokens(self, refresh_token: str) -> dict:
        try:
            token_payload = get_token_payload(refresh_token, settings().SECRET_KEY, settings().JWT_ALGORITHM)
            if not token_payload:
                raise HTTPException(status_code=400, detail="Invalid refresh token.")

            user_id = str_decode(token_payload.get('sub'))
            user_token = await self.token_repo.get_user_token(
                token_payload.get('t'),
                token_payload.get('a'),
                user_id,
            )

            if not user_token or user_token.expires_at <= datetime.utcnow():
                raise HTTPException(status_code=400, detail="Expired or invalid refresh token.")

            return await self.generate_tokens(user_token.user)

        except HTTPException:
            raise 

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error refreshing tokens.") from e

    async def validate_and_get_user(self, token: str) -> Optional[User]:
        try:
            payload = get_token_payload(token, settings().JWT_SECRET, settings().JWT_ALGORITHM)
            if not payload:
                return None
            user_id = str_decode(payload.get("sub"))
            return await self.user_repo.get_user_with_tokens(user_id)

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error validating token.") from e
    
    async def get_user_token(self, user_id: int) -> Optional[UserToken]:
        try:
            return await self.token_repo.get_token_by_user_id(user_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error fetching user token.") from e
