from fastapi import Header, HTTPException
import httpx
from ..core.config import settings

async def verify_user(access_token: str = Header(...)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings().AUTH_SERVICE_URL}/users/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=401, detail="Invalid token.")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail="Error connecting to authentication service.")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=response.status_code, detail="Invalid response from authentication service.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occurred while verifying the user.")
