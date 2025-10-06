# THE LINE - Baseline Estimation Rules

## Purpose
This document defines the **baseline estimation rules** for NEW users or when NO historical patterns exist.

These are the conservative defaults. Once we have user history, we use **PATTERN-BASED ESTIMATION** (see PATTERN_BASED_ESTIMATION.md).

---

## Core Principle

**Estimate what's calculable from standards. Never make up what's personal and highly variable.**

---

## ✅ ALWAYS ESTIMATE (Baseline for New Users)

### 1. Timestamps
**Rule**: Every log needs a time.

| Input | Estimated Time |
|-------|---------------|
| "ate chicken" | Current time |
| "had breakfast" | Today 7:30 AM |
| "morning run" | Today 7:00 AM |
| "after work workout" | Today 5:30 PM |

### 2. Food Portions (When Food Named)
**Rule**: Use standard portions from nutritional databases.

| Input | Portion Estimate |
|-------|-----------------|
| "ate chicken" | 5oz grilled chicken breast |
| "had eggs" | 3 eggs |
| "protein shake" | 1 scoop (30g) |

### 3. Macros (Calculate from Portions)
**Rule**: Calculate from portion estimates.

- Chicken 5oz: 235 cal, 44g protein, 0g carbs, 5g fat
- 3 eggs: 216 cal, 18g protein, 1.2g carbs, 15g fat

---

## ⚠️ CONDITIONALLY ESTIMATE (Only if Reasonable)

### 4. Activity Duration
**Rule**: Only for typical activities with known average durations.

| Input | Duration Estimate | Why |
|-------|------------------|-----|
| "morning run" | ~35 min | Typical recreational run |
| "workout" | ~50 min | Typical gym session |
| "walked dog" | ~20 min | Typical dog walk |

### 5. Calories
**Rule**: Only if you have duration (even estimated).

- Running 35min: ~350 cal (MET value × time)
- Strength training 50min: ~300 cal

### 6. RPE (Rate of Perceived Exertion)
**Rule**: Only if effort keywords present.

| Keyword | RPE |
|---------|-----|
| "easy" | 4 |
| "moderate" | 6 |
| "hard" | 8 |
| "max effort" | 10 |

---

## ❌ NEVER ESTIMATE (Too Personal/Variable)

### 7. Distance
**Why**: Too variable (could be 1km or 20km).

- "went for a run" → distance = null
- "morning run" → distance = null

**Exception**: If user provides distance ("ran 5k"), use it.

### 8. Pace
**Why**: Requires both distance and time.

- Only calculate if BOTH distance and time known
- Otherwise: pace = null

### 9. Exercises Not Mentioned
**Why**: Presumptuous - user might have done different exercises.

- "chest workout" → exercises = []
- "leg day" → exercises = []

**Exception**: If user names exercise ("did bench press"), log it.

### 10. Sets/Reps/Weights
**Why**: Impossible to know without user input.

- Always null unless user specifies

### 11. Foods Not Mentioned
**Why**: Don't add sides user didn't mention.

- "ate chicken" → only chicken, not rice/veggies

---

## 🔄 When to Use Baseline vs. Patterns

### NEW USERS (No History)
- Use this baseline (THE_LINE.md)
- Conservative estimates
- High `needs_clarification` rate

### RETURNING USERS (Has History)
- Use **PATTERN-BASED ESTIMATION** (see PATTERN_BASED_ESTIMATION.md)
- Smarter estimates from user's past logs
- Lower `needs_clarification` rate
- Higher confidence

---

## 🚨 Red Flags (Never Cross)

Even with patterns, NEVER:
1. ❌ Extrapolate wildly beyond user's typical behavior
2. ❌ Assume user always does the same thing
3. ❌ Ignore obvious changes in behavior
4. ❌ Make up data user has never logged before

---

## Summary

**THE_LINE for new users**:
- ✅ Timestamps (always)
- ✅ Food portions (when named)
- ✅ Macros (calculable)
- ⚠️ Typical durations
- ⚠️ Calories from duration
- ❌ Distance, pace, exercises, sets/reps, extra foods

**For returning users**: See PATTERN_BASED_ESTIMATION.md
