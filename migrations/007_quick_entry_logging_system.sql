-- =============================================================================
-- Migration 007: Quick Entry Logging System (Production-Ready)
-- =============================================================================
--
-- PURPOSE:
-- Create a comprehensive, production-ready logging system for Quick Entry that:
-- 1. Stores raw user input (text, images, audio, multimodal)
-- 2. Stores AI-processed structured data
-- 3. Generates vector embeddings for RAG
-- 4. Supports meal, workout, body measurement, and general logging
-- 5. Enables semantic search across all user data
-- 6. Optimizes for cost-efficient AI API usage
--
-- WORKFLOW:
-- User submits Quick Entry →
-- Raw data stored in quick_entry_logs →
-- AI processes and extracts structured data →
-- Structured data stored in specific log tables →
-- Vector embeddings generated and stored →
-- Data available for RAG context building
--
-- =============================================================================

-- Enable pgvector extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS vector;

-- =============================================================================
-- 1. MAIN QUICK ENTRY LOGS TABLE
-- =============================================================================
-- Stores ALL quick entry submissions with raw + processed data

CREATE TABLE IF NOT EXISTS public.quick_entry_logs (
    -- Identity
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Input metadata
    input_type TEXT NOT NULL CHECK (input_type IN ('text', 'voice', 'image', 'multimodal', 'pdf')),
    input_modalities TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[], -- e.g., ['text', 'image']

    -- Raw input data (what user provided)
    raw_text TEXT, -- User's original text input
    raw_transcription TEXT, -- If voice, the transcription
    image_urls TEXT[] DEFAULT ARRAY[]::TEXT[], -- Meal photos, workout photos, etc.
    audio_url TEXT, -- Voice note URL
    pdf_url TEXT, -- Uploaded PDF (nutrition label, workout plan, etc.)

    -- Storage references
    storage_bucket TEXT CHECK (storage_bucket IN ('user-images', 'user-audio', 'user-videos', 'user-documents')),
    file_metadata JSONB DEFAULT '{}'::JSONB, -- File sizes, mime types, etc.

    -- AI processing metadata
    ai_provider TEXT NOT NULL CHECK (ai_provider IN ('groq', 'openrouter', 'anthropic', 'openai', 'local', 'free')),
    ai_model TEXT NOT NULL, -- e.g., 'groq/llama-3.3-70b-versatile'
    ai_cost_usd NUMERIC(10, 6) DEFAULT 0, -- Track costs per entry
    tokens_used INTEGER DEFAULT 0,
    processing_duration_ms INTEGER, -- How long AI took

    -- AI extracted data (structured output from AI)
    ai_classification TEXT CHECK (ai_classification IN ('meal', 'workout', 'body_measurement', 'activity', 'goal', 'note', 'mixed', 'unknown')),
    ai_extracted_data JSONB NOT NULL DEFAULT '{}'::JSONB, -- Full AI response
    ai_confidence_score NUMERIC(3, 2) CHECK (ai_confidence_score >= 0 AND ai_confidence_score <= 1),
    ai_raw_response TEXT, -- Raw AI response for debugging

    -- Structured data flags (what was extracted)
    contains_meal BOOLEAN DEFAULT FALSE,
    contains_workout BOOLEAN DEFAULT FALSE,
    contains_body_measurement BOOLEAN DEFAULT FALSE,
    contains_activity BOOLEAN DEFAULT FALSE,
    contains_goal BOOLEAN DEFAULT FALSE,
    contains_note BOOLEAN DEFAULT FALSE,

    -- Linking to structured logs (populated after extraction)
    meal_log_ids UUID[] DEFAULT ARRAY[]::UUID[], -- Links to meal_logs
    workout_log_ids UUID[] DEFAULT ARRAY[]::UUID[], -- Links to activities (workout)
    body_measurement_ids UUID[] DEFAULT ARRAY[]::UUID[], -- Links to body_measurements
    activity_ids UUID[] DEFAULT ARRAY[]::UUID[], -- Links to activities

    -- User metadata
    logged_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    timezone TEXT DEFAULT 'UTC',
    location_lat NUMERIC(10, 8),
    location_lng NUMERIC(11, 8),

    -- Processing status
    processing_status TEXT NOT NULL DEFAULT 'pending' CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed', 'partial')),
    processing_error TEXT,
    retry_count INTEGER DEFAULT 0,

    -- Semantic search optimization
    embedding_generated BOOLEAN DEFAULT FALSE,
    embedding_id UUID, -- Links to quick_entry_embeddings

    -- Tags and categories
    auto_tags TEXT[] DEFAULT ARRAY[]::TEXT[], -- AI-generated tags
    user_tags TEXT[] DEFAULT ARRAY[]::TEXT[], -- User-added tags

    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Indexes will be created below
    CONSTRAINT quick_entry_logs_check_input_data CHECK (
        (input_type = 'text' AND raw_text IS NOT NULL) OR
        (input_type = 'voice' AND audio_url IS NOT NULL) OR
        (input_type = 'image' AND array_length(image_urls, 1) > 0) OR
        (input_type = 'pdf' AND pdf_url IS NOT NULL) OR
        (input_type = 'multimodal')
    )
);

