# Database Migration Instructions

## ⚠️ CRITICAL: Run These Migrations ASAP

Your Wagner Coach backend has **4 pending migrations** that are **BLOCKING food matching** from working correctly. The database currently has foods with **incomplete nutrition data** (0g carbs, 0g fat), which is causing all your meal logging to fail.

---

## Why These Migrations Are Critical

**Current Problem:**
- ❌ Foods in `foods_enhanced` table have NULL or 0 values for `total_carbs_g` and `total_fat_g`
- ❌ When users log meals, foods are matched but have 0.0g carbs and 0.0g fat
- ❌ The agentic food matcher cannot work correctly until bad data is marked as low quality

**What These Migrations Fix:**
- ✅ Mark incomplete foods as low quality (so AI creates new ones instead)
- ✅ Add nutrition validation functions to prevent future bad data
- ✅ Add audit logging for AI-created foods
- ✅ Fix serving sizes (convert 1g → 100g per 100g)
- ✅ Add auto-calculation triggers for meal nutrition

---

## 📋 Migrations to Run (IN ORDER)

### 1. Migration 007: Fix Meal Nutrition Calculations
**File:** `007_fix_meal_nutrition_calculations.sql`
**Purpose:** Adds database triggers to auto-calculate meal totals when foods are added

**Impact:**
- Creates `calculate_meal_nutrition()` trigger function
- Auto-updates `meal_logs` table with nutrition totals
- Prevents manual calculation errors

### 2. Migration 008: Fix Food Serving Sizes
**File:** `008_fix_food_serving_sizes.sql`
**Purpose:** Fixes foods with `serving_size = 1` (should be 100 for per-100g foods)

**Impact:**
- Updates ~1000+ foods with incorrect serving sizes
- Ensures nutrition is calculated correctly
- Fixes portion size display

### 3. Migration 010: Add AI Food Tracking
**File:** `010_add_ai_food_tracking.sql`
**Purpose:** Adds audit logging for AI-created foods

**Impact:**
- Creates `ai_created_foods_log` table
- Adds `source` column to `foods_enhanced`
- Enables admin review of AI-created foods

### 4. Migration 011: Fix Missing Nutrition Data ⚠️ **MOST CRITICAL**
**File:** `011_fix_missing_nutrition_data.sql`
**Purpose:** Marks foods with incomplete nutrition as low quality

**Impact:**
- Marks ~500+ foods with `data_quality_score = 0.2` (low quality)
- Creates `validate_nutrition_macros()` function
- Creates `foods_needing_review` view for admin oversight
- **CRITICAL:** Forces AI to create new foods instead of matching to incomplete ones

---

## 🚀 How to Run Migrations

