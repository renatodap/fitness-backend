"""
Conversation Memory Service - Advanced Context Management

Provides intelligent conversation history retrieval with:
- Sliding window (recent messages, full detail)
- Semantic retrieval (relevant past messages via RAG)
- Automatic summarization (compress old conversations)
- Token-aware loading (dynamic context budgeting)

This replaces the simple "last 10 messages" approach with a hybrid system
that balances recency + relevance + token efficiency.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from app.services.supabase_service import get_service_client
from app.services.multimodal_embedding_service import get_multimodal_service

logger = logging.getLogger(__name__)


class ConversationMemoryService:
    """
    Advanced conversation memory management.

    Strategy:
    1. Recent window: Last N messages (full detail)
    2. Semantic search: Most relevant past messages
    3. Summary: Compressed version of very old messages
    4. Token budget: Dynamically adjust based on available tokens
    """

    def __init__(self):
        self.supabase = get_service_client()
        self.embedding_service = get_multimodal_service()

        # Memory configuration
        self.recent_window_size = 10  # Last 10 messages (full detail)
        self.semantic_search_count = 5  # Top 5 relevant messages
        self.max_total_messages = 20  # Hard limit
        self.summary_threshold_days = 7  # Summarize conversations older than 7 days

    async def get_conversation_context(
        self,
        user_id: str,
        conversation_id: str,
        current_message: str,
        token_budget: int = 2000
    ) -> Dict[str, Any]:
        """
        Get optimal conversation context with hybrid retrieval.

        Args:
            user_id: User's UUID
            conversation_id: Conversation UUID
            current_message: Current user message (for semantic search)
            token_budget: Available tokens for context (default 2000)

        Returns:
            {
                "recent_messages": [...],  # Last N messages
                "relevant_messages": [...],  # Semantically similar messages
                "summary": str | None,  # Summary of old messages (if exists)
                "token_count": int,  # Estimated tokens used
                "strategy_used": str  # Which retrieval strategy was used
            }
        """
        logger.info(f"[ConversationMemory] Getting context for conversation {conversation_id}")

        try:
            # STEP 1: Get recent messages (sliding window)
            recent_messages = await self._get_recent_messages(
                user_id,
                conversation_id,
                limit=self.recent_window_size
            )

            logger.info(f"[ConversationMemory] Found {len(recent_messages)} recent messages")

            # STEP 2: Get semantically relevant messages (excluding recent ones)
            relevant_messages = []
            if current_message and len(recent_messages) > 0:
                # Only do semantic search if we have some conversation history
                relevant_messages = await self._get_relevant_messages(
                    user_id,
                    conversation_id,
                    query=current_message,
                    exclude_recent=self.recent_window_size,
                    limit=self.semantic_search_count
                )

                logger.info(f"[ConversationMemory] Found {len(relevant_messages)} semantically relevant messages")

            # STEP 3: Get conversation summary (if available)
            summary = await self._get_conversation_summary(conversation_id)

            # STEP 4: Estimate token usage
            estimated_tokens = self._estimate_tokens(recent_messages, relevant_messages, summary)

            logger.info(f"[ConversationMemory] Estimated tokens: {estimated_tokens}/{token_budget}")

            # STEP 5: Trim if over budget
            if estimated_tokens > token_budget:
                logger.warning(f"[ConversationMemory] Over budget, trimming context...")
                recent_messages, relevant_messages = self._trim_to_budget(
                    recent_messages,
                    relevant_messages,
                    token_budget
                )
                estimated_tokens = self._estimate_tokens(recent_messages, relevant_messages, summary)
                logger.info(f"[ConversationMemory] After trimming: {estimated_tokens} tokens")

            return {
                "recent_messages": recent_messages,
                "relevant_messages": relevant_messages,
                "summary": summary,
                "token_count": estimated_tokens,
                "strategy_used": "hybrid_retrieval"
            }

        except Exception as e:
            logger.error(f"[ConversationMemory] Failed to get context: {e}", exc_info=True)
            return {
                "recent_messages": [],
                "relevant_messages": [],
                "summary": None,
                "token_count": 0,
                "strategy_used": "error_fallback"
            }

    async def _get_recent_messages(
        self,
        user_id: str,
        conversation_id: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Get last N messages from conversation (chronological)."""
        try:
            response = self.supabase.table("coach_messages")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("conversation_id", conversation_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()

            # Reverse to get chronological order (oldest first)
            messages = list(reversed(response.data)) if response.data else []

            return messages

        except Exception as e:
            logger.error(f"[ConversationMemory] Failed to get recent messages: {e}")
            return []

    async def _get_relevant_messages(
        self,
        user_id: str,
        conversation_id: str,
        query: str,
        exclude_recent: int,
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Get semantically relevant messages using RAG.

        Args:
            user_id: User UUID
            conversation_id: Conversation UUID
            query: Current message to find relevant context for
            exclude_recent: Number of recent messages to exclude
            limit: Max relevant messages to return

        Returns:
            List of relevant messages with similarity scores
        """
        try:
            # Generate embedding for current message
            query_embedding = await self.embedding_service.embed_text(query)
            embedding_list = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else query_embedding

            # Get IDs of recent messages to exclude
            recent_msgs = await self.supabase.table("coach_messages")\
                .select("id")\
                .eq("conversation_id", conversation_id)\
                .order("created_at", desc=True)\
                .limit(exclude_recent)\
                .execute()

            exclude_ids = [msg["id"] for msg in (recent_msgs.data or [])]

            # Semantic search in coach_message_embeddings
            # This requires a pgvector function search_coach_messages
            try:
                response = await self.supabase.rpc(
                    "search_coach_messages",
                    {
                        "query_embedding": embedding_list,
                        "conversation_id_filter": conversation_id,
                        "user_id_filter": user_id,
                        "exclude_message_ids": exclude_ids,
                        "match_threshold": 0.5,
                        "match_count": limit
                    }
                ).execute()

                return response.data if response.data else []

            except Exception as rpc_err:
                logger.warning(f"[ConversationMemory] RPC search failed (function may not exist): {rpc_err}")
                # Fallback: Just get oldest messages if semantic search not available
                return await self._get_oldest_messages(user_id, conversation_id, exclude_recent, limit)

        except Exception as e:
            logger.error(f"[ConversationMemory] Failed to get relevant messages: {e}")
            return []

    async def _get_oldest_messages(
        self,
        user_id: str,
        conversation_id: str,
        skip: int,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Fallback: Get oldest messages when semantic search unavailable."""
        try:
            response = self.supabase.table("coach_messages")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("conversation_id", conversation_id)\
                .order("created_at", desc=False)\
                .offset(skip)\
                .limit(limit)\
                .execute()

            return response.data if response.data else []

        except Exception as e:
            logger.error(f"[ConversationMemory] Failed to get oldest messages: {e}")
            return []

    async def _get_conversation_summary(self, conversation_id: str) -> Optional[str]:
        """
        Get conversation summary if it exists.

        Summaries are generated for conversations older than threshold_days.
        """
        try:
            response = self.supabase.table("coach_conversation_summaries")\
                .select("summary")\
                .eq("conversation_id", conversation_id)\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()

            if response.data:
                return response.data[0]["summary"]

            return None

        except Exception as e:
            logger.warning(f"[ConversationMemory] Failed to get summary (table may not exist): {e}")
            return None

    def _estimate_tokens(
        self,
        recent_messages: List[Dict[str, Any]],
        relevant_messages: List[Dict[str, Any]],
        summary: Optional[str]
    ) -> int:
        """
        Estimate token count for context.

        Rough approximation: 1 token ≈ 4 characters
        """
        total_chars = 0

        # Recent messages
        for msg in recent_messages:
            content = msg.get("content", "")
            total_chars += len(str(content))

        # Relevant messages
        for msg in relevant_messages:
            content = msg.get("content", "")
            total_chars += len(str(content))

        # Summary
        if summary:
            total_chars += len(summary)

        # Convert chars to tokens (rough estimate)
        estimated_tokens = int(total_chars / 4)

        return estimated_tokens

    def _trim_to_budget(
        self,
        recent_messages: List[Dict[str, Any]],
        relevant_messages: List[Dict[str, Any]],
        token_budget: int
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Trim messages to fit within token budget.

        Priority:
        1. Always keep most recent messages
        2. Trim relevant messages first
        3. If still over, trim oldest recent messages
        """
        # Calculate current usage
        current_tokens = self._estimate_tokens(recent_messages, relevant_messages, None)

        # If under budget, return as is
        if current_tokens <= token_budget:
            return recent_messages, relevant_messages

        # STEP 1: Try removing relevant messages
        logger.info("[ConversationMemory] Trimming relevant messages...")
        while relevant_messages and current_tokens > token_budget:
            relevant_messages.pop()
            current_tokens = self._estimate_tokens(recent_messages, relevant_messages, None)

        # STEP 2: If still over, trim oldest recent messages
        if current_tokens > token_budget:
            logger.warning("[ConversationMemory] Still over budget, trimming recent messages...")
            while len(recent_messages) > 3 and current_tokens > token_budget:  # Keep at least 3
                recent_messages.pop(0)  # Remove oldest
                current_tokens = self._estimate_tokens(recent_messages, relevant_messages, None)

        return recent_messages, relevant_messages

    def format_context_for_claude(
        self,
        context: Dict[str, Any]
    ) -> str:
        """
        Format retrieved context for Claude's consumption.

        Returns formatted string with:
        - Summary (if exists)
        - Relevant past context (if any)
        - Recent conversation history
        """
        parts = []

        # Add summary first (if exists)
        if context.get("summary"):
            parts.append("=== CONVERSATION SUMMARY ===")
            parts.append(context["summary"])
            parts.append("")

        # Add relevant messages (if any)
        if context.get("relevant_messages"):
            parts.append("=== RELEVANT PAST CONTEXT ===")
            for msg in context["relevant_messages"]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                timestamp = msg.get("created_at", "")
                parts.append(f"[{role.upper()}] ({timestamp}): {content}")
            parts.append("")

        # Add recent messages
        if context.get("recent_messages"):
            parts.append("=== RECENT CONVERSATION ===")
            for msg in context["recent_messages"]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                parts.append(f"[{role.upper()}]: {content}")

        return "\n".join(parts)


# Singleton instance
_conversation_memory_service: Optional[ConversationMemoryService] = None


def get_conversation_memory_service() -> ConversationMemoryService:
    """Get the global ConversationMemoryService instance."""
    global _conversation_memory_service
    if _conversation_memory_service is None:
        _conversation_memory_service = ConversationMemoryService()
    return _conversation_memory_service
