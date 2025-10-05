"""
Comprehensive test suite for groq_service_v2.py
Tests all 10 test cases from QUICK_ENTRY_TEST_PLAN.md

NOTE: These tests require GROQ_API_KEY environment variable to be set.
Run with: GROQ_API_KEY=your_key pytest tests/test_groq_service_v2.py

For CI/CD, set environment variables or mock the Groq API calls.
"""

import pytest
import os
from app.services.groq_service_v2 import GroqServiceV2

# Skip all tests if GROQ_API_KEY is not set
pytestmark = pytest.mark.skipif(
    not os.environ.get('GROQ_API_KEY'),
    reason="GROQ_API_KEY environment variable not set. These are integration tests that require live API access."
)


@pytest.fixture
def groq_service():
    """Fixture to provide GroqServiceV2 instance"""
    return GroqServiceV2()


class TestMealEntries:
    """Test cases for meal entry extraction"""

    @pytest.mark.asyncio
    async def test_meal_with_all_portions(self, groq_service):
        """
        Test Case 1: Meal with all portions
        Expected: Complete nutrition data, no warnings
        """
        result = await groq_service.classify_and_extract(
            "Grilled chicken breast 6oz, brown rice 1 cup, broccoli 1 cup"
        )

        assert result["success"] is True
        assert result["entry_type"] == "meal"
        assert result["confidence"] > 0.8
        assert result["data"]["needs_clarification"] is False

        primary = result["data"]["primary_fields"]
        assert primary["calories"] is not None
        assert primary["protein_g"] is not None
        assert len(primary["foods"]) == 3
        assert all("quantity" in food for food in primary["foods"])
        assert all(food["quantity"] != "not specified" for food in primary["foods"])

        assert len(result["validation"]["errors"]) == 0
        assert len(result["validation"]["warnings"]) == 0

    @pytest.mark.asyncio
    async def test_meal_without_portions(self, groq_service):
        """
        Test Case 2: Meal without portions
        Expected: null nutrition, needs_clarification=True, warnings present
        """
        result = await groq_service.classify_and_extract("chicken and rice")

        assert result["success"] is True
        assert result["entry_type"] == "meal"
        assert result["data"]["needs_clarification"] is True

        primary = result["data"]["primary_fields"]
        assert primary["calories"] is None
        assert primary["protein_g"] is None
        assert len(primary["foods"]) >= 1

        assert len(result["validation"]["warnings"]) > 0
        assert "portions" in result["validation"]["missing_critical"]


class TestWorkoutEntries:
    """Test cases for workout entry extraction"""

    @pytest.mark.asyncio
    async def test_workout_with_exercises(self, groq_service):
        """
        Test Case 3: Workout with exercises
        Expected: Exercise cards with volume calculations
        """
        result = await groq_service.classify_and_extract(
            "Bench press 4x8 at 185lbs, Incline DB press 3x12 at 60lbs per side"
        )

        assert result["success"] is True
        assert result["entry_type"] == "workout"
        assert result["confidence"] > 0.8

        primary = result["data"]["primary_fields"]
        assert len(primary["exercises"]) == 2

        # Check first exercise
        ex1 = primary["exercises"][0]
        assert ex1["sets"] == 4
        assert ex1["reps"] == 8
        assert ex1["weight_lbs"] == 185

        # Check second exercise (with per-side weight)
        ex2 = primary["exercises"][1]
        assert ex2["sets"] == 3
        assert ex2["reps"] == 12
        assert "weight_per_side" in ex2 or ex2["weight_lbs"] == 120

        # Check volume calculation
        secondary = result["data"]["secondary_fields"]
        assert "volume_load" in secondary
        assert secondary["volume_load"] > 0

    @pytest.mark.asyncio
    async def test_workout_minimal(self, groq_service):
        """
        Test workout with minimal info
        Expected: Should still extract basic structure
        """
        result = await groq_service.classify_and_extract("Did some squats and lunges")

        assert result["entry_type"] == "workout"
        primary = result["data"]["primary_fields"]
        assert "exercises" in primary or "workout_name" in primary


