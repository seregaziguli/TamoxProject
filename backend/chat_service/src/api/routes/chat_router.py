from fastapi import APIRouter, Depends
from src.utils.logger import logger
from src.api.deps.chat_deps import get_current_user
from src.services.chat_service import ChatService
from src.api.schemas.chat import MessageCreate
from src.socket_manager import sio  
from src.api.deps.chat_deps import get_chat_service

active_connections = {}

@sio.on("connect")
async def connect(sid: str, environ, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    active_connections[user_id] = sid
    logger.info(f"User {user_id} connected with sid {sid}")

@sio.on("send_message")
async def send_message(
    sid: str,
    data: dict,
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        user_id = current_user["id"]
        message_data = MessageCreate(**data)
        
        await chat_service.send_message(user_id, message_data.to_user_id, message_data.content)

        to_user_sid = active_connections.get(message_data.to_user_id)
        if to_user_sid:
            await sio.emit(
                "receive_message",
                {"from_user_id": user_id, "content": message_data.content},
                to=to_user_sid,
            )
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")

@sio.on("disconnect")
async def disconnect(sid: str):
    user_id = next((key for key, value in active_connections.items() if value == sid), None)
    if user_id:
        active_connections.pop(user_id)
    logger.info(f"User {user_id} disconnected")
