"""
Photo Meal Matcher Service

Matches photo-detected food descriptions with database foods using fuzzy matching.

This service wraps the existing food_search_service to provide specialized
matching logic for photo-detected meals.
"""

import logging
from typing import Dict, Any, List

from app.services.food_search_service import get_food_search_service

logger = logging.getLogger(__name__)


class PhotoMealMatcherService:
    """Service for matching photo-detected foods with database."""

    def __init__(self):
        self.food_search = get_food_search_service()

    async def match_photo_foods(
        self,
        detected_foods: List[Dict[str, str]],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Match photo-detected foods with database foods.

        Uses the existing food_search_service.match_detected_foods method
        which implements fuzzy matching, cooking method detection, and
        prioritizes user's recent foods.

        Args:
            detected_foods: List of dicts from photo analysis:
                [
                    {
                        "name": "grilled chicken breast",
                        "quantity": "6",
                        "unit": "oz",
                        "grams": "170"
                    },
                    ...
                ]
            user_id: User ID for personalized matching (recent foods priority)

        Returns:
            Dict with matched and unmatched foods:
            {
                "matched_foods": [
                    {
                        "id": str,
                        "name": str,
                        "brand_name": str | None,
                        "serving_size": float,
                        "serving_unit": str,
                        "household_serving_grams": float | None,
                        "household_serving_unit": str | None,
                        "calories": float,
                        "protein_g": float,
                        "total_carbs_g": float,
                        "total_fat_g": float,
                        "dietary_fiber_g": float,
                        "total_sugars_g": float,
                        "sodium_mg": float,
                        "detected_quantity": float,
                        "detected_unit": str,
                        "detected_grams": float | None,
                        "match_confidence": float,
                        "match_method": str
                    }
                ],
                "unmatched_foods": [
                    {"name": str, "reason": str}
                ],
                "total_detected": int,
                "total_matched": int,
                "match_rate": float
            }
        """
        try:
            logger.info(f"Matching {len(detected_foods)} photo-detected foods for user {user_id}")

            # Call existing food matching service
            # Note: food_search_service expects format: [{"name": str, "quantity": str, "unit": str}]
            # Our detected_foods already have this format
            match_result = await self.food_search.match_detected_foods(
                detected_foods=detected_foods,
                user_id=user_id
            )

            # Enhance matched foods with detected grams (if provided)
            for food in match_result["matched_foods"]:
                # Find the original detected food to get grams estimate
                detected = next(
                    (f for f in detected_foods if f["name"].lower() == food.get("name", "").lower()),
                    None
                )

                if detected and "grams" in detected:
                    try:
                        food["detected_grams"] = float(detected["grams"])
                    except (ValueError, TypeError):
                        food["detected_grams"] = None
                else:
                    food["detected_grams"] = None

            logger.info(
                f"✅ Matching complete: {match_result['total_matched']}/{match_result['total_detected']} "
                f"({match_result['match_rate']*100:.1f}%)"
            )

            return match_result

        except Exception as e:
            logger.error(f"Photo food matching failed: {e}", exc_info=True)
            raise


# Global instance
_service: PhotoMealMatcherService | None = None


def get_photo_meal_matcher_service() -> PhotoMealMatcherService:
    """Get the global PhotoMealMatcherService instance."""
    global _service
    if _service is None:
        _service = PhotoMealMatcherService()
    return _service
