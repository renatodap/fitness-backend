# INCREMENT 1: Manual Testing Checklist

## Document Information
- **Increment**: 1
- **Feature**: Basic Coach Chat
- **Version**: 1.0
- **Last Updated**: 2025-10-01
- **Tester**: ________________
- **Test Date**: ________________

---

## Test Environment Setup

### Prerequisites
- [ ] Backend running on http://localhost:8000 (or production URL)
- [ ] Frontend running on http://localhost:3000 (or production URL)
- [ ] Valid Supabase account with test user
- [ ] OpenAI API key configured
- [ ] Browser DevTools open (F12)

### Test User Credentials
- **Email**: ________________
- **Password**: ________________
- **User ID**: ________________

---

## 1. Functional Tests

### Test 1.1: Page Load and Initial State
**Description**: Verify chat page loads correctly with empty state

**Steps**:
1. Navigate to `/coach/trainer`
2. Observe initial page state
3. Check browser console for errors

**Expected Result**:
- [ ] Page loads without errors (no 404, 500, etc.)
- [ ] Header displays "Chat with Coach Alex"
- [ ] Subtitle shows "Your AI fitness trainer"
- [ ] Welcome message appears in chat area
- [ ] Input field is auto-focused (cursor blinking)
- [ ] Send button is disabled
- [ ] Character counter shows "0/1000"
- [ ] No JavaScript errors in console

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 1.2: Send Valid Message
**Description**: Verify user can send a message and receive AI response

**Steps**:
1. Type message in input field: "What's a good workout for beginners?"
2. Click Send button (or press Enter)
3. Wait for AI response
4. Observe message flow

**Expected Result**:
- [ ] User message appears immediately (blue bubble, right-aligned)
- [ ] Message shows timestamp (e.g., "2:30 PM")
- [ ] Input field clears automatically
- [ ] Loading indicator appears (three bouncing dots)
- [ ] Loading indicator is left-aligned with gray background
- [ ] AI response appears within 5 seconds
- [ ] AI response is left-aligned with gray background
- [ ] AI response has timestamp
- [ ] Chat auto-scrolls to bottom
- [ ] Send button re-enabled after response
- [ ] Input field re-enabled after response

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 1.3: Multiple Messages (Conversation Flow)
**Description**: Verify multiple messages work in sequence

**Steps**:
1. Send message: "What muscles does squatting work?"
2. Wait for response
3. Send follow-up: "How many sets should I do?"
4. Wait for response
5. Send third message: "What about rest days?"

**Expected Result**:
- [ ] All messages display in chronological order
- [ ] User messages always right-aligned (blue)
- [ ] AI messages always left-aligned (gray)
- [ ] Each message has unique timestamp
- [ ] Conversation history persists (no messages disappear)
- [ ] Auto-scroll works for each new message
- [ ] No duplicate messages
- [ ] No memory errors or slowdowns

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 1.4: Enter Key to Send
**Description**: Verify Enter key sends message

**Steps**:
1. Type message: "How do I build muscle?"
2. Press Enter key (not Shift+Enter)
3. Observe behavior

**Expected Result**:
- [ ] Enter key sends the message
- [ ] Same behavior as clicking Send button
- [ ] Message appears, loading shows, response received

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 1.5: Shift+Enter for New Line
**Description**: Verify Shift+Enter creates new line without sending

**Steps**:
1. Type: "I have two questions:"
2. Press Shift+Enter
3. Type: "1. What's a good warmup?"
4. Press Shift+Enter
5. Type: "2. How long should I train?"
6. Press Enter (without Shift)

**Expected Result**:
- [ ] Shift+Enter creates new line in textarea
- [ ] Message NOT sent on Shift+Enter
- [ ] Final Enter (without Shift) sends the message
- [ ] Multi-line message displays correctly
- [ ] Line breaks preserved in sent message

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 1.6: Empty Message Prevention
**Description**: Verify empty messages cannot be sent

**Steps**:
1. Leave input field empty
2. Try to click Send button
3. Type only spaces: "     "
4. Try to click Send button
5. Type only newlines (multiple Enter with Shift)

**Expected Result**:
- [ ] Send button disabled when input empty
- [ ] Send button disabled for whitespace-only
- [ ] Send button disabled for newlines-only
- [ ] Clicking disabled button does nothing
- [ ] No API call made for empty input

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 1.7: Character Limit Enforcement
**Description**: Verify 1000 character limit is enforced

**Steps**:
1. Type or paste exactly 1000 characters
2. Observe character counter
3. Try to type more characters
4. Verify message can be sent

**Expected Result**:
- [ ] Counter shows "1000/1000"
- [ ] Input stops accepting characters at 1000
- [ ] Cannot type beyond 1000 characters
- [ ] Cannot paste beyond 1000 (truncates)
- [ ] Send button remains enabled
- [ ] Message sends successfully

