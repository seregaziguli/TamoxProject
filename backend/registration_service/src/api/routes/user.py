from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.schemas.user import RegisterUserRequest, UserResponse
from src.services.user_service import UserService
from src.db.session import get_async_session

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    try:
        new_user = await user_service.register_user(data)
        return UserResponse(**new_user.to_dict())  
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

