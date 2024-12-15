from ..models.user import User
from ..repositories.user_repository import UserRepository
from ..api.schemas.user import RegisterUserRequestDTO
from ..core.security import hash_password
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class RegistrationService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, data: RegisterUserRequestDTO):
        try:
            existing_user = await self.user_repo.get_user_by_email(data.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="User with this email already exists.")
            
            hashed_password = hash_password(data.password)
            new_user = User(
                email=data.email,
                password=hashed_password,
                is_active=True,
            )

            await self.user_repo.add_user(new_user)
            return new_user

        except IntegrityError as e:
            raise HTTPException(status_code=500, detail="Failed to register user due to a database error.") from e

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail="An unexpected error occurred during user registration.") from e
