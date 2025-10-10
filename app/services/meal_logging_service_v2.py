"""
Meal Logging Service V2 - Uses relational meal_foods table

Handles manual meal logging with:
- Creating meals with relational meal_foods
- Automatic nutrition calculation via database triggers
- Unit conversions
- Meal CRUD operations
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.services.supabase_service import get_service_client
from app.services.food_search_service import get_food_search_service
from app.services.quantity_converter import FoodQuantityConverter
from decimal import Decimal

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


class MealLoggingServiceV2:
    """Service for manual meal logging operations using relational schema."""

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
        Create new meal log with foods using relational schema.

        Args:
            user_id: User ID
            name: Meal name (optional)
            category: Meal type (breakfast, lunch, dinner, snack)
            logged_at: ISO timestamp
            notes: Optional notes
            food_items: List of {food_id, quantity, unit}

        Returns:
            Created meal with full nutrition data and foods
        """
        try:
            logger.info(f"Creating meal (V2): user_id={user_id}, category={category}, foods={len(food_items)}")

            # Step 1: Fetch food data for all items
            food_ids = [item["food_id"] for item in food_items]
            foods_data = await self._fetch_foods(food_ids)

            # Step 2: Create meal_log (without totals - triggers will calculate)
            meal_data = {
                "user_id": user_id,
                "name": name,
                "category": category,
                "logged_at": logged_at,
                "notes": notes,
                "source": "manual",
                "estimated": False,
                "ai_extracted": False,
                # Totals start at 0 - will be updated by trigger
                "total_calories": 0,
                "total_protein_g": 0,
                "total_carbs_g": 0,
                "total_fat_g": 0,
                "total_fiber_g": 0,
                "total_sugar_g": 0,
                "total_sodium_mg": 0
            }

            response = self.supabase.table("meal_logs").insert(meal_data).execute()
            meal = response.data[0]
            meal_id = meal["id"]

            logger.info(f"✅ Created meal_log: {meal_id}")

            # Step 3: Insert into meal_foods table
            meal_foods_to_insert = []

            for idx, item in enumerate(food_items):
                food_id = item["food_id"]
                input_quantity = item["quantity"]
                input_field = item.get("input_field", "grams")  # Default to grams for backward compatibility

                # Get food data
                food_data = foods_data.get(food_id)
                if not food_data:
                    logger.warning(f"Food not found: {food_id}, skipping")
                    continue

                # NEW: Calculate dual quantities using converter
                try:
                    quantities = FoodQuantityConverter.calculate_quantities(
                        food_data=food_data,
                        input_quantity=Decimal(str(input_quantity)),
                        input_field=input_field
                    )
                    
                    # Calculate nutrition from gram quantity
                    nutrition = FoodQuantityConverter.calculate_nutrition(
                        food_data=food_data,
                        gram_quantity=Decimal(str(quantities['gram_quantity']))
                    )
                    
                except Exception as calc_error:
                    logger.error(
                        f"Failed to calculate quantities for food {food_id}: {calc_error}. "
                        f"Using fallback."
                    )
                    # Fallback to old method
                    scaled_nutrition = self._scale_nutrition(
                        food_data=food_data,
                        quantity=input_quantity,
                        unit=item.get("unit", "g")
                    )
                    # Create fallback quantities
                    quantities = {
                        "serving_quantity": 1.0,
                        "serving_unit": None,
                        "gram_quantity": input_quantity,
                        "last_edited_field": "grams"
                    }
                    nutrition = scaled_nutrition

                # Build meal_food entry with DUAL QUANTITY TRACKING
                meal_food = {
                    "meal_log_id": meal_id,
                    "food_id": food_id,
                    "order_index": idx,  # Maintain order
                    
                    # OLD: Keep for backward compatibility (will remove after migration)
                    "quantity": quantities['gram_quantity'],
                    "unit": "g",
                    
                    # NEW: Dual quantity tracking
                    "serving_quantity": quantities['serving_quantity'],
                    "serving_unit": quantities['serving_unit'],
                    "gram_quantity": quantities['gram_quantity'],
                    "last_edited_field": quantities['last_edited_field'],
                    
                    # Nutrition (calculated from gram_quantity)
                    "calories": round(nutrition["calories"], 1),
                    "protein_g": round(nutrition["protein_g"], 1),
                    "carbs_g": round(nutrition["carbs_g"], 1),
                    "fat_g": round(nutrition["fat_g"], 1),
                    "fiber_g": round(nutrition["fiber_g"], 1),
                    "sugar_g": round(nutrition.get("sugar_g", 0), 1),
                    "sodium_mg": round(nutrition.get("sodium_mg", 0), 1)
                }

                meal_foods_to_insert.append(meal_food)

            # Batch insert meal_foods
            if meal_foods_to_insert:
                meal_foods_response = self.supabase.table("meal_foods").insert(meal_foods_to_insert).execute()
                logger.info(f"✅ Inserted {len(meal_foods_to_insert)} foods into meal_foods")

            # Step 4: Re-fetch meal with updated totals (triggers calculated them)
            final_meal = await self.get_meal_by_id(meal_id, user_id)

            # Step 5: Track food popularity
            for food_id in food_ids:
                try:
                    await self.food_search.increment_food_popularity(food_id, user_id)
                except:
                    pass  # Non-critical

            return final_meal

        except Exception as e:
            logger.error(f"Create meal (V2) failed: {e}", exc_info=True)
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
            Updated meal with foods
        """
        try:
            logger.info(f"Updating meal (V2): meal_id={meal_id}, user_id={user_id}")

            # If foods are being updated, replace meal_foods
            if "foods" in updates:
                food_items = updates.pop("foods")  # Remove from updates

                # Delete existing meal_foods
                self.supabase.table("meal_foods").delete().eq("meal_log_id", meal_id).execute()
                logger.info(f"Deleted existing meal_foods for meal {meal_id}")

                # Fetch food data
                food_ids = [item["food_id"] for item in food_items]
                foods_data = await self._fetch_foods(food_ids)

                # Insert new meal_foods
                meal_foods_to_insert = []

                for idx, item in enumerate(food_items):
                    food_id = item["food_id"]
                    input_quantity = item["quantity"]
                    input_field = item.get("input_field", "grams")

                    food_data = foods_data.get(food_id)
                    if not food_data:
                        continue

                    # NEW: Use dual quantity converter
                    try:
                        quantities = FoodQuantityConverter.calculate_quantities(
                            food_data=food_data,
                            input_quantity=Decimal(str(input_quantity)),
                            input_field=input_field
                        )
                        
                        nutrition = FoodQuantityConverter.calculate_nutrition(
                            food_data=food_data,
                            gram_quantity=Decimal(str(quantities['gram_quantity']))
                        )
                    except:
                        # Fallback
                        scaled_nutrition = self._scale_nutrition(
                            food_data=food_data,
                            quantity=input_quantity,
                            unit=item.get("unit", "g")
                        )
                        quantities = {
                            "serving_quantity": 1.0,
                            "serving_unit": None,
                            "gram_quantity": input_quantity,
                            "last_edited_field": "grams"
                        }
                        nutrition = scaled_nutrition

                    meal_food = {
                        "meal_log_id": meal_id,
                        "food_id": food_id,
                        "order_index": idx,
                        
                        # OLD (keep for compatibility)
                        "quantity": quantities['gram_quantity'],
                        "unit": "g",
                        
                        # NEW: Dual quantity
                        "serving_quantity": quantities['serving_quantity'],
                        "serving_unit": quantities['serving_unit'],
                        "gram_quantity": quantities['gram_quantity'],
                        "last_edited_field": quantities['last_edited_field'],
                        
                        # Nutrition
                        "calories": round(nutrition["calories"], 1),
                        "protein_g": round(nutrition["protein_g"], 1),
                        "carbs_g": round(nutrition["carbs_g"], 1),
                        "fat_g": round(nutrition["fat_g"], 1),
                        "fiber_g": round(nutrition["fiber_g"], 1),
                        "sugar_g": round(nutrition.get("sugar_g", 0), 1),
                        "sodium_mg": round(nutrition.get("sodium_mg", 0), 1)
                    }

                    meal_foods_to_insert.append(meal_food)

                if meal_foods_to_insert:
                    self.supabase.table("meal_foods").insert(meal_foods_to_insert).execute()
                    logger.info(f"✅ Inserted {len(meal_foods_to_insert)} new foods")

            # Update meal_log metadata (name, category, notes, etc.)
            if updates:
                updates["updated_at"] = datetime.utcnow().isoformat()

                response = self.supabase.table("meal_logs") \
                    .update(updates) \
                    .eq("id", meal_id) \
                    .eq("user_id", user_id) \
                    .execute()

                if not response.data:
                    raise ValueError(f"Meal not found or unauthorized: {meal_id}")

                logger.info(f"✅ Updated meal_log: {meal_id}")

            # Re-fetch meal with updated data
            updated_meal = await self.get_meal_by_id(meal_id, user_id)

            return updated_meal

        except Exception as e:
            logger.error(f"Update meal (V2) failed: {e}", exc_info=True)
            raise

    async def delete_meal(
        self,
        meal_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Delete meal (CASCADE deletes meal_foods automatically).

        Args:
            meal_id: Meal ID
            user_id: User ID

        Returns:
            Success status
        """
        try:
            logger.info(f"Deleting meal (V2): meal_id={meal_id}, user_id={user_id}")

            # Delete from meal_logs (CASCADE will delete meal_foods)
            response = self.supabase.table("meal_logs") \
                .delete() \
                .eq("id", meal_id) \
                .eq("user_id", user_id) \
                .execute()

            if not response.data:
                raise ValueError(f"Meal not found or unauthorized: {meal_id}")

            logger.info(f"✅ Deleted meal (and meal_foods): {meal_id}")

            return {"success": True, "meal_id": meal_id}

        except Exception as e:
            logger.error(f"Delete meal (V2) failed: {e}", exc_info=True)
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
        Get user's meal logs with filtering (includes meal_foods).

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
            logger.info(f"Getting meals (V2): user_id={user_id}, limit={limit}, offset={offset}")

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

            # Fetch meal_foods for each meal
            for meal in meals:
                meal["foods"] = await self._get_meal_foods(meal["id"])

            logger.info(f"Found {len(meals)} meals (total: {total})")

            return {
                "meals": meals,
                "total": total,
                "limit": limit,
                "offset": offset
            }

        except Exception as e:
            logger.error(f"Get user meals (V2) failed: {e}", exc_info=True)
            raise

    async def get_meal_by_id(
        self,
        meal_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get single meal by ID with meal_foods.

        Args:
            meal_id: Meal ID
            user_id: User ID

        Returns:
            Meal data with foods array
        """
        try:
            logger.info(f"Getting meal (V2): meal_id={meal_id}, user_id={user_id}")

            # Get meal_log
            response = self.supabase.table("meal_logs") \
                .select("*") \
                .eq("id", meal_id) \
                .eq("user_id", user_id) \
                .limit(1) \
                .execute()

            if not response.data:
                raise ValueError(f"Meal not found or unauthorized: {meal_id}")

            meal = response.data[0]

            # Get meal_foods
            meal["foods"] = await self._get_meal_foods(meal_id)

            logger.info(f"Found meal: {meal_id} with {len(meal['foods'])} foods")

            return meal

        except Exception as e:
            logger.error(f"Get meal by ID (V2) failed: {e}", exc_info=True)
            raise

    async def _get_meal_foods(
        self,
        meal_id: str
    ) -> List[Dict[str, Any]]:
        """
        Fetch meal_foods with food details for a meal.

        Returns:
            List of food items with full details
        """
        try:
            # Query meal_foods joined with foods_enhanced
            query = """
                SELECT
                    mf.id,
                    mf.food_id,
                    f.name,
                    f.brand_name,
                    mf.quantity,
                    mf.unit,
                    f.serving_size,
                    f.serving_unit,
                    mf.calories,
                    mf.protein_g,
                    mf.carbs_g,
                    mf.fat_g,
                    mf.fiber_g,
                    mf.sugar_g,
                    mf.sodium_mg,
                    mf.notes
                FROM meal_foods mf
                JOIN foods_enhanced f ON mf.food_id = f.id
                WHERE mf.meal_log_id = %s
                ORDER BY mf.created_at
            """

            # Note: Supabase Python client doesn't support raw SQL well
            # Use table query with select
            response = self.supabase.table("meal_foods") \
                .select("*, foods_enhanced(name, brand_name, serving_size, serving_unit)") \
                .eq("meal_log_id", meal_id) \
                .order("created_at") \
                .execute()

            # Transform response to flat structure
            foods = []
            for item in response.data:
                food_enhanced = item.pop("foods_enhanced", {})

                food = {
                    "id": item["id"],
                    "food_id": item["food_id"],
                    "name": food_enhanced.get("name"),
                    "brand_name": food_enhanced.get("brand_name"),
                    "quantity": item["quantity"],
                    "unit": item["unit"],
                    "serving_size": food_enhanced.get("serving_size"),
                    "serving_unit": food_enhanced.get("serving_unit"),
                    "calories": item["calories"],
                    "protein_g": item["protein_g"],
                    "carbs_g": item["carbs_g"],
                    "fat_g": item["fat_g"],
                    "fiber_g": item["fiber_g"],
                    "sugar_g": item.get("sugar_g", 0),
                    "sodium_mg": item.get("sodium_mg", 0),
                    "notes": item.get("notes")
                }

                foods.append(food)

            return foods

        except Exception as e:
            logger.error(f"Get meal foods failed: {e}", exc_info=True)
            return []

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
            # NEW: Include household serving fields for converter
            response = self.supabase.table("foods_enhanced") \
                .select("id, name, brand_name, serving_size, serving_unit, household_serving_size, household_serving_unit, calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, total_sugars_g, sodium_mg") \
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
        # Get base serving info with safe defaults
        base_serving_size = food_data.get("serving_size")
        base_serving_unit = food_data.get("serving_unit")
        
        # Handle missing serving information
        if base_serving_size is None or base_serving_unit is None:
            logger.warning(
                f"Missing serving info for food {food_data.get('name', 'unknown')} "
                f"(id: {food_data.get('id', 'unknown')}). Using default 100g."
            )
            base_serving_size = 100
            base_serving_unit = "g"

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
_service_v2: Optional[MealLoggingServiceV2] = None


def get_meal_logging_service_v2() -> MealLoggingServiceV2:
    """Get the global MealLoggingServiceV2 instance."""
    global _service_v2
    if _service_v2 is None:
        _service_v2 = MealLoggingServiceV2()
    return _service_v2
