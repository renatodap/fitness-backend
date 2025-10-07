"""
DUAL-API MODEL ROUTER - Groq + OpenRouter
Python Backend Implementation

STRATEGY:
- Groq: BLAZING FAST real-time tasks (coaching, streaming, quick responses)
- OpenRouter: Complex reasoning, vision, fallback, multimodal

FALLBACK CHAIN: Groq → OpenRouter → Specific Provider

100% FREE models with automatic failover
"""

import os
from enum import Enum
from typing import Optional, Dict, Any, List, AsyncIterator
from openai import AsyncOpenAI
from pydantic import BaseModel


class TaskType(str, Enum):
    """Task types for intelligent routing"""
    REAL_TIME_CHAT = "real-time-chat"          # GROQ: Sub-second coaching responses
    QUICK_CATEGORIZATION = "quick-categorization"  # GROQ: Instant classification
    COMPLEX_REASONING = "complex-reasoning"     # OPENROUTER: DeepSeek R1, planning
    LONG_CONTEXT = "long-context"              # OPENROUTER: Gemini 2.5 Pro, 1M tokens
    STRUCTURED_OUTPUT = "structured-output"     # GROQ (fast) or OPENROUTER (accurate)
    VISION = "vision"                          # OPENROUTER: Llama-4 Scout, Yi-Vision
    PROGRAM_GENERATION = "program-generation"   # OPENROUTER: Complex multi-step
    STREAMING_FEEDBACK = "streaming-feedback"   # GROQ: Live workout feedback
    VERIFICATION = "verification"              # OPENROUTER: Quality checks


class TaskConfig(BaseModel):
    """Configuration for a specific task"""
    type: TaskType
    context_tokens: Optional[int] = None
    requires_json: bool = False
    requires_vision: bool = False
    prioritize_speed: bool = False      # If true, prefer Groq
    prioritize_accuracy: bool = False   # If true, prefer OpenRouter
    critical_accuracy: bool = False


class ModelSelection(BaseModel):
    """Selected model configuration"""
    provider: str  # 'groq' or 'openrouter'
    model: str
    fallback_provider: str
    fallback_model: str
    max_tokens: int
    temperature: float


# GROQ MODELS - ULTRA FAST (LPU-based)
GROQ_MODELS = {
    "llama-3.3-70b": "llama-3.3-70b-versatile",
    "llama-3.1-8b": "llama-3.1-8b-instant",
    "mixtral-8x7b": "mixtral-8x7b-32768",
    "deepseek-r1": "deepseek-r1-distill-llama-70b",
}

# OPENROUTER MODELS - BEST FREE MODELS
OPENROUTER_MODELS = {
    "llama-4-scout": "meta-llama/llama-4-scout:free",
    "deepseek-r1": "deepseek/deepseek-r1:free",
    "deepseek-v3": "deepseek/deepseek-v3:free",
    "qwen-coder": "qwen/qwen-2.5-coder-32b-instruct:free",
    "yi-vision": "zero-one-ai/yi-vision:free",
    "gemini-flash": "google/gemini-2.0-flash-exp:free",
    "gemini-pro": "google/gemini-2.5-pro-exp:free",
    "groq-llama-70b": "groq/llama-3.3-70b-versatile",
}

