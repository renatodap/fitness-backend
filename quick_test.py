import requests
import json
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Get credentials
test_email = os.getenv("TEST_USER_EMAIL", "daprado@syr.edu")  # Default test email
test_password = os.getenv("TEST_USER_PASSWORD")

if not test_password:
    print("❌ TEST_USER_PASSWORD not set in .env")
    print("\nTo test with authentication, add:")
    print("TEST_USER_EMAIL=your-email@example.com")
    print("TEST_USER_PASSWORD=your-password")
    print("\nTesting without auth will fail...")
    exit(1)

# Authenticate with Supabase
print(f"Authenticating as: {test_email}")
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
try:
    auth_response = supabase.auth.sign_in_with_password({
        "email": test_email,
        "password": test_password
    })
    token = auth_response.session.access_token
    print(f"✅ Authenticated successfully\n")
except Exception as e:
    print(f"❌ Authentication failed: {e}")
    exit(1)

# Test food search endpoint
print("=" * 60)
print("Testing: /api/v1/foods/search?q=chicken")
print("=" * 60)

r = requests.get(
    'http://localhost:8000/api/v1/foods/search',
    params={'q': 'chicken'},
    headers={'Authorization': f'Bearer {token}'},
    timeout=10
)

print(f'Status: {r.status_code}\n')

if r.status_code == 200:
    data = r.json()
    foods = data.get('foods', [])
    print(f'✅ Found {len(foods)} foods\n')
    print('First 5 results:')
    for i, food in enumerate(foods[:5], 1):
        recent = "🕐" if food.get('is_recent') else ""
        template = "📋" if food.get('is_template') else ""
        print(f'{i}. {recent}{template} {food["name"]}')
        if food.get('brand_name'):
            print(f'   Brand: {food["brand_name"]}')
        print(f'   Calories: {food.get("calories", 0)} | Protein: {food.get("protein_g", 0)}g')
        print()
else:
    print(f'❌ Error: {r.status_code}')
    print(f'Response: {r.text}')

print("=" * 60)
