-- Migration 016: Remove Strava Integration
-- Makes Garmin the primary fitness device integration
-- Created: 2025-10-09

-- ============================================================================
-- REMOVE STRAVA CONNECTIONS TABLE
-- ============================================================================

-- Drop the strava_connections table (CASCADE removes dependent objects)
DROP TABLE IF EXISTS public.strava_connections CASCADE;

-- ============================================================================
-- UPDATE ACTIVITIES SOURCE CONSTRAINT
-- ============================================================================

-- Remove old constraint that includes 'strava'
ALTER TABLE public.activities
  DROP CONSTRAINT IF EXISTS activities_source_check;

-- Add new constraint without 'strava'
ALTER TABLE public.activities
  ADD CONSTRAINT activities_source_check
  CHECK (source IN ('garmin', 'manual', 'quick_entry', 'apple', 'fitbit', 'polar', 'suunto', 'wahoo'));

-- ============================================================================
-- OPTIONAL: CLEAN UP EXISTING STRAVA ACTIVITIES
-- ============================================================================

-- Option 1: Keep Strava activities but mark as 'manual' (RECOMMENDED)
-- This preserves user's historical data
UPDATE public.activities
SET source = 'manual',
    notes = CASE
      WHEN notes IS NULL THEN 'Originally synced from Strava'
      ELSE notes || E'\n\n[Originally synced from Strava]'
    END
WHERE source = 'strava';

-- Option 2: Delete Strava activities (DESTRUCTIVE - only if user wants clean slate)
-- Uncomment the line below ONLY if you want to delete Strava data
-- DELETE FROM public.activities WHERE source = 'strava';

-- ============================================================================
-- ADD COMMENT TO TRACK MIGRATION
-- ============================================================================

COMMENT ON TABLE public.activities IS 'Migration 016: Removed Strava integration, Garmin is now primary device source';

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- Summary:
-- ✅ Dropped strava_connections table
-- ✅ Updated activities source constraint (removed 'strava')
-- ✅ Migrated existing Strava activities to 'manual' source
-- ✅ Garmin is now the primary fitness device integration
