"""
Consultation API Endpoints

Handles adaptive AI-driven consultations with different specialists.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any

from app.api.middleware.auth import get_current_user
from app.services.consultation_service import get_consultation_service
from app.services.daily_recommendation_service import get_recommendation_service
from app.models.requests.consultation import (
    StartConsultationRequest,
    SendMessageRequest,
    CompleteConsultationRequest,
    UpdateRecommendationRequest,
    GenerateDailyPlanRequest
)
from app.models.responses.consultation import (
    ConsultationSessionResponse,
    ConsultationMessageResponse,
    ConsultationSummaryResponse,
    CompleteConsultationResponse,
    RecommendationResponse,
    DailyPlanResponse,
    NextActionResponse,
    ErrorResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/consultation", tags=["consultation"])


@router.post(
    "/start",
    response_model=ConsultationSessionResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid specialist type"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Start new consultation",
    description="""
    Start a new AI-driven consultation with a specialist.

    Available specialists:
    - `unified_coach`: All-in-one fitness & nutrition coach
    - `nutritionist`: Registered dietitian nutritionist
    - `trainer`: Certified personal trainer
    - `physiotherapist`: Licensed physiotherapist
    - `sports_psychologist`: Sports psychology specialist

    The AI will ask intelligent follow-up questions and extract structured data
    from natural conversation.

    **Rate limit**: 10 consultations per user per day
    """
)
async def start_consultation(
    request: StartConsultationRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Start a new consultation session with specialist."""
    try:
        user_id = current_user["user_id"]
        consultation_service = get_consultation_service()

        result = await consultation_service.start_consultation(
            user_id=user_id,
            specialist_type=request.specialist_type
        )

        logger.info(f"Started consultation {result['session_id']} for user {user_id}")

        return result

    except ValueError as e:
        logger.warning(f"Invalid consultation request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error starting consultation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start consultation. Please try again."
        )


