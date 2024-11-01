import logging
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
import base64
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from src.db.session import get_async_session
from src.core.config import settings
from src.models.user import UserToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user import User
from sqlalchemy import select

logger = logging.getLogger('uvicorn.error')
SPECIAL_CHARACTERS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>']
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
app_settings = settings()

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def is_password_strong_enough(password: str) -> bool:
    """if len(password < 5):
        return False
    
    if not any(char.isupper() for char in password):
        return False
    
    if not any(char.islower() for char in password):
        return False
    
    if not any(char.isdigit() for char in password):
        return False
    
    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False"""
    
    return True


def str_encode(string: str) -> str:
    return base64.b85encode(string.encode('ascii')).decode('ascii')


def str_decode(string: str) -> str:
    return base64.b85decode(string.encode('ascii')).decode('ascii')


def get_token_payload(token: str, secret: str, algo: str):
    try:
        payload = jwt.decode(token, secret, algorithms=algo)
    except Exception as jwt_exec:
        logger.info(f"JWT Error: {str(jwt_exec)}")
        payload = None
    return payload


def generate_token(payload: dict, secret: str, algo: str, expiry: timedelta):
    expire = datetime.utcnow() + expiry
    payload.update({"exp": expire})
    return jwt.encode(payload, secret, algorithm=algo)


async def load_user(email: str, session: AsyncSession) -> User | None:
    try:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
    except Exception as user_exec:
        logger.info(f"Error loading user: {user_exec}; Email: {email}")
        user = None
    return user

async def get_token_user(token: str, session: AsyncSession):
    payload = get_token_payload(token, app_settings.JWT_SECRET, app_settings.JWT_ALGORITHM)
    if payload:
        try:
            user_token_id = str_decode(payload.get('r'))
            user_id = str_decode(payload.get('sub'))
            access_token = payload.get('a')
            stmt = select(UserToken).options(joinedload(UserToken.user)).filter(UserToken.access_token == str(access_token),
                                                                                UserToken.id == int(user_token_id),
                                                                                UserToken.user_id == int(user_id),
                                                                                UserToken.expires_at > datetime.utcnow(),
                                                                                )
            result = await session.execute(stmt)
            user_token = result.scalars().first()
            
            if user_token:
                user_with_tokens = await User.get_user_with_tokens(session, user_token.user_id)
                return user_with_tokens
            
            logger.info(f"Token data - user_token_id: {user_token_id}, user_id: {user_id}, access_token: {access_token}")
            
        except Exception as e:
            logger.error(f"Error decoding token: {e}")
    
    return None
        
async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)) -> User | None:
    logger.info(f"Received token: {token}")
    user = await get_token_user(token=token, session=session)
    if user:
        logger.info(f"Authenticated user: {user.id}")
        return user
    logger.error("Authentication failed: Invalid token.")
    raise HTTPException(status_code=401, detail="Not authorised.")

