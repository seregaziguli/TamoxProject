from fastapi import HTTPException
import httpx

class AuthServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def create_user(self, user_data: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/users", json=user_data)

                if response.status_code != 201:
                    raise HTTPException(status_code=response.status_code, detail="Failed to create account")
                
                return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error during request to auth service: {str(exc)}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}")
