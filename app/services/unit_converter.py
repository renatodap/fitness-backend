"""
Unit Converter Service

Converts food quantities between different units (oz, lb, cup, tbsp, tsp, etc.) to grams.

CRITICAL: This fixes the nutrition calculation bug where "5 oz chicken" was calculated
as "5 grams chicken" resulting in 9.6 cal instead of ~233 cal.

Priority conversion strategy:
1. Use household_serving_grams from food database if available
2. Use standard conversion tables (oz→28g, lb→454g, etc.)
3. Return as-is if already in grams or unknown unit
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Standard conversion factors (per 1 unit → grams)
# Source: USDA standard reference, culinary standards
UNIT_TO_GRAMS = {
    # Weight conversions (universal)
    "g": 1.0,
    "gram": 1.0,
    "grams": 1.0,
    "kg": 1000.0,
    "kilogram": 1000.0,
    "kilograms": 1000.0,
    "oz": 28.35,  # 1 oz = 28.35g
    "ounce": 28.35,
    "ounces": 28.35,
    "lb": 453.59,  # 1 lb = 453.59g
    "lbs": 453.59,
    "pound": 453.59,
    "pounds": 453.59,

    # Volume conversions (approximate for water, varies by food)
    # NOTE: These are AVERAGES - actual conversion depends on food density
    "cup": 240.0,  # 1 cup ≈ 240g (for water)
    "cups": 240.0,
    "tbsp": 15.0,  # 1 tablespoon ≈ 15g
    "tablespoon": 15.0,
    "tablespoons": 15.0,
    "tsp": 5.0,  # 1 teaspoon ≈ 5g
    "teaspoon": 5.0,
    "teaspoons": 5.0,
    "ml": 1.0,  # 1 ml ≈ 1g (for water)
    "milliliter": 1.0,
    "milliliters": 1.0,
    "l": 1000.0,  # 1 liter ≈ 1000g
    "liter": 1000.0,
    "liters": 1000.0,
    "fl oz": 29.57,  # 1 fluid oz ≈ 29.57g (for water)
    "fluid ounce": 29.57,
    "fluid ounces": 29.57,
    "floz": 29.57,

    # Piece conversions (handled separately - use household_serving_grams)
    "serving": None,  # Special case - use household_serving_grams
    "servings": None,
    "piece": None,
    "pieces": None,
    "slice": None,
    "slices": None,
    "item": None,
    "items": None,
    "each": None,
    "whole": None,
    "unit": None,
    "units": None,
}

# Food-specific volume-to-weight conversions
# These override UNIT_TO_GRAMS for specific food types
# Format: {food_keyword: {unit: grams_per_unit}}
FOOD_SPECIFIC_CONVERSIONS: Dict[str, Dict[str, float]] = {
    # Grains & Starches (cooked)
    "rice": {
        "cup": 195.0,  # Cooked white rice: 1 cup ≈ 195g
    },
    "pasta": {
        "cup": 140.0,  # Cooked pasta: 1 cup ≈ 140g
    },
    "oatmeal": {
        "cup": 234.0,  # Cooked oatmeal: 1 cup ≈ 234g
    },
    "quinoa": {
        "cup": 185.0,  # Cooked quinoa: 1 cup ≈ 185g
    },

    # Proteins
    "chicken": {
        "cup": 140.0,  # Diced cooked chicken: 1 cup ≈ 140g
    },
    "beef": {
        "cup": 140.0,  # Ground beef: 1 cup ≈ 140g
    },
    "salmon": {
        "cup": 140.0,  # Flaked salmon: 1 cup ≈ 140g
    },

    # Vegetables (cooked)
    "broccoli": {
        "cup": 156.0,  # Cooked broccoli: 1 cup ≈ 156g
    },
    "spinach": {
        "cup": 180.0,  # Cooked spinach: 1 cup ≈ 180g
    },
    "carrots": {
        "cup": 156.0,  # Cooked carrots: 1 cup ≈ 156g
    },

    # Liquids
    "milk": {
        "cup": 244.0,  # 1 cup ≈ 244g
    },
    "water": {
        "cup": 240.0,  # 1 cup ≈ 240g
    },
    "juice": {
        "cup": 248.0,  # 1 cup ≈ 248g
    },

    # Fats
    "oil": {
        "cup": 218.0,  # 1 cup ≈ 218g
        "tbsp": 13.5,  # 1 tbsp ≈ 13.5g
    },
    "butter": {
        "cup": 227.0,  # 1 cup ≈ 227g
        "tbsp": 14.2,  # 1 tbsp ≈ 14.2g
    },
}


def convert_to_grams(
    quantity: float,
    unit: str,
    food_name: Optional[str] = None,
    household_serving_grams: Optional[float] = None
) -> float:
    """
    Convert quantity from any unit to grams.

    Priority:
    1. If unit is "serving" and household_serving_grams is provided, use that
    2. Check food-specific conversions (e.g., "1 cup rice" = 195g, not 240g)
    3. Use standard conversion table (oz→28g, lb→454g, etc.)
    4. If already in grams or unknown unit, return as-is

    Args:
        quantity: Numeric quantity (e.g., 5.0)
        unit: Unit string (e.g., "oz", "cup", "serving")
        food_name: Optional food name for food-specific conversions
        household_serving_grams: Optional grams per household serving from DB

    Returns:
        float: Quantity in grams

    Example:
        >>> convert_to_grams(5.0, "oz", "Chicken Breast")
        141.75  # 5 oz × 28.35 g/oz = 141.75g

        >>> convert_to_grams(1.0, "cup", "White Rice, Cooked")
        195.0  # 1 cup cooked rice = 195g (food-specific)

        >>> convert_to_grams(2.5, "serving", household_serving_grams=28.0)
        70.0  # 2.5 servings × 28g/serving = 70g
    """
    # Normalize unit to lowercase
    unit_normalized = unit.lower().strip()

    logger.info(
        f"[unit_converter] Converting {quantity} {unit_normalized} "
        f"(food={food_name}, household_serving_grams={household_serving_grams})"
    )

    # PRIORITY 1: Serving units with household_serving_grams from database
    if unit_normalized in ["serving", "servings", "piece", "pieces", "slice", "slices", "item", "items", "each", "whole", "unit", "units"]:
        if household_serving_grams is not None:
            grams = quantity * household_serving_grams
            logger.info(
                f"[unit_converter]   ✅ Using DB household_serving_grams: "
                f"{quantity} {unit_normalized} × {household_serving_grams}g = {grams}g"
            )
            return grams
        else:
            # Fallback: Assume 1 serving = 100g if not specified
            logger.warning(
                f"[unit_converter]   ⚠️  '{unit_normalized}' detected but no household_serving_grams! "
                f"Defaulting to 100g per {unit_normalized}"
            )
            return quantity * 100.0

    # PRIORITY 2: Food-specific conversions (e.g., "1 cup rice" ≠ "1 cup water")
    if food_name:
        food_name_lower = food_name.lower()
        for food_keyword, conversions in FOOD_SPECIFIC_CONVERSIONS.items():
            if food_keyword in food_name_lower:
                if unit_normalized in conversions:
                    conversion_factor = conversions[unit_normalized]
                    grams = quantity * conversion_factor
                    logger.info(
                        f"[unit_converter]   ✅ Using food-specific conversion for '{food_keyword}': "
                        f"{quantity} {unit_normalized} × {conversion_factor}g = {grams}g"
                    )
                    return grams

    # PRIORITY 3: Standard conversion table
    if unit_normalized in UNIT_TO_GRAMS:
        conversion_factor = UNIT_TO_GRAMS[unit_normalized]
        if conversion_factor is not None:
            grams = quantity * conversion_factor
            logger.info(
                f"[unit_converter]   ✅ Using standard conversion: "
                f"{quantity} {unit_normalized} × {conversion_factor}g = {grams}g"
            )
            return grams

    # PRIORITY 4: Already in grams or unknown unit - return as-is
    logger.warning(
        f"[unit_converter]   ⚠️  Unknown unit '{unit_normalized}', returning quantity as grams: {quantity}g"
    )
    return quantity


# Example usage for testing
if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.INFO)

    print("\n=== Unit Converter Test Cases ===\n")

    # Test 1: Weight conversions
    print("Test 1: Weight conversions")
    print(f"5 oz -> {convert_to_grams(5.0, 'oz')}g (expected: ~141.75g)")
    print(f"1 lb -> {convert_to_grams(1.0, 'lb')}g (expected: ~453.59g)")
    print(f"100 g -> {convert_to_grams(100.0, 'g')}g (expected: 100g)")

    # Test 2: Volume conversions (generic)
    print("\nTest 2: Volume conversions (generic)")
    print(f"1 cup (water) -> {convert_to_grams(1.0, 'cup')}g (expected: 240g)")
    print(f"1 tbsp -> {convert_to_grams(1.0, 'tbsp')}g (expected: 15g)")
    print(f"1 tsp -> {convert_to_grams(1.0, 'tsp')}g (expected: 5g)")

    # Test 3: Food-specific conversions
    print("\nTest 3: Food-specific conversions")
    print(f"1 cup rice -> {convert_to_grams(1.0, 'cup', 'White Rice, Cooked')}g (expected: 195g)")
    print(f"1 cup milk -> {convert_to_grams(1.0, 'cup', 'Milk')}g (expected: 244g)")
    print(f"1 cup chicken -> {convert_to_grams(1.0, 'cup', 'Chicken Breast')}g (expected: 140g)")

    # Test 4: Serving conversions with household_serving_grams
    print("\nTest 4: Serving conversions with household_serving_grams")
    print(f"2 slices (28g each) -> {convert_to_grams(2.0, 'slice', household_serving_grams=28.0)}g (expected: 56g)")
    print(f"1 piece (140g) -> {convert_to_grams(1.0, 'piece', household_serving_grams=140.0)}g (expected: 140g)")

    # Test 5: The actual bug case
    print("\nTest 5: The actual bug case from production logs")
    print(f"5 oz chicken (should be 141.75g, not 5g) -> {convert_to_grams(5.0, 'oz', 'Chicken Breast')}g")
    print(f"1 cup rice (should be 195g, not 1g) -> {convert_to_grams(1.0, 'cup', 'White Rice, Cooked')}g")

    print("\n=== All tests complete ===\n")
