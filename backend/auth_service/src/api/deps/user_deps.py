from ...utils.logger import logger
from ...services.registration_service import RegistrationService
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.security import oauth2_scheme
from ...services.auth_service import AuthService
from ...repositories.user_repository import UserRepository
from ...services.token_service import TokenService
from ...repositories.token_repository import TokenRepository
from .session_deps import get_async_session

async def get_token_repository(session: AsyncSession = Depends(get_async_session)) -> TokenRepository:
    return TokenRepository(session)

async def get_token_repository(
    session: AsyncSession = Depends(get_async_session)
) -> TokenRepository:
    try:
        return TokenRepository(session)
    except Exception as e:
        logger.error(f"Error initializing TokenRepository: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error in token repository")


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session)
) -> UserRepository:
    try:
        return UserRepository(session)
    except Exception as e:
        logger.error(f"Error initializing UserRepository: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error in user repository")


async def get_token_service(
    token_repo: TokenRepository = Depends(get_token_repository),
    user_repo: UserRepository = Depends(get_user_repository)
) -> TokenService:
    try:
        return TokenService(token_repo, user_repo)
    except Exception as e:
        logger.error(f"Error initializing TokenService: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error in token service")


async def get_auth_service(
    session: AsyncSession = Depends(get_async_session),
    user_repo: UserRepository = Depends(get_user_repository),
    token_service: TokenService = Depends(get_token_service)
) -> AuthService:
    try:
        return AuthService(session, user_repo, token_service)
    except Exception as e:
        logger.error(f"Error initializing AuthService: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error in authentication service")


async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user = await auth_service.get_token_user(token)
        if not user:
            logger.warning("Invalid or expired token provided")
            raise HTTPException(status_code=401, detail="Invalid or expired token.")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error while getting current user")


async def get_registration_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> RegistrationService:
    try:
        return RegistrationService(user_repo=user_repo)
    except Exception as e:
        logger.error(f"Error initializing RegistrationService: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error in registration service")