# TASK ROUTING CONFIGURATION
TASK_ROUTING: Dict[TaskType, Dict[str, Any]] = {
    TaskType.REAL_TIME_CHAT: {
        "provider": "groq",
        "model": GROQ_MODELS["llama-3.3-70b"],
        "fallback_provider": "openrouter",
        "fallback_model": OPENROUTER_MODELS["groq-llama-70b"],
        "max_tokens": 2000,
        "temperature": 0.7,
    },
    TaskType.QUICK_CATEGORIZATION: {
        "provider": "groq",
        "model": GROQ_MODELS["llama-3.1-8b"],
        "fallback_provider": "openrouter",
        "fallback_model": OPENROUTER_MODELS["gemini-flash"],
        "max_tokens": 500,
        "temperature": 0.1,
    },
    TaskType.COMPLEX_REASONING: {
        "provider": "openrouter",
        "model": OPENROUTER_MODELS["deepseek-r1"],
        "fallback_provider": "groq",
        "fallback_model": GROQ_MODELS["deepseek-r1"],
        "max_tokens": 4000,
        "temperature": 0.7,
    },
    TaskType.LONG_CONTEXT: {
        "provider": "openrouter",
        "model": OPENROUTER_MODELS["gemini-pro"],
        "fallback_provider": "openrouter",
        "fallback_model": OPENROUTER_MODELS["gemini-flash"],
        "max_tokens": 8000,
        "temperature": 0.7,
    },
    TaskType.STRUCTURED_OUTPUT: {
        "provider": "groq",
        "model": GROQ_MODELS["llama-3.3-70b"],
        "fallback_provider": "openrouter",
        "fallback_model": OPENROUTER_MODELS["qwen-coder"],
        "max_tokens": 4000,
        "temperature": 0.2,
    },
    TaskType.VISION: {
        "provider": "openrouter",
        "model": OPENROUTER_MODELS["llama-4-scout"],
        "fallback_provider": "openrouter",
        "fallback_model": OPENROUTER_MODELS["yi-vision"],
        "max_tokens": 4000,
        "temperature": 0.2,
    },
    TaskType.PROGRAM_GENERATION: {
        "provider": "openrouter",
        "model": OPENROUTER_MODELS["deepseek-r1"],
        "fallback_provider": "openrouter",
        "fallback_model": OPENROUTER_MODELS["deepseek-v3"],
        "max_tokens": 16000,
        "temperature": 0.7,
    },
    TaskType.STREAMING_FEEDBACK: {
        "provider": "groq",
        "model": GROQ_MODELS["llama-3.3-70b"],
        "fallback_provider": "openrouter",
        "fallback_model": OPENROUTER_MODELS["groq-llama-70b"],
        "max_tokens": 2000,
        "temperature": 0.6,
    },
    TaskType.VERIFICATION: {
        "provider": "openrouter",
        "model": OPENROUTER_MODELS["gemini-flash"],
        "fallback_provider": "groq",
        "fallback_model": GROQ_MODELS["llama-3.3-70b"],
        "max_tokens": 1000,
        "temperature": 0.1,
    },
}


