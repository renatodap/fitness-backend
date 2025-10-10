-- Migration: Add missing fields to meals table
-- Purpose: Fix production error - meals table missing source, estimated, ai_extracted, ai_confidence, extraction_metadata, quick_entry_log_id
-- Date: 2025-10-10
--
-- This migration adds the following fields to achieve schema consistency with activities and body_measurements:
-- - source: Entry method (manual, quick_entry, etc.)
-- - estimated: Boolean flag indicating if nutrition is estimated
-- - quick_entry_log_id: Links meal to quick_entry_logs for AI-powered entry tracking
-- - ai_extracted: Boolean flag indicating if meal was extracted by AI
-- - ai_confidence: Numeric confidence score from AI extraction (0.0 to 1.0)
-- - extraction_metadata: JSONB field for storing AI provider, model, cost, etc.

-- Add missing fields to meals table
ALTER TABLE public.meals
  ADD COLUMN IF NOT EXISTS source text DEFAULT 'manual'::text CHECK (source = ANY (ARRAY['manual'::text, 'quick_entry'::text, 'meal_scan'::text, 'coach_chat'::text])),
  ADD COLUMN IF NOT EXISTS estimated boolean DEFAULT false,
  ADD COLUMN IF NOT EXISTS quick_entry_log_id uuid,
  ADD COLUMN IF NOT EXISTS ai_extracted boolean DEFAULT false,
  ADD COLUMN IF NOT EXISTS ai_confidence numeric CHECK (ai_confidence >= 0::numeric AND ai_confidence <= 1::numeric),
  ADD COLUMN IF NOT EXISTS extraction_metadata jsonb DEFAULT '{}'::jsonb;

-- Add foreign key constraint for quick_entry_log_id (only if it doesn't exist)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'meals_quick_entry_log_id_fkey'
  ) THEN
    ALTER TABLE public.meals
      ADD CONSTRAINT meals_quick_entry_log_id_fkey
      FOREIGN KEY (quick_entry_log_id)
      REFERENCES public.quick_entry_logs(id);
  END IF;
END $$;

-- Create index on quick_entry_log_id for better query performance
CREATE INDEX IF NOT EXISTS idx_meals_quick_entry_log_id
  ON public.meals(quick_entry_log_id);

-- Create index on source for filtering entry methods
CREATE INDEX IF NOT EXISTS idx_meals_source
  ON public.meals(source);

-- Create index on ai_extracted for filtering AI vs manual entries
CREATE INDEX IF NOT EXISTS idx_meals_ai_extracted
  ON public.meals(ai_extracted);

-- Add comments for documentation
COMMENT ON COLUMN public.meals.source IS 'Entry method: manual, quick_entry, meal_scan, or coach_chat';
COMMENT ON COLUMN public.meals.estimated IS 'Boolean flag indicating if nutrition values are estimated (not precise)';
COMMENT ON COLUMN public.meals.quick_entry_log_id IS 'Foreign key linking to quick_entry_logs table for AI-powered meal entry tracking';
COMMENT ON COLUMN public.meals.ai_extracted IS 'Boolean flag indicating if this meal was extracted by AI (quick entry, meal scan, or coach chat)';
COMMENT ON COLUMN public.meals.ai_confidence IS 'AI confidence score for extraction quality (0.0 to 1.0)';
COMMENT ON COLUMN public.meals.extraction_metadata IS 'JSONB metadata containing AI provider, model, cost, and other extraction details';

-- Migration complete
--
-- Rollback instructions (if needed):
-- ALTER TABLE public.meals DROP COLUMN IF EXISTS source;
-- ALTER TABLE public.meals DROP COLUMN IF EXISTS estimated;
-- ALTER TABLE public.meals DROP COLUMN IF EXISTS quick_entry_log_id;
-- ALTER TABLE public.meals DROP COLUMN IF EXISTS ai_extracted;
-- ALTER TABLE public.meals DROP COLUMN IF EXISTS ai_confidence;
-- ALTER TABLE public.meals DROP COLUMN IF EXISTS extraction_metadata;
-- DROP INDEX IF EXISTS idx_meals_source;
-- DROP INDEX IF EXISTS idx_meals_quick_entry_log_id;
-- DROP INDEX IF EXISTS idx_meals_ai_extracted;
