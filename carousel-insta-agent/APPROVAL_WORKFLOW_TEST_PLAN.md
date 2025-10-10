# Approval Workflow - End-to-End Test Plan

## Test Execution Date: 2025-10-09

## Executive Summary

This document provides a comprehensive test plan for the Human-in-the-Loop approval workflow system. Tests validate the complete flow from carousel creation through final approval and engagement tracking.

---

## Test Environment

### Prerequisites
- Backend API running on `http://localhost:8000`
- Frontend running on `http://localhost:3000`
- PostgreSQL database with migration applied
- Test user authenticated with JWT token

### Test Data
```json
{
  "test_user_id": "550e8400-e29b-41d4-a716-446655440000",
  "test_carousel": {
    "topic": "10 AI Tools That Will Transform Your Workflow in 2025",
    "carousel_type": "explainer",
    "slide_count": 8,
    "brand_voice": "educational_engaging",
    "target_audience": "AI enthusiasts and productivity seekers"
  }
}
```

---

## Test Cases

### Test 1: Workflow Initialization
**Objective**: Verify approval workflow starts correctly when carousel is created

**Steps**:
1. POST `/api/v1/carousels` with test carousel data
2. Verify response includes `carousel_id`
3. GET `/api/v1/carousels/{carousel_id}/approval`
4. Verify 5 stages created: research, outline, copywriting, hook, visual
5. Verify first stage (research) is in "generating" status
6. Verify remaining stages are "pending"

**Expected Results**:
```json
{
  "carousel_id": "uuid",
  "current_stage": "research",
  "stages": [
    {
      "stage": "research",
      "stage_order": 1,
      "status": "generating",
      "variants_generated": false
    },
    {
      "stage": "outline",
      "stage_order": 2,
      "status": "pending",
      "variants_generated": false
    }
    // ... 3 more stages
  ],
  "overall_progress_percentage": 0,
  "awaiting_user_action": false
}
```

**Pass Criteria**: ✅ All 5 stages created, research stage generating

---

### Test 2: Research Variant Generation
**Objective**: Verify 3 research variants are generated with different strategies

**Steps**:
1. Wait for research stage status to change to "awaiting_approval" (poll every 5s)
2. GET `/api/v1/carousels/{carousel_id}/approval/stages/research`
3. Verify 3 variants returned
4. Verify variant strategies: "comprehensive", "focused", "visual_first"
5. Verify each variant has heuristic_score (0-10)
6. Verify each variant has scoring_criteria object

**Expected Results**:
```json
{
  "stage": "research",
  "variants": [
    {
      "id": "variant-uuid-1",
      "variant_number": 1,
      "data": {
        "variant_name": "Comprehensive Research",
        "strategy": "comprehensive",
        "key_facts": [...],
        "reddit_insights": [...],
        "twitter_trends": [...]
      },
      "heuristic_score": 8.5,
      "scoring_criteria": {
        "fact_count": 12,
        "source_diversity": 3,
        "recency_score": 0.9
      },
      "selected": false,
      "user_edited": false
    },
    // ... 2 more variants
  ]
}
```

**Pass Criteria**: ✅ 3 variants with different strategies, all have heuristic scores

---

### Test 3: User Approves Research Variant
**Objective**: Verify approval triggers outline stage generation

**Steps**:
1. POST `/api/v1/carousels/{carousel_id}/approval/approve`
   ```json
   {
     "variant_id": "variant-uuid-2",
     "user_notes": "I prefer the focused approach",
     "selection_reason": "More targeted for audience"
   }
   ```
2. Verify response confirms approval
3. GET `/api/v1/carousels/{carousel_id}/approval`
4. Verify research stage status is "approved"
5. Verify outline stage status is "generating"
6. Verify `user_selections` table has record for research stage

**Expected Results**:
```json
{
  "message": "Variant approved successfully",
  "next_stage": "outline",
  "workflow_progressed": true
}
```

**Database Check**:
```sql
SELECT * FROM user_selections WHERE carousel_id = '{carousel_id}' AND stage = 'research';
-- Should return 1 row with selected variant_id
```

**Pass Criteria**: ✅ Research approved, outline generation triggered

---

### Test 4: Outline Variant Generation
**Objective**: Verify outline variants use approved research data

