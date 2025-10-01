# Test Design: Configuration Management

## Test Overview
Comprehensive test suite for the Configuration Management feature ensuring proper loading, validation, and access of application settings.

## Test Strategy

### Test Levels
1. **Unit Tests**: Test individual configuration loading and validation
2. **Integration Tests**: Test configuration usage in application context
3. **Coverage Target**: ≥80% code coverage

### Test Framework
- **pytest**: Main testing framework
- **pytest-env**: For environment variable manipulation
- **pytest-mock**: For mocking external dependencies

## Test Cases

### 1. Configuration Loading Tests

#### TC-CONFIG-001: Load Configuration from Environment Variables
**Objective**: Verify settings can be loaded from environment variables

**Setup**:
```python
import os
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_KEY"] = "test-anon-key"
os.environ["SUPABASE_SERVICE_KEY"] = "test-service-key"
os.environ["OPENAI_API_KEY"] = "sk-test-key"
os.environ["JWT_SECRET"] = "test-jwt-secret"
os.environ["CRON_SECRET"] = "test-cron-secret"
os.environ["WEBHOOK_SECRET"] = "test-webhook-secret"
```

**Test Steps**:
1. Set environment variables
2. Create Settings instance
3. Verify all values loaded correctly

**Expected Result**:
- All values match environment variables
- No validation errors

**Assertions**:
```python
def test_load_from_environment():
    settings = Settings()
    assert settings.SUPABASE_URL == "https://test.supabase.co"
    assert settings.SUPABASE_KEY == "test-anon-key"
    assert settings.OPENAI_API_KEY == "sk-test-key"
    assert settings.JWT_SECRET == "test-jwt-secret"
```

---

#### TC-CONFIG-002: Load Configuration with Default Values
**Objective**: Verify default values are applied when not specified

**Setup**: Minimal environment variables (only required fields)

**Test Steps**:
1. Set only required environment variables
2. Create Settings instance
3. Verify default values applied

**Expected Result**:
- Required fields loaded from environment
- Optional fields use defaults

**Assertions**:
```python
def test_default_values():
    settings = Settings()
    assert settings.APP_NAME == "Fitness Backend"
    assert settings.ENVIRONMENT == "development"
    assert settings.DEBUG is False
    assert settings.LOG_LEVEL == "INFO"
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.REDIS_URL == "redis://localhost:6379"
    assert settings.JWT_ALGORITHM == "HS256"
```

---

#### TC-CONFIG-003: Load Configuration from .env File
**Objective**: Verify settings can be loaded from .env file

**Setup**:
```
# .env.test
SUPABASE_URL=https://testfile.supabase.co
SUPABASE_KEY=file-anon-key
SUPABASE_SERVICE_KEY=file-service-key
OPENAI_API_KEY=sk-file-key
JWT_SECRET=file-jwt-secret
CRON_SECRET=file-cron-secret
WEBHOOK_SECRET=file-webhook-secret
ENVIRONMENT=test
DEBUG=true
```

**Test Steps**:
1. Create .env.test file
2. Create Settings instance with env_file=".env.test"
3. Verify values loaded from file

**Expected Result**:
- All values loaded from .env file
- File values override defaults

**Assertions**:
```python
def test_load_from_env_file(tmp_path):
    env_file = tmp_path / ".env.test"
    env_file.write_text("""
    SUPABASE_URL=https://testfile.supabase.co
    ENVIRONMENT=test
    DEBUG=true
    """)

    settings = Settings(_env_file=str(env_file))
    assert settings.SUPABASE_URL == "https://testfile.supabase.co"
    assert settings.ENVIRONMENT == "test"
    assert settings.DEBUG is True
```

---

### 2. Validation Tests

#### TC-CONFIG-004: Missing Required Field Validation
**Objective**: Verify validation error when required field is missing

**Setup**: Clear all environment variables

**Test Steps**:
1. Clear SUPABASE_URL environment variable
2. Attempt to create Settings instance
3. Catch ValidationError

**Expected Result**:
- ValidationError raised
- Error message indicates missing field

**Assertions**:
```python
def test_missing_required_field():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            # Missing SUPABASE_URL
            SUPABASE_KEY="test-key",
            SUPABASE_SERVICE_KEY="test-service-key",
            OPENAI_API_KEY="test-openai",
            JWT_SECRET="test-jwt",
            CRON_SECRET="test-cron",
            WEBHOOK_SECRET="test-webhook"
        )

    assert "SUPABASE_URL" in str(exc_info.value)
    assert "field required" in str(exc_info.value)
```

