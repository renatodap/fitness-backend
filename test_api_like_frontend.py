import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Test user credentials (you'll need to use actual credentials)
test_email = 'renato@sharpened.me'  # Replace with actual test user
test_password = 'your-password'  # Replace with actual password

print('🔐 Step 1: Getting auth token from Supabase...')
# Sign in to get JWT token
auth_response = requests.post(
    f'{SUPABASE_URL}/auth/v1/token?grant_type=password',
    headers={
        'apikey': SUPABASE_KEY,
        'Content-Type': 'application/json'
    },
    json={
        'email': test_email,
        'password': test_password
    }
)

if auth_response.status_code != 200:
    print(f'❌ Auth failed: {auth_response.status_code}')
    print(f'Response: {auth_response.text}')
    print('\n💡 TIP: Update test_email and test_password in the script with your actual credentials')
    exit(1)

auth_data = auth_response.json()
token = auth_data['access_token']
user_id = auth_data['user']['id']

print(f'✅ Got auth token for user: {user_id}')
print(f'Token (first 20 chars): {token[:20]}...')

# Now test food search with this token
print('\n🔍 Step 2: Testing food search API...')
search_response = requests.get(
    'http://localhost:8000/api/v1/foods/search',
    params={'q': 'chicken', 'limit': 5, 'include_recent': 'true', 'include_templates': 'true'},
    headers={'Authorization': f'Bearer {token}'}
)

print(f'Status: {search_response.status_code}')

if search_response.status_code == 200:
    data = search_response.json()
    print(f'✅ SUCCESS! Found {data[\"total\"]} foods')
    print(f'\nResults:')
    for food in data['foods'][:5]:
        print(f'  - {food[\"name\"]} ({food.get(\"calories\", 0)} cal, {food.get(\"protein_g\", 0)}g protein)')
else:
    print(f'❌ FAILED: {search_response.text}')

# Test recent foods
print('\n🕐 Step 3: Testing recent foods API...')
recent_response = requests.get(
    'http://localhost:8000/api/v1/foods/recent',
    params={'limit': 10},
    headers={'Authorization': f'Bearer {token}'}
)

print(f'Status: {recent_response.status_code}')
if recent_response.status_code == 200:
    data = recent_response.json()
    print(f'✅ Found {len(data[\"foods\"])} recent foods')
else:
    print(f'❌ FAILED: {recent_response.text}')
