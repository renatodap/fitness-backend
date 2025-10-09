"""
Pydantic response models for Garmin integration.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import date


class GarminConnectionTestResponse(BaseModel):
    """Response for Garmin connection test."""

    success: bool
    message: str
    profile: Optional[Dict[str, str]] = None


class GarminSyncResultDetail(BaseModel):
    """Details for a specific sync operation."""

    synced_count: int = Field(..., description="Number of records synced")
    error_count: int = Field(..., description="Number of errors encountered")
    skipped_count: int = Field(..., description="Number of records skipped")
    errors: List[str] = Field(default=[], description="Error messages")


class GarminSyncResponse(BaseModel):
    """Response for Garmin sync operation."""

    success: bool
    user_id: str
    date_range: Dict[str, str] = Field(..., description="Start and end dates")
    total_synced: int = Field(..., description="Total records synced across all types")
    total_errors: int = Field(..., description="Total errors across all types")
    details: Dict[str, GarminSyncResultDetail] = Field(
        ...,
        description="Detailed results for each data type (sleep, hrv, etc.)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "user_id": "uuid-here",
                "date_range": {
                    "start": "2025-10-02",
                    "end": "2025-10-09"
                },
                "total_synced": 42,
                "total_errors": 0,
                "details": {
                    "sleep": {
                        "synced_count": 7,
                        "error_count": 0,
                        "skipped_count": 0,
                        "errors": []
                    },
                    "hrv": {
                        "synced_count": 7,
                        "error_count": 0,
                        "skipped_count": 0,
                        "errors": []
                    }
                }
            }
        }


class SleepLogResponse(BaseModel):
    """Response for sleep log entry."""

    id: str
    user_id: str
    sleep_date: str
    total_sleep_minutes: int
    deep_sleep_minutes: Optional[int] = None
    light_sleep_minutes: Optional[int] = None
    rem_sleep_minutes: Optional[int] = None
    sleep_score: Optional[int] = None
    sleep_quality: str
    source: str
    created_at: str


class ReadinessResponse(BaseModel):
    """Response for daily readiness."""

    id: str
    user_id: str
    date: str
    readiness_score: int = Field(..., ge=0, le=100)
    readiness_status: str
    sleep_score: Optional[int] = None
    hrv_status: Optional[str] = None
    energy_level: Optional[int] = None
    soreness_level: Optional[int] = None
    stress_level: Optional[int] = None
    mood: Optional[str] = None
    calculation_method: str
    factors_used: Dict[str, Any] = Field(default={})


class HealthMetricsSummaryResponse(BaseModel):
    """Summary of all health metrics for a date range."""

    user_id: str
    date_range: Dict[str, str]
    sleep_data_count: int
    hrv_data_count: int
    readiness_data_count: int
    stress_data_count: int
    body_battery_data_count: int
    steps_data_count: int
    training_load_data_count: int
    avg_readiness_score: Optional[float] = None
    avg_sleep_score: Optional[float] = None
    avg_sleep_hours: Optional[float] = None
    total_steps: Optional[int] = None
