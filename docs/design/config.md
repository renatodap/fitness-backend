# Feature Design: Configuration Management

## Overview
The Configuration Management feature provides a centralized, type-safe way to manage all application settings, environment variables, and configuration parameters across the fitness backend.

## Purpose
- Load configuration from environment variables
- Provide type-safe access to settings
- Support multiple environments (development, staging, production)
- Validate configuration at startup
- Provide sensible defaults where appropriate
- Prevent runtime errors due to missing or invalid configuration

## Requirements

### Functional Requirements
1. **Load from Environment**: Read configuration from `.env` files and environment variables
2. **Type Safety**: All settings must be strongly typed using Pydantic models
3. **Validation**: Validate all required settings at application startup
4. **Defaults**: Provide sensible defaults for non-critical settings
5. **Singleton Pattern**: Ensure single instance of settings across application
6. **Environment Support**: Support development, staging, and production environments

### Non-Functional Requirements
1. **Performance**: Configuration loading should happen once at startup (< 100ms)
2. **Security**: Sensitive values (API keys, secrets) must not be logged or exposed
3. **Maintainability**: Easy to add new configuration parameters
4. **Testability**: Must be easy to mock/override in tests

## Configuration Categories

### 1. Application Settings
- `APP_NAME`: Application name (default: "Fitness Backend")
- `ENVIRONMENT`: Environment name (development, staging, production)
- `DEBUG`: Debug mode flag (boolean)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### 2. API Settings
- `API_V1_PREFIX`: API version prefix (default: "/api/v1")
- `CORS_ORIGINS`: List of allowed CORS origins

### 3. Database Settings (Supabase)
- `SUPABASE_URL`: Supabase project URL (required)
- `SUPABASE_KEY`: Supabase anon key (required)
- `SUPABASE_SERVICE_KEY`: Supabase service role key (required)

### 4. External Services
- `OPENAI_API_KEY`: OpenAI API key (required)
- `REDIS_URL`: Redis connection URL (default: "redis://localhost:6379")

### 5. Celery Settings
- `CELERY_BROKER_URL`: Celery broker URL (default: "redis://localhost:6379/0")
- `CELERY_RESULT_BACKEND`: Celery result backend URL (default: "redis://localhost:6379/0")

### 6. Authentication
- `JWT_SECRET`: Secret key for JWT verification (required)
- `JWT_ALGORITHM`: JWT algorithm (default: "HS256")

### 7. Security
- `CRON_SECRET`: Secret for cron job authentication (required)
- `WEBHOOK_SECRET`: Secret for webhook authentication (required)

### 8. Monitoring
- `SENTRY_DSN`: Sentry DSN for error tracking (optional)

## Architecture

### Settings Class Hierarchy
```
BaseSettings (pydantic_settings)
    ↓
Settings
    ├── app_settings: AppSettings
    ├── api_settings: ApiSettings
    ├── database_settings: DatabaseSettings
    ├── external_services: ExternalServicesSettings
    ├── celery_settings: CelerySettings
    ├── auth_settings: AuthSettings
    ├── security_settings: SecuritySettings
    └── monitoring_settings: MonitoringSettings
```

### Singleton Pattern
Use `@lru_cache()` decorator to ensure single instance:
```python
@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

## Data Models

### Settings (Main Configuration)
```python
class Settings(BaseSettings):
    # App
    APP_NAME: str = "Fitness Backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Database
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str

    # External Services
    OPENAI_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Auth
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    # Security
    CRON_SECRET: str
    WEBHOOK_SECRET: str

    # Monitoring
    SENTRY_DSN: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True
```

## Usage Examples

### Basic Usage
```python
from app.config import settings

# Access configuration
print(f"Running in {settings.ENVIRONMENT} mode")
print(f"API prefix: {settings.API_V1_PREFIX}")
```

### Dependency Injection (FastAPI)
```python
from fastapi import Depends
from app.config import Settings, get_settings

@app.get("/info")
async def get_info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }
```

### Testing Override
```python
import pytest
from app.config import Settings

