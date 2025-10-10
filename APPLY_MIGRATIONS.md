# How to Apply Food Database Migrations to Supabase

## Problem
Food searches for "banana" and "pizza" return 0 results because the seed data migrations haven't been run on the production Supabase database yet.

## Solution
Run these migrations IN ORDER in your Supabase SQL Editor:

---

## Step 1: Verify Current State

Run this query in Supabase SQL Editor to check what exists:

```sql
-- Check if food categories exist
SELECT COUNT(*) as category_count FROM food_categories;

-- Check if any foods exist
SELECT COUNT(*) as food_count FROM foods_enhanced;

-- Try to find Banana
SELECT * FROM foods_enhanced WHERE name ILIKE '%banana%';
```

**Expected Results if migrations NOT run:**
- `category_count`: 0 or very low
- `food_count`: 0 or very low
- Banana: 0 rows

---

## Step 2: Run Migrations IN ORDER

### Migration 1: Food Architecture Setup
**File:** `migrations/002_food_architecture_cleanup.sql`

**What it does:**
- Creates `food_categories` table
- Adds categorization columns to `foods_enhanced`
- Seeds 8 top-level categories (Protein, Carbs, Fruits, etc.)

**How to run:**
1. Go to Supabase Dashboard → SQL Editor
2. Click "New Query"
3. Copy the ENTIRE contents of `migrations/002_food_architecture_cleanup.sql`
4. Paste and click "Run"
5. Check for errors (should see "Success")

---

### Migration 2: Seed Proteins & Carbs
**File:** `migrations/003a_seed_atomic_foods_proteins_carbs.sql`

**What it does:**
- Seeds ~110 protein foods (chicken, beef, fish, etc.)
- Seeds ~50 carb foods (rice, pasta, bread, etc.)

**How to run:**
1. Copy contents of `migrations/003a_seed_atomic_foods_proteins_carbs.sql`
2. Paste in SQL Editor
3. Click "Run"
4. Verify: `SELECT COUNT(*) FROM foods_enhanced;` should show ~160

---

### Migration 3: Seed Fruits, Vegetables, Fats
**File:** `migrations/003b_seed_fruits_vegetables_fats.sql`

**What it does:**
- Seeds 25 fruits (including **Banana**)
- Seeds 30 vegetables
- Seeds 25 fats/nuts/seeds

**How to run:**
1. Copy contents of `migrations/003b_seed_fruits_vegetables_fats.sql`
2. Paste in SQL Editor
3. Click "Run"
4. Verify Banana exists:
   ```sql
   SELECT * FROM foods_enhanced WHERE name ILIKE '%banana%';
   ```
   Should return 1 row with Banana

---

### Migration 4: Seed Beverages & Supplements
**File:** `migrations/003c_seed_beverages_supplements.sql`

**What it does:**
- Seeds ~15 beverages (coffee, tea, etc.)
- Seeds ~8 supplements (protein powder, etc.)

**How to run:**
1. Copy contents of `migrations/003c_seed_beverages_supplements.sql`
2. Paste in SQL Editor
3. Click "Run"
4. Verify: `SELECT COUNT(*) FROM foods_enhanced;` should show ~225

---

### Migration 5: Seed Community Meal Templates
**File:** `migrations/004a_seed_meal_templates_community.sql`

**What it does:**
- Seeds community meal templates (protein shakes, breakfast combos, etc.)

**How to run:**
1. Copy contents of `migrations/004a_seed_meal_templates_community.sql`
2. Paste in SQL Editor
3. Click "Run"

---

### Migration 6: Seed Restaurant Meal Templates
**File:** `migrations/004b_seed_meal_templates_restaurants.sql`

**What it does:**
- Seeds restaurant meals (Chipotle bowls, McDonald's, etc.)

**How to run:**
1. Copy contents of `migrations/004b_seed_meal_templates_restaurants.sql`
2. Paste in SQL Editor
3. Click "Run"

---

## Step 3: Verify Everything Works

Run this verification query:

```sql
-- Should return 225+ foods
SELECT COUNT(*) as total_foods FROM foods_enhanced;

-- Should return 1 Banana
SELECT name, calories, protein_g, total_carbs_g
FROM foods_enhanced
WHERE name ILIKE '%banana%';

-- Should return 8 categories
SELECT name FROM food_categories WHERE level = 0 ORDER BY sort_order;

-- Should return 30+ templates
SELECT COUNT(*) FROM meal_templates WHERE is_public = true;
```

---

## Step 4: Test Food Search

After running migrations, test in the app:

1. Go to Nutrition → Log Meal
2. Search for "banana"
3. Should see: **Banana** (Fruits, 105 cal)
4. Search for "chicken"
5. Should see multiple chicken options

---

## Troubleshooting

### Error: "relation does not exist"
- **Cause:** Table doesn't exist yet
- **Fix:** Run migration `000_SCHEMA.sql` first (creates all tables)

### Error: "duplicate key value"
- **Cause:** Migration already run
- **Fix:** Skip this migration or clear data first:
  ```sql
  DELETE FROM foods_enhanced;
  DELETE FROM food_categories CASCADE;
  ```

### Still 0 Results After Running Migrations
1. Check Railway backend logs for errors
2. Verify backend is using correct Supabase URL/keys
3. Check if backend code deployed (latest commit should have quality filter removed)
4. Clear browser cache and reload

---

## Pizza Missing?

**Pizza is NOT in the seed migrations.** To add it:

```sql
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Pizza (Cheese)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '1', 'slice', 266, 11, 33, 10, 2,
 true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy}', 1.0);
```

---

## Quick Command Reference

```sql
-- Check what's in database
SELECT COUNT(*) FROM foods_enhanced;
SELECT COUNT(*) FROM food_categories;
SELECT COUNT(*) FROM meal_templates WHERE is_public = true;

-- Search for specific food
SELECT * FROM foods_enhanced WHERE name ILIKE '%chicken%' LIMIT 5;

-- Clear all food data (DANGER!)
DELETE FROM meal_templates WHERE is_public = true;
DELETE FROM foods_enhanced;
DELETE FROM food_categories CASCADE;
```

---

## Migration Order Summary

1. ✅ `002_food_architecture_cleanup.sql` - Structure
2. ✅ `003a_seed_atomic_foods_proteins_carbs.sql` - Proteins + Carbs
3. ✅ `003b_seed_fruits_vegetables_fats.sql` - **Banana is here**
4. ✅ `003c_seed_beverages_supplements.sql` - Beverages
5. ✅ `004a_seed_meal_templates_community.sql` - Templates
6. ✅ `004b_seed_meal_templates_restaurants.sql` - Restaurants

**Total Time:** ~5-10 minutes to run all migrations

After this, food search will work! 🍌🍕