-- Indexes for performance
CREATE INDEX idx_quick_entry_logs_user_id ON public.quick_entry_logs(user_id);
CREATE INDEX idx_quick_entry_logs_logged_at ON public.quick_entry_logs(logged_at DESC);
CREATE INDEX idx_quick_entry_logs_classification ON public.quick_entry_logs(ai_classification) WHERE ai_classification IS NOT NULL;
CREATE INDEX idx_quick_entry_logs_status ON public.quick_entry_logs(processing_status);
CREATE INDEX idx_quick_entry_logs_user_logged ON public.quick_entry_logs(user_id, logged_at DESC);
CREATE INDEX idx_quick_entry_logs_contains_meal ON public.quick_entry_logs(user_id) WHERE contains_meal = TRUE;
CREATE INDEX idx_quick_entry_logs_contains_workout ON public.quick_entry_logs(user_id) WHERE contains_workout = TRUE;

-- Full-text search on raw text
CREATE INDEX idx_quick_entry_logs_raw_text_fts ON public.quick_entry_logs USING gin(to_tsvector('english', COALESCE(raw_text, '') || ' ' || COALESCE(raw_transcription, '')));

-- RLS Policies
ALTER TABLE public.quick_entry_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own quick entries"
    ON public.quick_entry_logs FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own quick entries"
    ON public.quick_entry_logs FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own quick entries"
    ON public.quick_entry_logs FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own quick entries"
    ON public.quick_entry_logs FOR DELETE
    USING (auth.uid() = user_id);

-- =============================================================================
-- 2. QUICK ENTRY EMBEDDINGS TABLE (Optimized for RAG)
-- =============================================================================
-- Stores vector embeddings for semantic search across all quick entries

