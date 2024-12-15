from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.user import User as UserSQLAlchemy
from fastapi import HTTPException

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_phone(self, phone_number: str):
        try:
            result = await self.session.execute(
                select(UserSQLAlchemy).where(UserSQLAlchemy.phone_number == phone_number)
            )
            return result.scalars().first()
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Error retrieving user by phone: {str(exc)}")

    async def create_user(self, name: str, email: str, phone_number: str, hashed_password: str):
        try:
            new_user = UserSQLAlchemy(
                name=name,
                email=email,
                phone_number=phone_number
            )
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(exc)}")

    async def get_all_users(self):
        try:
            result = await self.session.execute(select(UserSQLAlchemy))
            return result.scalars().all()
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Error retrieving all users: {str(exc)}")
