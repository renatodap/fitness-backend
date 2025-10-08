# Auto-Log Preference Implementation - COMPLETE

## Summary

Successfully implemented dual-mode logging system for Wagner Coach that allows users to choose between:
1. **Preview Mode** (default): Review logs before saving
2. **Auto-Save Mode**: Logs saved immediately, edit later

## What Was Built

### 1. Database Migration (`migrations/012_add_auto_log_preference.sql`)
- Added `auto_log_enabled` BOOLEAN column to `profiles` table (default: FALSE)
- Added index for efficient lookups
- Includes UP and DOWN migrations

### 2. Enhanced Tool Service (`app/services/tool_service.py`)
Modified 3 proactive logging tools to support dual-mode:

#### `create_meal_log_from_description`
```python
# Checks user preference
auto_log_enabled = profile_response.data.get("auto_log_enabled", False)

if auto_log_enabled:
    # Save to database immediately
    meal_id = await self._save_meal_to_database(...)
    return {"success": True, "auto_logged": True, "meal_id": meal_id, ...}
else:
    # Return preview for user confirmation
    return {"success": True, "requires_confirmation": True, "meal_data": {...}}
```

#### `create_activity_log_from_description`
- Same dual-mode logic for activity logging
- Saves to `activity_logs` table when auto_log=TRUE
- Returns preview when auto_log=FALSE

#### `create_body_measurement_log`
- Same dual-mode logic for body measurements
- Saves to `body_measurements` table when auto_log=TRUE
- Returns preview when auto_log=FALSE

### 3. Response Aggregation (`app/services/unified_coach_service.py`)
Enhanced the agentic chat handler to aggregate tool results:

```python
# Lines 453-485: Aggregate logging tool results
pending_logs = []  # For auto_log=FALSE
auto_logged_items = []  # For auto_log=TRUE

for tool_call in tool_calls_made:
    full_result = tool_call.get("full_result", {})

    if full_result.get("requires_confirmation"):
        pending_logs.append({
            "log_type": full_result.get("log_type"),
            "data": full_result.get("meal_data") or full_result.get("activity_data"),
            "message": full_result.get("message")
        })

    elif full_result.get("auto_logged"):
        auto_logged_items.append({
            "log_type": full_result.get("log_type"),
            "id": full_result.get("meal_id") or full_result.get("activity_id"),
            "message": full_result.get("message")
        })
```

### 4. Enhanced API Response
The `/coach/chat` endpoint now returns:

```json
{
  "success": true,
  "message": "AI response text...",
  "tools_used": ["create_meal_log_from_description", "create_activity_log_from_description"],

  // If auto_log_enabled=FALSE:
  "pending_logs": [
    {
      "log_type": "meal",
      "data": {
        "meal_type": "breakfast",
        "foods": ["eggs", "toast"],
        "calories": 450,
        ...
      },
      "message": "Breakfast logged: eggs, toast (450 cal)"
    },
    {
      "log_type": "activity",
      "data": {
        "activity_type": "running",
        "distance_km": 5.0,
        ...
      },
      "message": "Activity logged: 5.0 km run"
    }
  ],

  // If auto_log_enabled=TRUE:
  "auto_logged": [
    {
      "log_type": "meal",
      "id": "uuid-meal-1",
      "message": "Breakfast auto-logged: eggs, toast"
    },
    {
      "log_type": "activity",
      "id": "uuid-activity-1",
      "message": "Activity auto-logged: 5.0 km run"
    }
  ]
}
```

## How It Works

### User Flow 1: Preview Mode (auto_log_enabled=FALSE, default)

1. User says: "for breakfast i had eggs and toast, then i did a 5k run"
2. Claude detects 2 log-worthy items, calls:
   - `create_meal_log_from_description(meal_type="breakfast", foods=["eggs", "toast"])`
   - `create_activity_log_from_description(activity_type="running", distance_km=5)`
3. Both tools check `auto_log_enabled` → FALSE
4. Both tools return `requires_confirmation=True` with preview data
5. Response includes `pending_logs` array with 2 items
6. Frontend shows preview cards sequentially:
   - Show first preview card
   - User reviews/edits
   - User confirms → Save to DB → Show next card
7. User can edit any data before saving

### User Flow 2: Auto-Save Mode (auto_log_enabled=TRUE)

