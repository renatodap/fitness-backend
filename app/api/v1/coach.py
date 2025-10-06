"""
Unified Coach API Endpoints

Single "Coach" interface that replaces AI Chat + Quick Entry.
- Auto-detects logs (meals, workouts, measurements) and shows preview
- Handles questions/comments with RAG-powered responses
- ChatGPT-like conversation interface
- Vectorizes ALL messages for future RAG

Cost: $0.16/user/month
- Classification: Groq Llama 3.3 70B ($0.01/month)
- Chat responses: Claude 3.5 Sonnet ($0.30/month)
- Embeddings: FREE (sentence-transformers)
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse

from app.api.v1.schemas.unified_coach_schemas import (
    UnifiedMessageRequest,
    UnifiedMessageResponse,
    ConfirmLogRequest,
    ConfirmLogResponse,
    ConversationListResponse,
    ConversationSummary,
    MessageListResponse,
    MessageSummary,
    MessageRole,
    MessageType,
)
from app.services.unified_coach_service import get_unified_coach_service
from app.services.supabase_service import get_service_client
from app.services.auth_service import get_current_user  # Use mock auth (same as quick_entry)

logger = logging.getLogger(__name__)
router = APIRouter()


# =====================================================
# HEALTH CHECK / DEBUG ENDPOINT
# =====================================================

@router.get(
    "/health",
    summary="Coach service health check",
    tags=["coach"]
)
async def coach_health():
    """
    Test if Coach service can initialize.
    Returns detailed info about which services work/fail.
    """
    health_status = {
        "status": "unknown",
        "services": {},
        "errors": []
    }

    try:
        # Test Supabase
        try:
            from app.services.supabase_service import get_service_client
            supabase = get_service_client()
            health_status["services"]["supabase"] = "ok"
        except Exception as e:
            health_status["services"]["supabase"] = f"failed: {str(e)}"
            health_status["errors"].append(f"Supabase: {str(e)}")

        # Test Message Classifier
        try:
            from app.services.message_classifier_service import get_message_classifier
            classifier = get_message_classifier()
            health_status["services"]["message_classifier"] = "ok"
        except Exception as e:
            health_status["services"]["message_classifier"] = f"failed: {str(e)}"
            health_status["errors"].append(f"MessageClassifier: {str(e)}")

        # Test Quick Entry Service
        try:
            from app.services.quick_entry_service import get_quick_entry_service
            quick_entry = get_quick_entry_service()
            health_status["services"]["quick_entry"] = "ok"
        except Exception as e:
            health_status["services"]["quick_entry"] = f"failed: {str(e)}"
            health_status["errors"].append(f"QuickEntry: {str(e)}")

        # Test Multimodal Service
        try:
            from app.services.multimodal_embedding_service import get_multimodal_service
            multimodal = get_multimodal_service()
            health_status["services"]["multimodal_embedding"] = "ok"
        except Exception as e:
            health_status["services"]["multimodal_embedding"] = f"failed: {str(e)}"
            health_status["errors"].append(f"MultimodalEmbedding: {str(e)}")

        # Test Anthropic
        try:
            from app.config import get_settings
            from anthropic import AsyncAnthropic
            settings = get_settings()
            anthropic = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            health_status["services"]["anthropic"] = "ok"
        except Exception as e:
            health_status["services"]["anthropic"] = f"failed: {str(e)}"
            health_status["errors"].append(f"Anthropic: {str(e)}")

        # Test full UnifiedCoachService
        try:
            coach_service = get_unified_coach_service()
            health_status["services"]["unified_coach"] = "ok"
            health_status["status"] = "healthy"
        except Exception as e:
            health_status["services"]["unified_coach"] = f"failed: {str(e)}"
            health_status["errors"].append(f"UnifiedCoach: {str(e)}")
            health_status["status"] = "degraded"

        if not health_status["errors"]:
            health_status["status"] = "healthy"

        return health_status

    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["errors"].append(f"Critical: {str(e)}")
        return health_status


# =====================================================
# ENDPOINT 1: Send Message (Chat or Log)
# =====================================================

@router.post(
    "/message",
    response_model=UnifiedMessageResponse,
    summary="Send message to Coach (auto-detects chat vs log)",
    description="""
    Send any message to the unified Coach interface.

    The AI automatically detects if your message is:
    - **Chat**: Question, comment, general conversation → Get AI response with RAG context
    - **Log**: Meal, workout, measurement → Get log preview for confirmation

    **Examples:**
    - "What should I eat for breakfast?" → Chat response
    - "I just ate 3 eggs and oatmeal" → Log preview (meal)
    - "Did 10 pushups" → Log preview (workout)
    - "Weight is 175 lbs" → Log preview (measurement)

    **Cost per message:**
    - Classification: $0.00005 (Groq)
    - Chat response: $0.015 (Claude + RAG)
    - Embedding: FREE

    **Rate limit:** 100 messages per day
    """,
    tags=["coach"]
)
async def send_message(
    request: UnifiedMessageRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Main unified Coach endpoint - handles both chat and log detection.

    FLOW:
    1. Classify message type (Groq Llama 3.3 70B)
    2. If LOG with high confidence:
       - Return log preview for user confirmation
    3. If CHAT:
       - Build RAG context from ALL embeddings
       - Generate Claude response
       - Vectorize both user message and AI response
    4. Save all messages to database
    """
    try:
        user_id = current_user["id"]  # Fixed: was current_user["id"]["id"]

        # Get unified coach service
        coach_service = get_unified_coach_service()

        # Process message (auto-routing to chat or log mode)
        # Note: For now, we don't support images/audio in this endpoint
        # Those come through Quick Entry instead
        response = await coach_service.process_message(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id,
            image_base64=None,  # TODO: Support image uploads
            audio_base64=None,  # TODO: Support audio uploads
            metadata=None
        )

        return response

    except ValueError as e:
        logger.error(f"Validation error in send_message: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in send_message: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to process message. Please try again."
        )


