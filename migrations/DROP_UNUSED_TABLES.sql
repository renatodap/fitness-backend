-- ============================================================
-- DROP UNUSED TABLES - Wagner Coach Database Cleanup
-- ============================================================
-- This script removes 13 unused database tables identified through
-- comprehensive codebase analysis. All tables listed have ZERO
-- references in the backend Python services.
--
-- IMPORTANT: Run this script AFTER backing up your database!
--
-- Created: 2025-10-09
-- ============================================================

-- 1. Strava Integration (Removed - now using Garmin only)
DROP TABLE IF EXISTS strava_activities CASCADE;
DROP TABLE IF EXISTS strava_auth CASCADE;

-- 2. Old Workout System Tables (Replaced by activities table)
DROP TABLE IF EXISTS workout_log_exercises CASCADE;
DROP TABLE IF EXISTS workout_logs CASCADE;
DROP TABLE IF EXISTS workout_sets CASCADE;
DROP TABLE IF EXISTS workout_exercises CASCADE;
DROP TABLE IF EXISTS workouts CASCADE;
DROP TABLE IF EXISTS workout_days CASCADE;

-- 3. Unused Nutrition Tables (Replaced by foods_enhanced)
DROP TABLE IF EXISTS custom_foods CASCADE;

-- 4. Unused Goal Tables (No backend references)
DROP TABLE IF EXISTS nutrition_goals CASCADE;
DROP TABLE IF EXISTS weekly_workout_goals CASCADE;

-- 5. Unused Coach Tables (No backend references)
DROP TABLE IF EXISTS coach_tool_calls CASCADE;

-- 6. Unused Exercise Tables (No backend references)
DROP TABLE IF EXISTS custom_exercises CASCADE;

-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================
-- Run these to verify tables are gone:
--
-- SELECT table_name
-- FROM information_schema.tables
-- WHERE table_schema = 'public'
-- AND table_name IN (
--   'strava_activities', 'strava_auth', 'workout_log_exercises',
--   'workout_logs', 'workout_sets', 'workout_exercises', 'workouts',
--   'workout_days', 'custom_foods', 'nutrition_goals',
--   'weekly_workout_goals', 'coach_tool_calls', 'custom_exercises'
-- );
--
-- Should return 0 rows if all tables were successfully dropped.
-- ============================================================