### Step 1: Go to Supabase Dashboard
1. Open [https://app.supabase.com](https://app.supabase.com)
2. Select your Wagner Coach project
3. Click **SQL Editor** in the left sidebar

### Step 2: Run Each Migration (IN ORDER)

#### Run Migration 007
1. Open file: `wagner-coach-backend/migrations/007_fix_meal_nutrition_calculations.sql`
2. Copy the **ENTIRE file contents**
3. Paste into Supabase SQL Editor
4. Click **Run** (or press Ctrl+Enter)
5. ✅ Verify: Should see "Success. No rows returned"

#### Run Migration 008
1. Open file: `wagner-coach-backend/migrations/008_fix_food_serving_sizes.sql`
2. Copy the **ENTIRE file contents**
3. Paste into Supabase SQL Editor
4. Click **Run**
5. ✅ Verify: Should see "UPDATE X" rows message

#### Run Migration 010
1. Open file: `wagner-coach-backend/migrations/010_add_ai_food_tracking.sql`
2. Copy the **ENTIRE file contents**
3. Paste into Supabase SQL Editor
4. Click **Run**
5. ✅ Verify: Should see "Success. No rows returned"

#### Run Migration 011 ⚠️ **MOST IMPORTANT**
1. Open file: `wagner-coach-backend/migrations/011_fix_missing_nutrition_data.sql`
2. Copy the **ENTIRE file contents**
3. Paste into Supabase SQL Editor
4. Click **Run**
5. ✅ Verify: Should see "UPDATE X" rows message (X = number of foods marked as low quality)

### Step 3: Verify Migrations Worked

Run these verification queries in Supabase SQL Editor:

```sql
-- 1. Check how many foods were marked as low quality
SELECT COUNT(*) as low_quality_foods
FROM foods_enhanced
WHERE data_quality_score = 0.2;
-- Expected: 100-500+ foods

-- 2. Check foods needing review
SELECT * FROM foods_needing_review LIMIT 10;
-- Expected: List of foods with incomplete nutrition

-- 3. Test nutrition validation function
SELECT
    validate_nutrition_macros(200, 20, 10, 5) as valid_example,    -- Should be TRUE
    validate_nutrition_macros(200, 0, 0, 0) as invalid_example;    -- Should be FALSE
-- Expected: valid_example = true, invalid_example = false

-- 4. Check AI food tracking table exists
SELECT COUNT(*) FROM ai_created_foods_log;
-- Expected: 0 (empty table, ready for logging)
```

---

## 🧪 Test After Migrations

After running all migrations, **test the food matching**:

### Test 1: Simple Text Meal
**Input:** "I ate grilled chicken, sweet potato, asparagus"

**Expected Result:**
- ✅ 3 foods detected and matched
- ✅ All foods have complete nutrition (carbs > 0, fat > 0)
- ✅ Meal log page shows foods with correct macros

### Test 2: Branded Food
**Input:** "I ate Chipotle burrito bowl"

**Expected Result:**
- ✅ Burrito bowl detected and matched OR created by AI
- ✅ Complete nutrition data (not 0g carbs/fat)
- ✅ Meal log shows food with ID and nutrition

### Test 3: Mixed Format
**Input:** "I had eggs and oatmeal for breakfast"

**Expected Result:**
- ✅ 2 foods detected (eggs, oatmeal)
- ✅ Both matched or created with complete nutrition
- ✅ No "Auto-match failed" errors

---

## 📊 Expected Results

### Before Migrations
- ❌ Foods matched but show 0.0g carbs, 0.0g fat
- ❌ Grilled chicken matches "Grilled Chicken Sandwich (Chick-fil-A)" with incomplete data
- ❌ AI doesn't create new foods because it finds low-quality matches

### After Migrations
- ✅ Low-quality foods are ignored (data_quality_score < 0.5)
- ✅ AI creates new foods with complete nutrition
- ✅ Foods show correct macros (e.g., 165 cal, 31g P, 0g C, 3.6g F for grilled chicken)
- ✅ Meal logs populate correctly with database food IDs

---

## 🔍 Troubleshooting

### Migration Failed with "relation does not exist"
- **Cause:** Running migrations out of order
- **Fix:** Run migrations 007, 008, 010, 011 in exact order

### Migration Failed with "column already exists"
- **Cause:** Migration already ran (partially)
- **Fix:** Check which parts succeeded, comment out those lines, re-run

### Foods still showing 0g carbs/fat after migrations
- **Cause:** Migrations not run yet OR frontend caching old data
- **Fix:**
  1. Verify migration 011 ran: `SELECT COUNT(*) FROM foods_enhanced WHERE data_quality_score = 0.2;`
  2. Clear browser cache and re-test
  3. Check backend logs for "[AgenticMatcher]" entries

### "Auto-match failed" errors
- **Cause:** AI provider (Groq) API issue or rate limit
- **Fix:**
  1. Check backend logs for Groq errors
  2. Verify `GROQ_API_KEY` is set correctly
  3. Wait 1 minute and retry (rate limit cooldown)

---

## 🎯 Success Checklist

After running all migrations, you should have:

- ✅ Migration 007 ran successfully (meal nutrition triggers added)
- ✅ Migration 008 ran successfully (serving sizes fixed)
- ✅ Migration 010 ran successfully (AI audit logging added)
- ✅ Migration 011 ran successfully (incomplete foods marked as low quality)
- ✅ Verification queries all return expected results
- ✅ Test meals work correctly (no 0g carbs/fat)
- ✅ Backend logs show "[AgenticMatcher] ✅ Created" for new foods
- ✅ Meal log page populates with foods and nutrition

---

## 📞 Need Help?

If migrations fail or results are unexpected:

1. **Check backend logs:** Look for "[AgenticMatcher]" and "[UnifiedCoach]" entries
2. **Run verification queries** (see Step 3 above)
3. **Test with simple meal:** "I ate chicken and rice"
4. **Check Supabase SQL Editor** for error messages

**Common Issues:**
- Out of order execution → Re-run in correct order
- Partial migration → Comment out completed sections, re-run
- API errors → Check GROQ_API_KEY environment variable

---

## 🔄 Rollback (Emergency Only)

If you need to rollback migration 011 (restore all food quality scores):

```sql
-- ROLLBACK Migration 011 (restore food quality scores)
UPDATE foods_enhanced
SET data_quality_score = 0.8
WHERE data_quality_score = 0.2;

-- Drop validation function and view
DROP FUNCTION IF EXISTS validate_nutrition_macros;
DROP VIEW IF EXISTS foods_needing_review;
```

**⚠️ WARNING:** Only rollback if absolutely necessary. Rollback will re-enable matching to incomplete foods!

---

**Run these migrations NOW to fix food matching! 🚀**
