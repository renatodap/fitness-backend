"""
Pydantic models for consultation API requests.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import date


class StartConsultationRequest(BaseModel):
    """Request to start a new consultation session."""

    specialist_type: Literal['unified_coach', 'nutritionist', 'trainer', 'physiotherapist', 'sports_psychologist'] = Field(
        ...,
        description="Type of specialist to consult"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "specialist_type": "unified_coach"
            }
        }


class SendMessageRequest(BaseModel):
    """Request to send a message in consultation."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's message/response"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "I want to lose 20 pounds and build muscle"
            }
        }


class CompleteConsultationRequest(BaseModel):
    """Request to complete consultation."""

    generate_program: bool = Field(
        default=True,
        description="Whether to generate AI program from consultation"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "generate_program": True
            }
        }


class UpdateRecommendationRequest(BaseModel):
    """Request to update recommendation status."""

    status: Literal['accepted', 'rejected', 'completed'] = Field(
        ...,
        description="New status for recommendation"
    )

    feedback: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional user feedback"
    )

    feedback_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Rating 1-5 (5 = excellent)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "accepted",
                "feedback": "Perfect meal suggestion!",
                "feedback_rating": 5
            }
        }


class GenerateDailyPlanRequest(BaseModel):
    """Request to generate daily plan."""

    target_date: Optional[date] = Field(
        None,
        description="Date to generate plan for (defaults to today)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "target_date": "2025-10-08"
            }
        }
