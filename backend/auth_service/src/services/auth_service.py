from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User
from ..api.schemas.token import UserTokenDTO
from ..core.security import verify_password
from ..repositories.user_repository import UserRepository
from ..services.token_service import TokenService

class AuthService:
    def __init__(
        self, 
        session: AsyncSession,
        user_repo: UserRepository,
        token_service: TokenService,
        ):
        self.session = session
        self.user_repo = user_repo
        self.token_service = token_service

    async def authenticate_user(self, email: str, password: str) -> Optional[UserTokenDTO]:
            user = await self.user_repo.get_user_by_email(email)
            if user and verify_password(password, user.password):
                tokens = await self.token_service.generate_tokens(user)
                user_token = await self.token_service.get_user_token(user.id)
                
                if not user_token:
                    raise HTTPException(status_code=400, detail="Token generation failed.")
                
                return UserTokenDTO(
                    id=user_token.id,
                    access_token=tokens["access_token"],
                    refresh_token=tokens["refresh_token"],
                    expires_at=user_token.expires_at
                )
            
            raise HTTPException(status_code=400, detail="Invalid email or password.")
    
    async def refresh_tokens(self, refresh_token: str) -> dict:
        return await self.token_service.refresh_tokens(refresh_token)

    async def get_token_user(self, token: str) -> Optional[User]:
        return await self.token_service.validate_and_get_user(token)
