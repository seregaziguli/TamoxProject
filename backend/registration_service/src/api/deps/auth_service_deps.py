from src.services.auth_service_client import AuthServiceClient
from src.core.config import settings

async def get_auth_service_client() -> AuthServiceClient:
    return AuthServiceClient(base_url=settings().AUTH_SERVICE_URL)