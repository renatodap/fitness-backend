"""
Tests for dashboard API endpoints.

Run with: pytest tests/test_dashboard_api.py -v
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_dashboard_context_requires_auth(client):
    """Test that /context requires authentication."""
    response = client.get("/api/v1/dashboard/context")
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_dashboard_context_success(authenticated_client, mock_supabase):
    """Test successful context retrieval."""
    # Mock profile data
    mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = {
        "id": "user-123",
        "has_completed_consultation": True,
        "shows_weight_card": True,
        "shows_recovery_card": False,
        "shows_workout_card": True
    }

    # Mock active program check
    mock_supabase.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value.data = [
        {"id": "program-123"}
    ]

    # Mock meal logs for streak
    mock_supabase.table.return_value.select.return_value.eq.return_value.gte.return_value.order.return_value.execute.return_value.data = [
        {"logged_at": datetime.utcnow().isoformat()},
        {"logged_at": (datetime.utcnow() - timedelta(days=1)).isoformat()},
        {"logged_at": (datetime.utcnow() - timedelta(days=2)).isoformat()}
    ]

    response = authenticated_client.get("/api/v1/dashboard/context")

    assert response.status_code == 200
    data = response.json()

    # Verify structure
    assert "user" in data
    assert "program" in data or data["program"] is None
    assert "events" in data or data["events"] is None

    # Verify user context
    user = data["user"]
    assert "hasCompletedConsultation" in user
    assert "hasActiveProgram" in user
    assert "streakDays" in user
    assert "tracksWeight" in user
    assert "showsWeightCard" in user
    assert "showsRecoveryCard" in user
    assert "showsWorkoutCard" in user

    # Verify types
    assert isinstance(user["hasCompletedConsultation"], bool)
    assert isinstance(user["streakDays"], int)


@pytest.mark.asyncio
async def test_streak_calculation_consecutive_days(authenticated_client, mock_supabase):
    """Test streak calculation with consecutive meal logs."""
    # Mock 5 consecutive days of meal logs
    today = datetime.utcnow()
    mock_data = [
        {"logged_at": (today - timedelta(days=i)).isoformat()}
        for i in range(5)
    ]

    mock_supabase.table.return_value.select.return_value.eq.return_value.gte.return_value.order.return_value.execute.return_value.data = mock_data

    response = authenticated_client.get("/api/v1/dashboard/context")

    assert response.status_code == 200
    data = response.json()
    assert data["user"]["streakDays"] == 5


@pytest.mark.asyncio
async def test_streak_calculation_with_gap(authenticated_client, mock_supabase):
    """Test streak calculation stops at gap."""
    # Mock meal logs with gap on day 2
    today = datetime.utcnow()
    mock_data = [
        {"logged_at": today.isoformat()},
        {"logged_at": (today - timedelta(days=1)).isoformat()},
        # Gap on day 2
        {"logged_at": (today - timedelta(days=3)).isoformat()}
    ]

    mock_supabase.table.return_value.select.return_value.eq.return_value.gte.return_value.order.return_value.execute.return_value.data = mock_data

    response = authenticated_client.get("/api/v1/dashboard/context")

    assert response.status_code == 200
    data = response.json()
    assert data["user"]["streakDays"] == 2  # Should stop at gap


@pytest.mark.asyncio
async def test_behavior_signal_logging(authenticated_client, mock_supabase):
    """Test behavior signal logging."""
    mock_supabase.table.return_value.insert.return_value.execute.return_value = AsyncMock()

    response = authenticated_client.post(
        "/api/v1/dashboard/behavior",
        json={
            "signal_type": "dashboard_open",
            "signal_value": "balanced",
            "metadata": {"timestamp": "2025-10-11T10:30:00Z"}
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "message" in data


@pytest.mark.asyncio
async def test_behavior_signal_invalid_type(authenticated_client):
    """Test behavior signal with invalid type."""
    response = authenticated_client.post(
        "/api/v1/dashboard/behavior",
        json={
            "signal_type": "invalid_type",
            "signal_value": "test",
            "metadata": {}
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_app_open_logging(authenticated_client, mock_supabase):
    """Test app open event logging."""
    mock_supabase.table.return_value.insert.return_value.execute.return_value = AsyncMock()

    response = authenticated_client.post(
        "/api/v1/dashboard/app-open",
        json={
            "source": "notification",
            "time_of_day": "morning"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_dashboard_preference_update(authenticated_client, mock_supabase):
    """Test dashboard preference update."""
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = AsyncMock()

    response = authenticated_client.put(
        "/api/v1/dashboard/preference",
        json={"preference": "detailed"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["new_preference"] == "detailed"


@pytest.mark.asyncio
async def test_dashboard_preference_invalid_variant(authenticated_client):
    """Test dashboard preference with invalid variant."""
    response = authenticated_client.put(
        "/api/v1/dashboard/preference",
        json={"preference": "invalid"}
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_weight_tracking_auto_detection(authenticated_client, mock_supabase):
    """Test auto-detection of weight tracking."""
    # Mock profile with shows_weight_card = False
    mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = {
        "shows_weight_card": False,
        "shows_recovery_card": False,
        "shows_workout_card": True,
        "has_completed_consultation": True
    }

    # Mock 2+ weight logs in last 14 days
    mock_supabase.table.return_value.select.return_value.eq.return_value.gte.return_value.execute.return_value.count = 3

    response = authenticated_client.get("/api/v1/dashboard/context")

    assert response.status_code == 200
    data = response.json()

    # Auto-detection should enable weight card
    assert data["user"]["tracksWeight"] is True
    assert data["user"]["showsWeightCard"] is True  # Auto-detected


@pytest.mark.asyncio
async def test_program_context_calculation(authenticated_client, mock_supabase):
    """Test program context calculation."""
    # Mock active program started 5 days ago
    start_date = (datetime.utcnow() - timedelta(days=5)).date().isoformat()

    mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = {
        "id": "program-123",
        "program_name": "Test Program",
        "start_date": start_date,
        "total_weeks": 12
    }

    # Mock meal logs for adherence
    three_days_ago = (datetime.utcnow() - timedelta(days=3)).isoformat()
    mock_supabase.table.return_value.select.return_value.eq.return_value.gte.return_value.execute.return_value.count = 6  # 6 out of 9 expected

    response = authenticated_client.get("/api/v1/dashboard/context")

    assert response.status_code == 200
    data = response.json()

    # Verify program context
    assert data["program"] is not None
    program = data["program"]
    assert program["dayNumber"] == 6  # 5 days elapsed + 1
    assert program["weekNumber"] == 1
    assert program["programName"] == "Test Program"
    assert 0 <= program["adherenceLast3Days"] <= 100


@pytest.mark.asyncio
async def test_events_context_upcoming_event(authenticated_client, mock_supabase):
    """Test events context with upcoming event."""
    # Mock event 21 days in future
    event_date = (datetime.utcnow() + timedelta(days=21)).date().isoformat()

    mock_supabase.table.return_value.select.return_value.eq.return_value.gte.return_value.lte.return_value.order.return_value.limit.return_value.execute.return_value.data = [
        {
            "event_name": "Half Marathon",
            "event_date": event_date
        }
    ]

    response = authenticated_client.get("/api/v1/dashboard/context")

    assert response.status_code == 200
    data = response.json()

    # Verify events context
    assert data["events"] is not None
    assert data["events"]["primaryEvent"] is not None
    event = data["events"]["primaryEvent"]
    assert event["name"] == "Half Marathon"
    assert event["daysUntil"] == 21


@pytest.mark.asyncio
async def test_rate_limiting(authenticated_client):
    """Test rate limiting on dashboard endpoints."""
    # Make 101 rapid requests (assuming 100/day limit)
    responses = []
    for i in range(101):
        response = authenticated_client.get("/api/v1/dashboard/context")
        responses.append(response)

    # Last request should be rate limited
    assert responses[-1].status_code == 429


# Fixtures

@pytest.fixture
def client():
    """Create test client."""
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)


@pytest.fixture
def authenticated_client(client, mock_jwt):
    """Create authenticated test client with JWT."""
    client.headers = {"Authorization": f"Bearer {mock_jwt}"}
    return client


@pytest.fixture
def mock_jwt():
    """Mock JWT token for testing."""
    import jwt
    from app.config import settings

    payload = {
        "sub": "user-123",
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


@pytest.fixture
def mock_supabase():
    """Mock Supabase client."""
    with patch("app.services.supabase_service.get_supabase_client") as mock:
        yield mock.return_value
