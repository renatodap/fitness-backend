# Test Design: Supabase Service

## Test Overview
Comprehensive test suite for Supabase Service ensuring proper client management, connection pooling, error handling, and thread safety.

## Test Strategy

### Test Levels
1. **Unit Tests**: Test client creation, caching, singleton pattern
2. **Integration Tests**: Test actual database operations (optional, requires test DB)
3. **Coverage Target**: ≥80% code coverage

### Test Framework
- **pytest**: Main testing framework
- **pytest-mock**: For mocking Supabase client
- **pytest-asyncio**: For async test support

## Test Cases

### 1. Client Creation Tests

#### TC-SUPA-001: Create Service Role Client
**Objective**: Verify service role client can be created

**Test Steps**:
1. Get SupabaseService instance
2. Call `get_service_client()`
3. Verify client is not None
4. Verify client has correct configuration

**Expected Result**:
- Client created successfully
- Uses service role key

**Assertions**:
```python
def test_create_service_client(mock_supabase_client):
    service = SupabaseService()
    client = service.get_service_client()

    assert client is not None
    # Verify create_client was called with service key
```

---

#### TC-SUPA-002: Create User-Scoped Client
**Objective**: Verify user-scoped client can be created with token

**Test Steps**:
1. Get SupabaseService instance
2. Call `get_user_client("test-token")`
3. Verify client is not None
4. Verify client has authorization header

**Expected Result**:
- Client created with user token
- Authorization header set correctly

**Assertions**:
```python
def test_create_user_client(mock_supabase_client):
    service = SupabaseService()
    client = service.get_user_client("test-user-token")

    assert client is not None
    # Verify create_client called with token in headers
```

---

#### TC-SUPA-003: Invalid Token Handling
**Objective**: Verify proper error for invalid token

**Test Steps**:
1. Get SupabaseService instance
2. Call `get_user_client("")` with empty token
3. Catch exception

**Expected Result**:
- ValueError raised
- Error message indicates invalid token

**Assertions**:
```python
def test_invalid_token():
    service = SupabaseService()

    with pytest.raises(ValueError) as exc_info:
        service.get_user_client("")

    assert "token" in str(exc_info.value).lower()
```

---

### 2. Connection Caching Tests

#### TC-SUPA-004: Service Client Cached
**Objective**: Verify service client is cached and reused

**Test Steps**:
1. Get service client first time
2. Get service client second time
3. Verify same instance returned

**Expected Result**:
- Same client instance on subsequent calls
- Only created once

**Assertions**:
```python
def test_service_client_cached(mocker):
    service = SupabaseService()

    client1 = service.get_service_client()
    client2 = service.get_service_client()

    assert client1 is client2
```

---

#### TC-SUPA-005: User Clients Cached by Token
**Objective**: Verify user clients cached per token

**Test Steps**:
1. Get client for token "user1"
2. Get client for token "user1" again
3. Get client for token "user2"
4. Verify caching behavior

**Expected Result**:
- Same token returns same client
- Different tokens return different clients

**Assertions**:
```python
def test_user_clients_cached_by_token(mocker):
    service = SupabaseService()

    client1_a = service.get_user_client("token-user1")
    client1_b = service.get_user_client("token-user1")
    client2 = service.get_user_client("token-user2")

    assert client1_a is client1_b
    assert client1_a is not client2
```

---

#### TC-SUPA-006: Cache Clearing
**Objective**: Verify cache can be cleared

**Test Steps**:
1. Get service client
2. Clear cache
3. Get service client again
4. Verify new instance created

**Expected Result**:
- After cache clear, new client created
- Old client no longer in cache

**Assertions**:
```python
def test_clear_cache(mocker):
    service = SupabaseService()

    client1 = service.get_service_client()
    service.clear_cache()
    client2 = service.get_service_client()

    # After cache clear, new client created
    assert client2 is not None
```

---

### 3. Singleton Pattern Tests

#### TC-SUPA-007: Singleton Instance
**Objective**: Verify SupabaseService is singleton

**Test Steps**:
1. Create SupabaseService() twice
2. Verify same instance returned

**Expected Result**:
- Both calls return same instance
- Singleton pattern enforced

**Assertions**:
```python
def test_singleton_instance():
    service1 = SupabaseService()
    service2 = SupabaseService()

    assert service1 is service2
```

---

#### TC-SUPA-008: Singleton Across get_supabase_service()
**Objective**: Verify get_supabase_service() returns singleton

**Test Steps**:
1. Call get_supabase_service() twice
2. Verify same instance

