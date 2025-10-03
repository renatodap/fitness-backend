"""
Unit tests for Meal Parser Service
"""

import pytest
from unittest.mock import Mock, AsyncMock
import json

from app.services.meal_parser_service import MealParserService, ParsedMeal


@pytest.fixture
def mock_openai(mocker):
    """Mock OpenAI client."""
    mock_client = AsyncMock()

    # Mock chat completion response
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content=json.dumps({
            "meal_name": "Test Meal",
            "category": "lunch",
            "logged_at": "2025-09-30T12:00:00Z",
            "foods": [{"name": "chicken", "quantity": 6, "unit": "oz"}]
        })))
    ]
    mock_client.chat.completions.create.return_value = mock_response

    mocker.patch(
        "app.services.meal_parser_service.AsyncOpenAI",
        return_value=mock_client
    )
    return mock_client


@pytest.fixture
def mock_supabase(mocker):
    """Mock Supabase client."""
    mock_client = Mock()
    mock_client.table().select().ilike().limit().execute.return_value = Mock(data=[])

    mocker.patch(
        "app.services.meal_parser_service.get_service_client",
        return_value=mock_client
    )
    return mock_client


@pytest.fixture
def service(mock_openai, mock_supabase):
    """Create MealParserService instance."""
    return MealParserService()


# Test initialization
def test_service_initialization(service):
    """Test service initializes correctly."""
    assert service.openai is not None
    assert service.supabase is not None


# Test parse
@pytest.mark.asyncio
async def test_parse_success(service, mock_openai, mock_supabase):
    """Test successful meal parsing."""
    # Mock nutrition estimation
    mock_openai.chat.completions.create.side_effect = [
        Mock(choices=[Mock(message=Mock(content=json.dumps({
            "meal_name": "Chicken Meal",
            "category": "lunch",
            "logged_at": "2025-09-30T12:00:00Z",
            "foods": [{"name": "chicken", "quantity": 6, "unit": "oz"}]
        })))]),
        Mock(choices=[Mock(message=Mock(content=json.dumps({
            "calories": 200,
            "protein_g": 30,
            "carbs_g": 0,
            "fat_g": 8
        })))])
    ]

    result = await service.parse("6 oz grilled chicken")

    assert isinstance(result, ParsedMeal)
    assert result.meal_name == "Chicken Meal"
    assert len(result.foods) > 0


@pytest.mark.asyncio
async def test_parse_empty_description(service):
    """Test error handling for empty description."""
    with pytest.raises(ValueError):
        await service.parse("")


# Test totals calculation
def test_calculate_totals(service):
    """Test calculating nutrition totals."""
    from app.services.meal_parser_service import ParsedFoodItem

    foods = [
        ParsedFoodItem(
            name="Food 1",
            quantity=1,
            unit="serving",
            nutrition={"calories": 100, "protein_g": 10, "carbs_g": 20, "fat_g": 5},
            confidence="high",
            source="database"
        ),
        ParsedFoodItem(
            name="Food 2",
            quantity=1,
            unit="serving",
            nutrition={"calories": 150, "protein_g": 15, "carbs_g": 25, "fat_g": 7},
            confidence="high",
            source="database"
        )
    ]

    totals = service._calculate_totals(foods)

    assert totals["calories"] == 250
    assert totals["protein"] == 25
    assert totals["carbs"] == 45
    assert totals["fat"] == 12


# Test confidence calculation
def test_calculate_confidence(service):
    """Test confidence level calculation."""
    from app.services.meal_parser_service import ParsedFoodItem

    # All high confidence
    high_foods = [
        ParsedFoodItem(name="F1", quantity=1, unit="g", nutrition={}, confidence="high", source="database"),
        ParsedFoodItem(name="F2", quantity=1, unit="g", nutrition={}, confidence="high", source="database")
    ]
    assert service._calculate_confidence(high_foods) == "high"

    # Mixed confidence
    mixed_foods = [
        ParsedFoodItem(name="F1", quantity=1, unit="g", nutrition={}, confidence="high", source="database"),
        ParsedFoodItem(name="F2", quantity=1, unit="g", nutrition={}, confidence="medium", source="openai")
    ]
    assert service._calculate_confidence(mixed_foods) == "medium"
