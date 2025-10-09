-- Migration 017: Activity Deduplication System
-- Creates merge request tracking for duplicate activity detection
-- Created: 2025-10-09

-- ============================================================================
-- CREATE ACTIVITY MERGE REQUESTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.activity_merge_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Activity references
    primary_activity_id UUID NOT NULL REFERENCES public.activities(id) ON DELETE CASCADE,
    duplicate_activity_id UUID NOT NULL REFERENCES public.activities(id) ON DELETE CASCADE,

    -- Deduplication metadata
    confidence_score INTEGER NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 100),
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'auto_merged')),

    -- Reason details (JSON with matching signals)
    merge_reason JSONB NOT NULL DEFAULT '{}',
    -- Example: {
    --   "time_diff_minutes": 5,
    --   "duration_diff_pct": 2.3,
    --   "distance_diff_pct": 1.5,
    --   "same_type": true,
    --   "same_date": true,
    --   "signals_matched": ["time", "duration", "distance", "type"]
    -- }

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    resolved_by TEXT, -- 'user' or 'auto'

    -- Constraints
    CONSTRAINT different_activities CHECK (primary_activity_id != duplicate_activity_id),
    CONSTRAINT unique_merge_pair UNIQUE (user_id, primary_activity_id, duplicate_activity_id)
);

-- Indexes for efficient queries
CREATE INDEX idx_merge_requests_user_status ON public.activity_merge_requests(user_id, status);
CREATE INDEX idx_merge_requests_created ON public.activity_merge_requests(created_at DESC);
CREATE INDEX idx_merge_requests_confidence ON public.activity_merge_requests(confidence_score DESC);
CREATE INDEX idx_merge_requests_primary_activity ON public.activity_merge_requests(primary_activity_id);

-- ============================================================================
-- ROW LEVEL SECURITY POLICIES
-- ============================================================================

ALTER TABLE public.activity_merge_requests ENABLE ROW LEVEL SECURITY;

-- Users can view their own merge requests
CREATE POLICY "Users can view own merge requests"
ON public.activity_merge_requests FOR SELECT
USING (auth.uid() = user_id);

-- Users can insert merge requests (for manual detection)
CREATE POLICY "Users can create merge requests"
ON public.activity_merge_requests FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own merge requests (approve/reject)
CREATE POLICY "Users can update own merge requests"
ON public.activity_merge_requests FOR UPDATE
USING (auth.uid() = user_id);

-- Service role can manage all merge requests (for auto-detection)
CREATE POLICY "Service role can manage all merge requests"
ON public.activity_merge_requests FOR ALL
USING (auth.jwt()->>'role' = 'service_role');

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Function to get pending merge requests count for user
CREATE OR REPLACE FUNCTION public.get_pending_merge_requests_count(
    p_user_id UUID
)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT COUNT(*)::INTEGER
        FROM public.activity_merge_requests
        WHERE user_id = p_user_id
        AND status = 'pending'
    );
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- Function to approve merge request and mark duplicate as merged
CREATE OR REPLACE FUNCTION public.approve_merge_request(
    p_merge_request_id UUID,
    p_user_id UUID
)
RETURNS JSONB AS $$
DECLARE
    v_merge_request RECORD;
    v_result JSONB;
BEGIN
    -- Get merge request details
    SELECT * INTO v_merge_request
    FROM public.activity_merge_requests
    WHERE id = p_merge_request_id
    AND user_id = p_user_id
    AND status = 'pending';

    IF NOT FOUND THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Merge request not found or already resolved'
        );
    END IF;

    -- Mark duplicate activity as duplicate
    UPDATE public.activities
    SET is_duplicate = true,
        duplicate_of = v_merge_request.primary_activity_id,
        updated_at = NOW()
    WHERE id = v_merge_request.duplicate_activity_id
    AND user_id = p_user_id;

    -- Update merge request status
    UPDATE public.activity_merge_requests
    SET status = 'approved',
        resolved_at = NOW(),
        resolved_by = 'user'
    WHERE id = p_merge_request_id;

    RETURN jsonb_build_object(
        'success', true,
        'primary_activity_id', v_merge_request.primary_activity_id,
        'duplicate_activity_id', v_merge_request.duplicate_activity_id
    );
END;
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;

-- Function to reject merge request
CREATE OR REPLACE FUNCTION public.reject_merge_request(
    p_merge_request_id UUID,
    p_user_id UUID
)
RETURNS JSONB AS $$
BEGIN
    UPDATE public.activity_merge_requests
    SET status = 'rejected',
        resolved_at = NOW(),
        resolved_by = 'user'
    WHERE id = p_merge_request_id
    AND user_id = p_user_id
    AND status = 'pending';

    IF FOUND THEN
        RETURN jsonb_build_object('success', true);
    ELSE
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Merge request not found or already resolved'
        );
    END IF;
END;
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;

-- ============================================================================
-- ADD DUPLICATE TRACKING TO ACTIVITIES TABLE
-- ============================================================================

-- Add columns to activities table if they don't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'activities' AND column_name = 'is_duplicate'
    ) THEN
        ALTER TABLE public.activities ADD COLUMN is_duplicate BOOLEAN NOT NULL DEFAULT false;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'activities' AND column_name = 'duplicate_of'
    ) THEN
        ALTER TABLE public.activities ADD COLUMN duplicate_of UUID REFERENCES public.activities(id) ON DELETE SET NULL;
    END IF;
END $$;

-- Index for duplicate queries
CREATE INDEX IF NOT EXISTS idx_activities_duplicate ON public.activities(user_id, is_duplicate);
CREATE INDEX IF NOT EXISTS idx_activities_duplicate_of ON public.activities(duplicate_of) WHERE duplicate_of IS NOT NULL;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE public.activity_merge_requests IS 'Tracks duplicate activity detection and merge requests';
COMMENT ON COLUMN public.activity_merge_requests.confidence_score IS 'Confidence that activities are duplicates (0-100)';
COMMENT ON COLUMN public.activity_merge_requests.merge_reason IS 'JSON with matching signals (time, duration, distance, type)';
COMMENT ON COLUMN public.activity_merge_requests.status IS 'pending: awaiting user action, approved: merged, rejected: not duplicates, auto_merged: automatically merged';

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- Summary:
-- ✅ Created activity_merge_requests table
-- ✅ Added RLS policies for secure access
-- ✅ Created helper functions for merge approval/rejection
-- ✅ Added duplicate tracking columns to activities
-- ✅ Created indexes for efficient queries
