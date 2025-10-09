"""
Authentication Middleware

Provides JWT token verification and user identity extraction.
"""

import logging
from typing import Optional

from fastapi import Header, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import get_settings

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    Verify JWT token and extract user_id.

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        str: User ID extracted from token

    Raises:
        HTTPException: If token is invalid or expired
    """
    settings = get_settings()
    token = credentials.credentials

    try:
        # Decode and verify JWT
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_aud": False,  # Supabase doesn't always set aud
            },
        )

        # Extract user_id from 'sub' claim
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing 'sub' claim",
            )

        logger.debug(f"Token verified for user: {user_id[:8]}...")
        return user_id

    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
        )


async def get_current_user(
    authorization: str = Header(...)
) -> dict:
    """
    FastAPI dependency for required authentication.

    Args:
        authorization: Authorization header (Bearer <token>)

    Returns:
        dict: User information with 'user_id' and optional 'email'

    Raises:
        HTTPException: 401 if not authenticated
    """
    settings = get_settings()
    logger.info(f"🔐 [Auth] Received authorization header: {authorization[:20]}...")

    if not authorization.startswith("Bearer "):
        logger.warning(f"❌ [Auth] Invalid header format: {authorization[:50]}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )

    token = authorization.split(" ")[1]
    logger.info(f"🔑 [Auth] Extracted token (first 30 chars): {token[:30]}...")
    logger.info(f"📏 [Auth] Token length: {len(token)}")
    logger.info(f"🔧 [Auth] Using JWT_SECRET (first 10 chars): {settings.JWT_SECRET[:10]}...")
    logger.info(f"🔧 [Auth] Using algorithm: {settings.JWT_ALGORITHM}")

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_signature": True, "verify_exp": True, "verify_aud": False},
        )

        user_id = payload.get("sub")
        if not user_id:
            logger.error("❌ [Auth] Token missing 'sub' claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing 'sub' claim",
            )

        logger.info(f"✅ [Auth] Token verified successfully for user: {user_id[:8]}...")
        return {
            "user_id": user_id,
            "email": payload.get("email")
        }

    except JWTError as e:
        logger.error(f"❌ [Auth] JWT verification failed: {type(e).__name__}: {str(e)}")
        logger.error(f"❌ [Auth] Token being verified (first 50 chars): {token[:50]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
        )


async def get_current_user_optional(
    authorization: Optional[str] = Header(None)
) -> Optional[str]:
    """
    FastAPI dependency for optional authentication.

    Args:
        authorization: Optional authorization header

    Returns:
        Optional[str]: User ID if authenticated, None otherwise
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None

    settings = get_settings()
    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_signature": True, "verify_exp": True, "verify_aud": False},
        )

        return payload.get("sub")

    except JWTError:
        # For optional auth, return None on error instead of raising
        return None


async def verify_cron_secret(authorization: str = Header(...)) -> None:
    """
    Verify cron secret for scheduled jobs.

    Args:
        authorization: Authorization header (Bearer <secret>)

    Raises:
        HTTPException: 401 if secret is invalid
    """
    settings = get_settings()
    expected = f"Bearer {settings.CRON_SECRET}"

    if authorization != expected:
        logger.warning("Invalid cron secret attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid cron secret",
        )

    logger.info("Cron secret verified")


async def verify_webhook_secret(authorization: str = Header(...)) -> None:
    """
    Verify webhook secret for external webhooks.

    Args:
        authorization: Authorization header (Bearer <secret>)

    Raises:
        HTTPException: 401 if secret is invalid
    """
    settings = get_settings()
    expected = f"Bearer {settings.WEBHOOK_SECRET}"

    if authorization != expected:
        logger.warning("Invalid webhook secret attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook secret",
        )

    logger.info("Webhook secret verified")
