from fastapi import HTTPException
import httpx
from src.utils.logger import logger

class AuthServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def create_user(self, user_data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/users", json=user_data)
            logger.info(f"Response from auth service: {response.status_code}")
            
            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail="Failed to create account")
        
            return response.json()
    