@router.post(
    "/{session_id}/message",
    response_model=ConsultationMessageResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid message"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Session not found"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Send message in consultation",
    description="""
    Send a message/response in an active consultation.

    The AI will:
    1. Extract structured data from your response
    2. Generate an intelligent follow-up question
    3. Update consultation progress

    When the consultation is complete (progress = 100%), the status will be
    'ready_to_complete' and you'll receive a wrap-up message instead of a question.
    """
)
async def send_consultation_message(
    session_id: str,
    request: SendMessageRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Send a message in consultation session."""
    try:
        user_id = current_user["user_id"]
        consultation_service = get_consultation_service()

        result = await consultation_service.process_user_response(
            session_id=session_id,
            user_input=request.message
        )

        logger.info(
            f"Processed message in consultation {session_id}, "
            f"progress: {result['progress_percentage']}%"
        )

        return result

    except ValueError as e:
        logger.warning(f"Invalid consultation session: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing consultation message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process message. Please try again."
        )


@router.get(
    "/{session_id}/summary",
    response_model=ConsultationSummaryResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Session not found"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Get consultation summary",
    description="""
    Get a summary of all data extracted from the consultation.

    Returns structured data organized by category:
    - `health_history`: Medical conditions, medications, etc.
    - `nutrition_patterns`: Eating habits and patterns
    - `training_history`: Fitness background and experience
    - `goals`: User's objectives and timelines
    - `preferences`: Equipment, schedule, dietary preferences
    - `measurements`: Weight, height, age, etc.
    - `lifestyle`: Sleep, stress, recovery factors
    - `psychology`: Mental approach and mindset
    """
)
async def get_consultation_summary(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get summary of consultation data."""
    try:
        consultation_service = get_consultation_service()

        summary = await consultation_service.get_consultation_summary(
            session_id=session_id
        )

        return summary

    except Exception as e:
        logger.error(f"Error fetching consultation summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve consultation summary."
        )


@router.post(
    "/{session_id}/complete",
    response_model=CompleteConsultationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Consultation not ready to complete"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Session not found"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Complete consultation",
    description="""
    Complete the consultation and optionally generate an AI program.

    This will:
    1. Mark the consultation as completed
    2. Update user profile with extracted data
    3. Calculate nutrition plan (BMR, TDEE, macros)
    4. Optionally generate a personalized AI program

    The generated program will integrate all consultation insights.
    """
)
async def complete_consultation(
    session_id: str,
    request: CompleteConsultationRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Complete consultation and generate program."""
    try:
        consultation_service = get_consultation_service()

        result = await consultation_service.complete_consultation(
            session_id=session_id,
            generate_program=request.generate_program
        )

        logger.info(f"Completed consultation {session_id}")

        return result

    except ValueError as e:
        logger.warning(f"Cannot complete consultation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error completing consultation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete consultation. Please try again."
        )


@router.post(
    "/recommendations/generate",
    response_model=DailyPlanResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Generate daily plan",
    description="""
    Generate a complete daily plan with meal and workout recommendations.

    The AI will analyze:
    - Your nutrition goals and what you've logged today
    - Your active AI program (if any)
    - Your typical schedule and preferences
    - Remaining calories and macros for the day

    Returns time-aware recommendations for meals and workouts.
    """
)
async def generate_daily_plan(
    request: GenerateDailyPlanRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Generate daily plan with recommendations."""
    try:
        user_id = current_user["user_id"]
        recommendation_service = get_recommendation_service()

        recommendations = await recommendation_service.generate_daily_plan(
            user_id=user_id,
            target_date=request.target_date
        )

        # Build summary
        summary = {
            'total_recommendations': len(recommendations),
            'meals_suggested': len([r for r in recommendations if r['recommendation_type'] == 'meal']),
            'workouts_suggested': len([r for r in recommendations if r['recommendation_type'] == 'workout']),
        }

        logger.info(f"Generated {len(recommendations)} recommendations for user {user_id}")

        return {
            'recommendations': recommendations,
            'summary': summary
        }

    except Exception as e:
        logger.error(f"Error generating daily plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate daily plan. Please try again."
        )


@router.get(
    "/recommendations/today",
    response_model=DailyPlanResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Get today's recommendations",
    description="""
    Get all active recommendations for today.

    Returns only pending and accepted recommendations, ordered by time.
    """
)
async def get_todays_recommendations(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get today's recommendations."""
    try:
        user_id = current_user["user_id"]
        recommendation_service = get_recommendation_service()

        recommendations = await recommendation_service.get_active_recommendations(
            user_id=user_id
        )

        summary = {
            'total_recommendations': len(recommendations),
            'meals_suggested': len([r for r in recommendations if r['recommendation_type'] == 'meal']),
            'workouts_suggested': len([r for r in recommendations if r['recommendation_type'] == 'workout']),
        }

        return {
            'recommendations': recommendations,
            'summary': summary
        }

    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve recommendations."
        )


@router.get(
    "/recommendations/next",
    response_model=NextActionResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Get next recommended action",
    description="""
    Get the next immediate recommendation (meal or workout).

    The AI considers:
    - Current time
    - What you've logged today
    - Your schedule and preferences
    - Your active program

    Returns the most relevant next action with timing information.
    """
)
async def get_next_recommendation(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get next recommended action."""
    try:
        user_id = current_user["user_id"]
        recommendation_service = get_recommendation_service()

        next_rec = await recommendation_service.suggest_next_action(
            user_id=user_id
        )

        if not next_rec:
            return {
                'recommendation': None,
                'time_until_next': None,
                'message': "All caught up! No pending recommendations right now."
            }

        # Calculate time until recommendation
        from datetime import datetime, time as dt_time
        rec_time = next_rec.get('recommendation_time')
        if rec_time:
            if isinstance(rec_time, str):
                rec_time = datetime.strptime(rec_time, '%H:%M:%S').time()

            now = datetime.now()
            rec_datetime = datetime.combine(now.date(), rec_time)
            time_diff = (rec_datetime - now).total_seconds() / 60
            time_until = int(max(time_diff, 0))
        else:
            time_until = None

        # Build message
        rec_type = next_rec['recommendation_type']
        if time_until and time_until > 0:
            message = f"Your next {rec_type} is recommended in {time_until} minutes"
        else:
            message = f"Time for your {rec_type}!"

        return {
            'recommendation': next_rec,
            'time_until_next': time_until,
            'message': message
        }

    except Exception as e:
        logger.error(f"Error getting next recommendation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get next recommendation."
        )


@router.post(
    "/recommendations/{recommendation_id}/feedback",
    response_model=RecommendationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid status"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Recommendation not found"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Update recommendation status",
    description="""
    Accept, reject, or mark a recommendation as completed.

    Statuses:
    - `accepted`: User plans to follow this recommendation
    - `rejected`: User doesn't want this recommendation
    - `completed`: User followed the recommendation

    Optional feedback helps the AI learn your preferences.
    """
)
async def update_recommendation_status(
    recommendation_id: str,
    request: UpdateRecommendationRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update recommendation status with feedback."""
    try:
        user_id = current_user["user_id"]
        recommendation_service = get_recommendation_service()

        if request.status == 'accepted':
            result = await recommendation_service.accept_recommendation(
                recommendation_id=recommendation_id,
                user_id=user_id
            )
        elif request.status == 'rejected':
            result = await recommendation_service.reject_recommendation(
                recommendation_id=recommendation_id,
                user_id=user_id,
                feedback=request.feedback
            )
        else:  # completed
            result = await recommendation_service._update_recommendation_status(
                recommendation_id=recommendation_id,
                status='completed',
                user_id=user_id,
                feedback=request.feedback
            )

        # Save feedback rating if provided
        if request.feedback_rating:
            recommendation_service.supabase.table('daily_recommendations')\
                .update({'feedback_rating': request.feedback_rating})\
                .eq('id', recommendation_id)\
                .eq('user_id', user_id)\
                .execute()

        logger.info(f"Updated recommendation {recommendation_id} to {request.status}")

        return result

    except Exception as e:
        logger.error(f"Error updating recommendation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update recommendation."
        )


@router.get(
    "/status",
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Check consultation completion status",
    description="""
    Check if the user has completed any consultation.

    Used by the dashboard to show/hide the first-time user consultation banner.
    Returns a boolean indicating whether the user has at least one completed consultation.
    """
)
async def check_consultation_status(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Check if user has completed a consultation."""
    try:
        user_id = current_user["user_id"]
        consultation_service = get_consultation_service()

        has_completed = await consultation_service.has_completed_consultation(user_id)

        logger.info(f"Consultation status check for user {user_id}: {has_completed}")

        return {"has_completed": has_completed}

    except Exception as e:
        logger.error(f"Error checking consultation status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check consultation status."
        )


@router.get(
    "/active-session",
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Check for active consultation session",
    description="""
    Check if the user has an active consultation session in progress.

    Used by the consultation page to prevent users from starting multiple consultations
    simultaneously. Returns whether an active session exists and the session data if present.
    """
)
async def check_active_session(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Check if user has an active consultation session."""
    try:
        user_id = current_user["user_id"]
        consultation_service = get_consultation_service()

        active_session = await consultation_service.get_active_session(user_id)

        has_active_session = active_session is not None

        logger.info(f"Active session check for user {user_id}: {has_active_session}")

        return {
            "has_active_session": has_active_session,
            "session": active_session
        }

    except Exception as e:
        logger.error(f"Error checking active session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check for active consultation session."
        )
