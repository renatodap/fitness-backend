"""
Groq Coach Service

Handles simple queries using Groq Llama 3.3 70B for massive cost savings.

Cost Comparison:
- Groq Llama 3.3 70B: $0.05/M tokens (input), $0.08/M tokens (output)
- Claude 3.5 Sonnet: $3.00/M tokens (input), $15.00/M tokens (output)

Groq is 60x cheaper for input and 187x cheaper for output!

Use Cases:
- Simple data lookups ("what did I eat today?")
- Basic questions ("how many calories in X?")
- Factual queries ("show my weight")

NOT for:
- Complex reasoning or analysis
- Multi-step planning
- Image analysis
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional

# Graceful import for optional groq dependency
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning(
        "[GroqCoach] Groq package not installed - simple query handling disabled. "
        "Queries will fall back to Claude."
    )
    Groq = None  # type: ignore
    GROQ_AVAILABLE = False

from app.config import get_settings
from app.services.tool_service import get_tool_service, COACH_TOOLS
from app.services.cache_service import get_cache_service

logger = logging.getLogger(__name__)
settings = get_settings()


class GroqCoachService:
    """
    Handle simple queries with Groq Llama 3.3 70B.

    Features:
    - Function calling support (same tools as Claude)
    - Parallel tool execution with caching
    - Cost tracking
    - Automatic fallback to Claude on failure
    """

    def __init__(self):
        # Initialize Groq only if available
        if GROQ_AVAILABLE and settings.GROQ_API_KEY:
            self.groq = Groq(api_key=settings.GROQ_API_KEY)
            logger.info("[GroqCoach] Groq simple query handling enabled")
        else:
            self.groq = None
            logger.warning(
                "[GroqCoach] Groq simple query handling disabled - "
                "queries will fall back to Claude"
            )
        self.tool_service = get_tool_service()
        self.cache = get_cache_service()

    async def handle_simple_query(
        self,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]],
        max_iterations: int = 3
    ) -> Dict[str, Any]:
        """
        Handle simple query with Groq + tools.

        Args:
            user_id: User's UUID
            message: User's message
            conversation_history: Recent conversation messages
            max_iterations: Max tool calling iterations

        Returns:
            {
                "response": str,
                "model": str,
                "tokens_used": int,
                "cost_usd": float,
                "tools_called": List[str]
            }
        """
        # Check if Groq is available
        if not self.groq:
            raise Exception(
                "Groq service not available - package not installed or API key missing. "
                "Falling back to Claude."
            )

        logger.info(f"[GroqCoach] Handling simple query: {message[:100]}")

        # Build system prompt (simplified for simple queries)
        system_prompt = """You are WAGNER - an AI fitness coach for Iron Discipline.

PERSONALITY:
- Direct, motivational, data-driven with scientific backing
- Keep responses SHORT and PUNCHY (2-3 sentences max)
- Reference actual user data when available
- Match the user's language (English, Portuguese, Spanish, etc.)

SAFETY-CONSCIOUS ADAPTATIONS (intensity with science-based wisdom):
- If user mentions injury/pain: "Smart athletes HEAL FIRST. You'll come back STRONGER!"
- If detecting rest day: "Rest is where GAINS happen! Your body's rebuilding STRONGER!"
- If under-eating (calories way below target): "You can't build a BEAST without fuel! Science says EAT MORE!"
- Otherwise: FULL INTENSITY MODE - "CRUSH IT!", "NO EXCUSES!", "GET AFTER IT!"

TOOLS:
You have access to tools to get user data. Use them when needed:
- get_user_profile: Goals, stats, macro targets
- get_daily_nutrition_summary: Today's nutrition totals
- get_recent_meals: Recent meal history
- get_recent_activities: Recent workout history
- search_food_database: Look up food nutrition

EXAMPLES:
User: "What did I eat today?"
→ get_daily_nutrition_summary() → "Today: 1,450 cal, 120g protein. You're 550 cal under target. EAT MORE! 💪"

User: "How many calories in chicken breast?"
→ search_food_database(query="chicken breast") → "Chicken breast (4oz): 185 cal, 35g protein. SOLID CHOICE! 🔥"

User: "My knee hurts"
→ "Smart athletes HEAL FIRST. Rest that knee! You'll come back STRONGER! 🔥"