1. User says: "for breakfast i had eggs and toast, then i did a 5k run"
2. Claude detects 2 log-worthy items, calls same tools
3. Both tools check `auto_log_enabled` → TRUE
4. Both tools SAVE TO DATABASE immediately
5. Both tools return `auto_logged=True` with IDs
6. Response includes `auto_logged` array with 2 items
7. Frontend shows success toast: "2 logs saved! View in nutrition/activities"
8. User can navigate to logs and edit if needed

## Multi-Log Support

The system handles complex messages like:
```
"for breakfast i had eggs and toast (500 cal),
then i did a 5k run in 28 minutes,
then i ate chicken and rice for lunch (650 cal),
then i weighed myself at 185 lbs"
```

Claude will call:
1. `create_meal_log_from_description` (breakfast)
2. `create_activity_log_from_description` (run)
3. `create_meal_log_from_description` (lunch)
4. `create_body_measurement_log` (weight)

Result:
- **Preview mode**: 4 items in `pending_logs` → Review one by one
- **Auto-save mode**: 4 items in `auto_logged` → All saved, show count

## Backend Status: ✅ COMPLETE

All backend implementation is done:
- ✅ Database migration created
- ✅ Tool service modified for dual-mode
- ✅ Response aggregation implemented
- ✅ Proper error handling
- ✅ Structured logging
- ✅ Security (user_id validation)

## Testing Status: ⏳ PENDING MIGRATION

### To Test:
1. **Apply Migration** (see `apply_migration.py` for instructions)
2. **Run Test Script**:
   ```bash
   # Update TEST_USER_ID in test_auto_log_flows.py
   python test_auto_log_flows.py
   ```

### Manual Test Plan:

#### Test 1: Preview Mode (auto_log=FALSE)
```bash
# 1. Set preference
UPDATE profiles SET auto_log_enabled = FALSE WHERE id = 'test-user-id';

# 2. Send message via /coach/chat
POST /api/v1/coach/chat
{
  "message": "for breakfast i had eggs, then i did a 5k run",
  "mode": "chat"
}

# 3. Verify response has pending_logs (not auto_logged)
# Expected:
{
  "pending_logs": [
    {"log_type": "meal", "data": {...}},
    {"log_type": "activity", "data": {...}}
  ],
  "auto_logged": []  // Should be empty
}

# 4. Check database - NO new rows yet (user hasn't confirmed)
SELECT * FROM meal_logs WHERE user_id = 'test-user-id' ORDER BY created_at DESC LIMIT 1;
SELECT * FROM activity_logs WHERE user_id = 'test-user-id' ORDER BY created_at DESC LIMIT 1;
```

#### Test 2: Auto-Save Mode (auto_log=TRUE)
```bash
# 1. Set preference
UPDATE profiles SET auto_log_enabled = TRUE WHERE id = 'test-user-id';

# 2. Send same message
POST /api/v1/coach/chat
{
  "message": "for breakfast i had eggs, then i did a 5k run",
  "mode": "chat"
}

# 3. Verify response has auto_logged (not pending_logs)
# Expected:
{
  "pending_logs": [],  // Should be empty
  "auto_logged": [
    {"log_type": "meal", "id": "uuid-1", "message": "..."},
    {"log_type": "activity", "id": "uuid-2", "message": "..."}
  ]
}

# 4. Check database - SHOULD have new rows immediately
SELECT * FROM meal_logs WHERE user_id = 'test-user-id' ORDER BY created_at DESC LIMIT 1;
-- Should return the breakfast log

SELECT * FROM activity_logs WHERE user_id = 'test-user-id' ORDER BY created_at DESC LIMIT 1;
-- Should return the 5k run log
```

## Frontend TODO (Not Started)

The frontend needs to implement:

### 1. Settings Toggle
```tsx
// In settings page
<Switch
  checked={autoLogEnabled}
  onCheckedChange={async (enabled) => {
    await updateProfile({ auto_log_enabled: enabled });
  }}
/>
<Label>
  Auto-log meals and activities
  <p className="text-sm text-muted-foreground">
    When enabled, logs are saved immediately without review.
    When disabled, you can review and edit before saving.
  </p>
</Label>
```

