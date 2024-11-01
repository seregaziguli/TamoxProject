from datetime import datetime
from pydantic import EmailStr
from typing import Optional, Union
from src.api.schemas.base import BaseResponse

class UserResponse(BaseResponse):
    id: int
    email: str
    name: str
    phone_number: str
    created_at: Optional[str]
    
class RegisterUserRequest(BaseResponse):
    name: str
    email: EmailStr
    password: str
    phone_number: str
    
class VerifyUserRequest(BaseResponse):
    token: str
    email: str