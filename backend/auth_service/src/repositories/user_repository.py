from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user import User
from typing import Optional
from sqlalchemy.orm import joinedload, selectinload

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).options(
            selectinload(User.tokens)
        ).where(User.email == email)
        
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).options(selectinload(User.tokens)).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_user_with_tokens(self, user_id: int) -> Optional[User]:
        stmt = select(User).options(selectinload(User.tokens)).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()