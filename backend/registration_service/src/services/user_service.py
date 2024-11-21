from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.repositories.user_repository import UserRepository
from src.api.schemas.user import RegisterUserRequest
from src.core.security import hash_password
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('socketio')

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)

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
        
        async with httpx.AsyncClient() as client:
            auth_data = {
                "name": data.name,
                "email": data.email,
                "password": data.password,
                "phone_number": data.phone_number
            }
            response = await client.post("http://auth_service:8000/users", json=auth_data)
            logger.info(f"Response from auth service: {response.status_code}")
            
            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail="Failed to create account")
        
        return new_user