from fastapi import HTTPException
from src.repositories.user_repository import UserRepository
from src.api.schemas.user import RegisterUserRequest
from src.core.security import hash_password
import httpx
from src.utils.logger import logger
from src.services.auth_service_client import AuthServiceClient

class UserService:
    def __init__(self, user_repository: UserRepository, auth_service_client: AuthServiceClient):
        self.user_repository = user_repository
        self.auth_service_client = auth_service_client

    async def register_user(self, data: RegisterUserRequest):
        existing_user = await self.user_repository.get_user_by_phone(data.phone_number)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this phone number already exists.")
        
        hashed_password = hash_password(data.password)
        new_user = await self.user_repository.create_user(
            name=data.name,
            email=data.email,
            phone_number=data.phone_number,
            hashed_password=hashed_password
        )

        try:
            await self.auth_service_client.create_user({
                "name": data.name,
                "email": data.email,
                "password": data.password,
                "phone_number": data.phone_number
            })

        except Exception as e:
            logger.error(f"Error while creating user: {e}")
            raise HTTPException(status_code=500, detail='Failed to create account')

        return new_user
        
        