from datetime import datetime
from src.api.schemas.base import BaseResponse
from typing import Any

class UserToken(BaseResponse):
    id: int
    access_token: str
    refresh_token: str
    expires_at: Any
    
class TokenResponse(BaseResponse):
    access_token: str
    refresh_token: str
    expires_at: Any

class UserTokenPydantic(BaseResponse):
    id: int
    access_token: str
    refresh_token: str
    expires_at: datetime

    class Config:
        orm_mode = True