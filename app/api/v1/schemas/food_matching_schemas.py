"""
Food Matching Schemas

Request/Response models for matching detected foods to database.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class DetectedFood(BaseModel):
    """A food detected from image analysis."""
    name: str = Field(..., description="Detected food name (e.g., 'grilled chicken')")
    quantity: str = Field(..., description="Detected quantity (e.g., '150')")
    unit: str = Field(..., description="Detected unit (e.g., 'g', 'oz', 'cup')")


class MatchDetectedFoodsRequest(BaseModel):
    """Request to match detected foods to database."""
    detected_foods: List[DetectedFood] = Field(
        ...,
        description="List of foods detected from image analysis",
        min_items=1,
        max_items=20
    )


class MatchedFood(BaseModel):
    """A food that was matched to the database."""
    # Database fields
    id: str = Field(..., description="Database food ID")
    name: str = Field(..., description="Database food name")
    brand_name: Optional[str] = Field(None, description="Brand name if branded food")
    food_group: Optional[str] = Field(None, description="Food group category")

    # Serving information
    serving_size: float = Field(..., description="Standard serving size")
    serving_unit: str = Field(..., description="Standard serving unit")

    # Nutrition (per serving)
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = Field(None, alias="total_carbs_g")
    fat_g: Optional[float] = Field(None, alias="total_fat_g")
    fiber_g: Optional[float] = Field(None, alias="dietary_fiber_g")
    sugar_g: Optional[float] = Field(None, alias="total_sugars_g")
    sodium_mg: Optional[float] = None

    # Detected quantity (what user actually has)
    detected_quantity: float = Field(..., description="Quantity detected from image")
    detected_unit: str = Field(..., description="Unit detected from image")

    # Match metadata
    match_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score of the match (0-1)"
    )
    match_method: str = Field(
        ...,
        description="Method used to find match (exact, fuzzy, recent, generic)"
    )

    # Quality indicators
    is_recent: bool = Field(False, description="Whether this was in user's recent foods")
    data_quality_score: Optional[float] = None

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class UnmatchedFood(BaseModel):
    """A food that couldn't be matched to the database."""
    name: str = Field(..., description="Original detected food name")
    reason: str = Field(..., description="Why it couldn't be matched")


class MatchDetectedFoodsResponse(BaseModel):
    """Response with matched and unmatched foods."""
    matched_foods: List[MatchedFood] = Field(
        default_factory=list,
        description="Foods successfully matched to database"
    )
    unmatched_foods: List[UnmatchedFood] = Field(
        default_factory=list,
        description="Foods that couldn't be matched"
    )
    total_detected: int = Field(..., description="Total number of foods detected")
    total_matched: int = Field(..., description="Number of foods matched")
    match_rate: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Percentage of foods matched (0-1)"
    )