**Steps**:
1. Wait for outline stage to reach "awaiting_approval"
2. GET `/api/v1/carousels/{carousel_id}/approval/stages/outline`
3. Verify 3 outline variants returned
4. Verify variant strategies: "narrative", "informational", "action_oriented"
5. Inspect variant data to confirm it uses research from approved variant

**Expected Variant Structures**:
```json
{
  "variant_name": "Narrative Flow",
  "strategy": "narrative",
  "slides": [
    {
      "slide_number": 1,
      "theme": "Introduction",
      "key_point": "AI is transforming how we work"
    },
    // ... 7 more slides
  ],
  "based_on_research": "focused" // Should match approved variant strategy
}
```

**Pass Criteria**: ✅ 3 outline variants, data derived from approved research

---

### Test 5: User Edits Variant Before Approval
**Objective**: Verify edit functionality and user_edited flag

**Steps**:
1. PATCH `/api/v1/carousels/{carousel_id}/approval/edit`
   ```json
   {
     "variant_id": "outline-variant-1",
     "stage": "outline",
     "edited_data": {
       "slides": [
         {
           "slide_number": 1,
           "theme": "Hook - Attention Grabber",
           "key_point": "You're losing 10 hours/week to manual tasks"
         },
         // ... edited slides
       ]
     },
     "edit_notes": "Made hook more compelling, added specific time savings"
   }
   ```
2. Verify edited variant saved
3. Approve the edited variant
4. Verify `user_edited` flag is true in database

**Expected Results**:
```json
{
  "message": "Variant updated successfully",
  "variant": {
    "id": "outline-variant-1",
    "user_edited": true,
    "data": {
      "slides": [/* edited content */]
    }
  }
}
```

**Pass Criteria**: ✅ Edit saved, user_edited flag set, can approve edited variant

---

### Test 6: Copywriting Variant Generation
**Objective**: Verify copywriting variants use approved outline structure

**Steps**:
1. Approve edited outline variant
2. Wait for copywriting stage to reach "awaiting_approval"
3. GET `/api/v1/carousels/{carousel_id}/approval/stages/copywriting`
4. Verify 3 copywriting variants with tones: "educational", "conversational", "professional"
5. Verify slide copy matches outline structure from approved variant

**Expected Variant**:
```json
{
  "variant_name": "Conversational Tone",
  "strategy": "conversational",
  "slides": [
    {
      "slide_number": 1,
      "headline": "You're Wasting 10 Hours Every Week",
      "body": "Let's fix that. Here are 10 AI tools that'll give you your time back.",
      "cta": "Swipe to save hours →"
    },
    // ... matching outline structure
  ]
}
```

**Pass Criteria**: ✅ 3 copywriting variants, structure matches approved outline

---

### Test 7: Hook Variant Generation (10 Variants)
**Objective**: Verify hook stage generates 10 variations, not 3

**Steps**:
1. Approve copywriting variant (conversational tone)
2. Wait for hook stage to reach "awaiting_approval"
3. GET `/api/v1/carousels/{carousel_id}/approval/stages/hook`
4. Verify 10 hook variants returned (uses existing HookAgent)
5. Verify each hook has heuristic score based on:
   - Word count (5-10 optimal)
   - Question mark (curiosity)
   - Numbers (specificity)
   - Caps emphasis (1 word)

**Expected Heuristic Scoring**:
```json
{
  "id": "hook-variant-3",
  "data": {
    "hook": "Which of These 10 AI Tools Will SAVE You 10 Hours This Week?"
  },
  "heuristic_score": 9.2,
  "scoring_criteria": {
    "word_count_score": 10.0,  // 11 words (-0.5 penalty)
    "has_question": 2.0,        // Has question mark
    "has_numbers": 2.0,         // Has numbers (10, 10)
    "caps_emphasis": 1.0        // 1 caps word (SAVE)
  }
}
```

**Pass Criteria**: ✅ 10 hook variants, heuristic scores calculated correctly

---

### Test 8: Visual Variant Generation
**Objective**: Verify visual design template variants

**Steps**:
1. Approve hook variant with highest heuristic score
2. Wait for visual stage to reach "awaiting_approval"
3. GET `/api/v1/carousels/{carousel_id}/approval/stages/visual`
4. Verify 3 visual variants with templates:
   - Modern Minimal
   - Bold Vibrant
   - Tech Professional
5. Verify each has color scheme and font definitions

