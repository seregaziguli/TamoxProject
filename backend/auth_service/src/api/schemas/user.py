from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Union, Dict, Any, List
from src.api.schemas.base import BaseResponse
from src.api.schemas.token import UserTokenDTO

class LoginResponseDTO(BaseResponse):
    access_token: str
    refresh_token: str
    expires_at: Any
    token_type: str = "Bearer"

    class Config:
        orm_mode = True
    
class RegisterUserRequestDTO(BaseResponse):
    name: str
    email: EmailStr
    password: str
    phone_number: str

    class Config:
        orm_mode = True
    
class RegisterUserResponseDTO(BaseResponse):
    id: int
    name: str
    email: EmailStr
    phone_number: str

    class Config:
        orm_mode = True
    
class UserBase(BaseResponse):
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True
    
class User(UserBase):
    id: int
    is_active: bool
    tokens: List[UserTokenDTO]

    class Config:
        orm_mode = True