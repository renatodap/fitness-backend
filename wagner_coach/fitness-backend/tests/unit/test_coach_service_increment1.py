"""
Unit tests for Coach Service (INCREMENT 1)
Following TDD: Tests written before implementation
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from app.services.coach_service_interface import ICoachService
from app.api.v1.schemas.coach_schemas import (
    ChatRequest,
    ChatResponse,
    UserContext,
    CoachPersona
)


class TestCoachServiceUnit:
    """Unit tests for Coach Service"""

    @pytest.fixture
    def coach_service(self, test_settings, monkeypatch):
        """Create coach service instance with mocked dependencies"""
        # Mock the settings
        from app.config import get_settings
        monkeypatch.setattr('app.config.get_settings', lambda: test_settings)
        monkeypatch.setattr('app.services.coach_service.get_settings', lambda: test_settings)
        monkeypatch.setattr('app.services.supabase_service.get_settings', lambda: test_settings)

        # Mock Supabase client
        mock_client = Mock()
        monkeypatch.setattr('app.services.coach_service.get_service_client', lambda: mock_client)
        monkeypatch.setattr('app.services.context_builder.get_service_client', lambda: mock_client)

        # Now create the service
        from app.services.coach_service import CoachService
        return CoachService()

    @pytest.mark.asyncio
    async def test_get_trainer_persona(self, coach_service):
        """Test retrieving trainer persona"""
        # This test should pass when implementation is done
        persona = await coach_service.get_persona('trainer')

        assert persona is not None
        assert persona.name == 'trainer'
        assert persona.display_name is not None
        assert len(persona.system_prompt) > 0
        assert 'trainer' in persona.display_name.lower() or 'alex' in persona.display_name.lower()

    @pytest.mark.asyncio
    async def test_get_nutritionist_persona(self, coach_service):
        """Test retrieving nutritionist persona"""
        persona = await coach_service.get_persona('nutritionist')

        assert persona is not None
        assert persona.name == 'nutritionist'
        assert persona.display_name is not None
        assert len(persona.system_prompt) > 0

    @pytest.mark.asyncio
    async def test_get_invalid_persona(self, coach_service):
        """Test retrieving non-existent persona returns None"""
        persona = await coach_service.get_persona('invalid_coach')
        assert persona is None

    @pytest.mark.asyncio
    async def test_build_context_structure(self, coach_service, mock_user):
        """Test context building returns proper structure"""
        context = await coach_service.build_context(
            user_id=mock_user['id'],
            message="What should I do today?",
            coach_type='trainer'
        )

        # Verify context structure
        assert isinstance(context, UserContext)
        assert context.user_id == mock_user['id']
        assert context.profile is not None or context.profile == {}
        assert isinstance(context.recent_workouts, list)
        assert isinstance(context.recent_meals, list)
        assert isinstance(context.relevant_embeddings, list)

    @pytest.mark.asyncio
    async def test_build_context_with_workouts(self, coach_service, mock_user, mock_workout):
        """Test context building includes recent workouts"""
        # Mock the database call to return mock_workout
        with patch('app.services.coach_service.get_recent_workouts', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = [mock_workout]

            context = await coach_service.build_context(
                user_id=mock_user['id'],
                message="What should I do today?",
                coach_type='trainer'
            )

            assert len(context.recent_workouts) > 0

    @pytest.mark.asyncio
    async def test_generate_response_returns_valid_response(self, coach_service, mock_user):
        """Test AI response generation returns valid ChatResponse"""
        response = await coach_service.generate_response(
            user_id=mock_user['id'],
            message="What should I do today?",
            coach_type='trainer'
        )

        assert isinstance(response, ChatResponse)
        assert response.success is True
        assert len(response.message) > 0
        assert response.conversation_id is not None
        assert response.error is None

    @pytest.mark.asyncio
    async def test_generate_response_message_not_empty(self, coach_service, mock_user):
        """Test AI response is not empty"""
        response = await coach_service.generate_response(
            user_id=mock_user['id'],
            message="Hello coach",
            coach_type='trainer'
        )

        assert len(response.message) > 10  # Should be a meaningful response
        assert isinstance(response.message, str)

    @pytest.mark.asyncio
    async def test_save_conversation_creates_new(self, coach_service, mock_user):
        """Test conversation saving creates new conversation"""
        messages = [
            {"role": "user", "content": "Hello", "timestamp": datetime.utcnow().isoformat()},
            {"role": "assistant", "content": "Hi there!", "timestamp": datetime.utcnow().isoformat()}
        ]

        conv_id = await coach_service.save_conversation(
            user_id=mock_user['id'],
            coach_type='trainer',
            messages=messages
        )

        assert conv_id is not None
        assert isinstance(conv_id, str)
        assert len(conv_id) > 0

    @pytest.mark.asyncio
    async def test_save_conversation_updates_existing(self, coach_service, mock_user, mock_conversation):
        """Test conversation saving updates existing conversation"""
        new_messages = mock_conversation['messages'] + [
            {"role": "user", "content": "Follow up", "timestamp": datetime.utcnow().isoformat()}
        ]

        conv_id = await coach_service.save_conversation(
            user_id=mock_user['id'],
            coach_type='trainer',
            messages=new_messages,
            conversation_id=mock_conversation['id']
        )

        assert conv_id == mock_conversation['id']

    @pytest.mark.asyncio
    async def test_load_conversation_returns_latest(self, coach_service, mock_user):
        """Test loading conversation returns most recent"""
        conversation = await coach_service.load_conversation(
            user_id=mock_user['id'],
            coach_type='trainer'
        )

        # Should return None or a dict with messages
        assert conversation is None or (
            isinstance(conversation, dict) and
            'messages' in conversation and
            isinstance(conversation['messages'], list)
        )

    @pytest.mark.asyncio
    async def test_validate_chat_request_valid(self):
        """Test ChatRequest validation with valid data"""
        request = ChatRequest(
            coach_type='trainer',
            message='What should I do today?'
        )

        assert request.coach_type == 'trainer'
        assert request.message == 'What should I do today?'
        assert request.conversation_id is None

    @pytest.mark.asyncio
    async def test_validate_chat_request_invalid_coach_type(self):
        """Test ChatRequest validation rejects invalid coach type"""
        with pytest.raises(ValueError):
            ChatRequest(
                coach_type='invalid',
                message='Hello'
            )

    @pytest.mark.asyncio
    async def test_validate_chat_request_empty_message(self):
        """Test ChatRequest validation rejects empty message"""
        with pytest.raises(ValueError):
            ChatRequest(
                coach_type='trainer',
                message=''
            )

    @pytest.mark.asyncio
    async def test_validate_chat_request_message_too_long(self):
        """Test ChatRequest validation rejects too-long messages"""
        long_message = 'a' * 1001
        with pytest.raises(ValueError):
            ChatRequest(
                coach_type='trainer',
                message=long_message
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
