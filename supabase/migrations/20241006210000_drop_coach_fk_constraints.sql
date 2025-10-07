-- =====================================================
-- DROP FK CONSTRAINTS FROM COACH TABLES
-- =====================================================
-- Created: 2024-10-06 21:00
-- Purpose: Remove FK constraints blocking mock auth
--
-- PROBLEM: Tables already exist with FK to auth.users
-- Mock auth users don't exist in auth.users
-- Need to drop these constraints
-- =====================================================

-- Drop FK constraint from coach_conversations
ALTER TABLE public.coach_conversations
  DROP CONSTRAINT IF EXISTS coach_conversations_user_id_fkey;

-- Drop FK constraint from coach_message_embeddings
ALTER TABLE public.coach_message_embeddings
  DROP CONSTRAINT IF EXISTS coach_message_embeddings_user_id_fkey;

-- Add comments explaining why no FK
COMMENT ON COLUMN public.coach_conversations.user_id IS
  'No FK constraint to auth.users to support mock auth in development. Application validates via JWT.';

COMMENT ON COLUMN public.coach_message_embeddings.user_id IS
  'No FK constraint to auth.users to support mock auth in development. Application validates via JWT.';

-- =====================================================
-- MIGRATION COMPLETE
-- =====================================================
-- This allows Unified Coach to work with mock users
-- RLS policies still enforce security at row level
-- =====================================================
