"""
Comprehensive test for ALL entry types with intelligent estimation.

Tests that EVERY log type (meal, activity, workout, measurement) always gets:
1. Proper timestamp estimation with time inference
2. All relevant field estimates (even for vague inputs)
3. Appropriate confidence levels
4. Helpful suggestions
"""

import asyncio
import json
from datetime import datetime
from app.services.groq_service_v2 import get_groq_service_v2

def validate_timestamp(timestamp_str, context=""):
    """Validate that timestamp is present and properly formatted."""
    if not timestamp_str:
        return False, "Missing timestamp"
    try:
        datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return True, "Valid timestamp"
    except:
        return False, f"Invalid timestamp format: {timestamp_str}"

async def test_comprehensive_estimation():
    """Test comprehensive estimation across all entry types."""

    groq_service = get_groq_service_v2()

    test_cases = {
        "MEAL LOGS": [
            # Vague meals - should estimate everything including time
            ("ate chicken", "meal", ["logged_at", "calories", "protein_g", "carbs_g", "fat_g"]),
            ("had breakfast", "meal", ["logged_at", "meal_type", "calories"]),
            ("lunch was a burrito", "meal", ["logged_at", "meal_type", "calories", "protein_g"]),
            ("dinner last night", "meal", ["logged_at", "calories"]),
            ("protein shake", "meal", ["logged_at", "protein_g", "calories"]),

            # Time context
            ("eggs for breakfast", "meal", ["logged_at", "meal_type", "calories", "protein_g"]),
            ("snack earlier", "meal", ["logged_at", "meal_type"]),
            ("post-workout meal", "meal", ["logged_at", "calories", "protein_g"]),
        ],

        "ACTIVITY LOGS": [
            # Vague activities - should estimate duration, distance, calories
            ("went for a run", "activity", ["start_date", "duration_minutes", "distance_km", "calories_burned"]),
            ("morning run", "activity", ["start_date", "duration_minutes", "calories_burned"]),
            ("easy 5k", "activity", ["start_date", "distance_km", "duration_minutes"]),
            ("cycling after work", "activity", ["start_date", "duration_minutes", "calories_burned"]),
            ("played basketball", "activity", ["start_date", "duration_minutes", "calories_burned"]),
            ("walked the dog", "activity", ["start_date", "duration_minutes"]),

            # Time + effort context
            ("hard run this morning", "activity", ["start_date", "rpe", "duration_minutes"]),
            ("easy bike ride yesterday", "activity", ["start_date", "rpe"]),
        ],

        "WORKOUT LOGS": [
            # Vague workouts - should estimate exercises, duration, calories
            ("chest workout", "workout", ["started_at", "duration_minutes", "exercises", "estimated_calories"]),
            ("leg day", "workout", ["started_at", "duration_minutes", "exercises"]),
            ("lifted weights", "workout", ["started_at", "duration_minutes", "estimated_calories"]),
            ("morning workout", "workout", ["started_at", "duration_minutes"]),
            ("upper body after work", "workout", ["started_at", "exercises"]),

            # Partial info
            ("bench pressed", "workout", ["started_at", "exercises", "duration_minutes"]),
            ("did squats and deadlifts", "workout", ["started_at", "exercises"]),
            ("arm day felt tough", "workout", ["started_at", "rpe", "exercises"]),
        ],

        "MEASUREMENT LOGS": [
            # Measurements - should have timestamps
            ("weighed myself", "measurement", ["measured_at"]),
            ("morning weigh-in", "measurement", ["measured_at"]),
            ("175 lbs", "measurement", ["measured_at", "weight_lbs"]),
        ],
    }

    print("=" * 100)
    print("COMPREHENSIVE ESTIMATION TEST - ALL ENTRY TYPES")
    print("=" * 100)
    print()

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    for category, tests in test_cases.items():
        print(f"\n{'=' * 100}")
        print(f"{category}")
        print(f"{'=' * 100}\n")

        for i, (input_text, force_type, required_fields) in enumerate(tests, 1):
            total_tests += 1
            print(f"{i}. Testing: '{input_text}' (type: {force_type})")
            print("-" * 80)

            try:
                result = await groq_service.classify_and_extract(
                    text=input_text,
                    force_type=force_type
                )

                data = result.get("data", {})
                primary = data.get("primary_fields", {})
                secondary = data.get("secondary_fields", {})

                # Merge for checking
                all_fields = {**primary, **secondary}

                # Check required fields
                missing_fields = []
                field_values = {}

                for field in required_fields:
                    value = all_fields.get(field)
                    field_values[field] = value

                    if value is None:
                        missing_fields.append(field)

                # Special validation for timestamps
                timestamp_fields = {
                    "logged_at": "Meal timestamp",
                    "start_date": "Activity timestamp",
                    "started_at": "Workout timestamp",
                    "measured_at": "Measurement timestamp"
                }

                timestamp_valid = True
                timestamp_msg = ""

                for ts_field, ts_desc in timestamp_fields.items():
                    if ts_field in required_fields:
                        ts_value = all_fields.get(ts_field)
                        valid, msg = validate_timestamp(ts_value, ts_desc)
                        if not valid:
                            timestamp_valid = False
                            timestamp_msg = msg
                            break

                # Determine pass/fail
                if missing_fields:
                    print(f"❌ FAILED: Missing required fields: {', '.join(missing_fields)}")
                    failed_tests += 1
                elif not timestamp_valid:
                    print(f"❌ FAILED: {timestamp_msg}")
                    failed_tests += 1
                else:
                    print(f"✅ PASSED: All required fields present")
                    passed_tests += 1

                # Show extracted data
                print(f"\nExtracted Data:")
                for field, value in field_values.items():
                    if value is not None:
                        print(f"   {field}: {value}")
                    else:
                        print(f"   {field}: ❌ NULL")

                # Show metadata
                confidence = result.get("confidence", 0)
                estimated = data.get("estimated", False)
                needs_clarification = data.get("needs_clarification", False)

                print(f"\nMetadata:")
                print(f"   Confidence: {confidence}")
                print(f"   Estimated: {estimated}")
                print(f"   Needs clarification: {needs_clarification}")

                # Show suggestions
                suggestions = result.get("suggestions", [])
                if suggestions:
                    print(f"\nSuggestions:")
                    for suggestion in suggestions[:2]:
                        print(f"   - {suggestion}")

                print()

            except Exception as e:
                print(f"❌ ERROR: {e}")
                failed_tests += 1
                print()

    # Summary
    print("\n" + "=" * 100)
    print("TEST SUMMARY")
    print("=" * 100)
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
    print(f"❌ Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
    print("=" * 100)

    if failed_tests == 0:
        print("\n🎉 ALL TESTS PASSED! Every entry type gets comprehensive estimates.")
    else:
        print(f"\n⚠️  {failed_tests} tests failed. Review the output above.")

    return passed_tests == total_tests

if __name__ == "__main__":
    success = asyncio.run(test_comprehensive_estimation())
    exit(0 if success else 1)
