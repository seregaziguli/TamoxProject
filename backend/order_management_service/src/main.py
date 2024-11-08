from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import asyncio
import logging
from src.services.order_service import OrderManagementService
from src.repositories.order_repository import OrderManagementRepository
from src.handlers.order_handler import RabbitMQConsumer 
from src.config_env import RABBITMQ_URL, QUEUE_NAME 
from src.api.routes.healthcheck import healthcheck_router
from src.config_env import ORDER_SERVICE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

order_management_repository = OrderManagementRepository(base_url=ORDER_SERVICE_URL)
order_management_service = OrderManagementService(order_management_repository=order_management_repository)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting lifespan...")

    consumer = RabbitMQConsumer(RABBITMQ_URL, QUEUE_NAME)
    task = asyncio.create_task(consumer.start())
    
    try:
        yield
    finally:
        logger.info("Cleaning up lifespan...")
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8002",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
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