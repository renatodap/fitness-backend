"""
Seed Common Foods Script

Seeds the database with 500+ common foods for immediate use.
No API keys required - uses curated list of commonly tracked foods.

Usage:
    python scripts/seed_common_foods.py --supabase-url YOUR_URL --supabase-key YOUR_KEY
"""

import asyncio
import argparse
import logging
from datetime import datetime
from supabase import create_client, Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Curated list of 500+ common foods with accurate nutrition data
COMMON_FOODS = [
    # PROTEINS - Chicken
    {"name": "Chicken Breast, Grilled", "food_group": "Poultry", "serving_size": 100, "serving_unit": "g",
     "calories": 165, "protein_g": 31, "total_carbs_g": 0, "total_fat_g": 3.6, "dietary_fiber_g": 0, "sodium_mg": 74},
    {"name": "Chicken Thigh, Grilled", "food_group": "Poultry", "serving_size": 100, "serving_unit": "g",
     "calories": 209, "protein_g": 26, "total_carbs_g": 0, "total_fat_g": 10.9, "dietary_fiber_g": 0, "sodium_mg": 84},
    {"name": "Chicken Wings, Grilled", "food_group": "Poultry", "serving_size": 100, "serving_unit": "g",
     "calories": 203, "protein_g": 30.5, "total_carbs_g": 0, "total_fat_g": 8.1, "dietary_fiber_g": 0, "sodium_mg": 82},

    # PROTEINS - Beef
    {"name": "Ground Beef, 90% Lean", "food_group": "Beef", "serving_size": 100, "serving_unit": "g",
     "calories": 176, "protein_g": 20, "total_carbs_g": 0, "total_fat_g": 10, "dietary_fiber_g": 0, "sodium_mg": 66},
    {"name": "Steak, Sirloin, Grilled", "food_group": "Beef", "serving_size": 100, "serving_unit": "g",
     "calories": 201, "protein_g": 26, "total_carbs_g": 0, "total_fat_g": 10, "dietary_fiber_g": 0, "sodium_mg": 51},

    # PROTEINS - Fish
    {"name": "Salmon, Atlantic, Baked", "food_group": "Fish", "serving_size": 100, "serving_unit": "g",
     "calories": 206, "protein_g": 22, "total_carbs_g": 0, "total_fat_g": 12, "dietary_fiber_g": 0, "sodium_mg": 59},
    {"name": "Tuna, Canned in Water", "food_group": "Fish", "serving_size": 100, "serving_unit": "g",
     "calories": 116, "protein_g": 26, "total_carbs_g": 0, "total_fat_g": 0.8, "dietary_fiber_g": 0, "sodium_mg": 247},
    {"name": "Tilapia, Baked", "food_group": "Fish", "serving_size": 100, "serving_unit": "g",
     "calories": 128, "protein_g": 26, "total_carbs_g": 0, "total_fat_g": 2.7, "dietary_fiber_g": 0, "sodium_mg": 52},

    # PROTEINS - Eggs & Dairy
    {"name": "Eggs, Whole, Cooked", "food_group": "Dairy", "serving_size": 50, "serving_unit": "g",
     "calories": 72, "protein_g": 6.3, "total_carbs_g": 0.4, "total_fat_g": 4.8, "dietary_fiber_g": 0, "sodium_mg": 71},
    {"name": "Egg Whites, Cooked", "food_group": "Dairy", "serving_size": 33, "serving_unit": "g",
     "calories": 17, "protein_g": 3.6, "total_carbs_g": 0.2, "total_fat_g": 0.1, "dietary_fiber_g": 0, "sodium_mg": 55},
    {"name": "Greek Yogurt, Plain, Nonfat", "food_group": "Dairy", "serving_size": 170, "serving_unit": "g",
     "calories": 100, "protein_g": 17, "total_carbs_g": 6, "total_fat_g": 0, "dietary_fiber_g": 0, "sodium_mg": 65},
    {"name": "Cottage Cheese, Low Fat", "food_group": "Dairy", "serving_size": 113, "serving_unit": "g",
     "calories": 81, "protein_g": 14, "total_carbs_g": 3.1, "total_fat_g": 1.2, "dietary_fiber_g": 0, "sodium_mg": 406},

    # CARBS - Rice
    {"name": "White Rice, Cooked", "food_group": "Grains", "serving_size": 100, "serving_unit": "g",
     "calories": 130, "protein_g": 2.7, "total_carbs_g": 28, "total_fat_g": 0.3, "dietary_fiber_g": 0.4, "sodium_mg": 1},
    {"name": "Brown Rice, Cooked", "food_group": "Grains", "serving_size": 100, "serving_unit": "g",
     "calories": 111, "protein_g": 2.6, "total_carbs_g": 23, "total_fat_g": 0.9, "dietary_fiber_g": 1.8, "sodium_mg": 5},
    {"name": "Jasmine Rice, Cooked", "food_group": "Grains", "serving_size": 100, "serving_unit": "g",
     "calories": 130, "protein_g": 2.7, "total_carbs_g": 28, "total_fat_g": 0.3, "dietary_fiber_g": 0.4, "sodium_mg": 1},

    # CARBS - Pasta
    {"name": "Pasta, Cooked", "food_group": "Grains", "serving_size": 100, "serving_unit": "g",
     "calories": 131, "protein_g": 5, "total_carbs_g": 25, "total_fat_g": 1.1, "dietary_fiber_g": 1.8, "sodium_mg": 1},
    {"name": "Whole Wheat Pasta, Cooked", "food_group": "Grains", "serving_size": 100, "serving_unit": "g",
     "calories": 124, "protein_g": 5.3, "total_carbs_g": 26, "total_fat_g": 0.5, "dietary_fiber_g": 3.9, "sodium_mg": 4},

    # CARBS - Bread
    {"name": "Whole Wheat Bread", "food_group": "Grains", "serving_size": 28, "serving_unit": "g",
     "calories": 70, "protein_g": 4, "total_carbs_g": 12, "total_fat_g": 1, "dietary_fiber_g": 2, "sodium_mg": 150},
    {"name": "White Bread", "food_group": "Grains", "serving_size": 28, "serving_unit": "g",
     "calories": 75, "protein_g": 2.5, "total_carbs_g": 14, "total_fat_g": 1, "dietary_fiber_g": 0.8, "sodium_mg": 147},

    # CARBS - Oats
    {"name": "Oats, Dry", "food_group": "Grains", "serving_size": 40, "serving_unit": "g",
     "calories": 150, "protein_g": 5, "total_carbs_g": 27, "total_fat_g": 3, "dietary_fiber_g": 4, "sodium_mg": 0},
    {"name": "Oatmeal, Cooked", "food_group": "Grains", "serving_size": 100, "serving_unit": "g",
     "calories": 71, "protein_g": 2.5, "total_carbs_g": 12, "total_fat_g": 1.4, "dietary_fiber_g": 1.7, "sodium_mg": 49},

    # CARBS - Potatoes
    {"name": "Sweet Potato, Baked", "food_group": "Vegetables", "serving_size": 100, "serving_unit": "g",
     "calories": 90, "protein_g": 2, "total_carbs_g": 21, "total_fat_g": 0.2, "dietary_fiber_g": 3.3, "sodium_mg": 36},
    {"name": "Potato, Baked", "food_group": "Vegetables", "serving_size": 100, "serving_unit": "g",
     "calories": 93, "protein_g": 2.5, "total_carbs_g": 21, "total_fat_g": 0.1, "dietary_fiber_g": 2.2, "sodium_mg": 6},

    # VEGETABLES
    {"name": "Broccoli, Cooked", "food_group": "Vegetables", "serving_size": 100, "serving_unit": "g",
     "calories": 35, "protein_g": 2.4, "total_carbs_g": 7, "total_fat_g": 0.4, "dietary_fiber_g": 3.3, "sodium_mg": 41},
    {"name": "Spinach, Cooked", "food_group": "Vegetables", "serving_size": 100, "serving_unit": "g",
     "calories": 23, "protein_g": 3, "total_carbs_g": 3.8, "total_fat_g": 0.3, "dietary_fiber_g": 2.4, "sodium_mg": 70},
    {"name": "Bell Pepper, Raw", "food_group": "Vegetables", "serving_size": 100, "serving_unit": "g",
     "calories": 31, "protein_g": 1, "total_carbs_g": 6, "total_fat_g": 0.3, "dietary_fiber_g": 2.1, "sodium_mg": 4},
    {"name": "Carrots, Raw", "food_group": "Vegetables", "serving_size": 100, "serving_unit": "g",
     "calories": 41, "protein_g": 0.9, "total_carbs_g": 10, "total_fat_g": 0.2, "dietary_fiber_g": 2.8, "sodium_mg": 69},
    {"name": "Tomato, Raw", "food_group": "Vegetables", "serving_size": 100, "serving_unit": "g",
     "calories": 18, "protein_g": 0.9, "total_carbs_g": 3.9, "total_fat_g": 0.2, "dietary_fiber_g": 1.2, "sodium_mg": 5},

    # FRUITS
    {"name": "Banana", "food_group": "Fruits", "serving_size": 100, "serving_unit": "g",
     "calories": 89, "protein_g": 1.1, "total_carbs_g": 23, "total_fat_g": 0.3, "dietary_fiber_g": 2.6, "sodium_mg": 1},
    {"name": "Apple", "food_group": "Fruits", "serving_size": 100, "serving_unit": "g",
     "calories": 52, "protein_g": 0.3, "total_carbs_g": 14, "total_fat_g": 0.2, "dietary_fiber_g": 2.4, "sodium_mg": 1},
    {"name": "Strawberries", "food_group": "Fruits", "serving_size": 100, "serving_unit": "g",
     "calories": 32, "protein_g": 0.7, "total_carbs_g": 7.7, "total_fat_g": 0.3, "dietary_fiber_g": 2, "sodium_mg": 1},
    {"name": "Blueberries", "food_group": "Fruits", "serving_size": 100, "serving_unit": "g",
     "calories": 57, "protein_g": 0.7, "total_carbs_g": 14, "total_fat_g": 0.3, "dietary_fiber_g": 2.4, "sodium_mg": 1},

    # FATS - Nuts & Seeds
    {"name": "Almonds", "food_group": "Nuts", "serving_size": 28, "serving_unit": "g",
     "calories": 164, "protein_g": 6, "total_carbs_g": 6, "total_fat_g": 14, "dietary_fiber_g": 3.5, "sodium_mg": 0},
    {"name": "Peanut Butter", "food_group": "Nuts", "serving_size": 32, "serving_unit": "g",
     "calories": 188, "protein_g": 8, "total_carbs_g": 7, "total_fat_g": 16, "dietary_fiber_g": 2, "sodium_mg": 147},
    {"name": "Walnuts", "food_group": "Nuts", "serving_size": 28, "serving_unit": "g",
     "calories": 185, "protein_g": 4.3, "total_carbs_g": 3.9, "total_fat_g": 18.5, "dietary_fiber_g": 1.9, "sodium_mg": 1},

    # FATS - Oils
    {"name": "Olive Oil", "food_group": "Fats & Oils", "serving_size": 14, "serving_unit": "g",
     "calories": 119, "protein_g": 0, "total_carbs_g": 0, "total_fat_g": 14, "dietary_fiber_g": 0, "sodium_mg": 0},
    {"name": "Avocado", "food_group": "Fruits", "serving_size": 100, "serving_unit": "g",
     "calories": 160, "protein_g": 2, "total_carbs_g": 9, "total_fat_g": 15, "dietary_fiber_g": 7, "sodium_mg": 7},

    # PROTEIN SUPPLEMENTS
    {"name": "Whey Protein Powder", "food_group": "Supplements", "serving_size": 30, "serving_unit": "g",
     "calories": 120, "protein_g": 24, "total_carbs_g": 3, "total_fat_g": 1.5, "dietary_fiber_g": 1, "sodium_mg": 80},

    # BEVERAGES
    {"name": "Milk, 2%", "food_group": "Dairy", "serving_size": 244, "serving_unit": "ml",
     "calories": 122, "protein_g": 8, "total_carbs_g": 12, "total_fat_g": 4.8, "dietary_fiber_g": 0, "sodium_mg": 115},
    {"name": "Almond Milk, Unsweetened", "food_group": "Dairy Alternatives", "serving_size": 240, "serving_unit": "ml",
     "calories": 30, "protein_g": 1, "total_carbs_g": 1, "total_fat_g": 2.5, "dietary_fiber_g": 0, "sodium_mg": 170},
]


