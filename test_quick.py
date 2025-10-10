import os, sys, requests
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta

load_dotenv()

def test():
    # Create token
    secret = os.getenv('JWT_SECRET')
    token = jwt.encode({'user_id': '8f2f3472-b1cc-4e67-9b8d-9c24ccae5d45', 'id': '8f2f3472-b1cc-4e67-9b8d-9c24ccae5d45', 'exp': datetime.utcnow() + timedelta(hours=1)}, secret, algorithm='HS256')
    
    # Test database
    from app.services.supabase_service import get_service_client
    supabase = get_service_client()
    resp = supabase.table('foods').select('id, name, calories').limit(3).execute()
    print('\n💾 DATABASE TEST:')
    print(f'   Foods in DB: {len(resp.data) if resp.data else 0}')
    if resp.data:
        for f in resp.data: print(f'   - {f["name"]}')
    
    # Test API
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get('http://localhost:8000/api/v1/foods/search', params={'q': 'chicken', 'limit': 5}, headers=headers)
    print(f'\n🔍 API SEARCH TEST (chicken):')
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'   Found: {data["total"]} foods')
        if data['foods']:
            for f in data['foods'][:3]: print(f'   - {f["name"]}')
    else:
        print(f'   Error: {r.text}')

test()