### 2. Handle pending_logs Response
```tsx
// In UnifiedCoachClient component
useEffect(() => {
  if (response.pending_logs?.length > 0) {
    // Show preview cards sequentially
    setCurrentPreviewIndex(0);
    setShowPreviewModal(true);
  }
}, [response]);

// Preview modal
<PreviewModal
  log={response.pending_logs[currentPreviewIndex]}
  onConfirm={async (editedData) => {
    // Save to database
    await saveMealLog(editedData);

    // Show next preview or close
    if (currentPreviewIndex < response.pending_logs.length - 1) {
      setCurrentPreviewIndex(currentPreviewIndex + 1);
    } else {
      setShowPreviewModal(false);
    }
  }}
  onSkip={() => {
    // Move to next without saving
    if (currentPreviewIndex < response.pending_logs.length - 1) {
      setCurrentPreviewIndex(currentPreviewIndex + 1);
    } else {
      setShowPreviewModal(false);
    }
  }}
/>
```

### 3. Handle auto_logged Response
```tsx
// In UnifiedCoachClient component
useEffect(() => {
  if (response.auto_logged?.length > 0) {
    // Show success toast
    toast.success(
      `${response.auto_logged.length} logs saved!`,
      {
        action: {
          label: "View",
          onClick: () => router.push("/nutrition/log")
        }
      }
    );
  }
}, [response]);
```

## Files Modified

### Backend
- ✅ `wagner-coach-backend/migrations/012_add_auto_log_preference.sql` (NEW)
- ✅ `wagner-coach-backend/app/services/tool_service.py` (MODIFIED)
  - Lines 420-527: `create_meal_log_from_description` - Added dual-mode logic
  - Lines 531-634: `create_activity_log_from_description` - Added dual-mode logic
  - Lines 638-720: `create_body_measurement_log` - Added dual-mode logic
- ✅ `wagner-coach-backend/app/services/unified_coach_service.py` (MODIFIED)
  - Lines 453-485: Added pending_logs vs auto_logged aggregation
  - Lines 530-538: Added arrays to response

### Test Files (NEW)
- ✅ `test_auto_log_flows.py` - Automated test script (needs migration + user ID)
- ✅ `apply_migration.py` - Migration instructions

### Frontend
- ⏳ `wagner-coach-clean/app/(dashboard)/coach/page.tsx` - Needs pending_logs handling
- ⏳ `wagner-coach-clean/components/unified-coach-client.tsx` - Needs both array handlers
- ⏳ `wagner-coach-clean/app/(dashboard)/settings/page.tsx` - Needs auto_log toggle

## Cost Impact

**Zero cost increase** for this feature:
- Uses existing Claude tool calling (already paid for)
- Database writes only happen when user confirms OR auto_log=TRUE
- No additional AI calls required
- Efficient indexing for preference lookup

## Architecture Benefits

1. **User Control**: Users choose their workflow (preview vs auto-save)
2. **No Data Loss**: Multi-log messages properly detected and handled
3. **Backward Compatible**: Default behavior (preview) matches old system
4. **Scalable**: Can handle 10+ logs in one message
5. **Cost Efficient**: No additional AI calls needed
6. **Secure**: All logs validated with user_id
7. **Flexible**: Frontend can render previews any way they want

## Next Steps

1. **Apply Migration**:
   ```sql
   -- Run in Supabase SQL Editor
   ALTER TABLE profiles
   ADD COLUMN IF NOT EXISTS auto_log_enabled BOOLEAN DEFAULT FALSE;

   CREATE INDEX IF NOT EXISTS idx_profiles_auto_log_enabled
   ON profiles(auto_log_enabled) WHERE auto_log_enabled = TRUE;
   ```

2. **Test Backend** (run `test_auto_log_flows.py` after migration)

3. **Implement Frontend**:
   - Add settings toggle
   - Handle `pending_logs` array (show preview cards)
   - Handle `auto_logged` array (show success toast)

4. **Deploy**:
   - Backend: Push to Railway (migration will auto-apply)
   - Frontend: Deploy after implementing response handlers

## Questions?

- **Q**: What if user has auto_log=TRUE but wants to review a specific log?
  - **A**: They can edit it after saving. Future enhancement: Add "review before saving" button in coach UI

- **Q**: What if API call fails during auto-save?
  - **A**: Error is returned in response, log is NOT saved, user can retry

- **Q**: Can users change preference mid-conversation?
  - **A**: Yes, preference is checked PER MESSAGE, not per conversation

- **Q**: What about batch confirmation for multiple logs?
  - **A**: Future enhancement. Current: sequential review (one at a time)

---

**Status**: Backend implementation COMPLETE ✅
**Next**: Apply migration → Test → Implement frontend
