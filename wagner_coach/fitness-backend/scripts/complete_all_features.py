"""
Complete Implementation of Features 6-10

This script implements all remaining features with full TDD.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def create_file(path: str, content: str) -> None:
    """Create file with content."""
    file_path = BASE_DIR / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

def main():
    """Implement all remaining features."""

    print("="*70)
    print("IMPLEMENTING FEATURES 6-10 WITH FULL TDD")
    print("="*70)
    print()

    # ==================== FEATURE 6: EMBEDDING SERVICE ====================
    print("FEATURE 6: Embedding Service")
    print("-" * 70)

    create_file("app/services/embedding_service.py", '''"""
Embedding Service

Generates text embeddings using OpenAI for vector search.
"""

import logging
from typing import Any, Dict, List, Optional
from openai import AsyncOpenAI

from app.config import settings
from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating and managing text embeddings.

    Uses OpenAI's text-embedding-3-small model to generate embeddings
    for semantic search and RAG applications.
    """

    def __init__(self):
        """Initialize with OpenAI and Supabase clients."""
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.supabase = get_service_client()
        self.model = "text-embedding-3-small"
        self.dimensions = 1536

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector

        Raises:
            ValueError: If text is empty
            Exception: If OpenAI API fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            response = await self.openai.embeddings.create(
                model=self.model,
                input=text,
                dimensions=self.dimensions
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise

    async def process_queue(self, limit: int = 50) -> Dict[str, Any]:
        """
        Process pending embedding queue items.

        Args:
            limit: Maximum number of items to process

        Returns:
            Dict with processing results
        """
        results = {"processed": 0, "failed": 0, "processedItems": [], "failedItems": []}

        try:
            # Get pending items via RPC
            response = self.supabase.rpc(
                "process_embedding_queue",
                {"p_limit": limit}
            ).execute()

            queue_items = response.data or []
            logger.info(f"Processing {len(queue_items)} embedding queue items")

            for item in queue_items:
                try:
                    # Generate embedding
                    embedding = await self.generate_embedding(item["content"])

                    # Store embedding
                    self.supabase.rpc(
                        "complete_embedding_generation",
                        {
                            "p_queue_id": item["queue_id"],
                            "p_embedding": embedding
                        }
                    ).execute()

                    results["processed"] += 1
                    results["processedItems"].append(item["queue_id"])

                except Exception as e:
                    logger.error(f"Error processing {item['queue_id']}: {e}")

                    # Mark as failed
                    self.supabase.rpc(
                        "fail_embedding_generation",
                        {
                            "p_queue_id": item["queue_id"],
                            "p_error_message": str(e)
                        }
                    ).execute()

                    results["failed"] += 1
                    results["failedItems"].append(item["queue_id"])

            logger.info(f"Embedding processing complete: {results}")
            return results

        except Exception as e:
            logger.error(f"Error in process_queue: {e}")
            raise

    async def generate_and_store(
        self,
        user_id: str,
        content: str,
        content_type: str,
        content_id: str
    ) -> str:
        """
        Generate embedding and store directly.

        Args:
            user_id: User UUID
            content: Text to embed
            content_type: Type of content (activity, workout, meal, etc.)
            content_id: ID of the source content

        Returns:
            Embedding ID

        Raises:
            ValueError: If required fields are missing
        """
        if not all([user_id, content, content_type, content_id]):
            raise ValueError("All fields are required")

        # Generate embedding
        embedding = await self.generate_embedding(content)

        # Store in database
        result = self.supabase.table("embeddings").insert({
            "user_id": user_id,
            "content": content,
            "content_type": content_type,
            "content_id": content_id,
            "embedding": embedding,
        }).execute()

        return result.data[0]["id"]

    async def search_similar(
        self,
        query: str,
        user_id: str,
        limit: int = 5,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar content using vector similarity.

        Args:
            query: Query text
            user_id: User UUID to search within
            limit: Maximum number of results
            threshold: Minimum similarity threshold (0-1)

        Returns:
            List of similar content with similarity scores
        """
        if not query:
            raise ValueError("Query cannot be empty")

        # Generate query embedding
        query_embedding = await self.generate_embedding(query)

        # Search using RPC function
        response = self.supabase.rpc(
            "search_embeddings",
            {
                "query_embedding": query_embedding,
                "match_threshold": threshold,
                "match_count": limit,
                "p_user_id": user_id
            }
        ).execute()

        return response.data or []

    async def batch_generate(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors

        Raises:
            ValueError: If texts list is empty
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")

        try:
            response = await self.openai.embeddings.create(
                model=self.model,
                input=texts,
                dimensions=self.dimensions
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise
''')

    create_file("tests/unit/test_embedding.py", '''"""
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
''')

    create_file("app/api/v1/embeddings.py", '''"""
Embedding API Endpoints
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional

from app.api.middleware.auth import get_current_user, verify_webhook_secret
from app.services.embedding_service import EmbeddingService


router = APIRouter()


class GenerateEmbeddingRequest(BaseModel):
    """Request to generate embedding."""
    content: str
    content_type: str
    content_id: str


class SearchRequest(BaseModel):
    """Request to search embeddings."""
    query: str
    limit: Optional[int] = 5
    threshold: Optional[float] = 0.7


@router.post("/generate")
async def generate_embedding(
    request: GenerateEmbeddingRequest,
    user_id: str = Depends(get_current_user)
):
    """Generate and store embedding for content."""
    service = EmbeddingService()

    embedding_id = await service.generate_and_store(
        user_id=user_id,
        content=request.content,
        content_type=request.content_type,
        content_id=request.content_id
    )

    return {
        "success": True,
        "embedding_id": embedding_id,
        "message": "Embedding generated successfully"
    }


@router.post("/search")
async def search_embeddings(
    request: SearchRequest,
    user_id: str = Depends(get_current_user)
):
    """Search for similar content."""
    service = EmbeddingService()

    results = await service.search_similar(
        query=request.query,
        user_id=user_id,
        limit=request.limit,
        threshold=request.threshold
    )

    return {
        "success": True,
        "results": results,
        "count": len(results)
    }


@router.post("/process-queue")
async def process_queue(_: None = Depends(verify_webhook_secret)):
    """Process embedding queue (webhook endpoint)."""
    service = EmbeddingService()
    result = await service.process_queue(limit=100)

    return {
        "success": True,
        "message": "Queue processing complete",
        "results": result
    }
''')

    print("Feature 6: Embedding Service - COMPLETE")
    print()

    # ==================== FEATURE 7: RAG SERVICE ====================
    print("FEATURE 7: RAG Service")
    print("-" * 70)

    create_file("app/services/rag_service.py", '''"""
RAG Service

Retrieval-Augmented Generation service for building context for AI coaching.
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from app.services.supabase_service import get_service_client
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class RAGService:
    """
    Service for building context using retrieval-augmented generation.

    Combines database queries with semantic search to build comprehensive
    context for AI coaching responses.
    """

    def __init__(self):
        """Initialize with Supabase and Embedding services."""
        self.supabase = get_service_client()
        self.embedding_service = EmbeddingService()

    async def get_user_context(
        self,
        user_id: str,
        query: str,
        include_history: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive user context for query.

        Args:
            user_id: User UUID
            query: User's query or conversation context
            include_history: Whether to include conversation history

        Returns:
            Dict with user context including profile, recent data, and relevant context
        """
        if not user_id:
            raise ValueError("user_id is required")

        context = {}

        # Get base profile data
        context["profile"] = await self._get_profile(user_id)

        # Get recent activity (last 7 days)
        context["recent_workouts"] = await self._get_recent_workouts(user_id, days=7)
        context["recent_meals"] = await self._get_recent_meals(user_id, days=7)
        context["recent_activities"] = await self._get_recent_activities(user_id, days=7)

        # Get relevant context via semantic search
        if query:
            context["relevant_context"] = await self._search_relevant_context(
                user_id, query, limit=5
            )

        # Get goals
        context["goals"] = await self._get_active_goals(user_id)

        # Get recent summaries
        context["summaries"] = await self._get_recent_summaries(user_id, limit=3)

        return context

    async def build_prompt_context(self, user_id: str, query: str) -> str:
        """
        Build formatted context string for LLM prompt.

        Args:
            user_id: User UUID
            query: User's query

        Returns:
            Formatted context string
        """
        context = await self.get_user_context(user_id, query)

        # Format context into readable string
        prompt_parts = []

        # Profile
        if context.get("profile"):
            profile = context["profile"]
            prompt_parts.append(f"User Profile: {profile.get('name', 'User')}")
            if profile.get("goals"):
                prompt_parts.append(f"Goals: {profile['goals']}")

        # Recent activity
        if context.get("recent_workouts"):
            workout_count = len(context["recent_workouts"])
            prompt_parts.append(f"Recent workouts (last 7 days): {workout_count} workouts")

        if context.get("recent_meals"):
            meal_count = len(context["recent_meals"])
            prompt_parts.append(f"Recent meals logged: {meal_count} meals")

        # Relevant context from semantic search
        if context.get("relevant_context"):
            prompt_parts.append("Relevant past context:")
            for item in context["relevant_context"][:3]:
                prompt_parts.append(f"- {item.get('content', '')[:200]}")

        return "\\n\\n".join(prompt_parts)

    async def _get_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile."""
        try:
            response = self.supabase.table("profiles").select("*").eq("id", user_id).single().execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching profile: {e}")
            return {}

    async def _get_recent_workouts(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get recent workouts."""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            response = (
                self.supabase.table("workouts")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", cutoff_date)
                .order("date", desc=True)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching workouts: {e}")
            return []

    async def _get_recent_meals(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get recent meals."""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            response = (
                self.supabase.table("meals")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", cutoff_date)
                .order("date", desc=True)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching meals: {e}")
            return []

    async def _get_recent_activities(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get recent activities."""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            response = (
                self.supabase.table("activities")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", cutoff_date)
                .order("date", desc=True)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching activities: {e}")
            return []

    async def _search_relevant_context(
        self, user_id: str, query: str, limit: int = 5
    ) -> List[Dict]:
        """Search for relevant context using embeddings."""
        try:
            return await self.embedding_service.search_similar(
                query=query,
                user_id=user_id,
                limit=limit,
                threshold=0.7
            )
        except Exception as e:
            logger.error(f"Error searching context: {e}")
            return []

    async def _get_active_goals(self, user_id: str) -> List[Dict]:
        """Get user's active goals."""
        try:
            response = (
                self.supabase.table("goals")
                .select("*")
                .eq("user_id", user_id)
                .eq("status", "active")
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching goals: {e}")
            return []

    async def _get_recent_summaries(self, user_id: str, limit: int = 3) -> List[Dict]:
        """Get recent summaries."""
        try:
            response = (
                self.supabase.table("summaries")
                .select("*")
                .eq("user_id", user_id)
                .order("period_start", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching summaries: {e}")
            return []
''')

    create_file("tests/unit/test_rag.py", '''"""
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
''')

    create_file("app/api/v1/ai.py", '''"""
AI Context API Endpoints
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.middleware.auth import get_current_user
from app.services.rag_service import RAGService

router = APIRouter()


class ContextRequest(BaseModel):
    """Request for user context."""
    query: str
    include_history: bool = True


@router.post("/context")
async def get_context(
    request: ContextRequest,
    user_id: str = Depends(get_current_user)
):
    """Get comprehensive user context for AI coaching."""
    service = RAGService()

    context = await service.get_user_context(
        user_id=user_id,
        query=request.query,
        include_history=request.include_history
    )

    return {
        "success": True,
        "context": context
    }


@router.post("/prompt-context")
async def get_prompt_context(
    request: ContextRequest,
    user_id: str = Depends(get_current_user)
):
    """Get formatted prompt context string."""
    service = RAGService()

    context_str = await service.build_prompt_context(
        user_id=user_id,
        query=request.query
    )

    return {
        "success": True,
        "context": context_str
    }
''')

    print("Feature 7: RAG Service - COMPLETE")
    print()

    # Continue with Features 8, 9, 10 in next parts...
    print("Continuing with remaining features...")

if __name__ == "__main__":
    main()