from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Union, Dict, Any, List
from src.api.schemas.base import BaseResponse
from src.api.schemas.token import UserToken

class LoginResponse(BaseResponse):
    access_token: str
    refresh_token: str
    expires_at: Any
    token_type: str = "Bearer"
    
class RegisterUserRequest(BaseResponse):
    name: str
    email: EmailStr
    password: str
    phone_number: str
    
class RegisterUserResponse(BaseResponse):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    # tokens: Dict[str, Any]
    
class UserBase(BaseResponse):
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    
class User(UserBase):
    id: int
    is_active: bool
    tokens: List[UserToken]

    class Config:
        orm_mode = True

class UserTokenPydantic(BaseResponse):
    id: int
    access_token: str
    refresh_token: str
    expires_at: datetime

    class Config:
        orm_mode = True