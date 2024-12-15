from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from sqlalchemy.orm import selectinload
from ..models.user import User
from ..utils.logger import logger

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            stmt = select(User).options(selectinload(User.tokens)).where(User.email == email)
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting user by email: {e}", exc_info=True)
            return None

    async def get_user_with_tokens(self, user_id: int) -> Optional[User]:
        try:
            stmt = select(User).options(selectinload(User.tokens)).where(User.id == int(user_id))
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting user with tokens by ID: {e}", exc_info=True)
            return None

    async def add_user(self, user: User) -> None:
        try:
            self.session.add(user)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error adding user: {e}", exc_info=True)
            raise