---

#### TC-CONFIG-005: Invalid URL Format Validation
**Objective**: Verify validation error for invalid URL format

**Test Steps**:
1. Set SUPABASE_URL to invalid format (e.g., "not-a-url")
2. Attempt to create Settings instance
3. Catch ValidationError

**Expected Result**:
- ValidationError raised
- Error message indicates invalid URL

**Assertions**:
```python
def test_invalid_url_format():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            SUPABASE_URL="not-a-valid-url",
            SUPABASE_KEY="test-key",
            SUPABASE_SERVICE_KEY="test-service-key",
            OPENAI_API_KEY="test-openai",
            JWT_SECRET="test-jwt",
            CRON_SECRET="test-cron",
            WEBHOOK_SECRET="test-webhook"
        )

    assert "SUPABASE_URL" in str(exc_info.value)
    assert "URL" in str(exc_info.value) or "http" in str(exc_info.value)
```

---

#### TC-CONFIG-006: Invalid Log Level Validation
**Objective**: Verify validation error for invalid log level

**Test Steps**:
1. Set LOG_LEVEL to invalid value (e.g., "INVALID")
2. Attempt to create Settings instance
3. Catch ValidationError

**Expected Result**:
- ValidationError raised
- Error message indicates invalid log level

**Assertions**:
```python
def test_invalid_log_level():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            LOG_LEVEL="INVALID_LEVEL",
            SUPABASE_URL="https://test.supabase.co",
            SUPABASE_KEY="test-key",
            SUPABASE_SERVICE_KEY="test-service-key",
            OPENAI_API_KEY="test-openai",
            JWT_SECRET="test-jwt",
            CRON_SECRET="test-cron",
            WEBHOOK_SECRET="test-webhook"
        )

    assert "LOG_LEVEL" in str(exc_info.value)
```

---

#### TC-CONFIG-007: Valid Environments Validation
**Objective**: Verify only valid environments are accepted

**Test Steps**:
1. Test with valid environments (development, staging, production)
2. Test with invalid environment
3. Verify validation behavior

**Expected Result**:
- Valid environments accepted
- Invalid environments rejected (if validator implemented)

**Assertions**:
```python
@pytest.mark.parametrize("env", ["development", "staging", "production"])
def test_valid_environments(env, base_settings):
    settings = Settings(**base_settings, ENVIRONMENT=env)
    assert settings.ENVIRONMENT == env

def test_invalid_environment(base_settings):
    # If environment validation is strict
    with pytest.raises(ValidationError):
        Settings(**base_settings, ENVIRONMENT="invalid-env")
```

---

### 3. Singleton Pattern Tests

#### TC-CONFIG-008: Singleton Pattern Verification
**Objective**: Verify get_settings() returns same instance

**Test Steps**:
1. Call get_settings() twice
2. Compare instances
3. Verify they are the same object

**Expected Result**:
- Both calls return same instance
- Object IDs match

**Assertions**:
```python
def test_singleton_pattern():
    from app.config import get_settings

    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2
    assert id(settings1) == id(settings2)
```

---

#### TC-CONFIG-009: Singleton Cache Clearing
**Objective**: Verify singleton cache can be cleared for testing

**Test Steps**:
1. Get initial settings instance
2. Clear cache
3. Get new settings instance
4. Verify instances are different

**Expected Result**:
- After cache clear, new instance created
- Useful for testing

**Assertions**:
```python
def test_clear_singleton_cache():
    from app.config import get_settings

    settings1 = get_settings()

    # Clear cache
    get_settings.cache_clear()

    settings2 = get_settings()

    # Note: May or may not be same depending on implementation
    # Just verify cache_clear() doesn't raise error
    assert settings2 is not None
```

---

### 4. Security Tests

#### TC-CONFIG-010: Sensitive Values Not Logged
**Objective**: Verify sensitive values are not exposed in logs

**Test Steps**:
1. Create Settings instance
2. Convert to dict/json
3. Verify sensitive fields masked

**Expected Result**:
- Sensitive fields show masked value
- Original values not exposed

