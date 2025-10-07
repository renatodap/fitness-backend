"""
Auth Service - Supabase JWT token validation
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict
from app.services.supabase_service import get_service_client
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, str]:
    """
    Get current user from Supabase JWT token.

    Validates the token and returns user info.
    Raises 401 if token is invalid.
    """
    token = credentials.credentials

    try:
        # Validate token with Supabase
        supabase = get_service_client()

        # Get user from token
        user_response = supabase.auth.get_user(token)

        if not user_response or not user_response.user:
            logger.error("Invalid token: no user found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        user = user_response.user

        logger.info(f"Authenticated user: {user.id}")

        return {
            "id": user.id,
            "email": user.email
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