CREATE TABLE IF NOT EXISTS public.quick_entry_embeddings (
    -- Identity
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quick_entry_log_id UUID NOT NULL REFERENCES public.quick_entry_logs(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Embedding data
    embedding_type TEXT NOT NULL CHECK (embedding_type IN ('text', 'image', 'audio', 'multimodal', 'combined')),
    embedding vector(384) NOT NULL, -- FREE model: all-MiniLM-L6-v2 (384 dimensions)

    -- Content for context building
    content_text TEXT NOT NULL, -- Searchable text representation
    content_summary TEXT, -- AI-generated summary (1-2 sentences)

    -- Metadata for RAG context
    metadata JSONB DEFAULT '{}'::JSONB, -- Additional context
    source_classification TEXT, -- meal, workout, body_measurement, etc.

    -- Embedding model info
    embedding_model TEXT NOT NULL DEFAULT 'sentence-transformers/all-MiniLM-L6-v2',
    embedding_dimensions INTEGER NOT NULL DEFAULT 384,

    -- Search optimization
    content_hash TEXT NOT NULL, -- Hash of content_text to detect duplicates
    is_active BOOLEAN DEFAULT TRUE, -- Can deactivate old/irrelevant embeddings

    -- Timestamps
    logged_at TIMESTAMPTZ NOT NULL, -- Same as quick_entry_logs.logged_at for time-based filtering
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- Unique constraint to prevent duplicate embeddings
    CONSTRAINT unique_quick_entry_embedding UNIQUE (quick_entry_log_id, embedding_type)
);

-- Vector similarity search index (HNSW for fast approximate search)
CREATE INDEX idx_quick_entry_embeddings_vector
    ON public.quick_entry_embeddings
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Standard indexes
CREATE INDEX idx_quick_entry_embeddings_user_id ON public.quick_entry_embeddings(user_id);
CREATE INDEX idx_quick_entry_embeddings_logged_at ON public.quick_entry_embeddings(logged_at DESC);
CREATE INDEX idx_quick_entry_embeddings_classification ON public.quick_entry_embeddings(source_classification);
CREATE INDEX idx_quick_entry_embeddings_active ON public.quick_entry_embeddings(user_id, is_active) WHERE is_active = TRUE;
CREATE INDEX idx_quick_entry_embeddings_content_hash ON public.quick_entry_embeddings(content_hash);

-- Full-text search index
CREATE INDEX idx_quick_entry_embeddings_content_fts ON public.quick_entry_embeddings USING gin(to_tsvector('english', content_text));

-- RLS Policies
ALTER TABLE public.quick_entry_embeddings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own embeddings"
    ON public.quick_entry_embeddings FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "System can insert embeddings"
    ON public.quick_entry_embeddings FOR INSERT
    WITH CHECK (auth.uid() = user_id OR auth.role() = 'service_role');

CREATE POLICY "System can update embeddings"
    ON public.quick_entry_embeddings FOR UPDATE
    USING (auth.uid() = user_id OR auth.role() = 'service_role');

-- =============================================================================
-- 3. ENHANCED MEAL LOGS TABLE (Backward Compatible)
-- =============================================================================
-- Add quick_entry linking to existing meal_logs table

ALTER TABLE public.meal_logs
    ADD COLUMN IF NOT EXISTS quick_entry_log_id UUID REFERENCES public.quick_entry_logs(id) ON DELETE SET NULL,
    ADD COLUMN IF NOT EXISTS ai_extracted BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS ai_confidence NUMERIC(3, 2) CHECK (ai_confidence >= 0 AND ai_confidence <= 1),
    ADD COLUMN IF NOT EXISTS extraction_metadata JSONB DEFAULT '{}'::JSONB;

CREATE INDEX IF NOT EXISTS idx_meal_logs_quick_entry ON public.meal_logs(quick_entry_log_id) WHERE quick_entry_log_id IS NOT NULL;

COMMENT ON COLUMN public.meal_logs.quick_entry_log_id IS 'Links to quick_entry_logs if this meal was created via Quick Entry';
COMMENT ON COLUMN public.meal_logs.ai_extracted IS 'TRUE if this meal was extracted by AI from Quick Entry';
COMMENT ON COLUMN public.meal_logs.ai_confidence IS 'AI confidence score (0.0 to 1.0) for extraction accuracy';
COMMENT ON COLUMN public.meal_logs.extraction_metadata IS 'Metadata about AI extraction (model, tokens, cost, etc.)';

-- =============================================================================
-- 4. ENHANCED ACTIVITIES TABLE (Backward Compatible)
-- =============================================================================
-- Add quick_entry linking to existing activities table

ALTER TABLE public.activities
    ADD COLUMN IF NOT EXISTS quick_entry_log_id UUID REFERENCES public.quick_entry_logs(id) ON DELETE SET NULL,
    ADD COLUMN IF NOT EXISTS ai_extracted BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS ai_confidence NUMERIC(3, 2) CHECK (ai_confidence >= 0 AND ai_confidence <= 1),
    ADD COLUMN IF NOT EXISTS extraction_metadata JSONB DEFAULT '{}'::JSONB;

CREATE INDEX IF NOT EXISTS idx_activities_quick_entry ON public.activities(quick_entry_log_id) WHERE quick_entry_log_id IS NOT NULL;

COMMENT ON COLUMN public.activities.quick_entry_log_id IS 'Links to quick_entry_logs if this activity was created via Quick Entry';

-- =============================================================================
-- 5. ENHANCED BODY MEASUREMENTS TABLE (Backward Compatible)
-- =============================================================================
-- Add quick_entry linking to existing body_measurements table

ALTER TABLE public.body_measurements
    ADD COLUMN IF NOT EXISTS quick_entry_log_id UUID REFERENCES public.quick_entry_logs(id) ON DELETE SET NULL,
    ADD COLUMN IF NOT EXISTS ai_extracted BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS ai_confidence NUMERIC(3, 2) CHECK (ai_confidence >= 0 AND ai_confidence <= 1),
    ADD COLUMN IF NOT EXISTS extraction_metadata JSONB DEFAULT '{}'::JSONB;

CREATE INDEX IF NOT EXISTS idx_body_measurements_quick_entry ON public.body_measurements(quick_entry_log_id) WHERE quick_entry_log_id IS NOT NULL;

-- =============================================================================
-- 6. QUICK ENTRY STATISTICS TABLE (Analytics)
-- =============================================================================
-- Track user-level statistics for Quick Entry usage

CREATE TABLE IF NOT EXISTS public.quick_entry_stats (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Usage counts
    total_entries INTEGER DEFAULT 0,
    text_entries INTEGER DEFAULT 0,
    voice_entries INTEGER DEFAULT 0,
    image_entries INTEGER DEFAULT 0,
    multimodal_entries INTEGER DEFAULT 0,

    -- Extraction success rates
    meal_extractions INTEGER DEFAULT 0,
    workout_extractions INTEGER DEFAULT 0,
    body_measurement_extractions INTEGER DEFAULT 0,
    failed_extractions INTEGER DEFAULT 0,

    -- AI cost tracking
    total_ai_cost_usd NUMERIC(10, 2) DEFAULT 0,
    total_tokens_used BIGINT DEFAULT 0,

    -- Performance metrics
    avg_processing_time_ms INTEGER,
    avg_confidence_score NUMERIC(3, 2),

    -- Timestamps
    first_entry_at TIMESTAMPTZ,
    last_entry_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS
ALTER TABLE public.quick_entry_stats ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own stats"
    ON public.quick_entry_stats FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "System can update stats"
    ON public.quick_entry_stats FOR ALL
    USING (auth.role() = 'service_role');

-- =============================================================================
-- 7. DATABASE FUNCTIONS FOR SEMANTIC SEARCH
-- =============================================================================

-- Function: Search quick entry embeddings by semantic similarity
CREATE OR REPLACE FUNCTION public.search_quick_entry_embeddings(
    query_embedding vector(384),
    user_id_filter UUID,
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 10,
    classification_filter TEXT DEFAULT NULL,
    start_date TIMESTAMPTZ DEFAULT NULL,
    end_date TIMESTAMPTZ DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    quick_entry_log_id UUID,
    content_text TEXT,
    content_summary TEXT,
    similarity FLOAT,
    classification TEXT,
    logged_at TIMESTAMPTZ,
    metadata JSONB
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT
        qee.id,
        qee.quick_entry_log_id,
        qee.content_text,
        qee.content_summary,
        1 - (qee.embedding <=> query_embedding) AS similarity,
        qee.source_classification,
        qee.logged_at,
        qee.metadata
    FROM public.quick_entry_embeddings qee
    WHERE qee.user_id = user_id_filter
        AND qee.is_active = TRUE
        AND (1 - (qee.embedding <=> query_embedding)) > match_threshold
        AND (classification_filter IS NULL OR qee.source_classification = classification_filter)
        AND (start_date IS NULL OR qee.logged_at >= start_date)
        AND (end_date IS NULL OR qee.logged_at <= end_date)
    ORDER BY qee.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Function: Get RAG context for user query
CREATE OR REPLACE FUNCTION public.get_rag_context_for_quick_entry(
    p_user_id UUID,
    p_query_embedding vector(384),
    p_max_results INT DEFAULT 10,
    p_similarity_threshold FLOAT DEFAULT 0.7
)
RETURNS TEXT
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    context_text TEXT := '';
    result_record RECORD;
BEGIN
    -- Build context string from top semantic matches
    FOR result_record IN
        SELECT
            qee.content_text,
            qee.source_classification,
            qee.logged_at,
            qel.ai_classification,
            (1 - (qee.embedding <=> p_query_embedding)) AS similarity
        FROM public.quick_entry_embeddings qee
        JOIN public.quick_entry_logs qel ON qee.quick_entry_log_id = qel.id
        WHERE qee.user_id = p_user_id
            AND qee.is_active = TRUE
            AND (1 - (qee.embedding <=> p_query_embedding)) > p_similarity_threshold
        ORDER BY qee.embedding <=> p_query_embedding
        LIMIT p_max_results
    LOOP
        context_text := context_text || E'\n\n[' ||
            UPPER(result_record.source_classification) || ' | ' ||
            TO_CHAR(result_record.logged_at, 'YYYY-MM-DD HH24:MI') || ']\n' ||
            result_record.content_text;
    END LOOP;

    RETURN TRIM(context_text);
END;
$$;

-- Function: Update quick entry stats (trigger function)
CREATE OR REPLACE FUNCTION public.update_quick_entry_stats()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    -- Insert or update stats
    INSERT INTO public.quick_entry_stats (
        user_id,
        total_entries,
        text_entries,
        voice_entries,
        image_entries,
        multimodal_entries,
        meal_extractions,
        workout_extractions,
        body_measurement_extractions,
        failed_extractions,
        total_ai_cost_usd,
        total_tokens_used,
        first_entry_at,
        last_entry_at,
        updated_at
    )
    VALUES (
        NEW.user_id,
        1,
        CASE WHEN NEW.input_type = 'text' THEN 1 ELSE 0 END,
        CASE WHEN NEW.input_type = 'voice' THEN 1 ELSE 0 END,
        CASE WHEN NEW.input_type = 'image' THEN 1 ELSE 0 END,
        CASE WHEN NEW.input_type = 'multimodal' THEN 1 ELSE 0 END,
        CASE WHEN NEW.contains_meal THEN 1 ELSE 0 END,
        CASE WHEN NEW.contains_workout THEN 1 ELSE 0 END,
        CASE WHEN NEW.contains_body_measurement THEN 1 ELSE 0 END,
        CASE WHEN NEW.processing_status = 'failed' THEN 1 ELSE 0 END,
        COALESCE(NEW.ai_cost_usd, 0),
        COALESCE(NEW.tokens_used, 0),
        NEW.logged_at,
        NEW.logged_at,
        NOW()
    )
    ON CONFLICT (user_id) DO UPDATE SET
        total_entries = quick_entry_stats.total_entries + 1,
        text_entries = quick_entry_stats.text_entries + CASE WHEN NEW.input_type = 'text' THEN 1 ELSE 0 END,
        voice_entries = quick_entry_stats.voice_entries + CASE WHEN NEW.input_type = 'voice' THEN 1 ELSE 0 END,
        image_entries = quick_entry_stats.image_entries + CASE WHEN NEW.input_type = 'image' THEN 1 ELSE 0 END,
        multimodal_entries = quick_entry_stats.multimodal_entries + CASE WHEN NEW.input_type = 'multimodal' THEN 1 ELSE 0 END,
        meal_extractions = quick_entry_stats.meal_extractions + CASE WHEN NEW.contains_meal THEN 1 ELSE 0 END,
        workout_extractions = quick_entry_stats.workout_extractions + CASE WHEN NEW.contains_workout THEN 1 ELSE 0 END,
        body_measurement_extractions = quick_entry_stats.body_measurement_extractions + CASE WHEN NEW.contains_body_measurement THEN 1 ELSE 0 END,
        failed_extractions = quick_entry_stats.failed_extractions + CASE WHEN NEW.processing_status = 'failed' THEN 1 ELSE 0 END,
        total_ai_cost_usd = quick_entry_stats.total_ai_cost_usd + COALESCE(NEW.ai_cost_usd, 0),
        total_tokens_used = quick_entry_stats.total_tokens_used + COALESCE(NEW.tokens_used, 0),
        last_entry_at = NEW.logged_at,
        updated_at = NOW();

    RETURN NEW;
END;
$$;

-- Trigger: Update stats on new quick entry
CREATE TRIGGER trigger_update_quick_entry_stats
    AFTER INSERT ON public.quick_entry_logs
    FOR EACH ROW
    EXECUTE FUNCTION public.update_quick_entry_stats();

-- =============================================================================
-- 8. AUTOMATIC UPDATED_AT TRIGGER
-- =============================================================================

CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_quick_entry_logs_updated_at
    BEFORE UPDATE ON public.quick_entry_logs
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

-- =============================================================================
-- 9. VIEWS FOR EASY QUERYING
-- =============================================================================

-- View: Recent quick entries with embeddings
CREATE OR REPLACE VIEW public.quick_entries_with_embeddings AS
SELECT
    qel.id,
    qel.user_id,
    qel.input_type,
    qel.raw_text,
    qel.raw_transcription,
    qel.image_urls,
    qel.ai_classification,
    qel.ai_confidence_score,
    qel.contains_meal,
    qel.contains_workout,
    qel.contains_body_measurement,
    qel.logged_at,
    qel.processing_status,
    qel.ai_provider,
    qel.ai_model,
    qel.ai_cost_usd,
    qee.embedding IS NOT NULL AS has_embedding,
    qee.content_summary,
    qee.embedding_type
FROM public.quick_entry_logs qel
LEFT JOIN public.quick_entry_embeddings qee ON qel.id = qee.quick_entry_log_id;

-- View: Quick entry analytics per user
CREATE OR REPLACE VIEW public.quick_entry_analytics AS
SELECT
    user_id,
    COUNT(*) AS total_entries,
    COUNT(*) FILTER (WHERE processing_status = 'completed') AS successful_entries,
    COUNT(*) FILTER (WHERE processing_status = 'failed') AS failed_entries,
    COUNT(*) FILTER (WHERE contains_meal) AS meal_entries,
    COUNT(*) FILTER (WHERE contains_workout) AS workout_entries,
    COUNT(*) FILTER (WHERE contains_body_measurement) AS body_entries,
    AVG(ai_confidence_score) AS avg_confidence,
    SUM(ai_cost_usd) AS total_cost_usd,
    SUM(tokens_used) AS total_tokens,
    AVG(processing_duration_ms) AS avg_processing_time_ms,
    MIN(logged_at) AS first_entry_date,
    MAX(logged_at) AS last_entry_date
FROM public.quick_entry_logs
GROUP BY user_id;

-- =============================================================================
-- 10. COMMENTS FOR DOCUMENTATION
-- =============================================================================

COMMENT ON TABLE public.quick_entry_logs IS 'Main table storing ALL Quick Entry submissions with raw input, AI processing metadata, and structured extraction results';
COMMENT ON TABLE public.quick_entry_embeddings IS 'Vector embeddings for semantic search and RAG context building across all quick entries';
COMMENT ON TABLE public.quick_entry_stats IS 'Per-user statistics for Quick Entry usage, AI costs, and extraction success rates';

COMMENT ON FUNCTION public.search_quick_entry_embeddings IS 'Semantic similarity search across quick entry embeddings with filtering options';
COMMENT ON FUNCTION public.get_rag_context_for_quick_entry IS 'Build RAG context string from semantically similar quick entries for AI coach';

-- =============================================================================
-- 11. GRANT PERMISSIONS
-- =============================================================================

-- Grant authenticated users read access to their own data
GRANT SELECT ON public.quick_entry_logs TO authenticated;
GRANT SELECT ON public.quick_entry_embeddings TO authenticated;
GRANT SELECT ON public.quick_entry_stats TO authenticated;
GRANT SELECT ON public.quick_entries_with_embeddings TO authenticated;
GRANT SELECT ON public.quick_entry_analytics TO authenticated;

-- Grant service role full access for backend operations
GRANT ALL ON public.quick_entry_logs TO service_role;
GRANT ALL ON public.quick_entry_embeddings TO service_role;
GRANT ALL ON public.quick_entry_stats TO service_role;

-- Grant execute on functions
GRANT EXECUTE ON FUNCTION public.search_quick_entry_embeddings TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_rag_context_for_quick_entry TO service_role;

-- =============================================================================
-- MIGRATION COMPLETE
-- =============================================================================

-- Summary of changes:
-- ✅ Created quick_entry_logs table with full raw + processed data storage
-- ✅ Created quick_entry_embeddings table optimized for vector search
-- ✅ Enhanced existing meal_logs, activities, body_measurements tables
-- ✅ Created quick_entry_stats table for analytics
-- ✅ Added RLS policies on all tables
-- ✅ Created indexes for performance (including HNSW for vector search)
-- ✅ Created database functions for semantic search and RAG
-- ✅ Created triggers for automatic stats updates
-- ✅ Created views for easy querying
-- ✅ Added comprehensive comments

-- Next steps for implementation:
-- 1. Update backend service to use quick_entry_logs table
-- 2. Implement AI extraction pipeline (text → structured data)
-- 3. Generate embeddings using FREE sentence-transformers model
-- 4. Update RAG context builder to use search_quick_entry_embeddings()
-- 5. Add background job to clean up old embeddings (optional)
-- 6. Monitor AI costs using quick_entry_stats table
