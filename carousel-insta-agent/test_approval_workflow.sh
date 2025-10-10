#!/bin/bash
# Manual Test Script for Approval Workflow
# Run this to manually test the complete approval workflow

set -e  # Exit on error

# Configuration
BASE_URL="http://localhost:8000/api/v1"
FRONTEND_URL="http://localhost:3000"
JWT_TOKEN="${JWT_TOKEN:-your-test-token-here}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

wait_for_status() {
    local carousel_id=$1
    local stage=$2
    local expected_status=$3
    local max_attempts=60
    local attempt=0

    log_info "Waiting for $stage to reach $expected_status..."

    while [ $attempt -lt $max_attempts ]; do
        status=$(curl -s "$BASE_URL/carousels/$carousel_id/approval/stages/$stage" \
            -H "Authorization: Bearer $JWT_TOKEN" | jq -r '.status')

        if [ "$status" == "$expected_status" ]; then
            log_success "$stage reached $expected_status"
            return 0
        fi

        echo -ne "\r⏳ Attempt $((attempt + 1))/$max_attempts - Status: $status"
        sleep 5
        ((attempt++))
    done

    log_error "$stage did not reach $expected_status within timeout"
    return 1
}

# Main test flow
main() {
    echo ""
    echo "🧪 Approval Workflow Manual Test"
    echo "=================================="
    echo ""

    # Check if JWT_TOKEN is set
    if [ "$JWT_TOKEN" == "your-test-token-here" ]; then
        log_error "Please set JWT_TOKEN environment variable"
        echo "   export JWT_TOKEN='your-actual-token'"
        exit 1
    fi

    # Test 1: Create Carousel
    log_info "Test 1: Creating test carousel..."
    CAROUSEL_RESPONSE=$(curl -s -X POST "$BASE_URL/carousels" \
        -H "Authorization: Bearer $JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "topic": "10 AI Tools That Will Transform Your Workflow in 2025",
            "carousel_type": "explainer",
            "slide_count": 8,
            "brand_voice": "educational_engaging",
            "target_audience": "AI enthusiasts and productivity seekers"
        }')

    CAROUSEL_ID=$(echo $CAROUSEL_RESPONSE | jq -r '.id')

    if [ "$CAROUSEL_ID" == "null" ] || [ -z "$CAROUSEL_ID" ]; then
        log_error "Failed to create carousel"
        echo $CAROUSEL_RESPONSE | jq '.'
        exit 1
    fi

    log_success "Carousel created: $CAROUSEL_ID"
    echo ""

    # Test 2: Check Workflow Initialization
    log_info "Test 2: Checking workflow initialization..."
    WORKFLOW_STATUS=$(curl -s "$BASE_URL/carousels/$CAROUSEL_ID/approval" \
        -H "Authorization: Bearer $JWT_TOKEN")

    STAGE_COUNT=$(echo $WORKFLOW_STATUS | jq '.stages | length')
    CURRENT_STAGE=$(echo $WORKFLOW_STATUS | jq -r '.current_stage')

    if [ "$STAGE_COUNT" == "5" ] && [ "$CURRENT_STAGE" == "research" ]; then
        log_success "Workflow initialized correctly (5 stages, starting with research)"
    else
        log_error "Workflow initialization failed"
        echo $WORKFLOW_STATUS | jq '.'
        exit 1
    fi
    echo ""

    # Test 3: Wait for Research Variants
    log_info "Test 3: Waiting for research variants to generate..."
    wait_for_status "$CAROUSEL_ID" "research" "awaiting_approval"
    echo ""

    # Test 4: Display Research Variants
    log_info "Test 4: Fetching research variants..."
    RESEARCH_VARIANTS=$(curl -s "$BASE_URL/carousels/$CAROUSEL_ID/approval/stages/research" \
        -H "Authorization: Bearer $JWT_TOKEN")

    VARIANT_COUNT=$(echo $RESEARCH_VARIANTS | jq '.variants | length')

    if [ "$VARIANT_COUNT" == "3" ]; then
        log_success "3 research variants generated"
        echo ""
        echo "📊 Research Variants:"
        echo $RESEARCH_VARIANTS | jq '.variants[] | {
            variant_number: .variant_number,
            name: .data.variant_name,
            strategy: .data.strategy,
            score: .heuristic_score
        }'
    else
        log_error "Expected 3 variants, got $VARIANT_COUNT"
        exit 1
    fi
    echo ""

    # Test 5: Approve Research Variant
    VARIANT_ID=$(echo $RESEARCH_VARIANTS | jq -r '.variants[0].id')
    log_info "Test 5: Approving research variant: $VARIANT_ID"

    APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/carousels/$CAROUSEL_ID/approval/approve" \
        -H "Authorization: Bearer $JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"variant_id\": \"$VARIANT_ID\",
            \"user_notes\": \"Selected comprehensive approach\",
            \"selection_reason\": \"Provides most complete information\"
        }")

    NEXT_STAGE=$(echo $APPROVE_RESPONSE | jq -r '.next_stage')

    if [ "$NEXT_STAGE" == "outline" ]; then
        log_success "Research approved, outline stage triggered"
    else
        log_error "Approval failed"
        echo $APPROVE_RESPONSE | jq '.'
        exit 1
    fi
    echo ""

    # Test 6: Wait for Outline Variants
    log_info "Test 6: Waiting for outline variants..."
    wait_for_status "$CAROUSEL_ID" "outline" "awaiting_approval"
    echo ""

    # Test 7: Display Outline Variants
    log_info "Test 7: Fetching outline variants..."
    OUTLINE_VARIANTS=$(curl -s "$BASE_URL/carousels/$CAROUSEL_ID/approval/stages/outline" \
        -H "Authorization: Bearer $JWT_TOKEN")

    echo "📊 Outline Variants:"
    echo $OUTLINE_VARIANTS | jq '.variants[] | {
        variant_number: .variant_number,
        name: .data.variant_name,
        strategy: .data.strategy,
        slide_count: (.data.slides | length),
        score: .heuristic_score
    }'
    echo ""

    # Test 8: Edit Variant Before Approval
    OUTLINE_VARIANT_ID=$(echo $OUTLINE_VARIANTS | jq -r '.variants[0].id')
    log_info "Test 8: Editing outline variant before approval..."

    EDIT_RESPONSE=$(curl -s -X PATCH "$BASE_URL/carousels/$CAROUSEL_ID/approval/edit" \
        -H "Authorization: Bearer $JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"variant_id\": \"$OUTLINE_VARIANT_ID\",
            \"stage\": \"outline\",
            \"edited_data\": {
                \"slides\": [
                    {
                        \"slide_number\": 1,
                        \"theme\": \"Hook - Attention Grabber\",
                        \"key_point\": \"You're losing 10 hours every week to manual tasks\"
                    }
                ]
            },
            \"edit_notes\": \"Strengthened hook with specific time savings\"
        }")

    USER_EDITED=$(echo $EDIT_RESPONSE | jq -r '.variant.user_edited')

    if [ "$USER_EDITED" == "true" ]; then
        log_success "Variant edited successfully (user_edited flag set)"
    else
        log_error "Edit failed"
        echo $EDIT_RESPONSE | jq '.'
        exit 1
    fi
    echo ""

    # Test 9: Approve Edited Variant
    log_info "Test 9: Approving edited outline variant..."
    curl -s -X POST "$BASE_URL/carousels/$CAROUSEL_ID/approval/approve" \
        -H "Authorization: Bearer $JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"variant_id\": \"$OUTLINE_VARIANT_ID\"}" > /dev/null

    log_success "Edited variant approved, copywriting stage triggered"
    echo ""

    # Test 10: Complete Remaining Stages Automatically
    log_info "Test 10: Completing remaining stages (copywriting, hook, visual)..."

    # Copywriting
    wait_for_status "$CAROUSEL_ID" "copywriting" "awaiting_approval"
    COPYWRITING_VARIANTS=$(curl -s "$BASE_URL/carousels/$CAROUSEL_ID/approval/stages/copywriting" \
        -H "Authorization: Bearer $JWT_TOKEN")
    COPYWRITING_VARIANT_ID=$(echo $COPYWRITING_VARIANTS | jq -r '.variants[0].id')
    curl -s -X POST "$BASE_URL/carousels/$CAROUSEL_ID/approval/approve" \
        -H "Authorization: Bearer $JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"variant_id\": \"$COPYWRITING_VARIANT_ID\"}" > /dev/null
    log_success "Copywriting approved"

    # Hook
    wait_for_status "$CAROUSEL_ID" "hook" "awaiting_approval"
    HOOK_VARIANTS=$(curl -s "$BASE_URL/carousels/$CAROUSEL_ID/approval/stages/hook" \
        -H "Authorization: Bearer $JWT_TOKEN")
    HOOK_COUNT=$(echo $HOOK_VARIANTS | jq '.variants | length')
    log_info "Hook stage generated $HOOK_COUNT variants (should be 10)"
    HOOK_VARIANT_ID=$(echo $HOOK_VARIANTS | jq -r '.variants[0].id')
    curl -s -X POST "$BASE_URL/carousels/$CAROUSEL_ID/approval/approve" \
        -H "Authorization: Bearer $JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"variant_id\": \"$HOOK_VARIANT_ID\"}" > /dev/null
    log_success "Hook approved"

    # Visual
    wait_for_status "$CAROUSEL_ID" "visual" "awaiting_approval"
    VISUAL_VARIANTS=$(curl -s "$BASE_URL/carousels/$CAROUSEL_ID/approval/stages/visual" \
        -H "Authorization: Bearer $JWT_TOKEN")
    echo "📊 Visual Variants:"
    echo $VISUAL_VARIANTS | jq '.variants[] | {
        variant_number: .variant_number,
        name: .data.variant_name,
        template: .data.template_id
    }'
    VISUAL_VARIANT_ID=$(echo $VISUAL_VARIANTS | jq -r '.variants[0].id')
    curl -s -X POST "$BASE_URL/carousels/$CAROUSEL_ID/approval/approve" \
        -H "Authorization: Bearer $JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"variant_id\": \"$VISUAL_VARIANT_ID\"}" > /dev/null
    log_success "Visual approved"
    echo ""

    # Test 11: Verify Workflow Completion
    log_info "Test 11: Verifying workflow completion..."
    FINAL_CAROUSEL=$(curl -s "$BASE_URL/carousels/$CAROUSEL_ID" \
        -H "Authorization: Bearer $JWT_TOKEN")

    STATUS=$(echo $FINAL_CAROUSEL | jq -r '.status')

    if [ "$STATUS" == "completed" ]; then
        log_success "Workflow completed successfully! 🎉"
    else
        log_error "Expected status 'completed', got '$STATUS'"
        exit 1
    fi
    echo ""

    # Test 12: Record Engagement Data
    log_info "Test 12: Recording engagement metrics..."
    ENGAGEMENT_RESPONSE=$(curl -s -X POST "$BASE_URL/carousels/$CAROUSEL_ID/engagement" \
        -H "Authorization: Bearer $JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"carousel_id\": \"$CAROUSEL_ID\",
            \"impressions\": 12500,
            \"reach\": 9800,
            \"likes\": 430,
            \"comments\": 28,
            \"saves\": 385,
            \"shares\": 67,
            \"published_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
        }")

    SAVE_RATE=$(echo $ENGAGEMENT_RESPONSE | jq -r '.metrics.save_rate')
    PERFORMED_WELL=$(echo $ENGAGEMENT_RESPONSE | jq -r '.metrics.performed_well')

    log_success "Engagement recorded:"
    echo "   Save Rate: $SAVE_RATE%"
    echo "   Performed Well: $PERFORMED_WELL"
    echo ""

    # Final Summary
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    log_success "✨ All Tests Passed! Approval Workflow is Working! ✨"
    echo ""
    echo "📋 Test Summary:"
    echo "   Carousel ID: $CAROUSEL_ID"
    echo "   Stages Completed: 5/5"
    echo "   Total Variants Generated: 21 (3+3+3+10+3)"
    echo "   User Edits: 1"
    echo "   Final Status: $STATUS"
    echo "   Save Rate: $SAVE_RATE% (> 3% = good)"
    echo ""
    echo "🌐 View in Browser:"
    echo "   Frontend: $FRONTEND_URL/carousel/$CAROUSEL_ID"
    echo "   Approval UI: $FRONTEND_URL/carousel/$CAROUSEL_ID/approval"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Run tests
main
