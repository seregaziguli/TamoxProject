from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user import UserToken
from typing import Optional
from sqlalchemy.orm import joinedload

class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_token(self, user_token: UserToken) -> None:
        self.session.add(user_token)
        await self.session.commit()
    
    async def get_user_token(self, refresh_token: str, access_token: str, user_id: str) -> UserToken:
        stmt = select(UserToken).options(
            joinedload(UserToken.user)
        ).filter(
            UserToken.refresh_token == refresh_token,
            UserToken.access_token == access_token,
            UserToken.user_id == int(user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_token(self, user_token: UserToken) -> None:
        self.session.add(user_token)
        await self.session.commit()
        
    async def get_token_by_user_id(self, user_id: int) -> Optional[UserToken]:
        stmt = select(UserToken).filter(UserToken.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()