"""
Test script to verify meal nutritional estimation always works.

This script tests that the Quick Entry system ALWAYS estimates macros,
calories, and micronutrients regardless of input precision.
"""

import asyncio
import json
from app.services.groq_service_v2 import get_groq_service_v2

async def test_meal_estimation():
    """Test various meal inputs to ensure nutrition is always estimated."""

    groq_service = get_groq_service_v2()

    test_cases = [
        # Vague inputs (should still estimate)
        "chicken and rice",
        "had a burger",
        "ate pasta",
        "protein shake",

        # Specific inputs (should estimate accurately)
        "6oz grilled chicken breast with 1 cup brown rice and broccoli",
        "Big Mac from McDonald's",
        "Chipotle burrito bowl with chicken",

        # Restaurant meals (should estimate based on typical servings)
        "Chicken Margherita at Olive Garden",
        "Pad Thai from local Thai restaurant",

        # Mixed precision
        "2 eggs and toast",
        "salmon with veggies"
    ]

    print("=" * 80)
    print("MEAL NUTRITIONAL ESTIMATION TEST")
    print("=" * 80)
    print()

    for i, meal_input in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{meal_input}'")
        print("-" * 60)

        try:
            result = await groq_service.classify_and_extract(
                text=meal_input,
                force_type="meal"
            )

            # Extract nutrition data
            data = result.get("data", {})
            primary = data.get("primary_fields", {})
            secondary = data.get("secondary_fields", {})

            # Check for nutrition values
            calories = primary.get("calories") or secondary.get("calories")
            protein = primary.get("protein_g") or secondary.get("protein_g")
            carbs = primary.get("carbs_g") or secondary.get("carbs_g")
            fat = primary.get("fat_g") or secondary.get("fat_g")

            # Validate
            if calories is None or protein is None or carbs is None or fat is None:
                print("❌ FAILED: Missing nutrition data!")
                print(f"   Calories: {calories}")
                print(f"   Protein: {protein}g")
                print(f"   Carbs: {carbs}g")
                print(f"   Fat: {fat}g")
            else:
                print("✅ PASSED: Nutrition estimated")
                print(f"   Calories: {calories}")
                print(f"   Protein: {protein}g")
                print(f"   Carbs: {carbs}g")
                print(f"   Fat: {fat}g")

                # Check for micronutrients
                fiber = secondary.get("fiber_g")
                sugar = secondary.get("sugar_g")
                sodium = secondary.get("sodium_mg")

                if fiber or sugar or sodium:
                    print(f"   Micronutrients:")
                    if fiber: print(f"      - Fiber: {fiber}g")
                    if sugar: print(f"      - Sugar: {sugar}g")
                    if sodium: print(f"      - Sodium: {sodium}mg")

            # Show confidence and flags
            confidence = result.get("confidence", 0)
            estimated = data.get("estimated", False)
            needs_clarification = data.get("needs_clarification", False)

            print(f"   Confidence: {confidence}")
            print(f"   Estimated: {estimated}")
            print(f"   Needs clarification: {needs_clarification}")

            # Show suggestions
            suggestions = result.get("suggestions", [])
            if suggestions:
                print(f"   Suggestions:")
                for suggestion in suggestions[:2]:  # Show first 2
                    print(f"      - {suggestion}")

        except Exception as e:
            print(f"❌ ERROR: {e}")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_meal_estimation())
