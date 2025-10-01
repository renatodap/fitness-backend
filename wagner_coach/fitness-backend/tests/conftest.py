"""
Pytest configuration and shared fixtures.
"""

import pytest
from datetime import datetime, timedelta
from jose import jwt
from unittest.mock import Mock

from app.config import Settings, get_settings


@pytest.fixture
def base_settings_dict():
    """Provide minimal valid settings dictionary for testing."""
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
def test_settings(base_settings_dict):
    """Provide Settings instance for testing."""
    return Settings(**base_settings_dict)


@pytest.fixture(autouse=True)
def reset_settings_cache():
    """Reset settings cache before and after each test."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def mock_jwt_token():
    """Generate valid mock JWT token."""
    payload = {
        "sub": "test-user-id-123",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "iss": "https://test.supabase.co/auth/v1",
        "email": "test@example.com",
    }
    return jwt.encode(payload, "test-jwt-secret", algorithm="HS256")


@pytest.fixture
def mock_expired_token():
    """Generate expired mock JWT token."""
    payload = {
        "sub": "test-user-id-123",
        "exp": datetime.utcnow() - timedelta(hours=1),
        "iat": datetime.utcnow() - timedelta(hours=2),
    }
    return jwt.encode(payload, "test-jwt-secret", algorithm="HS256")


@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client."""
    mock_client = Mock()
    mock_table = Mock()
    mock_table.select().execute.return_value = Mock(data=[])
    mock_client.table.return_value = mock_table
    return mock_client
