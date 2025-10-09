"""
Integration tests for event system.

Tests:
- Event creation and countdown
- Event-specific program generation
- Event-aware daily recommendations
- AI coach event tools
"""
import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient

from app.main import app


@pytest.fixture
def future_event_data():
    """Event 30 days in the future."""
    event_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    return {
        "event_name": "Test Marathon",
        "event_type": "marathon",
        "event_date": event_date,
        "goal_performance": "Sub 4:00",
        "is_primary_goal": True
    }


@pytest.fixture
def taper_event_data():
    """Event 7 days in the future (taper week)."""
    event_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    return {
        "event_name": "Taper Marathon",
        "event_type": "marathon",
        "event_date": event_date,
        "goal_performance": "Sub 3:30",
        "is_primary_goal": True
    }


@pytest.fixture
def carb_load_event_data():
    """Event 2 days in the future (carb loading phase)."""
    event_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    return {
        "event_name": "Carb Load Marathon",
        "event_type": "marathon",
        "event_date": event_date,
        "goal_performance": "Sub 3:00",
        "is_primary_goal": True
    }


class TestEventCreation:
    """Test event creation and basic operations."""

    @pytest.mark.asyncio
    async def test_create_event_requires_auth(self):
        """Test that event creation requires authentication."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/v1/events", json={
                "event_name": "Test Event",
                "event_type": "marathon",
                "event_date": "2026-04-20"
            })
            assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_event_success(self, authenticated_client, future_event_data):
        """Test successful event creation."""
        response = await authenticated_client.post(
            "/api/v1/events",
            json=future_event_data
        )

        assert response.status_code == 201
        data = response.json()
        assert data["event_name"] == "Test Marathon"
        assert data["event_type"] == "marathon"
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_event_validation(self, authenticated_client):
        """Test event validation rejects invalid event types."""
        response = await authenticated_client.post("/api/v1/events", json={
            "event_name": "Invalid Event",
            "event_type": "invalid_type",  # Not in allowed types
            "event_date": "2026-04-20"
        })

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_event_past_date(self, authenticated_client):
        """Test event validation rejects past dates."""
        past_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        response = await authenticated_client.post("/api/v1/events", json={
            "event_name": "Past Event",
            "event_type": "marathon",
            "event_date": past_date
        })

        assert response.status_code == 422


class TestEventCountdown:
    """Test event countdown and training phase calculations."""

    @pytest.mark.asyncio
    async def test_get_primary_event_countdown(self, authenticated_client, future_event_data):
        """Test fetching primary event with countdown."""
        # Create event
        create_response = await authenticated_client.post(
            "/api/v1/events",
            json=future_event_data
        )
        assert create_response.status_code == 201

        # Get countdown
        countdown_response = await authenticated_client.get("/api/v1/events/primary/countdown")
        assert countdown_response.status_code == 200

        data = countdown_response.json()
        assert data["event_name"] == "Test Marathon"
        assert data["event_type"] == "marathon"
        assert "days_until_event" in data
        assert "current_training_phase" in data
        assert data["days_until_event"] == 30

    @pytest.mark.asyncio
    async def test_countdown_no_primary_event(self, authenticated_client):
        """Test countdown returns 404 when no primary event exists."""
        response = await authenticated_client.get("/api/v1/events/primary/countdown")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_training_phase_calculations(self, authenticated_client, taper_event_data):
        """Test training phase is correctly calculated."""
        # Create event 7 days out
        create_response = await authenticated_client.post(
            "/api/v1/events",
            json=taper_event_data
        )
        assert create_response.status_code == 201

        # Get countdown
        countdown_response = await authenticated_client.get("/api/v1/events/primary/countdown")
        data = countdown_response.json()

        assert data["current_training_phase"] == "taper"
        assert data["days_until_event"] == 7


class TestEventProgramGeneration:
    """Test event-specific program generation."""

    @pytest.mark.asyncio
    async def test_generate_program_with_event(self, authenticated_client, future_event_data):
        """Test generating program linked to event."""
        # Create event
        event_response = await authenticated_client.post(
            "/api/v1/events",
            json=future_event_data
        )
        assert event_response.status_code == 201
        event_id = event_response.json()["id"]

        # Start program generation
        start_response = await authenticated_client.post("/api/v1/programs/generate/start")
        assert start_response.status_code == 200
        session_id = start_response.json()["session_id"]

        # Complete program generation with event_id
        complete_response = await authenticated_client.post(
            "/api/v1/programs/generate/complete",
            json={
                "session_id": session_id,
                "answers": [
                    {"question": "Primary focus?", "answer": "endurance"},
                    {"question": "Training days?", "answer": "5_days"}
                ],
                "event_id": event_id
            }
        )

        assert complete_response.status_code == 200
        program_data = complete_response.json()
        assert "program_id" in program_data

        # Verify event has linked program
        event_detail_response = await authenticated_client.get(f"/api/v1/events/{event_id}")
        assert event_detail_response.status_code == 200
        event_detail = event_detail_response.json()
        assert event_detail["linked_program_id"] == program_data["program_id"]


class TestEventDailyRecommendations:
    """Test event-aware daily recommendations."""

    @pytest.mark.asyncio
    async def test_daily_recs_with_taper_event(self, authenticated_client, taper_event_data):
        """Test daily recommendations during taper week."""
        # Create taper event (7 days out)
        await authenticated_client.post("/api/v1/events", json=taper_event_data)

        # Get daily recommendations
        recs_response = await authenticated_client.get("/api/v1/recommendations/daily")
        assert recs_response.status_code == 200

        data = recs_response.json()
        recommendations = data.get("recommendations", [])

        # Should include event countdown notification
        event_recs = [r for r in recommendations if r.get("type") == "event_reminder"]
        assert len(event_recs) > 0

        event_rec = event_recs[0]
        assert "7 days" in event_rec["content"]["message"]
        assert event_rec["priority"] == 5  # High priority for imminent event

    @pytest.mark.asyncio
    async def test_daily_recs_carb_loading(self, authenticated_client, carb_load_event_data):
        """Test daily recommendations during carb loading phase."""
        # Create event 2 days out (carb loading phase)
        await authenticated_client.post("/api/v1/events", json=carb_load_event_data)

        # Get daily recommendations
        recs_response = await authenticated_client.get("/api/v1/recommendations/daily")
        assert recs_response.status_code == 200

        data = recs_response.json()
        recommendations = data.get("recommendations", [])

        # Should include meal recommendations with increased carbs
        meal_recs = [r for r in recommendations if r.get("type") == "meal"]

        # At least one meal should mention carb loading or increased carbs
        has_carb_focus = any(
            "carb" in r.get("reasoning", "").lower()
            for r in meal_recs
        )
        assert has_carb_focus

    @pytest.mark.asyncio
    async def test_daily_recs_without_event(self, authenticated_client):
        """Test daily recommendations work without events."""
        # Don't create any event
        recs_response = await authenticated_client.get("/api/v1/recommendations/daily")
        assert recs_response.status_code == 200

        data = recs_response.json()
        recommendations = data.get("recommendations", [])

        # Should not include event reminders
        event_recs = [r for r in recommendations if r.get("type") == "event_reminder"]
        assert len(event_recs) == 0


class TestEventCoachTools:
    """Test AI coach event awareness tools."""

    @pytest.mark.asyncio
    async def test_coach_can_see_upcoming_events(self, authenticated_client, future_event_data):
        """Test AI coach can retrieve upcoming events."""
        # Create event
        await authenticated_client.post("/api/v1/events", json=future_event_data)

        # Chat with coach asking about events
        chat_response = await authenticated_client.post("/api/v1/coach/chat", json={
            "message": "What events do I have coming up?",
            "conversation_type": "general"
        })

        assert chat_response.status_code == 200
        # Response should mention the marathon
        # (Exact assertion depends on streaming response format)

    @pytest.mark.asyncio
    async def test_coach_primary_event_countdown(self, authenticated_client, taper_event_data):
        """Test AI coach can access primary event countdown."""
        # Create taper event
        await authenticated_client.post("/api/v1/events", json=taper_event_data)

        # Chat with coach about training
        chat_response = await authenticated_client.post("/api/v1/coach/chat", json={
            "message": "What should I focus on this week?",
            "conversation_type": "training"
        })

        assert chat_response.status_code == 200
        # Coach should reference taper week
        # (Exact assertion depends on streaming response format)


class TestEventCRUD:
    """Test event CRUD operations."""

    @pytest.mark.asyncio
    async def test_list_user_events(self, authenticated_client, future_event_data):
        """Test listing user's events."""
        # Create multiple events
        await authenticated_client.post("/api/v1/events", json=future_event_data)

        event_2 = future_event_data.copy()
        event_2["event_name"] = "Another Marathon"
        event_2["is_primary_goal"] = False
        await authenticated_client.post("/api/v1/events", json=event_2)

        # List events
        list_response = await authenticated_client.get("/api/v1/events")
        assert list_response.status_code == 200

        data = list_response.json()
        assert len(data) >= 2

    @pytest.mark.asyncio
    async def test_update_event(self, authenticated_client, future_event_data):
        """Test updating an event."""
        # Create event
        create_response = await authenticated_client.post(
            "/api/v1/events",
            json=future_event_data
        )
        event_id = create_response.json()["id"]

        # Update event
        update_response = await authenticated_client.put(
            f"/api/v1/events/{event_id}",
            json={"goal_performance": "Sub 3:45"}
        )
        assert update_response.status_code == 200

        data = update_response.json()
        assert data["goal_performance"] == "Sub 3:45"

    @pytest.mark.asyncio
    async def test_delete_event(self, authenticated_client, future_event_data):
        """Test deleting an event."""
        # Create event
        create_response = await authenticated_client.post(
            "/api/v1/events",
            json=future_event_data
        )
        event_id = create_response.json()["id"]

        # Delete event
        delete_response = await authenticated_client.delete(f"/api/v1/events/{event_id}")
        assert delete_response.status_code == 204

        # Verify deleted
        get_response = await authenticated_client.get(f"/api/v1/events/{event_id}")
        assert get_response.status_code == 404


class TestEventRLS:
    """Test row-level security for events."""

    @pytest.mark.asyncio
    async def test_user_cannot_access_other_user_events(
        self,
        authenticated_client,
        authenticated_client_user_2,
        future_event_data
    ):
        """Test RLS prevents cross-user access."""
        # User 1 creates event
        create_response = await authenticated_client.post(
            "/api/v1/events",
            json=future_event_data
        )
        event_id = create_response.json()["id"]

        # User 2 tries to access User 1's event
        access_response = await authenticated_client_user_2.get(f"/api/v1/events/{event_id}")
        assert access_response.status_code == 404  # Should not find it

    @pytest.mark.asyncio
    async def test_user_cannot_update_other_user_events(
        self,
        authenticated_client,
        authenticated_client_user_2,
        future_event_data
    ):
        """Test RLS prevents cross-user updates."""
        # User 1 creates event
        create_response = await authenticated_client.post(
            "/api/v1/events",
            json=future_event_data
        )
        event_id = create_response.json()["id"]

        # User 2 tries to update User 1's event
        update_response = await authenticated_client_user_2.put(
            f"/api/v1/events/{event_id}",
            json={"goal_performance": "Sub 2:00"}
        )
        assert update_response.status_code in [403, 404]
