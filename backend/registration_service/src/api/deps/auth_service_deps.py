from ...services.auth_service_client import AuthServiceClient
from ...core.config import settings
from fastapi import HTTPException

async def get_auth_service_client() -> AuthServiceClient:
    try:
        return AuthServiceClient(base_url=settings().AUTH_SERVICE_URL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing AuthServiceClient: {e}")