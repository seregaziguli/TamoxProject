from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.core.conifg import settings

DATABASE_URL = f"postgresql+asyncpg://{settings().POSTGRES_USER}:{settings().POSTGRES_PASS}@{settings().POSTGRES_HOST}:{settings().POSTGRES_PORT}/{settings().POSTGRES_DB}"

class Base(DeclarativeBase):
    pass

metadata = Base.metadata

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session