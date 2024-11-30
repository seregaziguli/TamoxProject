from fastapi import Header, HTTPException, Depends
import httpx
from src.utils.logger import logger
from src.config_env import AUTH_SERVICE_URL

async def verify_user(access_token: str = Header(...)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/users/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            logger.info(response.status_code)
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=401, detail="Invalid token.")
        except Exception as e:
            logger.error(f"Error verifying user: {str(e)}")
            raise HTTPException(status_code=401, detail=str(e))
        