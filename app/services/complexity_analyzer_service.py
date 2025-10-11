"""
Complexity Analyzer Service

Analyzes user queries to determine complexity level for intelligent routing.

Complexity Levels:
- TRIVIAL: Greetings, acknowledgments, simple responses (→ Canned responses)
- SIMPLE: Single data lookups, basic questions (→ Groq Llama 3.3 70B)
- COMPLEX: Multi-step reasoning, analysis, planning (→ Claude 3.5 Sonnet)

This enables 60% cost reduction by routing queries to the most appropriate model.
"""

import logging
import re
import json
from typing import Dict, Any, Optional

# Graceful import for optional groq dependency
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning(
        "[ComplexityAnalyzer] Groq package not installed - smart routing will use "
        "keyword-based classification only (no AI classification)"
    )
    Groq = None  # type: ignore
    GROQ_AVAILABLE = False

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ComplexityAnalyzer:
    """
    Analyze query complexity for intelligent model routing.

    Strategy:
    1. Fast-path: Regex for trivial patterns (no AI needed)
    2. Image check: Images always need vision models (complex)
    3. Groq classification: Use cheap Llama 3.3 70B for ambiguous cases
    """

    def __init__(self):
        # Initialize Groq only if available
        if GROQ_AVAILABLE and settings.GROQ_API_KEY:
            self.groq = Groq(api_key=settings.GROQ_API_KEY)
            logger.info("[ComplexityAnalyzer] Groq AI classification enabled")
        else:
            self.groq = None
            logger.warning(
                "[ComplexityAnalyzer] Groq AI classification disabled - "
                "using keyword-based classification only"
            )

        # Regex patterns for trivial queries (instant classification)
        self.trivial_patterns = [
            r'^(hi|hello|hey|sup|yo|heya|howdy)\b',
            r'^(thanks|thank you|thx|ty|appreciated)\b',
            r'^(ok|okay|cool|nice|great|awesome|perfect|got it)\b',
            r'^(bye|goodbye|see you|later|cya)\b',
            r'^(yes|yeah|yep|yup|sure|alright)\b',
            r'^(no|nope|nah)\b',
        ]

        # Keywords that suggest simple queries
        self.simple_keywords = [
            'what did i eat', 'how many calories', 'what\'s my',
            'show me', 'get my', 'my recent', 'today\'s',
            'look up', 'search for', 'find'
        ]

        # Keywords that suggest complex queries
        self.complex_keywords = [
            'why', 'how should i', 'what should i', 'advice',
            'recommend', 'analyze', 'compare', 'explain',
            'plan', 'strategy', 'help me', 'should i'
        ]

    async def analyze_complexity(
        self,
        message: str,
        has_image: bool = False
    ) -> Dict[str, Any]:
        """
        Analyze query complexity and recommend routing.

        Args:
            message: User's message text
            has_image: Whether the message includes an image

        Returns:
            {
                "complexity": "trivial" | "simple" | "complex",
                "confidence": float (0.0-1.0),
                "reasoning": str,
                "recommended_model": str
            }
        """
        message_lower = message.lower().strip()

        # FAST PATH 1: Regex for trivial queries (no AI needed!)
        for pattern in self.trivial_patterns:
            if re.match(pattern, message_lower, re.IGNORECASE):
                logger.info(f"[ComplexityAnalyzer] TRIVIAL detected via regex: {message[:50]}")
                return {
                    "complexity": "trivial",
                    "confidence": 1.0,
                    "reasoning": "Greeting/acknowledgment detected via regex pattern",
                    "recommended_model": "canned_response"
                }

        # FAST PATH 2: Images almost always need vision models
        if has_image:
            logger.info(f"[ComplexityAnalyzer] COMPLEX detected: message has image")
            return {
                "complexity": "complex",
                "confidence": 0.95,
                "reasoning": "Image analysis requires vision-capable model",
                "recommended_model": "claude-3-5-sonnet"
            }

        # FAST PATH 3: Keyword-based heuristics (before calling AI)
        complexity_hint = self._analyze_keywords(message_lower)
        if complexity_hint:
            logger.info(
                f"[ComplexityAnalyzer] {complexity_hint['complexity'].upper()} "
                f"detected via keywords: {message[:50]}"
            )
            return complexity_hint

        # SLOW PATH: Use Groq for classification (cheap + fast)
        try:
            classification = await self._classify_with_groq(message)
            logger.info(
                f"[ComplexityAnalyzer] {classification['complexity'].upper()} "
                f"detected via Groq: {message[:50]}"
            )
            return classification
        except Exception as e:
            logger.error(f"[ComplexityAnalyzer] Groq classification failed: {e}")
            # Fallback: Default to complex (safer, always works)
            return {
                "complexity": "complex",
                "confidence": 0.5,
                "reasoning": "Classification failed, defaulting to complex for safety",
                "recommended_model": "claude-3-5-sonnet"
            }

    def _analyze_keywords(self, message_lower: str) -> Optional[Dict[str, Any]]:
        """
        Analyze message using keyword heuristics.

        Returns classification if confident, None if ambiguous.
        """
        # Check for simple query keywords
        simple_matches = sum(1 for kw in self.simple_keywords if kw in message_lower)

        # Check for complex query keywords
        complex_matches = sum(1 for kw in self.complex_keywords if kw in message_lower)

        # Confident simple query (e.g., "what did I eat today?")
        if simple_matches >= 1 and complex_matches == 0:
            return {
                "complexity": "simple",
                "confidence": 0.85,
                "reasoning": f"Simple data lookup keywords detected",
                "recommended_model": "groq/llama-3.3-70b"
            }

        # Confident complex query (e.g., "why should I eat more protein?")
        if complex_matches >= 1:
            return {
                "complexity": "complex",
                "confidence": 0.85,
                "reasoning": f"Complex reasoning keywords detected",
                "recommended_model": "claude-3-5-sonnet"
            }

        # Ambiguous - need AI classification
        return None

    async def _classify_with_groq(self, message: str) -> Dict[str, Any]:
        """
        Use Groq Llama 3.3 70B for fast complexity classification.

        Cost: ~$0.01 per 1000 queries (negligible)
        Speed: ~200ms
        """
        # Check if Groq is available
        if not self.groq:
            raise Exception("Groq not available - cannot perform AI classification")

        prompt = f"""Analyze this fitness coach user message and classify its complexity.

User message: "{message}"

Classify as ONE of these levels:

TRIVIAL: Simple greetings, acknowledgments, single-word responses
Examples: "hi", "thanks", "ok", "cool", "yes", "no"

SIMPLE: Single data lookup, basic factual question with clear answer
Examples: "what did I eat today?", "how many calories in chicken?", "show my weight"

COMPLEX: Requires reasoning, analysis, planning, advice, comparisons, multi-step thinking
Examples: "why am I not losing weight?", "should I eat more carbs?", "help me plan meals"

Respond ONLY with valid JSON in this exact format:
{{"complexity": "trivial|simple|complex", "confidence": 0.0-1.0, "reasoning": "brief explanation"}}"""

        response = self.groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=150
        )

        # Parse JSON response
        result = json.loads(response.choices[0].message.content)

        # Map complexity to recommended model
        model_mapping = {
            "trivial": "canned_response",
            "simple": "groq/llama-3.3-70b",
            "complex": "claude-3-5-sonnet"
        }

        result["recommended_model"] = model_mapping.get(
            result["complexity"],
            "claude-3-5-sonnet"  # Default to Claude for safety
        )

        return result


# Singleton instance
_complexity_analyzer: Optional[ComplexityAnalyzer] = None


def get_complexity_analyzer() -> ComplexityAnalyzer:
    """Get the global ComplexityAnalyzer instance."""
    global _complexity_analyzer
    if _complexity_analyzer is None:
        _complexity_analyzer = ComplexityAnalyzer()
    return _complexity_analyzer
