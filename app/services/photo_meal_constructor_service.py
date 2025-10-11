"""
Photo Meal Constructor Service

Constructs meal log preview structure from matched foods.

This service builds a complete meal log structure ready for confirmation/saving,
including:
- Individual food items with nutrition
- Common unit conversions (grams ↔ oz/cups)
- Total nutrition summary
- Metadata for frontend display
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


# Common unit conversion factors (to grams)
UNIT_CONVERSIONS = {
    "g": 1.0,
    "kg": 1000.0,
    "oz": 28.3495,
    "lb": 453.592,
    "ml": 1.0,  # Assume density of 1 for liquids
    "l": 1000.0,
    "cup": 240.0,  # Standard US cup
    "tbsp": 15.0,
    "tsp": 5.0,
    "serving": None,  # Handled specially (use food's serving_size)
}


class PhotoMealConstructorService:
    """Service for constructing meal preview structure from matched foods."""

    def __init__(self):
        pass

    async def construct_meal_preview(
        self,
        matched_foods: List[Dict[str, Any]],
        meal_metadata: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Construct a complete meal log preview structure.

        Args:
            matched_foods: List of matched foods from matcher service
            meal_metadata: Metadata from photo analysis (meal_type, description)
            user_id: User ID

        Returns:
            Complete meal preview structure ready for confirmation:
            {
                "preview_id": str (temporary ID),
                "meal_type": str,
                "description": str,
                "logged_at": str (ISO timestamp),
                "foods": [
                    {
                        "food_id": str,
                        "name": str,
                        "brand": str | None,
                        "grams": float,
                        "common_unit_amount": float,
                        "common_unit": str,
                        "serving_size": float,
                        "serving_unit": str,
                        "calories": float,
                        "protein_g": float,
                        "carbs_g": float,
                        "fat_g": float,
                        "fiber_g": float,
                        "sugar_g": float,
                        "sodium_mg": float,
                        "match_confidence": float
                    }
                ],
                "totals": {
                    "calories": float,
                    "protein_g": float,
                    "carbs_g": float,
                    "fat_g": float,
                    "fiber_g": float,
                    "sugar_g": float,
                    "sodium_mg": float
                },
                "meta": {
                    "total_foods": int,
                    "analysis_description": str,
                    "detected_at": str (ISO timestamp)
                }
            }
        """
        try:
            logger.info(f"Constructing meal preview: {len(matched_foods)} foods, user_id={user_id}")

            # Build food items with calculated nutrition
            constructed_foods = []
            totals = {
                "calories": 0.0,
                "protein_g": 0.0,
                "carbs_g": 0.0,
                "fat_g": 0.0,
                "fiber_g": 0.0,
                "sugar_g": 0.0,
                "sodium_mg": 0.0
            }

            for food in matched_foods:
                # Calculate nutrition based on detected quantity
                food_item = self._construct_food_item(food)
                constructed_foods.append(food_item)

                # Accumulate totals
                totals["calories"] += food_item["calories"]
                totals["protein_g"] += food_item["protein_g"]
                totals["carbs_g"] += food_item["carbs_g"]
                totals["fat_g"] += food_item["fat_g"]
                totals["fiber_g"] += food_item["fiber_g"]
                totals["sugar_g"] += food_item["sugar_g"]
                totals["sodium_mg"] += food_item["sodium_mg"]

            # Round totals
            for key in totals:
                totals[key] = round(totals[key], 1)

            # Build preview structure
            preview = {
                "preview_id": f"preview_{int(datetime.utcnow().timestamp())}",
                "meal_type": meal_metadata.get("meal_type", "lunch"),
                "description": meal_metadata.get("description", "Photo-detected meal"),
                "logged_at": datetime.utcnow().isoformat(),
                "foods": constructed_foods,
                "totals": totals,
                "meta": {
                    "total_foods": len(constructed_foods),
                    "analysis_description": meal_metadata.get("description", ""),
                    "detected_at": datetime.utcnow().isoformat()
                }
            }

            logger.info(
                f"✅ Meal preview constructed: {len(constructed_foods)} foods, "
                f"{totals['calories']} calories, {totals['protein_g']}g protein"
            )

            return preview

        except Exception as e:
            logger.error(f"Meal construction failed: {e}", exc_info=True)
            raise

    def _construct_food_item(self, matched_food: Dict[str, Any]) -> Dict[str, Any]:
        """
        Construct a single food item with nutrition calculations.

        Args:
            matched_food: Matched food from matcher service

        Returns:
            Food item dict with calculated nutrition
        """
        # Extract detected quantity and unit
        detected_qty = float(matched_food.get("detected_quantity", 1))
        detected_unit = matched_food.get("detected_unit", "serving")
        detected_grams = matched_food.get("detected_grams")

        # Get food's base nutrition (per serving_size)
        serving_size = matched_food.get("serving_size", 100)  # Default 100g
        serving_unit = matched_food.get("serving_unit", "g")

        # Calculate actual grams for this food
        if detected_grams:
            # Use OpenAI's gram estimate if available
            actual_grams = float(detected_grams)
        elif detected_unit == "g" or detected_unit == "grams":
            # User specified grams directly
            actual_grams = detected_qty
        elif detected_unit == "serving":
            # Use food's serving size
            actual_grams = detected_qty * serving_size
        else:
            # Convert detected unit to grams using conversion factors
            conversion = UNIT_CONVERSIONS.get(detected_unit)
            if conversion:
                actual_grams = detected_qty * conversion
            else:
                # Fallback: assume detected_qty is in servings
                actual_grams = detected_qty * serving_size

        # Calculate scaling factor
        scale = actual_grams / serving_size

        # Calculate scaled nutrition
        base_nutrition = {
            "calories": matched_food.get("calories", 0),
            "protein_g": matched_food.get("protein_g", 0),
            "total_carbs_g": matched_food.get("total_carbs_g", 0),
            "total_fat_g": matched_food.get("total_fat_g", 0),
            "dietary_fiber_g": matched_food.get("dietary_fiber_g", 0),
            "total_sugars_g": matched_food.get("total_sugars_g", 0),
            "sodium_mg": matched_food.get("sodium_mg", 0)
        }

        # Convert grams back to common unit for display
        common_unit_amount, common_unit = self._convert_grams_to_common_unit(
            actual_grams,
            detected_unit
        )

        return {
            "food_id": matched_food["id"],
            "name": matched_food["name"],
            "brand": matched_food.get("brand_name"),
            "grams": round(actual_grams, 1),
            "common_unit_amount": common_unit_amount,
            "common_unit": common_unit,
            "serving_size": serving_size,
            "serving_unit": serving_unit,
            "calories": round(base_nutrition["calories"] * scale, 1),
            "protein_g": round(base_nutrition["protein_g"] * scale, 1),
            "carbs_g": round(base_nutrition["total_carbs_g"] * scale, 1),
            "fat_g": round(base_nutrition["total_fat_g"] * scale, 1),
            "fiber_g": round(base_nutrition["dietary_fiber_g"] * scale, 1),
            "sugar_g": round(base_nutrition["total_sugars_g"] * scale, 1),
            "sodium_mg": round(base_nutrition["sodium_mg"] * scale, 1),
            "match_confidence": matched_food.get("match_confidence", 1.0)
        }

    def _convert_grams_to_common_unit(
        self,
        grams: float,
        original_unit: str
    ) -> tuple[float, str]:
        """
        Convert grams to a human-readable common unit.

        Args:
            grams: Amount in grams
            original_unit: The unit detected from photo

        Returns:
            Tuple of (amount, unit) for display
        """
        # If original unit was already in common units, try to preserve it
        if original_unit in ["oz", "cup", "tbsp", "tsp", "piece", "slice", "serving"]:
            conversion = UNIT_CONVERSIONS.get(original_unit)
            if conversion:
                amount = grams / conversion
                return (round(amount, 1), original_unit)

        # Default conversions based on gram amount
        if grams < 15:
            return (round(grams, 1), "g")
        elif grams < 500:
            # Convert to oz for medium amounts
            oz = grams / 28.3495
            return (round(oz, 1), "oz")
        else:
            # Keep in grams for large amounts
            return (round(grams, 1), "g")


# Global instance
_service: Optional[PhotoMealConstructorService] = None


def get_photo_meal_constructor_service() -> PhotoMealConstructorService:
    """Get the global PhotoMealConstructorService instance."""
    global _service
    if _service is None:
        _service = PhotoMealConstructorService()
    return _service
