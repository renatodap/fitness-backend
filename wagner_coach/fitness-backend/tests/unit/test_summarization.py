"""
Unit tests for Summarization Service
"""

import pytest
from datetime import date, datetime, timedelta
from unittest.mock import Mock, AsyncMock

from app.services.summarization_service import (
    SummarizationService,
    SummaryPeriodType,
)


@pytest.fixture
def mock_supabase(mocker):
    """Mock Supabase client for summarization tests."""
    mock_client = Mock()

    # Mock table responses
    mock_table = Mock()
    mock_table.select().execute.return_value = Mock(data=[])
    mock_table.insert().execute.return_value = Mock(data=[{"id": "test-id"}])
    mock_client.table.return_value = mock_table

    mocker.patch(
        "app.services.summarization_service.get_service_client",
        return_value=mock_client
    )
    return mock_client


@pytest.fixture
def service(mock_supabase):
    """Create SummarizationService instance."""
    return SummarizationService()


# Test initialization
def test_service_initialization(service):
    """Test service initializes with Supabase client."""
    assert service.supabase is not None


# Test helper methods
def test_is_first_day_of_month(service):
    """Test first day of month detection."""
    assert service._is_first_day_of_month(date(2025, 1, 1)) is True
    assert service._is_first_day_of_month(date(2025, 1, 2)) is False
    assert service._is_first_day_of_month(date(2025, 12, 31)) is False


def test_is_first_day_of_quarter(service):
    """Test first day of quarter detection."""
    assert service._is_first_day_of_quarter(date(2025, 1, 1)) is True
    assert service._is_first_day_of_quarter(date(2025, 4, 1)) is True
    assert service._is_first_day_of_quarter(date(2025, 7, 1)) is True
    assert service._is_first_day_of_quarter(date(2025, 10, 1)) is True
    assert service._is_first_day_of_quarter(date(2025, 2, 1)) is False
    assert service._is_first_day_of_quarter(date(2025, 1, 2)) is False


def test_get_quarter(service):
    """Test quarter calculation."""
    assert service._get_quarter(date(2025, 1, 15)) == 1
    assert service._get_quarter(date(2025, 4, 15)) == 2
    assert service._get_quarter(date(2025, 7, 15)) == 3
    assert service._get_quarter(date(2025, 10, 15)) == 4


# Test weekly summary generation
@pytest.mark.asyncio
async def test_generate_weekly_summary(service, mock_supabase):
    """Test weekly summary generation."""
    user_id = "test-user-123"
    end_date = date(2025, 1, 7)

    # Mock data fetching
    service._fetch_workouts = AsyncMock(return_value=[
        {"type": "cardio", "duration_minutes": 30, "calories": 200}
    ])
    service._fetch_nutrition = AsyncMock(return_value=[])
    service._fetch_activities = AsyncMock(return_value=[])

    summary = await service.generate_weekly_summary(user_id, end_date)

    assert summary["period_type"] == "weekly"
    assert summary["period_start"] == "2025-01-01"
    assert summary["period_end"] == "2025-01-07"
    assert summary["workouts"]["total_workouts"] == 1


# Test monthly summary generation
@pytest.mark.asyncio
async def test_generate_monthly_summary(service, mock_supabase):
    """Test monthly summary generation."""
    user_id = "test-user-123"

    service._fetch_workouts = AsyncMock(return_value=[])
    service._fetch_nutrition = AsyncMock(return_value=[])
    service._fetch_activities = AsyncMock(return_value=[])

    summary = await service.generate_monthly_summary(user_id, month=1, year=2025)

    assert summary["period_type"] == "monthly"
    assert summary["period_start"] == "2025-01-01"
    assert summary["period_end"] == "2025-01-31"


# Test user summary generation
@pytest.mark.asyncio
async def test_generate_user_summaries_invalid_user(service):
    """Test error handling for invalid user ID."""
    with pytest.raises(ValueError):
        await service.generate_user_summaries("")


# Test data aggregation
def test_aggregate_workouts_empty(service):
    """Test workout aggregation with no data."""
    result = service._aggregate_workouts([])

    assert result["total_workouts"] == 0
    assert result["total_duration_minutes"] == 0
    assert result["workout_types"] == {}


def test_aggregate_workouts_with_data(service):
    """Test workout aggregation with data."""
    workouts = [
        {"type": "cardio", "duration_minutes": 30, "calories": 200},
        {"type": "strength", "duration_minutes": 45, "calories": 150},
        {"type": "cardio", "duration_minutes": 25, "calories": 180},
    ]

    result = service._aggregate_workouts(workouts)

    assert result["total_workouts"] == 3
    assert result["total_duration_minutes"] == 100
    assert result["total_calories"] == 530
    assert result["workout_types"]["cardio"] == 2
    assert result["workout_types"]["strength"] == 1


def test_aggregate_nutrition_empty(service):
    """Test nutrition aggregation with no data."""
    result = service._aggregate_nutrition([])

    assert result["total_meals_logged"] == 0
    assert result["days_logged"] == 0


def test_aggregate_nutrition_with_data(service):
    """Test nutrition aggregation with data."""
    meals = [
        {"date": "2025-01-01", "calories": 500, "protein_g": 30, "carbs_g": 50, "fat_g": 15},
        {"date": "2025-01-01", "calories": 600, "protein_g": 35, "carbs_g": 60, "fat_g": 20},
        {"date": "2025-01-02", "calories": 550, "protein_g": 32, "carbs_g": 55, "fat_g": 18},
    ]

    result = service._aggregate_nutrition(meals)

    assert result["total_meals_logged"] == 3
    assert result["days_logged"] == 2
    assert result["avg_calories_per_day"] == 825.0  # (500+600+550)/2


# Test batch processing
@pytest.mark.asyncio
async def test_generate_all_summaries(service, mock_supabase):
    """Test batch summary generation for all users."""
    # Mock users
    mock_supabase.table().select().execute.return_value = Mock(
        data=[{"id": "user1"}, {"id": "user2"}]
    )

    service.generate_user_summaries = AsyncMock(return_value=1)

    result = await service.generate_all_summaries()

    assert result["processed"] == 2
    assert result["summaries_created"] == 2
    assert result["errors"] == 0


@pytest.mark.asyncio
async def test_generate_all_summaries_with_errors(service, mock_supabase):
    """Test batch processing handles individual errors."""
    mock_supabase.table().select().execute.return_value = Mock(
        data=[{"id": "user1"}, {"id": "user2"}, {"id": "user3"}]
    )

    async def mock_generate(user_id):
        if user_id == "user2":
            raise Exception("Test error")
        return 1

    service.generate_user_summaries = mock_generate

    result = await service.generate_all_summaries()

    assert result["processed"] == 2
    assert result["errors"] == 1
