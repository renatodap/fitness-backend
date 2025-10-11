-- Migration: Add Coach Conversation Summaries Table
-- Purpose: Store compressed summaries of long conversations to save tokens
-- Created: 2025-10-10

-- ============================================================================
-- UP MIGRATION
-- ============================================================================

-- Table: Store conversation summaries for long conversations
CREATE TABLE IF NOT EXISTS coach_conversation_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES coach_conversations(id) ON DELETE CASCADE,
    summary TEXT NOT NULL,
    message_count_at_summary INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index: Fast lookups by conversation_id
CREATE INDEX idx_conversation_summaries_conversation_id
ON coach_conversation_summaries(conversation_id);

-- Index: Fast lookups by created_at for analytics
CREATE INDEX idx_conversation_summaries_created_at
ON coach_conversation_summaries(created_at);

-- Comment on table
COMMENT ON TABLE coach_conversation_summaries IS 'Stores compressed summaries of long coach conversations (>20 messages) to reduce token usage on future requests.';

-- Comments on columns
COMMENT ON COLUMN coach_conversation_summaries.conversation_id IS 'Foreign key to coach_conversations table';
COMMENT ON COLUMN coach_conversation_summaries.summary IS 'AI-generated summary of the conversation up to this point';
COMMENT ON COLUMN coach_conversation_summaries.message_count_at_summary IS 'Number of messages in conversation when summary was generated';

-- ============================================================================
-- DOWN MIGRATION (for rollback)
-- ============================================================================

-- DROP INDEX IF EXISTS idx_conversation_summaries_created_at;
-- DROP INDEX IF EXISTS idx_conversation_summaries_conversation_id;
-- DROP TABLE IF EXISTS coach_conversation_summaries CASCADE;
