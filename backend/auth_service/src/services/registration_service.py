from ..models.user import User
from ..repositories.user_repository import UserRepository
from ..api.schemas.user import RegisterUserRequestDTO
from ..core.security import hash_password
from sqlalchemy.exc import IntegrityError

class RegistrationService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, data: RegisterUserRequestDTO):
        existing_user = await self.user_repo.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("User with this email already exists.")
        
        hashed_password = hash_password(data.password)
        new_user = User(
            email=data.email,
            password=hashed_password,
            is_active=True,
        )

        try:
            await self.user_repo.add_user(new_user)
            return new_user
        except IntegrityError as e:
            raise ValueError("Failed to register user.") from e