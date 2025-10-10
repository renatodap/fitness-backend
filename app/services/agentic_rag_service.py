"""
Agentic RAG Service for Unified Coach

Implements sophisticated agentic RAG architecture:
1. Query Analysis Agent: Classifies intent and determines data needs
2. Context Retrieval Agent: Multi-source semantic search
3. Routing Agent: Intelligently prioritizes sources based on query
4. Assembly Agent: Combines context with proper formatting

This ensures the coach has access to ALL user data:
- Profile & preferences
- Meal logs (all sources)
- Activity logs (all sources)
- Workout programs
- Nutrition compliance
- Quick entry history
- Conversation history
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from app.services.supabase_service import get_service_client
from app.services.multimodal_embedding_service import get_multimodal_service

logger = logging.getLogger(__name__)


class AgenticRAGService:
    """
    Agentic RAG service with intelligent query analysis and multi-source retrieval.

    Architecture:
    - Query Analysis: Determines what data is relevant
    - Multi-Source Retrieval: Searches ALL user data sources
    - Intelligent Routing: Prioritizes based on query intent
    - Context Assembly: Formats context optimally for LLM
    """

    def __init__(self):
        self.supabase = get_service_client()
        self.embedding_service = get_multimodal_service()

    async def build_context(
        self,
        user_id: str,
        query: str,
        max_tokens: int = 3000,
        include_conversation_history: bool = True
    ) -> Dict[str, Any]:
        """
        Build comprehensive RAG context using agentic architecture.

        Args:
            user_id: User's UUID
            query: User's query/message
            max_tokens: Maximum tokens for context (roughly chars/4)
            include_conversation_history: Whether to include chat history

        Returns:
            {
                "context_string": str,  # Formatted context for LLM
                "sources_used": List[str],  # Sources retrieved
                "stats": Dict[str, Any],  # Retrieval statistics
            }
        """
        logger.info(f"[AgenticRAG] Building context for query: '{query[:100]}...'")

        try:
            # AGENT 1: Query Analysis - Determine intent and data needs
            query_analysis = await self._analyze_query_intent(query)
            logger.info(f"[AgenticRAG] Query intent: {query_analysis['intent']}, confidence: {query_analysis['confidence']}")

            # AGENT 2: Multi-Source Retrieval - Get data from ALL relevant sources
            context_data = await self._retrieve_multi_source_context(
                user_id=user_id,
                query=query,
                query_analysis=query_analysis
            )

            # AGENT 3: Context Assembly - Format for LLM
            formatted_context = await self._assemble_context(
                context_data=context_data,
                query_analysis=query_analysis,
                max_tokens=max_tokens
            )

            logger.info(
                f"[AgenticRAG] Context built: {len(formatted_context)} chars, "
                f"sources: {context_data['sources_used']}"
            )

            return {
                "context_string": formatted_context,
                "sources_used": context_data['sources_used'],
                "stats": context_data['stats']
            }

        except Exception as e:
            logger.error(f"[AgenticRAG] Context building failed: {e}", exc_info=True)
            # Return minimal context on failure
            return {
                "context_string": "No user context available due to error.",
                "sources_used": [],
                "stats": {"error": str(e)}
            }

    async def _analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """
        AGENT 1: Query Analysis

        Analyzes query to determine:
        - Intent category (nutrition, training, general, measurement)
        - Data sources needed
        - Temporal scope (recent vs historical)
        """
        query_lower = query.lower()

        # Intent classification rules (simple heuristic for now)
        intents = {
            "nutrition": ["eat", "meal", "food", "calorie", "protein", "carb", "diet", "nutrition"],
            "training": ["workout", "exercise", "train", "gym", "lift", "run", "cardio", "strength"],
            "measurement": ["weight", "body", "measurement", "progress", "bodyfat"],
            "general": []  # Catch-all
        }

        # Score each intent
        intent_scores = {}
        for intent_name, keywords in intents.items():
            score = sum(1 for kw in keywords if kw in query_lower)
            if score > 0:
                intent_scores[intent_name] = score

        # Determine primary intent
        if intent_scores:
            primary_intent = max(intent_scores, key=intent_scores.get)
            confidence = intent_scores[primary_intent] / max(len(query_lower.split()), 1)
        else:
            primary_intent = "general"
            confidence = 0.5

        # Determine temporal scope
        temporal_keywords = {
            "recent": ["today", "yesterday", "this week", "recent", "lately", "now"],
            "historical": ["always", "usually", "history", "trend", "progress over time"]
        }

        temporal_scope = "recent"  # Default
        for scope, keywords in temporal_keywords.items():
            if any(kw in query_lower for kw in keywords):
                temporal_scope = scope
                break

        # Determine data sources needed
        data_sources = self._determine_data_sources(primary_intent, query_lower)

        return {
            "intent": primary_intent,
            "confidence": min(confidence, 1.0),
            "temporal_scope": temporal_scope,
            "data_sources_needed": data_sources,
            "raw_scores": intent_scores
        }

    def _determine_data_sources(self, intent: str, query_lower: str) -> List[str]:
        """Determine which data sources to query based on intent."""
        sources = ["profile"]  # Always include profile

        if intent == "nutrition":
            sources.extend(["meals", "nutrition_program", "quick_entry"])
        elif intent == "training":
            sources.extend(["activities", "workouts", "workout_program", "quick_entry"])
        elif intent == "measurement":
            sources.extend(["body_measurements", "quick_entry"])
        else:  # general
            sources.extend(["meals", "activities", "quick_entry"])

        # Add conversation history if query seems conversational
        conversational_keywords = ["you said", "earlier", "before", "remember", "we discussed"]
        if any(kw in query_lower for kw in conversational_keywords):
            sources.append("conversation_history")

        return sources

    async def _retrieve_multi_source_context(
        self,
        user_id: str,
        query: str,
        query_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        AGENT 2: Multi-Source Retrieval

        Retrieves data from ALL relevant sources based on query analysis.
        """
        context_data = {
            "profile": None,
            "meals": [],
            "activities": [],
            "workouts": [],
            "measurements": [],
            "programs": [],
            "quick_entry": [],
            "conversation": [],
            "sources_used": [],
            "stats": {}
        }

        data_sources = query_analysis["data_sources_needed"]
        temporal_scope = query_analysis["temporal_scope"]

        # Determine lookback period
        lookback_days = 7 if temporal_scope == "recent" else 30

        # ALWAYS get profile (critical for personalization)
        if "profile" in data_sources:
            logger.info("[AgenticRAG] Retrieving profile data...")
            context_data["profile"] = await self._get_profile_data(user_id)
            if context_data["profile"]:
                context_data["sources_used"].append("profile")

        # Get meals if nutrition-related
        if "meals" in data_sources:
            logger.info("[AgenticRAG] Retrieving meal logs...")
            context_data["meals"] = await self._get_meal_logs(user_id, lookback_days)
            if context_data["meals"]:
                context_data["sources_used"].append("meals")
                context_data["stats"]["meal_count"] = len(context_data["meals"])

        # Get activities if training-related
        if "activities" in data_sources:
            logger.info("[AgenticRAG] Retrieving activity logs...")
            context_data["activities"] = await self._get_activity_logs(user_id, lookback_days)
            if context_data["activities"]:
                context_data["sources_used"].append("activities")
                context_data["stats"]["activity_count"] = len(context_data["activities"])

        # Get nutrition program if nutrition-related
        if "nutrition_program" in data_sources:
            logger.info("[AgenticRAG] Retrieving nutrition program...")
            nutrition_program = await self._get_active_nutrition_program(user_id)
            if nutrition_program:
                context_data["programs"].append(nutrition_program)
                context_data["sources_used"].append("nutrition_program")

        # Get workout program if training-related
        if "workout_program" in data_sources:
            logger.info("[AgenticRAG] Retrieving workout program...")
            workout_program = await self._get_active_workout_program(user_id)
            if workout_program:
                context_data["programs"].append(workout_program)
                context_data["sources_used"].append("workout_program")

        # Get body measurements if measurement-related
        if "body_measurements" in data_sources:
            logger.info("[AgenticRAG] Retrieving body measurements...")
            context_data["measurements"] = await self._get_body_measurements(user_id, lookback_days)
            if context_data["measurements"]:
                context_data["sources_used"].append("body_measurements")
                context_data["stats"]["measurement_count"] = len(context_data["measurements"])

        # ALWAYS do semantic search on quick_entry_embeddings (RAG core)
        if "quick_entry" in data_sources:
            logger.info("[AgenticRAG] Performing semantic search on quick_entry...")
            context_data["quick_entry"] = await self._semantic_search_quick_entry(user_id, query, limit=10)
            if context_data["quick_entry"]:
                context_data["sources_used"].append("quick_entry_rag")
                context_data["stats"]["rag_results"] = len(context_data["quick_entry"])

        # Get conversation history if needed
        if "conversation_history" in data_sources:
            logger.info("[AgenticRAG] Retrieving conversation history...")
            context_data["conversation"] = await self._get_conversation_history(user_id, limit=10)
            if context_data["conversation"]:
                context_data["sources_used"].append("conversation_history")
                context_data["stats"]["conversation_messages"] = len(context_data["conversation"])

        logger.info(f"[AgenticRAG] Retrieved data from {len(context_data['sources_used'])} sources")

        return context_data

    async def _assemble_context(
        self,
        context_data: Dict[str, Any],
        query_analysis: Dict[str, Any],
        max_tokens: int
    ) -> str:
        """
        AGENT 3: Context Assembly

        Assembles retrieved data into optimal format for LLM.
        Prioritizes based on query intent and applies token limits.
        """
        context_parts = []
        max_chars = max_tokens * 4  # Rough estimate: 4 chars = 1 token

        # ALWAYS START WITH PROFILE (most important for personalization)
        if context_data["profile"]:
            context_parts.append("=== USER PROFILE ===")
            context_parts.append(self._format_profile(context_data["profile"]))
            context_parts.append("")

        # Add programs (structured goals/targets)
        if context_data["programs"]:
            context_parts.append("=== ACTIVE PROGRAMS ===")
            for program in context_data["programs"]:
                context_parts.append(self._format_program(program))
            context_parts.append("")

        # Add relevant structured data based on intent
        intent = query_analysis["intent"]

        if intent == "nutrition" and context_data["meals"]:
            context_parts.append("=== RECENT MEALS ===")
            context_parts.append(self._format_meals(context_data["meals"][:7]))  # Last 7 meals
            context_parts.append("")

        if intent == "training" and context_data["activities"]:
            context_parts.append("=== RECENT WORKOUTS ===")
            context_parts.append(self._format_activities(context_data["activities"][:7]))  # Last 7 workouts
            context_parts.append("")

        if intent == "measurement" and context_data["measurements"]:
            context_parts.append("=== BODY MEASUREMENTS ===")
            context_parts.append(self._format_measurements(context_data["measurements"]))
            context_parts.append("")

        # Add RAG context (semantic search results)
        if context_data["quick_entry"]:
            context_parts.append("=== RELEVANT HISTORY (Semantic Search) ===")
            context_parts.append(self._format_quick_entry_results(context_data["quick_entry"][:10]))
            context_parts.append("")

        # Add conversation history if relevant
        if context_data["conversation"]:
            context_parts.append("=== RECENT CONVERSATION ===")
            context_parts.append(self._format_conversation(context_data["conversation"][:5]))
            context_parts.append("")

        # Join and truncate if needed
        full_context = "\n".join(context_parts)

        if len(full_context) > max_chars:
            logger.warning(f"[AgenticRAG] Context truncated from {len(full_context)} to {max_chars} chars")
            full_context = full_context[:max_chars] + "\n\n[Context truncated due to length limit]"

        return full_context if full_context.strip() else "No relevant user data found."

    # ====== DATA RETRIEVAL METHODS ======

    async def _get_profile_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile with preferences."""
        try:
            response = self.supabase.table("profiles")\
                .select("*")\
                .eq("id", user_id)\
                .single()\
                .execute()

            return response.data if response.data else None
        except Exception as e:
            logger.error(f"[AgenticRAG] Failed to get profile: {e}")
            return None

    async def _get_meal_logs(self, user_id: str, days: int) -> List[Dict[str, Any]]:
        """Get recent meal logs."""
        try:
            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

            response = self.supabase.table("meals")\
                .select("*")\
                .eq("user_id", user_id)\
                .gte("logged_at", cutoff)\
                .order("logged_at", desc=True)\
                .limit(20)\
                .execute()

            return response.data if response.data else []
        except Exception as e:
            logger.error(f"[AgenticRAG] Failed to get meals: {e}")
            return []

    async def _get_activity_logs(self, user_id: str, days: int) -> List[Dict[str, Any]]:
        """Get recent activity/workout logs."""
        try:
            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

            response = self.supabase.table("activities")\
                .select("*")\
                .eq("user_id", user_id)\
                .gte("started_at", cutoff)\
                .order("started_at", desc=True)\
                .limit(20)\
                .execute()

            return response.data if response.data else []
        except Exception as e:
            logger.error(f"[AgenticRAG] Failed to get activities: {e}")
            return []

    async def _get_body_measurements(self, user_id: str, days: int) -> List[Dict[str, Any]]:
        """Get recent body measurements."""
        try:
            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

            response = self.supabase.table("body_measurements")\
                .select("*")\
                .eq("user_id", user_id)\
                .gte("measured_at", cutoff)\
                .order("measured_at", desc=True)\
                .limit(10)\
                .execute()

            return response.data if response.data else []
        except Exception as e:
            logger.error(f"[AgenticRAG] Failed to get measurements: {e}")
            return []

    async def _get_active_nutrition_program(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get active nutrition program."""
        try:
            response = self.supabase.table("nutrition_programs")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("status", "active")\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()

            if response.data:
                return {**response.data[0], "program_type": "nutrition"}
            return None
        except Exception as e:
            logger.error(f"[AgenticRAG] Failed to get nutrition program: {e}")
            return None

    async def _get_active_workout_program(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get active workout program."""
        try:
            response = self.supabase.table("workout_programs")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("status", "active")\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()

            if response.data:
                return {**response.data[0], "program_type": "workout"}
            return None
        except Exception as e:
            logger.error(f"[AgenticRAG] Failed to get workout program: {e}")
            return None

    async def _semantic_search_quick_entry(
        self,
        user_id: str,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Perform semantic search on quick_entry_embeddings."""
        try:
            # Generate query embedding
            query_embedding = await self.embedding_service.embed_text(query)
            embedding_list = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else query_embedding

            # Search with pgvector
            response = await self.supabase.rpc(
                "search_quick_entry_embeddings",
                {
                    "query_embedding": embedding_list,
                    "user_id_filter": user_id,
                    "match_threshold": 0.5,
                    "match_count": limit
                }
            ).execute()

            return response.data if response.data else []
        except Exception as e:
            logger.error(f"[AgenticRAG] Semantic search failed: {e}")
            return []

    async def _get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation messages."""
        try:
            response = self.supabase.table("coach_messages")\
                .select("role, content, created_at")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()

            # Reverse to get chronological order
            return list(reversed(response.data)) if response.data else []
        except Exception as e:
            logger.error(f"[AgenticRAG] Failed to get conversation history: {e}")
            return []

    # ====== FORMATTING METHODS ======

    def _format_profile(self, profile: Dict[str, Any]) -> str:
        """Format profile data."""
        parts = []

        if name := profile.get("full_name"):
            parts.append(f"Name: {name}")
        if age := profile.get("age"):
            parts.append(f"Age: {age}")
        if weight := profile.get("weight_kg"):
            parts.append(f"Weight: {weight} kg")
        if height := profile.get("height_cm"):
            parts.append(f"Height: {height} cm")
        if goal := profile.get("primary_goal"):
            parts.append(f"Primary Goal: {goal}")
        if fitness := profile.get("fitness_level"):
            parts.append(f"Fitness Level: {fitness}")
        if dietary := profile.get("dietary_preferences"):
            parts.append(f"Dietary Preferences: {dietary}")
        if workout_pref := profile.get("workout_preferences"):
            parts.append(f"Workout Preferences: {workout_pref}")

        return "\n".join(parts) if parts else "Profile incomplete"

    def _format_program(self, program: Dict[str, Any]) -> str:
        """Format program data."""
        program_type = program.get("program_type", "unknown")
        parts = [f"[{program_type.upper()} PROGRAM]"]

        if name := program.get("name"):
            parts.append(f"Name: {name}")
        if goal := program.get("goal"):
            parts.append(f"Goal: {goal}")

        if program_type == "nutrition":
            if cals := program.get("target_calories"):
                parts.append(f"Target Calories: {cals}")
            if protein := program.get("target_protein_grams"):
                parts.append(f"Target Protein: {protein}g")
        elif program_type == "workout":
            if freq := program.get("frequency_per_week"):
                parts.append(f"Frequency: {freq}x/week")

        return "\n".join(parts)

    def _format_meals(self, meals: List[Dict[str, Any]]) -> str:
        """Format meal logs."""
        parts = []
        for meal in meals[:7]:  # Last 7 meals
            logged = meal.get("logged_at", "unknown")
            description = meal.get("description", "Meal")
            cals = meal.get("calories") or meal.get("total_calories", 0)
            protein = meal.get("protein_g") or meal.get("total_protein_g", 0)

            parts.append(f"- {logged}: {description} ({cals} cal, {protein}g protein)")

        return "\n".join(parts) if parts else "No meals logged"

    def _format_activities(self, activities: List[Dict[str, Any]]) -> str:
        """Format activity logs."""
        parts = []
        for activity in activities[:7]:  # Last 7 activities
            started = activity.get("started_at", "unknown")
            activity_type = activity.get("activity_type", "Activity")
            duration = activity.get("duration_minutes", 0)

            parts.append(f"- {started}: {activity_type} ({duration} min)")

        return "\n".join(parts) if parts else "No workouts logged"

    def _format_measurements(self, measurements: List[Dict[str, Any]]) -> str:
        """Format body measurements."""
        parts = []
        for m in measurements:
            measured = m.get("measured_at", "unknown")
            weight = m.get("weight_kg") or m.get("weight_lbs")

            parts.append(f"- {measured}: Weight: {weight}")

        return "\n".join(parts) if parts else "No measurements logged"

    def _format_quick_entry_results(self, results: List[Dict[str, Any]]) -> str:
        """Format semantic search results from quick_entry."""
        parts = []
        for i, result in enumerate(results, 1):
            classification = result.get("source_classification", "entry")
            summary = result.get("content_summary", result.get("content_text", "")[:150])
            logged_at = result.get("logged_at", "unknown")
            similarity = result.get("similarity", 0)

            parts.append(
                f"{i}. [{classification.upper()}] ({logged_at}) [similarity: {similarity:.2f}]\n"
                f"   {summary}"
            )

        return "\n\n".join(parts) if parts else "No relevant history found"

    def _format_conversation(self, messages: List[Dict[str, Any]]) -> str:
        """Format conversation history."""
        parts = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:200]  # Truncate

            parts.append(f"{role.upper()}: {content}")

        return "\n".join(parts) if parts else "No conversation history"


# Global instance
_agentic_rag_service: Optional[AgenticRAGService] = None


def get_agentic_rag_service() -> AgenticRAGService:
    """Get the global AgenticRAGService instance."""
    global _agentic_rag_service
    if _agentic_rag_service is None:
        _agentic_rag_service = AgenticRAGService()
    return _agentic_rag_service
