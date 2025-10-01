# INCREMENT 1: Basic Coach Chat - Test Design Document

## Document Information
- **Increment**: 1
- **Feature**: Basic Coach Chat
- **Version**: 1.0
- **Last Updated**: 2025-10-01
- **Test Coverage Goal**: >=80%
- **Priority**: P0 (Critical)

## Table of Contents
1. [Test Objectives](#test-objectives)
2. [Test Scope](#test-scope)
3. [Backend Unit Tests](#backend-unit-tests)
4. [Frontend Unit Tests](#frontend-unit-tests)
5. [Backend Integration Tests](#backend-integration-tests)
6. [Frontend Integration Tests](#frontend-integration-tests)
7. [Test Data](#test-data)
8. [Coverage Requirements](#coverage-requirements)
9. [Test Environment](#test-environment)

## Test Objectives

The testing strategy for INCREMENT 1 aims to verify all functional requirements are met with high confidence:

1. **Functional Verification**: Ensure all chat features work as designed
2. **API Contract Validation**: Verify frontend-backend communication
3. **Error Handling**: Confirm graceful degradation and recovery
4. **User Experience**: Validate loading states, error messages, and feedback
5. **Performance**: Ensure response times meet requirements (<5s)
6. **Accessibility**: Verify WCAG compliance and keyboard navigation

## Test Scope

### In Scope

**Backend:**
- Coach API endpoint (`/api/v1/coach/chat`)
- CoachService.generate_response() method
- Request/response validation (Pydantic schemas)
- Error handling and status codes
- OpenAI integration

**Frontend:**
- Next.js API route (`/api/coach/chat`)
- Chat UI components
- Message sending and display
- Loading and error states
- User input validation
- Keyboard interactions

**Integration:**
- Full request/response flow
- State management across UI updates
- Error propagation from backend to frontend

### Out of Scope (Future Increments)

- Conversation persistence in database
- User authentication and authorization
- RAG context retrieval
- Multi-coach support
- Advanced features (voice, images, etc.)

## Backend Unit Tests

### Test File: `fitness-backend/tests/unit/test_coach_service_increment1.py`

#### Test 1: Valid Chat Request
```python
def test_generate_response_valid_message():
    """Test that valid message generates proper AI response"""
    # Arrange
    service = CoachService()
    message = "What's a good workout for beginners?"
    coach_type = "fitness"

    # Act
    response = service.generate_response(message, coach_type)

    # Assert
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    assert len(response) <= 4000  # Reasonable max length
```

#### Test 2: Missing Message
```python
def test_generate_response_missing_message():
    """Test that missing message raises validation error"""
    # Arrange
    service = CoachService()

    # Act & Assert
    with pytest.raises(ValueError, match="Message cannot be empty"):
        service.generate_response("", "fitness")
```

#### Test 3: Invalid Coach Type
```python
def test_generate_response_invalid_coach_type():
    """Test that invalid coach_type raises validation error"""
    # Arrange
    service = CoachService()
    message = "Hello"
    invalid_type = "invalid_coach"

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid coach type"):
        service.generate_response(message, invalid_type)
```

#### Test 4: OpenAI Error Handling
```python
@patch('app.services.coach_service.openai.ChatCompletion.create')
def test_generate_response_openai_error(mock_openai):
    """Test graceful handling of OpenAI API errors"""
    # Arrange
    service = CoachService()
    mock_openai.side_effect = openai.error.APIError("Service unavailable")

    # Act & Assert
    with pytest.raises(ServiceUnavailableError):
        service.generate_response("Hello", "fitness")
```

#### Test 5: Response Format Validation
```python
def test_response_format():
    """Test that response matches expected format"""
    # Arrange
    service = CoachService()
    message = "Give me a workout tip"

    # Act
    response = service.generate_response(message, "fitness")

    # Assert
    assert isinstance(response, str)
    assert not response.startswith("Error:")
    assert not response.startswith("Exception:")
    # Should be proper sentence/paragraph format
    assert len(response.split()) >= 10  # At least 10 words
```

### Additional Backend Unit Tests

#### Test 6: Whitespace Handling
```python
def test_whitespace_message_trimmed():
    """Test that whitespace-only messages are rejected"""
    service = CoachService()

    with pytest.raises(ValueError, match="Message cannot be empty"):
        service.generate_response("   \n\t  ", "fitness")
```

#### Test 7: Message Length Validation
```python
def test_message_too_long():
    """Test that messages exceeding max length are rejected"""
    service = CoachService()
    long_message = "a" * 2001  # Exceeds 2000 char limit

    with pytest.raises(ValueError, match="Message too long"):
        service.generate_response(long_message, "fitness")
```

## Frontend Unit Tests

### Test File: `__tests__/coach/CoachChat.test.tsx`

#### Test 1: Input State Updates
```typescript
test('input value updates on user typing', async () => {
  render(<CoachChatPage />);

  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);

  await userEvent.type(input, 'Hello Coach');

  expect(input).toHaveValue('Hello Coach');
});
```

#### Test 2: Send Button Disabled When Empty
```typescript
test('send button is disabled when input is empty', () => {
  render(<CoachChatPage />);

  const sendButton = screen.getByRole('button', { name: /send/i });

  expect(sendButton).toBeDisabled();
});
```

#### Test 3: Enter Key Sends Message
```typescript
test('pressing Enter key sends message', async () => {
  const mockFetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ response: 'AI response', conversation_id: '123' })
  });
  global.fetch = mockFetch;

  render(<CoachChatPage />);

  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);
  await userEvent.type(input, 'Test message{Enter}');

  expect(mockFetch).toHaveBeenCalled();
});
```

#### Test 4: Message Display with Correct Styling
```typescript
test('user messages display with blue background', async () => {
  render(<CoachChatPage />);

  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);
  const sendButton = screen.getByRole('button', { name: /send/i });

  await userEvent.type(input, 'Test message');
  await userEvent.click(sendButton);

  const userMessage = screen.getByText('Test message');
  expect(userMessage).toHaveClass('bg-blue-500'); // or similar
});
```

#### Test 5: Loading State During API Call
```typescript
test('loading indicator shows while waiting for response', async () => {
  global.fetch = jest.fn(() =>
    new Promise(resolve => setTimeout(resolve, 1000))
  );

  render(<CoachChatPage />);

  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);
  const sendButton = screen.getByRole('button', { name: /send/i });

  await userEvent.type(input, 'Test');
  await userEvent.click(sendButton);

  expect(screen.getByText(/typing/i)).toBeInTheDocument();
  expect(sendButton).toBeDisabled();
});
```

#### Test 6: Error Display
```typescript
test('error message displays on API failure', async () => {
  global.fetch = jest.fn().mockRejectedValue(new Error('Network error'));

  render(<CoachChatPage />);

  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);
  const sendButton = screen.getByRole('button', { name: /send/i });

  await userEvent.type(input, 'Test');
  await userEvent.click(sendButton);

  await waitFor(() => {
    expect(screen.getByText(/Unable to reach Coach Alex/i)).toBeInTheDocument();
  });
});
```

### Additional Frontend Unit Tests

#### Test 7: Character Counter
```typescript
test('character counter updates correctly', async () => {
  render(<CoachChatPage />);

  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);
  await userEvent.type(input, 'Hello');

  expect(screen.getByText('5 / 2000')).toBeInTheDocument();
});
```

#### Test 8: Shift+Enter Creates New Line
```typescript
test('Shift+Enter adds new line without sending', async () => {
  render(<CoachChatPage />);

  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);
  await userEvent.type(input, 'Line 1{Shift>}{Enter}{/Shift}Line 2');

  expect(input).toHaveValue('Line 1\nLine 2');
  expect(global.fetch).not.toHaveBeenCalled();
});
```

#### Test 9: Input Clears After Send
```typescript
test('input field clears after successful send', async () => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ response: 'Response', conversation_id: '123' })
  });

  render(<CoachChatPage />);

  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);
  const sendButton = screen.getByRole('button', { name: /send/i });

  await userEvent.type(input, 'Test message');
  await userEvent.click(sendButton);

  await waitFor(() => {
    expect(input).toHaveValue('');
  });
});
```

## Backend Integration Tests

### Test File: `fitness-backend/tests/integration/test_coach_api_increment1.py`

#### Test 1: Full Request/Response Flow
```python
def test_chat_endpoint_success(client, auth_headers):
    """Test complete successful chat flow"""
    # Arrange
    payload = {
        "message": "What's a good workout for beginners?",
        "coach_type": "fitness"
    }

    # Act
    response = client.post(
        "/api/v1/coach/chat",
        json=payload,
        headers=auth_headers
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "conversation_id" in data
    assert "timestamp" in data
    assert len(data["response"]) > 0
```

#### Test 2: Authentication Required
```python
def test_chat_endpoint_unauthorized(client):
    """Test that unauthenticated requests are rejected"""
    # Arrange
    payload = {
        "message": "Hello",
        "coach_type": "fitness"
    }

    # Act
    response = client.post("/api/v1/coach/chat", json=payload)

    # Assert
    assert response.status_code == 401
```

#### Test 3: Input Validation
```python
def test_chat_endpoint_invalid_input(client, auth_headers):
    """Test validation of request payload"""
    test_cases = [
        ({"message": "", "coach_type": "fitness"}, "Message cannot be empty"),
        ({"message": "Hello", "coach_type": "invalid"}, "Invalid coach type"),
        ({"coach_type": "fitness"}, "Field required"),
        ({"message": "a" * 2001, "coach_type": "fitness"}, "Message too long"),
    ]

    for payload, expected_error in test_cases:
        response = client.post(
            "/api/v1/coach/chat",
            json=payload,
            headers=auth_headers
        )
        assert response.status_code == 400
        assert expected_error in response.json()["detail"]
```

#### Test 4: Rate Limiting
```python
def test_rate_limiting(client, auth_headers):
    """Test that rate limiting is enforced"""
    # Arrange
    payload = {"message": "Hello", "coach_type": "fitness"}

    # Act - Send 21 requests (limit is 20/minute)
    responses = []
    for i in range(21):
        response = client.post(
            "/api/v1/coach/chat",
            json=payload,
            headers=auth_headers
        )
        responses.append(response)

    # Assert
    success_count = sum(1 for r in responses if r.status_code == 200)
    rate_limited = sum(1 for r in responses if r.status_code == 429)

    assert success_count == 20
    assert rate_limited == 1

    # Check retry-after header
    limited_response = next(r for r in responses if r.status_code == 429)
    assert "Retry-After" in limited_response.headers
```

## Frontend Integration Tests

### Test File: `__tests__/api/coach-chat.test.ts`

#### Test 1: Next.js API Route Integration
```typescript
test('POST /api/coach/chat returns AI response', async () => {
  const payload = {
    message: 'What should I do today?',
    coach_type: 'fitness'
  };

  const response = await fetch('/api/coach/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  expect(response.status).toBe(200);

  const data = await response.json();
  expect(data).toHaveProperty('response');
  expect(data).toHaveProperty('conversation_id');
  expect(typeof data.response).toBe('string');
});
```

#### Test 2: End-to-End Message Flow
```typescript
test('complete user message to AI response flow', async () => {
  render(<CoachChatPage />);

  // User types and sends message
  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);
  const sendButton = screen.getByRole('button', { name: /send/i });

  await userEvent.type(input, 'Give me a workout tip');
  await userEvent.click(sendButton);

  // User message appears immediately
  expect(screen.getByText('Give me a workout tip')).toBeInTheDocument();

  // Loading state shows
  expect(screen.getByText(/typing/i)).toBeInTheDocument();

  // AI response appears
  await waitFor(() => {
    const messages = screen.getAllByRole('article'); // Assuming messages have role="article"
    expect(messages.length).toBeGreaterThan(1);
  }, { timeout: 6000 });

  // Loading state disappears
  expect(screen.queryByText(/typing/i)).not.toBeInTheDocument();
});
```

#### Test 3: Error Handling Flow
```typescript
test('error propagates from backend to frontend display', async () => {
  // Mock backend to return error
  global.fetch = jest.fn().mockResolvedValue({
    ok: false,
    status: 500,
    json: async () => ({ error: 'Internal server error' })
  });

  render(<CoachChatPage />);

  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);
  const sendButton = screen.getByRole('button', { name: /send/i });

  await userEvent.type(input, 'Test');
  await userEvent.click(sendButton);

  await waitFor(() => {
    expect(screen.getByText(/Unable to reach Coach Alex/i)).toBeInTheDocument();
  });
});
```

#### Test 4: Session State Persistence
```typescript
test('chat history persists during session', async () => {
  const { rerender } = render(<CoachChatPage />);

  // Send first message
  const input = screen.getByPlaceholderText(/Ask Coach Alex/i);
  await userEvent.type(input, 'First message');
  await userEvent.click(screen.getByRole('button', { name: /send/i }));

  await waitFor(() => {
    expect(screen.getByText('First message')).toBeInTheDocument();
  });

  // Simulate component re-render
  rerender(<CoachChatPage />);

  // First message should still be visible
  expect(screen.getByText('First message')).toBeInTheDocument();
});
```

## Test Data

### Sample User Messages

```typescript
const SAMPLE_MESSAGES = {
  simple: "What's a good workout?",
  detailed: "I'm a beginner and want to start strength training. What exercises should I focus on?",
  multiline: "I have three questions:\n1. Best workout time?\n2. How many days per week?\n3. What about diet?",
  special_chars: "What's the #1 tip for building muscle? (asking for a friend!)",
  long: "I've been working out for 6 months now and I feel like I've hit a plateau. My lifts aren't increasing and I'm not seeing any changes in my physique. I'm currently doing a 3-day split focusing on chest/triceps, back/biceps, and legs/shoulders. I'm eating around 2500 calories per day with 150g of protein. What should I change?",
};
```

### Expected AI Response Patterns

```typescript
const EXPECTED_RESPONSE_PATTERNS = {
  greeting: /hello|hi|hey/i,
  workout_advice: /exercise|workout|training|sets|reps/i,
  nutrition: /calories|protein|diet|nutrition|macros/i,
  encouragement: /great|good job|keep it up|you're doing well/i,
  personalized: /based on your|considering your|given your/i,
};
```

### Invalid Test Cases

```typescript
const INVALID_INPUTS = {
  empty: "",
  whitespace: "   \n\t  ",
  too_long: "a".repeat(2001),
  sql_injection: "'; DROP TABLE users; --",
  xss_attempt: "<script>alert('xss')</script>",
  null_message: null,
  undefined_message: undefined,
};
```

## Coverage Requirements

### Minimum Coverage Targets

- **Backend API Endpoint**: >=90% line coverage
- **Backend CoachService**: >=85% line coverage
- **Frontend Components**: >=75% line coverage
- **Frontend API Routes**: >=80% line coverage
- **Overall Project**: >=80% line coverage

### Coverage Commands

**Backend:**
```bash
cd fitness-backend
pytest --cov=app.api.v1.coach --cov=app.services.coach_service \
       --cov-report=html --cov-report=term \
       tests/unit/test_coach_service_increment1.py \
       tests/integration/test_coach_api_increment1.py
```

**Frontend:**
```bash
cd wagner-coach-clean
npm run test:coverage -- __tests__/coach/
```

### Coverage Report Locations

- Backend: `fitness-backend/htmlcov/index.html`
- Frontend: `wagner-coach-clean/coverage/lcov-report/index.html`

## Test Environment

### Backend Test Environment

**Framework**: pytest
**Test Client**: FastAPI TestClient
**Mocking**: pytest-mock, unittest.mock
**Fixtures**: conftest.py

**Required Environment Variables:**
```bash
OPENAI_API_KEY=test-key-mock
DATABASE_URL=sqlite:///:memory:
ENVIRONMENT=test
```

**Test Database:**
- In-memory SQLite for unit tests
- Isolated test database for integration tests
- Automatic cleanup after each test

### Frontend Test Environment

**Framework**: Jest
**Testing Library**: React Testing Library
**Mocking**: jest.fn(), MSW (Mock Service Worker)

**Jest Configuration:**
```javascript
{
  "testEnvironment": "jsdom",
  "setupFilesAfterEnv": ["<rootDir>/jest.setup.js"],
  "moduleNameMapper": {
    "^@/(.*)$": "<rootDir>/src/$1"
  }
}
```

### Running Tests

**Backend:**
```bash
# All tests
pytest fitness-backend/tests/

# Unit tests only
pytest fitness-backend/tests/unit/

# Integration tests only
pytest fitness-backend/tests/integration/

# Specific test file
pytest fitness-backend/tests/unit/test_coach_service_increment1.py

# With coverage
pytest --cov=app --cov-report=html tests/
```

**Frontend:**
```bash
# All tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm run test:coverage

# Specific test file
npm test -- __tests__/coach/CoachChat.test.tsx
```

### Continuous Integration

Tests run automatically on:
- Every pull request
- Every commit to main branch
- Nightly builds

**CI Pipeline:**
1. Lint code (backend: flake8, frontend: eslint)
2. Run unit tests
3. Run integration tests
4. Generate coverage reports
5. Fail if coverage < 80%
6. Deploy if all tests pass

## Test Execution Checklist

### Before Implementation
- [ ] Review functional requirements
- [ ] Review API design
- [ ] Set up test environment
- [ ] Create test fixtures
- [ ] Write test data

### During Implementation
- [ ] Write tests before code (TDD)
- [ ] Run tests frequently
- [ ] Fix failing tests immediately
- [ ] Maintain test coverage >80%
- [ ] Document test failures

### After Implementation
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Coverage requirements met
- [ ] Manual testing completed
- [ ] Performance benchmarks met
- [ ] Accessibility tests pass
- [ ] Cross-browser tests pass
- [ ] Mobile responsive tests pass

---

**Document Status:** Ready for Implementation
**Next Steps:** Set up test environment → Write tests → Implement features (TDD)
