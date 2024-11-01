from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.user import LoginResponse, RegisterUserRequest, RegisterUserResponse, User as UserPydantic
from src.core.security import get_current_user
from src.db.session import get_async_session
from src.models.user import User as UserSQLAlchemy
from src.services.auth_service import AuthService 
from fastapi.exceptions import HTTPException
from src.core.security import hash_password
from src.utils.logger import logger

auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

async def get_auth_service(session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(session)

@auth_router.post("/login", response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    logger.info("User login attempt for username: %s", data.username)
    token = await auth_service.authenticate_user(data.username, data.password)
    if not token:
        logger.error("Invalid credentials for user: %s", data.usernmae)
        raise HTTPException(status_code=400, detail="Invalid credentials")
    logger.info("User logged in successfully: %s", data.username)
    return token

@auth_router.post("/refresh", response_model=LoginResponse)
async def refresh_token(refresh_token: str = Header(), auth_service: AuthService = Depends(get_auth_service)):
    logger.info("Refreshing token for user with refresh token: %s", refresh_token)
    token = await auth_service.refresh_tokens(refresh_token)
    logger.info("Token refreshed successfully.")
    return token

@auth_router.get("/me", response_model=UserPydantic)
async def read_users_me(current_user: UserSQLAlchemy = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    user_with_tokens = await UserSQLAlchemy.get_user_with_tokens(session, current_user.id)
    return user_with_tokens

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

@auth_router.post("", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse)
async def register_user(data: RegisterUserRequest, session: AsyncSession = Depends(get_async_session), auth_service: AuthService = Depends(get_auth_service)):
    existing_user = await session.execute(select(UserSQLAlchemy).where(UserSQLAlchemy.email == data.email))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    hashed_password = hash_password(data.password)
    new_user = UserSQLAlchemy(email=data.email, password=hashed_password, is_active=True)
    
    session.add(new_user)
    await session.commit()
    
    tokens = await auth_service._generate_tokens(new_user)
    
    return {
        "id": new_user.id,
        "name": data.name,
        "email": new_user.email,
        "phone_number": data.phone_number,
        "tokens": tokens
    }