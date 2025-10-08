# End-to-End Test Plan: Activity Logging with Exercises

## Overview
This document provides step-by-step testing instructions to verify that the complete activity logging flow works, especially for strength training with exercises and sets.

---

## Prerequisites

### 1. Backend Running
- Wagner Coach backend API running at `http://localhost:8000` or deployed URL
- Environment variables configured (SUPABASE_URL, SUPABASE_SERVICE_KEY, etc.)
- Database migrations applied

### 2. Frontend Running
- Wagner Coach frontend running at `http://localhost:3000` or deployed URL
- Environment variables configured (NEXT_PUBLIC_API_BASE_URL, NEXT_PUBLIC_SUPABASE_URL, etc.)
- User authenticated (logged in)

### 3. Database Access
- Access to Supabase dashboard or direct PostgreSQL client
- Can query tables: `activities`, `activity_exercises`, `activity_sets`

---

## Test Scenarios

### Test 1: Navigation Flow ✅

**Purpose:** Verify back button works from activity type selector to dashboard

**Steps:**
1. Log in to the application
2. Navigate to Dashboard
3. Click "Log Activity" (from quick actions or navigation)
4. **Verify:** You see the activity type selector screen
5. **Verify:** There's a back arrow (←) button in the header
6. Click the back arrow button
7. **Expected:** You return to the dashboard

**Pass Criteria:**
- ✅ Back button is visible in header
- ✅ Back button navigates to dashboard
- ✅ No console errors

---

### Test 2: Strength Training - Detailed Exercise Logging ✅

**Purpose:** Verify user can log a workout with multiple exercises, sets, reps, and weights

**Steps:**

#### Part A: Select Activity Type
1. Navigate to `/activities/log`
2. Select "Strength Training" activity type
3. **Verify:** Form appears with fields

#### Part B: Fill Basic Information
1. **Activity Name:** "Upper Body Workout"
2. **Date & Time:** Select today's date and current time
3. **Duration:** 60 minutes
4. **Location:** "24 Hour Fitness"
5. **Calories:** 350
6. **Perceived Exertion (RPE):** 7

#### Part C: Add Exercises with Sets

**Exercise 1: Bench Press**
1. Click "Add Exercise" button
2. **Verify:** Exercise card appears
3. Enter exercise name: "Bench Press"
4. Click "Add Set" button 3 times to add 3 sets
5. Fill in sets:
   - Set 1: 10 reps, 135 lbs, RPE 6
   - Set 2: 8 reps, 155 lbs, RPE 7
   - Set 3: 6 reps, 165 lbs, RPE 8

**Exercise 2: Overhead Press**
1. Click "Add Exercise" button (below previous exercise)
2. Enter exercise name: "Overhead Press"
3. Click "Add Set" button 3 times
4. Fill in sets:
   - Set 1: 10 reps, 95 lbs, RPE 6
   - Set 2: 8 reps, 105 lbs, RPE 7
   - Set 3: 8 reps, 105 lbs, RPE 8

**Exercise 3: Pull-ups**
1. Click "Add Exercise" button
2. Enter exercise name: "Pull-ups"
3. Click "Add Set" button 4 times
4. Fill in sets:
   - Set 1: 12 reps, 0 lbs (bodyweight), RPE 5
   - Set 2: 10 reps, 0 lbs, RPE 6
   - Set 3: 8 reps, 0 lbs, RPE 7
   - Set 4: 6 reps, 0 lbs, RPE 8

#### Part D: Test Weight Unit Toggle
1. Click the "KG" button at the top of the exercise builder
2. **Verify:** All weight values convert to kilograms (e.g., 135 lbs → 61.2 kg)
3. Click "LBS" button
4. **Verify:** Weights convert back to pounds

#### Part E: Fill Subjective Metrics (NEW!)
1. Scroll down to "How You Felt" section
2. **Mood:** Select "Good" (😊)
3. **Energy Level:** Select "4"
4. **Soreness Level:** Slide to "3"
5. **Overall Rating:** Select 4 stars (⭐⭐⭐⭐)

