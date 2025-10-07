-- =====================================================
-- CLEAN MOCK DATA & RESTORE FK CONSTRAINTS
-- =====================================================
-- Created: 2024-10-06 21:20
-- Purpose: Delete mock data, then add FK constraints
--
-- Problem: Existing rows reference fake user IDs
-- Solution: Delete mock data, then add constraints
-- =====================================================

-- Step 1: Delete all mock/test data from coach tables
DELETE FROM public.coach_message_embeddings
WHERE user_id = '00000000-0000-0000-0000-000000000001';

DELETE FROM public.coach_messages
WHERE user_id = '00000000-0000-0000-0000-000000000001';

DELETE FROM public.coach_conversations
WHERE user_id = '00000000-0000-0000-0000-000000000001';

-- Step 2: Add FK constraints (now that bad data is gone)
ALTER TABLE public.coach_conversations
  ADD CONSTRAINT coach_conversations_user_id_fkey
  FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;

ALTER TABLE public.coach_message_embeddings
  ADD CONSTRAINT coach_message_embeddings_user_id_fkey
  FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;

-- =====================================================
-- MIGRATION COMPLETE
-- =====================================================
-- Mock data deleted
-- FK constraints restored
-- Ready for production with real auth
-- =====================================================