@pytest.fixture
def test_settings():
    return Settings(
        ENVIRONMENT="test",
        DEBUG=True,
        SUPABASE_URL="http://test.supabase.co",
        SUPABASE_KEY="test-key",
        SUPABASE_SERVICE_KEY="test-service-key",
        OPENAI_API_KEY="test-openai-key",
        JWT_SECRET="test-jwt-secret",
        CRON_SECRET="test-cron-secret",
        WEBHOOK_SECRET="test-webhook-secret"
    )
```

## Validation Rules

### Required Fields
These fields MUST be present or validation fails:
- SUPABASE_URL
- SUPABASE_KEY
- SUPABASE_SERVICE_KEY
- OPENAI_API_KEY
- JWT_SECRET
- CRON_SECRET
- WEBHOOK_SECRET

### Format Validation
- `SUPABASE_URL`: Must be valid URL starting with http:// or https://
- `CORS_ORIGINS`: Must be valid list of URLs
- `LOG_LEVEL`: Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `ENVIRONMENT`: Must be one of: development, staging, production

### Custom Validators
```python
@validator("SUPABASE_URL")
def validate_supabase_url(cls, v):
    if not v.startswith(("http://", "https://")):
        raise ValueError("SUPABASE_URL must start with http:// or https://")
    return v

@validator("LOG_LEVEL")
def validate_log_level(cls, v):
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if v.upper() not in valid_levels:
        raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
    return v.upper()
```

## Error Handling

### Missing Required Field
```python
# If SUPABASE_URL is missing:
ValidationError: 1 validation error for Settings
SUPABASE_URL
  field required (type=value_error.missing)
```

### Invalid Format
```python
# If SUPABASE_URL is invalid:
ValidationError: 1 validation error for Settings
SUPABASE_URL
  SUPABASE_URL must start with http:// or https:// (type=value_error)
```

## Security Considerations

### 1. Never Log Sensitive Values
```python
# BAD
logger.info(f"Using API key: {settings.OPENAI_API_KEY}")

# GOOD
logger.info("OpenAI API key loaded successfully")
```

### 2. Mask Sensitive Values in Serialization
```python
class Settings(BaseSettings):
    OPENAI_API_KEY: str

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        # Mask sensitive fields
        for key in ["OPENAI_API_KEY", "JWT_SECRET", "CRON_SECRET", "WEBHOOK_SECRET"]:
            if key in data:
                data[key] = "***REDACTED***"
        return data
```

### 3. Environment Variable Precedence
1. Explicit environment variables (highest priority)
2. .env file
3. Default values (lowest priority)

## Testing Strategy

### Unit Tests
1. Test loading configuration from environment variables
2. Test default values
3. Test validation for required fields
4. Test validation for format constraints
5. Test singleton pattern
6. Test configuration override in tests

### Integration Tests
1. Test configuration loading at application startup
2. Test configuration dependency injection in FastAPI routes

## Performance Considerations

1. **Lazy Loading**: Settings loaded only when first accessed
2. **Caching**: Use `@lru_cache()` to cache settings instance
3. **Fast Validation**: Pydantic validation is optimized and fast

## Future Enhancements

1. **Config File Support**: Support loading from JSON/YAML files
2. **Remote Config**: Support loading from AWS Parameter Store / Vault
3. **Dynamic Reload**: Support hot-reloading configuration without restart
4. **Feature Flags**: Integrate feature flag system
5. **Environment Profiles**: Support profile-based configuration (dev, staging, prod)

## Success Criteria

✅ All configuration loaded from environment variables
✅ Type safety enforced via Pydantic
✅ Required fields validated at startup
✅ Settings accessible via singleton pattern
✅ Easy to override in tests
✅ No sensitive values logged or exposed
✅ 80%+ test coverage
✅ Documentation complete

## Dependencies

- `pydantic-settings`: For settings management
- `python-dotenv`: For .env file loading (included in pydantic-settings)

## References

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [FastAPI Settings Documentation](https://fastapi.tiangolo.com/advanced/settings/)
- [12-Factor App - Config](https://12factor.net/config)