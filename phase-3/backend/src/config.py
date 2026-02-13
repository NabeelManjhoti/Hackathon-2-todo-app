"""Configuration management for the application."""

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        """Initialize settings and validate required variables."""
        self.database_url: str = self._get_required_env("DATABASE_URL")
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")

        # JWT Authentication settings
        self.jwt_secret: str = self._get_required_env("JWT_SECRET")
        self.jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_expiry_minutes: int = int(os.getenv("JWT_EXPIRY_MINUTES", "60"))

        # AI Chatbot settings
        self.openai_api_key: str = self._get_required_env("OPENAI_API_KEY")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
        self.chat_timeout_seconds: int = int(os.getenv("CHAT_TIMEOUT_SECONDS", "30"))
        self.max_conversation_history: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "20"))

    def _get_required_env(self, key: str) -> str:
        """Get required environment variable or raise error.

        Args:
            key: Environment variable name

        Returns:
            Environment variable value

        Raises:
            ValueError: If environment variable is not set
        """
        value: Optional[str] = os.getenv(key)
        if value is None:
            raise ValueError(f"Required environment variable {key} is not set")
        return value


# Global settings instance
settings = Settings()
