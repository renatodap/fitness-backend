"""
Activity API Schemas

Pydantic models for activity logging requests and responses.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


# ============================================================================
# REQUEST MODELS
# ============================================================================

class CreateActivityRequest(BaseModel):
    """Request to create an activity log"""

    # Required fields (common to all activities)
    activity_type: str = Field(..., description="Type of activity (running, cycling, strength_training, etc.)")
    name: str = Field(..., min_length=1, max_length=200, description="Activity name")
    start_date: datetime = Field(..., description="When activity started")

    # Common optional fields
    end_date: Optional[datetime] = Field(None, description="When activity ended")
    timezone: Optional[str] = Field(None, description="Timezone of activity")
    elapsed_time_seconds: Optional[int] = Field(None, ge=0, description="Total elapsed time")
    duration_minutes: Optional[int] = Field(None, ge=0, description="Duration in minutes")

    # Cardio metrics
    distance_meters: Optional[float] = Field(None, ge=0, description="Distance in meters")
    average_speed: Optional[float] = Field(None, ge=0, description="Average speed in m/s")
    max_speed: Optional[float] = Field(None, ge=0, description="Max speed in m/s")
    average_pace: Optional[str] = Field(None, description="Average pace (e.g., '8:30 min/mile')")

    # Elevation
    total_elevation_gain: Optional[float] = Field(None, ge=0, description="Elevation gain in meters")
    total_elevation_loss: Optional[float] = Field(None, ge=0, description="Elevation loss in meters")
    elevation_high: Optional[float] = Field(None, description="Highest point in meters")
    elevation_low: Optional[float] = Field(None, description="Lowest point in meters")

    # Heart rate
    average_heartrate: Optional[int] = Field(None, ge=40, le=220, description="Average heart rate in bpm")
    max_heartrate: Optional[int] = Field(None, ge=40, le=220, description="Max heart rate in bpm")
    min_heartrate: Optional[int] = Field(None, ge=40, le=220, description="Min heart rate in bpm")

    # Power (cycling)
    average_power: Optional[float] = Field(None, ge=0, description="Average power in watts")
    max_power: Optional[int] = Field(None, ge=0, description="Max power in watts")
    normalized_power: Optional[float] = Field(None, ge=0, description="Normalized power in watts")

    # Cadence
    average_cadence: Optional[float] = Field(None, ge=0, description="Average cadence (rpm or spm)")
    max_cadence: Optional[int] = Field(None, ge=0, description="Max cadence")

    # Swimming
    pool_length: Optional[float] = Field(None, ge=0, description="Pool length in meters")
    total_strokes: Optional[int] = Field(None, ge=0, description="Total strokes")
    average_stroke_rate: Optional[float] = Field(None, ge=0, description="Average stroke rate")
    average_swolf: Optional[float] = Field(None, ge=0, description="Average SWOLF score")
    lap_count: Optional[int] = Field(None, ge=0, description="Number of laps")

    # Strength training
    total_reps: Optional[int] = Field(None, ge=0, description="Total repetitions")
    total_sets: Optional[int] = Field(None, ge=0, description="Total sets")
    total_weight_lifted_kg: Optional[float] = Field(None, ge=0, description="Total weight lifted in kg")
    exercise_count: Optional[int] = Field(None, ge=0, description="Number of exercises")

    # Tennis
    total_shots: Optional[int] = Field(None, ge=0, description="Total shots")
    forehand_count: Optional[int] = Field(None, ge=0, description="Forehand count")
    backhand_count: Optional[int] = Field(None, ge=0, description="Backhand count")
    serve_count: Optional[int] = Field(None, ge=0, description="Serve count")
    ace_count: Optional[int] = Field(None, ge=0, description="Ace count")
    winner_count: Optional[int] = Field(None, ge=0, description="Winner count")
    unforced_error_count: Optional[int] = Field(None, ge=0, description="Unforced error count")
    sets_played: Optional[int] = Field(None, ge=0, description="Sets played")
    games_played: Optional[int] = Field(None, ge=0, description="Games played")

    # Yoga/Flexibility
    poses_held: Optional[int] = Field(None, ge=0, description="Number of poses held")
    average_hold_duration: Optional[int] = Field(None, ge=0, description="Average hold duration in seconds")
    flexibility_score: Optional[int] = Field(None, ge=1, le=10, description="Flexibility score 1-10")

    # Calories
    calories: Optional[int] = Field(None, ge=0, description="Calories burned")
    active_calories: Optional[int] = Field(None, ge=0, description="Active calories burned")

    # Subjective metrics
    perceived_exertion: Optional[int] = Field(None, ge=1, le=10, description="RPE (1-10)")
    rpe: Optional[int] = Field(None, ge=1, le=10, description="Rate of perceived exertion (1-10)")
    mood: Optional[str] = Field(None, description="Mood (terrible, bad, okay, good, amazing)")
    energy_level: Optional[int] = Field(None, ge=1, le=5, description="Energy level (1-5)")
    soreness_level: Optional[int] = Field(None, ge=0, le=10, description="Soreness level (0-10)")
    workout_rating: Optional[int] = Field(None, ge=1, le=5, description="Workout rating (1-5)")

    # Weather
    weather_conditions: Optional[str] = Field(None, description="Weather conditions")
    temperature_celsius: Optional[float] = Field(None, description="Temperature in Celsius")
    humidity_percentage: Optional[int] = Field(None, ge=0, le=100, description="Humidity percentage")
    wind_speed_kmh: Optional[float] = Field(None, ge=0, description="Wind speed in km/h")

    # Location
    location: Optional[str] = Field(None, description="Location name")
    route_name: Optional[str] = Field(None, description="Route name")
    city: Optional[str] = Field(None, description="City")
    indoor: Optional[bool] = Field(False, description="Indoor activity")

    # Notes
    notes: Optional[str] = Field(None, max_length=1000, description="Activity notes")
    private_notes: Optional[str] = Field(None, max_length=1000, description="Private notes")

    # Metadata
    tags: Optional[List[str]] = Field(default_factory=list, description="Activity tags")
    trainer: Optional[bool] = Field(False, description="Indoor trainer (for cycling)")
    race: Optional[bool] = Field(False, description="Race/competition")
    workout_type: Optional[str] = Field(None, description="Workout type")
    sport_type: Optional[str] = Field(None, description="Specific sport type")

    # Source tracking
    source: str = Field(default="manual", description="Source of activity (manual, quick_entry, strava, garmin)")
    quick_entry_log_id: Optional[str] = Field(None, description="Quick entry log ID if from quick entry")

    @validator("mood")
    def validate_mood(cls, v):
        if v is not None:
            allowed = ["terrible", "bad", "okay", "good", "amazing"]
            if v not in allowed:
                raise ValueError(f"mood must be one of {allowed}")
        return v

    @validator("source")
    def validate_source(cls, v):
        allowed = ["manual", "quick_entry", "strava", "garmin", "apple", "fitbit"]
        if v not in allowed:
            raise ValueError(f"source must be one of {allowed}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "activity_type": "running",
                "name": "Morning Run",
                "start_date": "2025-10-08T07:00:00Z",
                "duration_minutes": 45,
                "distance_meters": 8000,
                "average_pace": "5:37 /mi",
                "average_heartrate": 155,
                "total_elevation_gain": 120,
                "calories": 450,
                "perceived_exertion": 7,
                "mood": "good",
                "notes": "Felt strong, good weather",
                "source": "manual"
            }
        }


class UpdateActivityRequest(BaseModel):
    """Request to update an activity log"""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    start_date: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    distance_meters: Optional[float] = Field(None, ge=0)
    average_pace: Optional[str] = None
    average_heartrate: Optional[int] = Field(None, ge=40, le=220)
    calories: Optional[int] = Field(None, ge=0)
    perceived_exertion: Optional[int] = Field(None, ge=1, le=10)
    mood: Optional[str] = None
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = Field(None, max_length=1000)
    tags: Optional[List[str]] = None


class ActivityExerciseRequest(BaseModel):
    """Exercise in a strength training activity"""
    exercise_name: str = Field(..., description="Name of exercise")
    sets: Optional[List['ActivitySetRequest']] = Field(default_factory=list, description="Sets for this exercise")
    order_index: Optional[int] = Field(0, description="Order of exercise in workout")
    notes: Optional[str] = Field(None, description="Exercise notes")


class ActivitySetRequest(BaseModel):
    """Set in a strength training exercise"""
    set_number: int = Field(..., ge=1, description="Set number")
    reps_completed: Optional[int] = Field(None, ge=0, description="Reps completed")
    weight_lbs: Optional[float] = Field(None, ge=0, description="Weight in lbs")
    weight_kg: Optional[float] = Field(None, ge=0, description="Weight in kg")
    rpe: Optional[int] = Field(None, ge=1, le=10, description="RPE for this set")
    rest_seconds: Optional[int] = Field(None, ge=0, description="Rest after set")
    completed: Optional[bool] = Field(True, description="Set completed")
    notes: Optional[str] = Field(None, description="Set notes")


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class ActivitySetResponse(BaseModel):
    """Activity set response"""
    id: str
    set_number: int
    reps_completed: Optional[int]
    weight_lbs: Optional[float]
    weight_kg: Optional[float]
    rpe: Optional[int]
    rest_seconds: Optional[int]
    completed: bool
    notes: Optional[str]
    created_at: str


class ActivityExerciseResponse(BaseModel):
    """Activity exercise response"""
    id: str
    exercise_name: str
    order_index: int
    sets: List[ActivitySetResponse]
    notes: Optional[str]
    created_at: str


class ActivityResponse(BaseModel):
    """Activity log response"""

    # Core fields
    id: str
    user_id: str
    activity_type: str
    sport_type: Optional[str]
    name: str
    source: str

    # Timing
    start_date: str
    end_date: Optional[str]
    elapsed_time_seconds: Optional[int]
    duration_minutes: Optional[int]

    # Cardio metrics
    distance_meters: Optional[float]
    average_speed: Optional[float]
    max_speed: Optional[float]
    average_pace: Optional[str]

    # Elevation
    total_elevation_gain: Optional[float]
    total_elevation_loss: Optional[float]
    elevation_high: Optional[float]
    elevation_low: Optional[float]

    # Heart rate
    average_heartrate: Optional[int]
    max_heartrate: Optional[int]
    min_heartrate: Optional[int]

    # Power
    average_power: Optional[float]
    max_power: Optional[int]
    normalized_power: Optional[float]

    # Cadence
    average_cadence: Optional[float]
    max_cadence: Optional[int]

    # Swimming
    pool_length: Optional[float]
    total_strokes: Optional[int]
    average_stroke_rate: Optional[float]
    average_swolf: Optional[float]
    lap_count: Optional[int]

    # Strength
    total_reps: Optional[int]
    total_sets: Optional[int]
    total_weight_lifted_kg: Optional[float]
    exercise_count: Optional[int]
    exercises: Optional[List[ActivityExerciseResponse]]

    # Tennis
    total_shots: Optional[int]
    serve_count: Optional[int]
    ace_count: Optional[int]
    winner_count: Optional[int]
    sets_played: Optional[int]

    # Calories
    calories: Optional[int]
    active_calories: Optional[int]

    # Subjective
    perceived_exertion: Optional[int]
    rpe: Optional[int]
    mood: Optional[str]
    energy_level: Optional[int]
    soreness_level: Optional[int]
    workout_rating: Optional[int]

    # Weather
    weather_conditions: Optional[str]
    temperature_celsius: Optional[float]
    indoor: bool

    # Location
    location: Optional[str]
    route_name: Optional[str]
    city: Optional[str]

    # Notes
    notes: Optional[str]
    private_notes: Optional[str]

    # Metadata
    tags: List[str]
    trainer: bool
    race: bool
    workout_type: Optional[str]

    # Timestamps
    created_at: str
    updated_at: str

    # Quick entry integration
    quick_entry_log_id: Optional[str]
    ai_extracted: bool = False
    ai_confidence: Optional[float]


class ActivitiesListResponse(BaseModel):
    """List of activities with pagination"""
    activities: List[ActivityResponse]
    total: int
    limit: int
    offset: int


class ActivityTypeConfigResponse(BaseModel):
    """Activity type configuration response"""
    activity_type: str
    display_name: str
    category: str
    icon: str
    description: str
    primary_fields: List[Dict[str, Any]]
    secondary_fields: List[Dict[str, Any]]
    supports_segments: bool
    supports_exercises: bool
    supports_sets: bool


class ActivityTypesResponse(BaseModel):
    """All activity types configuration"""
    activity_types: Dict[str, ActivityTypeConfigResponse]


# Allow forward references
ActivityExerciseRequest.model_rebuild()
ActivitySetRequest.model_rebuild()
