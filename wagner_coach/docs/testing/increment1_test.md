# INCREMENT 1: Basic Coach Chat - Test Design

**Date:** 2025-10-01
**Feature:** Basic Coach Chat with AI Trainer
**Test Coverage Goal:** ≥80%
**Priority:** P0 (Critical)

---

## 🎯 TESTING OBJECTIVES

1. **Functional Testing:** Verify all chat features work as designed
2. **Integration Testing:** Ensure frontend ↔ backend ↔ database communication
3. **Unit Testing:** Test individual components and functions
4. **E2E Testing:** Validate complete user flows
5. **UI/UX Testing:** Verify all interface elements are accessible and functional

---

## 📋 TEST PLAN OVERVIEW

### Testing Layers

```
┌─────────────────────────────────────────────┐
│  E2E Tests (Playwright/Cypress)             │
│  - Complete user journeys                   │
└─────────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────────┐
│  Integration Tests (Python pytest)          │
│  - API endpoints                            │
│  - Database operations                      │
│  - RAG system                               │
└─────────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────────┐
│  Unit Tests (Jest + pytest)                 │
│  - Individual functions                     │
│  - Component rendering                      │
│  - State management                         │
└─────────────────────────────────────────────┘
```

---

## 🔧 BACKEND TESTS (Python pytest)

### 1. Unit Tests: Coach Service

**File:** `tests/unit/test_coach_service.py`

```python
import pytest
from app.services.coach_service import CoachService

class TestCoachService:
    """Test Coach Service functionality"""

    @pytest.fixture
    def coach_service(self):
        return CoachService()

    def test_get_trainer_persona(self, coach_service):
        """Test retrieving trainer persona"""
        persona = coach_service.get_persona('trainer')
        assert persona is not None
        assert persona['name'] == 'trainer'
        assert 'system_prompt' in persona
        assert len(persona['system_prompt']) > 0

    def test_get_invalid_persona(self, coach_service):
        """Test retrieving non-existent persona returns None"""
        persona = coach_service.get_persona('invalid')
        assert persona is None

    def test_build_context_with_workouts(self, coach_service, mock_user):
        """Test context building includes recent workouts"""
        context = coach_service.build_context(
            user_id=mock_user['id'],
            message="What should I do today?"
        )
        assert 'user_profile' in context
        assert 'recent_workouts' in context
        assert isinstance(context['recent_workouts'], list)

    def test_build_context_with_embeddings(self, coach_service, mock_user):
        """Test context includes RAG embeddings"""
        context = coach_service.build_context(
            user_id=mock_user['id'],
            message="How can I improve my squat?"
        )
        assert 'relevant_context' in context
        assert isinstance(context['relevant_context'], list)
        # Should retrieve embeddings related to squats

    def test_generate_response(self, coach_service, mock_user):
        """Test AI response generation"""
        response = coach_service.generate_response(
            user_id=mock_user['id'],
            message="What should I do today?",
            coach_type='trainer'
        )
        assert response is not None
        assert len(response) > 0
        assert isinstance(response, str)

    def test_save_conversation(self, coach_service, mock_user):
        """Test conversation saving to database"""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        conv_id = coach_service.save_conversation(
            user_id=mock_user['id'],
            coach_type='trainer',
            messages=messages
        )
        assert conv_id is not None
        assert isinstance(conv_id, str)

    def test_load_conversation(self, coach_service, mock_user, mock_conversation):
        """Test loading previous conversation"""
        conversation = coach_service.load_conversation(
            user_id=mock_user['id'],
            coach_type='trainer'
        )
        assert conversation is not None
        assert 'messages' in conversation
        assert len(conversation['messages']) > 0
```

### 2. Integration Tests: Coach API Endpoint

