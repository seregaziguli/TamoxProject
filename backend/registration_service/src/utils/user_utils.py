from src.api.schemas.user import RegisterUserRequest
from src.models.user import User as UserSQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from src.core.security import hash_password
from datetime import datetime
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('socketio')

async def create_user_account(data: RegisterUserRequest, session: AsyncSession):
    existing_user = await session.execute(select(UserSQLAlchemy).where(UserSQLAlchemy.phone_number == data.phone_number))
    existing_user = existing_user.scalars().first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this phone number already exists.")
    
    new_user = UserSQLAlchemy(name=data.name, phone_number=data.phone_number, email=data.email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    async with httpx.AsyncClient() as client:
        auth_data = {
            "name": data.name,
            "email": data.email,
            "password": data.password,
            "phone_number": data.phone_number
        }
        response = await client.post("http://auth_service:8000/users", json=auth_data)
        logging.info(f"response: {response}")
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Failed to create account")
        
    return new_user
