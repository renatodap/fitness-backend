#!/usr/bin/env python3
"""
Quick verification script to check if backend is ready to deploy.
Run: poetry run python verify_setup.py
"""

import sys
from pathlib import Path

def check_imports():
    """Test if all modules can be imported."""
    print("Checking imports...")
    try:
        from app.main import app
        print("  SUCCESS: app.main imports")

        from app.config import get_settings
        print("  SUCCESS: app.config imports")

        from app.services.supabase_service import get_supabase_service
        print("  SUCCESS: supabase_service imports")

        from app.services.summarization_service import SummarizationService
        print("  SUCCESS: summarization_service imports")

        from app.services.embedding_service import EmbeddingService
        print("  SUCCESS: embedding_service imports")

        from app.services.rag_service import RAGService
        print("  SUCCESS: rag_service imports")

        from app.services.meal_parser_service import MealParserService
        print("  SUCCESS: meal_parser_service imports")

        from app.services.garmin_service import GarminService
        print("  SUCCESS: garmin_service imports")

        from app.workers.celery_app import celery_app
        print("  SUCCESS: celery_app imports")

        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        return False

def check_env_file():
    """Check if .env file exists."""
    print("\nChecking environment file...")
    env_file = Path(".env")
    if env_file.exists():
        print("  SUCCESS: .env file exists")

        # Check for required variables
        content = env_file.read_text()
        required = [
            "SUPABASE_URL",
            "SUPABASE_KEY",
            "OPENAI_API_KEY",
            "JWT_SECRET",
        ]

        missing = []
        for var in required:
            if var not in content:
                missing.append(var)

        if missing:
            print(f"  WARNING: Missing variables: {', '.join(missing)}")
            return False
        else:
            print("  SUCCESS: All required variables present")
            return True
    else:
        print("  FAILED: .env file not found")
        print("  ACTION: Copy .env.example to .env and add your API keys")
        return False

def check_docker_files():
    """Check if Docker configuration exists."""
    print("\nChecking Docker configuration...")
    dockerfile = Path("Dockerfile")
    compose = Path("docker-compose.yml")

    success = True
    if dockerfile.exists():
        print("  SUCCESS: Dockerfile exists")
    else:
        print("  FAILED: Dockerfile not found")
        success = False

    if compose.exists():
        print("  SUCCESS: docker-compose.yml exists")
    else:
        print("  FAILED: docker-compose.yml not found")
        success = False

    return success

def check_tests():
    """Check if test files exist."""
    print("\nChecking test files...")
    tests_dir = Path("tests/unit")

    if not tests_dir.exists():
        print("  FAILED: tests/unit directory not found")
        return False

    test_files = list(tests_dir.glob("test_*.py"))
    if len(test_files) >= 10:
        print(f"  SUCCESS: {len(test_files)} test files found")
        return True
    else:
        print(f"  WARNING: Only {len(test_files)} test files found (expected 10+)")
        return False

def check_config():
    """Check if configuration loads correctly."""
    print("\nChecking configuration...")
    try:
        from app.config import get_settings
        settings = get_settings()

        print(f"  App Name: {settings.APP_NAME}")
        print(f"  Environment: {settings.ENVIRONMENT}")
        print(f"  Debug: {settings.DEBUG}")
        print(f"  CORS Origins: {settings.CORS_ORIGINS}")
        print("  SUCCESS: Configuration loads correctly")
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("BACKEND VERIFICATION")
    print("=" * 60)

    checks = [
        ("Imports", check_imports()),
        ("Environment File", check_env_file()),
        ("Docker Configuration", check_docker_files()),
        ("Test Files", check_tests()),
        ("Configuration", check_config()),
    ]

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    for name, passed in checks:
        status = "PASS" if passed else "FAIL"
        symbol = "SUCCESS" if passed else "FAILED"
        print(f"{symbol}: {name}")

    all_passed = all(passed for _, passed in checks)

    print("\n" + "=" * 60)
    if all_passed:
        print("SUCCESS: Backend is ready to deploy!")
        print("\nNext steps:")
        print("1. Review ACTION_PLAN.md for deployment instructions")
        print("2. Start local server: poetry run uvicorn app.main:app --reload")
        print("3. Deploy with Docker: docker-compose up")
        print("=" * 60)
        return 0
    else:
        print("FAILED: Backend needs fixes before deployment")
        print("\nPlease address the issues above, then run this script again.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())