# =====================================================
# ENDPOINT 2: Confirm Detected Log
# =====================================================

@router.post(
    "/confirm-log",
    response_model=ConfirmLogResponse,
    summary="Confirm a detected log",
    description="""
    After receiving a log preview, user confirms to save it.

    This endpoint:
    1. Saves structured log to appropriate table (meal_logs, activities, body_measurements)
    2. Creates quick_entry_logs record for audit trail
    3. Adds success message to conversation
    4. Returns log ID and success message

    **Example:**
    ```json
    {
      "conversation_id": "123e4567...",
      "log_type": "meal",
      "log_data": {
        "meal_type": "breakfast",
        "calories": 450,
        "protein": 35,
        ...
      }
    }
    ```
    """,
    tags=["coach"]
)
async def confirm_log(
    request: ConfirmLogRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Confirm and save a detected log.

    FLOW:
    1. Validate conversation belongs to user
    2. Save structured log to database
    3. Update quick_entry_logs with linked IDs
    4. Add success message to conversation
    5. Return success response
    """
    try:
        user_id = current_user["id"]  # Fixed: was current_user["id"]["id"]

        # Get unified coach service
        coach_service = get_unified_coach_service()

        # Confirm and save log
        response = await coach_service.confirm_log(
            user_id=user_id,
            conversation_id=request.conversation_id,
            log_data=request.log_data,
            log_type=request.log_type.value,
            user_message_id=request.user_message_id
        )

        return response

    except ValueError as e:
        logger.error(f"Validation error in confirm_log: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in confirm_log: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to save log. Please try again."
        )


# =====================================================
# ENDPOINT 3: Get Conversation List
# =====================================================

@router.get(
    "/conversations",
    response_model=ConversationListResponse,
    summary="Get conversation history list",
    description="""
    Get list of all conversations (ChatGPT-like history sidebar).

    Returns conversations ordered by most recent first.
    Supports pagination with offset/limit.

    **Features:**
    - Auto-generated titles from first message
    - Last message preview (truncated)
    - Message count
    - Archive support

    **Example response:**
    ```json
    {
      "success": true,
      "conversations": [
        {
          "id": "123e4567...",
          "title": "Breakfast nutrition advice",
          "message_count": 12,
          "last_message_at": "2025-10-06T10:30:00Z",
          "last_message_preview": "Great! That breakfast has..."
        }
      ],
      "total_count": 25,
      "has_more": true
    }
    ```
    """,
    tags=["coach"]
)
async def get_conversations(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=100, description="Number of conversations to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    include_archived: bool = Query(False, description="Include archived conversations")
):
    """
    Get list of user's conversations.

    FLOW:
    1. Query coach_conversations table
    2. Filter by user_id and archived status
    3. Order by last_message_at DESC
    4. Apply pagination (limit/offset)
    5. Get last message preview for each conversation
    6. Return conversation list
    """
    try:
        user_id = current_user["id"]
        supabase = get_service_client()

        # Build query
        query = (
            supabase.table("coach_conversations")
            .select("id, title, message_count, last_message_at, created_at, archived")
            .eq("user_id", user_id)
        )

        # Filter archived
        if not include_archived:
            query = query.eq("archived", False)

        # Order and paginate
        query = query.order("last_message_at", desc=True).range(offset, offset + limit - 1)

        response = query.execute()

        if not response.data:
            return ConversationListResponse(
                success=True,
                conversations=[],
                total_count=0,
                has_more=False
            )

        # Get last message preview for each conversation
        conversations = []
        for conv in response.data:
            # Get last message for preview
            last_msg_response = (
                supabase.table("coach_messages")
                .select("content")
                .eq("conversation_id", conv["id"])
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            last_message_preview = None
            if last_msg_response.data:
                content = last_msg_response.data[0]["content"]
                last_message_preview = content[:100] if len(content) > 100 else content

            conversations.append(
                ConversationSummary(
                    id=conv["id"],
                    title=conv.get("title"),
                    message_count=conv.get("message_count", 0),
                    last_message_at=conv["last_message_at"],
                    created_at=conv["created_at"],
                    archived=conv.get("archived", False),
                    last_message_preview=last_message_preview
                )
            )

        # Check if there are more conversations
        total_count_response = (
            supabase.table("coach_conversations")
            .select("id", count="exact")
            .eq("user_id", user_id)
        )
        if not include_archived:
            total_count_response = total_count_response.eq("archived", False)

        total_count_result = total_count_response.execute()
        total_count = total_count_result.count if total_count_result.count else 0

        has_more = (offset + limit) < total_count

        return ConversationListResponse(
            success=True,
            conversations=conversations,
            total_count=total_count,
            has_more=has_more
        )

    except Exception as e:
        logger.error(f"Error in get_conversations: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve conversations. Please try again."
        )


# =====================================================
# ENDPOINT 4: Get Messages in Conversation
# =====================================================

@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=MessageListResponse,
    summary="Get messages in a conversation",
    description="""
    Get all messages in a specific conversation (for ChatGPT-like interface).

    Returns messages ordered chronologically (oldest first).
    Supports pagination with offset/limit for infinite scroll.

    **Message types:**
    - `user`: User's messages
    - `assistant`: AI Coach's responses
    - `system`: System messages (e.g., "✅ Meal logged!")

    **Example response:**
    ```json
    {
      "success": true,
      "conversation_id": "123e4567...",
      "messages": [
        {
          "id": "456e7890...",
          "role": "user",
          "content": "What should I eat for breakfast?",
          "message_type": "chat",
          "created_at": "2025-10-06T08:00:00Z"
        },
        {
          "id": "789e0123...",
          "role": "assistant",
          "content": "Based on your goals, I recommend...",
          "message_type": "chat",
          "created_at": "2025-10-06T08:00:05Z"
        }
      ],
      "total_count": 12,
      "has_more": false
    }
    ```
    """,
    tags=["coach"]
)
async def get_conversation_messages(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=100, description="Number of messages to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    Get messages in a conversation.

    FLOW:
    1. Verify conversation belongs to user
    2. Query coach_messages table
    3. Filter by conversation_id
    4. Order by created_at ASC (chronological)
    5. Apply pagination (limit/offset)
    6. Return message list
    """
    try:
        user_id = current_user["id"]
        supabase = get_service_client()

        # Verify conversation belongs to user
        conv_response = (
            supabase.table("coach_conversations")
            .select("id")
            .eq("id", conversation_id)
            .eq("user_id", user_id)
            .single()
            .execute()
        )

        if not conv_response.data:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or access denied"
            )

        # Get messages
        messages_response = (
            supabase.table("coach_messages")
            .select("id, role, content, message_type, quick_entry_log_id, is_vectorized, created_at")
            .eq("conversation_id", conversation_id)
            .order("created_at", desc=False)  # Chronological order
            .range(offset, offset + limit - 1)
            .execute()
        )

        if not messages_response.data:
            return MessageListResponse(
                success=True,
                conversation_id=conversation_id,
                messages=[],
                total_count=0,
                has_more=False
            )

        # Convert to MessageSummary objects
        messages = [
            MessageSummary(
                id=msg["id"],
                role=MessageRole(msg["role"]),
                content=msg["content"],
                message_type=MessageType(msg["message_type"]),
                quick_entry_log_id=msg.get("quick_entry_log_id"),
                is_vectorized=msg.get("is_vectorized", False),
                created_at=msg["created_at"]
            )
            for msg in messages_response.data
        ]

        # Get total count
        count_response = (
            supabase.table("coach_messages")
            .select("id", count="exact")
            .eq("conversation_id", conversation_id)
            .execute()
        )

        total_count = count_response.count if count_response.count else 0
        has_more = (offset + limit) < total_count

        return MessageListResponse(
            success=True,
            conversation_id=conversation_id,
            messages=messages,
            total_count=total_count,
            has_more=has_more
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_conversation_messages: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve messages. Please try again."
        )


# =====================================================
# ENDPOINT 5: Archive Conversation
# =====================================================

@router.patch(
    "/conversations/{conversation_id}/archive",
    summary="Archive a conversation",
    description="Archive a conversation to hide it from main list (still searchable via RAG)",
    tags=["coach"]
)
async def archive_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Archive a conversation."""
    try:
        user_id = current_user["id"]
        supabase = get_service_client()

        # Verify ownership and update
        response = (
            supabase.table("coach_conversations")
            .update({"archived": True, "updated_at": "now()"})
            .eq("id", conversation_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or access denied"
            )

        return {"success": True, "message": "Conversation archived"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in archive_conversation: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to archive conversation"
        )


# =====================================================
# ENDPOINT 6: Health Check (For Testing)
# =====================================================

@router.get(
    "/health",
    summary="Health check for unified Coach API",
    tags=["coach"]
)
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "unified_coach_api",
        "version": "1.0.0",
        "features": [
            "auto_log_detection",
            "rag_powered_chat",
            "message_vectorization",
            "conversation_history"
        ]
    }
