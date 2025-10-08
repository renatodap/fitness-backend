"""
Activity Type Configuration

Defines field requirements and metadata for each activity type.
This drives both backend validation and frontend form generation.
"""

from typing import Dict, List, Optional
from enum import Enum


class ActivityTypeCategory(str, Enum):
    """High-level activity categories"""
    CARDIO = "cardio"
    STRENGTH = "strength"
    SPORTS = "sports"
    FLEXIBILITY = "flexibility"
    MIND_BODY = "mind_body"
    RECREATIONAL = "recreational"


class FieldType(str, Enum):
    """Field data types for validation"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    ARRAY = "array"
    OBJECT = "object"


class ActivityField:
    """Definition of an activity field"""
    def __init__(
        self,
        name: str,
        label: str,
        field_type: FieldType,
        required: bool = False,
        unit: Optional[str] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        placeholder: Optional[str] = None,
        help_text: Optional[str] = None
    ):
        self.name = name
        self.label = label
        self.field_type = field_type
        self.required = required
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.placeholder = placeholder
        self.help_text = help_text

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "name": self.name,
            "label": self.label,
            "field_type": self.field_type.value,
            "required": self.required,
            "unit": self.unit,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "placeholder": self.placeholder,
            "help_text": self.help_text
        }


class ActivityTypeConfig:
    """Configuration for an activity type"""
    def __init__(
        self,
        activity_type: str,
        display_name: str,
        category: ActivityTypeCategory,
        icon: str,
        description: str,
        primary_fields: List[ActivityField],
        secondary_fields: List[ActivityField],
        supports_segments: bool = False,
        supports_exercises: bool = False,
        supports_sets: bool = False
    ):
        self.activity_type = activity_type
        self.display_name = display_name
        self.category = category
        self.icon = icon
        self.description = description
        self.primary_fields = primary_fields
        self.secondary_fields = secondary_fields
        self.supports_segments = supports_segments
        self.supports_exercises = supports_exercises
        self.supports_sets = supports_sets

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "activity_type": self.activity_type,
            "display_name": self.display_name,
            "category": self.category.value,
            "icon": self.icon,
            "description": self.description,
            "primary_fields": [f.to_dict() for f in self.primary_fields],
            "secondary_fields": [f.to_dict() for f in self.secondary_fields],
            "supports_segments": self.supports_segments,
            "supports_exercises": self.supports_exercises,
            "supports_sets": self.supports_sets
        }


# ============================================================================
# ACTIVITY TYPE CONFIGURATIONS
# ============================================================================

ACTIVITY_TYPE_CONFIGS: Dict[str, ActivityTypeConfig] = {
    # CARDIO ACTIVITIES
    "running": ActivityTypeConfig(
        activity_type="running",
        display_name="Running",
        category=ActivityTypeCategory.CARDIO,
        icon="🏃",
        description="Outdoor or treadmill running",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Morning Run"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=600),
            ActivityField("distance_meters", "Distance", FieldType.FLOAT, required=True, unit="meters", min_value=0),
        ],
        secondary_fields=[
            ActivityField("average_pace", "Average Pace", FieldType.STRING, unit="min/mile", placeholder="8:30"),
            ActivityField("average_speed", "Average Speed", FieldType.FLOAT, unit="mph", min_value=0),
            ActivityField("total_elevation_gain", "Elevation Gain", FieldType.FLOAT, unit="meters", min_value=0),
            ActivityField("average_heartrate", "Avg Heart Rate", FieldType.INTEGER, unit="bpm", min_value=40, max_value=220),
            ActivityField("max_heartrate", "Max Heart Rate", FieldType.INTEGER, unit="bpm", min_value=40, max_value=220),
            ActivityField("average_cadence", "Avg Cadence", FieldType.INTEGER, unit="spm", min_value=0),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING, placeholder="How did it feel?"),
        ],
        supports_segments=True,
        supports_exercises=False,
        supports_sets=False
    ),

    "cycling": ActivityTypeConfig(
        activity_type="cycling",
        display_name="Cycling",
        category=ActivityTypeCategory.CARDIO,
        icon="🚴",
        description="Road, mountain, or indoor cycling",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Evening Ride"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=600),
            ActivityField("distance_meters", "Distance", FieldType.FLOAT, required=True, unit="meters", min_value=0),
        ],
        secondary_fields=[
            ActivityField("average_speed", "Average Speed", FieldType.FLOAT, unit="mph", min_value=0),
            ActivityField("max_speed", "Max Speed", FieldType.FLOAT, unit="mph", min_value=0),
            ActivityField("total_elevation_gain", "Elevation Gain", FieldType.FLOAT, unit="meters", min_value=0),
            ActivityField("average_heartrate", "Avg Heart Rate", FieldType.INTEGER, unit="bpm", min_value=40, max_value=220),
            ActivityField("average_power", "Avg Power", FieldType.FLOAT, unit="watts", min_value=0),
            ActivityField("max_power", "Max Power", FieldType.INTEGER, unit="watts", min_value=0),
            ActivityField("normalized_power", "Normalized Power", FieldType.FLOAT, unit="watts", min_value=0),
            ActivityField("average_cadence", "Avg Cadence", FieldType.INTEGER, unit="rpm", min_value=0),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("trainer", "Indoor Trainer", FieldType.BOOLEAN),
            ActivityField("notes", "Notes", FieldType.STRING),
        ],
        supports_segments=True,
        supports_exercises=False,
        supports_sets=False
    ),

    "swimming": ActivityTypeConfig(
        activity_type="swimming",
        display_name="Swimming",
        category=ActivityTypeCategory.CARDIO,
        icon="🏊",
        description="Pool or open water swimming",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Swim Workout"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=300),
            ActivityField("distance_meters", "Distance", FieldType.FLOAT, required=True, unit="meters", min_value=0),
        ],
        secondary_fields=[
            ActivityField("pool_length", "Pool Length", FieldType.FLOAT, unit="meters", placeholder="25 or 50"),
            ActivityField("total_strokes", "Total Strokes", FieldType.INTEGER, min_value=0),
            ActivityField("average_stroke_rate", "Avg Stroke Rate", FieldType.FLOAT, unit="strokes/min", min_value=0),
            ActivityField("average_swolf", "Avg SWOLF", FieldType.FLOAT, min_value=0),
            ActivityField("lap_count", "Total Laps", FieldType.INTEGER, min_value=0),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING),
        ],
        supports_segments=True,
        supports_exercises=False,
        supports_sets=False
    ),

    "walking": ActivityTypeConfig(
        activity_type="walking",
        display_name="Walking",
        category=ActivityTypeCategory.CARDIO,
        icon="🚶",
        description="Casual or brisk walking",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Morning Walk"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=600),
        ],
        secondary_fields=[
            ActivityField("distance_meters", "Distance", FieldType.FLOAT, unit="meters", min_value=0),
            ActivityField("average_speed", "Average Speed", FieldType.FLOAT, unit="mph", min_value=0),
            ActivityField("total_elevation_gain", "Elevation Gain", FieldType.FLOAT, unit="meters", min_value=0),
            ActivityField("average_heartrate", "Avg Heart Rate", FieldType.INTEGER, unit="bpm", min_value=40, max_value=220),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING),
        ],
        supports_segments=False,
        supports_exercises=False,
        supports_sets=False
    ),

    "hiking": ActivityTypeConfig(
        activity_type="hiking",
        display_name="Hiking",
        category=ActivityTypeCategory.RECREATIONAL,
        icon="🥾",
        description="Trail hiking or mountaineering",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Trail Hike"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=1200),
        ],
        secondary_fields=[
            ActivityField("distance_meters", "Distance", FieldType.FLOAT, unit="meters", min_value=0),
            ActivityField("total_elevation_gain", "Elevation Gain", FieldType.FLOAT, unit="meters", min_value=0),
            ActivityField("elevation_high", "High Point", FieldType.FLOAT, unit="meters"),
            ActivityField("average_heartrate", "Avg Heart Rate", FieldType.INTEGER, unit="bpm", min_value=40, max_value=220),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("location", "Location/Trail Name", FieldType.STRING),
            ActivityField("notes", "Notes", FieldType.STRING),
        ],
        supports_segments=False,
        supports_exercises=False,
        supports_sets=False
    ),

    # STRENGTH TRAINING
    "strength_training": ActivityTypeConfig(
        activity_type="strength_training",
        display_name="Strength Training",
        category=ActivityTypeCategory.STRENGTH,
        icon="🏋️",
        description="Weightlifting, bodyweight, or resistance training",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Upper Body Workout"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=300),
        ],
        secondary_fields=[
            ActivityField("total_sets", "Total Sets", FieldType.INTEGER, min_value=0),
            ActivityField("total_reps", "Total Reps", FieldType.INTEGER, min_value=0),
            ActivityField("total_weight_lifted_kg", "Total Weight Lifted", FieldType.FLOAT, unit="kg", min_value=0),
            ActivityField("exercise_count", "Number of Exercises", FieldType.INTEGER, min_value=0),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING),
        ],
        supports_segments=False,
        supports_exercises=True,  # Uses activity_exercises table
        supports_sets=True  # Uses activity_sets table
    ),

    "crossfit": ActivityTypeConfig(
        activity_type="crossfit",
        display_name="CrossFit/Functional Fitness",
        category=ActivityTypeCategory.STRENGTH,
        icon="⚡",
        description="CrossFit WOD or functional fitness",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Fran WOD"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=120),
        ],
        secondary_fields=[
            ActivityField("total_reps", "Total Reps", FieldType.INTEGER, min_value=0),
            ActivityField("total_rounds", "Rounds", FieldType.INTEGER, min_value=0, help_text="For AMRAP workouts"),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING, help_text="WOD details, movements, weights"),
        ],
        supports_segments=True,  # Can track rounds
        supports_exercises=True,
        supports_sets=True
    ),

    # SPORTS
    "tennis": ActivityTypeConfig(
        activity_type="tennis",
        display_name="Tennis",
        category=ActivityTypeCategory.SPORTS,
        icon="🎾",
        description="Tennis practice or match",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Tennis Match"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=300),
        ],
        secondary_fields=[
            ActivityField("match_type", "Match Type", FieldType.STRING, help_text="Singles, doubles, practice"),
            ActivityField("sets_played", "Sets Played", FieldType.INTEGER, min_value=0),
            ActivityField("games_played", "Games Played", FieldType.INTEGER, min_value=0),
            ActivityField("total_shots", "Total Shots", FieldType.INTEGER, min_value=0),
            ActivityField("forehand_count", "Forehands", FieldType.INTEGER, min_value=0),
            ActivityField("backhand_count", "Backhands", FieldType.INTEGER, min_value=0),
            ActivityField("serve_count", "Serves", FieldType.INTEGER, min_value=0),
            ActivityField("ace_count", "Aces", FieldType.INTEGER, min_value=0),
            ActivityField("winner_count", "Winners", FieldType.INTEGER, min_value=0),
            ActivityField("unforced_error_count", "Unforced Errors", FieldType.INTEGER, min_value=0),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING, help_text="Score, opponents, conditions"),
        ],
        supports_segments=False,
        supports_exercises=False,
        supports_sets=False
    ),

    "soccer": ActivityTypeConfig(
        activity_type="soccer",
        display_name="Soccer/Football",
        category=ActivityTypeCategory.SPORTS,
        icon="⚽",
        description="Soccer training or match",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Soccer Practice"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=200),
        ],
        secondary_fields=[
            ActivityField("session_type", "Session Type", FieldType.STRING, help_text="Training, match, scrimmage"),
            ActivityField("position", "Position Played", FieldType.STRING),
            ActivityField("distance_meters", "Distance Covered", FieldType.FLOAT, unit="meters", min_value=0),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING, help_text="Score, goals, assists"),
        ],
        supports_segments=False,
        supports_exercises=False,
        supports_sets=False
    ),

    "basketball": ActivityTypeConfig(
        activity_type="basketball",
        display_name="Basketball",
        category=ActivityTypeCategory.SPORTS,
        icon="🏀",
        description="Basketball training or game",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Basketball Game"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=180),
        ],
        secondary_fields=[
            ActivityField("session_type", "Session Type", FieldType.STRING, help_text="Training, game, pickup"),
            ActivityField("position", "Position Played", FieldType.STRING),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING, help_text="Score, stats, highlights"),
        ],
        supports_segments=False,
        supports_exercises=False,
        supports_sets=False
    ),

    # FLEXIBILITY & MIND-BODY
    "yoga": ActivityTypeConfig(
        activity_type="yoga",
        display_name="Yoga",
        category=ActivityTypeCategory.MIND_BODY,
        icon="🧘",
        description="Yoga practice or class",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Morning Yoga"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=120),
        ],
        secondary_fields=[
            ActivityField("yoga_style", "Yoga Style", FieldType.STRING, help_text="Hatha, Vinyasa, Ashtanga, etc."),
            ActivityField("poses_held", "Poses Held", FieldType.INTEGER, min_value=0),
            ActivityField("average_hold_duration", "Avg Hold Time", FieldType.INTEGER, unit="seconds", min_value=0),
            ActivityField("flexibility_score", "Flexibility Score", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING),
        ],
        supports_segments=False,
        supports_exercises=False,
        supports_sets=False
    ),

    # RECREATIONAL
    "climbing": ActivityTypeConfig(
        activity_type="climbing",
        display_name="Rock Climbing",
        category=ActivityTypeCategory.RECREATIONAL,
        icon="🧗",
        description="Indoor or outdoor climbing",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Climbing Session"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=300),
        ],
        secondary_fields=[
            ActivityField("climbing_type", "Climbing Type", FieldType.STRING, help_text="Bouldering, sport, trad, top-rope"),
            ActivityField("location", "Location/Gym", FieldType.STRING),
            ActivityField("total_elevation_gain", "Elevation Climbed", FieldType.FLOAT, unit="meters", min_value=0),
            ActivityField("route_count", "Routes Completed", FieldType.INTEGER, min_value=0),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING, help_text="Grades, sends, projects"),
        ],
        supports_segments=False,
        supports_exercises=False,
        supports_sets=False
    ),

    # GENERAL
    "workout": ActivityTypeConfig(
        activity_type="workout",
        display_name="General Workout",
        category=ActivityTypeCategory.STRENGTH,
        icon="💪",
        description="General workout or training session",
        primary_fields=[
            ActivityField("name", "Activity Name", FieldType.STRING, required=True, placeholder="Training Session"),
            ActivityField("start_date", "Start Time", FieldType.DATETIME, required=True),
            ActivityField("duration_minutes", "Duration", FieldType.INTEGER, required=True, unit="minutes", min_value=1, max_value=300),
        ],
        secondary_fields=[
            ActivityField("workout_type", "Workout Type", FieldType.STRING, help_text="What kind of workout?"),
            ActivityField("calories", "Calories Burned", FieldType.INTEGER, unit="cal", min_value=0),
            ActivityField("perceived_exertion", "RPE", FieldType.INTEGER, unit="/10", min_value=1, max_value=10),
            ActivityField("notes", "Notes", FieldType.STRING),
        ],
        supports_segments=False,
        supports_exercises=True,
        supports_sets=True
    ),
}


def get_activity_type_config(activity_type: str) -> Optional[ActivityTypeConfig]:
    """Get configuration for an activity type"""
    return ACTIVITY_TYPE_CONFIGS.get(activity_type)


def get_all_activity_types() -> Dict[str, ActivityTypeConfig]:
    """Get all activity type configurations"""
    return ACTIVITY_TYPE_CONFIGS


def get_activity_types_by_category(category: ActivityTypeCategory) -> Dict[str, ActivityTypeConfig]:
    """Get activity types filtered by category"""
    return {
        k: v for k, v in ACTIVITY_TYPE_CONFIGS.items()
        if v.category == category
    }


def get_supported_activity_types() -> List[str]:
    """Get list of all supported activity type keys"""
    return list(ACTIVITY_TYPE_CONFIGS.keys())
