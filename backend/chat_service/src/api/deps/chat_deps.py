from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps.session import get_async_session
from src.repositories.chat_repository import ChatRepository
from src.services.chat_service import ChatService
from fastapi import Depends
from src.utils.logger import logger
from src.utils.user import verify_user
from fastapi import WebSocket, Depends, HTTPException
from src.services.chat_service import ChatService
from urllib.parse import urlparse, parse_qs

async def get_current_user(user: dict = Depends(verify_user)) -> dict:
    return user

async def get_chat_repository(session: AsyncSession = Depends(get_async_session)) -> ChatRepository:
    return ChatRepository(session)

async def get_chat_service(chat_repository: ChatRepository = Depends(get_chat_repository)) -> ChatService:
    return ChatService(chat_repository=chat_repository)

async def get_access_token_from_url(websocket: WebSocket) -> str:
    url = websocket.url
    url = urlparse(str(websocket.url))
    query_params = parse_qs(url.query)

    token = query_params.get("access_token", [None])[0]
    logger.info(f"url: {url}; query params: {query_params}; token: {token}")
    logger.info(f"just here")
    if not token:
        raise HTTPException(status_code=401, detail="Authorization token missing")
    return token

async def get_access_token_from_headers(websocket: WebSocket) -> str:
    token = websocket.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token missing")
    return token.split("Bearer ")[1]
