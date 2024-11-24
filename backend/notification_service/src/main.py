from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import asyncio
from src.api.deps.notification_deps import get_notification_service
from src.api.schemas.notification import NotificationResponse
from src.services.notification_service import NotificationService
from src.repositories.notification_repository import NotificationRepository
from src.db.session import async_session_maker
from typing import List
from src.config_env import RABBITMQ_URL
from src.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with async_session_maker() as session:
        repository = NotificationRepository(session)
        service = NotificationService(repository)
        task = asyncio.create_task(service.process_notifications(RABBITMQ_URL))

        try:
            yield
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.get("/notifications/{user_id}", response_model=List[NotificationResponse])
async def get_notifications_by_user_id(
    user_id: int, 
    notification_service: NotificationService = Depends(get_notification_service)
):
    try:
        return await notification_service.get_user_notifications(user_id)
    except Exception as e:
        logger.error(f"Error fetching notifications for user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch notifications")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

