from .base import BaseResponse
from datetime import datetime

class MessageCreate(BaseResponse):
    to_user_id: int
    content: str

class MessageResponseDTO(BaseResponse):
    id: int
    from_user_id: int
    to_user_id: int
    edited_at: datetime

    class Config:
        orm_mode = True