**Expected Visual Variant**:
```json
{
  "variant_name": "Bold Vibrant",
  "strategy": "bold_vibrant",
  "template_id": "bold_vibrant",
  "colors": {
    "primary": "#f59e0b",
    "secondary": "#ef4444",
    "accent": "#10b981",
    "background": "#1f2937",
    "text": "#ffffff"
  },
  "fonts": {
    "primary": "Montserrat",
    "secondary": "Raleway"
  },
  "style": "Eye-catching colors and dynamic layouts"
}
```

**Pass Criteria**: ✅ 3 visual templates with complete color/font specs

---

### Test 9: Workflow Completion
**Objective**: Verify carousel finalization after all stages approved

**Steps**:
1. Approve visual variant (Modern Minimal)
2. Verify workflow status changes to "completed"
3. GET `/api/v1/carousels/{carousel_id}`
4. Verify carousel status is "completed"
5. Verify `completed_at` timestamp is set
6. Verify final carousel has all approved variant data:
   - Research data
   - Outline structure
   - Slide copywriting
   - Final hook
   - Visual template

**Expected Carousel Data**:
```json
{
  "id": "carousel-uuid",
  "status": "completed",
  "completed_at": "2025-10-09T14:30:00Z",
  "research_data": {/* approved research variant */},
  "outline": {/* approved outline variant */},
  "slides": [/* approved copywriting variant */],
  "hook": "Which of These 10 AI Tools Will SAVE You 10 Hours This Week?",
  "visual_template": "modern_minimal"
}
```

**Pass Criteria**: ✅ Carousel completed, all approved variants composed into final output

---

### Test 10: Engagement Data Recording
**Objective**: Verify real Instagram metrics can be recorded and save_rate calculated

**Steps**:
1. POST `/api/v1/carousels/{carousel_id}/engagement`
   ```json
   {
     "carousel_id": "carousel-uuid",
     "impressions": 12500,
     "reach": 9800,
     "likes": 430,
     "comments": 28,
     "saves": 385,
     "shares": 67,
     "published_at": "2025-10-09T10:00:00Z"
   }
   ```
2. Verify response includes calculated metrics
3. Verify `engagement_learnings` table record created
4. Verify `performed_well` flag set correctly (save_rate > 3%)

**Expected Response**:
```json
{
  "message": "Engagement data recorded successfully",
  "metrics": {
    "save_rate": 3.08,  // (385 / 12500) * 100
    "engagement_rate": 7.28,  // ((430+28+385+67) / 12500) * 100
    "performed_well": true  // 3.08% > 3%
  },
  "learning_id": "learning-uuid"
}
```

**Database Check**:
```sql
SELECT * FROM engagement_learnings WHERE carousel_id = '{carousel_id}';
-- Should link to all approved variant IDs
```

**Pass Criteria**: ✅ Engagement recorded, save_rate > 3%, performed_well = true

---

### Test 11: Rejection and Regeneration
**Objective**: Verify user can reject all variants and trigger regeneration

**Steps**:
1. Create new test carousel
2. Wait for research variants to generate
3. POST `/api/v1/carousels/{carousel_id}/approval/reject`
   ```json
   {
     "carousel_id": "carousel-uuid-2",
     "stage": "research",
     "rejection_reason": "Not enough focus on enterprise use cases",
     "regeneration_prompt": "Focus on enterprise AI adoption, include ROI data and case studies from Fortune 500 companies"
   }
   ```
4. Verify research stage status returns to "generating"
5. Verify new variants incorporate regeneration_prompt
6. Verify rejection recorded in database

**Expected Behavior**:
- All 3 research variants marked as rejected
- New variants generated with adjusted prompt
- User can approve or reject again

**Pass Criteria**: ✅ Rejection triggers regeneration, new variants reflect user feedback

---

### Test 12: Frontend Approval UI
**Objective**: Verify frontend UI displays workflow correctly

**Manual Test Steps**:
1. Navigate to `http://localhost:3000/carousel/{carousel_id}/approval`
2. Verify 5-stage progress tracker displays
3. Verify current stage highlighted
4. Verify 3 variant cards displayed for current stage
5. Verify each card shows:
   - Variant number
   - Heuristic score
   - Content preview
   - Approve/Edit buttons
6. Click "Approve" on variant
7. Verify stage progresses automatically
8. Verify next stage variants load
9. Complete workflow to visual stage
10. Navigate to engagement form
11. Submit Instagram metrics
12. Verify success message with save_rate calculation

