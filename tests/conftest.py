"""
Pytest configuration and fixtures for backend tests
Sets up test environment variables before any imports
"""

import os
import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent.parent
sys.path.insert(0, str(app_dir))

# Set required environment variables for testing
# These are dummy values - tests should mock API calls
os.environ.setdefault('SUPABASE_URL', 'https://test.supabase.co')
os.environ.setdefault('SUPABASE_KEY', 'test-key-' + 'x' * 100)
os.environ.setdefault('SUPABASE_SERVICE_KEY', 'test-service-key-' + 'x' * 100)
os.environ.setdefault('OPENAI_API_KEY', 'sk-test-' + 'x' * 40)
os.environ.setdefault('GROQ_API_KEY', 'gsk_test_' + 'x' * 50)
os.environ.setdefault('JWT_SECRET', 'test-jwt-secret-' + 'x' * 32)
os.environ.setdefault('CRON_SECRET', 'test-cron-secret')
os.environ.setdefault('WEBHOOK_SECRET', 'test-webhook-secret')
os.environ.setdefault('ENVIRONMENT', 'test')
os.environ.setdefault('DEBUG', 'true')
os.environ.setdefault('ALLOWED_ORIGINS', 'http://localhost:3000')

# Import pytest and testing libraries
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch
import jwt
from datetime import datetime, timedelta


# Test user fixtures
TEST_USER_1_ID = "test-user-1-uuid"
TEST_USER_2_ID = "test-user-2-uuid"


@pytest.fixture
def test_user_1():
    """First test user."""
    return {
        "id": TEST_USER_1_ID,
        "email": "test1@wagnercoach.com",
        "name": "Test User 1"
    }


@pytest.fixture
def test_user_2():
    """Second test user for RLS testing."""
    return {
        "id": TEST_USER_2_ID,
        "email": "test2@wagnercoach.com",
        "name": "Test User 2"
    }


@pytest.fixture
def test_jwt_token_user_1():
    """Generate JWT token for test user 1."""
    payload = {
        "sub": TEST_USER_1_ID,
        "email": "test1@wagnercoach.com",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, os.environ["JWT_SECRET"], algorithm="HS256")
    return token


@pytest.fixture
def test_jwt_token_user_2():
    """Generate JWT token for test user 2."""
    payload = {
        "sub": TEST_USER_2_ID,
        "email": "test2@wagnercoach.com",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, os.environ["JWT_SECRET"], algorithm="HS256")
    return token


@pytest.fixture
async def authenticated_client(test_jwt_token_user_1):
    """Authenticated HTTP client for test user 1."""
    from app.main import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers["Authorization"] = f"Bearer {test_jwt_token_user_1}"
        yield client


@pytest.fixture
async def authenticated_client_user_2(test_jwt_token_user_2):
    """Authenticated HTTP client for test user 2."""
    from app.main import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers["Authorization"] = f"Bearer {test_jwt_token_user_2}"
        yield client


@pytest.fixture
def mock_supabase():
    """Mock Supabase client for unit tests."""
    mock = MagicMock()
    mock.table = MagicMock(return_value=mock)
    mock.select = MagicMock(return_value=mock)
    mock.insert = MagicMock(return_value=mock)
    mock.update = MagicMock(return_value=mock)
    mock.delete = MagicMock(return_value=mock)
    mock.eq = MagicMock(return_value=mock)
    mock.execute = AsyncMock(return_value=MagicMock(data=[], error=None))
    return mock


@pytest.fixture
def mock_anthropic():
    """Mock Anthropic API client."""
    mock = AsyncMock()
    mock.messages.create = AsyncMock(return_value=MagicMock(
        content=[MagicMock(text="Mocked AI response")],
        usage=MagicMock(input_tokens=100, output_tokens=50)
    ))
    return mock
