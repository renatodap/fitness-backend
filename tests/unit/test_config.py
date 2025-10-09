"""
Unit tests for Configuration Management

Tests configuration loading, validation, singleton pattern, and security.
"""

import os
import pytest
from pydantic import ValidationError
from app.config import Settings, get_settings


@pytest.fixture
def base_settings():
    """Provide minimal valid settings for testing."""
    return {
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_KEY": "test-anon-key",
        "SUPABASE_SERVICE_KEY": "test-service-key",
        "OPENAI_API_KEY": "sk-test-key",
        "JWT_SECRET": "test-jwt-secret",
        "CRON_SECRET": "test-cron-secret",
        "WEBHOOK_SECRET": "test-webhook-secret",
    }


@pytest.fixture
def test_settings(base_settings):
    """Provide Settings instance for testing."""
    return Settings(**base_settings)


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Clean environment variables before each test."""
    # Remove all relevant env vars
    for key in list(os.environ.keys()):
        if key.startswith(
            (
                "SUPABASE_",
                "OPENAI_",
                "JWT_",
                "CRON_",
                "WEBHOOK_",
                "REDIS_",
                "CELERY_",
                "APP_",
                "ENVIRONMENT",
                "DEBUG",
                "LOG_",
                "API_",
                "CORS_",
                "SENTRY_",
            )
        ):
            monkeypatch.delenv(key, raising=False)

    # Clear settings cache
    get_settings.cache_clear()

    yield

    # Clean up after test
    get_settings.cache_clear()


# TC-CONFIG-001: Load Configuration from Environment Variables
def test_load_from_environment(monkeypatch):
    """Verify settings can be loaded from environment variables."""
    monkeypatch.setenv("SUPABASE_URL", "https://test.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "test-anon-key")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "test-service-key")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("JWT_SECRET", "test-jwt-secret")
    monkeypatch.setenv("CRON_SECRET", "test-cron-secret")
    monkeypatch.setenv("WEBHOOK_SECRET", "test-webhook-secret")

    settings = Settings()

    assert settings.SUPABASE_URL == "https://test.supabase.co"
    assert settings.SUPABASE_KEY == "test-anon-key"
    assert settings.SUPABASE_SERVICE_KEY == "test-service-key"
    assert settings.OPENAI_API_KEY == "sk-test-key"
    assert settings.JWT_SECRET == "test-jwt-secret"
    assert settings.CRON_SECRET == "test-cron-secret"
    assert settings.WEBHOOK_SECRET == "test-webhook-secret"


# TC-CONFIG-002: Load Configuration with Default Values
def test_default_values(base_settings):
    """Verify default values are applied when not specified."""
    settings = Settings(**base_settings)

    assert settings.APP_NAME == "Fitness Backend"
    assert settings.ENVIRONMENT == "development"
    assert settings.DEBUG is False
    assert settings.LOG_LEVEL == "INFO"
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.REDIS_URL == "redis://localhost:6379"
    assert settings.CELERY_BROKER_URL == "redis://localhost:6379/0"
    assert settings.CELERY_RESULT_BACKEND == "redis://localhost:6379/0"
    assert settings.JWT_ALGORITHM == "HS256"
    # CORS_ORIGINS is a string by default, can be parsed to list via cors_origins_list property
    assert isinstance(settings.CORS_ORIGINS, str)


# TC-CONFIG-003: Load Configuration from .env File
def test_load_from_env_file(tmp_path):
    """Verify settings can be loaded from .env file."""
    env_file = tmp_path / ".env.test"
    env_file.write_text(
        """SUPABASE_URL=https://testfile.supabase.co
