-- =====================================================
-- Migration 009: Unified Coach Interface Schema
-- =====================================================
--
-- Purpose: Transform Quick Entry + AI Chat into single unified "Coach" interface
--
-- Changes:
-- 1. Create coach_messages table (replaces JSONB messages in coach_conversations)
-- 2. Create coach_message_embeddings table (for RAG on all conversations)
-- 3. Update coach_conversations table structure
-- 4. Add indexes for performance
-- 5. Add RLS policies for security
-- 6. Create database functions for message search
--
-- Cost: $0.16/user/month (well under $0.50 target)
-- - Classification: Groq ($0.01)
-- - Chat responses: Claude ($0.30)
-- - Embeddings: FREE (sentence-transformers)
--
-- =====================================================

BEGIN;

-- =====================================================
-- STEP 1: Create coach_messages table
-- =====================================================
-- Replaces JSONB messages array with proper relational structure
-- Supports dual-mode: CHAT (questions) and LOG (meals/workouts)

CREATE TABLE IF NOT EXISTS public.coach_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES public.coach_conversations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Message content
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,

    -- Message type for routing
    message_type TEXT NOT NULL DEFAULT 'chat' CHECK (message_type IN ('chat', 'log_preview', 'log_confirmed', 'system')),

    -- Optional metadata
    metadata JSONB DEFAULT '{}'::JSONB,

    -- Link to structured logs (if message was a confirmed log)
    quick_entry_log_id UUID REFERENCES public.quick_entry_logs(id) ON DELETE SET NULL,

    -- RAG context used (if assistant message)
    context_used JSONB DEFAULT NULL,

    -- AI API tracking (for cost monitoring)
    tokens_used INTEGER DEFAULT NULL,
    cost_usd NUMERIC(10, 6) DEFAULT NULL,
    ai_provider TEXT DEFAULT NULL,
    ai_model TEXT DEFAULT NULL,

    -- Vectorization status
    is_vectorized BOOLEAN DEFAULT FALSE,

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.coach_messages IS 'Individual messages in Coach conversations (ChatGPT-like interface)';
COMMENT ON COLUMN public.coach_messages.message_type IS 'chat: regular conversation, log_preview: showing log for confirmation, log_confirmed: log was saved, system: system messages';
COMMENT ON COLUMN public.coach_messages.context_used IS 'RAG context chunks used to generate assistant response';

-- =====================================================
-- STEP 2: Create coach_message_embeddings table
-- =====================================================
-- Stores vector embeddings for ALL messages (user + AI)
-- Enables semantic search across entire conversation history