**UI Components to Verify**:
- `ApprovalPage` component renders
- `VariantCard` components display correctly
- Stage progression updates in real-time (5s polling)
- Edit dialog works
- Engagement form calculates metrics correctly

**Pass Criteria**: ✅ All UI components functional, workflow progresses smoothly

---

### Test 13: Error Handling
**Objective**: Verify graceful error handling

**Test Cases**:
1. **Approve non-existent variant**:
   - POST approve with invalid variant_id
   - Expect 404 error with message

2. **Approve already approved stage**:
   - POST approve on completed stage
   - Expect 400 error

3. **Missing required fields**:
   - POST approve without variant_id
   - Expect 422 validation error

4. **Database connection failure**:
   - Simulate DB disconnect
   - Expect 500 error with retry message

5. **AI service timeout**:
   - Variant generation exceeds timeout
   - Expect graceful retry mechanism

**Pass Criteria**: ✅ All errors handled gracefully, user-friendly messages

---

### Test 14: Performance & Cost Validation
**Objective**: Verify system performance and AI costs

**Metrics to Track**:
1. **Response Times**:
   - Approval status: < 200ms
   - Approve variant: < 500ms
   - Variant generation: < 30s per stage

2. **AI Costs Per Carousel**:
   - Research variants (3): ~$0.15 (Groq)
   - Outline variants (3): ~$0.20 (Groq)
   - Copywriting variants (3): ~$0.30 (Claude)
   - Hook variants (10): ~$0.10 (Claude)
   - Visual variants (3): $0.00 (templates)
   - **Total: ~$0.75 per carousel**

3. **Database Queries**:
   - Use `EXPLAIN ANALYZE` to verify indexes used
   - Approval status query: < 50ms
   - Variant fetch: < 30ms

**Cost Monitoring**:
```sql
SELECT
  SUM(cost) as total_cost,
  COUNT(*) as api_calls,
  AVG(cost) as avg_cost_per_call
FROM api_usage_logs
WHERE carousel_id = '{carousel_id}';
```

**Pass Criteria**: ✅ Response times acceptable, costs within budget ($0.75/carousel)

---

### Test 15: Learning System Validation
**Objective**: Verify variant performance tracking

**Steps**:
1. Create 3 test carousels with different variant combinations
2. Record engagement for each:
   - Carousel A: save_rate 4.2% (performed well)
   - Carousel B: save_rate 2.1% (underperformed)
   - Carousel C: save_rate 3.8% (performed well)
3. Query `variant_performance` table
4. Verify patterns identified:
   - Which hook patterns perform best
   - Which copywriting tones get highest saves
   - Which research strategies lead to success

**Expected Analytics**:
```sql
SELECT
  hook_pattern,
  AVG(save_rate) as avg_save_rate,
  COUNT(*) as usage_count
FROM variant_performance
WHERE performed_well = true
GROUP BY hook_pattern
ORDER BY avg_save_rate DESC;
```

**Pass Criteria**: ✅ Performance data linked to variants, patterns identifiable

---

## Test Execution Checklist

### Pre-Test Setup
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database migration applied
- [ ] Test user created and authenticated
- [ ] API keys configured (Anthropic, Groq, OpenAI)

### Core Workflow Tests
- [ ] Test 1: Workflow Initialization
- [ ] Test 2: Research Variant Generation
- [ ] Test 3: User Approves Research Variant
- [ ] Test 4: Outline Variant Generation
- [ ] Test 5: User Edits Variant Before Approval
- [ ] Test 6: Copywriting Variant Generation
- [ ] Test 7: Hook Variant Generation (10 Variants)
- [ ] Test 8: Visual Variant Generation
- [ ] Test 9: Workflow Completion
- [ ] Test 10: Engagement Data Recording

### Edge Cases & Error Handling
- [ ] Test 11: Rejection and Regeneration
- [ ] Test 13: Error Handling

### UI & Performance
- [ ] Test 12: Frontend Approval UI
- [ ] Test 14: Performance & Cost Validation
- [ ] Test 15: Learning System Validation

---

## Success Criteria

The approval workflow is considered **production-ready** when:

1. ✅ All 15 test cases pass
2. ✅ No critical bugs identified
3. ✅ Response times within acceptable limits
4. ✅ AI costs within budget ($0.75/carousel)
5. ✅ User experience smooth and intuitive
6. ✅ Real engagement data validates quality (save_rate > 3%)
7. ✅ Learning system captures successful patterns

---

## Test Results Summary

