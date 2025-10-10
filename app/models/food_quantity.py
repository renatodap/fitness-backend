"""
Food Quantity Models - Dual Quantity Tracking

This module defines models for handling both serving and gram quantities
simultaneously, solving the fundamental issue of lossy conversions.
"""
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator


class FoodQuantity(BaseModel):
    """
    Represents both serving and gram quantities for a food item.
    
    This model ensures bidirectional tracking - we always know both
    how many servings AND how many grams the user has logged.
    
    Attributes:
        serving_quantity: Number of servings (e.g., 2.5 slices)
        serving_unit: Serving unit name (e.g., "slice", "medium", "scoop")
        gram_quantity: Quantity in grams (source of truth for calculations)
        last_edited_field: Which field user last edited ('serving' or 'grams')
    
    Example:
        >>> quantity = FoodQuantity(
        ...     serving_quantity=Decimal('2.5'),
        ...     serving_unit='slice',
        ...     gram_quantity=Decimal('70'),
        ...     last_edited_field='serving'
        ... )
    """
    serving_quantity: Decimal = Field(
        ..., 
        gt=0, 
        description="Number of servings (e.g., 2.5)"
    )
    serving_unit: Optional[str] = Field(
        None, 
        description="Serving unit name (slice, medium, etc.) or None for generic"
    )
    gram_quantity: Decimal = Field(
        ..., 
        gt=0, 
        description="Quantity in grams (always stored)"
    )
    last_edited_field: Literal['serving', 'grams'] = Field(
        'grams',
        description="Which field user last edited"
    )
    
    @validator('serving_quantity', 'gram_quantity')
    def validate_positive(cls, v):
        """Ensure quantities are positive and within reasonable bounds."""
        if v <= 0:
            raise ValueError("Quantity must be positive")
        if v > 100000:  # Sanity check: 100kg max
            raise ValueError("Quantity exceeds reasonable limits (max 100kg)")
        return v
    
    @validator('serving_unit')
    def validate_serving_unit(cls, v):
        """Ensure serving unit is reasonable."""
        if v and len(v) > 50:
            raise ValueError("Serving unit name too long (max 50 characters)")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "serving_quantity": 2.5,
                "serving_unit": "slice",
                "gram_quantity": 70.0,
                "last_edited_field": "serving"
            }
        }


class FoodQuantityRequest(BaseModel):
    """
    Request model for updating food quantity.
    
    Used when user edits either serving or gram quantity in the UI.
    The system will calculate the other quantity automatically.
    
    Attributes:
        input_quantity: The quantity value user entered
        input_field: Which field was edited ('serving' or 'grams')
    
    Example:
        >>> request = FoodQuantityRequest(
        ...     input_quantity=Decimal('3'),
        ...     input_field='serving'
        ... )
    """
    input_quantity: Decimal = Field(
        ..., 
        gt=0,
        description="The quantity value user entered"
    )
    input_field: Literal['serving', 'grams'] = Field(
        ...,
        description="Which field was edited"
    )
    
    @validator('input_quantity')
    def validate_input_quantity(cls, v):
        """Ensure input quantity is positive and reasonable."""
        if v <= 0:
            raise ValueError("Input quantity must be positive")
        if v > 100000:
            raise ValueError("Input quantity exceeds reasonable limits")
        return v


class FoodQuantityResponse(BaseModel):
    """
    Response model with calculated quantity data.
    
    Returns both serving and gram quantities plus nutrition information.
    """
    serving_quantity: float
    serving_unit: Optional[str]
    gram_quantity: float
    last_edited_field: str
    
    # Calculated nutrition based on gram_quantity
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    sugar_g: Optional[float] = None
    sodium_mg: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "serving_quantity": 2.0,
                "serving_unit": "slice",
                "gram_quantity": 56.0,
                "last_edited_field": "serving",
                "calories": 156.8,
                "protein_g": 8.4,
                "carbs_g": 26.0,
                "fat_g": 2.2,
                "fiber_g": 3.6,
                "sugar_g": 2.8,
                "sodium_mg": 280.0
            }
        }