**Test Data**: Use this 1000-char string:
```
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliq.
```

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 1.8: Error Handling - Network Failure
**Description**: Verify error handling when backend is unreachable

**Steps**:
1. Stop the backend server (or disconnect internet)
2. Type message: "Test error handling"
3. Click Send
4. Observe error behavior
5. Restart backend
6. Try sending again

**Expected Result**:
- [ ] Error message displays (red banner)
- [ ] Error text is user-friendly (no technical jargon)
- [ ] Optimistic message is removed (blue bubble disappears)
- [ ] Input field restored with original text
- [ ] User can edit and retry message
- [ ] After backend restarts, message sends successfully
- [ ] Error message disappears on success

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 1.9: Error Handling - Backend Error (500)
**Description**: Verify error handling for server errors

**Steps**:
1. (If possible) Trigger a 500 error from backend
2. OR remove OpenAI API key to cause backend error
3. Send a message
4. Observe error behavior

**Expected Result**:
- [ ] Error message displays
- [ ] Message indicates service issue
- [ ] App remains functional (no crash)
- [ ] Can try sending other messages

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 1.10: Special Characters in Message
**Description**: Verify special characters are handled correctly

**Steps**:
1. Send message with special chars: "What's the #1 tip for building muscle? (asking for a friend!)"
2. Send message with emojis: "How do I get stronger? 💪🏋️"
3. Send message with symbols: "@Coach, I need help with $nutrition & *workouts*"

**Expected Result**:
- [ ] All special characters display correctly
- [ ] Emojis render properly (if supported)
- [ ] No encoding issues (no � characters)
- [ ] AI responds appropriately to content
- [ ] Special chars don't break UI layout

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

## 2. UI/UX Tests

### Test 2.1: Button States
**Description**: Verify all button states work correctly

**Steps**:
1. Observe Send button when input empty (disabled state)
2. Type text and observe enabled state
3. Hover over enabled button
4. Click button and observe loading state
5. Observe button after response (enabled again)

**Expected Result**:
- [ ] Disabled state: Gray background, cursor "not-allowed"
- [ ] Enabled state: Blue background, cursor "pointer"
- [ ] Hover state: Darker blue, slight scale effect
- [ ] Loading state: Shows "Sending...", disabled
- [ ] No flickering or state glitches

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 2.2: Loading Indicators
**Description**: Verify loading states are clear and accurate

**Steps**:
1. Send a message
2. Watch for loading indicator
3. Time how long it displays
4. Verify it disappears when response arrives

**Expected Result**:
- [ ] Loading dots appear immediately after send
- [ ] Three dots with bouncing animation
- [ ] Animation is smooth (no stuttering)
- [ ] Staggered bounce (not synchronized)
- [ ] Disappears when AI response arrives
- [ ] Only one loading indicator at a time

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 2.3: Message Styling
**Description**: Verify message bubbles are styled correctly

**Steps**:
1. Send several user messages
2. Receive several AI responses
3. Compare styling

