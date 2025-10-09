"""
Coach Service Interface Definition
Following TDD: This defines the contract for the coach service
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from app.api.v1.schemas.coach_schemas import (
    ChatResponse,
    UserContext,
    CoachPersona
)


class ICoachService(ABC):
    """Interface for Coach Service"""

    @abstractmethod
    async def get_persona(self, coach_type: str) -> Optional[CoachPersona]:
        """
        Retrieve coach persona by type

        Args:
            coach_type: 'trainer' or 'nutritionist'

        Returns:
            CoachPersona object or None if not found
        """
        pass

    @abstractmethod
    async def build_context(
        self,
        user_id: str,
        message: str,
        coach_type: str
    ) -> UserContext:
        """
        Build complete user context for AI coach

        Args:
            user_id: User's UUID
            message: User's current message
            coach_type: Type of coach

        Returns:
            UserContext with all relevant user data
        """
        pass

    @abstractmethod
    async def generate_response(
        self,
        user_id: str,
        message: str,
        coach_type: str,
        conversation_id: Optional[str] = None
    ) -> ChatResponse:
        """
        Generate AI coach response

        Args:
            user_id: User's UUID
            message: User's message
            coach_type: Type of coach
            conversation_id: Optional conversation ID

        Returns:
            ChatResponse with AI's message
        """
        pass

    @abstractmethod
    async def save_conversation(
        self,
        user_id: str,
        coach_type: str,
        messages: List[Dict[str, Any]],
        conversation_id: Optional[str] = None
    ) -> str:
        """
        Save conversation to database

        Args:
            user_id: User's UUID
            coach_type: Type of coach
            messages: List of message dicts
            conversation_id: Optional conversation ID for updates

        Returns:
            Conversation ID (UUID)
        """
        pass

    @abstractmethod
    async def load_conversation(
        self,
        user_id: str,
        coach_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Load most recent conversation

        Args:
            user_id: User's UUID
            coach_type: Type of coach

        Returns:
            Conversation dict or None
        """
        pass


class IRAGService(ABC):
    """Interface for RAG (Retrieval-Augmented Generation) Service"""

    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text

        Args:
            text: Input text

        Returns:
            List of floats (embedding vector)
        """
        pass

    @abstractmethod
    async def search_embeddings(
        self,
        user_id: str,
        query: str,
        limit: int = 10,
        threshold: float = 0.7,
        source_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings

        Args:
            user_id: User's UUID
            query: Search query
            limit: Max number of results
            threshold: Minimum similarity score
            source_types: Filter by source types

        Returns:
            List of embedding results with content and similarity scores
        """
        pass

    @abstractmethod
    async def store_embedding(
        self,
        user_id: str,
        content: str,
        source_type: str,
        source_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store embedding in database

        Args:
            user_id: User's UUID
            content: Text content
            source_type: Type of source (workout, meal, etc.)
            source_id: ID of source record
            metadata: Optional metadata dict

        Returns:
            Embedding ID (UUID)
        """
        pass