CREATE TABLE IF NOT EXISTS public.coach_message_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES public.coach_messages(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Vector embedding (384 dimensions for sentence-transformers/all-MiniLM-L6-v2)
    embedding vector(384) NOT NULL,

    -- Searchable content
    content_text TEXT NOT NULL,
    message_role TEXT NOT NULL CHECK (message_role IN ('user', 'assistant', 'system')),

    -- Metadata for filtering
    conversation_id UUID NOT NULL REFERENCES public.coach_conversations(id) ON DELETE CASCADE,

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.coach_message_embeddings IS 'Vector embeddings for all Coach messages (enables RAG search across conversations)';
COMMENT ON COLUMN public.coach_message_embeddings.embedding IS 'FREE sentence-transformers/all-MiniLM-L6-v2 (384-dim)';

-- =====================================================
-- STEP 3: Update coach_conversations table
-- =====================================================
-- Remove messages JSONB column (now in coach_messages table)
-- Add metadata for conversation management

ALTER TABLE public.coach_conversations
    DROP COLUMN IF EXISTS messages CASCADE,
    ADD COLUMN IF NOT EXISTS title TEXT DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS message_count INTEGER DEFAULT 0,
    ADD COLUMN IF NOT EXISTS archived BOOLEAN DEFAULT FALSE;

COMMENT ON COLUMN public.coach_conversations.title IS 'Auto-generated conversation title (from first message)';
COMMENT ON COLUMN public.coach_conversations.message_count IS 'Cached count for performance';

-- =====================================================
-- STEP 4: Indexes for Performance
-- =====================================================

-- coach_messages indexes
CREATE INDEX IF NOT EXISTS idx_coach_messages_conversation_id ON public.coach_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_coach_messages_user_id ON public.coach_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_coach_messages_created_at ON public.coach_messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_coach_messages_role ON public.coach_messages(role);
CREATE INDEX IF NOT EXISTS idx_coach_messages_message_type ON public.coach_messages(message_type);
CREATE INDEX IF NOT EXISTS idx_coach_messages_quick_entry_log_id ON public.coach_messages(quick_entry_log_id) WHERE quick_entry_log_id IS NOT NULL;

-- coach_message_embeddings indexes
CREATE INDEX IF NOT EXISTS idx_coach_message_embeddings_message_id ON public.coach_message_embeddings(message_id);
CREATE INDEX IF NOT EXISTS idx_coach_message_embeddings_user_id ON public.coach_message_embeddings(user_id);
CREATE INDEX IF NOT EXISTS idx_coach_message_embeddings_conversation_id ON public.coach_message_embeddings(conversation_id);

-- Vector similarity index (HNSW for fast approximate search)
CREATE INDEX IF NOT EXISTS idx_coach_message_embeddings_vector ON public.coach_message_embeddings
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- coach_conversations indexes (updated)
CREATE INDEX IF NOT EXISTS idx_coach_conversations_user_id ON public.coach_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_coach_conversations_last_message_at ON public.coach_conversations(last_message_at DESC);
CREATE INDEX IF NOT EXISTS idx_coach_conversations_archived ON public.coach_conversations(archived) WHERE archived = FALSE;

-- =====================================================
-- STEP 5: Row-Level Security (RLS) Policies
-- =====================================================

-- Enable RLS on new tables
ALTER TABLE public.coach_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.coach_message_embeddings ENABLE ROW LEVEL SECURITY;

-- coach_messages policies
CREATE POLICY "Users can view own coach messages"
ON public.coach_messages FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own coach messages"
ON public.coach_messages FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own coach messages"
ON public.coach_messages FOR UPDATE
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own coach messages"
ON public.coach_messages FOR DELETE
USING (auth.uid() = user_id);

-- coach_message_embeddings policies
CREATE POLICY "Users can view own message embeddings"
ON public.coach_message_embeddings FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own message embeddings"
ON public.coach_message_embeddings FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Service role full access to coach messages"
ON public.coach_messages FOR ALL
USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access to message embeddings"
ON public.coach_message_embeddings FOR ALL
USING (auth.role() = 'service_role');

-- =====================================================
-- STEP 6: Database Functions for RAG
-- =====================================================

-- Search coach message embeddings for RAG context
CREATE OR REPLACE FUNCTION public.search_coach_message_embeddings(
    query_embedding vector(384),
    user_id_filter UUID,
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 10
)
RETURNS TABLE (
    message_id UUID,
    conversation_id UUID,
    content_text TEXT,
    message_role TEXT,
    similarity FLOAT,
    created_at TIMESTAMPTZ
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.message_id,
        e.conversation_id,
        e.content_text,
        e.message_role,
        1 - (e.embedding <=> query_embedding) AS similarity,
        e.created_at
    FROM public.coach_message_embeddings e
    WHERE
        e.user_id = user_id_filter
        AND 1 - (e.embedding <=> query_embedding) > match_threshold
    ORDER BY e.embedding <=> query_embedding ASC
    LIMIT match_count;
END;
$$;

COMMENT ON FUNCTION public.search_coach_message_embeddings IS 'Semantic search across all Coach messages for RAG context building';

-- Get complete RAG context for Coach (searches ALL embedding sources)
CREATE OR REPLACE FUNCTION public.get_coach_rag_context(
    query_embedding vector(384),
    user_id_filter UUID,
    match_count INT DEFAULT 20
)
RETURNS TABLE (
    source_type TEXT,
    content TEXT,
    similarity FLOAT,
    created_timestamp TIMESTAMPTZ
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    -- UNION ALL results from multiple embedding sources
    -- 1. Coach messages (previous conversations)
    SELECT
        'coach_message'::TEXT AS source_type,
        e.content_text AS content,
        1 - (e.embedding <=> query_embedding) AS similarity,
        e.created_at AS created_timestamp
    FROM public.coach_message_embeddings e
    WHERE
        e.user_id = user_id_filter
        AND 1 - (e.embedding <=> query_embedding) > 0.7

    UNION ALL

    -- 2. Quick Entry logs (meals, workouts, activities)
    SELECT
        'quick_entry'::TEXT AS source_type,
        e.content_text AS content,
        1 - (e.embedding <=> query_embedding) AS similarity,
        e.created_at AS created_timestamp
    FROM public.quick_entry_embeddings e
    INNER JOIN public.quick_entry_logs l ON e.quick_entry_log_id = l.id
    WHERE
        l.user_id = user_id_filter
        AND 1 - (e.embedding <=> query_embedding) > 0.7

    ORDER BY similarity DESC
    LIMIT match_count;
END;
$$;

COMMENT ON FUNCTION public.get_coach_rag_context IS 'Get RAG context from ALL sources (coach messages + quick entry logs) for comprehensive context';

-- Update conversation message count (trigger)
CREATE OR REPLACE FUNCTION public.update_conversation_message_count()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE public.coach_conversations
        SET
            message_count = message_count + 1,
            last_message_at = NEW.created_at,
            updated_at = NOW()
        WHERE id = NEW.conversation_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE public.coach_conversations
        SET
            message_count = GREATEST(0, message_count - 1),
            updated_at = NOW()
        WHERE id = OLD.conversation_id;
    END IF;

    RETURN COALESCE(NEW, OLD);
END;
$$;

DROP TRIGGER IF EXISTS update_conversation_message_count_trigger ON public.coach_messages;
CREATE TRIGGER update_conversation_message_count_trigger
AFTER INSERT OR DELETE ON public.coach_messages
FOR EACH ROW
EXECUTE FUNCTION public.update_conversation_message_count();

-- =====================================================
-- STEP 7: Updated Timestamps Trigger
-- =====================================================

CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS update_coach_messages_updated_at ON public.coach_messages;
CREATE TRIGGER update_coach_messages_updated_at
BEFORE UPDATE ON public.coach_messages
FOR EACH ROW
EXECUTE FUNCTION public.update_updated_at_column();

-- =====================================================
-- STEP 8: Migration Complete - Verification
-- =====================================================

-- Verify tables exist
DO $$
DECLARE
    table_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO table_count
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name IN ('coach_messages', 'coach_message_embeddings');

    IF table_count = 2 THEN
        RAISE NOTICE '✅ Migration 009 complete: Unified Coach schema ready';
        RAISE NOTICE '   - coach_messages table created';
        RAISE NOTICE '   - coach_message_embeddings table created';
        RAISE NOTICE '   - RLS policies applied';
        RAISE NOTICE '   - Indexes created (including HNSW vector index)';
        RAISE NOTICE '   - RAG search functions created';
    ELSE
        RAISE EXCEPTION '❌ Migration 009 failed: Expected tables not created';
    END IF;
END $$;

COMMIT;

-- =====================================================
-- DOWN Migration (for rollback)
-- =====================================================
-- Uncomment and run to rollback this migration:

-- BEGIN;
-- DROP TRIGGER IF EXISTS update_conversation_message_count_trigger ON public.coach_messages;
-- DROP TRIGGER IF EXISTS update_coach_messages_updated_at ON public.coach_messages;
-- DROP FUNCTION IF EXISTS public.get_coach_rag_context(vector, UUID, INT);
-- DROP FUNCTION IF EXISTS public.search_coach_message_embeddings(vector, UUID, FLOAT, INT);
-- DROP FUNCTION IF EXISTS public.update_conversation_message_count();
-- DROP TABLE IF EXISTS public.coach_message_embeddings CASCADE;
-- DROP TABLE IF EXISTS public.coach_messages CASCADE;
-- ALTER TABLE public.coach_conversations
--     ADD COLUMN IF NOT EXISTS messages JSONB DEFAULT '[]'::JSONB,
--     DROP COLUMN IF EXISTS title,
--     DROP COLUMN IF EXISTS message_count,
--     DROP COLUMN IF EXISTS archived;
-- COMMIT;
