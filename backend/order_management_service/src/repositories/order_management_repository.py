import httpx
from fastapi import HTTPException

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
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to fetch order with ID {order_id}. HTTP status: {e.response.status_code}"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching order with ID {order_id}: {str(e)}")

    async def update_order(self, order_id: int, order_data: dict) -> None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(f"{self.base_url}/orders/{order_id}", json=order_data)
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to update order with ID {order_id}. HTTP status: {e.response.status_code}"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating order with ID {order_id}: {str(e)}")

    async def process_order(self, order_id: int) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/orders/{order_id}/process")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to process order with ID {order_id}. HTTP status: {e.response.status_code}"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing order with ID {order_id}: {str(e)}")