class DualModelRouter:
    """
    Dual-API Model Router with Groq + OpenRouter
    """

    def __init__(self):
        self.groq: Optional[AsyncOpenAI] = None
        self.openrouter: Optional[AsyncOpenAI] = None
        self.failed_models: set = set()
        self.usage_stats: Dict[str, int] = {}

        # Initialize Groq client
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            self.groq = AsyncOpenAI(
                api_key=groq_key,
                base_url="https://api.groq.com/openai/v1",
                default_headers={"X-Title": "Wagner Coach"},
            )
            print("[DualRouter] Groq API initialized")
        else:
            print("[DualRouter] WARNING: Groq API key not found, will use OpenRouter fallback")

        # Initialize OpenRouter client
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            self.openrouter = AsyncOpenAI(
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": os.getenv("NEXT_PUBLIC_APP_URL", "http://localhost:3000"),
                    "X-Title": "Wagner Coach",
                },
            )
            print("[DualRouter] OpenRouter API initialized")
        else:
            print("[DualRouter] WARNING: OpenRouter API key not found")

        if not self.groq and not self.openrouter:
            print("[DualRouter] WARNING: No valid API keys found. AI features will not work.")
            # Don't raise error - allow the app to start for non-AI endpoints

    def _select_model(self, config: TaskConfig) -> ModelSelection:
        """Select the best provider and model for the task"""
        base_routing = TASK_ROUTING[config.type]

        # Override based on priorities
        if config.prioritize_speed and self.groq and base_routing["provider"] == "openrouter":
            print(f"[DualRouter] Speed priority: Switching to Groq for {config.type}")
            return ModelSelection(
                provider="groq",
                model=GROQ_MODELS["llama-3.3-70b"],
                fallback_provider="openrouter",  # Fallback to OpenRouter if Groq fails
                fallback_model=base_routing["model"],  # Use the original OpenRouter model
                max_tokens=base_routing["max_tokens"],
                temperature=base_routing["temperature"],
            )

        if config.prioritize_accuracy and base_routing["provider"] == "groq":
            print(f"[DualRouter] Accuracy priority: Switching to OpenRouter for {config.type}")
            return ModelSelection(
                provider="openrouter",
                model=OPENROUTER_MODELS["deepseek-r1"],
                fallback_provider="groq",  # Fallback to Groq if OpenRouter fails
                fallback_model=base_routing["model"],  # Use the original Groq model
                max_tokens=base_routing["max_tokens"],
                temperature=base_routing["temperature"],
            )

        # Check if primary provider is available
        primary_key = f"{base_routing['provider']}:{base_routing['model']}"
        if primary_key in self.failed_models:
            print(f"[DualRouter] Primary failed, using fallback for {config.type}")
            return ModelSelection(
                provider=base_routing["fallback_provider"],
                model=base_routing["fallback_model"],
                fallback_provider=base_routing["provider"],
                fallback_model=base_routing["model"],
                max_tokens=base_routing["max_tokens"],
                temperature=base_routing["temperature"],
            )

        return ModelSelection(**base_routing)

    def _get_client(self, provider: str) -> AsyncOpenAI:
        """Get the appropriate client for the provider"""
        if provider == "groq":
            if not self.groq:
                print("[DualRouter] Groq not available, falling back to OpenRouter")
                if not self.openrouter:
                    raise ValueError("No API clients available")
                return self.openrouter
            return self.groq
        else:
            if not self.openrouter:
                print("[DualRouter] OpenRouter not available, falling back to Groq")
                if not self.groq:
                    raise ValueError("No API clients available")
                return self.groq
            return self.openrouter

    async def complete(
        self,
        config: TaskConfig,
        messages: List[Dict[str, Any]],
        response_format: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Complete a task with intelligent routing and fallback"""
        selection = self._select_model(config)
        client = self._get_client(selection.provider)
        model_key = f"{selection.provider}:{selection.model}"

        # Track usage
        self.usage_stats[model_key] = self.usage_stats.get(model_key, 0) + 1

        print(f"[DualRouter] Using {selection.provider.upper()} - {selection.model}")

        try:
            completion_params = {
                "model": selection.model,
                "messages": messages,
                "temperature": selection.temperature,
                "max_tokens": selection.max_tokens,
            }
            if response_format:
                completion_params["response_format"] = response_format

            response = await client.chat.completions.create(**completion_params)
            return response

        except Exception as error:
            error_msg = str(error)
            print(f"[DualRouter] ERROR: {selection.provider} failed: {error_msg}")

            # Check if it's a quota/rate limit/auth error
            if ("429" in error_msg or "401" in error_msg or
                "quota" in error_msg.lower() or
                "rate limit" in error_msg.lower() or
                "unauthorized" in error_msg.lower() or
                "user not found" in error_msg.lower()):
                self.failed_models.add(model_key)
                print(f"[DualRouter] Falling back to {selection.fallback_provider}")

                # Retry with fallback
                fallback_client = self._get_client(selection.fallback_provider)
                completion_params["model"] = selection.fallback_model
                fallback_response = await fallback_client.chat.completions.create(**completion_params)
                return fallback_response

            # Other error, propagate
            raise error

    async def stream(
        self,
        config: TaskConfig,
        messages: List[Dict[str, Any]],
        response_format: Optional[Dict[str, str]] = None,
    ) -> AsyncIterator:
        """Stream completion with intelligent routing"""
        selection = self._select_model(config)
        client = self._get_client(selection.provider)

        print(f"[DualRouter] Streaming with {selection.provider.upper()} - {selection.model}")

        try:
            completion_params = {
                "model": selection.model,
                "messages": messages,
                "temperature": selection.temperature,
                "max_tokens": selection.max_tokens,
                "stream": True,
            }
            if response_format:
                completion_params["response_format"] = response_format

            response = await client.chat.completions.create(**completion_params)
            return response

        except Exception as error:
            error_msg = str(error)
            if ("429" in error_msg or "401" in error_msg or
                "quota" in error_msg.lower() or
                "unauthorized" in error_msg.lower() or
                "user not found" in error_msg.lower()):
                self.failed_models.add(f"{selection.provider}:{selection.model}")
                print(f"[DualRouter] Streaming fallback to {selection.fallback_provider}")

                fallback_client = self._get_client(selection.fallback_provider)
                completion_params["model"] = selection.fallback_model
                fallback_response = await fallback_client.chat.completions.create(**completion_params)
                return fallback_response

            raise error

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        groq_count = 0
        openrouter_count = 0

        for key, count in self.usage_stats.items():
            if key.startswith("groq:"):
                groq_count += count
            else:
                openrouter_count += count

        return {
            "groq": groq_count,
            "openrouter": openrouter_count,
            "breakdown": self.usage_stats,
        }

    def reset_failures(self) -> None:
        """Reset failure tracking"""
        self.failed_models.clear()
        print("[DualRouter] Failure tracking reset")


# Export singleton
dual_router = DualModelRouter()