SUPABASE_KEY=file-anon-key
SUPABASE_SERVICE_KEY=file-service-key
OPENAI_API_KEY=sk-file-key
JWT_SECRET=file-jwt-secret
CRON_SECRET=file-cron-secret
WEBHOOK_SECRET=file-webhook-secret
ENVIRONMENT=test
DEBUG=true
LOG_LEVEL=DEBUG
"""
    )

    settings = Settings(_env_file=str(env_file))

    assert settings.SUPABASE_URL == "https://testfile.supabase.co"
    assert settings.SUPABASE_KEY == "file-anon-key"
    assert settings.ENVIRONMENT == "test"
    assert settings.DEBUG is True
    assert settings.LOG_LEVEL == "DEBUG"


# TC-CONFIG-004: Missing Required Field Validation
def test_missing_required_field():
    """Verify validation error when required field is missing."""
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            # Missing SUPABASE_URL
            SUPABASE_KEY="test-key",
            SUPABASE_SERVICE_KEY="test-service-key",
            OPENAI_API_KEY="test-openai",
            JWT_SECRET="test-jwt",
            CRON_SECRET="test-cron",
            WEBHOOK_SECRET="test-webhook",
        )

    error_str = str(exc_info.value)
    assert "SUPABASE_URL" in error_str or "supabase_url" in error_str


# TC-CONFIG-005: Invalid URL Format Validation
def test_invalid_url_format():
    """Verify validation error for invalid URL format."""
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            SUPABASE_URL="not-a-valid-url",
            SUPABASE_KEY="test-key",
            SUPABASE_SERVICE_KEY="test-service-key",
            OPENAI_API_KEY="test-openai",
            JWT_SECRET="test-jwt",
            CRON_SECRET="test-cron",
            WEBHOOK_SECRET="test-webhook",
        )

    error_str = str(exc_info.value)
    assert "SUPABASE_URL" in error_str or "http" in error_str.lower()


# TC-CONFIG-006: Invalid Log Level Validation
def test_invalid_log_level():
    """Verify validation error for invalid log level."""
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            LOG_LEVEL="INVALID_LEVEL",
            SUPABASE_URL="https://test.supabase.co",
            SUPABASE_KEY="test-key",
            SUPABASE_SERVICE_KEY="test-service-key",
            OPENAI_API_KEY="test-openai",
            JWT_SECRET="test-jwt",
            CRON_SECRET="test-cron",
            WEBHOOK_SECRET="test-webhook",
        )

    error_str = str(exc_info.value)
    assert "LOG_LEVEL" in error_str or "log_level" in error_str


# TC-CONFIG-007: Valid Environments Validation
@pytest.mark.parametrize("env", ["development", "staging", "production", "test"])
def test_valid_environments(env, base_settings):
    """Verify only valid environments are accepted."""
    settings = Settings(**base_settings, ENVIRONMENT=env)
    assert settings.ENVIRONMENT == env


def test_invalid_environment(base_settings):
    """Verify invalid environment is rejected."""
    with pytest.raises(ValidationError) as exc_info:
        Settings(**base_settings, ENVIRONMENT="invalid-env")

    error_str = str(exc_info.value)
    assert "ENVIRONMENT" in error_str or "environment" in error_str


# TC-CONFIG-008: Singleton Pattern Verification
def test_singleton_pattern(monkeypatch):
    """Verify get_settings() returns same instance."""
    monkeypatch.setenv("SUPABASE_URL", "https://test.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "test-key")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "test-service-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    monkeypatch.setenv("CRON_SECRET", "test-cron")
    monkeypatch.setenv("WEBHOOK_SECRET", "test-webhook")

    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2
    assert id(settings1) == id(settings2)


# TC-CONFIG-009: Singleton Cache Clearing
def test_clear_singleton_cache(monkeypatch):
    """Verify singleton cache can be cleared for testing."""
    monkeypatch.setenv("SUPABASE_URL", "https://test.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "test-key")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "test-service-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    monkeypatch.setenv("CRON_SECRET", "test-cron")
    monkeypatch.setenv("WEBHOOK_SECRET", "test-webhook")

    settings1 = get_settings()

    # Clear cache
    get_settings.cache_clear()

    settings2 = get_settings()

    # After cache clear, new instance may be created
    assert settings2 is not None
    # Values should still be the same
    assert settings1.SUPABASE_URL == settings2.SUPABASE_URL


# TC-CONFIG-010: Sensitive Values Masked
def test_sensitive_values_masked(base_settings):
    """Verify sensitive values are masked in model_dump()."""
    settings = Settings(
        **base_settings,
        OPENAI_API_KEY="sk-secret-key-12345",
        JWT_SECRET="jwt-secret-67890",
    )

    settings_dict = settings.model_dump()

    # Sensitive fields should be masked
    assert settings_dict["OPENAI_API_KEY"] == "***REDACTED***"
    assert settings_dict["JWT_SECRET"] == "***REDACTED***"
    assert settings_dict["CRON_SECRET"] == "***REDACTED***"
    assert settings_dict["WEBHOOK_SECRET"] == "***REDACTED***"
    assert settings_dict["SUPABASE_KEY"] == "***REDACTED***"
    assert settings_dict["SUPABASE_SERVICE_KEY"] == "***REDACTED***"


# TC-CONFIG-011: No Secrets in String Representation
def test_no_secrets_in_string(base_settings):
    """Verify secrets not in __str__ or __repr__."""
    settings = Settings(
        **base_settings,
        OPENAI_API_KEY="sk-secret-key-12345",
        JWT_SECRET="jwt-secret-67890",
    )

    settings_str = str(settings)
    settings_repr = repr(settings)

    # Note: Pydantic may include field names but not values
    # We just ensure the actual secret values aren't there
    assert "sk-secret-key-12345" not in settings_str
    assert "jwt-secret-67890" not in settings_str
    assert "sk-secret-key-12345" not in settings_repr
    assert "jwt-secret-67890" not in settings_repr


# TC-CONFIG-012: FastAPI Dependency Injection
def test_fastapi_dependency_injection():
    """Verify settings work with FastAPI dependency injection."""
    from fastapi import Depends, FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    @app.get("/config-test")
    def config_test(settings: Settings = Depends(get_settings)):
        return {"app_name": settings.APP_NAME, "environment": settings.ENVIRONMENT}

    client = TestClient(app)
    response = client.get("/config-test")

    assert response.status_code == 200
    data = response.json()
    assert "app_name" in data
    assert "environment" in data
    assert data["app_name"] == "Fitness Backend"


# TC-CONFIG-013: Configuration Access in Services
def test_settings_in_service():
    """Verify settings can be accessed in service classes."""
    from app.config import get_settings

    class TestService:
        def __init__(self):
            settings = get_settings()
            self.api_prefix = settings.API_V1_PREFIX

        def get_endpoint(self, path: str) -> str:
            return f"{self.api_prefix}{path}"

    service = TestService()
    endpoint = service.get_endpoint("/users")
    assert endpoint == "/api/v1/users"


# TC-CONFIG-014: Empty String vs None
def test_empty_string_vs_none(base_settings):
    """Verify proper handling of empty strings vs None."""
    settings = Settings(**base_settings, SENTRY_DSN="")

    # Empty string should be preserved or converted to None
    assert settings.SENTRY_DSN == "" or settings.SENTRY_DSN is None


# TC-CONFIG-015: Boolean String Parsing
def test_boolean_string_parsing(base_settings):
    """Verify boolean values parsed correctly from strings."""
    settings = Settings(**base_settings, DEBUG="true")

    assert settings.DEBUG is True
    assert isinstance(settings.DEBUG, bool)

    settings2 = Settings(**base_settings, DEBUG="false")
    assert settings2.DEBUG is False


# TC-CONFIG-016: List Parsing from String
def test_list_parsing(base_settings):
    """Verify list values parsed correctly from strings."""
    origins = "http://localhost:3000,https://app.example.com"
    settings = Settings(**base_settings, CORS_ORIGINS=origins)

    # CORS_ORIGINS is stored as string, parsed via cors_origins_list property
    assert isinstance(settings.CORS_ORIGINS, str)
    origins_list = settings.cors_origins_list
    assert isinstance(origins_list, list)
    assert len(origins_list) == 2
    assert "http://localhost:3000" in origins_list
    assert "https://app.example.com" in origins_list


# Additional test: Log level case insensitive
def test_log_level_case_insensitive(base_settings):
    """Verify LOG_LEVEL is case insensitive."""
    settings = Settings(**base_settings, LOG_LEVEL="debug")
    assert settings.LOG_LEVEL == "DEBUG"

    settings2 = Settings(**base_settings, LOG_LEVEL="InFo")
    assert settings2.LOG_LEVEL == "INFO"


# Additional test: Override defaults
def test_override_defaults(base_settings):
    """Verify default values can be overridden."""
    settings = Settings(
        **base_settings,
        APP_NAME="Custom App",
        API_V1_PREFIX="/api/v2",
        REDIS_URL="redis://custom:6379",
    )

    assert settings.APP_NAME == "Custom App"
    assert settings.API_V1_PREFIX == "/api/v2"
    assert settings.REDIS_URL == "redis://custom:6379"


# Additional test: Multiple URL formats accepted
@pytest.mark.parametrize(
    "url",
    [
        "http://localhost:54321",
        "https://test.supabase.co",
        "https://test.supabase.co/",
        "http://192.168.1.1:8080",
    ],
)
def test_valid_url_formats(url, base_settings):
    """Verify various valid URL formats are accepted."""
    settings = Settings(**base_settings, SUPABASE_URL=url)
    assert settings.SUPABASE_URL == url