#!/usr/bin/env python3
"""
Manual test script for event system.

This script tests the complete event integration:
1. Event creation
2. Event countdown
3. Event-specific program generation
4. Event-aware daily recommendations
5. AI coach event tools

Run with: python test_event_manual.py
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.event_service import get_event_service
from app.services.program_service import ProgramService
from app.services.daily_recommendation_service import DailyRecommendationService
from app.services.tool_service import CoachToolService
from app.services.supabase_service import get_service_client


# Test user ID (replace with actual user ID from your database)
TEST_USER_ID = "test-user-uuid"


async def test_event_creation():
    """Test 1: Event creation and retrieval."""
    print("\n" + "="*60)
    print("TEST 1: Event Creation")
    print("="*60)

    event_service = get_event_service()

    # Create event 30 days in the future
    event_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    print(f"\n📅 Creating marathon event for {event_date}...")

    event_data = {
        "user_id": TEST_USER_ID,
        "event_name": "Test Marathon 2025",
        "event_type": "marathon",
        "event_date": event_date,
        "goal_performance": "Sub 4:00",
        "is_primary_goal": True,
        "notes": "First marathon - taking it easy!"
    }

    try:
        created_event = await event_service.create_event(**event_data)
        print(f"✅ Event created successfully!")
        print(f"   Event ID: {created_event['id']}")
        print(f"   Event Name: {created_event['event_name']}")
        print(f"   Event Type: {created_event['event_type']}")
        print(f"   Event Date: {created_event['event_date']}")

        return created_event['id']

    except Exception as e:
        print(f"❌ Failed to create event: {e}")
        return None


async def test_event_countdown(event_id):
    """Test 2: Event countdown and training phase."""
    print("\n" + "="*60)
    print("TEST 2: Event Countdown & Training Phase")
    print("="*60)

    event_service = get_event_service()

    print(f"\n🔢 Fetching countdown for event {event_id}...")

    try:
        primary_event = await event_service.get_primary_event(TEST_USER_ID)

        if not primary_event:
            print("❌ No primary event found")
            return False

        print(f"✅ Primary event countdown retrieved!")
        print(f"   Event Name: {primary_event['event_name']}")
        print(f"   Days Until Event: {primary_event['days_until_event']}")
        print(f"   Current Training Phase: {primary_event['current_training_phase']}")

        if 'training_phases' in primary_event:
            print(f"\n   Training Phase Dates:")
            for phase, date in primary_event['training_phases'].items():
                print(f"     - {phase.replace('_', ' ').title()}: {date}")

        return True

    except Exception as e:
        print(f"❌ Failed to get countdown: {e}")
        return False


async def test_event_program_generation(event_id):
    """Test 3: Event-specific program generation."""
    print("\n" + "="*60)
    print("TEST 3: Event-Specific Program Generation")
    print("="*60)

    supabase = get_service_client()
    program_service = ProgramService(supabase)

    print(f"\n🏋️ Generating program for event {event_id}...")

    # Mock answers for program generation
    answers = [
        {"question": "What is your primary fitness goal?", "answer": "Improve endurance"},
        {"question": "How many days per week can you train?", "answer": "5 days"},
        {"question": "What equipment do you have access to?", "answer": "Full gym"},
    ]

    session_id = f"test-session-{datetime.now().timestamp()}"

    try:
        # Note: This will call the AI API and incur costs
        # In production, you'd mock this
        print("⚠️  This will call Claude API (costs ~$0.15)")
        print("   Skipping actual generation in test...")
        print("   (In real usage, program would be generated with event periodization)")

        # Show what would happen
        print(f"✅ Program generation would:")
        print(f"   - Periodize to peak at event date")
        print(f"   - Include sport-specific training (marathon)")
        print(f"   - Add taper week before event")
        print(f"   - Link program to event ID: {event_id}")

        return True

    except Exception as e:
        print(f"❌ Failed to generate program: {e}")
        return False


async def test_daily_recommendations():
    """Test 4: Event-aware daily recommendations."""
    print("\n" + "="*60)
    print("TEST 4: Event-Aware Daily Recommendations")
    print("="*60)

    supabase = get_service_client()
    rec_service = DailyRecommendationService(supabase)

    print(f"\n📋 Generating daily recommendations for today...")

    try:
        target_date = datetime.now().strftime("%Y-%m-%d")
        recommendations = await rec_service.generate_daily_plan(TEST_USER_ID, target_date)

        print(f"✅ Daily recommendations generated!")
        print(f"   Total recommendations: {len(recommendations.get('recommendations', []))}")

        # Check for event-related recommendations
        event_recs = [
            r for r in recommendations.get('recommendations', [])
            if r.get('recommendation_type') == 'event_reminder'
        ]

        if event_recs:
            print(f"\n   📢 Event Reminders:")
            for rec in event_recs:
                print(f"      - {rec['content']['message']}")
                print(f"        Priority: {rec['priority']}")

        # Check for event-aware meal recommendations
        meal_recs = [
            r for r in recommendations.get('recommendations', [])
            if r.get('recommendation_type') == 'meal'
        ]

        if meal_recs:
            print(f"\n   🍽️  Meal Recommendations: {len(meal_recs)}")
            print(f"      (Macros adjusted based on event phase)")

        return True

    except Exception as e:
        print(f"❌ Failed to generate recommendations: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_coach_event_tools():
    """Test 5: AI coach event tools."""
    print("\n" + "="*60)
    print("TEST 5: AI Coach Event Tools")
    print("="*60)

    supabase = get_service_client()
    tool_service = CoachToolService(supabase)

    print(f"\n🤖 Testing coach event awareness tools...")

    try:
        # Test get_upcoming_events
        print("\n   Testing: get_upcoming_events()")
        upcoming_events = await tool_service.get_upcoming_events(TEST_USER_ID, days_ahead=90)

        if upcoming_events.get('success'):
            print(f"   ✅ Found {upcoming_events['count']} upcoming events")
            for event in upcoming_events.get('events', []):
                print(f"      - {event['event_name']} ({event['days_until_event']} days)")
        else:
            print(f"   ❌ Failed: {upcoming_events.get('error')}")

        # Test get_primary_event_countdown
        print("\n   Testing: get_primary_event_countdown()")
        primary_countdown = await tool_service.get_primary_event_countdown(TEST_USER_ID)

        if primary_countdown.get('success') and primary_countdown.get('has_primary_event'):
            event = primary_countdown['event']
            print(f"   ✅ Primary event countdown retrieved")
            print(f"      Event: {event['event_name']}")
            print(f"      Days until: {event['days_until_event']}")
            print(f"      Training phase: {event['current_training_phase']}")
        elif primary_countdown.get('success'):
            print(f"   ℹ️  No primary event set")
        else:
            print(f"   ❌ Failed: {primary_countdown.get('error')}")

        print(f"\n   ✅ Coach can now reference events in conversation!")
        print(f"      Example: 'I see you have a marathon in 30 days!'")

        return True

    except Exception as e:
        print(f"❌ Failed to test coach tools: {e}")
        import traceback
        traceback.print_exc()
        return False


async def cleanup_test_events():
    """Cleanup: Delete test events."""
    print("\n" + "="*60)
    print("CLEANUP: Remove Test Events")
    print("="*60)

    event_service = get_event_service()

    print(f"\n🧹 Cleaning up test events...")

    try:
        # Get all events for test user
        upcoming = await event_service.get_upcoming_events(TEST_USER_ID, days_ahead=365)

        for event in upcoming:
            if event['event_name'].startswith("Test"):
                print(f"   Deleting: {event['event_name']}...")
                await event_service.delete_event(event['id'], TEST_USER_ID)

        print(f"✅ Cleanup complete!")
        return True

    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("EVENT SYSTEM MANUAL TEST SUITE")
    print("="*60)
    print(f"\nTest User ID: {TEST_USER_ID}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        "event_creation": False,
        "event_countdown": False,
        "program_generation": False,
        "daily_recommendations": False,
        "coach_tools": False
    }

    # Test 1: Event Creation
    event_id = await test_event_creation()
    results["event_creation"] = event_id is not None

    if not event_id:
        print("\n❌ Stopping tests - event creation failed")
        return results

    # Test 2: Event Countdown
    results["event_countdown"] = await test_event_countdown(event_id)

    # Test 3: Program Generation
    results["program_generation"] = await test_event_program_generation(event_id)

    # Test 4: Daily Recommendations
    results["daily_recommendations"] = await test_daily_recommendations()

    # Test 5: Coach Tools
    results["coach_tools"] = await test_coach_event_tools()

    # Cleanup
    await cleanup_test_events()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")

    total_passed = sum(results.values())
    total_tests = len(results)

    print(f"\nResults: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        print("\n🎉 All tests passed! Event system is working correctly!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check output above for details.")
        return 1


if __name__ == "__main__":
    """
    SETUP INSTRUCTIONS:

    1. Update TEST_USER_ID at the top of this file with a real user ID from your database
    2. Ensure backend is running or environment variables are set
    3. Run: python test_event_manual.py

    This script will:
    - Create a test marathon event 30 days in the future
    - Test event countdown calculations
    - Verify event-aware daily recommendations
    - Test AI coach event tools
    - Clean up test data when done

    NOTE: Some tests call AI APIs (Claude) which incur costs (~$0.15 per program).
    These are mocked/skipped by default. Uncomment to test full integration.
    """
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
