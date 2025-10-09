"""
Activity Merge Requests API Endpoints

Handles duplicate activity detection and merge request management.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.middleware.auth import get_current_user
from app.services.activity_deduplication_service import ActivityDeduplicationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/merge-requests", tags=["merge-requests"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class MergeRequestResponse(BaseModel):
    """Merge request with activity details."""
    id: str
    primary_activity_id: str
    duplicate_activity_id: str
    confidence_score: int
    status: str
    merge_reason: dict
    created_at: str
    primary: dict  # Primary activity details
    duplicate: dict  # Duplicate activity details


class DetectDuplicatesRequest(BaseModel):
    """Request to detect duplicates for an activity."""
    activity_id: str = Field(..., description="Activity ID to check for duplicates")


class DetectDuplicatesResponse(BaseModel):
    """Response from duplicate detection."""
    success: bool
    duplicates_found: int
    merge_requests_created: int
    auto_merged: int
    message: str


class ApproveRejectResponse(BaseModel):
    """Response from approve/reject action."""
    success: bool
    message: str
    primary_activity_id: str = None
    duplicate_activity_id: str = None


# ============================================================================
# MERGE REQUEST ENDPOINTS
# ============================================================================

@router.get(
    "",
    response_model=List[MergeRequestResponse],
    summary="Get pending merge requests",
    description="""
    Get all pending merge requests for the authenticated user.

    Merge requests are created when:
    - Activities from different sources appear to be duplicates
    - Confidence score is 80-95% (high confidence but needs user confirmation)

    **Returns:**
    - List of pending merge requests ordered by confidence (highest first)
    - Each request includes both activities for comparison
    - Merge reason explains why they're considered duplicates

    **Auto-merged activities (>95% confidence):**
    - Don't appear in pending requests
    - Can be viewed in activity history with `is_duplicate=true`
    """
)
async def get_pending_merge_requests(
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """
    Get pending merge requests for user.

    Args:
        limit: Maximum number of requests to return (default: 10)
        current_user: Authenticated user from JWT

    Returns:
        List of merge requests with activity details
    """
    try:
        service = ActivityDeduplicationService()
        user_id = current_user["user_id"]

        merge_requests = await service.get_pending_merge_requests(
            user_id=user_id,
            limit=limit
        )

        logger.info(f"[MergeRequests] Retrieved {len(merge_requests)} pending for user {user_id}")

        return merge_requests

    except Exception as e:
        logger.error(f"[MergeRequests] Failed to get pending requests: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve merge requests"
        )


@router.post(
    "/detect",
    response_model=DetectDuplicatesResponse,
    summary="Detect duplicates for activity",
    description="""
    Manually trigger duplicate detection for a specific activity.

    **When to use:**
    - After manually logging an activity
    - To check if a new activity is a duplicate
    - When you suspect duplicates exist

    **What happens:**
    1. Scans for activities within ±30 minutes
    2. Compares multiple signals (time, duration, distance, HR, calories)
    3. Calculates confidence score (0-100%)
    4. Auto-merges very high confidence matches (>95%)
    5. Creates merge requests for high confidence matches (80-95%)
    6. Ignores low confidence matches (<80%)

    **Confidence Scoring:**
    - 100: Perfect match (all signals identical)
    - 90-99: Very high (time ±5min, duration/distance ±5%)
    - 80-89: High (time ±15min, duration/distance ±10%)
    - <80: Not duplicates (too different)
    """
)
async def detect_duplicates_for_activity(
    request: DetectDuplicatesRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Detect duplicates for a specific activity.

    Args:
        request: Request with activity_id
        current_user: Authenticated user from JWT

    Returns:
        Detection results with counts
    """
    try:
        service = ActivityDeduplicationService()
        user_id = current_user["user_id"]

        # Detect duplicates
        matches = await service.detect_duplicates_for_activity(
            activity_id=request.activity_id,
            user_id=user_id
        )

        if not matches:
            return DetectDuplicatesResponse(
                success=True,
                duplicates_found=0,
                merge_requests_created=0,
                auto_merged=0,
                message="No duplicates found"
            )

        # Create merge requests
        result = await service.create_merge_requests(
            matches=matches,
            user_id=user_id
        )

        logger.info(
            f"[MergeRequests] Detected {len(matches)} duplicates for activity {request.activity_id}"
        )

        return DetectDuplicatesResponse(
            success=True,
            duplicates_found=len(matches),
            merge_requests_created=result.get("merge_requests_created", 0),
            auto_merged=result.get("auto_merged", 0),
            message=f"Found {len(matches)} potential duplicates"
        )

    except Exception as e:
        logger.error(f"[MergeRequests] Failed to detect duplicates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to detect duplicates"
        )


