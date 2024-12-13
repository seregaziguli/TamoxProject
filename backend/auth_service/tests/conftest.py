import asyncio
from src.db.session import Base, async_session_maker, engine
from src.core.config import settings
from src.models.user import User, UserToken
import json
from sqlalchemy import insert
import pytest
import os
from datetime import datetime

from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.main import app as fastapi_app

@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings().MODE == "TEST"
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)
    
    users = open_mock_json("users")
    user_tokens = open_mock_json("user_tokens")
    
    for user_token in user_tokens:
        user_token["expires_at"] = datetime.strptime(user_token["expires_at"], "%Y-%m-%dT%H:%M:%S")
    
    async with async_session_maker() as session:
        add_users = insert(User).values(users)
        add_user_tokens = insert(UserToken).values(user_tokens)
        
        await session.execute(add_users)
        await session.execute(add_user_tokens)
        
        await session.commit()
        
        
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    

@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
        

@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session