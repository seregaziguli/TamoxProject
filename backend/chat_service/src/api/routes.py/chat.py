from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from src.services.chat_service import ChatService
from src.api.deps.chat_deps import get_chat_service, get_current_user
from src.models import MessageCreate
from typing import Dict

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

active_connections = Dict[int, WebSocket]

@chat_router.websocket("/ws/chat")
async def chat_websocket(
    websocket: WebSocket,
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    user_id = current_user["id"]
    await websocket.accept()
    active_connections[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_json()
            message_data = MessageCreate(**data)
            await chat_service.send_message(user_id, message_data.to_user_id, message_data.content)

            if message_data.to_user_id in active_connections:
                await active_connections[message_data.to_user_id].send_json(
                    {"from_user_id": user_id, "content": message_data.content}
                )

    except WebSocketDisconnect:
        active_connections.pop(user_id, None)