#### Part F: Fill Environment (NEW!)
1. **Indoor Activity:** Toggle ON (should turn orange)
2. **Verify:** Weather dropdown disappears (since it's indoor)

#### Part G: Add Notes
1. **Notes:** "Great workout! Felt strong on bench press PRs."

#### Part H: Submit
1. Click "Log Activity" button
2. **Verify:** Loading state appears (button disabled, "Logging..." text)
3. **Verify:** Success toast appears: "Activity Logged! Upper Body Workout has been logged successfully."
4. **Verify:** Redirects to `/activities` page

**Pass Criteria:**
- ✅ Can add multiple exercises
- ✅ Can add multiple sets per exercise
- ✅ Can input reps, weight, RPE for each set
- ✅ LBS/KG conversion works correctly
- ✅ Can remove sets (trash icon works)
- ✅ Can remove exercises (trash icon works)
- ✅ Subjective metrics fields visible and functional
- ✅ Indoor toggle works, hides weather conditionally
- ✅ Form submits successfully
- ✅ Success toast appears
- ✅ Redirects after success

---

### Test 3: Database Verification ✅

**Purpose:** Verify data is correctly saved to database with exercises and sets

**Steps:**

#### Part A: Query Activities Table
```sql
-- Find the activity we just created
SELECT
  id,
  user_id,
  activity_type,
  name,
  start_date,
  duration_minutes,
  location,
  calories,
  perceived_exertion,
  mood,
  energy_level,
  soreness_level,
  workout_rating,
  indoor,
  notes,
  created_at
FROM activities
WHERE name = 'Upper Body Workout'
ORDER BY created_at DESC
LIMIT 1;
```

**Expected Result:**
- ✅ Record exists
- ✅ `activity_type = 'strength_training'`
- ✅ `name = 'Upper Body Workout'`
- ✅ `duration_minutes = 60`
- ✅ `location = '24 Hour Fitness'`
- ✅ `calories = 350`
- ✅ `perceived_exertion = 7`
- ✅ `mood = 'good'`
- ✅ `energy_level = 4`
- ✅ `soreness_level = 3`
- ✅ `workout_rating = 4`
- ✅ `indoor = true`
- ✅ `notes` contains "Great workout..."

**Copy the `id` from this result for next queries.**

#### Part B: Query Activity Exercises Table
```sql
-- Replace 'ACTIVITY_ID_HERE' with the id from Part A
SELECT
  id,
  activity_id,
  exercise_name,
  order_index,
  notes,
  created_at
FROM activity_exercises
WHERE activity_id = 'ACTIVITY_ID_HERE'
ORDER BY order_index;
```

**Expected Result:**
- ✅ 3 records returned
- ✅ Record 1: `exercise_name = 'Bench Press'`, `order_index = 0`
- ✅ Record 2: `exercise_name = 'Overhead Press'`, `order_index = 1`
- ✅ Record 3: `exercise_name = 'Pull-ups'`, `order_index = 2`

**Copy the `id` values for each exercise for next query.**

#### Part C: Query Activity Sets Table
```sql
-- Bench Press sets
SELECT
  id,
  activity_exercise_id,
  set_number,
  reps_completed,
  weight_lbs,
  weight_kg,
  rpe,
  completed,
  created_at
FROM activity_sets
WHERE activity_exercise_id = 'BENCH_PRESS_EXERCISE_ID_HERE'
ORDER BY set_number;
```

**Expected Result for Bench Press:**
- ✅ 3 records returned
- ✅ Set 1: `reps_completed = 10`, `weight_lbs = 135`, `weight_kg = 61.23`, `rpe = 6`
- ✅ Set 2: `reps_completed = 8`, `weight_lbs = 155`, `weight_kg = 70.31`, `rpe = 7`
- ✅ Set 3: `reps_completed = 6`, `weight_lbs = 165`, `weight_kg = 74.84`, `rpe = 8`
- ✅ All sets: `completed = true`

**Repeat for Overhead Press and Pull-ups to verify their sets.**

**Pass Criteria:**
- ✅ Activity record exists with all fields
- ✅ 3 exercise records exist with correct names and order
- ✅ All sets exist with correct reps, weights, RPE
- ✅ Weight conversions are accurate (lbs ↔ kg)
- ✅ Foreign keys are correct (exercise_id references activity, set_id references exercise)

---

### Test 4: Cardio Activity (Baseline Check) ✅

**Purpose:** Verify cardio activities still work (no regression)

**Steps:**
1. Navigate to `/activities/log`
2. Select "Running" activity type
3. Fill in:
   - **Name:** "Morning Run"
   - **Date/Time:** Today
   - **Duration:** 45 minutes
   - **Distance:** 5.2 miles
   - **Average Pace:** "8:30"
   - **Elevation Gain:** 250 feet
   - **Average Heart Rate:** 155 bpm
   - **Calories:** 450
   - **RPE:** 7
   - **Location:** "Griffith Park"
   - **Mood:** "Amazing"
   - **Energy Level:** 5
   - **Indoor:** OFF
   - **Weather:** "Sunny"
   - **Notes:** "Perfect morning run!"
4. Click "Log Activity"

**Expected:**
- ✅ Form submits successfully
- ✅ Success toast appears
- ✅ Activity saved to database with cardio-specific fields

---

### Test 5: Edge Cases ✅

#### Test 5A: Empty Exercise
**Steps:**
1. Create strength training activity
2. Click "Add Exercise" but don't fill name
3. Click "Add Set" and fill set data
4. Try to submit

**Expected:**
- ✅ Form submits (exercise name is optional in backend schema)
- OR
- ✅ Frontend validation shows error (if validation added)

#### Test 5B: Exercise Without Sets
**Steps:**
1. Create strength training activity
2. Add exercise with name "Dead Hang"
3. Don't add any sets
4. Submit

**Expected:**
- ✅ Form submits successfully (sets are optional)
- ✅ Exercise exists in DB with 0 sets

#### Test 5C: Remove Exercise
**Steps:**
1. Create strength training activity
2. Add 3 exercises
3. Click trash icon on 2nd exercise
4. Verify only 2 exercises remain
5. Submit

**Expected:**
- ✅ Only 2 exercises saved to database
- ✅ order_index is re-indexed (0, 1 not 0, 2)

#### Test 5D: Remove Set
**Steps:**
1. Add exercise with 5 sets
2. Remove set #3
3. Verify sets are renumbered (1, 2, 3, 4 not 1, 2, 4, 5)

**Expected:**
- ✅ Set numbers are sequential after removal

---

## Error Scenarios to Test

### Error 1: Network Failure
**Steps:**
1. Disconnect internet or stop backend
2. Try to submit activity

**Expected:**
- ✅ Error toast appears: "Failed to log activity. Please try again."
- ✅ Form stays filled (doesn't lose data)
- ✅ Can retry after reconnecting

### Error 2: Authentication Expired
**Steps:**
1. Log out in another tab
2. Try to submit activity

**Expected:**
- ✅ Error appears: "Not authenticated" or "Token expired"
- ✅ Redirects to login page

### Error 3: Invalid Data
**Steps:**
1. Fill activity name with 500 characters (exceeds 200 max)
2. Submit

**Expected:**
- ✅ Backend returns 400 error with validation message
- ✅ Frontend shows error toast with explanation

---

## Accessibility Testing

### Keyboard Navigation
**Steps:**
1. Navigate to activity log page
2. Tab through all form fields
3. Verify focus indicators visible
4. Use Enter to add exercise
5. Use Tab/Shift+Tab to navigate between set inputs

**Pass Criteria:**
- ✅ All interactive elements are keyboard accessible
- ✅ Focus indicators visible (blue ring)
- ✅ Tab order is logical (top to bottom, left to right)
- ✅ Can submit form with Enter key

### Screen Reader (Optional)
**Steps:**
1. Enable VoiceOver (Mac) or NVDA (Windows)
2. Navigate through form
3. Verify all labels are read
4. Verify button purposes are clear

**Pass Criteria:**
- ✅ Input labels are announced
- ✅ Buttons have descriptive labels ("Add Exercise", "Remove Set")
- ✅ Set number is announced ("Set 1", "Set 2")

---

## Mobile Testing

### Responsive Design
**Steps:**
1. Open app on mobile device (or Chrome DevTools mobile view)
2. Navigate to activity log
3. Test at widths: 320px, 375px, 414px, 768px

**Pass Criteria:**
- ✅ Bottom navigation visible and functional
- ✅ Form fields are appropriately sized
- ✅ Buttons are large enough (min 44x44px)
- ✅ No horizontal scrolling
- ✅ Exercise builder table is readable on small screens

### Touch Interactions
**Steps:**
1. On mobile, tap "Add Exercise"
2. Tap set inputs
3. Use number inputs on mobile keyboard

**Pass Criteria:**
- ✅ Buttons respond to touch
- ✅ Mobile keyboard shows appropriate type (numeric for numbers)
- ✅ No accidental taps on wrong elements

---

## Performance Testing

### Load Time
**Steps:**
1. Clear browser cache
2. Navigate to `/activities/log`
3. Measure time to interactive

**Pass Criteria:**
- ✅ Page loads in < 2 seconds
- ✅ Form is interactive immediately
- ✅ No layout shifts while loading

### Large Workout
**Steps:**
1. Create strength training with 10 exercises
2. Add 5 sets to each exercise (50 total sets)
3. Submit

**Pass Criteria:**
- ✅ Form remains responsive while filling
- ✅ Submission completes in < 5 seconds
- ✅ No browser freezing

---

## Summary Checklist

After running all tests, verify:

- [ ] ✅ Back button works from activity type selector to dashboard
- [ ] ✅ Can create strength training activity with multiple exercises
- [ ] ✅ Can add multiple sets per exercise with reps, weight, RPE
- [ ] ✅ LBS/KG weight unit conversion works correctly
- [ ] ✅ Can remove exercises and sets (trash icons work)
- [ ] ✅ Subjective metrics section works (mood, energy, soreness, rating)
- [ ] ✅ Indoor toggle works and conditionally shows weather
- [ ] ✅ Form submits successfully with loading state
- [ ] ✅ Success toast appears with activity name
- [ ] ✅ Activity saved to `activities` table with all fields
- [ ] ✅ Exercises saved to `activity_exercises` table in correct order
- [ ] ✅ Sets saved to `activity_sets` table with accurate data
- [ ] ✅ Cardio activities still work (no regression)
- [ ] ✅ Error handling works (network errors, validation errors)
- [ ] ✅ Keyboard navigation works throughout form
- [ ] ✅ Mobile responsive design works (320px to 768px)
- [ ] ✅ Form performance is acceptable (no lag)

---

## Known Issues / Future Improvements

### Current Limitations:
1. Exercise drag-and-drop reordering not yet implemented (UI has grip icon but no functionality)
2. Auto-calculation of total_sets, total_reps, total_weight_lifted from exercises not implemented (backend can calculate)
3. No autocomplete for exercise names yet
4. No exercise history/suggestions from past workouts

### Future Enhancements:
1. Add exercise search/autocomplete from exercise database
2. Show previous performance for same exercise (last weight, reps)
3. Rest timer between sets
4. Progressive overload suggestions
5. Exercise form videos/instructions
6. Superset/circuit support
7. Export workout as PDF/share

---

## Contact for Issues

If any test fails, document:
1. Which test scenario
2. Expected vs actual result
3. Browser console errors
4. Network tab (if API error)
5. Screenshots if visual issue

Then report to development team with full details.

---

**Test Plan Version:** 1.0
**Created:** 2025-10-08
**Updated:** 2025-10-08
**Status:** Ready for Testing