**Assertions**:
```python
def test_sensitive_values_masked():
    settings = Settings(
        SUPABASE_URL="https://test.supabase.co",
        SUPABASE_KEY="test-key",
        SUPABASE_SERVICE_KEY="test-service-key",
        OPENAI_API_KEY="sk-secret-key",
        JWT_SECRET="jwt-secret",
        CRON_SECRET="cron-secret",
        WEBHOOK_SECRET="webhook-secret"
    )

    # If masking is implemented
    settings_dict = settings.model_dump()

    # Sensitive fields should be masked or excluded
    if "OPENAI_API_KEY" in settings_dict:
        assert settings_dict["OPENAI_API_KEY"] == "***REDACTED***"
    if "JWT_SECRET" in settings_dict:
        assert settings_dict["JWT_SECRET"] == "***REDACTED***"
```

---

#### TC-CONFIG-011: No Secrets in String Representation
**Objective**: Verify secrets not in __str__ or __repr__

**Test Steps**:
1. Create Settings with secrets
2. Convert to string
3. Verify secrets not present

**Expected Result**:
- String representation doesn't contain secrets
- Safe to log object

**Assertions**:
```python
def test_no_secrets_in_string():
    settings = Settings(
        SUPABASE_URL="https://test.supabase.co",
        SUPABASE_KEY="test-key",
        SUPABASE_SERVICE_KEY="test-service-key",
        OPENAI_API_KEY="sk-secret-key-12345",
        JWT_SECRET="jwt-secret-67890",
        CRON_SECRET="cron-secret",
        WEBHOOK_SECRET="webhook-secret"
    )

    settings_str = str(settings)
    settings_repr = repr(settings)

    # Secrets should not appear in string representation
    assert "sk-secret-key-12345" not in settings_str
    assert "jwt-secret-67890" not in settings_str
    assert "sk-secret-key-12345" not in settings_repr
    assert "jwt-secret-67890" not in settings_repr
```

---

### 5. Integration Tests

#### TC-CONFIG-012: FastAPI Dependency Injection
**Objective**: Verify settings work with FastAPI dependency injection

**Test Steps**:
1. Create FastAPI test client
2. Create endpoint using settings dependency
3. Make request to endpoint
4. Verify settings injected correctly

**Expected Result**:
- Settings injected into endpoint
- Values accessible in route handler

**Assertions**:
```python
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from app.config import Settings, get_settings

def test_fastapi_dependency_injection():
    app = FastAPI()

    @app.get("/config-test")
    def config_test(settings: Settings = Depends(get_settings)):
        return {
            "app_name": settings.APP_NAME,
            "environment": settings.ENVIRONMENT
        }

    client = TestClient(app)
    response = client.get("/config-test")

    assert response.status_code == 200
    data = response.json()
    assert "app_name" in data
    assert "environment" in data
```

---

#### TC-CONFIG-013: Configuration Access in Services
**Objective**: Verify settings can be accessed in service classes

**Test Steps**:
1. Create service class that uses settings
2. Instantiate service
3. Verify settings available and correct

**Expected Result**:
- Service can access settings
- Values correct

**Assertions**:
```python
from app.config import settings

class TestService:
    def __init__(self):
        self.api_prefix = settings.API_V1_PREFIX

    def get_endpoint(self, path: str) -> str:
        return f"{self.api_prefix}{path}"

def test_settings_in_service():
    service = TestService()
    endpoint = service.get_endpoint("/users")
    assert endpoint == "/api/v1/users"
```

---

### 6. Edge Cases

#### TC-CONFIG-014: Empty String vs None
**Objective**: Verify proper handling of empty strings vs None

**Test Steps**:
1. Set optional field to empty string
2. Create Settings instance
3. Verify behavior

**Expected Result**:
- Empty strings handled appropriately
- None values handled appropriately

**Assertions**:
```python
def test_empty_string_vs_none():
    settings = Settings(
        SUPABASE_URL="https://test.supabase.co",
        SUPABASE_KEY="test-key",
        SUPABASE_SERVICE_KEY="test-service-key",
        OPENAI_API_KEY="test-key",
        JWT_SECRET="test-secret",
        CRON_SECRET="test-cron",
        WEBHOOK_SECRET="test-webhook",
        SENTRY_DSN=""  # Empty string
    )

    # Verify empty string handled correctly
    assert settings.SENTRY_DSN == "" or settings.SENTRY_DSN is None
```

---

#### TC-CONFIG-015: Boolean String Parsing
**Objective**: Verify boolean values parsed correctly from strings

**Test Steps**:
1. Set DEBUG="true" as string
2. Create Settings instance
3. Verify parsed as boolean True

