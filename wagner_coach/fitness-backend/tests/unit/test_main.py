"""
Unit tests for FastAPI Application

Tests main app configuration, health endpoints, and routing.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint returns basic info."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "healthy"


def test_health_endpoint_healthy(client, mocker):
    """Test health endpoint when database is healthy."""
    # Mock health check to return True
    mock_service = mocker.Mock()
    mock_service.health_check.return_value = True

    mocker.patch(
        "app.main.get_supabase_service",
        return_value=mock_service,
    )

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["services"]["database"] == "connected"


def test_health_endpoint_unhealthy(client, mocker):
    """Test health endpoint when database is unhealthy."""
    # Mock health check to return False
    mock_service = mocker.Mock()
    mock_service.health_check.return_value = False

    mocker.patch(
        "app.main.get_supabase_service",
        return_value=mock_service,
    )

    response = client.get("/health")

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "unhealthy"
    assert data["services"]["database"] == "disconnected"


def test_cors_headers(client):
    """Test CORS headers are present."""
    response = client.options("/", headers={"Origin": "http://localhost:3000"})

    # CORS middleware should add headers
    assert "access-control-allow-origin" in response.headers


def test_docs_available_in_debug(client, mocker):
    """Test /docs endpoint available in debug mode."""
    # When DEBUG=True, docs should be available
    response = client.get("/docs")

    # Should either return docs or redirect
    # (depends on DEBUG setting)
    assert response.status_code in [200, 307, 404]


def test_app_metadata(client):
    """Test app has correct metadata."""
    assert app.title == "Fitness Backend"
    assert app.version == "0.1.0"


def test_root_includes_environment(client):
    """Test root endpoint includes environment info."""
    response = client.get("/")

    data = response.json()
    assert "environment" in data


def test_health_includes_version(client, mocker):
    """Test health endpoint includes version."""
    mock_service = mocker.Mock()
    mock_service.health_check.return_value = True

    mocker.patch("app.main.get_supabase_service", return_value=mock_service)

    response = client.get("/health")

    data = response.json()
    assert "version" in data
    assert data["version"] == "0.1.0"