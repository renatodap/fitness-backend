"""
Coach API Endpoints

API routes for AI coach interactions (Trainer and Nutritionist).
"""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.services.coach_service import get_coach_service
from app.api.v1.dependencies import get_current_user
from app.api.middleware.rate_limit import coach_chat_rate_limit

logger = logging.getLogger(__name__)
router = APIRouter()


# Request/Response Models
from app.api.v1.schemas.coach_schemas import ChatRequest, ChatResponse, ContextInfo

# Legacy models for backwards compatibility
class ChatMessageRequest(BaseModel):
    """Request to send message to coach."""
    coach_type: str = Field(..., description="Coach type: 'trainer', 'nutritionist', or 'coach' (unified)")
    message: str = Field(..., description="User's message to the coach")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID")
    model: str = Field(default="gpt-4o-mini", description="OpenAI model to use")


class ChatMessageResponse(BaseModel):
    """Response from coach chat."""
    coach_type: str
    coach_name: str
    message: str
    timestamp: str
    model_used: str
    tokens_used: int


class RecommendationsRequest(BaseModel):
    """Request to generate weekly recommendations."""
    coach_type: str = Field(..., description="Coach type: 'trainer' or 'nutritionist'")


class UpdateRecommendationRequest(BaseModel):
    """Request to update recommendation status."""
    status: str = Field(..., description="Status: 'accepted', 'rejected', or 'completed'")
    feedback_text: Optional[str] = Field(None, description="Optional feedback text")


# Endpoints

@router.post("/chat")
@coach_chat_rate_limit()
async def chat_with_coach(
    request: ChatRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Chat with AI coach (Unified Coach, Trainer, or Nutritionist) - INCREMENT 1.

    Sends a message to the specified coach and receives a personalized response
    based on user's history, goals, and current context.
    """
    try:
        # Validate coach_type and message
        if request.coach_type not in ['trainer', 'nutritionist', 'coach']:
            raise HTTPException(status_code=400, detail="Invalid coach_type. Must be 'trainer', 'nutritionist', or 'coach'")

        if not request.message or len(request.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        if len(request.message) > 1000:
            raise HTTPException(status_code=400, detail="Message too long (max 1000 characters)")

        # Extract user_id from current_user
        user_id = current_user

        coach_service = get_coach_service()

        # Use INCREMENT 1 compatible method
        response_dict = await coach_service.generate_response(
            user_id=user_id,
            message=request.message,
            coach_type=request.coach_type,
            conversation_id=request.conversation_id
        )

        # Return ChatResponse format
        return {
            "success": response_dict.get("success", True),
            "conversation_id": response_dict.get("conversation_id", ""),
            "message": response_dict.get("message", ""),
            "context_used": response_dict.get("context_used"),
            "error": response_dict.get("error")
        }

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in chat_with_coach: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in chat_with_coach: {e}")
        raise HTTPException(status_code=500, detail="Failed to get coach response")


@router.post("/recommendations/generate")
async def generate_recommendations(
    request: RecommendationsRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Generate weekly recommendations from coach.

    Analyzes user's recent data and generates 3-5 actionable recommendations
    for the upcoming week.
    """
    try:
        coach_service = get_coach_service()

        recommendations = await coach_service.create_weekly_recommendations(
            user_id=user_id,
            coach_type=request.coach_type
        )

        return {
            "success": True,
            "recommendations": recommendations,
            "count": len(recommendations)
        }

    except ValueError as e:
        logger.error(f"Validation error in generate_recommendations: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in generate_recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")


@router.get("/recommendations")
async def get_recommendations(
    coach_type: Optional[str] = None,
    user_id: str = Depends(get_current_user)
):
    """
    Get active recommendations for user.

    Optionally filter by coach type ('trainer' or 'nutritionist').
    Returns recommendations ordered by priority.
    """
    try:
        coach_service = get_coach_service()

        recommendations = await coach_service.get_active_recommendations(
            user_id=user_id,
            coach_type=coach_type
        )

        return {
            "success": True,
            "recommendations": recommendations,
            "count": len(recommendations)
        }

    except Exception as e:
        logger.error(f"Error in get_recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get recommendations")


@router.patch("/recommendations/{recommendation_id}")
async def update_recommendation(
    recommendation_id: str,
    request: UpdateRecommendationRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Update recommendation status.

    Allows user to accept, reject, or mark as completed a recommendation.
    Optionally provide feedback text.
    """
    try:
        coach_service = get_coach_service()

        updated_recommendation = await coach_service.update_recommendation_status(
            recommendation_id=recommendation_id,
            user_id=user_id,
            status=request.status,
            feedback_text=request.feedback_text
        )

        return {
            "success": True,
            "recommendation": updated_recommendation
        }

    except Exception as e:
        logger.error(f"Error in update_recommendation: {e}")
        raise HTTPException(status_code=500, detail="Failed to update recommendation")


@router.get("/personas")
async def get_coach_personas(
    _: str = Depends(get_current_user)  # Just require authentication
):
    """
    Get all available coach personas.

    Returns information about the Trainer and Nutritionist personas.
    """
    from app.services.supabase_service import get_service_client

    try:
        supabase = get_service_client()

        response = (
            supabase.table("coach_personas")
            .select("id, name, display_name, specialty")
            .execute()
        )

        return {
            "success": True,
            "personas": response.data if response.data else []
        }

    except Exception as e:
        logger.error(f"Error in get_coach_personas: {e}")
        raise HTTPException(status_code=500, detail="Failed to get coach personas")


@router.get("/conversations/{coach_type}")
async def get_conversation_history(
    coach_type: str,
    limit: int = 50,
    user_id: str = Depends(get_current_user)
):
    """
    Get conversation history with specific coach.

    Returns the most recent messages from the conversation.
    """
    from app.services.supabase_service import get_service_client

    try:
        supabase = get_service_client()

        # Get coach persona
        persona_response = (
            supabase.table("coach_personas")
            .select("id")
            .eq("name", coach_type)
            .single()
            .execute()
        )

        if not persona_response.data:
            raise HTTPException(status_code=404, detail="Coach persona not found")

        persona_id = persona_response.data["id"]

        # Get conversation
        conv_response = (
            supabase.table("coach_conversations")
            .select("messages, last_message_at")
            .eq("user_id", user_id)
            .eq("coach_persona_id", persona_id)
            .order("last_message_at", desc=True)
            .limit(1)
            .execute()
        )

        if not conv_response.data:
            return {
                "success": True,
                "messages": [],
                "count": 0
            }

        messages = conv_response.data[0].get("messages", [])
        recent_messages = messages[-limit:] if messages else []

        return {
            "success": True,
            "messages": recent_messages,
            "count": len(recent_messages),
            "last_message_at": conv_response.data[0].get("last_message_at")
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_conversation_history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversation history")
