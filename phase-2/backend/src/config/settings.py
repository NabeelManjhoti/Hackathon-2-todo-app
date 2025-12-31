from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/todo_app")
    db_echo: bool = os.getenv("DB_ECHO", "False").lower() == "true"

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-jwt-signing-key-here")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Application settings
    app_name: str = "Todo API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        env_file = ".env"


# Create a single instance of settings
settings = Settings()