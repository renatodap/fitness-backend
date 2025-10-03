# Feature Design: Supabase Service

## Overview
The Supabase Service provides a centralized, tested interface for all database operations using Supabase. It manages connection pooling, error handling, and provides both service-role and user-scoped database access.

## Purpose
- Centralize all Supabase client instantiation
- Provide connection pooling for better performance
- Support both service-role (admin) and user-scoped access
- Handle database errors consistently
- Enable easy mocking for tests
- Provide type-safe database operations

## Requirements

### Functional Requirements
1. **Service Role Client**: Provide admin client bypassing RLS
2. **User-Scoped Client**: Provide client respecting user's RLS rules
3. **Connection Pooling**: Reuse connections efficiently
4. **Error Handling**: Wrap Supabase errors with context
5. **Lazy Loading**: Create clients only when needed
6. **Thread Safety**: Safe for concurrent access

### Non-Functional Requirements
1. **Performance**: Client creation < 50ms, reuse for subsequent calls
2. **Reliability**: Handle connection failures gracefully
3. **Security**: Never log service role key
4. **Testability**: Easy to mock for unit tests
5. **Maintainability**: Clear separation of concerns

## Architecture

### Client Types

#### 1. Service Role Client
- Uses `SUPABASE_SERVICE_KEY`
- Bypasses Row Level Security (RLS)
- Used for:
  - Background jobs (summarization, embedding generation)
  - Admin operations
  - Cron jobs
  - System-level queries

#### 2. User-Scoped Client
- Uses user's JWT token
- Respects Row Level Security (RLS)
- Used for:
  - User-initiated API requests
  - Operations that should respect user permissions
  - Multi-tenant data access

### Connection Pooling Strategy

```
┌─────────────────────────────────────────┐
│       SupabaseService (Singleton)       │
├─────────────────────────────────────────┤
│  - _service_client: Client (cached)     │
│  - _user_clients: Dict[str, Client]     │
├─────────────────────────────────────────┤
│  + get_service_client() -> Client       │
│  + get_user_client(token) -> Client     │
│  + clear_cache()                        │
└─────────────────────────────────────────┘
```

## Interface Definition

### SupabaseService Class

```python
class SupabaseService:
    """Supabase client management with connection pooling."""

    _instance: Optional["SupabaseService"] = None
    _service_client: Optional[Client] = None
    _user_clients: Dict[str, Client] = {}
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "SupabaseService":
        """Ensure singleton instance."""

    def get_service_client(self) -> Client:
        """Get service role client (bypasses RLS)."""

    def get_user_client(self, access_token: str) -> Client:
        """Get user-scoped client (respects RLS)."""

    def clear_cache(self) -> None:
        """Clear all cached clients (for testing)."""

    def health_check(self) -> bool:
        """Check if Supabase connection is healthy."""
```

### Helper Functions

```python
def get_supabase_service() -> SupabaseService:
    """Get SupabaseService singleton."""

def get_service_client() -> Client:
    """Convenience function to get service role client."""

def get_user_client(access_token: str) -> Client:
    """Convenience function to get user-scoped client."""
```

## Usage Examples

### Service Role Operations (Background Jobs)

```python
from app.services.supabase_service import get_service_client

# In a background job
def generate_summaries():
    client = get_service_client()

    # Bypasses RLS - can access all users' data
    users = client.table("profiles").select("id").execute()

    for user in users.data:
        # Process each user
        pass
```

### User-Scoped Operations (API Endpoints)

```python
from app.services.supabase_service import get_user_client
from fastapi import Depends, Header

async def get_user_workouts(
    authorization: str = Header(...)
):
    # Extract token from "Bearer <token>"
    token = authorization.split(" ")[1]

    client = get_user_client(token)

    # Respects RLS - only gets current user's workouts
    workouts = client.table("workouts").select("*").execute()

    return workouts.data
```

### FastAPI Dependency Injection

```python
from fastapi import Depends
from supabase import Client

async def get_user_db(
    authorization: str = Header(...)
) -> Client:
    """FastAPI dependency for user-scoped database access."""
    token = authorization.split(" ")[1]
    return get_user_client(token)

@app.get("/workouts")
async def list_workouts(db: Client = Depends(get_user_db)):
    result = db.table("workouts").select("*").execute()
    return result.data
```

## Error Handling

### Database Connection Errors

```python
class SupabaseConnectionError(Exception):
    """Raised when cannot connect to Supabase."""

class SupabaseQueryError(Exception):
    """Raised when query fails."""
```

### Error Wrapping

