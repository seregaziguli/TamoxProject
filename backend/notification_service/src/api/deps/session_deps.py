from sqlalchemy.ext.asyncio import AsyncSession
from ...db.session import async_session_maker
from typing import AsyncGenerator
from ...utils.logger import logger
from fastapi import HTTPException

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session_maker() as session:
            yield session
    except Exception as e:
        logger.error(f"Error creating async session: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error while creating session")