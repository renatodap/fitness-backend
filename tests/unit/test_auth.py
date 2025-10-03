"""
Unit tests for Authentication Middleware

Tests JWT verification, user extraction, and secret validation.
"""

import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from unittest.mock import Mock

from app.api.middleware.auth import (
    verify_token,
    get_current_user,
    get_current_user_optional,
    verify_cron_secret,
    verify_webhook_secret,
)
from app.config import settings


@pytest.fixture
def valid_token():
    """Generate valid JWT token for testing."""
    payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "iss": "https://test.supabase.co/auth/v1",
        "email": "test@example.com",
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


@pytest.fixture
def expired_token():
    """Generate expired JWT token."""
    payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() - timedelta(hours=1),
        "iat": datetime.utcnow() - timedelta(hours=2),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


@pytest.fixture
def token_without_sub():
    """Generate token missing 'sub' claim."""
    payload = {
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "email": "test@example.com",
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


# Test verify_token function
@pytest.mark.asyncio
async def test_verify_valid_token(valid_token):
    """Test verification of valid token."""
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=valid_token)

    user_id = await verify_token(credentials)

    assert user_id == "test-user-id"


@pytest.mark.asyncio
async def test_verify_expired_token(expired_token):
    """Test rejection of expired token."""
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=expired_token)

    with pytest.raises(HTTPException) as exc_info:
        await verify_token(credentials)

    assert exc_info.value.status_code == 401
    assert "expired" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
async def test_verify_token_invalid_signature():
    """Test rejection of token with invalid signature."""
    payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    # Sign with wrong secret
    invalid_token = jwt.encode(payload, "wrong-secret", algorithm="HS256")

    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=invalid_token)

    with pytest.raises(HTTPException) as exc_info:
        await verify_token(credentials)

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_verify_token_missing_sub(token_without_sub):
    """Test rejection of token without 'sub' claim."""
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials=token_without_sub
    )

    with pytest.raises(HTTPException) as exc_info:
        await verify_token(credentials)

    assert exc_info.value.status_code == 401
    assert "sub" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
async def test_verify_malformed_token():
    """Test rejection of malformed token."""
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="not-a-jwt")

    with pytest.raises(HTTPException) as exc_info:
        await verify_token(credentials)

    assert exc_info.value.status_code == 401


# Test get_current_user dependency
@pytest.mark.asyncio
async def test_get_current_user_valid(valid_token):
    """Test get_current_user with valid token."""
    user_id = await get_current_user(f"Bearer {valid_token}")

    assert user_id == "test-user-id"


@pytest.mark.asyncio
async def test_get_current_user_missing_bearer():
    """Test get_current_user with missing Bearer prefix."""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user("invalid-format")

    assert exc_info.value.status_code == 401
    assert "authorization header" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
async def test_get_current_user_expired(expired_token):
    """Test get_current_user with expired token."""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(f"Bearer {expired_token}")

    assert exc_info.value.status_code == 401


# Test get_current_user_optional dependency
@pytest.mark.asyncio
async def test_get_current_user_optional_valid(valid_token):
    """Test optional auth with valid token."""
    user_id = await get_current_user_optional(f"Bearer {valid_token}")

    assert user_id == "test-user-id"


@pytest.mark.asyncio
async def test_get_current_user_optional_no_header():
    """Test optional auth with no header."""
    user_id = await get_current_user_optional(None)

    assert user_id is None


@pytest.mark.asyncio
async def test_get_current_user_optional_invalid_token():
    """Test optional auth with invalid token returns None."""
    user_id = await get_current_user_optional("Bearer invalid-token")

    assert user_id is None


@pytest.mark.asyncio
async def test_get_current_user_optional_expired(expired_token):
    """Test optional auth with expired token returns None."""
    user_id = await get_current_user_optional(f"Bearer {expired_token}")

    assert user_id is None


# Test verify_cron_secret
@pytest.mark.asyncio
async def test_verify_cron_secret_valid():
    """Test cron secret verification with valid secret."""
    # Should not raise exception
    await verify_cron_secret(f"Bearer {settings.CRON_SECRET}")


@pytest.mark.asyncio
async def test_verify_cron_secret_invalid():
    """Test cron secret verification with invalid secret."""
    with pytest.raises(HTTPException) as exc_info:
        await verify_cron_secret("Bearer wrong-secret")

    assert exc_info.value.status_code == 401
    assert "cron secret" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
async def test_verify_cron_secret_missing_bearer():
    """Test cron secret without Bearer prefix."""
    with pytest.raises(HTTPException) as exc_info:
        await verify_cron_secret(settings.CRON_SECRET)

    assert exc_info.value.status_code == 401


# Test verify_webhook_secret
@pytest.mark.asyncio
async def test_verify_webhook_secret_valid():
    """Test webhook secret verification with valid secret."""
    # Should not raise exception
    await verify_webhook_secret(f"Bearer {settings.WEBHOOK_SECRET}")


@pytest.mark.asyncio
async def test_verify_webhook_secret_invalid():
    """Test webhook secret verification with invalid secret."""
    with pytest.raises(HTTPException) as exc_info:
        await verify_webhook_secret("Bearer wrong-secret")

    assert exc_info.value.status_code == 401
    assert "webhook secret" in str(exc_info.value.detail).lower()


# Integration test with FastAPI
@pytest.mark.asyncio
async def test_auth_with_fastapi_route(valid_token):
    """Test auth middleware with FastAPI route."""
    from fastapi import Depends, FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    @app.get("/protected")
    async def protected_route(user_id: str = Depends(get_current_user)):
        return {"user_id": user_id}

    client = TestClient(app)

    # Test with valid token
    response = client.get("/protected", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert response.json()["user_id"] == "test-user-id"

    # Test without token
    response = client.get("/protected")
    assert response.status_code == 403  # FastAPI default for missing auth


@pytest.mark.asyncio
async def test_optional_auth_with_fastapi_route(valid_token):
    """Test optional auth with FastAPI route."""
    from fastapi import Depends, FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    @app.get("/public")
    async def public_route(user_id: str = Depends(get_current_user_optional)):
        return {"user_id": user_id, "authenticated": user_id is not None}

    client = TestClient(app)

    # Test with valid token
    response = client.get("/public", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert response.json()["authenticated"] is True

    # Test without token
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json()["authenticated"] is False


# Edge cases
@pytest.mark.asyncio
async def test_token_with_extra_spaces():
    """Test handling of authorization header with extra spaces."""
    with pytest.raises(HTTPException):
        await get_current_user("Bearer  token-with-extra-spaces")


@pytest.mark.asyncio
async def test_empty_authorization_header():
    """Test handling of empty authorization header."""
    with pytest.raises(HTTPException):
        await get_current_user("")


@pytest.mark.asyncio
async def test_case_sensitive_bearer():
    """Test that Bearer is case-sensitive."""
    with pytest.raises(HTTPException):
        await get_current_user("bearer token")  # lowercase