from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import asyncio
from fastapi import FastAPI
from src.services.notification_service import NotificationService
from src.repositories.notification_repository import NotificationRepository
from src.db.session import async_session_maker
from src.core.config import settings
from src.api.routes import notification, healthcheck


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with async_session_maker() as session:
        repository = NotificationRepository(session)
        service = NotificationService(repository)
        task = asyncio.create_task(service.process_notifications(settings().RABBITMQ_URL))

        try:
            yield
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

app = FastAPI(lifespan=lifespan)

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

app.include_router(notification.notification_router)
app.include_router(healthcheck.healthcheck_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

