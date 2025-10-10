-- ============================================================================
-- MASTER SCRIPT: Fresh Start for Food & Meal System
-- ============================================================================
-- Purpose: Complete reset and initialization of food tracking system
-- Date: 2025-01-10
--
-- This script will:
-- 1. Drop all existing food/meal tables
-- 2. Create clean new schema with dual quantity tracking
-- 3. Seed with intuitive household units
--
-- ⚠️  WARNING: THIS WILL DELETE ALL EXISTING FOOD AND MEAL DATA!
-- Make sure you have a backup if needed.
--
-- Usage:
--   psql -U your_user -d your_database -f RUN_ME_fresh_start.sql
-- ============================================================================

\echo ''
\echo '╔════════════════════════════════════════════════════════════════════╗'
\echo '║  FRESH START: Food & Meal System Reset                            ║'
\echo '╚════════════════════════════════════════════════════════════════════╝'
\echo ''

-- Step 1: Cleanup
\echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
\echo 'Step 1/3: Cleaning up old tables...'
\echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
\i CLEANUP_food_and_meals.sql
\echo ''

-- Step 2: Create Schema
\echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
\echo 'Step 2/3: Creating clean schema...'
\echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
\i CREATE_clean_food_system.sql
\echo ''

-- Step 3: Seed Data
\echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
\echo 'Step 3/3: Loading seed data...'
\echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
\i SEED_foods_with_household_units.sql
\echo ''

-- Final Summary
\echo '╔════════════════════════════════════════════════════════════════════╗'
\echo '║  ✅ FRESH START COMPLETE!                                         ║'
\echo '╠════════════════════════════════════════════════════════════════════╣'
\echo '║                                                                    ║'
\echo '║  Schema Features:                                                  ║'
\echo '║  • Dual quantity tracking (servings + grams)                       ║'
\echo '║  • Intuitive household units (slice, scoop, medium, etc)           ║'
\echo '║  • Clean, normalized design                                        ║'
\echo '║  • User preferences tracking                                       ║'
\echo '║                                                                    ║'
\echo '║  Tables Created:                                                   ║'
\echo '║  • foods              (nutrition database)                         ║'
\echo '║  • meals              (user meal logs)                             ║'
\echo '║  • meal_foods         (foods in meals with dual quantities)        ║'
\echo '║  • food_preferences   (user quantity preferences)                  ║'
\echo '║                                                                    ║'
\echo '║  Sample Foods:                                                     ║'
\echo '║  🍕 Pizza (slice = 107g)                                           ║'
\echo '║  🥄 Whey Protein (scoop = 30g)                                     ║'
\echo '║  🍌 Banana (medium = 118g)                                         ║'
\echo '║  🥚 Egg (egg = 50g)                                                ║'
\echo '║  🍞 Bread (slice = 28g)                                            ║'
\echo '║                                                                    ║'
\echo '║  Next Steps:                                                       ║'
\echo '║  1. Update backend models to match new schema                      ║'
\echo '║  2. Test meal logging with dual quantities                         ║'
\echo '║  3. Verify frontend displays both serving and gram inputs          ║'
\echo '║                                                                    ║'
\echo '╚════════════════════════════════════════════════════════════════════╝'
\echo ''
