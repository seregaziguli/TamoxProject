from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import Optional
from ..models.user import UserToken
from ..utils.logger import logger


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_token_user_by_access(self, user_token_id: int, user_id: int, access_token: str) -> Optional[UserToken]:
        try:
            stmt = (
                select(UserToken)
                .options(joinedload(UserToken.user))
                .where(
                    UserToken.id == int(user_token_id),
                    UserToken.user_id == int(user_id),
                    UserToken.access_token == str(access_token),
                    UserToken.expires_at > datetime.utcnow()
                )
            )
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting token user by access: {e}", exc_info=True)
            return None

    async def add_token(self, user_token: UserToken) -> None:
        try:
            self.session.add(user_token)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error adding token: {e}", exc_info=True)
            raise

    async def get_user_token(self, refresh_token: str, access_token: str, user_id: str) -> Optional[UserToken]:
        try:
            stmt = select(UserToken).options(joinedload(UserToken.user)).filter(
                UserToken.refresh_token == str(refresh_token),
                UserToken.access_token == str(access_token),
                UserToken.user_id == int(user_id)
            )
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting user token: {e}", exc_info=True)
            return None

    async def update_token(self, user_token: UserToken) -> None:
        try:
            self.session.add(user_token)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating token: {e}", exc_info=True)
            raise

    async def get_token_by_user_id(self, user_id: int) -> Optional[UserToken]:
        try:
            stmt = select(UserToken).filter(UserToken.user_id == user_id)
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting token by user ID: {e}", exc_info=True)
            return None

    async def delete_tokens_by_user_id(self, user_id: int) -> None:
        try:
            stmt = select(UserToken).where(UserToken.user_id == user_id)
            result = await self.session.execute(stmt)
            tokens = result.scalars().all()
            for token in tokens:
                await self.session.delete(token)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error deleting tokens by user ID: {e}", exc_info=True)
            raise
