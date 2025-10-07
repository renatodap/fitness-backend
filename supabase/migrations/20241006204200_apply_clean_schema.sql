-- =====================================================
-- UNIFIED COACH SCHEMA MIGRATION
-- =====================================================
-- Created: 2024-10-06
-- Purpose: Add missing tables for Unified Coach interface
--
-- WHAT THIS MIGRATION DOES:
-- 1. Creates coach_conversations table for conversation tracking
-- 2. Creates coach_message_embeddings table for RAG
-- 3. Adds foreign key constraint to coach_messages
-- 4. Adds RLS policies for security
-- 5. Adds performance indexes
-- 6. Creates vector search function for coach messages
-- =====================================================

-- Enable pgvector extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "vector";

-- =====================================================
-- 1. CREATE COACH_CONVERSATIONS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS public.coach_conversations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title text,
  message_count integer DEFAULT 0 CHECK (message_count >= 0),
  archived boolean DEFAULT false,
  last_message_at timestamptz DEFAULT now(),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Add index for performance
CREATE INDEX IF NOT EXISTS idx_coach_conversations_user_id
  ON public.coach_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_coach_conversations_last_message
  ON public.coach_conversations(last_message_at DESC);

-- Enable RLS
ALTER TABLE public.coach_conversations ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own conversations"
  ON public.coach_conversations FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own conversations"
  ON public.coach_conversations FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own conversations"
  ON public.coach_conversations FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own conversations"
  ON public.coach_conversations FOR DELETE
  USING (auth.uid() = user_id);

-- Trigger for updated_at
CREATE TRIGGER update_coach_conversations_updated_at
  BEFORE UPDATE ON public.coach_conversations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 2. CREATE COACH_MESSAGE_EMBEDDINGS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS public.coach_message_embeddings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id uuid NOT NULL REFERENCES public.coach_messages(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  embedding vector(384) NOT NULL,
  content_text text NOT NULL,
  embedding_model text NOT NULL DEFAULT 'sentence-transformers/all-MiniLM-L6-v2',
  embedding_dimensions integer NOT NULL DEFAULT 384,
  created_at timestamptz DEFAULT now()
);

-- Add indexes for performance and vector search
CREATE INDEX IF NOT EXISTS idx_coach_message_embeddings_message_id
  ON public.coach_message_embeddings(message_id);
CREATE INDEX IF NOT EXISTS idx_coach_message_embeddings_user_id
  ON public.coach_message_embeddings(user_id);
CREATE INDEX IF NOT EXISTS idx_coach_message_embeddings_role
  ON public.coach_message_embeddings(role);

-- Vector similarity search index
CREATE INDEX IF NOT EXISTS idx_coach_message_embeddings_vector
  ON public.coach_message_embeddings
  USING ivfflat (embedding vector_cosine_ops);

-- Enable RLS
ALTER TABLE public.coach_message_embeddings ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own message embeddings"
  ON public.coach_message_embeddings FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own message embeddings"
  ON public.coach_message_embeddings FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- =====================================================
-- 3. ADD FOREIGN KEY TO COACH_MESSAGES
-- =====================================================

-- Add foreign key constraint if it doesn't exist
-- This links coach_messages to coach_conversations
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.table_constraints
    WHERE constraint_name = 'coach_messages_conversation_id_fkey'
    AND table_name = 'coach_messages'
  ) THEN
    ALTER TABLE public.coach_messages
      ADD CONSTRAINT coach_messages_conversation_id_fkey
      FOREIGN KEY (conversation_id)
      REFERENCES public.coach_conversations(id)
      ON DELETE CASCADE;
  END IF;
END $$;

-- =====================================================
-- 4. CREATE VECTOR SEARCH FUNCTION FOR COACH MESSAGES
-- =====================================================

CREATE OR REPLACE FUNCTION search_coach_message_embeddings(
  query_embedding vector(384),
  user_id_filter uuid,
  match_threshold float DEFAULT 0.6,
  match_count int DEFAULT 10
)
RETURNS TABLE (
  id uuid,
  message_id uuid,
  content_text text,
  role text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    cme.id,
    cme.message_id,
    cme.content_text,
    cme.role,
    1 - (cme.embedding <=> query_embedding) as similarity
  FROM coach_message_embeddings cme
  WHERE cme.user_id = user_id_filter
    AND 1 - (cme.embedding <=> query_embedding) > match_threshold
  ORDER BY cme.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- =====================================================
-- 5. CREATE RPC FUNCTION FOR GETTING USER CONVERSATIONS
-- =====================================================

CREATE OR REPLACE FUNCTION get_user_conversations(
  p_user_id uuid,
  p_limit int DEFAULT 50,
  p_offset int DEFAULT 0
)
RETURNS TABLE (
  conversation_id uuid,
  title text,
  message_count integer,
  last_message_at timestamptz,
  last_message_preview text,
  created_at timestamptz
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    c.id as conversation_id,
    c.title,
    c.message_count,
    c.last_message_at,
    (
      SELECT content
      FROM coach_messages
      WHERE conversation_id = c.id
      ORDER BY created_at DESC
      LIMIT 1
    ) as last_message_preview,
    c.created_at
  FROM coach_conversations c
  WHERE c.user_id = p_user_id
    AND c.archived = false
  ORDER BY c.last_message_at DESC
  LIMIT p_limit
  OFFSET p_offset;
END;
$$;

-- =====================================================
-- MIGRATION COMPLETE
-- =====================================================
--
-- This migration adds:
-- ✅ coach_conversations table with RLS
-- ✅ coach_message_embeddings table with RLS
-- ✅ Foreign key constraint linking messages to conversations
-- ✅ Performance indexes (including vector index)
-- ✅ Vector search function for RAG
-- ✅ RPC function for conversation listing
--
-- The Unified Coach interface can now:
-- - Track conversations properly
-- - Vectorize all messages for RAG
-- - Search conversation history semantically
-- - Display conversation list
-- =====================================================
