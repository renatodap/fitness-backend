# INCREMENT 1: Basic Coach Chat - Design Document

## Document Information
- **Increment**: 1
- **Feature**: Basic Coach Chat
- **Version**: 1.0
- **Last Updated**: 2025-10-01
- **Status**: Design Complete

## Table of Contents
1. [Objective](#objective)
2. [Functional Requirements](#functional-requirements)
3. [Non-Functional Requirements](#non-functional-requirements)
4. [Architecture](#architecture)
5. [API Design](#api-design)
6. [UI/UX Design](#uiux-design)
7. [Acceptance Criteria](#acceptance-criteria)
8. [Testing Strategy](#testing-strategy)
9. [Security Considerations](#security-considerations)
10. [References](#references)

## Objective

Enable users to have real-time chat conversations with an AI fitness trainer (Coach Alex). This increment establishes the foundational chat interface and backend integration that will be extended in subsequent increments.

**Key Goals:**
- Provide a simple, intuitive chat interface for users to interact with Coach Alex
- Establish reliable backend-frontend communication for AI responses
- Create a scalable foundation for future coach features (context, memory, personalization)
- Ensure excellent user experience with appropriate loading states and error handling

## Functional Requirements

### FR-1: Navigation to Coach Page
- Users can navigate to `/coach` route from the main navigation
- Page loads with empty chat state ready for interaction
- Coach Alex greeting message displays automatically on first load

### FR-2: Chat Input Field
- Text input field for users to type messages
- Input field supports multi-line text (textarea component)
- Input field has appropriate placeholder text: "Ask Coach Alex anything about your fitness journey..."
- Character limit: 2000 characters with visual counter
- Input field auto-focuses on page load

### FR-3: Send Message Button
- "Send" button next to input field
- Button disabled when input is empty or contains only whitespace
- Button disabled during message processing (loading state)
- Clear visual indication of button state (enabled/disabled)

### FR-4: Keyboard Shortcuts
- Enter key sends message (with Shift+Enter for new line)
- Input clears after successful message send
- Focus returns to input field after message sent

### FR-5: Message Display
- User messages display with right alignment, blue background (#3B82F6)
- AI messages display with left alignment, gray background (#F3F4F6)
- Messages include timestamp in "HH:mm" format
- Messages support markdown formatting (bold, italic, lists)
- Avatar/icon for both user and AI messages

### FR-6: Loading States
- Loading indicator displays while waiting for AI response
- "Coach Alex is typing..." indicator with animated dots
- Send button shows loading spinner during processing
- Input field disabled during AI response generation

### FR-7: Error Handling Display
- Error messages display in toast/alert format
- Clear error messages for common scenarios:
  - "Unable to reach Coach Alex. Please try again."
  - "Message too long. Please keep under 2000 characters."
  - "Rate limit exceeded. Please wait a moment."
- Retry mechanism for failed requests

### FR-8: Chat History Display
- All messages in conversation display in chronological order
- Auto-scroll to bottom when new message arrives
- Smooth scroll animation for better UX
- Chat history persists during session (not between sessions)

### FR-9: Empty State
- Welcoming empty state when no messages exist
- Suggested starter questions to guide users:
  - "What's a good workout for beginners?"
  - "How do I stay motivated?"
  - "Can you create a workout plan for me?"

### FR-10: Message Formatting
- Support for basic markdown in AI responses
- Proper line breaks and paragraph spacing
- Hyperlinks rendered as clickable elements
- Code blocks or exercise names highlighted

### FR-11: Responsive Design
- Mobile-first design approach
- Chat interface adapts to screen size (mobile, tablet, desktop)
- Input and send button properly sized on mobile devices
- Messages readable on all screen sizes

### FR-12: Accessibility
- Proper ARIA labels for all interactive elements
- Keyboard navigation support
- Screen reader announcements for new messages
- Sufficient color contrast (WCAG AA compliance)

## Non-Functional Requirements

### NFR-1: Performance
- AI response time: < 5 seconds (95th percentile)
- Page load time: < 2 seconds
- Message send latency: < 500ms
- Smooth animations (60fps) for scroll and transitions

### NFR-2: Reliability
- System uptime: 99% availability
- Graceful degradation when AI service unavailable
- Automatic retry with exponential backoff for transient failures
- Error recovery without data loss

### NFR-3: Scalability
- Support for conversations up to 50 messages
- Handle concurrent users efficiently
- Rate limiting: 20 messages per minute per user
- Backend can process 100 requests/second

### NFR-4: Error Handling
- All API errors properly caught and handled
- User-friendly error messages (no technical jargon)
- Fallback mechanisms for service degradation
- Logging of all errors for debugging

### NFR-5: Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard-only navigation support
- Screen reader compatibility (NVDA, JAWS, VoiceOver)
- High contrast mode support

### NFR-6: Mobile Responsiveness
- Touch-friendly interface (44px minimum touch targets)
- Optimized for iOS and Android devices
- Support for screen sizes from 320px to 2560px width
- No horizontal scrolling required

### NFR-7: Security
- Input sanitization to prevent XSS attacks
- Rate limiting to prevent abuse
- Authentication required for API access
- Secure transmission (HTTPS only)

## Architecture

### Component Hierarchy

```
CoachPage
├── CoachHeader
│   ├── CoachAvatar
│   └── CoachTitle
├── ChatContainer
│   ├── ChatHistory
│   │   ├── MessageList
│   │   │   ├── UserMessage (multiple)
│   │   │   └── AIMessage (multiple)
│   │   └── LoadingIndicator
│   └── EmptyState
└── ChatInput
    ├── TextArea
    ├── CharacterCounter
    └── SendButton
```

### Data Flow

```
User Action (Type & Send)
    ↓
Frontend State Update (add user message)
    ↓
API Request to /api/coach/chat
    ↓
Backend API Route (/api/v1/coach/chat)
    ↓
CoachService.generate_response()
    ↓
OpenAI API Call
    ↓
Response Processing
    ↓
Frontend receives AI response
    ↓
State Update (add AI message)
    ↓
UI Update (display message, scroll to bottom)
```

### State Management

**Frontend State (React useState/Context):**
```typescript
interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  inputValue: string;
}

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  metadata?: Record<string, any>;
}
```

**Backend State (Session-based):**
- Stateless API - each request independent
- Future: Conversation context stored in database
- Rate limiting tracked per user session

### Technology Stack

**Frontend:**
- Next.js 14 with App Router
- React 18 for UI components
- TypeScript for type safety
- Tailwind CSS for styling
- React Markdown for message formatting

**Backend:**
- FastAPI (Python) for API endpoints
- OpenAI Python SDK for AI integration
- Pydantic for request/response validation
- SQLAlchemy (future) for conversation storage

## API Design

### Frontend API Route

**Endpoint:** `POST /api/coach/chat`

**Request Body:**
```typescript
{
  "message": string;          // User's message (required, max 2000 chars)
  "coach_type": string;       // Type of coach (default: "fitness")
  "conversation_id"?: string; // Optional conversation ID (future)
}
```

**Response (Success):**
```typescript
{
  "response": string;         // AI-generated response
  "conversation_id": string;  // Conversation identifier
  "timestamp": string;        // ISO 8601 timestamp
  "metadata": {
    "model": string;          // AI model used
    "tokens_used": number;    // Token count
  }
}
```

**Response (Error):**
```typescript
{
  "error": string;            // Error message
  "code": string;             // Error code
  "details"?: any;            // Additional error details
}
```

### Backend API Route

**Endpoint:** `POST /api/v1/coach/chat`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <token> (if authenticated)
```

**Request Body (Pydantic Schema):**
```python
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    coach_type: str = Field(default="fitness", pattern="^(fitness|nutrition|wellness)$")
    conversation_id: Optional[str] = None

    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
```

**Response Body (Pydantic Schema):**
```python
class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: datetime
    metadata: Dict[str, Any]
```

**Status Codes:**
- 200: Success
- 400: Bad Request (invalid input)
- 429: Too Many Requests (rate limit exceeded)
- 500: Internal Server Error
- 503: Service Unavailable (OpenAI down)

### Error Responses

**400 Bad Request:**
```json
{
  "detail": "Message exceeds maximum length of 2000 characters"
}
```

**429 Too Many Requests:**
```json
{
  "detail": "Rate limit exceeded. Please try again in 30 seconds.",
  "retry_after": 30
}
```

**500 Internal Server Error:**
```json
{
  "detail": "An unexpected error occurred. Please try again."
}
```

## UI/UX Design

### Visual Hierarchy

1. **Coach Header** (Fixed top)
   - Coach avatar and name
   - Status indicator (online/typing)
   - Minimal, non-intrusive design

2. **Chat History** (Scrollable middle)
   - Primary focus area
   - Clear message distinction (user vs AI)
   - Timestamps for context

3. **Input Area** (Fixed bottom)
   - Always accessible
   - Clear call-to-action (Send button)
   - Character counter for guidance

### Color Palette

**User Messages:**
- Background: Blue (#3B82F6)
- Text: White (#FFFFFF)
- Border: None
- Shadow: Subtle drop shadow

**AI Messages:**
- Background: Gray (#F3F4F6)
- Text: Dark Gray (#1F2937)
- Border: Light Gray (#E5E7EB)
- Shadow: None

**Interactive Elements:**
- Primary Button: Blue (#3B82F6)
- Primary Button Hover: Darker Blue (#2563EB)
- Disabled State: Gray (#9CA3AF)
- Error State: Red (#EF4444)

### Typography

- **Headers**: Inter, 18px, Semi-bold (600)
- **Message Text**: Inter, 16px, Regular (400)
- **Timestamps**: Inter, 12px, Regular (400), Gray (#6B7280)
- **Input Placeholder**: Inter, 16px, Regular (400), Light Gray (#9CA3AF)

### Spacing & Layout

**Desktop (>=1024px):**
- Max chat width: 800px (centered)
- Message padding: 16px
- Message margin: 12px vertical
- Input area height: 80px + dynamic based on content

**Tablet (768px - 1023px):**
- Full width with 24px side margins
- Message padding: 14px
- Message margin: 10px vertical

**Mobile (<768px):**
- Full width with 16px side margins
- Message padding: 12px
- Message margin: 8px vertical
- Fixed input area at bottom (safe-area-inset support)

### Interaction States

**Send Button:**
- Default: Blue background, white text, pointer cursor
- Hover: Darker blue background, slight scale (1.02)
- Active: Even darker blue, scale (0.98)
- Disabled: Gray background, not-allowed cursor
- Loading: Spinner animation, disabled state

**Input Field:**
- Default: Light border, focus outline
- Focus: Blue border (#3B82F6), no outline ring
- Error: Red border (#EF4444)
- Disabled: Gray background, not-allowed cursor

### Animations

- Message appearance: Fade in + slide up (200ms)
- Auto-scroll: Smooth scroll (300ms)
- Loading indicator: Pulsing dots (1s loop)
- Button hover: Transform scale (150ms)

## Acceptance Criteria

### AC-1: Page Renders Successfully
- [ ] Coach page loads without errors at `/coach` route
- [ ] Empty state displays with suggested questions
- [ ] Input field is auto-focused and ready for input
- [ ] All UI elements render correctly on all screen sizes
- [ ] No console errors or warnings

### AC-2: Send Message Flow
- [ ] User can type message in input field
- [ ] Character counter updates correctly (max 2000)
- [ ] Send button disabled when input empty/whitespace only
- [ ] Enter key sends message (Shift+Enter for new line)
- [ ] Input clears after successful send
- [ ] User message appears immediately in chat history

### AC-3: AI Response Flow
- [ ] Loading indicator displays while waiting for response
- [ ] "Coach Alex is typing..." message shows
- [ ] AI response appears within 5 seconds
- [ ] Response formatted correctly with markdown support
- [ ] Auto-scroll to bottom when response arrives
- [ ] Input re-enabled after response received

### AC-4: Chat History Management
- [ ] Messages display in chronological order
- [ ] User messages right-aligned with blue background
- [ ] AI messages left-aligned with gray background
- [ ] Timestamps display for all messages
- [ ] Chat history persists during session
- [ ] Scroll position maintained when appropriate

### AC-5: Error Handling
- [ ] Network errors display user-friendly message
- [ ] Rate limit errors show specific wait time
- [ ] Retry mechanism works for failed requests
- [ ] Input validation errors display inline
- [ ] Error messages clear after successful action
- [ ] App remains functional after errors

### AC-6: Accessibility
- [ ] All interactive elements keyboard navigable
- [ ] ARIA labels present on all controls
- [ ] Screen reader announces new messages
- [ ] Color contrast meets WCAG AA standards
- [ ] Focus indicators clearly visible
- [ ] No keyboard traps present

### AC-7: Mobile Responsiveness
- [ ] Chat interface works on 320px width screens
- [ ] Touch targets minimum 44px size
- [ ] Input area remains accessible (no keyboard hiding)
- [ ] Messages readable without horizontal scroll
- [ ] All features work on touch devices
- [ ] Safe area insets respected on iOS devices

## Testing Strategy

### Unit Tests

**Backend Tests (pytest):**
- `test_valid_chat_request()` - Valid message returns proper response
- `test_missing_message()` - Missing message returns 400 error
- `test_invalid_coach_type()` - Invalid coach_type returns 400 error
- `test_message_too_long()` - Message >2000 chars returns 400 error
- `test_openai_error_handling()` - OpenAI errors handled gracefully
- `test_response_format()` - Response matches schema
- `test_rate_limiting()` - Rate limits enforced correctly

**Frontend Tests (Jest + React Testing Library):**
- `test_input_state_updates()` - Input value updates correctly
- `test_send_button_disabled_when_empty()` - Button disabled for empty input
- `test_enter_key_sends_message()` - Enter key triggers send
- `test_message_display()` - Messages render with correct styling
- `test_loading_state()` - Loading indicator shows during API call
- `test_error_display()` - Errors display user-friendly messages
- `test_character_counter()` - Character counter accurate
- `test_markdown_rendering()` - Markdown formatted correctly

### Integration Tests

**Backend Integration:**
- `test_full_chat_flow()` - Complete request/response cycle
- `test_concurrent_requests()` - Multiple users handled correctly
- `test_openai_integration()` - Real OpenAI API integration
- `test_error_recovery()` - System recovers from failures

**Frontend Integration:**
- `test_api_route_integration()` - Frontend API route works
- `test_message_flow_end_to_end()` - Full user journey
- `test_error_scenarios()` - All error paths covered
- `test_session_persistence()` - State persists correctly

### Manual Testing

**Functional Testing:**
- Complete chat conversation (5+ messages)
- Test all error scenarios manually
- Verify UI/UX on multiple devices
- Test accessibility with screen reader
- Performance testing (response times)

**Browser Compatibility:**
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

### Test Data

**Valid Messages:**
- "What's a good workout for beginners?"
- "How many calories should I eat per day?"
- Multi-line message with line breaks
- Message with special characters (!@#$%)

**Invalid Inputs:**
- Empty string
- Whitespace only
- 2001+ character message
- SQL injection attempt
- XSS script tags

## Security Considerations

### Input Validation

**Frontend Validation:**
- Maximum length: 2000 characters
- Trim whitespace before sending
- Sanitize for XSS (React handles by default)
- Disable during processing to prevent double-submit

**Backend Validation:**
- Pydantic schema validation
- SQL injection prevention (parameterized queries)
- HTML/script tag stripping
- Length and format validation

### Rate Limiting

**Implementation:**
- 20 requests per minute per user
- Token bucket algorithm
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- 429 response with `Retry-After` header

**Rate Limit Bypass Prevention:**
- IP-based tracking (with X-Forwarded-For validation)
- User ID tracking (if authenticated)
- Distributed rate limiting (Redis) for production

### Authentication & Authorization

**Current Increment:**
- No authentication required (MVP)
- Session-based tracking for rate limiting

**Future Increments:**
- JWT-based authentication
- User-specific conversation history
- Role-based access control

### Data Privacy

**Current Scope:**
- No conversation storage (stateless)
- No personal data collected
- HTTPS only in production

**Future Considerations:**
- Conversation encryption at rest
- Data retention policies
- GDPR compliance for user data
- Opt-out mechanisms

### API Security

**Best Practices:**
- CORS configured properly
- OpenAI API key secured (environment variables)
- Error messages don't leak sensitive info
- Request/response logging (without sensitive data)

## References

### Related Documents
- [INCREMENTAL_BUILD_PLAN.md](../../INCREMENTAL_BUILD_PLAN.md) - Overall build strategy
- [Backend Coach Service](../../fitness-backend/app/services/coach_service.py) - Existing implementation
- [Backend Coach API](../../fitness-backend/app/api/v1/coach.py) - API endpoint code
- [Test Configuration](../../fitness-backend/tests/conftest.py) - Test setup

### External Resources
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Next.js App Router](https://nextjs.org/docs/app)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

### Design Decisions Log

**Decision 1: Stateless Initial Implementation**
- Rationale: Simplify MVP, reduce database dependencies
- Trade-off: No conversation persistence between sessions
- Future: Add database storage in Increment 3

**Decision 2: OpenAI for AI Responses**
- Rationale: High-quality responses, reliable service
- Trade-off: External dependency, API costs
- Alternative considered: Local LLM (rejected for quality)

**Decision 3: Next.js API Routes**
- Rationale: Secure API key handling, server-side logic
- Trade-off: Additional API layer complexity
- Alternative: Direct frontend-to-backend (rejected for security)

**Decision 4: Session-based Rate Limiting**
- Rationale: Simple implementation, works without auth
- Trade-off: Can be bypassed with new sessions
- Future: IP + User ID based limiting

---

**Document Status:** Ready for Implementation
**Next Steps:** Review with team → Create test plan → Begin development
