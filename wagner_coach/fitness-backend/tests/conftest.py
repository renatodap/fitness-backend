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


@pytest.fixture
def mock_user():
    """Mock user data for testing"""
    return {
        'id': 'test-user-id-123',
        'email': 'test@example.com',
        'full_name': 'Test User',
        'primary_goal': 'build_muscle',
        'experience_level': 'intermediate',
        'age': 28,
        'weight_lbs': 180,
        'height_inches': 72
    }


@pytest.fixture
def mock_workout():
    """Mock workout data for testing"""
    return {
        'id': 'workout-123',
        'user_id': 'test-user-id-123',
        'name': 'Push Day',
        'workout_type': 'strength',
        'started_at': datetime.utcnow().isoformat(),
        'ended_at': (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        'duration_minutes': 60,
        'perceived_exertion': 8,
        'energy_level': 7
    }


@pytest.fixture
def mock_conversation():
    """Mock conversation data for testing"""
    return {
        'id': 'conv-123',
        'user_id': 'test-user-id-123',
        'coach_persona_id': 'trainer-persona-id',
        'messages': [
            {
                'role': 'user',
                'content': 'What should I do today?',
                'timestamp': datetime.utcnow().isoformat()
            },
            {
                'role': 'assistant',
                'content': 'Based on your recent workouts...',
                'timestamp': datetime.utcnow().isoformat()
            }
        ],
        'last_message_at': datetime.utcnow().isoformat(),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
