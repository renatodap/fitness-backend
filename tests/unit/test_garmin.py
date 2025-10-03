"""
Unit tests for Garmin Service
"""

import pytest
from unittest.mock import Mock, patch

from app.services.garmin_service import GarminService, GARMIN_AVAILABLE


@pytest.fixture
def mock_supabase(mocker):
    """Mock Supabase client."""
    mock_client = Mock()
    mock_client.table().upsert().execute.return_value = Mock(data=[{"id": "activity-1"}])

    mocker.patch(
        "app.services.garmin_service.get_service_client",
        return_value=mock_client
    )
    return mock_client


@pytest.fixture
def service(mock_supabase):
    """Create GarminService instance."""
    return GarminService()


# Test initialization
def test_service_initialization(service):
    """Test service initializes correctly."""
    assert service.supabase is not None


# Test test_connection
@pytest.mark.asyncio
@pytest.mark.skipif(not GARMIN_AVAILABLE, reason="garminconnect not installed")
async def test_connection_missing_credentials(service):
    """Test error handling for missing credentials."""
    with pytest.raises(ValueError):
        await service.test_connection("", "")


# Test sync_activities
@pytest.mark.asyncio
async def test_sync_activities_missing_fields(service):
    """Test error handling for missing required fields."""
    with pytest.raises(ValueError):
        await service.sync_activities("", "email", "password")
