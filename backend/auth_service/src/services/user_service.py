import httpx
from fastapi.exceptions import HTTPException
from src.core.config import settings

class ExternalUserService:
    async def get_user_from_registration_service(self, email: str) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{settings().REGISTRATION_SERVICE_URL}./users/{email}")
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                raise HTTPException(status_code=500, detail="Error communicating with registration service")