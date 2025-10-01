# Feature Design: Authentication Middleware

## Overview
The Authentication Middleware provides JWT token verification and user identity extraction for the FastAPI backend. It validates Supabase JWT tokens and makes user information available to route handlers.

## Purpose
- Verify JWT tokens from Supabase Auth
- Extract user_id from validated tokens
- Provide FastAPI dependencies for protected routes
- Support both required and optional authentication
- Handle authentication errors consistently
- Enable easy testing with mock authentication

## Requirements

### Functional Requirements
1. **JWT Verification**: Validate Supabase JWT tokens
2. **User Extraction**: Extract user_id and claims from token
3. **FastAPI Integration**: Provide dependency injection for routes
4. **Optional Auth**: Support routes with optional authentication
5. **Error Handling**: Return appropriate HTTP errors for auth failures
6. **Secret Validation**: Support multiple auth secrets (cron, webhook)

### Non-Functional Requirements
1. **Performance**: Token verification < 10ms
2. **Security**: Validate signature, expiration, issuer
3. **Reliability**: Graceful degradation on auth service issues
4. **Testability**: Easy to mock for unit tests
5. **Maintainability**: Clear error messages

## Architecture

### Authentication Flow

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ Authorization: Bearer <token>
       ↓
┌─────────────────────────────────┐
│   FastAPI Middleware            │
│   ├─ Extract Token              │
│   ├─ Verify JWT                 │
│   ├─ Extract user_id            │
│   └─ Inject into request        │
└──────┬──────────────────────────┘
       │ user_id available
       ↓
┌─────────────────────────────────┐
│   Route Handler                 │
│   (has access to user_id)       │
└─────────────────────────────────┘
```

### Components

1. **verify_token()**: Core JWT verification function
2. **get_current_user()**: FastAPI dependency (required auth)
3. **get_current_user_optional()**: FastAPI dependency (optional auth)
4. **verify_cron_secret()**: Dependency for cron endpoints
5. **verify_webhook_secret()**: Dependency for webhook endpoints

## Interface Definition

### Core Function

```python
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
```

### FastAPI Dependencies

```python
async def get_current_user(
    authorization: str = Header(...)
) -> str:
    """
    FastAPI dependency for required authentication.

    Returns:
        str: User ID

    Raises:
        HTTPException: 401 if not authenticated
    """

async def get_current_user_optional(
    authorization: Optional[str] = Header(None)
) -> Optional[str]:
    """
    FastAPI dependency for optional authentication.

    Returns:
        Optional[str]: User ID if authenticated, None otherwise
    """

async def verify_cron_secret(
    authorization: str = Header(...)
) -> None:
    """
    Verify cron secret for scheduled jobs.

    Raises:
        HTTPException: 401 if secret is invalid
    """

async def verify_webhook_secret(
    authorization: str = Header(...)
) -> None:
    """
    Verify webhook secret for external webhooks.

    Raises:
        HTTPException: 401 if secret is invalid
    """
```

### Token Claims

```python
class TokenClaims(BaseModel):
    """JWT token claims."""
    sub: str  # user_id
    aud: str  # audience
    exp: int  # expiration timestamp
    iat: int  # issued at timestamp
    iss: str  # issuer
    email: Optional[str] = None
    role: Optional[str] = None
```

## Usage Examples

### Protected Route (Required Auth)

```python
from fastapi import APIRouter, Depends
from app.api.middleware.auth import get_current_user

router = APIRouter()

@router.get("/workouts")
async def list_workouts(user_id: str = Depends(get_current_user)):
    """List workouts for authenticated user."""
    # user_id is guaranteed to be present
    return {"user_id": user_id, "workouts": []}
```

### Optional Auth Route

```python
@router.get("/public-data")
async def get_public_data(
    user_id: Optional[str] = Depends(get_current_user_optional)
):
    """Get data, personalized if authenticated."""
    if user_id:
        # Return personalized data
        return {"personalized": True, "user_id": user_id}
    else:
        # Return public data
        return {"personalized": False}
```

### Cron Job Endpoint

```python
from app.api.middleware.auth import verify_cron_secret

@router.post("/background/summarize")
async def run_summarization(_: None = Depends(verify_cron_secret)):
    """Run daily summarization (requires cron secret)."""
    # Secret verified, proceed with job
    return {"status": "started"}
```

### Webhook Endpoint

```python
from app.api.middleware.auth import verify_webhook_secret

@router.post("/webhooks/strava")
async def strava_webhook(_: None = Depends(verify_webhook_secret)):
    """Handle Strava webhook (requires webhook secret)."""
    # Secret verified, process webhook
    return {"status": "received"}
```

## Token Verification

### JWT Validation Steps

1. **Extract Token**: Get token from Authorization header
2. **Decode Header**: Extract algorithm and key ID
3. **Verify Signature**: Validate JWT signature with Supabase JWT secret
4. **Check Expiration**: Ensure token not expired
5. **Validate Issuer**: Check token issued by Supabase
6. **Extract Claims**: Get user_id and other claims

### Example Implementation

```python
from jose import jwt, JWTError
from app.config import settings

def verify_token(token: str) -> str:
    """Verify JWT token and extract user_id."""
    try:
        # Decode and verify token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_aud": False,  # Supabase doesn't always set aud
            }
        )

        # Extract user_id
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token missing 'sub' claim")

        return user_id

    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}"
        )
