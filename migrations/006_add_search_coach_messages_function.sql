-- Migration: Add Search Coach Messages Function
-- Purpose: Semantic search function for conversation history using pgvector
-- Created: 2025-10-10

-- ============================================================================
-- UP MIGRATION
-- ============================================================================

-- Function: Semantic search for coach messages using vector similarity
CREATE OR REPLACE FUNCTION search_coach_messages(
    query_embedding vector(384),
    conversation_id_filter UUID,
    user_id_filter UUID,
    exclude_message_ids UUID[] DEFAULT '{}',
    match_threshold FLOAT DEFAULT 0.5,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    conversation_id UUID,
    role TEXT,
    content TEXT,
    created_at TIMESTAMPTZ,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        cm.id,
        cm.conversation_id,
        cm.role,
        cm.content,
        cm.created_at,
        1 - (cme.embedding <=> query_embedding) AS similarity
    FROM coach_messages cm
    JOIN coach_message_embeddings cme ON cme.message_id = cm.id
    WHERE
        cm.user_id = user_id_filter
        AND cm.conversation_id = conversation_id_filter
        AND NOT (cm.id = ANY(exclude_message_ids))
        AND (1 - (cme.embedding <=> query_embedding)) > match_threshold
    ORDER BY similarity DESC
    LIMIT match_count;
END;
$$;

-- Comment on function
COMMENT ON FUNCTION search_coach_messages IS 'Semantic search for coach messages using pgvector cosine similarity. Returns most relevant messages based on embedding similarity.';

-- Grant execute permission to authenticated users
-- GRANT EXECUTE ON FUNCTION search_coach_messages TO authenticated;

-- ============================================================================
-- DOWN MIGRATION (for rollback)
-- ============================================================================

-- DROP FUNCTION IF EXISTS search_coach_messages(vector(384), UUID, UUID, UUID[], FLOAT, INT);
