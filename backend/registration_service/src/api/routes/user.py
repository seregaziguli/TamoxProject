from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.schemas.user import RegisterUserRequest, UserResponse
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
from src.api.deps.auth_service_deps import get_auth_service_client
from src.api.deps.session import get_async_session
from src.api.deps.registration_deps import get_user_service

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    data: RegisterUserRequest,
    user_service: UserService = Depends(get_user_service)
):

    try:
        new_user = await user_service.register_user(data)
        return UserResponse(**new_user.to_dict())
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
