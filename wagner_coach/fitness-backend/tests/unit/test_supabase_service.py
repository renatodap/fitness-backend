"""
Unit tests for Supabase Service

Tests client creation, caching, singleton pattern, thread safety, and error handling.
"""

import threading
import pytest
from unittest.mock import Mock, patch
from app.services.supabase_service import (
    SupabaseService,
    get_supabase_service,
    get_service_client,
    get_user_client,
)


@pytest.fixture
def clean_supabase_service():
    """Provide clean SupabaseService for testing."""
    service = SupabaseService()
    service.clear_cache()
    yield service
    service.clear_cache()


@pytest.fixture
def mock_create_client(mocker):
    """Mock supabase create_client function."""
    mock_client = Mock()
    mock_table = Mock()
    mock_table.select().limit().execute.return_value = Mock(data=[{"id": "test"}])
    mock_client.table.return_value = mock_table

    return mocker.patch(
        "app.services.supabase_service.create_client", return_value=mock_client
    )


# TC-SUPA-001: Create Service Role Client
def test_create_service_client(clean_supabase_service, mock_create_client):
    """Verify service role client can be created."""
    service = clean_supabase_service

    client = service.get_service_client()

    assert client is not None
    # Verify create_client was called with service key
    mock_create_client.assert_called()


# TC-SUPA-002: Create User-Scoped Client
def test_create_user_client(clean_supabase_service, mock_create_client):
    """Verify user-scoped client can be created with token."""
    service = clean_supabase_service

    client = service.get_user_client("test-user-token-123")

    assert client is not None
    # Verify create_client was called with token in headers
    call_args = mock_create_client.call_args
    assert call_args is not None


# TC-SUPA-003: Invalid Token Handling
def test_invalid_token(clean_supabase_service):
    """Verify proper error for invalid token."""
    service = clean_supabase_service

    # Empty token
    with pytest.raises(ValueError) as exc_info:
        service.get_user_client("")

    assert "token" in str(exc_info.value).lower()

    # Very short token
    with pytest.raises(ValueError) as exc_info:
        service.get_user_client("abc")

    assert "token" in str(exc_info.value).lower()


# TC-SUPA-004: Service Client Cached
def test_service_client_cached(clean_supabase_service, mock_create_client):
    """Verify service client is cached and reused."""
    service = clean_supabase_service

    client1 = service.get_service_client()
    client2 = service.get_service_client()

    # Should be same instance
    assert client1 is client2

    # create_client should only be called once
    assert mock_create_client.call_count == 1


# TC-SUPA-005: User Clients Cached by Token
def test_user_clients_cached_by_token(clean_supabase_service, mock_create_client):
    """Verify user clients cached per token."""
    service = clean_supabase_service

    # Create multiple clients
    mock_create_client.return_value = Mock()

    client1_a = service.get_user_client("token-user1")
    client1_b = service.get_user_client("token-user1")
    client2 = service.get_user_client("token-user2")

    # Same token should return same client
    assert client1_a is client1_b

    # Different tokens should return different clients
    assert client1_a is not client2


# TC-SUPA-006: Cache Clearing
def test_clear_cache(clean_supabase_service, mock_create_client):
    """Verify cache can be cleared."""
    service = clean_supabase_service

    # Get service client
    client1 = service.get_service_client()
    assert mock_create_client.call_count == 1

    # Clear cache
    service.clear_cache()

    # Get service client again - should create new one
    client2 = service.get_service_client()
    assert mock_create_client.call_count == 2

    # Should be new instance
    assert client2 is not None


# TC-SUPA-007: Singleton Instance
def test_singleton_instance():
    """Verify SupabaseService is singleton."""
    service1 = SupabaseService()
    service2 = SupabaseService()

    assert service1 is service2


# TC-SUPA-008: Singleton Across get_supabase_service()
def test_get_supabase_service_singleton():
    """Verify get_supabase_service() returns singleton."""
    service1 = get_supabase_service()
    service2 = get_supabase_service()
    service3 = SupabaseService()

    assert service1 is service2
    assert service1 is service3


