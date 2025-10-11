"""
Rate Limiting Middleware

Implements rate limiting for API endpoints to prevent abuse and manage costs.
Uses Redis for distributed rate limiting across multiple instances.
"""

import time
from typing import Callable, Optional
from functools import wraps

from fastapi import HTTPException, Request, status
import redis.asyncio as redis
import structlog

from app.config import get_settings

logger = structlog.get_logger(__name__)


class RateLimiter:
    """
    Redis-based rate limiter with sliding window algorithm.

    Supports per-user and per-endpoint rate limiting with configurable
    time windows and request limits.
    """

    def __init__(self, redis_url: str = None):
        """
        Initialize rate limiter with Redis connection.

        Args:
            redis_url: Redis connection URL (defaults to settings.REDIS_URL)
        """
        settings = get_settings()
        self.redis_url = redis_url or settings.REDIS_URL
        self._redis: Optional[redis.Redis] = None

    async def get_redis(self) -> redis.Redis:
        """Get or create Redis connection."""
        if self._redis is None:
            self._redis = await redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
        return self._redis

    async def check_rate_limit(
        self,
        key: str,
        max_requests: int,
        window_seconds: int
    ) -> tuple[bool, int, int]:
        """
        Check if request is within rate limit using sliding window.

        Args:
            key: Unique identifier for rate limit (e.g., user_id:endpoint)
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds

        Returns:
            Tuple of (is_allowed, requests_remaining, retry_after_seconds)
        """
        try:
            r = await self.get_redis()
            now = time.time()
            window_start = now - window_seconds

            # Use Redis sorted set with timestamps as scores
            pipe = r.pipeline()

            # Remove old entries outside the window
            pipe.zremrangebyscore(key, 0, window_start)

            # Count requests in current window
            pipe.zcard(key)

            # Add current request
            pipe.zadd(key, {str(now): now})

            # Set expiry on the key
            pipe.expire(key, window_seconds)

            results = await pipe.execute()
            request_count = results[1]  # Count before adding current request

            if request_count >= max_requests:
                # Rate limit exceeded
                retry_after = int(window_seconds)
                return False, 0, retry_after

            # Within rate limit
            requests_remaining = max_requests - request_count - 1
            return True, requests_remaining, 0

        except Exception as e:
            # If Redis fails, allow the request but log error
            logger.error("Rate limit check failed", error=str(e), key=key)
            return True, max_requests, 0

    async def close(self):
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()


# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


async def rate_limit_middleware(request: Request, call_next: Callable):
    """
    Middleware to apply rate limiting to all requests.

    Checks rate limits and adds headers to response.
    """
    # Skip rate limiting for health checks and docs
    if request.url.path in ["/", "/health", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)

    response = await call_next(request)
    return response


def rate_limit(
    max_requests: int,
    window_seconds: int,
    key_prefix: str = "api"
):
    """
    Decorator to apply rate limiting to specific endpoints.

    Usage:
        @router.post("/chat")
        @rate_limit(max_requests=100, window_seconds=86400, key_prefix="coach_chat")
        async def coach_chat(request: ChatRequest, user: dict = Depends(get_current_user)):
            ...

    Args:
        max_requests: Maximum requests allowed in time window
        window_seconds: Time window in seconds
        key_prefix: Prefix for rate limit key (endpoint identifier)

    Returns:
        Decorator function
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract user from kwargs (injected by get_current_user dependency)
            user = kwargs.get('current_user') or kwargs.get('user')

            if not user:
                # No user context, skip rate limiting (for public endpoints)
                return await func(*args, **kwargs)

            # Try multiple possible user ID fields
            user_id = user.get('id') or user.get('user_id') or user.get('sub')
            if not user_id:
                logger.warning("Rate limit: No user_id found in user context", user_keys=list(user.keys()))
                return await func(*args, **kwargs)

            # Create rate limit key: prefix:user_id
            rate_limit_key = f"{key_prefix}:{user_id}"

            # Check rate limit
            limiter = get_rate_limiter()
            is_allowed, remaining, retry_after = await limiter.check_rate_limit(
                key=rate_limit_key,
                max_requests=max_requests,
                window_seconds=window_seconds
            )

            if not is_allowed:
                logger.warning(
                    "Rate limit exceeded",
                    user_id=user_id,
                    endpoint=key_prefix,
                    max_requests=max_requests,
                    window_seconds=window_seconds
                )

                # Return rate limit error
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"You have exceeded the rate limit of {max_requests} requests per {window_seconds // 3600} hour(s). Please try again later.",
                        "retry_after": retry_after,
                        "limit": max_requests,
                        "window": window_seconds
                    }
                )

            # Log rate limit check
            logger.info(
                "Rate limit check",
                user_id=user_id,
                endpoint=key_prefix,
                remaining=remaining,
                limit=max_requests
            )

            # Execute the endpoint function
            result = await func(*args, **kwargs)

            # Add rate limit headers to response if it's a Response object
            if hasattr(result, 'headers'):
                result.headers['X-RateLimit-Limit'] = str(max_requests)
                result.headers['X-RateLimit-Remaining'] = str(remaining)
                result.headers['X-RateLimit-Reset'] = str(int(time.time()) + window_seconds)

            return result

        return wrapper
    return decorator


# Predefined rate limiters for common use cases
def coach_chat_rate_limit():
    """Rate limit for coach chat: 100 messages per day."""
    return rate_limit(
        max_requests=100,
        window_seconds=86400,  # 24 hours
        key_prefix="coach_chat"
    )


def quick_entry_rate_limit():
    """Rate limit for quick entry: 200 entries per day."""
    return rate_limit(
        max_requests=200,
        window_seconds=86400,  # 24 hours
        key_prefix="quick_entry"
    )


def program_generation_rate_limit():
    """Rate limit for program generation: 5 programs per month."""
    return rate_limit(
        max_requests=5,
        window_seconds=2592000,  # 30 days
        key_prefix="program_generation"
    )


def ai_api_rate_limit():
    """Rate limit for general AI API calls: 500 per day."""
    return rate_limit(
        max_requests=500,
        window_seconds=86400,  # 24 hours
        key_prefix="ai_api"
    )
