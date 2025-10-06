"""
Debug endpoint to test JWT authentication.
"""
import logging
from fastapi import APIRouter, Header, HTTPException
from jose import jwt, JWTError
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/debug/jwt")
async def debug_jwt(authorization: str = Header(None)):
    """
    Debug JWT token verification.
    Returns detailed info about why auth is failing.
    """
    if not authorization:
        return {"error": "No Authorization header provided"}

    if not authorization.startswith("Bearer "):
        return {"error": "Authorization header must start with 'Bearer '"}

    token = authorization.split(" ")[1]

    # Try to decode WITHOUT verification first to see the payload
    try:
        unverified = jwt.get_unverified_claims(token)
        logger.info(f"Unverified JWT payload: {unverified}")
    except Exception as e:
        return {"error": f"Failed to decode token: {str(e)}"}

    # Now try with verification
    try:
        verified = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_signature": True, "verify_exp": True, "verify_aud": False},
        )
        return {
            "success": True,
            "message": "JWT verification successful!",
            "user_id": verified.get("sub"),
            "payload": verified
        }
    except JWTError as e:
        return {
            "error": "JWT verification failed",
            "details": str(e),
            "jwt_algorithm_configured": settings.JWT_ALGORITHM,
            "jwt_secret_length": len(settings.JWT_SECRET) if settings.JWT_SECRET else 0,
            "unverified_payload": unverified
        }
