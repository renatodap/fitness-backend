#!/usr/bin/env python3
"""
Quick diagnostic script to check foods table content
"""
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Create Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")  # Note: Uses SUPABASE_SERVICE_KEY from .env
)

print("=" * 60)
print("FOODS TABLE DIAGNOSTIC")
print("=" * 60)

# Check total count
try:
    result = supabase.table("foods").select("*", count="exact").limit(1).execute()
    print(f"\n✓ Total foods in database: {result.count}")
except Exception as e:
    print(f"\n✗ Error counting foods: {e}")

# Search for chicken
try:
    print("\n" + "-" * 60)
    print("Searching for 'chicken' (ILIKE %chicken%)")
    print("-" * 60)
    
    foods = supabase.table("foods").select(
        "id, name, brand_name, food_type, calories, serving_size, serving_unit"
    ).or_("name.ilike.%chicken%,brand_name.ilike.%chicken%").limit(10).execute()
    
    print(f"Found {len(foods.data)} results:")
    
    if foods.data:
        for i, food in enumerate(foods.data, 1):
            print(f"\n{i}. {food['name']}")
            if food.get('brand_name'):
                print(f"   Brand: {food['brand_name']}")
            print(f"   Type: {food.get('food_type', 'N/A')}")
            print(f"   Calories: {food.get('calories', 0)} per {food.get('serving_size', 1)} {food.get('serving_unit', 'serving')}")
    else:
        print("No results found!")
        
except Exception as e:
    print(f"✗ Error searching: {e}")

# Check some sample foods
try:
    print("\n" + "-" * 60)
    print("Sample of first 5 foods in database:")
    print("-" * 60)
    
    sample = supabase.table("foods").select("id, name, brand_name, calories").limit(5).execute()
    
    for i, food in enumerate(sample.data, 1):
        print(f"{i}. {food['name']} - {food.get('brand_name', 'No brand')} ({food.get('calories', 0)} cal)")
        
except Exception as e:
    print(f"✗ Error getting sample: {e}")

print("\n" + "=" * 60)
