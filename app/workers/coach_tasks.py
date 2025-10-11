"""
Celery Background Tasks for AI Coach

Handles non-critical operations asynchronously to keep responses FAST:
- Message vectorization (for RAG)
- Analytics updates
- Conversation summarization
- Cache warming
- Database cleanup

These tasks run in the background AFTER responding to the user.
"""

import logging
from datetime import datetime
from typing import Dict, Any

from app.workers.celery_app import celery_app
from app.services.supabase_service import get_service_client
from app.services.multimodal_embedding_service import get_multimodal_service

logger = logging.getLogger(__name__)


@celery_app.task(name="coach_tasks.vectorize_message")
def vectorize_message(
    user_id: str,
    message_id: str,
    content: str,
    role: str
):
    """
    Vectorize message for RAG (background task).

    This is SLOW (~200-500ms) so we do it AFTER responding to user.

    Args:
        user_id: User UUID
        message_id: Message UUID
        content: Message text
        role: "user" or "assistant"
    """
    try:
        logger.info(f"[Celery:vectorize_message] START - message_id: {message_id}, role: {role}")

        supabase = get_service_client()
        embedding_service = get_multimodal_service()

        # Generate embedding (BLOCKING but in background)
        embedding = embedding_service.embed_text_sync(content)  # Sync version for Celery

        # Store in coach_message_embeddings
        embedding_data = {
            "message_id": message_id,
            "user_id": user_id,
            "role": role,
            "embedding": embedding.tolist() if hasattr(embedding, 'tolist') else embedding,
            "content_text": content[:5000],  # Truncate for storage
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "created_at": datetime.utcnow().isoformat()
        }

        supabase.table("coach_message_embeddings").insert(embedding_data).execute()

        # Update message with vectorization flag
        supabase.table("coach_messages").update({
            "is_vectorized": True
        }).eq("id", message_id).execute()

        logger.info(f"[Celery:vectorize_message] SUCCESS - message_id: {message_id}")

    except Exception as e:
        logger.error(f"[Celery:vectorize_message] FAILED - message_id: {message_id}, error: {e}", exc_info=True)
        raise  # Let Celery handle retry


@celery_app.task(name="coach_tasks.update_conversation_analytics")
def update_conversation_analytics(
    user_id: str,
    conversation_id: str
):
    """
    Update conversation analytics (background task).

    Updates:
    - Message count
    - Last message timestamp
    - Conversation title (if not set)

    Args:
        user_id: User UUID
        conversation_id: Conversation UUID
    """
    try:
        logger.info(f"[Celery:update_analytics] START - conversation_id: {conversation_id}")

        supabase = get_service_client()

        # Get message count
        messages = supabase.table("coach_messages")\
            .select("id, content, created_at")\
            .eq("conversation_id", conversation_id)\
            .execute()

        message_count = len(messages.data) if messages.data else 0
        last_message_at = messages.data[-1]["created_at"] if messages.data else datetime.utcnow().isoformat()

        # Generate conversation title if not set (use first user message)
        conversation = supabase.table("coach_conversations")\
            .select("title")\
            .eq("id", conversation_id)\
            .single()\
            .execute()

        title = conversation.data.get("title") if conversation.data else None

        if not title and messages.data:
            # Use first user message as title (truncated)
            first_message = next((msg for msg in messages.data if msg.get("role") == "user"), None)
            if first_message:
                title = first_message["content"][:50] + ("..." if len(first_message["content"]) > 50 else "")

        # Update conversation
        update_data = {
            "message_count": message_count,
            "last_message_at": last_message_at
        }

        if title:
            update_data["title"] = title

        supabase.table("coach_conversations").update(update_data).eq("id", conversation_id).execute()

        logger.info(f"[Celery:update_analytics] SUCCESS - conversation_id: {conversation_id}, {message_count} messages")

    except Exception as e:
        logger.error(f"[Celery:update_analytics] FAILED - conversation_id: {conversation_id}, error: {e}", exc_info=True)
        raise