```

## Error Handling

### Authentication Errors

```python
# Missing Authorization header
401 Unauthorized
{
    "detail": "Not authenticated"
}

# Invalid token format
401 Unauthorized
{
    "detail": "Invalid authentication credentials: Invalid token"
}

# Expired token
401 Unauthorized
{
    "detail": "Invalid authentication credentials: Token has expired"
}

# Invalid signature
401 Unauthorized
{
    "detail": "Invalid authentication credentials: Signature verification failed"
}
```

### Error Types

```python
class AuthenticationError(Exception):
    """Base authentication error."""

class TokenExpiredError(AuthenticationError):
    """Token has expired."""

class TokenInvalidError(AuthenticationError):
    """Token is invalid."""

class TokenMissingError(AuthenticationError):
    """Token is missing."""
```

## Security Considerations

### 1. Secret Management
```python
# NEVER log JWT secret
logger.info("Verifying token")  # OK
logger.info(f"Secret: {settings.JWT_SECRET}")  # NEVER

# Rotate secrets regularly
# Update JWT_SECRET quarterly
```

### 2. Token Expiration
```python
# Always verify expiration
options = {
    "verify_exp": True,  # Must be True
    "verify_signature": True,  # Must be True
}
```

### 3. Secure Headers
```python
# Use Security from fastapi.security
from fastapi.security import HTTPBearer

security = HTTPBearer()

# Automatically extracts Bearer token
# Returns 401 if header missing or malformed
```

### 4. Rate Limiting
```python
# Consider rate limiting auth endpoints
# Prevent brute force attacks
@router.post("/login")
@rate_limit(max_requests=5, window=60)
async def login():
    pass
```

## Performance Optimizations

### 1. Token Caching (Optional)
```python
# Cache verified tokens for short period
# Reduces JWT decoding overhead

from functools import lru_cache

@lru_cache(maxsize=1000)
def _verify_token_cached(token: str, exp: int) -> str:
    """Cache token verification until expiration."""
    return verify_token(token)
```

### 2. Async JWT Verification
```python
# Use async JWT library if available
# Or run CPU-bound verification in thread pool

import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def verify_token_async(token: str) -> str:
    """Async token verification."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, verify_token_sync, token)
```

## Testing Strategy

### Unit Tests
1. Test valid token verification
2. Test expired token rejection
3. Test invalid signature rejection
4. Test missing token handling
5. Test malformed token handling
6. Test secret verification (cron, webhook)
7. Test optional auth dependency

### Integration Tests
1. Test with real Supabase tokens (staging)
2. Test FastAPI route protection
3. Test error responses
4. Test multiple concurrent requests

### Test Fixtures

```python
@pytest.fixture
def mock_token():
    """Generate mock JWT token for testing."""
    from jose import jwt
    from datetime import datetime, timedelta

    payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "iss": "https://test.supabase.co/auth/v1"
    }

    return jwt.encode(payload, "test-secret", algorithm="HS256")

@pytest.fixture
def mock_expired_token():
    """Generate expired mock JWT token."""
    payload = {
        "sub": "test-user-id",
        "exp": datetime.utcnow() - timedelta(hours=1),  # Expired
        "iat": datetime.utcnow() - timedelta(hours=2),
    }

    return jwt.encode(payload, "test-secret", algorithm="HS256")
```

## Supabase JWT Structure

### Example Token Claims

```json
{
  "aud": "authenticated",
  "exp": 1735574400,
  "iat": 1735570800,
  "iss": "https://your-project.supabase.co/auth/v1",
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "phone": "",
  "app_metadata": {
    "provider": "email",
    "providers": ["email"]
  },
  "user_metadata": {
    "name": "John Doe"
  },
  "role": "authenticated",
  "aal": "aal1",
  "amr": [
    {
      "method": "password",
      "timestamp": 1735570800
    }
  ],
  "session_id": "abc123-def456"
}
```

### Key Claims

- `sub`: User ID (UUID)
- `email`: User's email address
- `exp`: Expiration timestamp (Unix)
- `iss`: Issuer (Supabase Auth URL)
- `role`: User role (authenticated, anon, service_role)

## Success Criteria

✅ Valid tokens verified correctly
✅ Invalid tokens rejected with 401
✅ Expired tokens rejected
✅ FastAPI dependencies work correctly
✅ Optional auth supports unauthenticated requests
✅ Cron/webhook secrets verified
✅ Clear error messages for all failure cases
✅ 80%+ test coverage
✅ Performance < 10ms per verification

## Dependencies

- `python-jose[cryptography]`: JWT encoding/decoding
- `fastapi.security`: HTTP Bearer security
- `app.config`: Configuration management

## Future Enhancements

1. **Token Refresh**: Support refreshing expired tokens
2. **Scope-Based Access**: Check token scopes/permissions
3. **Multi-Tenant Support**: Extract tenant ID from token
4. **API Key Authentication**: Support API keys alongside JWT
5. **OAuth Integration**: Support OAuth providers (Google, GitHub)
6. **Audit Logging**: Log all authentication attempts
7. **Anomaly Detection**: Detect suspicious auth patterns

## References

- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [JWT Best Practices](https://datatracker.ietf.org/doc/html/rfc8725)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [python-jose Documentation](https://python-jose.readthedocs.io/)