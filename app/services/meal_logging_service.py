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
        Create new meal log with foods using relational meal_foods table.

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

            # Step 2: Create meal log WITHOUT foods (will be in meal_foods table)
            meal_data = {
                "user_id": user_id,
                "name": name,
                "category": category,
                "logged_at": logged_at,
                "notes": notes,
                "source": "manual",
                "estimated": False,
                "ai_extracted": False,
                # Totals will be auto-calculated by triggers
                "total_calories": 0,
                "total_protein_g": 0,
                "total_carbs_g": 0,
                "total_fat_g": 0,
                "total_fiber_g": 0,
                "total_sugar_g": 0,
                "total_sodium_mg": 0,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }

            response = self.supabase.table("meals").insert(meal_data).execute()
            created_meal = response.data[0]
            meal_id = created_meal["id"]

            logger.info(f"✅ Created meal_log: {meal_id}")

            # Step 3: Insert foods into meal_foods table
            meal_foods_records = []

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

                # Build meal_foods record
                meal_food_record = {
                    "meal_id": meal_id,
                    "food_id": food_id,
                    "serving_quantity": 1,
                    "serving_unit": unit,
                    "gram_quantity": quantity if unit == "g" else quantity,
                    "last_edited_field": "grams",
                    "display_order": idx,
                    "calories": round(scaled_nutrition.get("calories", 0), 1),
                    "protein_g": round(scaled_nutrition.get("protein_g", 0), 1),
                    "carbs_g": round(scaled_nutrition.get("carbs_g", 0), 1),
                    "fat_g": round(scaled_nutrition.get("fat_g", 0), 1),
                    "fiber_g": round(scaled_nutrition.get("fiber_g", 0), 1),
                    "sugar_g": round(scaled_nutrition.get("sugar_g", 0), 1),
                    "sodium_mg": round(scaled_nutrition.get("sodium_mg", 0), 1),
                }

                meal_foods_records.append(meal_food_record)

            # Batch insert meal_foods
            if meal_foods_records:
                self.supabase.table("meal_foods").insert(meal_foods_records).execute()
                logger.info(f"✅ Inserted {len(meal_foods_records)} meal_foods records")

            # Step 4: Track food popularity
            for food_id in food_ids:
                try:
                    await self.food_search.increment_food_popularity(food_id, user_id)
                except:
                    pass  # Non-critical

            # Step 5: Fetch complete meal with foods joined
            return await self.get_meal_by_id(meal_id, user_id)

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
        Update existing meal using relational meal_foods table.

        Args:
            meal_id: Meal ID
            user_id: User ID
            updates: Fields to update (name, category, notes, foods, etc.)

        Returns:
            Updated meal
        """
        try:
            logger.info(f"Updating meal: meal_id={meal_id}, user_id={user_id}")

            # Extract foods if being updated
            food_items = updates.pop("foods", None)

            # If foods are being updated, replace meal_foods records
            if food_items is not None:
                logger.info(f"Updating foods for meal {meal_id}")

                # Delete existing meal_foods (triggers will auto-update totals to 0)
                self.supabase.table("meal_foods") \
                    .delete() \
                    .eq("meal_id", meal_id) \
                    .execute()

                # Fetch food data
                food_ids = [item["food_id"] for item in food_items]
                foods_data = await self._fetch_foods(food_ids)

                # Insert new meal_foods records
                meal_foods_records = []

                for idx, item in enumerate(food_items):
                    food_id = item["food_id"]
                    quantity = item["quantity"]
                    unit = item["unit"]

                    food_data = foods_data.get(food_id)
                    if not food_data:
                        logger.warning(f"Food not found: {food_id}")
                        continue

                    scaled_nutrition = self._scale_nutrition(
                        food_data=food_data,
                        quantity=quantity,
                        unit=unit
                    )

                    meal_food_record = {
                        "meal_id": meal_id,
                        "food_id": food_id,
                        "serving_quantity": 1,
                        "serving_unit": unit,
                        "gram_quantity": quantity if unit == "g" else quantity,
                        "last_edited_field": "grams",
                        "display_order": idx,
                        "calories": round(scaled_nutrition.get("calories", 0), 1),
                        "protein_g": round(scaled_nutrition.get("protein_g", 0), 1),
                        "carbs_g": round(scaled_nutrition.get("carbs_g", 0), 1),
                        "fat_g": round(scaled_nutrition.get("fat_g", 0), 1),
                        "fiber_g": round(scaled_nutrition.get("fiber_g", 0), 1),
                        "sugar_g": round(scaled_nutrition.get("sugar_g", 0), 1),
                        "sodium_mg": round(scaled_nutrition.get("sodium_mg", 0), 1),
                    }

                    meal_foods_records.append(meal_food_record)

                # Insert new foods (triggers will auto-update totals)
                if meal_foods_records:
                    self.supabase.table("meal_foods").insert(meal_foods_records).execute()
                    logger.info(f"✅ Updated {len(meal_foods_records)} meal_foods records")

            # Update meal_logs if there are other field updates
            if updates:
                updates["updated_at"] = datetime.utcnow().isoformat()

                response = self.supabase.table("meals") \
                    .update(updates) \
                    .eq("id", meal_id) \
                    .eq("user_id", user_id) \
                    .execute()

                if not response.data:
                    raise ValueError(f"Meal not found or unauthorized: {meal_id}")

            # Fetch complete updated meal with foods
            updated_meal = await self.get_meal_by_id(meal_id, user_id)

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
            response = self.supabase.table("meals") \
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
        Get user's meal logs with filtering and foods from meal_foods table.

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
            query = self.supabase.table("meals") \
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

            # For each meal, fetch foods from meal_foods table
            for meal in meals:
                meal_id = meal["id"]

                # Get meal_foods with food details joined
                meal_foods_response = self.supabase.table("meal_foods") \
                    .select("*, foods(id, name, brand_name, serving_size, serving_unit)") \
                    .eq("meal_id", meal_id) \
                    .order("added_at") \
                    .execute()

                # Build foods array
                foods = []
                for idx, mf in enumerate(meal_foods_response.data, 1):
                    food_info = mf.get("foods", {})

                    food_item = {
                        "food_id": mf["food_id"],
                        "name": food_info.get("name", "Unknown Food"),
                        "brand": food_info.get("brand_name"),
                        "quantity": mf["quantity"],
                        "unit": mf["unit"],
                        "serving_size": food_info.get("serving_size", 1),
                        "serving_unit": food_info.get("serving_unit", "serving"),
                        "calories": mf["calories"],
                        "protein_g": mf["protein_g"],
                        "carbs_g": mf["carbs_g"],
                        "fat_g": mf["fat_g"],
                        "fiber_g": mf["fiber_g"],
                        "sugar_g": mf.get("sugar_g"),
                        "sodium_mg": mf.get("sodium_mg"),
                        "order": idx
                    }
                    foods.append(food_item)

                # Add foods to meal
                meal["foods"] = foods

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
        Get single meal by ID with foods from meal_foods table.

        Args:
            meal_id: Meal ID
            user_id: User ID

        Returns:
            Meal data with foods array
        """
        try:
            logger.info(f"Getting meal: meal_id={meal_id}, user_id={user_id}")

            # Get meal log
            response = self.supabase.table("meals") \
                .select("*") \
                .eq("id", meal_id) \
                .eq("user_id", user_id) \
                .limit(1) \
                .execute()

            if not response.data:
                raise ValueError(f"Meal not found or unauthorized: {meal_id}")

            meal = response.data[0]

            # Get meal_foods with food details joined
            meal_foods_response = self.supabase.table("meal_foods") \
                .select("*, foods(id, name, brand_name, serving_size, serving_unit)") \
                .eq("meal_id", meal_id) \
                .order("added_at") \
                .execute()

            # Build foods array for API response (matching FoodItem schema)
            foods = []
            for idx, mf in enumerate(meal_foods_response.data, 1):
                food_info = mf.get("foods", {})

                food_item = {
                    "food_id": mf["food_id"],
                    "name": food_info.get("name", "Unknown Food"),
                    "brand": food_info.get("brand_name"),
                    "quantity": mf["quantity"],
                    "unit": mf["unit"],
                    "serving_size": food_info.get("serving_size", 1),
                    "serving_unit": food_info.get("serving_unit", "serving"),
                    "calories": mf["calories"],
                    "protein_g": mf["protein_g"],
                    "carbs_g": mf["carbs_g"],
                    "fat_g": mf["fat_g"],
                    "fiber_g": mf["fiber_g"],
                    "sugar_g": mf.get("sugar_g"),
                    "sodium_mg": mf.get("sodium_mg"),
                    "order": idx
                }
                foods.append(food_item)

            # Add foods to meal
            meal["foods"] = foods

            logger.info(f"Found meal: {meal_id} with {len(foods)} foods")

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
            response = self.supabase.table("foods") \
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
