from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import asyncio
from .utils.logger import logger
from .services.order_management_service import OrderManagementService
from .repositories.order_management_repository import OrderManagementRepository
from .handlers.order_handler import RabbitMQConsumer 
from .core.config import settings
from .api.routes.healthcheck import healthcheck_router

order_management_repository = OrderManagementRepository(base_url=settings().ORDER_SERVICE_URL)
order_management_service = OrderManagementService(order_management_repository=order_management_repository)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting lifespan...")
    consumer = RabbitMQConsumer(settings().RABBITMQ_URL, settings().QUEUE_NAME, order_management_service)
    task = asyncio.create_task(consumer.start())
    try:
        yield
    finally:
        logger.info("Cleaning up lifespan...")
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

app.include_router(healthcheck_router)

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    return await order_management_service.get_order_by_id(order_id)

@app.put("/orders/{order_id}")
async def update_order(order_id: int, order_data: dict):
    await order_management_service.update_order(order_id, order_data)
    return {"message": "Order updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)