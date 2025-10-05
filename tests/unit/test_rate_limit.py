"""
Unit Tests for Rate Limiting

Tests the Redis-based rate limiting middleware.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException

from app.api.middleware.rate_limit import (
    RateLimiter,
    get_rate_limiter,
    rate_limit,
)


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    redis_mock = AsyncMock()
    redis_mock.pipeline.return_value.execute = AsyncMock(return_value=[None, 0, None, None])
    return redis_mock


@pytest.mark.asyncio
class TestRateLimiter:
    """Test RateLimiter class."""

    async def test_check_rate_limit_allowed(self, mock_redis):
        """Test rate limit check when request is allowed."""
        limiter = RateLimiter()
        limiter._redis = mock_redis

        # Mock Redis responses: [remove_result, count_before=0, add_result, expire_result]
        mock_redis.pipeline.return_value.execute = AsyncMock(
            return_value=[None, 0, None, None]
        )

        is_allowed, remaining, retry_after = await limiter.check_rate_limit(
            key="test:user123",
            max_requests=10,
            window_seconds=60
        )

        assert is_allowed is True
        assert remaining == 9  # 10 - 0 - 1
        assert retry_after == 0

    async def test_check_rate_limit_exceeded(self, mock_redis):
        """Test rate limit check when limit is exceeded."""
        limiter = RateLimiter()
        limiter._redis = mock_redis

        # Mock Redis responses: count_before=10 (at limit)
        mock_redis.pipeline.return_value.execute = AsyncMock(
            return_value=[None, 10, None, None]
        )

        is_allowed, remaining, retry_after = await limiter.check_rate_limit(
            key="test:user123",
            max_requests=10,
            window_seconds=60
        )

        assert is_allowed is False
        assert remaining == 0
        assert retry_after == 60

    async def test_check_rate_limit_redis_failure(self, mock_redis):
        """Test rate limit check when Redis fails (should allow request)."""
        limiter = RateLimiter()
        limiter._redis = mock_redis

        # Mock Redis failure
        mock_redis.pipeline.side_effect = Exception("Redis connection failed")

        is_allowed, remaining, retry_after = await limiter.check_rate_limit(
            key="test:user123",
            max_requests=10,
            window_seconds=60
        )

        # Should allow request when Redis fails (fail open)
        assert is_allowed is True
        assert remaining == 10
        assert retry_after == 0


@pytest.mark.asyncio
class TestRateLimitDecorator:
    """Test rate_limit decorator."""

    async def test_rate_limit_decorator_with_user(self):
        """Test rate limit decorator with authenticated user."""
        # Mock the rate limiter
        with patch('app.api.middleware.rate_limit.get_rate_limiter') as mock_get_limiter:
            mock_limiter = AsyncMock()
            mock_limiter.check_rate_limit = AsyncMock(
                return_value=(True, 99, 0)  # allowed, 99 remaining, 0 retry_after
            )
            mock_get_limiter.return_value = mock_limiter

            # Create a test endpoint
            @rate_limit(max_requests=100, window_seconds=86400, key_prefix="test")
            async def test_endpoint(current_user: dict):
                return {"message": "success"}

            # Call with user context
            user = {"user_id": "user123"}
            result = await test_endpoint(current_user=user)

            assert result == {"message": "success"}
            mock_limiter.check_rate_limit.assert_called_once()

    async def test_rate_limit_decorator_rate_exceeded(self):
        """Test rate limit decorator when rate limit exceeded."""
        # Mock the rate limiter
        with patch('app.api.middleware.rate_limit.get_rate_limiter') as mock_get_limiter:
            mock_limiter = AsyncMock()
            mock_limiter.check_rate_limit = AsyncMock(
                return_value=(False, 0, 3600)  # not allowed, 0 remaining, retry in 3600s
            )
            mock_get_limiter.return_value = mock_limiter

            # Create a test endpoint
            @rate_limit(max_requests=100, window_seconds=86400, key_prefix="test")
            async def test_endpoint(current_user: dict):
                return {"message": "success"}

            # Call with user context
            user = {"user_id": "user123"}

            with pytest.raises(HTTPException) as exc_info:
                await test_endpoint(current_user=user)

            assert exc_info.value.status_code == 429
            assert "Rate limit exceeded" in str(exc_info.value.detail)

    async def test_rate_limit_decorator_no_user(self):
        """Test rate limit decorator without user (should skip rate limiting)."""
        # Create a test endpoint
        @rate_limit(max_requests=100, window_seconds=86400, key_prefix="test")
        async def test_endpoint(current_user: dict = None):
            return {"message": "success"}

        # Call without user context
        result = await test_endpoint(current_user=None)

        # Should succeed without rate limiting
        assert result == {"message": "success"}


def test_get_rate_limiter():
    """Test get_rate_limiter returns singleton."""
    limiter1 = get_rate_limiter()
    limiter2 = get_rate_limiter()

    assert limiter1 is limiter2  # Same instance


@pytest.mark.asyncio
async def test_rate_limiter_close():
    """Test rate limiter close."""
    limiter = RateLimiter()
    mock_redis = AsyncMock()
    limiter._redis = mock_redis

    await limiter.close()

    mock_redis.close.assert_called_once()
