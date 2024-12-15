import httpx
from fastapi.exceptions import HTTPException
from ..core.config import settings

class ExternalUserService:
    async def get_user_from_registration_service(self, email: str) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{settings().REGISTRATION_SERVICE_URL}/users/{email}")
                if response.status_code == 200:
                    return response.json()
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch user data.")
            except httpx.RequestError as e:
                raise HTTPException(status_code=500, detail=f"Request error: {str(e)}") from e
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=f"Error response from registration service: {e.response.text}") from e
            except Exception as e:
                raise HTTPException(status_code=500, detail="Error communicating with registration service.") from e
