from sqlalchemy.ext.asyncio import AsyncSession
from ...db.session import async_session_maker
from typing import AsyncGenerator
from fastapi import HTTPException

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session_maker() as session:
            yield session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting async session: {str(e)}")