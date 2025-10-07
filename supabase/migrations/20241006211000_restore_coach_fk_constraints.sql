-- =====================================================
-- RESTORE FK CONSTRAINTS TO COACH TABLES
-- =====================================================
-- Created: 2024-10-06 21:10
-- Purpose: Add back proper FK constraints for security
--
-- PROPER APPROACH: Use real auth, not mock shit
-- FK constraints enforce referential integrity
-- =====================================================

-- Add FK constraint to coach_conversations
ALTER TABLE public.coach_conversations
  ADD CONSTRAINT coach_conversations_user_id_fkey
  FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;

-- Add FK constraint to coach_message_embeddings
ALTER TABLE public.coach_message_embeddings
  ADD CONSTRAINT coach_message_embeddings_user_id_fkey
  FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;

-- =====================================================
-- MIGRATION COMPLETE
-- =====================================================
-- FK constraints restored for proper security
-- Use real Supabase auth, not mock/test users
-- =====================================================
