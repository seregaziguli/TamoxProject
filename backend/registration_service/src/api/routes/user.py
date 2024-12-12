from fastapi import APIRouter, status, Depends, HTTPException
from src.api.schemas.user import RegisterUserRequestDTO, UserResponseDTO
from src.services.user_service import UserService
from src.api.deps.registration_deps import get_user_service
from typing import List

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponseDTO)
async def register_user(
    data: RegisterUserRequestDTO,
    user_service: UserService = Depends(get_user_service)
):
    try:
        new_user = await user_service.register_user(data)
        return UserResponseDTO(**new_user.to_dict())
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    
@user_router.get("/all", response_model=List[UserResponseDTO]) 
async def get_users(user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_all_users()
    if not users:
        raise HTTPException(status_code=404, detail="No users found.")
    return [UserResponseDTO(**user.to_dict()) for user in users]  

