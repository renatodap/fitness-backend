import requests
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Get auth token
password = input("Enter password for renato@sharpened.me: ")
auth_response = requests.post(
    f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
    headers={"apikey": SUPABASE_KEY, "Content-Type": "application/json"},
    json={"email": "renato@sharpened.me", "password": password}
)

if auth_response.status_code == 200:
    token = auth_response.json()["access_token"]
    print(f"✅ Auth successful, token: {token[:30]}...")
    
    # Test food search
    response = requests.get(
        "http://localhost:8000/api/v1/foods/search",
        params={"q": "chicken", "limit": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"\n🔍 Food Search Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total']} foods:")
        for f in data['foods'][:5]:
            print(f"  - {f['name']} ({f.get('calories',0)} cal)")
    else:
        print(f"❌ Error: {response.text}")
else:
    print(f"❌ Auth failed: {auth_response.text}")
