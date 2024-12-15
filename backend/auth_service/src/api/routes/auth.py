from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.exceptions import HTTPException

from ...api.schemas.user import LoginResponseDTO, RegisterUserRequestDTO, RegisterUserResponseDTO, User as UserPydantic
from ...api.deps.user_deps import get_current_user, get_async_session, get_auth_service, get_registration_service
from ...services.registration_service import RegistrationService
from ...models.user import User as UserSQLAlchemy
from ...utils.logger import logger
from ...services.auth_service import AuthService

auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)


@auth_router.post("/login", response_model=LoginResponseDTO)
async def user_login(
    data: OAuth2PasswordRequestForm = Depends(), 
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        logger.info("User login attempt: %s", data.username)
        token = await auth_service.authenticate_user(data.username, data.password)
        if not token:
            logger.warning("Invalid credentials for user: %s", data.username)
            raise HTTPException(status_code=400, detail="Invalid credentials")
        logger.info("User logged in successfully: %s", data.username)
        return token
    except Exception as e:
        logger.error(f"Error during user login: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.post("/refresh", response_model=LoginResponseDTO)
async def refresh_token(
    refresh_token: str = Header(), 
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        logger.info("Refreshing token")
        token = await auth_service.refresh_tokens(refresh_token)
        if not token:
            logger.warning("Invalid or expired refresh token")
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        logger.info("Token refreshed successfully")
        return token
    except Exception as e:
        logger.error(f"Error during token refresh: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.get("/me", response_model=UserPydantic)
async def read_users_me(
    current_user: UserSQLAlchemy = Depends(get_current_user), 
    session: AsyncSession = Depends(get_async_session)
):
    try:
        user_with_tokens = await UserSQLAlchemy.get_user_with_tokens(session, current_user.id)
        if not user_with_tokens:
            logger.warning("User not found: %s", current_user.id)
            raise HTTPException(status_code=404, detail="User not found")
        return user_with_tokens
    except Exception as e:
        logger.error(f"Error fetching user: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.get("/verify-token", response_model=UserPydantic)
async def verify_token(
    access_token: str = Header(...), 
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user = await auth_service.get_token_user(access_token)
        if not user:
            logger.warning("Invalid or expired access token")
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return user
    except Exception as e:
        logger.error(f"Error verifying token: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.post(
    "", 
    status_code=status.HTTP_201_CREATED, 
    response_model=RegisterUserResponseDTO
) # this router accepts a post request from the registration service
async def register_user(
    data: RegisterUserRequestDTO,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    try:
        logger.info("Registering new user: %s", data.email)
        new_user = await registration_service.register_user(data)
        return RegisterUserResponseDTO(
            id=new_user.id,
            name=data.name,
            email=new_user.email,
            phone_number=data.phone_number
        )
    except ValueError as e:
        logger.warning(f"Registration failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