**File:** `tests/integration/test_coach_api.py`

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestCoachAPI:
    """Test Coach Chat API endpoint"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    @pytest.fixture
    def auth_headers(self, mock_user):
        return {
            "X-User-ID": mock_user['id'],
            "Authorization": f"Bearer {mock_user['token']}"
        }

    def test_chat_endpoint_success(self, client, auth_headers):
        """Test successful chat message"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "What should I do today?"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'message' in data
        assert 'conversation_id' in data
        assert len(data['message']) > 0

    def test_chat_endpoint_unauthorized(self, client):
        """Test chat without auth fails"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "Hello"
            }
        )
        assert response.status_code == 401

    def test_chat_endpoint_invalid_coach_type(self, client, auth_headers):
        """Test invalid coach type"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "invalid",
                "message": "Hello"
            },
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_chat_endpoint_empty_message(self, client, auth_headers):
        """Test empty message fails"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": ""
            },
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_chat_endpoint_message_too_long(self, client, auth_headers):
        """Test message length limit"""
        long_message = "a" * 1001  # Exceeds 1000 char limit
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": long_message
            },
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_chat_conversation_persistence(self, client, auth_headers):
        """Test conversation persists across messages"""
        # First message
        response1 = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "My name is John"
            },
            headers=auth_headers
        )
        conv_id = response1.json()['conversation_id']

        # Second message referencing first
        response2 = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "What's my name?",
                "conversation_id": conv_id
            },
            headers=auth_headers
        )
        assert response2.status_code == 200
        # AI should remember the name from previous message
        assert "john" in response2.json()['message'].lower()

    def test_chat_context_awareness(self, client, auth_headers, mock_workout):
        """Test coach uses RAG context"""
        response = client.post(
            "/api/v1/coach/chat",
            json={
                "coach_type": "trainer",
                "message": "What did I do in my last workout?"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        # Response should reference the mock workout
        assert mock_workout['name'].lower() in data['message'].lower()
```

### 3. Unit Tests: RAG Service

**File:** `tests/unit/test_rag_context.py`

```python
import pytest
from app.services.rag_service import RAGService

class TestRAGService:
    """Test RAG system for context retrieval"""

    @pytest.fixture
    def rag_service(self):
        return RAGService()

    def test_generate_embedding(self, rag_service):
        """Test embedding generation"""
        text = "Completed 5x5 squats at 225lbs"
        embedding = rag_service.generate_embedding(text)
        assert len(embedding) == 1536  # OpenAI embedding dimension
        assert all(isinstance(x, float) for x in embedding)

    def test_search_embeddings(self, rag_service, mock_user):
        """Test semantic search"""
        query = "squat workout"
        results = rag_service.search_embeddings(
            user_id=mock_user['id'],
            query=query,
            limit=5
        )
        assert isinstance(results, list)
        assert len(results) <= 5
        for result in results:
            assert 'content' in result
            assert 'similarity' in result
            assert result['similarity'] >= 0.7  # Minimum threshold

    def test_store_embedding(self, rag_service, mock_user):
        """Test storing embedding in database"""
        content = "Great leg day workout"
        embedding_id = rag_service.store_embedding(
            user_id=mock_user['id'],
            content=content,
            source_type='workout',
            source_id='test-workout-id'
        )
        assert embedding_id is not None
```

---

## 🎨 FRONTEND TESTS (Jest + React Testing Library)

### 4. Component Tests: TrainerChatClient

**File:** `__tests__/coach/TrainerChatClient.test.tsx`

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TrainerChatClient from '@/app/coach/trainer/TrainerChatClient';

describe('TrainerChatClient', () => {
  const mockProfile = {
    id: 'test-user',
    full_name: 'Test User',
    primary_goal: 'Build Muscle'
  };

  beforeEach(() => {
    // Mock fetch API
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders welcome message for new users', () => {
    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    expect(screen.getByText(/Welcome to your AI fitness coach/i)).toBeInTheDocument();
  });

  test('renders previous conversation messages', () => {
    const previousConversation = {
      id: 'conv-123',
      messages: [
        { role: 'user', content: 'Hello', timestamp: new Date() },
        { role: 'assistant', content: 'Hi there!', timestamp: new Date() }
      ]
    };

    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
        previousConversation={previousConversation}
      />
    );

    expect(screen.getByText('Hello')).toBeInTheDocument();
    expect(screen.getByText('Hi there!')).toBeInTheDocument();
  });

  test('input field is visible and functional', () => {
    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    const input = screen.getByPlaceholderText(/Ask your trainer/i);
    expect(input).toBeInTheDocument();
    expect(input).toBeEnabled();

    fireEvent.change(input, { target: { value: 'Test message' } });
    expect(input).toHaveValue('Test message');
  });

  test('send button is visible and clickable', () => {
    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    const sendButton = screen.getByRole('button', { name: /send/i });
    expect(sendButton).toBeInTheDocument();
    expect(sendButton).toBeEnabled();
  });

  test('send button disabled when input is empty', () => {
    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    const sendButton = screen.getByRole('button', { name: /send/i });
    expect(sendButton).toBeDisabled();
  });

  test('sends message on button click', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        message: 'AI response',
        conversation_id: 'conv-123'
      })
    });

    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    const input = screen.getByPlaceholderText(/Ask your trainer/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    await userEvent.type(input, 'What should I do today?');
    await userEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('What should I do today?')).toBeInTheDocument();
    });

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/coach/chat'),
      expect.objectContaining({
        method: 'POST',
        body: expect.stringContaining('What should I do today?')
      })
    );
  });

  test('sends message on Enter key', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        message: 'AI response',
        conversation_id: 'conv-123'
      })
    });

    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    const input = screen.getByPlaceholderText(/Ask your trainer/i);
    await userEvent.type(input, 'Test message{Enter}');

    await waitFor(() => {
      expect(screen.getByText('Test message')).toBeInTheDocument();
    });
  });

  test('Shift+Enter adds new line without sending', async () => {
    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    const input = screen.getByPlaceholderText(/Ask your trainer/i);
    await userEvent.type(input, 'Line 1{Shift>}{Enter}{/Shift}Line 2');

    expect(input).toHaveValue('Line 1\nLine 2');
    expect(screen.queryByText('Line 1')).not.toBeInTheDocument();
  });

  test('shows loading indicator while waiting for response', async () => {
    (global.fetch as jest.Mock).mockImplementationOnce(
      () => new Promise(resolve => setTimeout(resolve, 1000))
    );

    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    const input = screen.getByPlaceholderText(/Ask your trainer/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    await userEvent.type(input, 'Test');
    await userEvent.click(sendButton);

    expect(screen.getByText(/Coach is thinking/i)).toBeInTheDocument();
    expect(sendButton).toBeDisabled();
  });

  test('displays AI response', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        message: 'Based on your last workout, I recommend...',
        conversation_id: 'conv-123'
      })
    });

    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    const input = screen.getByPlaceholderText(/Ask your trainer/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    await userEvent.type(input, 'What should I do?');
    await userEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/Based on your last workout/i)).toBeInTheDocument();
    });
  });

  test('handles API error gracefully', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    const input = screen.getByPlaceholderText(/Ask your trainer/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    await userEvent.type(input, 'Test');
    await userEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
    });
  });

  test('clears input after successful send', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        message: 'Response',
        conversation_id: 'conv-123'
      })
    });

    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    const input = screen.getByPlaceholderText(/Ask your trainer/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    await userEvent.type(input, 'Test message');
    await userEvent.click(sendButton);

    await waitFor(() => {
      expect(input).toHaveValue('');
    });
  });

  test('auto-scrolls to latest message', async () => {
    const scrollIntoViewMock = jest.fn();
    window.HTMLElement.prototype.scrollIntoView = scrollIntoViewMock;

    render(
      <TrainerChatClient
        userId="test-user"
        profile={mockProfile}
      />
    );

    expect(scrollIntoViewMock).toHaveBeenCalled();
  });
});
```

---

## 🌐 E2E TESTS (Playwright/Cypress)

### 5. End-to-End User Flow

**File:** `e2e/coach-chat.spec.ts`

```typescript
import { test, expect } from '@playwright/test';

test.describe('Trainer Chat Feature', () => {
  test.beforeEach(async ({ page }) => {
    // Login first
    await page.goto('/auth');
    await page.fill('input[type="email"]', 'test@example.com');
    await page.fill('input[type="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
  });

  test('complete chat flow from navigation to response', async ({ page }) => {
    // Navigate to coach chat
    await page.goto('/coach/trainer');

    // Verify page loaded
    await expect(page.locator('h1')).toContainText('TRAINER CHAT');

    // Verify welcome message
    await expect(page.getByText(/Welcome to your AI fitness coach/i)).toBeVisible();

    // Type message
    await page.fill('textarea[placeholder*="Ask your trainer"]', 'What should I do today?');

    // Verify send button is enabled
    const sendButton = page.getByRole('button', { name: /send/i });
    await expect(sendButton).toBeEnabled();

    // Send message
    await sendButton.click();

    // Verify message appears in chat
    await expect(page.getByText('What should I do today?')).toBeVisible();

    // Verify loading indicator
    await expect(page.getByText(/Coach is thinking/i)).toBeVisible();

    // Wait for AI response (timeout 10s)
    await expect(page.getByText(/Based on/i)).toBeVisible({ timeout: 10000 });

    // Verify input was cleared
    const input = page.locator('textarea[placeholder*="Ask your trainer"]');
    await expect(input).toHaveValue('');
  });

  test('conversation persists across page refresh', async ({ page }) => {
    await page.goto('/coach/trainer');

    // Send a message
    await page.fill('textarea', 'Test persistence');
    await page.click('button[name="send"]');
    await expect(page.getByText('Test persistence')).toBeVisible();

    // Refresh page
    await page.reload();

    // Verify message still appears
    await expect(page.getByText('Test persistence')).toBeVisible();
  });

  test('all UI elements have proper hover states', async ({ page }) => {
    await page.goto('/coach/trainer');

    const sendButton = page.getByRole('button', { name: /send/i });

    // Hover over send button
    await sendButton.hover();

    // Check if button has hover state (color change, etc.)
    const bgColor = await sendButton.evaluate((el) =>
      window.getComputedStyle(el).backgroundColor
    );
    expect(bgColor).toBeTruthy();
  });

  test('mobile responsive layout', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/coach/trainer');

    // Verify chat container is visible
    await expect(page.locator('[data-testid="chat-container"]')).toBeVisible();

    // Verify input is accessible
    await expect(page.locator('[data-testid="input-container"]')).toBeVisible();
  });

  test('accessibility: keyboard navigation works', async ({ page }) => {
    await page.goto('/coach/trainer');

    // Tab to input
    await page.keyboard.press('Tab');
    const input = page.locator('textarea');
    await expect(input).toBeFocused();

    // Type message
    await page.keyboard.type('Keyboard test');

    // Tab to send button
    await page.keyboard.press('Tab');
    const sendButton = page.getByRole('button', { name: /send/i });
    await expect(sendButton).toBeFocused();

    // Press Enter to send
    await page.keyboard.press('Enter');

    // Verify message sent
    await expect(page.getByText('Keyboard test')).toBeVisible();
  });
});
```

---

## ✅ MANUAL TESTING CHECKLIST

### UI/UX Verification (Step 7 of TDD Process)

#### 7a. All Buttons Created
- [ ] Send button exists
- [ ] Send button has icon (arrow/send icon)
- [ ] Send button has text or aria-label for accessibility
- [ ] Clear chat button exists (if applicable)
- [ ] Back/navigation button exists

#### 7b. All Pages Accessible
- [ ] /coach/trainer page loads without error
- [ ] Page requires authentication (redirects if not logged in)
- [ ] Page accessible from navigation menu
- [ ] Direct URL navigation works
- [ ] Deep linking works

#### 7c. All Buttons Give Proper Feedback
- [ ] Send button shows disabled state when input empty
- [ ] Send button shows loading state while processing
- [ ] Send button shows hover effect
- [ ] Send button shows active/pressed state
- [ ] Clear chat button shows confirmation prompt

#### 7d. All Buttons Apparent Enough to Click
- [ ] Send button has minimum touch target size (44x44px)
- [ ] Button colors contrast well with background
- [ ] Button labels are clear and descriptive
- [ ] Icons are recognizable
- [ ] Buttons are positioned logically

#### 7e. Everything Visible with Good Style Practices
- [ ] Message bubbles have good contrast
- [ ] Text is readable (minimum 14px font size)
- [ ] Proper spacing between messages
- [ ] Loading indicator is obvious
- [ ] Error states are clearly highlighted
- [ ] Focus states are visible for keyboard navigation
- [ ] Colors follow design system
- [ ] Mobile layout doesn't have overflow issues
- [ ] Scrolling is smooth

---

## 📊 TEST COVERAGE REQUIREMENTS

### Minimum Coverage Targets
- **Overall Code Coverage:** ≥80%
- **Backend API:** ≥90%
- **Coach Service:** ≥85%
- **RAG Service:** ≥80%
- **Frontend Components:** ≥75%

### Coverage Report Command
```bash
# Backend
cd fitness-backend
pytest --cov=app --cov-report=html tests/

# Frontend
cd wagner-coach-clean
npm run test:coverage
```

---

## 🐛 ERROR SCENARIOS TO TEST

1. **Network Errors**
   - API unreachable
   - Timeout (>30s)
   - Connection lost mid-request

2. **Authentication Errors**
   - Invalid token
   - Expired session
   - Missing auth header

3. **Validation Errors**
   - Empty message
   - Message too long
   - Invalid characters

4. **AI Service Errors**
   - OpenAI API down
   - Rate limit exceeded
   - Invalid response format

5. **Database Errors**
   - Connection lost
   - Insert failed
   - Query timeout

---

## ✅ DEFINITION OF DONE (TESTING)

INCREMENT 1 testing is complete when:

1. ✅ All unit tests pass (100%)
2. ✅ All integration tests pass (100%)
3. ✅ All E2E tests pass (100%)
4. ✅ Code coverage ≥80%
5. ✅ All manual UI checks completed
6. ✅ All error scenarios tested
7. ✅ Performance benchmarks met
8. ✅ Accessibility tests pass
9. ✅ Mobile responsive tests pass
10. ✅ Cross-browser tests pass (Chrome, Firefox, Safari)

---

**Last Updated:** 2025-10-01
**Status:** Ready for Implementation Phase
