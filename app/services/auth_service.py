"""
Auth Service - Simple JWT token validation
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, str]:
    """
    Get current user from JWT token.

    For now, returns a mock user.
    In production, validate token with Supabase.
    """
    token = credentials.credentials

    # TODO: Validate token with Supabase
    # For now, return mock user
    return {
        "id": "user_123",  # Replace with actual user ID from token
        "email": "user@example.com"
    }
