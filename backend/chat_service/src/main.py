from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.socket_manager import create_socket_manager_app
import socketio
from src.utils.logger import logger

app = FastAPI()

logger.info("Socket.IO server is running 1")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='sockets'
)

logger.info("Socket.IO server is running 2")

app.mount("/sockets", sio_app, name="sockets")

