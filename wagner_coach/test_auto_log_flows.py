"""
Test script for auto-log preference flows.

Tests both modes:
1. auto_log_enabled=FALSE (default): Returns pending_logs for user review
2. auto_log_enabled=TRUE: Saves immediately and returns auto_logged

Usage:
    python test_auto_log_flows.py
"""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv("wagner-coach-backend/.env")

# Import services
import sys
sys.path.insert(0, "wagner-coach-backend")

from app.services.unified_coach_service import UnifiedCoachService
from app.services.tool_service import ToolService
from supabase import create_client, Client
from anthropic import AsyncAnthropic

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Test user ID (replace with actual test user)
TEST_USER_ID = "YOUR_TEST_USER_ID"  # TODO: Replace with actual test user


async def setup_services():
    """Initialize services for testing."""
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    anthropic = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    tool_service = ToolService(supabase)
    coach_service = UnifiedCoachService(supabase, anthropic, tool_service)

    return supabase, coach_service


async def set_auto_log_preference(supabase: Client, user_id: str, enabled: bool):
    """Set user's auto_log_enabled preference."""
    print(f"\n{'='*60}")
    print(f"Setting auto_log_enabled={enabled} for user {user_id[:8]}...")

    result = await supabase.table("profiles").update({
        "auto_log_enabled": enabled
    }).eq("user_id", user_id).execute()

    print(f"✓ Preference updated: auto_log_enabled={enabled}")
    return result


async def test_preview_mode(coach_service: UnifiedCoachService, user_id: str):
    """Test auto_log=FALSE (preview mode)."""
    print(f"\n{'='*60}")
    print("TEST 1: PREVIEW MODE (auto_log_enabled=FALSE)")
    print(f"{'='*60}")

    message = "for breakfast i had scrambled eggs and toast, then i did a 5k run, then i ate grilled chicken and rice for lunch"
    print(f"\nSending message: {message}")

    response = await coach_service.process_message(
        user_id=user_id,
        message=message,
        mode="chat"
    )

    print(f"\n--- RESPONSE ---")
    print(f"Success: {response.get('success')}")
    print(f"Message: {response.get('message')[:200]}...")
    print(f"Tools used: {response.get('tools_used', [])}")

    # Check pending_logs
    pending_logs = response.get("pending_logs", [])
    print(f"\n--- PENDING LOGS (should be 3) ---")
    print(f"Count: {len(pending_logs)}")
    for i, log in enumerate(pending_logs, 1):
        print(f"\n  {i}. {log.get('log_type')}")
        print(f"     Message: {log.get('message')}")
        data = log.get('data', {})
        if 'meal_type' in data:
            print(f"     Meal: {data.get('meal_type')} - {data.get('foods')}")
        elif 'activity_type' in data:
            print(f"     Activity: {data.get('activity_type')} - {data.get('distance_km')}km")

    # Check auto_logged (should be empty)
    auto_logged = response.get("auto_logged", [])
    print(f"\n--- AUTO LOGGED (should be 0) ---")
    print(f"Count: {len(auto_logged)}")

    # Assertions
    assert len(pending_logs) == 3, f"Expected 3 pending logs, got {len(pending_logs)}"
    assert len(auto_logged) == 0, f"Expected 0 auto-logged, got {len(auto_logged)}"

    log_types = [log.get('log_type') for log in pending_logs]
    assert 'meal' in log_types, "Expected meal log in pending_logs"
    assert 'activity' in log_types, "Expected activity log in pending_logs"

    print(f"\n✓ PREVIEW MODE TEST PASSED")
    return response


async def test_auto_save_mode(coach_service: UnifiedCoachService, user_id: str):
    """Test auto_log=TRUE (auto-save mode)."""
    print(f"\n{'='*60}")
    print("TEST 2: AUTO-SAVE MODE (auto_log_enabled=TRUE)")
    print(f"{'='*60}")

    message = "for breakfast i had oatmeal and berries, then i did a 30min bike ride, then i ate salmon and veggies for dinner"
    print(f"\nSending message: {message}")

    response = await coach_service.process_message(
        user_id=user_id,
        message=message,
        mode="chat"
    )

    print(f"\n--- RESPONSE ---")
    print(f"Success: {response.get('success')}")
    print(f"Message: {response.get('message')[:200]}...")
    print(f"Tools used: {response.get('tools_used', [])}")

    # Check pending_logs (should be empty)
    pending_logs = response.get("pending_logs", [])
    print(f"\n--- PENDING LOGS (should be 0) ---")
    print(f"Count: {len(pending_logs)}")

    # Check auto_logged (should have 3 items)
    auto_logged = response.get("auto_logged", [])
    print(f"\n--- AUTO LOGGED (should be 3) ---")
    print(f"Count: {len(auto_logged)}")
    for i, log in enumerate(auto_logged, 1):
        print(f"\n  {i}. {log.get('log_type')}")
        print(f"     ID: {log.get('id')}")
        print(f"     Message: {log.get('message')}")

    # Assertions
    assert len(auto_logged) == 3, f"Expected 3 auto-logged items, got {len(auto_logged)}"
    assert len(pending_logs) == 0, f"Expected 0 pending logs, got {len(pending_logs)}"

    log_types = [log.get('log_type') for log in auto_logged]
    assert 'meal' in log_types, "Expected meal log in auto_logged"
    assert 'activity' in log_types, "Expected activity log in auto_logged"

    print(f"\n✓ AUTO-SAVE MODE TEST PASSED")
    return response


async def main():
    """Run all tests."""
    print(f"\n{'='*60}")
    print("AUTO-LOG PREFERENCE TESTING")
    print(f"{'='*60}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Check test user ID
    if TEST_USER_ID == "YOUR_TEST_USER_ID":
        print("\n❌ ERROR: Please set TEST_USER_ID in the script")
        print("You can get a user ID from the profiles table in Supabase")
        return

    # Setup
    supabase, coach_service = await setup_services()

    try:
        # Test 1: Preview mode (auto_log=FALSE)
        await set_auto_log_preference(supabase, TEST_USER_ID, False)
        await test_preview_mode(coach_service, TEST_USER_ID)

        # Wait a bit between tests
        await asyncio.sleep(2)

        # Test 2: Auto-save mode (auto_log=TRUE)
        await set_auto_log_preference(supabase, TEST_USER_ID, True)
        await test_auto_save_mode(coach_service, TEST_USER_ID)

        print(f"\n{'='*60}")
        print("✓ ALL TESTS PASSED")
        print(f"{'='*60}")

    except AssertionError as e:
        print(f"\n{'='*60}")
        print(f"❌ TEST FAILED: {e}")
        print(f"{'='*60}")
        raise

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ ERROR: {e}")
        print(f"{'='*60}")
        raise

    finally:
        # Reset to default (auto_log=FALSE)
        await set_auto_log_preference(supabase, TEST_USER_ID, False)
        print(f"\n✓ Reset auto_log_enabled to FALSE (default)")


if __name__ == "__main__":
    asyncio.run(main())
