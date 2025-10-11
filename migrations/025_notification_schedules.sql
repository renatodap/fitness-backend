-- Migration: Notification Schedules
-- Description: Add tables for adaptive notification system based on user behavior patterns
-- Date: 2025-10-11

-- ============================================
-- Table: notification_schedules
-- ============================================
-- Stores user's notification preferences and schedules
CREATE TABLE IF NOT EXISTS notification_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Schedule settings
    enabled BOOLEAN DEFAULT FALSE,
    notification_time TIME NOT NULL, -- Time of day to send (e.g., 07:00:00)
    timezone TEXT DEFAULT 'UTC',
    days_of_week INTEGER[] DEFAULT '{1,2,3,4,5,6,7}', -- 1=Monday, 7=Sunday

    -- Adaptive settings
    is_auto_detected BOOLEAN DEFAULT TRUE, -- TRUE if system suggested this time
    detection_confidence FLOAT DEFAULT 0.0, -- 0.0-1.0 confidence in auto-detection
    pattern_frequency INTEGER DEFAULT 0, -- How many times this pattern was observed

    -- Notification content
    notification_type TEXT DEFAULT 'daily_reminder', -- daily_reminder, meal_reminder, workout_reminder
    message_template TEXT, -- Optional custom message

    -- Metadata
    last_sent_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT valid_notification_type CHECK (notification_type IN ('daily_reminder', 'meal_reminder', 'workout_reminder', 'custom')),
    CONSTRAINT valid_confidence CHECK (detection_confidence BETWEEN 0.0 AND 1.0)
);

-- Indexes
CREATE INDEX idx_notification_schedules_user_id ON notification_schedules(user_id);
CREATE INDEX idx_notification_schedules_enabled ON notification_schedules(enabled);
CREATE INDEX idx_notification_schedules_notification_time ON notification_schedules(notification_time);

-- RLS Policies
ALTER TABLE notification_schedules ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own notification schedules"
ON notification_schedules FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own notification schedules"
ON notification_schedules FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own notification schedules"
ON notification_schedules FOR UPDATE
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own notification schedules"
ON notification_schedules FOR DELETE
USING (auth.uid() = user_id);


-- ============================================
-- Table: notification_logs
-- ============================================
-- Tracks sent notifications for analytics
CREATE TABLE IF NOT EXISTS notification_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    schedule_id UUID REFERENCES notification_schedules(id) ON DELETE SET NULL,

    -- Notification details
    notification_type TEXT NOT NULL,
    message TEXT NOT NULL,
    sent_at TIMESTAMPTZ DEFAULT NOW(),

    -- Engagement tracking
    opened BOOLEAN DEFAULT FALSE,
    opened_at TIMESTAMPTZ,
    action_taken TEXT, -- e.g., 'logged_meal', 'opened_dashboard', 'dismissed'
    action_taken_at TIMESTAMPTZ,

    -- Metadata
    delivery_status TEXT DEFAULT 'sent', -- sent, delivered, failed
    error_message TEXT,

    CONSTRAINT valid_delivery_status CHECK (delivery_status IN ('sent', 'delivered', 'failed'))
);

-- Indexes
CREATE INDEX idx_notification_logs_user_id ON notification_logs(user_id);
CREATE INDEX idx_notification_logs_sent_at ON notification_logs(sent_at);
CREATE INDEX idx_notification_logs_schedule_id ON notification_logs(schedule_id);

-- RLS Policies
ALTER TABLE notification_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own notification logs"
ON notification_logs FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own notification logs"
ON notification_logs FOR INSERT
WITH CHECK (auth.uid() = user_id);


-- ============================================
-- Table: notification_pattern_analysis
-- ============================================
-- Stores analyzed patterns for notification suggestions
CREATE TABLE IF NOT EXISTS notification_pattern_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Pattern details
    pattern_type TEXT NOT NULL, -- app_open_pattern, meal_log_pattern, workout_pattern
    time_bucket TEXT NOT NULL, -- e.g., '07:00-07:30'
    frequency INTEGER DEFAULT 0, -- How many times observed in analysis window
    confidence FLOAT DEFAULT 0.0, -- 0.0-1.0 confidence score

    -- Analysis window
    analysis_start_date DATE NOT NULL,
    analysis_end_date DATE NOT NULL,
    days_analyzed INTEGER DEFAULT 0,

    -- Recommendation
    recommended_notification_time TIME,
    recommendation_reason TEXT,

    -- Metadata
    analyzed_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT valid_pattern_confidence CHECK (confidence BETWEEN 0.0 AND 1.0)
);

-- Indexes
CREATE INDEX idx_notification_pattern_analysis_user_id ON notification_pattern_analysis(user_id);
CREATE INDEX idx_notification_pattern_analysis_analyzed_at ON notification_pattern_analysis(analyzed_at);

-- RLS Policies
ALTER TABLE notification_pattern_analysis ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own pattern analysis"
ON notification_pattern_analysis FOR SELECT
USING (auth.uid() = user_id);


-- ============================================
-- Function: Update updated_at timestamp
-- ============================================
CREATE OR REPLACE FUNCTION update_notification_schedule_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER notification_schedules_updated_at
BEFORE UPDATE ON notification_schedules
FOR EACH ROW
EXECUTE FUNCTION update_notification_schedule_updated_at();


-- ============================================
-- Sample data (optional - for testing)
-- ============================================
-- Uncomment to insert sample notification schedule
-- INSERT INTO notification_schedules (user_id, enabled, notification_time, notification_type, is_auto_detected, detection_confidence, pattern_frequency)
-- VALUES (
--     'YOUR_USER_ID',
--     true,
--     '07:00:00',
--     'daily_reminder',
--     true,
--     0.85,
--     14
-- );
