"""
Meal Logging Service

Handles manual meal logging with:
- Creating meals from food database
- Calculating nutrition totals
- Unit conversions
- Meal CRUD operations
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID

from app.services.supabase_service import get_service_client
from app.services.food_search_service import get_food_search_service

logger = logging.getLogger(__name__)


# Unit conversion factors (to grams)
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


class MealLoggingService:
    """Service for manual meal logging operations."""

    def __init__(self):
        self.supabase = get_service_client()
        self.food_search = get_food_search_service()

    async def create_meal(
        self,
        user_id: str,
        name: Optional[str],
        category: str,
        logged_at: str,
        notes: Optional[str],
        food_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create new meal log with foods.

        Args:
            user_id: User ID
            name: Meal name (optional)
            category: Meal type (breakfast, lunch, dinner, snack)
            logged_at: ISO timestamp
            notes: Optional notes
            food_items: List of {food_id, quantity, unit}

        Returns:
            Created meal with full nutrition data
        """
        try:
            logger.info(f"Creating meal: user_id={user_id}, category={category}, foods={len(food_items)}")

            # Step 1: Fetch food data for all items
            food_ids = [item["food_id"] for item in food_items]
            foods_data = await self._fetch_foods(food_ids)

            # Step 2: Calculate nutrition for each food item
            foods_with_nutrition = []
            total_calories = 0.0
            total_protein = 0.0
            total_carbs = 0.0
            total_fat = 0.0
            total_fiber = 0.0
            total_sugar = 0.0
            total_sodium = 0.0

            for idx, item in enumerate(food_items):
                food_id = item["food_id"]
                quantity = item["quantity"]
                unit = item["unit"]

                # Get food data
                food_data = foods_data.get(food_id)
                if not food_data:
                    logger.warning(f"Food not found: {food_id}")
                    continue

                # Calculate scaled nutrition
                scaled_nutrition = self._scale_nutrition(
                    food_data=food_data,
                    quantity=quantity,
                    unit=unit
                )

                # Build food item for JSONB
                food_item = {
                    "food_id": food_id,
                    "name": food_data["name"],
                    "brand": food_data.get("brand_name"),
                    "quantity": quantity,
                    "unit": unit,
                    "serving_size": food_data["serving_size"],
                    "serving_unit": food_data["serving_unit"],
                    **scaled_nutrition,
                    "order": idx + 1
                }

                foods_with_nutrition.append(food_item)

                # Accumulate totals
                total_calories += scaled_nutrition.get("calories", 0)
                total_protein += scaled_nutrition.get("protein_g", 0)
                total_carbs += scaled_nutrition.get("carbs_g", 0)
                total_fat += scaled_nutrition.get("fat_g", 0)
                total_fiber += scaled_nutrition.get("fiber_g", 0)
                total_sugar += scaled_nutrition.get("sugar_g", 0)
                total_sodium += scaled_nutrition.get("sodium_mg", 0)

            # Step 3: Create meal log in database
            meal_data = {
                "user_id": user_id,
                "name": name,
                "category": category,
                "logged_at": logged_at,
                "notes": notes,
                "foods": foods_with_nutrition,
                "source": "manual",
                "total_calories": round(total_calories, 1),
                "total_protein_g": round(total_protein, 1),
                "total_carbs_g": round(total_carbs, 1),
                "total_fat_g": round(total_fat, 1),
                "total_fiber_g": round(total_fiber, 1),
                "total_sugar_g": round(total_sugar, 1),
                "total_sodium_mg": round(total_sodium, 1),
                "estimated": False,
                "ai_extracted": False,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }

            response = self.supabase.table("meal_logs").insert(meal_data).execute()
            created_meal = response.data[0]

            logger.info(f"✅ Created meal: {created_meal['id']}")

            # Step 4: Track food popularity
            for food_id in food_ids:
                try:
                    await self.food_search.increment_food_popularity(food_id, user_id)
                except:
                    pass  # Non-critical

            return created_meal

        except Exception as e:
            logger.error(f"Create meal failed: {e}", exc_info=True)
            raise

    async def update_meal(
        self,
        meal_id: str,
        user_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update existing meal.

        Args:
            meal_id: Meal ID
            user_id: User ID
            updates: Fields to update (name, category, notes, foods, etc.)

        Returns:
            Updated meal
        """
        try:
            logger.info(f"Updating meal: meal_id={meal_id}, user_id={user_id}")

            # If foods are being updated, recalculate nutrition
            if "foods" in updates:
                food_items = updates["foods"]

                # Fetch food data
                food_ids = [item["food_id"] for item in food_items]
                foods_data = await self._fetch_foods(food_ids)

                # Calculate nutrition for each food
                foods_with_nutrition = []
                total_calories = 0.0
                total_protein = 0.0
                total_carbs = 0.0
                total_fat = 0.0
                total_fiber = 0.0
                total_sugar = 0.0
                total_sodium = 0.0

                for idx, item in enumerate(food_items):
                    food_id = item["food_id"]
                    quantity = item["quantity"]
                    unit = item["unit"]

                    food_data = foods_data.get(food_id)
                    if not food_data:
                        continue

                    scaled_nutrition = self._scale_nutrition(
                        food_data=food_data,
                        quantity=quantity,
                        unit=unit
                    )

                    food_item = {
                        "food_id": food_id,
                        "name": food_data["name"],
                        "brand": food_data.get("brand_name"),
                        "quantity": quantity,
                        "unit": unit,
                        "serving_size": food_data["serving_size"],
                        "serving_unit": food_data["serving_unit"],
                        **scaled_nutrition,
                        "order": idx + 1
                    }

                    foods_with_nutrition.append(food_item)

                    total_calories += scaled_nutrition.get("calories", 0)
                    total_protein += scaled_nutrition.get("protein_g", 0)
                    total_carbs += scaled_nutrition.get("carbs_g", 0)
                    total_fat += scaled_nutrition.get("fat_g", 0)
                    total_fiber += scaled_nutrition.get("fiber_g", 0)
                    total_sugar += scaled_nutrition.get("sugar_g", 0)
                    total_sodium += scaled_nutrition.get("sodium_mg", 0)

                # Update foods and totals
                updates["foods"] = foods_with_nutrition
                updates["total_calories"] = round(total_calories, 1)
                updates["total_protein_g"] = round(total_protein, 1)
                updates["total_carbs_g"] = round(total_carbs, 1)
                updates["total_fat_g"] = round(total_fat, 1)
                updates["total_fiber_g"] = round(total_fiber, 1)
                updates["total_sugar_g"] = round(total_sugar, 1)
                updates["total_sodium_mg"] = round(total_sodium, 1)

            # Add updated_at
            updates["updated_at"] = datetime.utcnow().isoformat()

            # Update in database
            response = self.supabase.table("meal_logs") \
                .update(updates) \
                .eq("id", meal_id) \
                .eq("user_id", user_id) \
                .execute()

            if not response.data:
                raise ValueError(f"Meal not found or unauthorized: {meal_id}")

            updated_meal = response.data[0]
            logger.info(f"✅ Updated meal: {meal_id}")

            return updated_meal

        except Exception as e:
            logger.error(f"Update meal failed: {e}", exc_info=True)
            raise

    async def delete_meal(
        self,
        meal_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Delete meal.

        Args:
            meal_id: Meal ID
            user_id: User ID

        Returns:
            Success status
        """
        try:
            logger.info(f"Deleting meal: meal_id={meal_id}, user_id={user_id}")

            # Delete from database
            response = self.supabase.table("meal_logs") \
                .delete() \
                .eq("id", meal_id) \
                .eq("user_id", user_id) \
                .execute()

            if not response.data:
                raise ValueError(f"Meal not found or unauthorized: {meal_id}")

            logger.info(f"✅ Deleted meal: {meal_id}")

            return {"success": True, "meal_id": meal_id}

        except Exception as e:
            logger.error(f"Delete meal failed: {e}", exc_info=True)
            raise

    async def get_user_meals(
        self,
        user_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get user's meal logs with filtering.

        Args:
            user_id: User ID
            start_date: Optional start date filter (ISO format)
            end_date: Optional end date filter (ISO format)
            category: Optional meal type filter
            limit: Max results
            offset: Pagination offset

        Returns:
            List of meals with pagination info
        """
        try:
            logger.info(f"Getting meals: user_id={user_id}, limit={limit}, offset={offset}")

            # Build query
            query = self.supabase.table("meal_logs") \
                .select("*", count="exact") \
                .eq("user_id", user_id)

            # Apply filters
            if start_date:
                query = query.gte("logged_at", start_date)
            if end_date:
                query = query.lte("logged_at", end_date)
            if category:
                query = query.eq("category", category)

            # Order and paginate
            query = query.order("logged_at", desc=True) \
                .range(offset, offset + limit - 1)

            response = query.execute()

            meals = response.data if response.data else []
            total = response.count if response.count else 0

            logger.info(f"Found {len(meals)} meals (total: {total})")

            return {
                "meals": meals,
                "total": total,
                "limit": limit,
                "offset": offset
            }

        except Exception as e:
            logger.error(f"Get user meals failed: {e}", exc_info=True)
            raise

    async def get_meal_by_id(
        self,
        meal_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get single meal by ID.

        Args:
            meal_id: Meal ID
            user_id: User ID

        Returns:
            Meal data
        """
        try:
            logger.info(f"Getting meal: meal_id={meal_id}, user_id={user_id}")

            response = self.supabase.table("meal_logs") \
                .select("*") \
                .eq("id", meal_id) \
                .eq("user_id", user_id) \
                .limit(1) \
                .execute()

            if not response.data:
                raise ValueError(f"Meal not found or unauthorized: {meal_id}")

            meal = response.data[0]
            logger.info(f"Found meal: {meal_id}")

            return meal

        except Exception as e:
            logger.error(f"Get meal by ID failed: {e}", exc_info=True)
            raise

    async def _fetch_foods(
        self,
        food_ids: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Fetch multiple foods by ID.

        Returns:
            Dict mapping food_id to food data
        """
        if not food_ids:
            return {}

        try:
            response = self.supabase.table("foods_enhanced") \
                .select("id, name, brand_name, serving_size, serving_unit, calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, total_sugars_g, sodium_mg") \
                .in_("id", food_ids) \
                .execute()

            foods_dict = {food["id"]: food for food in response.data}
            return foods_dict

        except Exception as e:
            logger.error(f"Fetch foods failed: {e}", exc_info=True)
            return {}

    def _scale_nutrition(
        self,
        food_data: Dict[str, Any],
        quantity: float,
        unit: str
    ) -> Dict[str, float]:
        """
        Scale nutrition based on quantity and unit.

        Args:
            food_data: Food from database
            quantity: Quantity value
            unit: Unit (g, oz, cup, etc.)

        Returns:
            Scaled nutrition dict
        """
        # Get base serving info
        base_serving_size = food_data["serving_size"]  # e.g., 100
        base_serving_unit = food_data["serving_unit"]  # e.g., "g"

        # Calculate scale factor
        if unit == "serving":
            # "serving" means use the food's serving size directly
            scale = quantity
        else:
            # Convert user's unit to base unit
            user_grams = self._convert_to_grams(quantity, unit)
            base_grams = self._convert_to_grams(base_serving_size, base_serving_unit)

            if user_grams is None or base_grams is None or base_grams == 0:
                # Fallback: assume 1:1 scale
                scale = quantity
            else:
                scale = user_grams / base_grams

        # Scale all nutrition values
        return {
            "calories": (food_data.get("calories") or 0) * scale,
            "protein_g": (food_data.get("protein_g") or 0) * scale,
            "carbs_g": (food_data.get("total_carbs_g") or 0) * scale,
            "fat_g": (food_data.get("total_fat_g") or 0) * scale,
            "fiber_g": (food_data.get("dietary_fiber_g") or 0) * scale,
            "sugar_g": (food_data.get("total_sugars_g") or 0) * scale,
            "sodium_mg": (food_data.get("sodium_mg") or 0) * scale
        }

    def _convert_to_grams(
        self,
        quantity: float,
        unit: str
    ) -> Optional[float]:
        """
        Convert quantity in any unit to grams.

        Returns:
            Grams or None if conversion not possible
        """
        if unit == "serving":
            return None  # Handled specially

        conversion = UNIT_CONVERSIONS.get(unit)
        if conversion is None:
            return None

        return quantity * conversion


# Global instance
_service: Optional[MealLoggingService] = None


def get_meal_logging_service() -> MealLoggingService:
    """Get the global MealLoggingService instance."""
    global _service
    if _service is None:
        _service = MealLoggingService()
    return _service