**Test Execution Date**: _[To be filled during testing]_

**Overall Pass Rate**: _[X/15 tests passed]_

**Critical Issues Found**: _[List any blocking issues]_

**Recommendations**: _[Next steps based on test results]_

---

## Automated Test Script

```bash
#!/bin/bash
# Run automated API tests

BASE_URL="http://localhost:8000/api/v1"
CAROUSEL_ID=""

echo "🧪 Starting Approval Workflow Tests..."

# Test 1: Create carousel
echo "Test 1: Creating carousel..."
RESPONSE=$(curl -s -X POST "$BASE_URL/carousels" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "10 AI Tools That Will Transform Your Workflow in 2025",
    "carousel_type": "explainer",
    "slide_count": 8
  }')

CAROUSEL_ID=$(echo $RESPONSE | jq -r '.id')
echo "✅ Carousel created: $CAROUSEL_ID"

# Test 2: Check workflow status
echo "Test 2: Checking workflow status..."
curl -s "$BASE_URL/carousels/$CAROUSEL_ID/approval" | jq '.stages'

# Test 3: Wait for research variants
echo "Test 3: Waiting for research variants..."
while true; do
  STATUS=$(curl -s "$BASE_URL/carousels/$CAROUSEL_ID/approval/stages/research" | jq -r '.status')
  if [ "$STATUS" == "awaiting_approval" ]; then
    echo "✅ Research variants ready"
    break
  fi
  echo "⏳ Status: $STATUS (waiting...)"
  sleep 5
done

# ... more automated tests

echo "✅ All automated tests completed"
```

---

## Manual Testing Checklist

### User Experience Flow
1. [ ] User creates carousel from dashboard
2. [ ] User receives notification when research stage ready
3. [ ] User reviews 3 research variants
4. [ ] User approves variant with highest score
5. [ ] System auto-progresses to outline stage
6. [ ] User edits outline variant before approving
7. [ ] User continues through copywriting, hook, visual stages
8. [ ] User receives completed carousel
9. [ ] User publishes to Instagram
10. [ ] User records engagement metrics 24-48 hours later
11. [ ] System confirms performance (save_rate > 3%)
12. [ ] System learns from successful variant combination

### UI/UX Validation
- [ ] Progress tracker clearly shows current stage
- [ ] Variant cards are visually distinct
- [ ] Heuristic scores are explained
- [ ] Edit dialog is intuitive
- [ ] Approve/Reject buttons are prominent
- [ ] Loading states provide feedback
- [ ] Error messages are helpful
- [ ] Mobile responsive (optional)

---

## Post-Test Actions

### If All Tests Pass:
1. ✅ Mark system as production-ready
2. ✅ Deploy to staging environment
3. ✅ Conduct user acceptance testing
4. ✅ Prepare for beta launch
5. ✅ Monitor engagement data from first 10 carousels

### If Tests Fail:
1. ❌ Document all failures
2. ❌ Prioritize by severity (critical, major, minor)
3. ❌ Fix critical bugs immediately
4. ❌ Re-run failed tests
5. ❌ Repeat until all tests pass

---

## Appendix: Test Data Examples

### Sample Research Variant
```json
{
  "variant_name": "Comprehensive Research",
  "strategy": "comprehensive",
  "key_facts": [
    "ChatGPT reached 100M users in 2 months, fastest growth in tech history",
    "70% of knowledge workers now use AI tools daily (McKinsey, 2025)",
    "AI automation saves average 10 hours/week per employee"
  ],
  "reddit_insights": [
    "r/productivity top post: 'I automated my email with Claude, saved 2 hrs/day'",
    "r/entrepreneur: 'AI tools are the new competitive advantage'"
  ],
  "twitter_trends": [
    "#AIProductivity trending with 50K mentions this week"
  ]
}
```

### Sample Engagement Learning
```json
{
  "carousel_id": "uuid",
  "impressions": 12500,
  "saves": 385,
  "save_rate": 3.08,
  "performed_well": true,
  "research_variant_id": "focused-variant-uuid",
  "outline_variant_id": "narrative-variant-uuid",
  "copywriting_variant_id": "conversational-variant-uuid",
  "hook_variant_id": "hook-9-variant-uuid",
  "visual_variant_id": "modern-minimal-uuid",
  "pattern_identified": "focused_research + conversational_copy + question_hook = high_saves"
}
```

---

**End of Test Plan**
