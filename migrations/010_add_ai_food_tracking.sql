-- Migration: Add AI Food Creation Tracking
-- Purpose: Track foods created by AI agent and enable admin review

-- Add source column to foods_enhanced to track creation method
ALTER TABLE foods_enhanced
ADD COLUMN IF NOT EXISTS source TEXT DEFAULT 'manual';

COMMENT ON COLUMN foods_enhanced.source IS 'How this food was added: manual, usda, ai_created, user_submitted';

-- Create index for filtering AI-created foods
CREATE INDEX IF NOT EXISTS idx_foods_enhanced_source ON foods_enhanced(source);

-- Create audit log table for AI-created foods
CREATE TABLE IF NOT EXISTS ai_created_foods_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    detected_food_name TEXT NOT NULL,
    created_food_id UUID REFERENCES foods_enhanced(id) ON DELETE SET NULL,
    food_data JSONB NOT NULL,
    agent_reasoning TEXT,
    confidence FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed BOOLEAN DEFAULT FALSE,
    approved BOOLEAN DEFAULT NULL,
    reviewer_notes TEXT
);

-- Enable RLS on audit log table
ALTER TABLE ai_created_foods_log ENABLE ROW LEVEL SECURITY;

-- Allow service role to insert (backend)
CREATE POLICY "Service can insert AI food logs"
ON ai_created_foods_log FOR INSERT
WITH CHECK (true);

-- Allow service role to read all logs
CREATE POLICY "Service can read AI food logs"
ON ai_created_foods_log FOR SELECT
USING (true);

-- Create index for quick lookups
CREATE INDEX IF NOT EXISTS idx_ai_foods_log_user_id ON ai_created_foods_log(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_foods_log_created_food_id ON ai_created_foods_log(created_food_id);
CREATE INDEX IF NOT EXISTS idx_ai_foods_log_reviewed ON ai_created_foods_log(reviewed);

-- Add comment
COMMENT ON TABLE ai_created_foods_log IS 'Audit log of all foods created by AI agent for admin review';
