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

    For now, returns a mock user with valid UUID.
    In production, validate token with Supabase.
    """
    token = credentials.credentials

    # TODO: Validate token with Supabase
    # For now, return mock user with valid UUID (Supabase users table requires UUID)
    return {
        "id": "00000000-0000-0000-0000-000000000001",  # Valid UUID for testing
        "email": "user@example.com"
    }
