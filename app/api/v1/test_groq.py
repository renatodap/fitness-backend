"""
Test endpoint to verify Groq API is working
"""

from fastapi import APIRouter, HTTPException
import logging
from openai import OpenAI
from app.config import get_settings

router = APIRouter(prefix="/test", tags=["test"])
logger = logging.getLogger(__name__)
settings = get_settings()


@router.get("/groq-status")
async def test_groq():
    """
    Test if Groq API is accessible and working.

    Returns:
        - api_key_set: Whether GROQ_API_KEY environment variable is set
        - api_key_preview: First 10 chars of the key
        - api_test: Result of a simple API call
    """
    # Check if API key is set
    if not settings.GROQ_API_KEY:
        return {
            "status": "error",
            "api_key_set": False,
            "error": "GROQ_API_KEY environment variable is not set"
        }

    # Try a simple API call
    try:
        client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            timeout=10.0
        )

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Say 'hello' in JSON format: {\"message\": \"hello\"}"}
            ],
            response_format={"type": "json_object"},
            max_tokens=50
        )

        result = response.choices[0].message.content

        return {
            "status": "success",
            "api_key_set": True,
            "api_key_preview": settings.GROQ_API_KEY[:10] + "...",
            "api_test": "passed",
            "test_response": result,
            "message": "✅ Groq API is working correctly"
        }

    except Exception as e:
        logger.error(f"Groq API test failed: {e}")
        return {
            "status": "error",
            "api_key_set": True,
            "api_key_preview": settings.GROQ_API_KEY[:10] + "...",
            "api_test": "failed",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "message": f"❌ Groq API error: {type(e).__name__}"
        }
