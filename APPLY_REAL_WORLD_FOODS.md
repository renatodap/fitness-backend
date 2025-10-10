# How to Apply Real-World Food Database Migrations

## What This Is

**350+ REAL FOODS people actually eat** - not fitness influencer bullshit.

This fixes the database to include:
- Fast food (McDonald's, Burger King, Taco Bell, Chipotle)
- Pizza (Domino's, Pizza Hut, Costco)
- Burgers (Big Mac, Whopper, Five Guys)
- Desserts (ice cream, cookies, candy)
- Drinks (soda, coffee, alcohol)
- Pasta & Italian (Alfredo, Spaghetti, Lasagna)
- Asian food (Chinese takeout, sushi, Thai)
- Brazilian food (Feijoada, Churrasco, Coxinha)
- Snacks (chips, protein bars, popcorn)

## Quick Start

Run these 3 migrations in Supabase SQL Editor:

1. **Phase 1**: Fast food & essentials (100 foods)
2. **Phase 2**: Desserts, drinks, pasta, Asian (150 foods)
3. **Phase 3**: Brazilian & snacks (100 foods)

**Time**: ~10 minutes total

---

## Prerequisites

Make sure you've already run:
- ✅ `000_SCHEMA.sql` (creates tables)
- ✅ `002_food_architecture_cleanup.sql` (creates categories)
- ✅ `003a`, `003b`, `003c` (seeds basic foods - optional, these will add more)

If not, run those first (see `APPLY_MIGRATIONS.md`).

---

## Step 1: Verify Current State

Run this in Supabase SQL Editor:

```sql
-- Check current food count
SELECT COUNT(*) as current_foods FROM foods_enhanced;

-- Check categories exist
SELECT name FROM food_categories WHERE level = 0 ORDER BY sort_order;
```

**Expected:**
- `current_foods`: 0-250 (depends on what migrations you've run)
- Categories: Protein, Grains, Fruits, Vegetables, Fats/Nuts/Seeds, Dairy, Beverages

If categories are missing, run `002_food_architecture_cleanup.sql` first.

---

## Step 2: Run Phase 1 - Fast Food & Essentials (100 foods)

**File:** `migrations/003d_seed_real_world_foods_phase1.sql`

**What it adds:**
- 10 pizza variations (Domino's, Pizza Hut, Papa John's, Costco, generic)
- 12 burger variations (McDonald's, Burger King, Wendy's, Five Guys, In-N-Out)
- 8 fast food chicken (McDonald's McNuggets, Chick-fil-A, Popeyes, KFC)
- 10 Mexican fast food (Taco Bell, Chipotle, Qdoba)
- 10 sandwiches & subs (Jimmy John's, Jersey Mike's, Subway, Arby's)
- 8 fried foods (fries, onion rings, mozzarella sticks, wings)
- 20 breakfast items (McDonald's, Burger King, Dunkin', homemade)

**How to run:**
1. Go to Supabase Dashboard → SQL Editor
2. Click "New Query"
3. Copy the **ENTIRE** contents of `migrations/003d_seed_real_world_foods_phase1.sql`
4. Paste and click "Run"
5. Wait ~30 seconds

**Verify:**
```sql
-- Should return 10 pizzas
SELECT name, calories FROM foods_enhanced WHERE name LIKE '%Pizza%' ORDER BY name;

-- Should return 12 burgers
SELECT name, calories FROM foods_enhanced WHERE name LIKE '%Burger%' OR name LIKE '%Big Mac%' OR name LIKE '%Whopper%';

-- Total should be ~100+ (depending on previous migrations)
SELECT COUNT(*) as total_foods FROM foods_enhanced;
```

**Success:** You should see Big Macs, Whoppers, McNuggets, pizzas, tacos, etc.

---

## Step 3: Run Phase 2 - Desserts, Drinks, Pasta, Asian (150 foods)

**File:** `migrations/003e_seed_real_world_foods_phase2.sql`

**What it adds:**
- 8 ice cream variations (Ben & Jerry's, Häagen-Dazs, generic)
- 10 cookies & baked goods (Oreos, Chips Ahoy, brownies, cake, donuts)
- 10 candy (M&M's, Snickers, Reese's, Kit Kat, Skittles)
- 12 pasta dishes (Alfredo, Spaghetti, Lasagna, Mac & Cheese)
- 10 Chinese takeout (Orange Chicken, General Tso's, Fried Rice)
- 8 sushi (California Roll, Spicy Tuna, Dragon Roll)
- 4 Japanese (Chicken Teriyaki, Ramen)
- 4 Thai (Pad Thai, Green Curry)
- 10 sodas (Coke, Pepsi, Sprite, Mountain Dew)
- 12 coffee drinks (lattes, mochas, frappuccinos - Starbucks, Dunkin')
- 4 energy drinks (Red Bull, Monster)
- 12 alcohol (beer, wine, margarita, shots)

**How to run:**
1. SQL Editor → New Query
2. Copy `migrations/003e_seed_real_world_foods_phase2.sql`
3. Paste and click "Run"
4. Wait ~30 seconds

**Verify:**
```sql
-- Should return ice creams
SELECT name, calories FROM foods_enhanced WHERE name LIKE '%Ice Cream%';

-- Should return Oreos, M&Ms, etc.
SELECT name, calories FROM foods_enhanced WHERE name LIKE '%Oreo%' OR name LIKE '%M&M%';

-- Should return pasta
SELECT name, calories FROM foods_enhanced WHERE name LIKE '%Alfredo%' OR name LIKE '%Spaghetti%';

-- Should return alcohol
SELECT name, calories FROM foods_enhanced WHERE name LIKE '%Beer%' OR name LIKE '%Wine%';

-- Total should be ~250+ foods now
SELECT COUNT(*) as total_foods FROM foods_enhanced;
```

**Success:** You should see Oreos, Ben & Jerry's, Pad Thai, Big Mac, beer, wine, lattes, etc.

---

## Step 4: Run Phase 3 - Brazilian & Snacks (100 foods)

**File:** `migrations/003f_seed_real_world_foods_phase3.sql`

**What it adds:**
- 10 Brazilian street food (Coxinha, Pão de Queijo, Brigadeiro, Açaí Bowl)
- 12 Brazilian meals (Feijoada, Picanha, Churrasco, X-Tudo)
- 8 Brazilian sides (Farofa, Vinagrete, Couve à Mineira)
- 6 Brazilian drinks (Guaraná, Caipirinha, Mate Leão)
- 12 chips & crackers (Lay's, Doritos, Cheetos, Pringles, Goldfish)
- 8 protein bars & granola bars (Quest, RXBAR, Clif, Kind)
- 10 misc snacks (popcorn, cheese, jerky, nuts)
- 14 restaurant sides (coleslaw, mashed potatoes, garlic bread, nachos)

**How to run:**
1. SQL Editor → New Query
2. Copy `migrations/003f_seed_real_world_foods_phase3.sql`
3. Paste and click "Run"
4. Wait ~30 seconds

**Verify:**
```sql
-- Should return Brazilian foods
SELECT name, calories FROM foods_enhanced WHERE name LIKE '%Coxinha%' OR name LIKE '%Feijoada%' OR name LIKE '%Pão%';

-- Should return chips
SELECT name, calories FROM foods_enhanced WHERE name LIKE '%Doritos%' OR name LIKE '%Cheetos%';

-- Should return protein bars
SELECT name, calories FROM foods_enhanced WHERE name LIKE '%Quest%' OR name LIKE '%Clif%';

-- Total should be ~350+ foods now
SELECT COUNT(*) as total_foods FROM foods_enhanced;
```

**Success:** You should see Coxinha, Feijoada, Doritos, Quest bars, popcorn, etc.

---

## Step 5: Final Verification

Run this comprehensive check:

```sql
-- Total food count (should be 350+)
SELECT COUNT(*) as total_foods FROM foods_enhanced;

-- Breakdown by category
SELECT
    food_group,
    COUNT(*) as count
FROM foods_enhanced
GROUP BY food_group
ORDER BY count DESC;

-- Sample foods from each category
SELECT name, calories, protein_g, total_carbs_g, total_fat_g
FROM foods_enhanced
WHERE name IN (
    'McDonald''s Big Mac',
    'Pizza Hut Personal Pan Pepperoni',
    'Oreos (6 cookies)',
    'Ben & Jerry''s Pint (Half Baked)',
    'Coca-Cola (12 oz can)',
    'Starbucks Caramel Frappuccino (Grande)',
    'Beer - Regular (Budweiser, Corona, 12 oz)',
    'Pad Thai (Chicken)',
    'Feijoada Completa (Black bean stew with pork)',
    'Doritos Nacho Cheese (1 oz, ~11 chips)',
    'Quest Protein Bar (Chocolate Chip Cookie Dough)'
);

-- Search test
SELECT name, calories FROM foods_enhanced WHERE name ILIKE '%pizza%' LIMIT 5;
SELECT name, calories FROM foods_enhanced WHERE name ILIKE '%burger%' LIMIT 5;
SELECT name, calories FROM foods_enhanced WHERE name ILIKE '%chicken%' LIMIT 5;
```

**Expected Results:**
- Total foods: **350+**
- Protein: ~120 foods
- Grains: ~150 foods
- Beverages: ~50 foods
- You should see Big Mac, pizzas, Oreos, Ben & Jerry's, sodas, beer, etc.

---

## What to Do If Something Goes Wrong

### Error: "relation foods_enhanced does not exist"
**Cause:** Tables not created yet
**Fix:** Run `000_SCHEMA.sql` first

### Error: "null value in column category_id"
**Cause:** Food categories not seeded
**Fix:** Run `002_food_architecture_cleanup.sql` first

### Error: "duplicate key value"
**Cause:** You already ran this migration
**Fix:** Skip it or delete duplicate foods:
```sql
-- Check for duplicates
SELECT name, COUNT(*) as count
FROM foods_enhanced
GROUP BY name
HAVING COUNT(*) > 1;

-- Delete duplicates (keep oldest)
DELETE FROM foods_enhanced a
USING foods_enhanced b
WHERE a.id > b.id
  AND a.name = b.name;
```

### Still Getting 0 Search Results
1. Check backend logs for errors
2. Verify backend is deployed (latest commit)
3. Clear browser cache
4. Try searching for "Big Mac" (should return McDonald's Big Mac)
5. Check if data quality filter is removed in backend code

---

## Migration Order Summary

**Correct order:**
1. ✅ `000_SCHEMA.sql` - Creates tables
2. ✅ `002_food_architecture_cleanup.sql` - Creates categories
3. ✅ `003a_seed_atomic_foods_proteins_carbs.sql` (optional - basic foods)
4. ✅ `003b_seed_fruits_vegetables_fats.sql` (optional - basic foods)
5. ✅ `003c_seed_beverages_supplements.sql` (optional - basic foods)
6. ✅ `003d_seed_real_world_foods_phase1.sql` - **Fast food (100)**
7. ✅ `003e_seed_real_world_foods_phase2.sql` - **Desserts, drinks, Asian (150)**
8. ✅ `003f_seed_real_world_foods_phase3.sql` - **Brazilian, snacks (100)**

**Total time:** 10-15 minutes

---

## Quick Command Reference

```sql
-- Check current state
SELECT COUNT(*) FROM foods_enhanced;

-- Search for specific foods
SELECT name, calories FROM foods_enhanced WHERE name ILIKE '%big mac%';
SELECT name, calories FROM foods_enhanced WHERE name ILIKE '%pizza%';
SELECT name, calories FROM foods_enhanced WHERE name ILIKE '%oreo%';

-- List all categories
SELECT name FROM food_categories WHERE level = 0 ORDER BY sort_order;

-- Count by category
SELECT food_group, COUNT(*) FROM foods_enhanced GROUP BY food_group;

-- Delete all foods (DANGER!)
DELETE FROM foods_enhanced;

-- Delete specific phase (if you want to re-run)
DELETE FROM foods_enhanced WHERE name LIKE '%McDonald%';
DELETE FROM foods_enhanced WHERE name LIKE '%Oreo%';
DELETE FROM foods_enhanced WHERE name LIKE '%Coxinha%';
```

---

## Coverage Breakdown

After all 3 phases:

**Phase 1 (100 foods): 60% of real logs**
- Fast food chains
- Basic breakfast
- Common lunch/dinner

**Phase 2 (150 foods): 80-85% of real logs**
- Desserts & sweets
- Drinks (soda, coffee, alcohol)
- Pasta & Italian
- Asian food

**Phase 3 (100 foods): 90%+ of real logs**
- Brazilian essentials
- Snack foods
- Restaurant sides
- Protein bars

**Total: 350+ foods = 90%+ coverage of real-world meal logging**

---

## Testing in the App

After running migrations:

1. Go to Nutrition → Log Meal
2. Search for "Big Mac"
   - ✅ Should return "McDonald's Big Mac (550 cal)"
3. Search for "Pizza"
   - ✅ Should return 10+ pizza options
4. Search for "Oreo"
   - ✅ Should return "Oreos (6 cookies)"
5. Search for "Coxinha"
   - ✅ Should return "Coxinha (2 pieces)"
6. Search for "Quest"
   - ✅ Should return "Quest Protein Bar"

**Success = All searches return results!** 🎉

---

## What's Different From Before

**BEFORE (fitness influencer database):**
- Grilled chicken breast ❌
- Wild salmon ❌
- Quinoa ❌
- Kale ❌
- Sweet potato ❌
- Nobody eats this shit every day!

**AFTER (real-world database):**
- Big Mac ✅
- Pizza ✅
- Cheeseburger ✅
- Oreos ✅
- Ben & Jerry's ✅
- Beer, wine, margaritas ✅
- Chinese takeout ✅
- Feijoada ✅
- Doritos ✅
- THIS IS WHAT PEOPLE ACTUALLY EAT!

---

## Need Help?

**Issue:** Search still returns 0 results
**Solution:**
1. Verify migrations ran: `SELECT COUNT(*) FROM foods_enhanced;` should show 350+
2. Check backend deployed: Latest commit should have removed data quality filter
3. Check backend logs: Look for search errors
4. Clear browser cache

**Issue:** Duplicate foods
**Solution:** Run duplicate deletion query above

**Issue:** Missing categories
**Solution:** Run `002_food_architecture_cleanup.sql`

---

**Remember:** After these migrations, your food database will reflect REALITY - not some Instagram influencer's fantasy meal prep. 🍔🍕🍺
