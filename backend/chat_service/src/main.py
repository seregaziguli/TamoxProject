from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.socket_manager import create_socket_manager_app

app = FastAPI()

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

sio = create_socket_manager_app(app)