@router.post(
    "/{merge_request_id}/approve",
    response_model=ApproveRejectResponse,
    summary="Approve merge request",
    description="""
    Approve a merge request and mark duplicate activity as merged.

    **What happens:**
    1. Marks duplicate activity as `is_duplicate=true`
    2. Sets `duplicate_of` to point to primary activity
    3. Updates merge request status to "approved"
    4. Duplicate activity is hidden from activity list (can still be viewed in history)

    **Primary activity:**
    - Kept as the single source of truth
    - Selected based on data completeness and source quality
    - Remains visible in activity feeds

    **Duplicate activity:**
    - Marked as duplicate
    - No longer shows in default activity queries
    - Can be viewed in "Show Duplicates" view
    """
)
async def approve_merge_request(
    merge_request_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Approve a merge request.

    Args:
        merge_request_id: UUID of merge request
        current_user: Authenticated user from JWT

    Returns:
        Success status and activity IDs
    """
    try:
        from app.services.supabase_service import get_service_client
        supabase = get_service_client()
        user_id = current_user["user_id"]

        # Call database function to approve
        result = supabase.rpc(
            "approve_merge_request",
            {
                "p_merge_request_id": merge_request_id,
                "p_user_id": user_id
            }
        ).execute()

        if not result.data or not result.data.get("success"):
            error_msg = result.data.get("error", "Failed to approve merge request") if result.data else "Merge request not found"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        logger.info(f"[MergeRequests] Approved merge request {merge_request_id} for user {user_id}")

        return ApproveRejectResponse(
            success=True,
            message="Merge request approved",
            primary_activity_id=result.data.get("primary_activity_id"),
            duplicate_activity_id=result.data.get("duplicate_activity_id")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[MergeRequests] Failed to approve merge request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve merge request"
        )


@router.post(
    "/{merge_request_id}/reject",
    response_model=ApproveRejectResponse,
    summary="Reject merge request",
    description="""
    Reject a merge request, marking the activities as NOT duplicates.

    **What happens:**
    1. Updates merge request status to "rejected"
    2. Both activities remain in the activity list
    3. System won't suggest this pairing again

    **When to reject:**
    - Activities are actually different workouts
    - You want to keep both activities separate
    - Confidence score was wrong
    """
)
async def reject_merge_request(
    merge_request_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Reject a merge request.

    Args:
        merge_request_id: UUID of merge request
        current_user: Authenticated user from JWT

    Returns:
        Success status
    """
    try:
        from app.services.supabase_service import get_service_client
        supabase = get_service_client()
        user_id = current_user["user_id"]

        # Call database function to reject
        result = supabase.rpc(
            "reject_merge_request",
            {
                "p_merge_request_id": merge_request_id,
                "p_user_id": user_id
            }
        ).execute()

        if not result.data or not result.data.get("success"):
            error_msg = result.data.get("error", "Failed to reject merge request") if result.data else "Merge request not found"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        logger.info(f"[MergeRequests] Rejected merge request {merge_request_id} for user {user_id}")

        return ApproveRejectResponse(
            success=True,
            message="Merge request rejected"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[MergeRequests] Failed to reject merge request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reject merge request"
        )


@router.get(
    "/count",
    summary="Get pending merge requests count",
    description="""
    Get count of pending merge requests for the authenticated user.

    **Use case:**
    - Display notification badge count
    - Check if user has pending merge requests
    - Quick status check without fetching full data
    """
)
async def get_merge_requests_count(
    current_user: dict = Depends(get_current_user)
):
    """
    Get count of pending merge requests.

    Args:
        current_user: Authenticated user from JWT

    Returns:
        Count of pending requests
    """
    try:
        from app.services.supabase_service import get_service_client
        supabase = get_service_client()
        user_id = current_user["user_id"]

        # Call database function
        result = supabase.rpc(
            "get_pending_merge_requests_count",
            {"p_user_id": user_id}
        ).execute()

        count = result.data if result.data is not None else 0

        return {"count": count}

    except Exception as e:
        logger.error(f"[MergeRequests] Failed to get count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get merge requests count"
        )
