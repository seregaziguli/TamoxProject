from fastapi import HTTPException
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from ....src.db.session import async_session_maker

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session_maker() as session:
            yield session
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating database session.") from e