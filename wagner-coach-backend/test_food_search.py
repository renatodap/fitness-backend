#!/usr/bin/env python3
"""
Quick test script to verify food search is working locally
"""
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_USER_ID = "8f2f3472-b1cc-4e67-9b8d-9c24ccae5d45"

# Create a JWT token for testing
def create_test_token():
    """Create a test JWT token"""
    from jose import jwt
    from datetime import datetime, timedelta
    
    secret = os.getenv("JWT_SECRET")
    payload = {
        "user_id": TEST_USER_ID,
        "id": TEST_USER_ID,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def test_health():
    """Test health endpoint"""
    print("\n🏥 Testing /health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_food_search(query="chicken"):
    """Test food search endpoint"""
    print(f"\n🔍 Testing /api/v1/foods/search?q={query}...")
    
    try:
        token = create_test_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{BASE_URL}/api/v1/foods/search",
            params={"q": query, "limit": 5},
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {data['total']} foods")
            print(f"   Foods returned: {len(data['foods'])}")
            
            if data['foods']:
                print("\n   Sample results:")
                for food in data['foods'][:3]:
                    print(f"   - {food['name']} ({food.get('calories', 0)} cal)")
            else:
                print("   ⚠️  No foods returned (empty results)")
            
            return data['total'] > 0
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_recent_foods():
    """Test recent foods endpoint"""
    print(f"\n🕐 Testing /api/v1/foods/recent...")
    
    try:
        token = create_test_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{BASE_URL}/api/v1/foods/recent",
            params={"limit": 10},
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {len(data['foods'])} recent foods")
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_database_direct():
    """Test direct database query"""
    print(f"\n💾 Testing direct database query...")
    
    try:
        from app.services.supabase_service import get_service_client
        
        supabase = get_service_client()
        
        # Query foods table directly
        response = supabase.table("foods").select("id, name, calories").limit(5).execute()
        
        if response.data:
            print(f"   ✅ Database connection working")
            print(f"   Found {len(response.data)} foods in database")
            print("\n   Sample foods from DB:")
            for food in response.data[:3]:
                print(f"   - {food['name']} ({food.get('calories', 0)} cal)")
            return True
        else:
            print(f"   ⚠️  No foods in database")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 WAGNER COACH BACKEND - LOCAL TEST SUITE")
    print("=" * 60)
    
    results = {}
    
    # Run tests
    results['health'] = test_health()
    results['database'] = test_database_direct()
    results['food_search_chicken'] = test_food_search("chicken")
    results['food_search_banana'] = test_food_search("banana")
    results['recent_foods'] = test_recent_foods()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Food search is working!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check output above.")
        sys.exit(1)
