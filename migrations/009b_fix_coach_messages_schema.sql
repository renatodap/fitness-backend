-- =====================================================
-- Migration 009b: Fix coach_messages schema
-- =====================================================
--
-- Purpose: Add missing columns to existing coach_messages table
--
-- Issue: Table was created without all required columns
-- This migration adds them if they don't exist
--
-- =====================================================

BEGIN;

-- Add message_type column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'coach_messages'
        AND column_name = 'message_type'
    ) THEN
        ALTER TABLE public.coach_messages
        ADD COLUMN message_type TEXT NOT NULL DEFAULT 'chat'
        CHECK (message_type IN ('chat', 'log_preview', 'log_confirmed', 'system'));

        RAISE NOTICE '✅ Added message_type column to coach_messages';
    ELSE
        RAISE NOTICE 'ℹ️  message_type column already exists';
    END IF;
END $$;

-- Add metadata column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'coach_messages'
        AND column_name = 'metadata'
    ) THEN
        ALTER TABLE public.coach_messages
        ADD COLUMN metadata JSONB DEFAULT '{}'::JSONB;

        RAISE NOTICE '✅ Added metadata column to coach_messages';
    ELSE
        RAISE NOTICE 'ℹ️  metadata column already exists';
    END IF;
END $$;

-- Add quick_entry_log_id column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'coach_messages'
        AND column_name = 'quick_entry_log_id'
    ) THEN
        ALTER TABLE public.coach_messages
        ADD COLUMN quick_entry_log_id UUID REFERENCES public.quick_entry_logs(id) ON DELETE SET NULL;

        RAISE NOTICE '✅ Added quick_entry_log_id column to coach_messages';
    ELSE
        RAISE NOTICE 'ℹ️  quick_entry_log_id column already exists';
    END IF;
END $$;

-- Add context_used column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'coach_messages'
        AND column_name = 'context_used'
    ) THEN
        ALTER TABLE public.coach_messages
        ADD COLUMN context_used JSONB DEFAULT NULL;

        RAISE NOTICE '✅ Added context_used column to coach_messages';
    ELSE
        RAISE NOTICE 'ℹ️  context_used column already exists';
    END IF;
END $$;

-- Add tokens_used column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'coach_messages'
        AND column_name = 'tokens_used'
    ) THEN
        ALTER TABLE public.coach_messages
        ADD COLUMN tokens_used INTEGER DEFAULT NULL;

        RAISE NOTICE '✅ Added tokens_used column to coach_messages';
    ELSE
        RAISE NOTICE 'ℹ️  tokens_used column already exists';
    END IF;
END $$;

-- Add cost_usd column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'coach_messages'
        AND column_name = 'cost_usd'
    ) THEN
        ALTER TABLE public.coach_messages
        ADD COLUMN cost_usd NUMERIC(10, 6) DEFAULT NULL;

        RAISE NOTICE '✅ Added cost_usd column to coach_messages';
    ELSE
        RAISE NOTICE 'ℹ️  cost_usd column already exists';
    END IF;
END $$;

-- Add ai_provider column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'coach_messages'
        AND column_name = 'ai_provider'
    ) THEN
        ALTER TABLE public.coach_messages
        ADD COLUMN ai_provider TEXT DEFAULT NULL;

        RAISE NOTICE '✅ Added ai_provider column to coach_messages';
    ELSE
        RAISE NOTICE 'ℹ️  ai_provider column already exists';
    END IF;
END $$;

-- Add ai_model column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'coach_messages'
        AND column_name = 'ai_model'
    ) THEN
        ALTER TABLE public.coach_messages
        ADD COLUMN ai_model TEXT DEFAULT NULL;

        RAISE NOTICE '✅ Added ai_model column to coach_messages';
    ELSE
        RAISE NOTICE 'ℹ️  ai_model column already exists';
    END IF;
END $$;

-- Add is_vectorized column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'coach_messages'
        AND column_name = 'is_vectorized'
    ) THEN
        ALTER TABLE public.coach_messages
        ADD COLUMN is_vectorized BOOLEAN DEFAULT FALSE;

        RAISE NOTICE '✅ Added is_vectorized column to coach_messages';
    ELSE
        RAISE NOTICE 'ℹ️  is_vectorized column already exists';
    END IF;
END $$;

COMMIT;

-- Verification
DO $$
DECLARE
    col_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO col_count
    FROM information_schema.columns
    WHERE table_schema = 'public'
    AND table_name = 'coach_messages'
    AND column_name IN ('message_type', 'metadata', 'quick_entry_log_id', 'context_used',
                        'tokens_used', 'cost_usd', 'ai_provider', 'ai_model', 'is_vectorized');

    IF col_count >= 9 THEN
        RAISE NOTICE '✅ Migration 009b complete: coach_messages schema fixed';
        RAISE NOTICE '   All required columns present: % of 9', col_count;
    ELSE
        RAISE WARNING '⚠️  Migration 009b incomplete: Only % of 9 columns present', col_count;
    END IF;
END $$;