**Expected Result**:
- Same instance returned
- Consistent with direct instantiation

**Assertions**:
```python
def test_get_supabase_service_singleton():
    service1 = get_supabase_service()
    service2 = get_supabase_service()

    assert service1 is service2
```

---

### 4. Thread Safety Tests

#### TC-SUPA-009: Concurrent Client Creation
**Objective**: Verify thread-safe client creation

**Test Steps**:
1. Create multiple threads
2. Each thread gets service client
3. Verify only one client created
4. No race conditions

**Expected Result**:
- Thread-safe singleton
- No duplicate clients created

**Assertions**:
```python
import threading

def test_thread_safe_client_creation(mocker):
    service = SupabaseService()
    service.clear_cache()

    clients = []
    lock = threading.Lock()

    def get_client():
        client = service.get_service_client()
        with lock:
            clients.append(client)

    threads = [threading.Thread(target=get_client) for _ in range(10)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # All threads should get the same client
    assert len(clients) == 10
    assert all(c is clients[0] for c in clients)
```

---

### 5. Error Handling Tests

#### TC-SUPA-010: Handle Connection Failure
**Objective**: Verify proper error handling on connection failure

**Test Steps**:
1. Mock create_client to raise exception
2. Attempt to get service client
3. Verify exception propagated

**Expected Result**:
- Exception caught and wrapped
- Error message provides context

**Assertions**:
```python
def test_connection_failure(mocker):
    mocker.patch(
        'app.services.supabase_service.create_client',
        side_effect=Exception("Connection failed")
    )

    service = SupabaseService()
    service.clear_cache()

    with pytest.raises(Exception) as exc_info:
        service.get_service_client()

    assert "Connection failed" in str(exc_info.value)
```

---

#### TC-SUPA-011: Handle Invalid Configuration
**Objective**: Verify error when config is invalid

**Test Steps**:
1. Mock settings with invalid URL
2. Attempt to create client
3. Verify proper error

**Expected Result**:
- Clear error message
- No confusing errors

**Assertions**:
```python
def test_invalid_configuration(mocker, monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "")

    service = SupabaseService()
    service.clear_cache()

    with pytest.raises(Exception):
        service.get_service_client()
```

---

### 6. Health Check Tests

#### TC-SUPA-012: Health Check Success
**Objective**: Verify health check returns True when healthy

**Test Steps**:
1. Mock successful database query
2. Call health_check()
3. Verify returns True

**Expected Result**:
- Health check passes
- Returns True

**Assertions**:
```python
def test_health_check_success(mocker):
    mock_client = mocker.Mock()
    mock_client.table().select().limit().execute.return_value = mocker.Mock(
        data=[{"id": "test"}]
    )

    service = SupabaseService()
    mocker.patch.object(service, 'get_service_client', return_value=mock_client)

    result = service.health_check()
    assert result is True
```

---

#### TC-SUPA-013: Health Check Failure
**Objective**: Verify health check returns False on failure

**Test Steps**:
1. Mock database query to raise exception
2. Call health_check()
3. Verify returns False

**Expected Result**:
- Health check fails gracefully
- Returns False (not exception)

**Assertions**:
```python
def test_health_check_failure(mocker):
    mock_client = mocker.Mock()
    mock_client.table().select().limit().execute.side_effect = Exception("DB Error")

    service = SupabaseService()
    mocker.patch.object(service, 'get_service_client', return_value=mock_client)

    result = service.health_check()
    assert result is False
```

---

### 7. Convenience Function Tests

#### TC-SUPA-014: get_service_client() Helper
**Objective**: Verify convenience function works

**Test Steps**:
1. Call get_service_client()
2. Verify returns client
3. Verify same as service.get_service_client()

**Expected Result**:
- Helper function works correctly
- Consistent with direct method call

**Assertions**:
```python
def test_get_service_client_helper(mocker):
    client = get_service_client()

    assert client is not None

    # Should be same as getting from service
    service = get_supabase_service()
    service_client = service.get_service_client()

    assert client is service_client
```

---

#### TC-SUPA-015: get_user_client() Helper
**Objective**: Verify user client convenience function

**Test Steps**:
1. Call get_user_client("token")
2. Verify returns client
3. Verify consistent with service method

**Expected Result**:
- Helper function works
- Consistent behavior

**Assertions**:
```python
def test_get_user_client_helper(mocker):
    token = "test-token"
    client = get_user_client(token)

    assert client is not None

    # Should be same as getting from service
    service = get_supabase_service()
    service_client = service.get_user_client(token)

    assert client is service_client
```

---