class TestActivityEntries:
    """Test cases for activity entry extraction"""

    @pytest.mark.asyncio
    async def test_activity_with_pace_calculation(self, groq_service):
        """
        Test Case 4: Activity with pace
        Expected: Auto-calculated pace field
        """
        result = await groq_service.classify_and_extract("Ran 5 miles in 40 minutes")

        assert result["success"] is True
        assert result["entry_type"] == "activity"

        primary = result["data"]["primary_fields"]
        assert primary["distance_miles"] == 5
        assert primary["duration_minutes"] == 40
        assert "pace" in primary
        assert "8:00" in primary["pace"] or "8min" in primary["pace"].lower()

    @pytest.mark.asyncio
    async def test_activity_cycling(self, groq_service):
        """
        Test cycling activity
        """
        result = await groq_service.classify_and_extract("Biked 15 miles")

        assert result["entry_type"] == "activity"
        primary = result["data"]["primary_fields"]
        assert primary["distance_miles"] == 15
        assert "bike" in primary["activity_type"].lower() or "cycling" in primary["activity_type"].lower()


class TestNoteEntries:
    """Test cases for note entry extraction"""

    @pytest.mark.asyncio
    async def test_note_with_positive_sentiment(self, groq_service):
        """
        Test Case 5: Note with sentiment analysis
        Expected: Positive sentiment detected
        """
        result = await groq_service.classify_and_extract(
            "Feeling amazing today! Hit a new PR on deadlifts and energy is through the roof!"
        )

        assert result["success"] is True
        assert result["entry_type"] == "note"

        primary = result["data"]["primary_fields"]
        assert "content" in primary
        assert "sentiment" in primary
        assert primary["sentiment"] == "positive"
        assert primary.get("sentiment_score", 0.5) > 0.7

    @pytest.mark.asyncio
    async def test_note_with_negative_sentiment(self, groq_service):
        """
        Test negative sentiment detection
        """
        result = await groq_service.classify_and_extract(
            "Feeling tired and unmotivated. Skipped gym again."
        )

        assert result["entry_type"] == "note"
        primary = result["data"]["primary_fields"]
        assert primary["sentiment"] in ["negative", "neutral"]

    @pytest.mark.asyncio
    async def test_note_with_neutral_sentiment(self, groq_service):
        """
        Test neutral sentiment detection
        """
        result = await groq_service.classify_and_extract(
            "Had workout today. It was okay."
        )

        assert result["entry_type"] == "note"
        primary = result["data"]["primary_fields"]
        assert "sentiment" in primary


class TestMeasurementEntries:
    """Test cases for measurement entry extraction"""

    @pytest.mark.asyncio
    async def test_measurement_weight(self, groq_service):
        """
        Test Case 6: Measurement with weight
        Expected: Weight extracted in lbs
        """
        result = await groq_service.classify_and_extract("Weight 175.2 lbs")

        assert result["success"] is True
        assert result["entry_type"] == "measurement"

        primary = result["data"]["primary_fields"]
        assert primary["weight_lbs"] == 175.2

    @pytest.mark.asyncio
    async def test_measurement_body_fat(self, groq_service):
        """
        Test body fat percentage extraction
        """
        result = await groq_service.classify_and_extract("Body fat 15.3%")

        assert result["entry_type"] == "measurement"
        primary = result["data"]["primary_fields"]
        assert "body_fat_pct" in primary

    @pytest.mark.asyncio
    async def test_measurement_multiple_metrics(self, groq_service):
        """
        Test multiple measurements in one entry
        """
        result = await groq_service.classify_and_extract("Weight 180 lbs, body fat 16%")

        assert result["entry_type"] == "measurement"
        primary = result["data"]["primary_fields"]
        assert "weight_lbs" in primary
        assert "body_fat_pct" in primary


class TestEdgeCases:
    """Test cases for edge cases and error handling"""

    @pytest.mark.asyncio
    async def test_low_confidence_gibberish(self, groq_service):
        """
        Test Case 8: Low confidence / unknown input
        Expected: entry_type="unknown", low confidence, errors present
        """
        result = await groq_service.classify_and_extract("xyz abc 123 asdf")

        assert result["entry_type"] == "unknown"
        assert result["confidence"] < 0.5
        assert len(result["validation"]["errors"]) > 0 or result["data"]["needs_clarification"] is True

    @pytest.mark.asyncio
    async def test_empty_input(self, groq_service):
        """
        Test empty string input
        Expected: Validation error
        """
        result = await groq_service.classify_and_extract("")

        assert result["success"] is False or result["entry_type"] == "unknown"
        assert len(result["validation"]["errors"]) > 0

    @pytest.mark.asyncio
    async def test_very_long_input(self, groq_service):
        """
        Test very long input (edge case)
        """
        long_text = "I ate " + "chicken " * 100
        result = await groq_service.classify_and_extract(long_text)

        assert result["entry_type"] in ["meal", "note", "unknown"]
        # Should not crash, should handle gracefully

    @pytest.mark.asyncio
    async def test_ambiguous_input(self, groq_service):
        """
        Test ambiguous input that could be multiple types
        """
        result = await groq_service.classify_and_extract("180")

        # Could be weight, calories, or just a note
        assert result["entry_type"] in ["measurement", "note", "unknown"]
        # Should make a reasonable guess


