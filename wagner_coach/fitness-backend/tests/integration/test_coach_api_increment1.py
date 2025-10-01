"""
Integration tests for Coach Chat API (INCREMENT 1)
Following TDD: Tests written before implementation
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock


class TestCoachAPIIntegration:
    """Integration tests for Coach Chat API endpoint"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        from app.main import app
        return TestClient(app)

    @pytest.fixture
    def auth_headers(self, mock_user):
        """Create auth headers for requests"""
        return {
            "X-User-ID": mock_user['id'],
            "Authorization": f"Bearer test-token-{mock_user['id']}"
        }

    def test_chat_endpoint_exists(self, client):
        """Test chat endpoint exists"""
        response = client.post("/api/v1/coach/chat")
        # Should return 401 or 422, not 404
        assert response.status_code in [401, 422]

    def test_chat_endpoint_requires_auth(self, client):
        """Test chat without auth fails with 401"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "Hello"
            }
        )
        assert response.status_code == 401

    def test_chat_endpoint_success_trainer(self, client, auth_headers):
        """Test successful chat message to trainer"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "What should I do today?"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'message' in data
        assert 'conversation_id' in data
        assert len(data['message']) > 0
        assert data['error'] is None or data['error'] == ''

    def test_chat_endpoint_success_nutritionist(self, client, auth_headers):
        """Test successful chat message to nutritionist"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "nutritionist",
                "message": "What should I eat today?"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    def test_chat_endpoint_invalid_coach_type(self, client, auth_headers):
        """Test invalid coach type returns 400"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "invalid",
                "message": "Hello"
            },
            headers=auth_headers
        )

        assert response.status_code in [400, 422]

    def test_chat_endpoint_empty_message(self, client, auth_headers):
        """Test empty message returns 400"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": ""
            },
            headers=auth_headers
        )

        assert response.status_code in [400, 422]

    def test_chat_endpoint_message_too_long(self, client, auth_headers):
        """Test message length limit"""
        long_message = "a" * 1001
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": long_message
            },
            headers=auth_headers
        )

        assert response.status_code in [400, 422]

    def test_chat_endpoint_missing_coach_type(self, client, auth_headers):
        """Test missing coach_type returns 422"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "message": "Hello"
            },
            headers=auth_headers
        )

        assert response.status_code == 422

    def test_chat_endpoint_missing_message(self, client, auth_headers):
        """Test missing message returns 422"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer"
            },
            headers=auth_headers
        )

        assert response.status_code == 422

    def test_chat_response_structure(self, client, auth_headers):
        """Test response has correct structure"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "Test message"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert 'success' in data
        assert 'message' in data
        assert 'conversation_id' in data

        # Check types
        assert isinstance(data['success'], bool)
        assert isinstance(data['message'], str)
        assert isinstance(data['conversation_id'], str)

    def test_chat_conversation_persistence(self, client, auth_headers):
        """Test conversation persists across messages"""
        # First message
        response1 = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "My name is John"
            },
            headers=auth_headers
        )
        assert response1.status_code == 200
        conv_id = response1.json()['conversation_id']

        # Second message with same conversation
        response2 = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "What's my name?",
                "conversation_id": conv_id
            },
            headers=auth_headers
        )
        assert response2.status_code == 200
        assert response2.json()['conversation_id'] == conv_id

    def test_chat_context_info_included(self, client, auth_headers):
        """Test response includes context information"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "What should I do?"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Context info should be included (optional field)
        if 'context_used' in data:
            assert isinstance(data['context_used'], dict)
            # Check expected fields in context_used
            context = data['context_used']
            if 'recent_workouts' in context:
                assert isinstance(context['recent_workouts'], int)
                assert context['recent_workouts'] >= 0

    def test_chat_handles_special_characters(self, client, auth_headers):
        """Test chat handles special characters in message"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "I weigh 180lbs & lift @gym! 💪"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    def test_chat_handles_multiline_message(self, client, auth_headers):
        """Test chat handles multiline messages"""
        message = """I need help with my workout.

        I've been training for 3 months.
        What should I focus on next?"""

        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": message
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
