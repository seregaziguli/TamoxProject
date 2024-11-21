import httpx
import logging

logger = logging.getLogger(__name__)

class OrderManagementRepository:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_order_by_id(self, order_id: int) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/orders/{order_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to fetch order with ID {order_id}. HTTP status: {e.response.status_code}")
            raise
        except Exception as e:
            logging.error(f"Error fetching order with ID {order_id}: {str(e)}")
            raise

    async def update_order(self, order_id: int, order_data: dict) -> None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(f"{self.base_url}/orders/{order_id}", json=order_data)
                response.raise_for_status()
                logger.info(f"Order with id {order_id} updated successfully.")
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to update order with ID {order_id}. HTTP status: {e.response.status_code}")
            raise
        except Exception as e:
            logging.error(f"Error updating order with ID {order_id}: {str(e)}")
            raise