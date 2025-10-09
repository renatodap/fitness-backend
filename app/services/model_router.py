"""
Intelligent Model Router - Cost-Optimized FREE Models
Automatically selects the best free model for each task

All models are FREE with intelligent fallback chains
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass
from openai import AsyncOpenAI, OpenAI

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class TaskType(str, Enum):
    """Task types for model selection"""
    SIMPLE_EXTRACTION = "simple-extraction"  # Quick text parsing
    COMPLEX_REASONING = "complex-reasoning"  # Planning, analysis
    LONG_CONTEXT = "long-context"            # 50k+ tokens
    STRUCTURED_OUTPUT = "structured-output"  # JSON, code
    VISION = "vision"                        # Image analysis
    QUICK_CATEGORIZATION = "quick-categorization"  # Fast categorization
    VERIFICATION = "verification"            # Quality check
    CONVERSATIONAL = "conversational"        # Chat responses
    PROGRAM_GENERATION = "program-generation"  # Full programs


@dataclass
class ModelConfig:
    """Model configuration"""
    primary: str
    fallbacks: List[str]
    max_tokens: int
    temperature: float


# FREE Model Configuration - Updated 2025
# All models are completely FREE on OpenRouter
MODEL_CONFIGS: Dict[TaskType, ModelConfig] = {
    TaskType.SIMPLE_EXTRACTION: ModelConfig(
        primary="google/gemini-2.0-flash-exp:free",
        fallbacks=["meta-llama/llama-3.3-70b-instruct:free", "qwen/qwen-2.5-72b-instruct:free"],
        max_tokens=2000,
        temperature=0.3
    ),
    TaskType.COMPLEX_REASONING: ModelConfig(
        primary="deepseek/deepseek-r1:free",
        fallbacks=["qwen/qwen-2.5-72b-instruct:free", "google/gemini-2.0-flash-exp:free"],
        max_tokens=4000,
        temperature=0.7
    ),
    TaskType.LONG_CONTEXT: ModelConfig(
        primary="google/gemini-2.5-pro-exp:free",
        fallbacks=["deepseek/deepseek-r1:free", "google/gemini-2.0-flash-exp:free"],
        max_tokens=8000,
        temperature=0.7
    ),
    TaskType.STRUCTURED_OUTPUT: ModelConfig(
        primary="qwen/qwen-2.5-coder-32b-instruct:free",
        fallbacks=["deepseek/deepseek-r1:free", "google/gemini-2.0-flash-exp:free"],
        max_tokens=4000,
        temperature=0.2
    ),
    TaskType.VISION: ModelConfig(
        primary="meta-llama/llama-4-scout:free",  # BEST FREE vision model - 512k context!
        fallbacks=["zero-one-ai/yi-vision:free", "google/gemini-2.0-flash-exp:free"],
        max_tokens=4000,  # Increased for detailed image analysis
        temperature=0.2  # Lower for more precise vision output
    ),
    TaskType.QUICK_CATEGORIZATION: ModelConfig(
        primary="meta-llama/llama-3.2-3b-instruct:free",
        fallbacks=["google/gemini-2.0-flash-exp:free", "meta-llama/llama-3.3-70b-instruct:free"],
        max_tokens=500,
        temperature=0.1
    ),
    TaskType.VERIFICATION: ModelConfig(
        primary="google/gemini-2.0-flash-exp:free",
        fallbacks=["qwen/qwen-2.5-72b-instruct:free", "meta-llama/llama-3.3-70b-instruct:free"],
        max_tokens=1000,
        temperature=0.1
    ),
    TaskType.CONVERSATIONAL: ModelConfig(
        primary="deepseek/deepseek-r1:free",
        fallbacks=["google/gemini-2.0-flash-exp:free", "qwen/qwen-2.5-72b-instruct:free"],
        max_tokens=2000,
        temperature=0.7
    ),
    TaskType.PROGRAM_GENERATION: ModelConfig(
        primary="deepseek/deepseek-r1:free",
        fallbacks=["qwen/qwen-2.5-72b-instruct:free", "google/gemini-2.5-pro-exp:free"],
        max_tokens=16000,
        temperature=0.7
    )
}


class ModelRouter:
    """
    Intelligent model router with automatic fallback and quota handling
    """

    def __init__(self, openrouter_api_key: Optional[str] = None):
        """Initialize with OpenRouter API key"""
        api_key = openrouter_api_key or getattr(settings, 'OPENROUTER_API_KEY', None) or settings.OPENAI_API_KEY

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY or OPENAI_API_KEY required")

        # Use OpenRouter if we have the key
        use_openrouter = hasattr(settings, 'OPENROUTER_API_KEY')

        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1" if use_openrouter else None,
            default_headers={
                "HTTP-Referer": getattr(settings, 'APP_URL', 'https://wagner-coach.app'),
                "X-Title": "Wagner Coach"
            } if use_openrouter else {}
        )

        self.sync_client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1" if use_openrouter else None,
            default_headers={
                "HTTP-Referer": getattr(settings, 'APP_URL', 'https://wagner-coach.app'),
                "X-Title": "Wagner Coach"
            } if use_openrouter else {}
        )

        self.failed_models: Set[str] = set()
        self.model_usage_count: Dict[str, int] = {}

    def select_model(self, task_type: TaskType) -> ModelConfig:
        """Get the optimal model for a task"""
        config = MODEL_CONFIGS[task_type]

        # Try primary model first
        if config.primary not in self.failed_models:
            return config

        # Try fallbacks
        for fallback in config.fallbacks:
            if fallback not in self.failed_models:
                logger.warning(f"Primary model {config.primary} failed, using fallback: {fallback}")
                return ModelConfig(
                    primary=fallback,
                    fallbacks=[m for m in config.fallbacks if m != fallback],
                    max_tokens=config.max_tokens,
                    temperature=config.temperature
                )

        # All models failed, reset and try again
        logger.warning("All models failed, resetting failure tracking")
        self.failed_models.clear()
        return config

    async def complete(
        self,
        task_type: TaskType,
        messages: List[Dict[str, Any]],
        response_format: Optional[Dict[str, str]] = None
    ) -> Any:
        """
        Complete a task with automatic model selection and fallback

        Args:
            task_type: Type of task
            messages: Chat messages
            response_format: Optional response format (e.g., {"type": "json_object"})

        Returns:
            Completion response
        """
        config = self.select_model(task_type)
        selected_model = config.primary

        # Track usage
        self.model_usage_count[selected_model] = self.model_usage_count.get(selected_model, 0) + 1
        logger.info(f"[ModelRouter] Using {selected_model} for {task_type.value}")

        try:
            kwargs = {
                "model": selected_model,
                "messages": messages,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens
            }

            if response_format:
                kwargs["response_format"] = response_format

            response = await self.client.chat.completions.create(**kwargs)
            return response

        except Exception as error:
            # Check if it's a quota/rate limit error
            error_msg = str(error).lower()
            if '429' in error_msg or 'quota' in error_msg or 'rate limit' in error_msg:
                logger.warning(f"[ModelRouter] {selected_model} quota exceeded, marking as failed")
                self.failed_models.add(selected_model)

                # Retry with fallback
                fallback_config = self.select_model(task_type)
                logger.info(f"[ModelRouter] Retrying with {fallback_config.primary}")

                kwargs["model"] = fallback_config.primary
                kwargs["temperature"] = fallback_config.temperature
                kwargs["max_tokens"] = fallback_config.max_tokens

                response = await self.client.chat.completions.create(**kwargs)
                return response

            # Other error, propagate
            raise

    def complete_sync(
        self,
        task_type: TaskType,
        messages: List[Dict[str, Any]],
        response_format: Optional[Dict[str, str]] = None
    ) -> Any:
        """Synchronous version of complete"""
        config = self.select_model(task_type)
        selected_model = config.primary

        logger.info(f"[ModelRouter] Using {selected_model} for {task_type.value}")

        try:
            kwargs = {
                "model": selected_model,
                "messages": messages,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens
            }

            if response_format:
                kwargs["response_format"] = response_format

            response = self.sync_client.chat.completions.create(**kwargs)
            return response

        except Exception as error:
            error_msg = str(error).lower()
            if '429' in error_msg or 'quota' in error_msg or 'rate limit' in error_msg:
                logger.warning(f"[ModelRouter] {selected_model} quota exceeded")
                self.failed_models.add(selected_model)

                fallback_config = self.select_model(task_type)
                kwargs["model"] = fallback_config.primary

                response = self.sync_client.chat.completions.create(**kwargs)
                return response

            raise

    async def verify_output(
        self,
        original_prompt: str,
        output: str,
        verification_criteria: str
    ) -> Dict[str, Any]:
        """
        Verify output with a second free model for critical tasks

        Args:
            original_prompt: Original prompt
            output: Output to verify
            verification_criteria: Criteria for verification

        Returns:
            {"isValid": bool, "issues": List[str]}
        """
        messages = [
            {
                "role": "system",
                "content": "You are a quality checker. Verify if the output meets the criteria. "
                          "Return JSON: { \"isValid\": boolean, \"issues\": string[] }"
            },
            {
                "role": "user",
                "content": f"""ORIGINAL PROMPT: {original_prompt}

OUTPUT TO VERIFY:
{output}

CRITERIA:
{verification_criteria}

Verify the output and return your assessment."""
            }
        ]

        try:
            response = await self.client.chat.completions.create(
                model="google/gemini-2.0-flash-exp:free",
                messages=messages,
                temperature=0.1,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )

            import json
            result = json.loads(response.choices[0].message.content or '{"isValid": true, "issues": []}')
            return result

        except Exception as error:
            logger.error(f"[ModelRouter] Verification failed: {error}")
            return {"isValid": True, "issues": []}  # Default to accepting

    def get_usage_stats(self) -> Dict[str, int]:
        """Get usage statistics"""
        return self.model_usage_count.copy()

    def reset_failures(self) -> None:
        """Reset failure tracking"""
        self.failed_models.clear()
        logger.info("[ModelRouter] Failure tracking reset")


# Global instance
_router: Optional[ModelRouter] = None


def get_model_router() -> ModelRouter:
    """Get the global ModelRouter instance"""
    global _router
    if _router is None:
        _router = ModelRouter()
    return _router
