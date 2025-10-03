"""
Common API Dependencies

Provides reusable FastAPI dependencies for authentication and authorization.
"""

from app.api.middleware.auth import get_current_user, get_current_user_optional

# Re-export auth dependencies for convenience
__all__ = ["get_current_user", "get_current_user_optional"]
