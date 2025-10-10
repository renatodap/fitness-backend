#!/usr/bin/env python3
"""Test API calls exactly like the frontend would make them"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# IMPORTANT: Replace with your actual test user credentials
test_email = 'renato@sharpened.me'
test_password = input('Enter password for renato@sharpened.me: ')

print('\n' + '='*60)
print('🧪 TESTING BACKEND API (LIKE FRONTEND)')
print('='*60)

print('\n🔐 Step 1: Getting auth token from Supabase...')
# Sign in to get JWT token (exactly like frontend does)
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
    exit(1)

auth_data = auth_response.json()
token = auth_data['access_token']
user_id = auth_data['user']['id']

print(f'✅ Got auth token for user: {user_id}')
print(f'Token (first 30 chars): {token[:30]}...')

# Test 1: Food search
print('\n' + '='*60)
print('🔍 TEST 1: Food Search (q=chicken)')
print('='*60)
search_response = requests.get(
    'http://localhost:8000/api/v1/foods/search',
    params={
        'q': 'chicken',
        'limit': 5,
        'include_recent': 'true',
        'include_templates': 'true'
    },
    headers={'Authorization': f'Bearer {token}'}
)

print(f'Status: {search_response.status_code}')

if search_response.status_code == 200:
    data = search_response.json()
    print(f'✅ SUCCESS! Found {data["total"]} foods')
    print(f'\nResults:')
    for i, food in enumerate(data['foods'][:5], 1):
        print(f'{i}. {food["name"]}')
        print(f'   Calories: {food.get("calories", 0)}, Protein: {food.get("protein_g", 0)}g')
else:
    print(f'❌ FAILED')
    print(f'Response: {search_response.text}')

# Test 2: Recent foods
print('\n' + '='*60)
print('🕐 TEST 2: Recent Foods')
print('='*60)
recent_response = requests.get(
    'http://localhost:8000/api/v1/foods/recent',
    params={'limit': 10},
    headers={'Authorization': f'Bearer {token}'}
)

print(f'Status: {recent_response.status_code}')
if recent_response.status_code == 200:
    data = recent_response.json()
    print(f'✅ Found {len(data["foods"])} recent foods')
    if data["foods"]:
        for i, food in enumerate(data["foods"][:5], 1):
            print(f'{i}. {food["name"]}')
    else:
        print('(No recent foods - user hasn\'t logged any meals yet)')
else:
    print(f'❌ FAILED')
    print(f'Response: {recent_response.text}')

# Test 3: Nutrition summary
print('\n' + '='*60)
print('📊 TEST 3: Nutrition Summary (Today)')
print('='*60)
summary_response = requests.get(
    'http://localhost:8000/api/v1/nutrition/summary/today',
    headers={'Authorization': f'Bearer {token}'}
)

print(f'Status: {summary_response.status_code}')
if summary_response.status_code == 200:
    data = summary_response.json()
    print(f'✅ SUCCESS')
    print(f'Consumed: {data["consumed"]["calories"]} cal, {data["consumed"]["protein"]}g protein')
    print(f'Target: {data["target"]["calories"]} cal, {data["target"]["protein"]}g protein')
else:
    print(f'❌ FAILED')
    print(f'Response: {summary_response.text}')

print('\n' + '='*60)
print('✅ ALL TESTS COMPLETE')
print('='*60)