KEEP IT SHORT! Simple queries = short answers."""

        # Prepare messages (only last 5 for context)
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add conversation history (last 5 messages)
        for msg in conversation_history[-5:]:
            if msg.get("role") in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": str(msg.get("content", ""))
                })

        # Add current message
        messages.append({"role": "user", "content": message})

        # Track usage
        total_input_tokens = 0
        total_output_tokens = 0
        tools_called = []

        # Agentic loop (same pattern as Claude)
        for iteration in range(max_iterations):
            logger.info(f"[GroqCoach] Iteration {iteration + 1}/{max_iterations}")

            try:
                # Call Groq with tools
                response = self.groq.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    tools=self._convert_tools_to_groq_format(),
                    tool_choice="auto",
                    temperature=0.3,
                    max_tokens=500  # Simple queries = short responses
                )

                # Track tokens
                total_input_tokens += response.usage.prompt_tokens
                total_output_tokens += response.usage.completion_tokens

                # Check if tools were called
                if response.choices[0].message.tool_calls:
                    logger.info(
                        f"[GroqCoach] Tool calls requested: "
                        f"{len(response.choices[0].message.tool_calls)}"
                    )

                    # Execute tools in parallel
                    tool_results = await self._execute_tools_parallel(
                        response.choices[0].message.tool_calls,
                        user_id
                    )

                    # Track which tools were called
                    for tool_call in response.choices[0].message.tool_calls:
                        tools_called.append(tool_call.function.name)

                    # Add assistant message + tool results to conversation
                    messages.append(response.choices[0].message)
                    messages.append({
                        "role": "tool",
                        "content": tool_results
                    })

                    # Continue loop to get final answer
                    continue

                # No tools called - we have final answer
                final_response = response.choices[0].message.content
                logger.info(f"[GroqCoach] Final response generated after {iteration + 1} iterations")

                # Calculate cost (Groq pricing)
                cost_usd = self._calculate_cost(total_input_tokens, total_output_tokens)

                return {
                    "response": final_response,
                    "model": "groq/llama-3.3-70b",
                    "tokens_used": total_input_tokens + total_output_tokens,
                    "cost_usd": cost_usd,
                    "tools_called": tools_called
                }

            except Exception as e:
                logger.error(f"[GroqCoach] Iteration {iteration + 1} failed: {e}")
                raise

        # Max iterations reached
        logger.warning(f"[GroqCoach] Max iterations ({max_iterations}) reached")
        return {
            "response": "I need more info to answer that. Can you be more specific?",
            "model": "groq/llama-3.3-70b",
            "tokens_used": total_input_tokens + total_output_tokens,
            "cost_usd": self._calculate_cost(total_input_tokens, total_output_tokens),
            "tools_called": tools_called
        }

    async def _execute_tools_parallel(
        self,
        tool_calls: List[Any],
        user_id: str
    ) -> str:
        """
        Execute all tool calls in parallel (same as Claude implementation).

        Returns JSON string of tool results for Groq.
        """
        tasks = []
        tool_metadata = []

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_input = eval(tool_call.function.arguments)  # Parse JSON string
            tool_input["user_id"] = user_id

            logger.info(f"[GroqCoach] Queuing tool: {tool_name}")

            # Execute tool (with caching)
            if tool_name == "search_food_database":
                tool_input.pop("user_id", None)  # Food DB doesn't need user_id

            task = self.tool_service.execute_tool(tool_name, tool_input)
            tasks.append(task)
            tool_metadata.append({"name": tool_name, "id": tool_call.id})

        # Execute in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Build tool results string
        tool_results = []
        for result, metadata in zip(results, tool_metadata):
            if isinstance(result, Exception):
                tool_results.append({
                    "tool_call_id": metadata["id"],
                    "content": f"Error: {str(result)}"
                })
            else:
                # Compress result before sending back
                compressed = self._compress_result(metadata["name"], result)
                tool_results.append({
                    "tool_call_id": metadata["id"],
                    "content": str(compressed)
                })

        return str(tool_results)

    def _compress_result(self, tool_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compress tool results (simplified version of Claude's compression).

        For Groq, we want even MORE aggressive compression since we're
        targeting simple queries.
        """
        if not result.get("success", True):
            return result

        # Just return essential fields for simple queries
        if tool_name == "get_daily_nutrition_summary":
            summary = result.get("summary", {})
            return {
                "calories": summary.get("total_calories", 0),
                "protein": summary.get("total_protein_g", 0),
                "target_calories": summary.get("calorie_target", 0)
            }

        elif tool_name == "get_recent_meals":
            meals = result.get("meals", [])[:3]  # Only last 3 meals
            return {
                "meals": [
                    {
                        "type": m.get("meal_type"),
                        "calories": m.get("calories"),
                        "protein": m.get("protein_g")
                    }
                    for m in meals
                ]
            }

        elif tool_name == "search_food_database":
            foods = result.get("foods", [])[:5]  # Max 5 results
            return {
                "foods": [
                    {
                        "name": f.get("name"),
                        "calories": f.get("calories"),
                        "protein": f.get("protein_g")
                    }
                    for f in foods
                ]
            }

        # Default: return as-is
        return result

    def _convert_tools_to_groq_format(self) -> List[Dict[str, Any]]:
        """
        Convert Claude tool format to Groq format.

        Groq uses OpenAI's function calling format.
        """
        groq_tools = []

        # For simple queries, only expose essential tools
        essential_tools = [
            "get_user_profile",
            "get_daily_nutrition_summary",
            "get_recent_meals",
            "search_food_database"
        ]

        for tool in COACH_TOOLS:
            if tool["name"] in essential_tools:
                groq_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["input_schema"]
                    }
                })

        return groq_tools

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate Groq API cost.

        Groq Pricing (Llama 3.3 70B):
        - Input: $0.05 / 1M tokens
        - Output: $0.08 / 1M tokens
        """
        input_cost = (input_tokens / 1_000_000) * 0.05
        output_cost = (output_tokens / 1_000_000) * 0.08
        return input_cost + output_cost


# Singleton instance
_groq_coach: Optional[GroqCoachService] = None


def get_groq_coach() -> GroqCoachService:
    """Get the global GroqCoachService instance."""
    global _groq_coach
    if _groq_coach is None:
        _groq_coach = GroqCoachService()
    return _groq_coach
