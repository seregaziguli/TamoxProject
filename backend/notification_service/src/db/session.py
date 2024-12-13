from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from ..core.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings().POSTGRES_USER}:{settings().POSTGRES_PASS}@{settings().POSTGRES_HOST}:{settings().POSTGRES_PORT}/{settings().POSTGRES_DB}"

class Base(DeclarativeBase):
    pass

metadata = Base.metadata

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