```python
try:
    result = client.table("workouts").select("*").execute()
except Exception as e:
    logger.error(f"Query failed: {e}")
    raise SupabaseQueryError(f"Failed to fetch workouts: {e}") from e
```

## Security Considerations

### 1. Service Role Key Protection
```python
# NEVER log service role key
logger.info("Using service client")  # OK
logger.info(f"Key: {settings.SUPABASE_SERVICE_KEY}")  # NEVER DO THIS
```

### 2. Token Validation
```python
# User tokens should be validated before use
def get_user_client(access_token: str) -> Client:
    if not access_token or len(access_token) < 10:
        raise ValueError("Invalid access token")

    # Create client with token
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY,
        options={"headers": {"Authorization": f"Bearer {access_token}"}}
    )
```

### 3. RLS Enforcement
- Service role client bypasses RLS → use with caution
- Always use user-scoped client for user-initiated operations
- Document which operations use service role

## Performance Optimizations

### 1. Connection Caching
```python
# Service client cached (used frequently)
_service_client: Optional[Client] = None

# User clients cached by token (LRU with max size)
_user_clients: Dict[str, Client] = {}
MAX_USER_CLIENTS = 100
```

### 2. Lazy Loading
```python
def get_service_client(self) -> Client:
    if self._service_client is None:
        with self._lock:
            if self._service_client is None:
                self._service_client = self._create_service_client()
    return self._service_client
```

### 3. Client Cleanup
```python
# Periodically clean up old user clients
def _cleanup_user_clients(self):
    if len(self._user_clients) > MAX_USER_CLIENTS:
        # Remove oldest 20% of clients
        oldest_tokens = list(self._user_clients.keys())[:20]
        for token in oldest_tokens:
            del self._user_clients[token]
```

## Health Check

```python
def health_check(self) -> bool:
    """
    Check if Supabase connection is healthy.

    Returns:
        bool: True if connection is healthy, False otherwise
    """
    try:
        client = self.get_service_client()
        # Simple query to test connection
        result = client.table("profiles").select("id").limit(1).execute()
        return True
    except Exception as e:
        logger.error(f"Supabase health check failed: {e}")
        return False
```

## Testing Strategy

### Unit Tests
1. Test service role client creation
2. Test user-scoped client creation
3. Test connection caching/reuse
4. Test singleton pattern
5. Test error handling
6. Test health check

### Integration Tests
1. Test actual database queries
2. Test RLS enforcement
3. Test concurrent access
4. Test connection pooling under load

### Mocking for Other Services
```python
@pytest.fixture
def mock_supabase_service(mocker):
    """Mock SupabaseService for testing other services."""
    mock_client = mocker.Mock()
    mock_client.table().select().execute.return_value = mocker.Mock(
        data=[{"id": "test-id"}]
    )

    mock_service = mocker.Mock()
    mock_service.get_service_client.return_value = mock_client

    return mock_service
```

## Migration from Direct Usage

### Before (Direct Supabase Import)
```python
from supabase import create_client

client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY
)
```

### After (Using SupabaseService)
```python
from app.services.supabase_service import get_service_client

client = get_service_client()
```

## Thread Safety

```python
import threading

class SupabaseService:
    _lock: threading.Lock = threading.Lock()

    def get_service_client(self) -> Client:
        if self._service_client is None:
            with self._lock:
                # Double-check locking pattern
                if self._service_client is None:
                    self._service_client = self._create_service_client()
        return self._service_client
```

## Configuration

All configuration comes from `app.config.Settings`:
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase anon key
- `SUPABASE_SERVICE_KEY`: Supabase service role key

## Success Criteria

✅ Service role client cached and reused
✅ User-scoped clients cached per token
✅ Thread-safe singleton implementation
✅ Health check endpoint works
✅ All errors wrapped with context
✅ Easy to mock in tests
✅ 80%+ test coverage
✅ No service key in logs

## Dependencies

- `supabase-py`: Official Supabase Python client
- `app.config`: Configuration management

## Future Enhancements

1. **Connection Pool Size Limits**: Configurable max connections
2. **Metrics**: Track client creation, query times, error rates
3. **Query Retry Logic**: Automatic retry on transient failures
4. **Read Replicas**: Support for read-only replicas
5. **Query Logging**: Optional query logging for debugging
6. **Connection Health Monitoring**: Periodic health checks

## References

- [Supabase Python Client Documentation](https://supabase.com/docs/reference/python/introduction)
- [Row Level Security (RLS)](https://supabase.com/docs/guides/auth/row-level-security)
- [Connection Pooling Best Practices](https://supabase.com/docs/guides/database/connecting-to-postgres)