"""
Unit tests for Embedding Service
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from app.services.embedding_service import EmbeddingService


@pytest.fixture
def mock_openai(mocker):
    """Mock OpenAI client."""
    mock_client = AsyncMock()
    mock_response = Mock()
    mock_response.data = [Mock(embedding=[0.1] * 1536)]
    mock_client.embeddings.create.return_value = mock_response

    mocker.patch(
        "app.services.embedding_service.AsyncOpenAI",
        return_value=mock_client
    )
    return mock_client


@pytest.fixture
def mock_supabase(mocker):
    """Mock Supabase client."""
    mock_client = Mock()
    mock_client.rpc().execute.return_value = Mock(data=[])
    mock_client.table().insert().execute.return_value = Mock(data=[{"id": "test-id"}])

    mocker.patch(
        "app.services.embedding_service.get_service_client",
        return_value=mock_client
    )
    return mock_client


@pytest.fixture
def service(mock_openai, mock_supabase):
    """Create EmbeddingService instance."""
    return EmbeddingService()


# Test initialization
def test_service_initialization(service):
    """Test service initializes correctly."""
    assert service.openai is not None
    assert service.supabase is not None
    assert service.model == "text-embedding-3-small"
    assert service.dimensions == 1536


# Test generate_embedding
@pytest.mark.asyncio
async def test_generate_embedding_success(service, mock_openai):
    """Test successful embedding generation."""
    embedding = await service.generate_embedding("test text")

    assert isinstance(embedding, list)
    assert len(embedding) == 1536
    mock_openai.embeddings.create.assert_called_once()


@pytest.mark.asyncio
async def test_generate_embedding_empty_text(service):
    """Test error handling for empty text."""
    with pytest.raises(ValueError) as exc_info:
        await service.generate_embedding("")

    assert "empty" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_generate_embedding_whitespace_only(service):
    """Test error handling for whitespace-only text."""
    with pytest.raises(ValueError):
        await service.generate_embedding("   ")


# Test process_queue
@pytest.mark.asyncio
async def test_process_queue_empty(service, mock_supabase):
    """Test processing empty queue."""
    mock_supabase.rpc().execute.return_value = Mock(data=[])

    result = await service.process_queue()

    assert result["processed"] == 0
    assert result["failed"] == 0


@pytest.mark.asyncio
async def test_process_queue_with_items(service, mock_supabase):
    """Test processing queue with items."""
    mock_supabase.rpc().execute.return_value = Mock(data=[
        {"queue_id": "q1", "content": "test 1"},
        {"queue_id": "q2", "content": "test 2"}
    ])

    result = await service.process_queue(limit=10)

    assert result["processed"] == 2
    assert result["failed"] == 0
    assert len(result["processedItems"]) == 2


# Test generate_and_store
@pytest.mark.asyncio
async def test_generate_and_store_success(service, mock_supabase):
    """Test generating and storing embedding."""
    embedding_id = await service.generate_and_store(
        user_id="user-123",
        content="test content",
        content_type="activity",
        content_id="activity-123"
    )

    assert embedding_id == "test-id"
    mock_supabase.table().insert().execute.assert_called_once()


@pytest.mark.asyncio
async def test_generate_and_store_missing_fields(service):
    """Test error handling for missing required fields."""
    with pytest.raises(ValueError):
        await service.generate_and_store("", "content", "type", "id")


# Test search_similar
@pytest.mark.asyncio
async def test_search_similar_success(service, mock_supabase):
    """Test similarity search."""
    mock_supabase.rpc().execute.return_value = Mock(data=[
        {"content": "similar 1", "similarity": 0.9},
        {"content": "similar 2", "similarity": 0.85}
    ])

    results = await service.search_similar(
        query="test query",
        user_id="user-123",
        limit=5
    )

    assert len(results) == 2
    mock_supabase.rpc.assert_called_once()


@pytest.mark.asyncio
async def test_search_similar_empty_query(service):
    """Test error handling for empty query."""
    with pytest.raises(ValueError):
        await service.search_similar("", "user-123")


# Test batch_generate
@pytest.mark.asyncio
async def test_batch_generate_success(service, mock_openai):
    """Test batch embedding generation."""
    mock_openai.embeddings.create.return_value = Mock(
        data=[
            Mock(embedding=[0.1] * 1536),
            Mock(embedding=[0.2] * 1536),
            Mock(embedding=[0.3] * 1536),
        ]
    )

    texts = ["text 1", "text 2", "text 3"]
    embeddings = await service.batch_generate(texts)

    assert len(embeddings) == 3
    assert all(len(e) == 1536 for e in embeddings)


@pytest.mark.asyncio
async def test_batch_generate_empty_list(service):
    """Test error handling for empty text list."""
    with pytest.raises(ValueError):
        await service.batch_generate([])
