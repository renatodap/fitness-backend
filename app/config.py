"""
Configuration Management Module

Provides centralized, type-safe configuration management for the fitness backend.
Loads settings from environment variables and .env files with validation.
"""

from functools import lru_cache
from typing import Any
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All required fields must be provided via environment variables or .env file.
    Optional fields have sensible defaults.
    """

    # Application Settings
    APP_NAME: str = "Fitness Backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    # CORS can be a comma-separated string from env or list
    CORS_ORIGINS: str = "http://localhost:3000,https://www.sharpened.me,https://sharpened.me"
    ALLOW_ALL_ORIGINS: bool = False  # SECURITY: Set to False in production!

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS into a list."""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        # Split by comma and strip whitespace
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    # Database Settings (Supabase)
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str

    # External Services
    OPENAI_API_KEY: str
    GROQ_API_KEY: str  # Groq API for ultra-fast, ultra-cheap LLM inference
    REDIS_URL: str = "redis://localhost:6379"

    # Celery Settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Authentication
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    # Security
    CRON_SECRET: str
    WEBHOOK_SECRET: str

    # Monitoring
    SENTRY_DSN: str | None = None

    @field_validator("SUPABASE_URL")
    @classmethod
    def validate_supabase_url(cls, v: str) -> str:
        """Validate SUPABASE_URL is a valid URL."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("SUPABASE_URL must start with http:// or https://")
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate LOG_LEVEL is a valid logging level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v_upper

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate ENVIRONMENT is a valid environment name."""
        valid_environments = ["development", "staging", "production", "test"]
        if v not in valid_environments:
            raise ValueError(f"ENVIRONMENT must be one of {valid_environments}")
        return v

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        """
        Override model_dump to mask sensitive values.

        Returns dictionary with sensitive fields redacted for safe logging.
        """
        data = super().model_dump(**kwargs)

        # Mask sensitive fields
        sensitive_fields = [
            "OPENAI_API_KEY",
            "GROQ_API_KEY",
            "JWT_SECRET",
            "CRON_SECRET",
            "WEBHOOK_SECRET",
            "SUPABASE_KEY",
            "SUPABASE_SERVICE_KEY",
        ]

        for field in sensitive_fields:
            if field in data and data[field]:
                data[field] = "***REDACTED***"

        return data

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings singleton.

    Returns cached Settings instance. Use get_settings.cache_clear()
    to reset cache in tests.

    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Global settings instance for convenience
# Only initialize if not in test mode
if not any(arg.endswith('pytest') or 'pytest' in arg for arg in __import__('sys').argv):
    settings = get_settings()
else:
    settings = None  # Will be set by test fixtures