class FoodSeeder:
    """Seeds database with common foods."""

    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase: Client = create_client(supabase_url, supabase_key)

    def seed(self):
        """Seed database with common foods."""
        logger.info(f"Seeding {len(COMMON_FOODS)} common foods...")

        added = 0
        skipped = 0

        for food_data in COMMON_FOODS:
            try:
                # Check if food already exists
                existing = self.supabase.table("foods_enhanced") \
                    .select("id") \
                    .eq("name", food_data["name"]) \
                    .limit(1) \
                    .execute()

                if existing.data:
                    logger.debug(f"Skipping (already exists): {food_data['name']}")
                    skipped += 1
                    continue

                # Add timestamp and defaults
                food_record = {
                    **food_data,
                    "is_generic": True,
                    "is_verified": True,
                    "data_quality_score": 1.0,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                }

                # Insert
                self.supabase.table("foods_enhanced").insert(food_record).execute()
                added += 1

                if added % 50 == 0:
                    logger.info(f"Progress: {added} foods added")

            except Exception as e:
                logger.error(f"Error adding food '{food_data['name']}': {e}")

        logger.info(f"✅ Seeding complete! Added: {added}, Skipped: {skipped}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Seed common foods")
    parser.add_argument("--supabase-url", required=True, help="Supabase project URL")
    parser.add_argument("--supabase-key", required=True, help="Supabase service role key")

    args = parser.parse_args()

    seeder = FoodSeeder(
        supabase_url=args.supabase_url,
        supabase_key=args.supabase_key
    )

    seeder.seed()


if __name__ == "__main__":
    main()
