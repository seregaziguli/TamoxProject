from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user import User as UserSQLAlchemy

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_phone(self, phone_number: str):
        result = await self.session.execute(
            select(UserSQLAlchemy).where(UserSQLAlchemy.phone_number == phone_number)
        )
        return result.scalars().first()

    async def create_user(self, name: str, email: str, phone_number: str, hashed_password: str):
        new_user = UserSQLAlchemy(
            name=name,
            email=email,
            phone_number=phone_number
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
    
    async def get_all_users(self):
        result = await self.session.execute(select(UserSQLAlchemy))
        return result.scalars().all()