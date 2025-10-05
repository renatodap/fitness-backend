"""
Pytest configuration and fixtures for backend tests
Sets up test environment variables before any imports
"""

import os
import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent.parent
sys.path.insert(0, str(app_dir))

# Set required environment variables for testing
# These are dummy values - tests should mock API calls
os.environ.setdefault('SUPABASE_URL', 'https://test.supabase.co')
os.environ.setdefault('SUPABASE_KEY', 'test-key-' + 'x' * 100)
os.environ.setdefault('SUPABASE_SERVICE_KEY', 'test-service-key-' + 'x' * 100)
os.environ.setdefault('OPENAI_API_KEY', 'sk-test-' + 'x' * 40)
os.environ.setdefault('GROQ_API_KEY', 'gsk_test_' + 'x' * 50)
os.environ.setdefault('JWT_SECRET', 'test-jwt-secret-' + 'x' * 32)
os.environ.setdefault('CRON_SECRET', 'test-cron-secret')
os.environ.setdefault('WEBHOOK_SECRET', 'test-webhook-secret')
os.environ.setdefault('ENVIRONMENT', 'test')
os.environ.setdefault('DEBUG', 'true')
os.environ.setdefault('ALLOWED_ORIGINS', 'http://localhost:3000')
