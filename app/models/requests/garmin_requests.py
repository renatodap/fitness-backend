"""
Pydantic request models for Garmin integration.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional


class GarminConnectionTestRequest(BaseModel):
    """Request to test Garmin Connect connection."""

    email: str = Field(..., description="Garmin account email", max_length=255)
    password: str = Field(..., description="Garmin account password", min_length=6)

    @validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower().strip()


class GarminSyncRequest(BaseModel):
    """Request to sync Garmin health data."""

    email: str = Field(..., description="Garmin account email")
    password: str = Field(..., description="Garmin account password")
    days_back: int = Field(
        default=7,
        ge=1,
        le=90,
        description="Number of days to sync (1-90)"
    )
    sync_types: Optional[list[str]] = Field(
        default=None,
        description="Specific data types to sync (sleep, hrv, stress, etc.). If null, syncs all."
    )

    @validator("sync_types")
    def validate_sync_types(cls, v):
        if v is not None:
            valid_types = {
                "sleep", "hrv", "stress", "body_battery",
                "steps_activity", "training_load", "readiness", "activities"
            }
            invalid = set(v) - valid_types
            if invalid:
                raise ValueError(f"Invalid sync types: {invalid}. Valid types: {valid_types}")
        return v


class ManualSleepEntryRequest(BaseModel):
    """Manual sleep entry for non-Garmin users."""

    sleep_date: str = Field(..., description="Sleep date (YYYY-MM-DD)")
    sleep_start: str = Field(..., description="Sleep start time (ISO 8601)")
    sleep_end: str = Field(..., description="Sleep end time (ISO 8601)")
    sleep_quality: str = Field(
        ...,
        description="Sleep quality rating"
    )
    notes: Optional[str] = Field(None, max_length=1000)

    @validator("sleep_quality")
    def validate_quality(cls, v):
        valid_qualities = ["poor", "fair", "good", "excellent"]
        if v not in valid_qualities:
            raise ValueError(f"sleep_quality must be one of {valid_qualities}")
        return v


class ManualReadinessCheckInRequest(BaseModel):
    """Morning check-in for readiness assessment."""

    energy_level: int = Field(..., ge=1, le=10, description="Energy level (1-10)")
    soreness_level: int = Field(..., ge=0, le=10, description="Muscle soreness (0-10)")
    stress_level: int = Field(..., ge=0, le=10, description="Stress level (0-10)")
    mood: str = Field(..., description="Mood rating")
    motivation_level: int = Field(..., ge=1, le=10, description="Motivation level (1-10)")
    notes: Optional[str] = Field(None, max_length=500)

    @validator("mood")
    def validate_mood(cls, v):
        valid_moods = ["terrible", "bad", "okay", "good", "amazing"]
        if v not in valid_moods:
            raise ValueError(f"mood must be one of {valid_moods}")
        return v