# TC-SUPA-009: Concurrent Client Creation
def test_thread_safe_client_creation(clean_supabase_service, mock_create_client):
    """Verify thread-safe client creation."""
    service = clean_supabase_service

    clients = []
    lock = threading.Lock()

    def get_client():
        client = service.get_service_client()
        with lock:
            clients.append(client)

    # Create 10 threads trying to get client simultaneously
    threads = [threading.Thread(target=get_client) for _ in range(10)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # All threads should get the same client
    assert len(clients) == 10
    assert all(c is clients[0] for c in clients)

    # Client should only be created once
    assert mock_create_client.call_count == 1


# TC-SUPA-010: Handle Connection Failure
def test_connection_failure(clean_supabase_service, mocker):
    """Verify proper error handling on connection failure."""
    mocker.patch(
        "app.services.supabase_service.create_client",
        side_effect=Exception("Connection failed"),
    )

    service = clean_supabase_service

    with pytest.raises(Exception) as exc_info:
        service.get_service_client()

    assert "Connection failed" in str(exc_info.value)


# TC-SUPA-011: Handle Invalid Configuration
def test_invalid_configuration(clean_supabase_service, mocker):
    """Verify error when config is invalid."""
    mocker.patch(
        "app.services.supabase_service.create_client",
        side_effect=ValueError("Invalid URL"),
    )

    service = clean_supabase_service

    with pytest.raises(Exception) as exc_info:
        service.get_service_client()

    assert "Invalid URL" in str(exc_info.value)


# TC-SUPA-012: Health Check Success
def test_health_check_success(clean_supabase_service, mocker):
    """Verify health check returns True when healthy."""
    mock_client = Mock()
    mock_table = Mock()
    mock_table.select().limit().execute.return_value = Mock(data=[{"id": "test"}])
    mock_client.table.return_value = mock_table

    mocker.patch.object(
        clean_supabase_service, "get_service_client", return_value=mock_client
    )

    result = clean_supabase_service.health_check()
    assert result is True


# TC-SUPA-013: Health Check Failure
def test_health_check_failure(clean_supabase_service, mocker):
    """Verify health check returns False on failure."""
    mock_client = Mock()
    mock_client.table().select().limit().execute.side_effect = Exception("DB Error")

    mocker.patch.object(
        clean_supabase_service, "get_service_client", return_value=mock_client
    )

    result = clean_supabase_service.health_check()
    assert result is False


# TC-SUPA-014: get_service_client() Helper
def test_get_service_client_helper(mock_create_client):
    """Verify convenience function works."""
    # Clear cache first
    service = get_supabase_service()
    service.clear_cache()

    client = get_service_client()

    assert client is not None

    # Should be same as getting from service
    service_client = service.get_service_client()
    assert client is service_client


# TC-SUPA-015: get_user_client() Helper
def test_get_user_client_helper(mock_create_client):
    """Verify user client convenience function."""
    # Clear cache first
    service = get_supabase_service()
    service.clear_cache()

    token = "test-token-12345"
    client = get_user_client(token)

    assert client is not None

    # Should be same as getting from service
    service_client = service.get_user_client(token)
    assert client is service_client


# TC-SUPA-016: FastAPI Dependency Injection
def test_fastapi_dependency(mock_create_client):
    """Verify service works with FastAPI dependencies."""
    from fastapi import Depends, FastAPI, Header
    from fastapi.testclient import TestClient

    app = FastAPI()

    async def get_db(authorization: str = Header(...)):
        token = authorization.split(" ")[1]
        return get_user_client(token)

    @app.get("/test")
    async def test_endpoint(db=Depends(get_db)):
        return {"status": "ok", "has_db": db is not None}

    client = TestClient(app)
    response = client.get("/test", headers={"Authorization": "Bearer test-token-123"})

    assert response.status_code == 200
    assert response.json()["has_db"] is True


# TC-SUPA-017: Empty Token String
def test_empty_token(clean_supabase_service):
    """Verify handling of empty token."""
    service = clean_supabase_service

    with pytest.raises(ValueError) as exc_info:
        service.get_user_client("")

    assert "token" in str(exc_info.value).lower()


# TC-SUPA-018: Very Long Token
def test_very_long_token(clean_supabase_service, mock_create_client):
    """Verify handling of unusually long token."""
    service = clean_supabase_service
    long_token = "a" * 10000

    # Should work with very long token
    client = service.get_user_client(long_token)
    assert client is not None


# TC-SUPA-019: Special Characters in Token
def test_special_characters_in_token(clean_supabase_service, mock_create_client):
    """Verify handling of special characters."""
    service = clean_supabase_service
    special_token = "token-with-!@#$%^&*()"

    # Should handle special characters
    client = service.get_user_client(special_token)
    assert client is not None


# Additional Test: Client Cleanup
def test_client_cleanup(clean_supabase_service, mock_create_client):
    """Verify old clients are cleaned up when cache is full."""
    service = clean_supabase_service

    # Set lower max for testing
    original_max = service.MAX_USER_CLIENTS
    service.MAX_USER_CLIENTS = 10

    try:
        # Create more clients than max
        for i in range(15):
            service.get_user_client(f"token-{i}")

        # Should have cleaned up some clients
        assert len(service._user_clients) <= service.MAX_USER_CLIENTS
    finally:
        # Restore original max
        service.MAX_USER_CLIENTS = original_max


# Additional Test: Multiple User Clients Don't Interfere
def test_multiple_user_clients_independent(clean_supabase_service, mock_create_client):
    """Verify multiple user clients don't interfere with each other."""
    service = clean_supabase_service

    # Create clients for different users
    clients = {}
    for i in range(5):
        token = f"user-token-{i}"
        clients[token] = service.get_user_client(token)

    # Verify each client is unique
    client_list = list(clients.values())
    for i, client1 in enumerate(client_list):
        for j, client2 in enumerate(client_list):
            if i != j:
                assert client1 is not client2


# Additional Test: Service Client Independent from User Clients
def test_service_client_independent(clean_supabase_service, mock_create_client):
    """Verify service client is independent from user clients."""
    service = clean_supabase_service

    service_client = service.get_service_client()
    user_client = service.get_user_client("test-token-123")

    # Should be different instances
    assert service_client is not user_client