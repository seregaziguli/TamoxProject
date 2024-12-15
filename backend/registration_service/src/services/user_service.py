from fastapi import HTTPException
from ..repositories.user_repository import UserRepository
from ..api.schemas.user import RegisterUserRequestDTO
from ..core.security import hash_password
from ..services.auth_service_client import AuthServiceClient

class UserService:
    def __init__(self, user_repository: UserRepository, auth_service_client: AuthServiceClient):
        self.user_repository = user_repository
        self.auth_service_client = auth_service_client

    async def register_user(self, data: RegisterUserRequestDTO):
        try:
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

            await self.auth_service_client.create_user({
                "name": data.name,
                "email": data.email,
                "password": data.password,
                "phone_number": data.phone_number
            })

            return new_user
        except HTTPException as http_exc:
            raise http_exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}")
    
    async def get_all_users(self):
        try:
            return await self.user_repository.get_all_users()
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve users: {str(exc)}")
