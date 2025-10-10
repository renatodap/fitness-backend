#!/usr/bin/env python3
"""
Test the food search API endpoint with proper authentication
"""
import os
import requests
from supabase import create_client
from dotenv import load_dotenv

# Load environment
load_dotenv()

BACKEND_URL = "http://localhost:8000"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Anon key for auth

print("=" * 70)
print("FOOD SEARCH API TEST")
print("=" * 70)

# First check if backend is running
try:
    health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
    print(f"\n✓ Backend health check: {health_response.status_code}")
    print(f"  Response: {health_response.json()}")
except Exception as e:
    print(f"\n✗ Backend not reachable: {e}")
    print("  Make sure backend is running with: uvicorn app.main:app --reload")
    exit(1)

# Test the search endpoint without authentication (should work with service role)
print("\n" + "-" * 70)
print("Testing: Search for 'chicken' (no auth)")
print("-" * 70)

try:
    response = requests.get(
        f"{BACKEND_URL}/api/nutrition/search",
        params={"query": "chicken"},
        timeout=10
    )
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        foods = data.get("foods", [])
        print(f"\n✓ Found {len(foods)} foods:")
        
        for i, food in enumerate(foods[:5], 1):  # Show first 5
            print(f"\n{i}. {food['name']}")
            if food.get('brand_name'):
                print(f"   Brand: {food['brand_name']}")
            print(f"   Calories: {food.get('calories', 0)}")
            print(f"   Is Recent: {food.get('is_recent', False)}")
    else:
        print(f"\n✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n✗ Request failed: {e}")

# Try with user authentication if credentials are available
print("\n" + "-" * 70)
print("Attempting authenticated search (if user creds available)")
print("-" * 70)

try:
    # Try to get user credentials from environment
    test_email = os.getenv("TEST_USER_EMAIL")
    test_password = os.getenv("TEST_USER_PASSWORD")
    
    if test_email and test_password:
        print(f"Authenticating as: {test_email}")
        
        # Create Supabase client and sign in
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        auth_response = supabase.auth.sign_in_with_password({
            "email": test_email,
            "password": test_password
        })
        
        access_token = auth_response.session.access_token
        print(f"✓ Authenticated successfully")
        
        # Test search with token
        response = requests.get(
            f"{BACKEND_URL}/api/nutrition/search",
            params={"query": "chicken"},
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        
        print(f"\nStatus code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            foods = data.get("foods", [])
            recent_count = sum(1 for f in foods if f.get("is_recent"))
            
            print(f"✓ Found {len(foods)} foods ({recent_count} recent)")
            
            if recent_count > 0:
                print("\nRecent foods:")
                for food in [f for f in foods if f.get("is_recent")][:3]:
                    print(f"  - {food['name']}")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    else:
        print("⚠ No test credentials found in environment")
        print("  Set TEST_USER_EMAIL and TEST_USER_PASSWORD to test authenticated search")
        
except Exception as e:
    print(f"✗ Authentication/request failed: {e}")

print("\n" + "=" * 70)
