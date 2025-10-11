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
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from pydantic import BaseModel, Field

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
from app.api.middleware.rate_limit import coach_chat_rate_limit

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

    **Rate limit:** 100 messages per day (enforced)
    """,
    tags=["coach"]
)
@coach_chat_rate_limit()
async def send_message(
    request: UnifiedMessageRequest,
    background_tasks: BackgroundTasks,
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
       - Vectorize both user message and AI response (in background for speed!)
    4. Save all messages to database
    """
    logger.info("[COACH_ENDPOINT] Received message request")

    try:
        # STEP 1: Extract user ID with detailed logging
        logger.info(f"[COACH_ENDPOINT] Current user data: {current_user}")

        if not current_user:
            logger.error("[COACH_ENDPOINT] current_user is None")
            raise HTTPException(status_code=401, detail="Authentication required")

        if "id" not in current_user:
            logger.error(f"[COACH_ENDPOINT] current_user missing 'id' field. Keys: {current_user.keys()}")
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        user_id = current_user["id"]
        logger.info(f"[COACH_ENDPOINT] Extracted user_id: {user_id}")

        # STEP 2: Validate request data
        logger.info(f"[COACH_ENDPOINT] Request message: '{request.message[:100]}...' (length: {len(request.message)})")
        logger.info(f"[COACH_ENDPOINT] Request conversation_id: {request.conversation_id}")

        if not request.message or not request.message.strip():
            logger.error("[COACH_ENDPOINT] Empty message received")
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # STEP 3: Initialize coach service
        logger.info("[COACH_ENDPOINT] Initializing unified coach service...")
        try:
            coach_service = get_unified_coach_service()
            logger.info("[COACH_ENDPOINT] Coach service initialized successfully")
        except Exception as svc_err:
            logger.error(f"[COACH_ENDPOINT] Failed to initialize coach service: {svc_err}", exc_info=True)
            raise HTTPException(
                status_code=503,
                detail="AI Coach service is temporarily unavailable. Please try again."
            )

        # STEP 4: Handle image URLs if provided (convert first URL to base64)
        image_base64 = None
        if request.image_urls and len(request.image_urls) > 0:
            try:
                import httpx
                import base64

                logger.info(f"[COACH_ENDPOINT] Downloading image from URL: {request.image_urls[0]}")
                async with httpx.AsyncClient() as client:
                    img_response = await client.get(request.image_urls[0], timeout=10.0)
                    if img_response.status_code == 200:
                        image_base64 = base64.b64encode(img_response.content).decode('utf-8')
                        logger.info(f"[COACH_ENDPOINT] Successfully converted image to base64 (size: {len(image_base64)} chars)")
                    else:
                        logger.warning(f"[COACH_ENDPOINT] Failed to download image: HTTP {img_response.status_code}")
            except Exception as img_err:
                logger.error(f"[COACH_ENDPOINT] Error downloading/converting image: {img_err}")
                # Continue without image rather than failing entirely

        # STEP 5: Process message (auto-routing to chat or log mode)
        logger.info(f"[COACH_ENDPOINT] Processing message for user {user_id}...")
        try:
            response = await coach_service.process_message(
                user_id=user_id,
                message=request.message,
                conversation_id=request.conversation_id,
                image_base64=image_base64,
                audio_base64=None,  # TODO: Support audio uploads
                metadata=None,
                background_tasks=background_tasks  # Pass background tasks for async vectorization
            )
            logger.info(f"[COACH_ENDPOINT] Message processed successfully. Mode: {response.get('mode')}")
        except Exception as proc_err:
            logger.error(f"[COACH_ENDPOINT] process_message failed: {proc_err}", exc_info=True)
            raise

        # STEP 6: Return response
        logger.info("[COACH_ENDPOINT] Returning response to client")
        return response

    except HTTPException:
        # Re-raise HTTP exceptions (already logged)
        raise
    except ValueError as e:
        logger.error(f"[COACH_ENDPOINT] Validation error: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"[COACH_ENDPOINT] CRITICAL UNHANDLED ERROR: {e}", exc_info=True)
        logger.error(f"[COACH_ENDPOINT] Error type: {type(e).__name__}")
        logger.error(f"[COACH_ENDPOINT] Error args: {e.args}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process message. Please try again."
        )


# =====================================================
# ENDPOINT 2: Confirm Detected Log
# =====================================================

@router.options("/confirm-log")
async def confirm_log_options():
    """Handle CORS preflight for confirm-log endpoint."""
    return {"status": "ok"}


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
    2. Extract original_text from user message
    3. Save structured log to database
    4. Update quick_entry_logs with linked IDs
    5. Add success message to conversation
    6. Return success response
    """
    logger.info("[CONFIRM_LOG] ======= Starting confirm_log endpoint =======")
    logger.info(f"[CONFIRM_LOG] Request: conversation_id={request.conversation_id}, log_type={request.log_type}, user_message_id={request.user_message_id}")
    logger.info(f"[CONFIRM_LOG] Log data keys: {list(request.log_data.keys())}")
    logger.info(f"[CONFIRM_LOG] Current user: {current_user}")

    try:
        logger.info("[CONFIRM_LOG] Extracting user_id...")
        user_id = current_user["id"]
        logger.info(f"[CONFIRM_LOG] User ID: {user_id}")

        logger.info("[CONFIRM_LOG] Getting Supabase client...")
        supabase = get_service_client()
        logger.info("[CONFIRM_LOG] Supabase client obtained")

        # Extract original_text from user message
        original_text = ""
        if request.user_message_id:
            try:
                logger.info(f"[CONFIRM_LOG] Fetching original message: {request.user_message_id}")
                msg_response = supabase.table("coach_messages") \
                    .select("content") \
                    .eq("id", request.user_message_id) \
                    .limit(1) \
                    .execute()

                if msg_response.data:
                    original_text = msg_response.data[0].get("content", "")
                    logger.info(f"[CONFIRM_LOG] Original text length: {len(original_text)}")
                else:
                    logger.warning("[CONFIRM_LOG] No message data found")
            except Exception as e:
                logger.warning(f"[CONFIRM_LOG] Could not fetch original message: {e}")
                # Continue with empty string - non-critical

        # Get unified coach service
        logger.info("[CONFIRM_LOG] Initializing unified coach service...")
        coach_service = get_unified_coach_service()
        logger.info("[CONFIRM_LOG] Coach service initialized")

        # Confirm and save log with all required parameters
        logger.info("[CONFIRM_LOG] Calling coach_service.confirm_log...")
        logger.info(f"[CONFIRM_LOG] Parameters: user_id={user_id}, conversation_id={request.conversation_id}, log_type={request.log_type.value}")
        response = await coach_service.confirm_log(
            user_id=user_id,
            conversation_id=request.conversation_id,
            user_message_id=request.user_message_id,
            log_type=request.log_type.value,
            log_data=request.log_data,
            original_text=original_text
        )

        logger.info(f"[CONFIRM_LOG] ✅ Success! Response: {response}")
        return response

    except ValueError as e:
        logger.error(f"[CONFIRM_LOG] ❌ Validation error: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as he:
        logger.error(f"[CONFIRM_LOG] ❌ HTTP exception: {he.status_code} - {he.detail}")
        raise
    except Exception as e:
        logger.error(f"[CONFIRM_LOG] ❌ CRITICAL ERROR: {e}", exc_info=True)
        logger.error(f"[CONFIRM_LOG] Error type: {type(e).__name__}")
        logger.error(f"[CONFIRM_LOG] Error args: {e.args}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save log: {str(e)}"  # Include error message for debugging
        )


# =====================================================
# ENDPOINT 2b: Cancel Detected Log
# =====================================================

class CancelLogRequest(BaseModel):
    """Request to cancel a detected log."""
    conversation_id: str = Field(..., description="Conversation ID")
    user_message_id: str = Field(..., description="User message ID that triggered detection")


@router.post(
    "/cancel-log",
    summary="Cancel a detected log",
    description="""
    When user cancels a detected log (e.g., from meal preview page).

    This endpoint:
    1. Adds an assistant message acknowledging the cancellation
    2. Keeps conversation flowing naturally
    3. Returns success status

    **Example:**
    ```json
    {
      "conversation_id": "123e4567...",
      "user_message_id": "456e7890..."
    }
    ```
    """,
    tags=["coach"]
)
async def cancel_log(
    request: CancelLogRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Cancel a detected log and add coach acknowledgment message.

    FLOW:
    1. Validate conversation belongs to user
    2. Add assistant message: "No problem! I won't log that meal..."
    3. Return success
    """
    try:
        user_id = current_user["id"]
        supabase = get_service_client()

        # Verify conversation belongs to user
        conv_check = (
            supabase.table("coach_conversations")
            .select("id")
            .eq("id", request.conversation_id)
            .eq("user_id", user_id)
            .single()
            .execute()
        )

        if not conv_check.data:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or access denied"
            )

        # Add assistant cancellation message
        assistant_message = "No problem! I won't log that meal. Let me know if you change your mind or if there's anything else I can help you with. 💪"

        message_id = supabase.table("coach_messages").insert({
            "conversation_id": request.conversation_id,
            "role": "assistant",
            "content": assistant_message,
            "message_type": "chat",
            "is_vectorized": False
        }).execute().data[0]["id"]

        # Update conversation last_message_at
        supabase.table("coach_conversations").update({
            "last_message_at": "now()",
            "message_count": supabase.table("coach_conversations")
                .select("message_count")
                .eq("id", request.conversation_id)
                .single()
                .execute()
                .data["message_count"] + 1
        }).eq("id", request.conversation_id).execute()

        return {
            "success": True,
            "message": assistant_message,
            "message_id": message_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in cancel_log: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to cancel log. Please try again."
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