**Expected Result**:
**User Messages:**
- [ ] Blue background (#3B82F6 or similar)
- [ ] White text
- [ ] Right-aligned
- [ ] Rounded corners
- [ ] Adequate padding
- [ ] Readable font size

**AI Messages:**
- [ ] Gray background (#F3F4F6 or similar)
- [ ] Dark text
- [ ] Left-aligned
- [ ] Rounded corners
- [ ] Adequate padding
- [ ] Readable font size

**Both:**
- [ ] Timestamps in smaller, lighter text
- [ ] Max width ~80% of container
- [ ] Proper spacing between messages
- [ ] Text wraps correctly (no overflow)

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 2.4: Scroll Behavior
**Description**: Verify auto-scroll works correctly

**Steps**:
1. Send 10+ messages to fill chat area
2. Scroll up to read earlier messages
3. Send a new message while scrolled up
4. Observe scroll behavior

**Expected Result**:
- [ ] Auto-scrolls to bottom on new message
- [ ] Smooth scroll animation (not instant jump)
- [ ] Manual scroll position maintained when appropriate
- [ ] Can scroll up to read history
- [ ] Scroll bar appears when content overflows
- [ ] Scroll doesn't jump erratically

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 2.5: Input Field Behavior
**Description**: Verify textarea input works properly

**Steps**:
1. Type short message (one line)
2. Type long message (multiple lines)
3. Paste text from clipboard
4. Use keyboard shortcuts (Ctrl+A, Ctrl+C, Ctrl+V)

**Expected Result**:
- [ ] Textarea auto-resizes for content (or scrolls internally)
- [ ] Starts at 2 rows height
- [ ] Copy/paste works correctly
- [ ] Keyboard shortcuts function normally
- [ ] Placeholder text shows when empty
- [ ] Placeholder disappears when typing
- [ ] Text cursor visible and blinking

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 2.6: Error Message Display
**Description**: Verify error messages are clear and dismissible

**Steps**:
1. Trigger an error (stop backend)
2. Observe error banner
3. Send successful message
4. Verify error dismisses

**Expected Result**:
- [ ] Error banner appears above input area
- [ ] Red background with red border
- [ ] Red text, readable font
- [ ] Error message is user-friendly
- [ ] Error auto-dismisses on successful action
- [ ] Error doesn't block interaction with chat

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 2.7: Visual Hierarchy
**Description**: Verify page layout and visual priority

**Steps**:
1. View the page at a glance
2. Identify primary, secondary, tertiary elements
3. Assess visual flow

**Expected Result**:
- [ ] Header is clearly visible (not too prominent)
- [ ] Chat area is primary focus (largest, centered)
- [ ] Input area is easily accessible (bottom, fixed)
- [ ] Character counter subtle but visible
- [ ] Colors have proper contrast (readable)
- [ ] No visual clutter or distractions
- [ ] Professional, clean appearance

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

## 3. Accessibility Tests

### Test 3.1: Keyboard Navigation
**Description**: Verify full keyboard accessibility

**Steps**:
1. Use only keyboard (no mouse)
2. Tab through all elements
3. Navigate to input field
4. Type and send message using Enter
5. Try Shift+Tab to go backwards

**Expected Result**:
- [ ] Tab key moves focus through all interactive elements
- [ ] Focus indicators clearly visible (blue outline)
- [ ] Tab order is logical (header → messages → input → button)
- [ ] Can reach all clickable elements via Tab
- [ ] Shift+Tab goes backwards correctly
- [ ] No keyboard traps (can always navigate out)
- [ ] Enter sends message from input field

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 3.2: Screen Reader Compatibility
**Description**: Verify page works with screen readers (basic test)

**Steps**:
1. Enable screen reader (NVDA, JAWS, or VoiceOver)
2. Navigate to chat page
3. Listen to announcements
4. Try sending a message

**Expected Result**:
- [ ] Page title announced correctly
- [ ] Header text read aloud
- [ ] Input field labeled properly ("Ask your trainer...")
- [ ] Button label read ("Send" or "Sending...")
- [ ] New messages announced (ideally)
- [ ] Error messages announced
- [ ] ARIA labels present (check DevTools)

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 3.3: Color Contrast
**Description**: Verify sufficient color contrast for readability

**Steps**:
1. Use browser DevTools or online contrast checker
2. Check user message text (white on blue)
3. Check AI message text (dark on gray)
4. Check error text (red on light red)

**Expected Result**:
- [ ] User messages: Contrast ratio ≥ 4.5:1 (WCAG AA)
- [ ] AI messages: Contrast ratio ≥ 4.5:1
- [ ] Error messages: Contrast ratio ≥ 4.5:1
- [ ] All text readable without strain
- [ ] No color-only indicators (use text/icons too)

**Tool**: https://webaim.org/resources/contrastchecker/

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 3.4: Focus Management
**Description**: Verify focus is managed correctly

**Steps**:
1. Type message and send
2. Observe where focus goes after send
3. Send message with Enter key
4. Check focus after response arrives

**Expected Result**:
- [ ] Focus returns to input field after send
- [ ] Can immediately type next message
- [ ] No need to click back into input
- [ ] Focus visible at all times
- [ ] Focus doesn't jump unexpectedly

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 3.5: Reduced Motion
**Description**: Verify animations respect prefers-reduced-motion

**Steps**:
1. Enable reduced motion in OS settings
   - Windows: Settings → Accessibility → Visual effects → Off
   - macOS: System Preferences → Accessibility → Display → Reduce motion
2. Reload page
3. Send messages and observe animations

**Expected Result**:
- [ ] Animations reduced or disabled
- [ ] Scroll still works (instant instead of smooth)
- [ ] Loading indicator still visible (no animation)
- [ ] Page remains functional
- [ ] No jarring motion

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

## 4. Mobile Responsiveness Tests

### Test 4.1: Mobile Phone (iPhone SE / Small Android)
**Description**: Verify functionality on small mobile screens

**Device**: iPhone SE (375×667) or similar

**Steps**:
1. Open on device or use Chrome DevTools device emulation
2. Navigate to `/coach/trainer`
3. Test full chat flow

**Expected Result**:
- [ ] Page fits screen width (no horizontal scroll)
- [ ] Header readable and not cut off
- [ ] Messages display correctly
- [ ] Input field accessible
- [ ] Send button reachable
- [ ] Virtual keyboard doesn't hide input
- [ ] Touch targets ≥ 44×44 pixels
- [ ] Text readable without zooming
- [ ] All features functional

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 4.2: Tablet (iPad)
**Description**: Verify tablet experience

**Device**: iPad (768×1024) or similar

**Steps**:
1. Open on device or use browser emulation
2. Test in portrait and landscape
3. Complete chat flow

**Expected Result**:
- [ ] Layout adapts to tablet size
- [ ] Adequate spacing and padding
- [ ] Messages not too wide or narrow
- [ ] Comfortable reading experience
- [ ] Both orientations work well
- [ ] Touch interactions smooth

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 4.3: Large Android Phone
**Description**: Verify on larger mobile devices

**Device**: Pixel 5 (393×851) or similar

**Steps**:
1. Open on device or emulator
2. Test chat functionality
3. Check layout and spacing

**Expected Result**:
- [ ] Layout optimized for larger screen
- [ ] One-handed usage comfortable
- [ ] Messages well-spaced
- [ ] Input accessible at bottom
- [ ] No wasted space
- [ ] Responsive to device size

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 4.4: Virtual Keyboard Handling
**Description**: Verify virtual keyboard doesn't break layout

**Steps**:
1. On mobile device, tap input field
2. Observe virtual keyboard appearance
3. Type a message
4. Send message
5. Observe keyboard dismissal

**Expected Result**:
- [ ] Keyboard appears smoothly
- [ ] Input field remains visible above keyboard
- [ ] Can see at least the last message
- [ ] Can scroll to see more messages
- [ ] Layout doesn't break when keyboard appears
- [ ] Keyboard dismisses after send
- [ ] Layout restores correctly

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

## 5. Browser Compatibility Tests

### Test 5.1: Chrome (Latest)
**Description**: Verify full functionality in Chrome

**Browser Version**: ________________

**Steps**:
1. Open in Chrome
2. Complete full chat flow
3. Check DevTools console

**Expected Result**:
- [ ] All features work perfectly
- [ ] No console errors
- [ ] No console warnings
- [ ] Animations smooth
- [ ] Styles render correctly

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 5.2: Firefox (Latest)
**Description**: Verify compatibility with Firefox

**Browser Version**: ________________

**Steps**:
1. Open in Firefox
2. Complete full chat flow
3. Check browser console

**Expected Result**:
- [ ] All features work correctly
- [ ] No console errors or warnings
- [ ] Animations work
- [ ] Layout identical to Chrome
- [ ] No Firefox-specific issues

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

### Test 5.3: Safari (Latest)
**Description**: Verify compatibility with Safari

**Browser Version**: ________________

**Steps**:
1. Open in Safari (macOS or iOS)
2. Complete full chat flow
3. Check Web Inspector console

**Expected Result**:
- [ ] All features work correctly
- [ ] No console errors or warnings
- [ ] Animations smooth
- [ ] Touch interactions work (iOS)
- [ ] No Safari-specific rendering issues

**Actual Result**: ________________

**Status**: ⬜ Pass | ⬜ Fail | ⬜ Blocked

**Notes**: ________________

---

## Test Summary

### Overall Statistics
- **Total Tests**: 29
- **Tests Passed**: _____ / 29
- **Tests Failed**: _____ / 29
- **Tests Blocked**: _____ / 29
- **Pass Rate**: _____ %

### Critical Issues Found
1. ________________
2. ________________
3. ________________

### Minor Issues Found
1. ________________
2. ________________
3. ________________

### Recommendations
1. ________________
2. ________________
3. ________________

### Sign-Off

**Tested By**: ________________
**Date**: ________________
**Signature**: ________________

**Approved By**: ________________
**Date**: ________________
**Signature**: ________________

---

## Appendix: Test Data

### Sample Messages for Testing
```
1. "What's a good workout for beginners?"
2. "How many calories should I eat per day?"
3. "Can you create a workout plan for me?"
4. "What muscles does squatting work?"
5. "How do I stay motivated to exercise?"
6. "What's the best time to work out?"
7. "Should I do cardio before or after weights?"
8. "How much protein do I need?"
9. "What are compound exercises?"
10. "How do I prevent workout injuries?"
```

### Edge Case Messages
```
1. "x" (single character)
2. "     " (whitespace only)
3. "\n\n\n" (newlines only)
4. "What's the #1 tip? 💪" (special chars + emoji)
5. [1000 character lorem ipsum - see Test 1.7]
6. "'; DROP TABLE users; --" (SQL injection attempt)
7. "<script>alert('xss')</script>" (XSS attempt)
```

### Expected Response Times
- **Page Load**: < 2 seconds
- **Message Send**: < 500ms (optimistic UI)
- **AI Response**: < 5 seconds (95th percentile)
- **Error Display**: Immediate

---

**Document Version**: 1.0
**Last Updated**: 2025-10-01
**Status**: Ready for Use
