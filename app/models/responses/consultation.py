"""
Pydantic models for consultation API responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Literal
from datetime import datetime, date, time


class ConsultationSessionResponse(BaseModel):
    """Response for consultation session."""

    session_id: str = Field(..., description="Session UUID")
    specialist_type: str = Field(..., description="Type of specialist")
    conversation_stage: str = Field(..., description="Current conversation stage")
    progress_percentage: int = Field(..., description="Completion percentage (0-100)")
    initial_question: Optional[str] = Field(None, description="Initial question from specialist")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "specialist_type": "nutritionist",
                "conversation_stage": "introduction",
                "progress_percentage": 0,
                "initial_question": "What's your primary motivation for seeking nutrition guidance?"
            }
        }


class ConsultationMessageResponse(BaseModel):
    """Response after sending a message."""

    session_id: str
    status: Literal['active', 'ready_to_complete']
    next_question: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None
    conversation_stage: str
    progress_percentage: int
    is_complete: bool
    wrap_up_message: Optional[str] = None
    extraction_summary: Optional[Dict[str, Any]] = None

    # Goal-driven consultation fields
    goals_met: Optional[int] = Field(None, description="Number of goals completed")
    goals_total: Optional[int] = Field(None, description="Total number of goals")
    goals_detail: Optional[Dict[str, str]] = Field(None, description="Detailed status of each goal (✅/⏳)")
    logged_items: Optional[List[Dict[str, Any]]] = Field(None, description="Items auto-logged during consultation")

    # Limit tracking fields
    minutes_elapsed: Optional[int] = Field(None, description="Minutes since consultation started")
    messages_sent: Optional[int] = Field(None, description="Number of messages sent in consultation")
    approaching_limit: Optional[bool] = Field(None, description="True if approaching time/message limit")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "active",
                "next_question": "How many meals do you typically eat per day?",
                "extracted_data": {
                    "goals": {
                        "primary_goal": "lose_fat",
                        "target_weight": 75
                    }
                },
                "conversation_stage": "eating_patterns",
                "progress_percentage": 40,
                "is_complete": False,
                "goals_met": 4,
                "goals_total": 10,
                "goals_detail": {
                    "primary_fitness_goal": "✅ Identified",
                    "measurements": "✅ Collected",
                    "typical_eating_patterns": "⏳ Pending",
                    "food_preferences": "⏳ Pending"
                },
                "logged_items": [
                    {
                        "type": "meal",
                        "content": "Breakfast: 3 eggs, oatmeal, banana"
                    }
                ],
                "minutes_elapsed": 8,
                "messages_sent": 12,
                "approaching_limit": False
            }
        }


class ConsultationSummaryResponse(BaseModel):
    """Response with consultation summary."""

    health_history: Optional[Dict[str, Any]] = None
    nutrition_patterns: Optional[Dict[str, Any]] = None
    training_history: Optional[Dict[str, Any]] = None
    goals: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None
    measurements: Optional[Dict[str, Any]] = None
    lifestyle: Optional[Dict[str, Any]] = None
    psychology: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = Field(None, alias="_metadata")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "goals": {
                    "primary_goal": "lose_fat",
                    "target_weight": 75,
                    "timeline": "3 months"
                },
                "measurements": {
                    "current_weight_kg": 85,
                    "height_cm": 180,
                    "age": 28
                },
                "preferences": {
                    "equipment_access": ["full_gym"],
                    "training_frequency": 4
                },
                "_metadata": {
                    "specialist_type": "nutritionist",
                    "total_messages": 12,
                    "session_duration_minutes": 15
                }
            }
        }


class CompleteConsultationResponse(BaseModel):
    """Response after completing consultation."""

    session_id: str
    status: Literal['completed']
    summary: ConsultationSummaryResponse
    program_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "completed",
                "summary": {},
                "program_id": "660e8400-e29b-41d4-a716-446655440000"
            }
        }


class RecommendationResponse(BaseModel):
    """Response for a single recommendation."""

    id: str
    user_id: str
    recommendation_date: date
    recommendation_time: Optional[time]
    recommendation_type: Literal['meal', 'workout', 'rest', 'hydration', 'supplement', 'note', 'check_in']
    content: Dict[str, Any]
    reasoning: Optional[str]
    priority: int
    status: Literal['pending', 'accepted', 'rejected', 'completed', 'expired']
    based_on_data: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "770e8400-e29b-41d4-a716-446655440000",
                "user_id": "880e8400-e29b-41d4-a716-446655440000",
                "recommendation_date": "2025-10-08",
                "recommendation_time": "12:00:00",
                "recommendation_type": "meal",
                "content": {
                    "meal_name": "High Protein Lunch",
                    "foods": ["grilled chicken", "brown rice", "broccoli"],
                    "estimated_calories": 500,
                    "estimated_protein_g": 45
                },
                "reasoning": "You haven't logged lunch yet. Target: 500 cal, 45g protein",
                "priority": 4,
                "status": "pending",
                "based_on_data": {
                    "logged_calories": 450,
                    "remaining_calories": 1550
                },
                "created_at": "2025-10-08T08:00:00Z"
            }
        }


class DailyPlanResponse(BaseModel):
    """Response with daily plan."""

    recommendations: List[RecommendationResponse]
    summary: Dict[str, Any] = Field(
        ...,
        description="Summary of the day's plan"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "recommendations": [],
                "summary": {
                    "total_recommendations": 5,
                    "meals_suggested": 3,
                    "workouts_suggested": 1,
                    "target_calories": 2000,
                    "target_protein_g": 150
                }
            }
        }


class NextActionResponse(BaseModel):
    """Response with next suggested action."""

    recommendation: Optional[RecommendationResponse] = None
    time_until_next: Optional[int] = Field(
        None,
        description="Minutes until next recommended action"
    )
    message: str = Field(
        ...,
        description="User-friendly message about next action"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "recommendation": None,
                "time_until_next": 45,
                "message": "Your next meal (lunch) is recommended in 45 minutes at 12:00 PM"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    status_code: int = Field(..., description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Session not found",
                "details": {
                    "session_id": "invalid-uuid"
                },
                "status_code": 404
            }
        }
