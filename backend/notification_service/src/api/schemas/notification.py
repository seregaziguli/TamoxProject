from datetime import datetime
from src.api.schemas.base import BaseResponse

class NotificationResponseDTO(BaseResponse):
    id: int
    user_id: int
    message: str
    created_at: datetime

    class Config:
        orm_mode = True