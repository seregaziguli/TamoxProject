from pydantic_settings import BaseSettings
import os
from functools import lru_cache
from typing import Literal

class Settings(BaseSettings):
        
    DB_NAME: str
    DB_PORT: int
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    ACCESS_KEY: str
    SECRET_KEY: str
    ENDPOINT_URL: str
    BUCKET_NAME: str
    RABBITMQ_URL: str
    NOTIFICATION_SERVICE_URL: str
    AUTH_SERVICE_URL: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_DB: str

    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "allow"

@lru_cache()
def settings() -> Settings:
    return Settings()
