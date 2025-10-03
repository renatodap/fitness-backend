"""
Unit tests for RAG Service
"""

import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta

from app.services.rag_service import RAGService


@pytest.fixture
def mock_supabase(mocker):
    """Mock Supabase client."""
    mock_client = Mock()
    mock_client.table().select().eq().single().execute.return_value = Mock(
        data={"id": "user-123", "name": "Test User"}
    )
    mock_client.table().select().eq().gte().order().execute.return_value = Mock(data=[])

    mocker.patch(
        "app.services.rag_service.get_service_client",
        return_value=mock_client
    )
    return mock_client


@pytest.fixture
def mock_embedding_service(mocker):
    """Mock EmbeddingService."""
    mock_service = Mock()
    mock_service.search_similar = AsyncMock(return_value=[])

    mocker.patch(
        "app.services.rag_service.EmbeddingService",
        return_value=mock_service
    )
    return mock_service


@pytest.fixture
def service(mock_supabase, mock_embedding_service):
    """Create RAGService instance."""
    return RAGService()


# Test initialization
def test_service_initialization(service):
    """Test service initializes correctly."""
    assert service.supabase is not None
    assert service.embedding_service is not None


# Test get_user_context
@pytest.mark.asyncio
async def test_get_user_context_success(service):
    """Test getting user context."""
    context = await service.get_user_context("user-123", "test query")

    assert "profile" in context
    assert "recent_workouts" in context
    assert "recent_meals" in context
    assert "recent_activities" in context
    assert "relevant_context" in context
    assert "goals" in context
    assert "summaries" in context


@pytest.mark.asyncio
async def test_get_user_context_no_user_id(service):
    """Test error handling for missing user_id."""
    with pytest.raises(ValueError):
        await service.get_user_context("", "query")


# Test build_prompt_context
@pytest.mark.asyncio
async def test_build_prompt_context(service, mock_supabase):
    """Test building formatted prompt context."""
    mock_supabase.table().select().eq().single().execute.return_value = Mock(
        data={"id": "user-123", "name": "Test User", "goals": "Lose weight"}
    )

    context_str = await service.build_prompt_context("user-123", "test query")

    assert isinstance(context_str, str)
    assert len(context_str) > 0


# Test helper methods
@pytest.mark.asyncio
async def test_get_profile(service, mock_supabase):
    """Test getting user profile."""
    profile = await service._get_profile("user-123")

    assert profile["id"] == "user-123"
    assert profile["name"] == "Test User"


@pytest.mark.asyncio
async def test_get_recent_workouts(service, mock_supabase):
    """Test getting recent workouts."""
    mock_supabase.table().select().eq().gte().order().execute.return_value = Mock(
        data=[{"id": "w1", "type": "cardio"}]
    )

    workouts = await service._get_recent_workouts("user-123", days=7)

    assert len(workouts) == 1


@pytest.mark.asyncio
async def test_search_relevant_context(service, mock_embedding_service):
    """Test searching relevant context."""
    mock_embedding_service.search_similar.return_value = [
        {"content": "relevant 1", "similarity": 0.9}
    ]

    results = await service._search_relevant_context("user-123", "query")

    assert len(results) == 1
    mock_embedding_service.search_similar.assert_called_once()