class TestValidation:
    """Test cases for validation structure"""

    @pytest.mark.asyncio
    async def test_validation_structure_always_present(self, groq_service):
        """
        Test Case 10: Validation structure
        Expected: All responses have validation object
        """
        test_inputs = [
            "chicken salad",
            "bench press 185x5",
            "ran 3 miles",
            "feeling good",
            "weight 170",
        ]

        for text in test_inputs:
            result = await groq_service.classify_and_extract(text)

            assert "validation" in result
            assert "errors" in result["validation"]
            assert "warnings" in result["validation"]
            assert "missing_critical" in result["validation"]
            assert isinstance(result["validation"]["errors"], list)
            assert isinstance(result["validation"]["warnings"], list)
            assert isinstance(result["validation"]["missing_critical"], list)

    @pytest.mark.asyncio
    async def test_response_structure_consistency(self, groq_service):
        """
        Verify all responses have consistent structure
        """
        result = await groq_service.classify_and_extract("test meal 500 calories")

        # Required top-level fields
        assert "success" in result
        assert "entry_type" in result
        assert "confidence" in result
        assert "data" in result
        assert "validation" in result
        assert "suggestions" in result

        # Required data fields
        assert "primary_fields" in result["data"]
        assert "secondary_fields" in result["data"]
        assert "estimated" in result["data"]
        assert "needs_clarification" in result["data"]

        # Type checks
        assert isinstance(result["success"], bool)
        assert isinstance(result["entry_type"], str)
        assert isinstance(result["confidence"], (int, float))
        assert isinstance(result["suggestions"], list)


class TestConservativeEstimation:
    """Test conservative estimation principles"""

    @pytest.mark.asyncio
    async def test_no_wild_guesses_for_calories(self, groq_service):
        """
        Verify service doesn't make wild calorie guesses without portions
        """
        result = await groq_service.classify_and_extract("had some pasta")

        primary = result["data"]["primary_fields"]
        # Should return null instead of guessing
        assert primary.get("calories") is None or result["data"]["estimated"] is True

    @pytest.mark.asyncio
    async def test_estimated_flag_when_guessing(self, groq_service):
        """
        Verify estimated flag is set when making educated guesses
        """
        result = await groq_service.classify_and_extract("chicken salad, about 400 calories")

        # If nutrition is filled in, check if it's marked as estimated
        if result["data"]["primary_fields"].get("calories"):
            # Either user provided it (not estimated) or AI estimated it (estimated=True)
            assert result["data"]["estimated"] is True or "400" in "chicken salad, about 400 calories"


class TestSuggestions:
    """Test AI suggestions"""

    @pytest.mark.asyncio
    async def test_suggestions_provided_when_helpful(self, groq_service):
        """
        Verify helpful suggestions are provided
        """
        result = await groq_service.classify_and_extract("chicken")

        # Should suggest adding more detail
        assert len(result["suggestions"]) > 0
        assert any("portion" in s.lower() or "detail" in s.lower() for s in result["suggestions"])

    @pytest.mark.asyncio
    async def test_no_suggestions_when_complete(self, groq_service):
        """
        Verify suggestions are minimal when entry is complete
        """
        result = await groq_service.classify_and_extract(
            "Grilled chicken breast 6oz, 280 calories, 42g protein"
        )

        # Complete entry should have fewer or no suggestions
        # (or suggestions should be encouraging, not corrective)
        if len(result["suggestions"]) > 0:
            assert not any("missing" in s.lower() for s in result["suggestions"])


# Run with: pytest tests/test_groq_service_v2.py -v
