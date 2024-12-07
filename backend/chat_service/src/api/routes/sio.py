from fastapi import APIRouter, Depends
from src.utils.logger import logger
from src.api.deps.chat_deps import get_current_user
from src.services.chat_service import ChatService
from src.api.schemas.chat import MessageCreate
from src.main import sio_server
from src.api.deps.chat_deps import get_chat_service
from src.utils.user import verify_user
from fastapi import HTTPException
from src.repositories.chat_repository import ChatRepository
from src.api.deps.session import get_async_session

active_connections = {}

def log_active_connections():
    logger.info("Active connections: {}".format(active_connections))
    for user_id, sid in active_connections.items():
        rooms = sio_server.rooms(sid)
        logger.info(f"User {user_id} with SID {sid} is in rooms: {rooms}")

@sio_server.event
async def connect(sid, environ):
    logger.info("a_11")
    access_token = environ["HTTP_AUTHORIZATION"].split(" ")[1] if "HTTP_AUTHORIZATION" in environ else None
    if not access_token:
        logger.error(f"Access token missing for SID {sid}")
        await sio_server.disconnect(sid)
        return
    try:
        current_user = await verify_user(access_token)
        user_id = current_user["id"]
        active_connections[user_id] = sid
        await sio_server.enter_room(sid, str(user_id))
        logger.info(f"User {user_id} connected with sid {sid}")
    except HTTPException as e:
        logger.error(f"Failed to verify user for SID {sid}: {str(e)}")
        await sio_server.disconnect(sid)


@sio_server.event
async def send_message(sid, data):
    logger.info("a_22")
    access_token = None
    if "HTTP_AUTHORIZATION" in sio_server.environ[sid]:
        access_token = sio_server.environ[sid]["HTTP_AUTHORIZATION"].split(" ")[1]
    
    if not access_token:
        logger.error(f"Access token missing for SID {sid}")
        await sio_server.disconnect(sid)
        return

    try:
        current_user = await verify_user(access_token)
        user_id = current_user["id"]
        logger.info(f"User {user_id} is sending a message.")

        try:
            message_data = MessageCreate(**data)
        except Exception as e:
            logger.error(f"Invalid message data: {str(e)}")
            return

        async with get_async_session() as session:
            chat_repository = ChatRepository(session)
            chat_service = ChatService(chat_repository=chat_repository)

            message = await chat_service.send_message(
                from_user_id=user_id,
                to_user_id=message_data.to_user_id,
                content=message_data.content
            )

            logger.info(f"Message saved: {message}")

            to_user_sid = active_connections.get(message_data.to_user_id)
            if to_user_sid:
                await sio_server.emit(
                    "receive_message",
                    {"from_user_id": user_id, "content": message_data.content},
                    room=to_user_sid
                )
                logger.info(f"Message delivered to user {message_data.to_user_id} with SID {to_user_sid}.")
            else:
                logger.info(f"User {message_data.to_user_id} is not connected.")
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")

@sio_server.event
async def disconnect(sid):
    logger.info("a_33")
    user_id = next((key for key, value in active_connections.items() if value == sid), None)
    if user_id:
        active_connections.pop(user_id)
    logger.info(f"User {user_id} disconnected")