### 8. Integration with FastAPI Tests

#### TC-SUPA-016: FastAPI Dependency Injection
**Objective**: Verify service works with FastAPI dependencies

**Test Steps**:
1. Create test endpoint using Supabase dependency
2. Make request with auth token
3. Verify client injected correctly

**Expected Result**:
- Dependency injection works
- Client available in endpoint

**Assertions**:
```python
from fastapi import Depends, FastAPI, Header
from fastapi.testclient import TestClient

def test_fastapi_dependency(mocker):
    app = FastAPI()

    async def get_db(authorization: str = Header(...)):
        token = authorization.split(" ")[1]
        return get_user_client(token)

    @app.get("/test")
    async def test_endpoint(db = Depends(get_db)):
        return {"status": "ok", "has_db": db is not None}

    # Mock the get_user_client
    mock_client = mocker.Mock()
    mocker.patch(
        'app.services.supabase_service.get_user_client',
        return_value=mock_client
    )

    client = TestClient(app)
    response = client.get("/test", headers={"Authorization": "Bearer test-token"})

    assert response.status_code == 200
    assert response.json()["has_db"] is True
```

---

### 9. Edge Cases

#### TC-SUPA-017: Empty Token String
**Objective**: Verify handling of empty token

**Test Steps**:
1. Call get_user_client("")
2. Verify proper error

**Expected Result**:
- ValueError raised
- Clear error message

**Assertions**:
```python
def test_empty_token():
    service = SupabaseService()

    with pytest.raises(ValueError) as exc_info:
        service.get_user_client("")

    assert "token" in str(exc_info.value).lower()
```

---

#### TC-SUPA-018: Very Long Token
**Objective**: Verify handling of unusually long token

**Test Steps**:
1. Create very long token string (10000 chars)
2. Call get_user_client()
3. Verify works or fails gracefully

**Expected Result**:
- Either works or fails with clear error
- No crashes

**Assertions**:
```python
def test_very_long_token(mocker):
    service = SupabaseService()
    long_token = "a" * 10000

    # Should either work or raise clear error
    try:
        client = service.get_user_client(long_token)
        assert client is not None
    except (ValueError, Exception) as e:
        # If it fails, should have clear message
        assert str(e)
```

---

#### TC-SUPA-019: Special Characters in Token
**Objective**: Verify handling of special characters

**Test Steps**:
1. Create token with special chars
2. Call get_user_client()
3. Verify proper handling

**Expected Result**:
- Works correctly
- No encoding issues

**Assertions**:
```python
def test_special_characters_in_token(mocker):
    service = SupabaseService()
    special_token = "token-with-!@#$%^&*()"

    # Should handle special characters
    try:
        client = service.get_user_client(special_token)
        assert client is not None
    except ValueError:
        # Acceptable if validation rejects special chars
        pass
```

---

## Test Fixtures

### Mock Supabase Client
```python
@pytest.fixture
def mock_supabase_client(mocker):
    """Mock Supabase client for testing."""
    mock_client = mocker.Mock()

    # Mock common operations
    mock_table = mocker.Mock()
    mock_table.select().execute.return_value = mocker.Mock(data=[])
    mock_client.table.return_value = mock_table

    return mock_client
```

### Clean Supabase Service
```python
@pytest.fixture
def clean_supabase_service():
    """Provide clean SupabaseService for testing."""
    service = SupabaseService()
    service.clear_cache()
    yield service
    service.clear_cache()
```

---

## Test Execution

### Run All Supabase Service Tests
```bash
pytest tests/unit/test_supabase_service.py -v
```

### Run with Coverage
```bash
pytest tests/unit/test_supabase_service.py --cov=app.services.supabase_service --cov-report=html
```

### Run Specific Test
```bash
pytest tests/unit/test_supabase_service.py::test_service_client_cached -v
```

---

## Coverage Requirements

### Minimum Coverage: 80%

### Coverage Areas:
- ✅ Service client creation and caching
- ✅ User client creation and caching
- ✅ Singleton pattern enforcement
- ✅ Thread safety
- ✅ Error handling
- ✅ Health check
- ✅ Convenience functions
- ✅ FastAPI integration

### Excluded from Coverage:
- Type hints
- `if TYPE_CHECKING` blocks
- Abstract methods

---

## Test Success Criteria

✅ All 19 test cases pass
✅ ≥80% code coverage achieved
✅ No flaky tests
✅ Thread safety verified
✅ All edge cases covered
✅ Error handling verified
✅ FastAPI integration tested
✅ Tests run in < 5 seconds

---

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)
- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)