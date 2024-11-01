from pydantic_settings import BaseSettings
import os
from functools import lru_cache
from typing import Literal

class Settings(BaseSettings):
    
    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "allow"

@lru_cache()
def settings() -> Settings:
    return Settings()
