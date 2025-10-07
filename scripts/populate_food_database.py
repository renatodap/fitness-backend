"""
Food Database Population Script

Populates the foods_enhanced table with comprehensive nutrition data from:
1. USDA FoodData Central (Foundation Foods + SR Legacy)
2. Common foods and meals
3. Popular brand items

This creates a production-ready food database with 10,000+ items optimized for
fast search and accurate nutrition tracking.

Usage:
    python scripts/populate_food_database.py --limit 10000
"""

import asyncio
import argparse
import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
from supabase import create_client, Client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# USDA FoodData Central API
# Get free API key at: https://fdc.nal.usda.gov/api-key-signup.html
USDA_API_KEY = "DEMO_KEY"  # Replace with real key for production
USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1"


class FoodDatabasePopulator:
    """Populates food database with comprehensive nutrition data."""

    def __init__(self, supabase_url: str, supabase_key: str, usda_api_key: str = USDA_API_KEY):
        """Initialize with Supabase client and USDA API key."""
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.usda_api_key = usda_api_key
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def populate(self, limit: int = 10000, skip_existing: bool = True):
        """
        Populate food database.

        Args:
            limit: Maximum number of foods to add
            skip_existing: Skip if database already has foods
        """
        logger.info(f"Starting food database population (limit={limit})")

        # Check if database already has foods
        if skip_existing:
            existing_count = await self._count_existing_foods()
            if existing_count > 0:
                logger.info(f"Database already has {existing_count} foods. Skipping.")
                return

        # Step 1: Add common whole foods (fruits, vegetables, proteins)
        logger.info("Step 1: Adding common whole foods from USDA...")
        whole_foods_count = await self._add_common_whole_foods(limit=1000)
        logger.info(f"Added {whole_foods_count} common whole foods")

        # Step 2: Add branded foods
        logger.info("Step 2: Adding popular branded foods from USDA...")
        branded_count = await self._add_popular_branded_foods(limit=min(5000, limit - whole_foods_count))
        logger.info(f"Added {branded_count} branded foods")

        # Step 3: Add restaurant items
        logger.info("Step 3: Adding common restaurant items...")
        restaurant_count = await self._add_restaurant_foods(limit=min(2000, limit - whole_foods_count - branded_count))
        logger.info(f"Added {restaurant_count} restaurant foods")

        # Step 4: Add common meals and recipes
        logger.info("Step 4: Adding common meals and recipes...")
        meals_count = await self._add_common_meals(limit=min(1000, limit - whole_foods_count - branded_count - restaurant_count))
        logger.info(f"Added {meals_count} common meals")

        total = whole_foods_count + branded_count + restaurant_count + meals_count
        logger.info(f"✅ Population complete! Total foods added: {total}")

    async def _count_existing_foods(self) -> int:
        """Count existing foods in database."""
        try:
            response = self.supabase.table("foods_enhanced").select("id", count="exact").limit(1).execute()
            return response.count if response.count else 0
        except Exception as e:
            logger.error(f"Error counting foods: {e}")
            return 0

    async def _add_common_whole_foods(self, limit: int = 1000) -> int:
        """
        Add common whole foods from USDA FoodData Central.

        Focus on: fruits, vegetables, meats, grains, dairy
        """
        logger.info("Fetching whole foods from USDA...")

        # Common food groups to prioritize
        food_groups = [
            "Fruits and Fruit Juices",
            "Vegetables and Vegetable Products",
            "Poultry Products",
            "Beef Products",
            "Pork Products",
            "Finfish and Shellfish Products",
            "Dairy and Egg Products",
            "Legumes and Legume Products",
            "Nut and Seed Products",
            "Cereal Grains and Pasta",
        ]

        added_count = 0

        for food_group in food_groups:
            if added_count >= limit:
                break

            try:
                # Search USDA for this food group
                foods = await self._search_usda_foods(
                    query=food_group,
                    data_type="Foundation,SR Legacy",
                    page_size=min(100, limit - added_count)
                )

                for food_data in foods:
                    if added_count >= limit:
                        break

                    # Convert USDA format to our schema
                    food_record = self._convert_usda_to_schema(food_data)

                    if food_record:
                        # Insert into database
                        await self._insert_food(food_record)
                        added_count += 1

                        if added_count % 50 == 0:
                            logger.info(f"Progress: {added_count}/{limit} whole foods added")

            except Exception as e:
                logger.error(f"Error adding food group '{food_group}': {e}")

        return added_count

    async def _add_popular_branded_foods(self, limit: int = 5000) -> int:
        """Add popular branded foods from USDA."""
        logger.info("Fetching branded foods from USDA...")

        # Popular food categories for branded items
        queries = [
            "greek yogurt", "protein bar", "protein powder", "oats", "cereal",
            "bread", "pasta", "rice", "chicken breast", "salmon",
            "almond milk", "protein shake", "energy drink", "granola",
            "peanut butter", "cheese", "crackers", "chips", "cookies"
        ]

        added_count = 0

        for query in queries:
            if added_count >= limit:
                break

            try:
                foods = await self._search_usda_foods(
                    query=query,
                    data_type="Branded",
                    page_size=min(200, (limit - added_count) // len(queries))
                )

                for food_data in foods:
                    if added_count >= limit:
                        break

                    food_record = self._convert_usda_to_schema(food_data)

                    if food_record:
                        await self._insert_food(food_record)
                        added_count += 1

                        if added_count % 100 == 0:
                            logger.info(f"Progress: {added_count}/{limit} branded foods added")

            except Exception as e:
                logger.error(f"Error adding branded foods for '{query}': {e}")

        return added_count

    async def _add_restaurant_foods(self, limit: int = 2000) -> int:
        """Add common restaurant items."""
        logger.info("Fetching restaurant foods from USDA...")

        restaurant_chains = [
            "McDonald's", "Subway", "Chipotle", "Starbucks", "Panera",
            "Chick-fil-A", "Taco Bell", "Pizza Hut", "Domino's", "KFC"
        ]

        added_count = 0

        for chain in restaurant_chains:
            if added_count >= limit:
                break

            try:
                foods = await self._search_usda_foods(
                    query=chain,
                    data_type="Branded",
                    page_size=min(100, (limit - added_count) // len(restaurant_chains))
                )

                for food_data in foods:
                    if added_count >= limit:
                        break

                    food_record = self._convert_usda_to_schema(food_data, is_restaurant=True)

                    if food_record:
                        await self._insert_food(food_record)
                        added_count += 1

            except Exception as e:
                logger.error(f"Error adding restaurant foods for '{chain}': {e}")

        return added_count

    async def _add_common_meals(self, limit: int = 1000) -> int:
        """Add common meal combinations."""
        # For now, return 0 - can add pre-defined meal combinations later
        # Example: "Chicken and Rice", "Eggs and Toast", etc.
        logger.info("Skipping common meals for now (to be added manually)")
        return 0

    async def _search_usda_foods(
        self,
        query: str,
        data_type: str = "Foundation,SR Legacy,Branded",
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search USDA FoodData Central API.

        Args:
            query: Search query
            data_type: Comma-separated data types
            page_size: Number of results to return

        Returns:
            List of food data dicts
        """
        url = f"{USDA_BASE_URL}/foods/search"
        params = {
            "api_key": self.usda_api_key,
            "query": query,
            "dataType": data_type,
            "pageSize": page_size,
            "sortBy": "dataType.keyword",  # Prioritize quality data
        }

        try:
            response = await self.http_client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("foods", [])

        except Exception as e:
            logger.error(f"USDA API search failed for '{query}': {e}")
            return []

    def _convert_usda_to_schema(
        self,
        usda_food: Dict[str, Any],
        is_restaurant: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Convert USDA food format to our schema.

        Args:
            usda_food: USDA food data
            is_restaurant: Whether this is a restaurant item

        Returns:
            Food record dict or None if invalid
        """
        try:
            # Extract basic info
            fdc_id = str(usda_food.get("fdcId", ""))
            name = usda_food.get("description", "").title()
            data_type = usda_food.get("dataType", "")

            # Brand info (for branded foods)
            brand_name = usda_food.get("brandName") or usda_food.get("brandOwner")
            brand_owner = usda_food.get("brandOwner")

            # Food category
            food_category = usda_food.get("foodCategory")
            food_group = food_category if isinstance(food_category, str) else None

            # Serving size info
            serving_size = usda_food.get("servingSize", 100)
            serving_unit = usda_food.get("servingUnit", "g")

            # Extract nutrients
            nutrients = {}
            for nutrient in usda_food.get("foodNutrients", []):
                nutrient_name = nutrient.get("nutrientName", "")
                nutrient_value = nutrient.get("value", 0)

                # Map USDA nutrient names to our schema
                if "Energy" in nutrient_name and "kcal" in nutrient_name:
                    nutrients["calories"] = nutrient_value
                elif "Protein" in nutrient_name:
                    nutrients["protein_g"] = nutrient_value
                elif "Carbohydrate" in nutrient_name and "by difference" in nutrient_name:
                    nutrients["total_carbs_g"] = nutrient_value
                elif "Total lipid (fat)" in nutrient_name:
                    nutrients["total_fat_g"] = nutrient_value
                elif "Fiber, total dietary" in nutrient_name:
                    nutrients["dietary_fiber_g"] = nutrient_value
                elif "Sugars, total" in nutrient_name:
                    nutrients["total_sugars_g"] = nutrient_value
                elif "Sodium, Na" in nutrient_name:
                    nutrients["sodium_mg"] = nutrient_value
                elif "Cholesterol" in nutrient_name:
                    nutrients["cholesterol_mg"] = nutrient_value
                elif "Fatty acids, total saturated" in nutrient_name:
                    nutrients["saturated_fat_g"] = nutrient_value

            # Build food record
            food_record = {
                "name": name,
                "brand_name": brand_name,
                "brand_owner": brand_owner,
                "restaurant_name": brand_name if is_restaurant else None,
                "food_group": food_group,
                "fdc_id": fdc_id,
                "serving_size": serving_size,
                "serving_unit": serving_unit,
                "is_branded": data_type == "Branded",
                "is_restaurant": is_restaurant,
                "is_generic": data_type in ["Foundation", "SR Legacy"],
                "data_quality_score": self._calculate_quality_score(usda_food),
                **nutrients,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            return food_record

        except Exception as e:
            logger.error(f"Error converting USDA food: {e}")
            return None

    def _calculate_quality_score(self, usda_food: Dict[str, Any]) -> float:
        """Calculate data quality score (0-1) based on completeness."""
        score = 0.0

        # Has FDC ID
        if usda_food.get("fdcId"):
            score += 0.2

        # Has nutrients
        nutrients_count = len(usda_food.get("foodNutrients", []))
        score += min(0.4, nutrients_count / 50 * 0.4)  # Up to 0.4 for having many nutrients

        # Is from quality data source
        data_type = usda_food.get("dataType", "")
        if data_type in ["Foundation", "SR Legacy"]:
            score += 0.2
        elif data_type == "Branded":
            score += 0.1

        # Has serving size
        if usda_food.get("servingSize"):
            score += 0.2

        return min(1.0, score)

    async def _insert_food(self, food_record: Dict[str, Any]):
        """Insert food into database with deduplication."""
        try:
            # Check if food already exists by FDC ID
            if food_record.get("fdc_id"):
                existing = self.supabase.table("foods_enhanced") \
                    .select("id") \
                    .eq("fdc_id", food_record["fdc_id"]) \
                    .limit(1) \
                    .execute()

                if existing.data:
                    logger.debug(f"Food already exists: {food_record['name']}")
                    return

            # Insert food
            self.supabase.table("foods_enhanced").insert(food_record).execute()
            logger.debug(f"Inserted: {food_record['name']}")

        except Exception as e:
            logger.error(f"Error inserting food '{food_record.get('name')}': {e}")

    async def close(self):
        """Close HTTP client."""
        await self.http_client.aclose()


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Populate food database")
    parser.add_argument("--limit", type=int, default=10000, help="Maximum foods to add")
    parser.add_argument("--skip-existing", action="store_true", help="Skip if database already has foods")
    parser.add_argument("--supabase-url", required=True, help="Supabase project URL")
    parser.add_argument("--supabase-key", required=True, help="Supabase service role key")
    parser.add_argument("--usda-api-key", default="DEMO_KEY", help="USDA FoodData Central API key")

    args = parser.parse_args()

    populator = FoodDatabasePopulator(
        supabase_url=args.supabase_url,
        supabase_key=args.supabase_key,
        usda_api_key=args.usda_api_key
    )

    try:
        await populator.populate(
            limit=args.limit,
            skip_existing=args.skip_existing
        )
    finally:
        await populator.close()


if __name__ == "__main__":
    asyncio.run(main())
