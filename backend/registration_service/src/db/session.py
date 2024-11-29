from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
import os
from src.core.config import settings
from sqlalchemy import NullPool
from src.config_env import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

if settings().MODE == "TEST":
    DATABASE_URL = f"postgresql+asyncpg://{settings().TEST_DB_USER}:{settings().TEST_DB_PASS}@{settings().TEST_DB_HOST}:{settings().TEST_DB_PORT}/{settings().TEST_DB_NAME}"
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    DATABASE_PARAMS = {}

class Base(DeclarativeBase):
    pass

metadata = Base.metadata

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