@celery_app.task(name="coach_tasks.summarize_conversation")
def summarize_conversation(
    conversation_id: str
):
    """
    Generate conversation summary (background task).

    For long conversations (>20 messages), generate a compressed summary
    to save tokens on future requests.

    Args:
        conversation_id: Conversation UUID
    """
    try:
        logger.info(f"[Celery:summarize] START - conversation_id: {conversation_id}")

        supabase = get_service_client()

        # Get all messages
        messages = supabase.table("coach_messages")\
            .select("*")\
            .eq("conversation_id", conversation_id)\
            .order("created_at", desc=False)\
            .execute()

        if not messages.data or len(messages.data) < 20:
            logger.info(f"[Celery:summarize] Skipping - only {len(messages.data or [])} messages")
            return

        # TODO: Use Claude to generate summary
        # For now, just create a simple summary
        user_messages = [m for m in messages.data if m.get("role") == "user"]
        ai_messages = [m for m in messages.data if m.get("role") == "assistant"]

        summary = f"""Conversation Summary:
- Total messages: {len(messages.data)}
- User messages: {len(user_messages)}
- AI responses: {len(ai_messages)}
- Started: {messages.data[0].get('created_at')}
- Last activity: {messages.data[-1].get('created_at')}

Key topics discussed: (AI summary would go here)
"""

        # Store summary
        summary_data = {
            "conversation_id": conversation_id,
            "summary": summary,
            "message_count_at_summary": len(messages.data),
            "created_at": datetime.utcnow().isoformat()
        }

        supabase.table("coach_conversation_summaries").insert(summary_data).execute()

        logger.info(f"[Celery:summarize] SUCCESS - conversation_id: {conversation_id}")

    except Exception as e:
        logger.error(f"[Celery:summarize] FAILED - conversation_id: {conversation_id}, error: {e}", exc_info=True)
        raise


@celery_app.task(name="coach_tasks.warm_user_cache")
def warm_user_cache(
    user_id: str
):
    """
    Warm caches for user (background task).

    Pre-loads frequently accessed data to speed up future requests:
    - User profile
    - Recent nutrition summary
    - Recent activity summary

    Args:
        user_id: User UUID
    """
    try:
        logger.info(f"[Celery:warm_cache] START - user_id: {user_id}")

        supabase = get_service_client()

        # Pre-load profile (triggers Supabase cache)
        supabase.table("profiles").select("*").eq("id", user_id).single().execute()

        # Pre-load recent meals
        supabase.table("meals")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("logged_at", desc=True)\
            .limit(10)\
            .execute()

        # Pre-load recent activities
        supabase.table("activities")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("started_at", desc=True)\
            .limit(10)\
            .execute()

        logger.info(f"[Celery:warm_cache] SUCCESS - user_id: {user_id}")

    except Exception as e:
        logger.error(f"[Celery:warm_cache] FAILED - user_id: {user_id}, error: {e}", exc_info=True)
        # Don't raise - cache warming is best-effort


@celery_app.task(name="coach_tasks.cleanup_old_embeddings")
def cleanup_old_embeddings(days_old: int = 90):
    """
    Clean up old embeddings (background task).

    Deletes embeddings older than N days to save storage.

    Args:
        days_old: Delete embeddings older than this many days
    """
    try:
        logger.info(f"[Celery:cleanup] START - deleting embeddings older than {days_old} days")

        supabase = get_service_client()

        cutoff_date = (datetime.utcnow() - timedelta(days=days_old)).isoformat()

        # Delete old embeddings
        result = supabase.table("coach_message_embeddings")\
            .delete()\
            .lt("created_at", cutoff_date)\
            .execute()

        deleted_count = len(result.data) if result.data else 0

        logger.info(f"[Celery:cleanup] SUCCESS - deleted {deleted_count} old embeddings")

    except Exception as e:
        logger.error(f"[Celery:cleanup] FAILED - error: {e}", exc_info=True)
        raise


# Helper: Batch vectorization for multiple messages
@celery_app.task(name="coach_tasks.batch_vectorize_messages")
def batch_vectorize_messages(
    messages: list[Dict[str, Any]]
):
    """
    Vectorize multiple messages in one task (more efficient).

    Args:
        messages: List of {user_id, message_id, content, role}
    """
    try:
        logger.info(f"[Celery:batch_vectorize] START - {len(messages)} messages")

        for msg in messages:
            try:
                vectorize_message(
                    user_id=msg["user_id"],
                    message_id=msg["message_id"],
                    content=msg["content"],
                    role=msg["role"]
                )
            except Exception as e:
                logger.error(f"[Celery:batch_vectorize] Failed for message {msg['message_id']}: {e}")
                # Continue with other messages

        logger.info(f"[Celery:batch_vectorize] SUCCESS - {len(messages)} messages")

    except Exception as e:
        logger.error(f"[Celery:batch_vectorize] FAILED - error: {e}", exc_info=True)
        raise
