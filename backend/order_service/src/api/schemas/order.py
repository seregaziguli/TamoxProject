from sqlalchemy import DateTime
from src.api.schemas.base import BaseResponse
from typing import Optional
from datetime import datetime
from enum import Enum
from src.models.order import OrderAssignmentPolicy

class OrderResponse(BaseResponse):
    id: int
    description: str
    service_type_name: str
    scheduled_date: datetime
    status: str

class OrderRequest(BaseResponse):
    description: str
    service_type_name: str 
    scheduled_date: Optional[datetime] = None
    assignment_policy: Optional[OrderAssignmentPolicy] = OrderAssignmentPolicy.MULTIPLE