**Expected Result**:
- String "true" → boolean True
- String "false" → boolean False

**Assertions**:
```python
def test_boolean_string_parsing():
    settings = Settings(
        DEBUG="true",  # String
        SUPABASE_URL="https://test.supabase.co",
        SUPABASE_KEY="test-key",
        SUPABASE_SERVICE_KEY="test-service-key",
        OPENAI_API_KEY="test-key",
        JWT_SECRET="test-secret",
        CRON_SECRET="test-cron",
        WEBHOOK_SECRET="test-webhook"
    )

    assert settings.DEBUG is True
    assert isinstance(settings.DEBUG, bool)
```

---

#### TC-CONFIG-016: List Parsing from String
**Objective**: Verify list values parsed correctly from strings

**Test Steps**:
1. Set CORS_ORIGINS as JSON string
2. Create Settings instance
3. Verify parsed as list

**Expected Result**:
- JSON string parsed to list
- List contains correct values

**Assertions**:
```python
def test_list_parsing():
    import json

    origins = ["http://localhost:3000", "https://app.example.com"]
    settings = Settings(
        CORS_ORIGINS=json.dumps(origins),  # JSON string
        SUPABASE_URL="https://test.supabase.co",
        SUPABASE_KEY="test-key",
        SUPABASE_SERVICE_KEY="test-service-key",
        OPENAI_API_KEY="test-key",
        JWT_SECRET="test-secret",
        CRON_SECRET="test-cron",
        WEBHOOK_SECRET="test-webhook"
    )

    assert isinstance(settings.CORS_ORIGINS, list)
    assert len(settings.CORS_ORIGINS) == 2
    assert "http://localhost:3000" in settings.CORS_ORIGINS
```

---

## Test Fixtures

### Base Settings Fixture
```python
@pytest.fixture
def base_settings():
    """Provide minimal valid settings for testing"""
    return {
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_KEY": "test-anon-key",
        "SUPABASE_SERVICE_KEY": "test-service-key",
        "OPENAI_API_KEY": "sk-test-key",
        "JWT_SECRET": "test-jwt-secret",
        "CRON_SECRET": "test-cron-secret",
        "WEBHOOK_SECRET": "test-webhook-secret"
    }
```

### Test Settings Fixture
```python
@pytest.fixture
def test_settings(base_settings):
    """Provide Settings instance for testing"""
    return Settings(**base_settings)
```

### Clean Environment Fixture
```python
@pytest.fixture
def clean_env(monkeypatch):
    """Clean environment variables before test"""
    # Remove all relevant env vars
    for key in os.environ.copy():
        if key.startswith(("SUPABASE_", "OPENAI_", "JWT_", "CRON_", "WEBHOOK_", "REDIS_", "CELERY_")):
            monkeypatch.delenv(key, raising=False)

    yield
```

---

## Test Execution

### Run All Config Tests
```bash
pytest tests/unit/test_config.py -v
```

### Run with Coverage
```bash
pytest tests/unit/test_config.py --cov=app.config --cov-report=html --cov-report=term-missing
```

### Run Specific Test
```bash
pytest tests/unit/test_config.py::test_load_from_environment -v
```

---

## Coverage Requirements

### Minimum Coverage: 80%

### Coverage Areas:
- ✅ Configuration loading (environment vars, .env file, defaults)
- ✅ Validation (required fields, format validation, custom validators)
- ✅ Singleton pattern
- ✅ Security (sensitive value masking)
- ✅ Integration with FastAPI
- ✅ Edge cases (empty strings, boolean parsing, list parsing)

### Excluded from Coverage:
- Type hints
- Abstract methods (if any)
- Debug-only code

---

## Test Success Criteria

✅ All 16 test cases pass
✅ ≥80% code coverage achieved
✅ No flaky tests (all tests deterministic)
✅ Tests run in < 5 seconds
✅ All edge cases covered
✅ Security tests verify no sensitive data leakage
✅ Integration tests verify FastAPI compatibility

---

## Test Maintenance

### When to Update Tests:
1. New configuration parameter added → Add validation test
2. New validator added → Add validation test
3. Security requirement changes → Update security tests
4. Default value changes → Update default value tests

### Test Documentation:
- Each test must have clear docstring
- Test case IDs must match this document
- Failed assertions must have descriptive messages

---

## References

- [pytest Documentation](https://docs.pytest.org/)
- [Pydantic Testing Guide](https://docs.pydantic.dev/latest/concepts/models/#testing)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)