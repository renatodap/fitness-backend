"""
AI Coach Service

Manages AI coach personas (Trainer and Nutritionist) with RAG-enhanced context.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from openai import AsyncOpenAI

from app.config import get_settings
from app.services.supabase_service import get_service_client
from app.services.context_builder import get_context_builder

settings = get_settings()
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class CoachService:
    """Service for AI coach interactions."""

    def __init__(self):
        self.supabase = get_service_client()
        self.context_builder = get_context_builder()

    async def get_persona(self, coach_type: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve coach persona by type (for INCREMENT 1 compatibility)

        Args:
            coach_type: 'trainer' or 'nutritionist'

        Returns:
            CoachPersona dict or None if not found
        """
        return await self._get_coach_persona(coach_type)

    async def build_context(
        self,
        user_id: str,
        message: str,
        coach_type: str
    ) -> Dict[str, Any]:
        """
        Build complete user context for AI coach (for INCREMENT 1 compatibility)

        Args:
            user_id: User's UUID
            message: User's current message
            coach_type: Type of coach

        Returns:
            UserContext dict with all relevant user data
        """
        if coach_type == "trainer":
            context_str = await self.context_builder.build_trainer_context(
                user_id=user_id,
                query=message
            )
        else:
            context_str = await self.context_builder.build_nutritionist_context(
                user_id=user_id,
                query=message
            )

        # Return structured context (matches INCREMENT 1 expectations)
        return {
            "user_id": user_id,
            "context_str": context_str,
            "coach_type": coach_type
        }

    async def generate_response(
        self,
        user_id: str,
        message: str,
        coach_type: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate AI coach response (for INCREMENT 1 compatibility)

        Args:
            user_id: User's UUID
            message: User's message
            coach_type: Type of coach
            conversation_id: Optional conversation ID

        Returns:
            ChatResponse dict with AI's message
        """
        try:
            response = await self.get_coach_response(
                user_id=user_id,
                coach_type=coach_type,
                user_message=message
            )

            # Get conversation ID from database
            persona = await self._get_coach_persona(coach_type)
            conversation = await self._get_or_create_conversation(
                user_id=user_id,
                coach_persona_id=persona["id"]
            )

            return {
                "success": True,
                "conversation_id": conversation["id"],
                "message": response["message"],
                "context_used": {
                    "recent_workouts": 0,  # TODO: Add actual counts
                    "recent_meals": 0,
                    "embeddings_retrieved": 0,
                    "profile_used": True
                }
            }
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "success": False,
                "error": str(e),
                "conversation_id": conversation_id or "",
                "message": ""
            }

    async def save_conversation(
        self,
        user_id: str,
        coach_type: str,
        messages: List[Dict[str, Any]],
        conversation_id: Optional[str] = None
    ) -> str:
        """
        Save conversation to database (for INCREMENT 1 compatibility)

        Args:
            user_id: User's UUID
            coach_type: Type of coach
            messages: List of message dicts
            conversation_id: Optional conversation ID for updates

        Returns:
            Conversation ID (UUID)
        """
        try:
            persona = await self._get_coach_persona(coach_type)
            if not persona:
                raise ValueError(f"Coach persona not found: {coach_type}")

            if conversation_id:
                # Update existing conversation
                await self.supabase.table("coach_conversations").update({
                    "messages": messages,
                    "last_message_at": datetime.utcnow().isoformat()
                }).eq("id", conversation_id).execute()
                return conversation_id
            else:
                # Create new conversation
                response = await self.supabase.table("coach_conversations").insert({
                    "user_id": user_id,
                    "coach_persona_id": persona["id"],
                    "messages": messages,
                    "last_message_at": datetime.utcnow().isoformat()
                }).execute()
                return response.data[0]["id"] if response.data else ""
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            raise

    async def load_conversation(
        self,
        user_id: str,
        coach_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Load most recent conversation (for INCREMENT 1 compatibility)

        Args:
            user_id: User's UUID
            coach_type: Type of coach

        Returns:
            Conversation dict or None
        """
        try:
            persona = await self._get_coach_persona(coach_type)
            if not persona:
                return None

            response = (
                self.supabase.table("coach_conversations")
                .select("*")
                .eq("user_id", user_id)
                .eq("coach_persona_id", persona["id"])
                .order("last_message_at", desc=True)
                .limit(1)
                .execute()
            )

            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error loading conversation: {e}")
            return None

    async def get_coach_response(
        self,
        user_id: str,
        coach_type: str,
        user_message: str,
        model: str = "gpt-4o-mini"
    ) -> Dict[str, Any]:
        """
        Get AI coach response to user message.

        Args:
            user_id: User ID
            coach_type: 'trainer' or 'nutritionist'
            user_message: User's message
            model: OpenAI model to use

        Returns:
            Dictionary with coach response and metadata

        Raises:
            ValueError if coach_type is invalid
        """
        if coach_type not in ["trainer", "nutritionist"]:
            raise ValueError(f"Invalid coach_type: {coach_type}")

        # 1. Get coach persona
        persona = await self._get_coach_persona(coach_type)
        if not persona:
            raise ValueError(f"Coach persona not found: {coach_type}")

        # 2. Build context using RAG + structured data
        if coach_type == "trainer":
            context = await self.context_builder.build_trainer_context(
                user_id=user_id,
                query=user_message
            )
        else:
            context = await self.context_builder.build_nutritionist_context(
                user_id=user_id,
                query=user_message
            )

        # 3. Get conversation history
        conversation = await self._get_or_create_conversation(
            user_id=user_id,
            coach_persona_id=persona["id"]
        )

        # 4. Build messages for OpenAI
        messages = self._build_messages(
            persona=persona,
            context=context,
            conversation_history=conversation.get("messages", []),
            user_message=user_message
        )

        # 5. Call OpenAI
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            assistant_message = response.choices[0].message.content

            # 6. Save conversation
            await self._save_conversation_message(
                conversation_id=conversation["id"],
                user_message=user_message,
                assistant_message=assistant_message
            )

            return {
                "coach_type": coach_type,
                "coach_name": persona["display_name"],
                "message": assistant_message,
                "timestamp": datetime.utcnow().isoformat(),
                "model_used": model,
                "tokens_used": response.usage.total_tokens
            }

        except Exception as e:
            logger.error(f"Error getting coach response: {e}")
            raise

    async def create_weekly_recommendations(
        self,
        user_id: str,
        coach_type: str
    ) -> List[Dict[str, Any]]:
        """
        Generate weekly recommendations from coach.

        Args:
            user_id: User ID
            coach_type: 'trainer' or 'nutritionist'

        Returns:
            List of recommendation dictionaries
        """
        # Get coach persona
        persona = await self._get_coach_persona(coach_type)
        if not persona:
            raise ValueError(f"Coach persona not found: {coach_type}")

        # Build context (last 7 days)
        if coach_type == "trainer":
            context = await self.context_builder.build_trainer_context(
                user_id=user_id,
                query="Analyze my progress and suggest improvements for next week",
                days_lookback=7
            )
        else:
            context = await self.context_builder.build_nutritionist_context(
                user_id=user_id,
                query="Analyze my nutrition and suggest improvements for next week",
                days_lookback=7
            )

        # Build prompt for recommendations
        system_prompt = persona["system_prompt"]
        user_prompt = f"""Based on the user's data below, provide 3-5 specific, actionable recommendations for next week.

For each recommendation, provide:
1. Title (brief, action-oriented)
2. Description (specific details)
3. Reasoning (why this recommendation)
4. Priority (1-5, where 5 is highest)

Format your response as a JSON array of objects with keys: title, description, reasoning, priority

Context:
{context}
"""

        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            # Parse recommendations
            recommendations_text = response.choices[0].message.content

            try:
                recommendations_data = json.loads(recommendations_text)
                # Handle both array and object with "recommendations" key
                if isinstance(recommendations_data, dict) and "recommendations" in recommendations_data:
                    recommendations = recommendations_data["recommendations"]
                elif isinstance(recommendations_data, list):
                    recommendations = recommendations_data
                else:
                    logger.warning(f"Unexpected recommendations format: {recommendations_data}")
                    recommendations = []
            except json.JSONDecodeError:
                logger.error(f"Failed to parse recommendations JSON: {recommendations_text}")
                recommendations = []

            # Save recommendations to database
            saved_recommendations = []
            for rec in recommendations:
                saved_rec = await self._save_recommendation(
                    user_id=user_id,
                    coach_persona_id=persona["id"],
                    recommendation_data=rec
                )
                saved_recommendations.append(saved_rec)

            return saved_recommendations

        except Exception as e:
            logger.error(f"Error creating weekly recommendations: {e}")
            raise

    async def get_active_recommendations(
        self,
        user_id: str,
        coach_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get active recommendations for user.

        Args:
            user_id: User ID
            coach_type: Optional filter by coach type

        Returns:
            List of active recommendations
        """
        try:
            query = (
                self.supabase.table("coach_recommendations")
                .select("*, coach_personas(*)")
                .eq("user_id", user_id)
                .eq("status", "pending")
                .order("priority", desc=True)
            )

            if coach_type:
                # Filter by coach type
                persona = await self._get_coach_persona(coach_type)
                if persona:
                    query = query.eq("coach_persona_id", persona["id"])

            response = query.execute()

            return response.data if response.data else []

        except Exception as e:
            logger.error(f"Error getting active recommendations: {e}")
            raise

    async def update_recommendation_status(
        self,
        recommendation_id: str,
        user_id: str,
        status: str,
        feedback_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update recommendation status with user feedback.

        Args:
            recommendation_id: Recommendation ID
            user_id: User ID
            status: New status ('accepted', 'rejected', 'completed')
            feedback_text: Optional feedback text

        Returns:
            Updated recommendation
        """
        try:
            # Update recommendation status
            update_response = (
                self.supabase.table("coach_recommendations")
                .update({"status": status})
                .eq("id", recommendation_id)
                .eq("user_id", user_id)
                .execute()
            )

            # Save feedback
            if feedback_text:
                self.supabase.table("recommendation_feedback").insert({
                    "recommendation_id": recommendation_id,
                    "user_id": user_id,
                    "feedback_type": status,
                    "feedback_text": feedback_text
                }).execute()

            return update_response.data[0] if update_response.data else {}

        except Exception as e:
            logger.error(f"Error updating recommendation status: {e}")
            raise

    async def _get_coach_persona(self, coach_type: str) -> Optional[Dict[str, Any]]:
        """Get coach persona by type."""
        try:
            response = (
                self.supabase.table("coach_personas")
                .select("*")
                .eq("name", coach_type)
                .single()
                .execute()
            )

            return response.data

        except Exception as e:
            logger.error(f"Error getting coach persona: {e}")
            return None

    async def _get_or_create_conversation(
        self,
        user_id: str,
        coach_persona_id: str
    ) -> Dict[str, Any]:
        """Get existing conversation or create new one."""
        try:
            # Try to get existing conversation
            response = (
                self.supabase.table("coach_conversations")
                .select("*")
                .eq("user_id", user_id)
                .eq("coach_persona_id", coach_persona_id)
                .order("last_message_at", desc=True)
                .limit(1)
                .execute()
            )

            if response.data:
                return response.data[0]

            # Create new conversation
            create_response = (
                self.supabase.table("coach_conversations")
                .insert({
                    "user_id": user_id,
                    "coach_persona_id": coach_persona_id,
                    "messages": [],
                    "last_message_at": datetime.utcnow().isoformat()
                })
                .execute()
            )

            return create_response.data[0]

        except Exception as e:
            logger.error(f"Error getting/creating conversation: {e}")
            raise

    def _build_messages(
        self,
        persona: Dict[str, Any],
        context: str,
        conversation_history: List[Dict[str, Any]],
        user_message: str
    ) -> List[Dict[str, str]]:
        """Build messages array for OpenAI."""
        messages = []

        # System message with persona and context
        system_content = f"""{persona['system_prompt']}

You have access to the following context about the user:

{context}

Use this information to provide personalized, specific advice. Reference their actual data when relevant.
"""
        messages.append({"role": "system", "content": system_content})

        # Add recent conversation history (last 10 messages)
        recent_history = conversation_history[-10:] if conversation_history else []
        for msg in recent_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        return messages

    async def _save_conversation_message(
        self,
        conversation_id: str,
        user_message: str,
        assistant_message: str
    ) -> None:
        """Save conversation messages to database."""
        try:
            # Get current conversation
            response = (
                self.supabase.table("coach_conversations")
                .select("messages")
                .eq("id", conversation_id)
                .single()
                .execute()
            )

            current_messages = response.data.get("messages", []) if response.data else []

            # Add new messages
            timestamp = datetime.utcnow().isoformat()
            current_messages.extend([
                {
                    "role": "user",
                    "content": user_message,
                    "timestamp": timestamp
                },
                {
                    "role": "assistant",
                    "content": assistant_message,
                    "timestamp": timestamp
                }
            ])

            # Update conversation
            self.supabase.table("coach_conversations").update({
                "messages": current_messages,
                "last_message_at": timestamp
            }).eq("id", conversation_id).execute()

        except Exception as e:
            logger.error(f"Error saving conversation message: {e}")
            raise

    async def _save_recommendation(
        self,
        user_id: str,
        coach_persona_id: str,
        recommendation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save recommendation to database."""
        try:
            response = (
                self.supabase.table("coach_recommendations")
                .insert({
                    "user_id": user_id,
                    "coach_persona_id": coach_persona_id,
                    "recommendation_type": recommendation_data.get("type", "general"),
                    "title": recommendation_data.get("title"),
                    "description": recommendation_data.get("description"),
                    "reasoning": recommendation_data.get("reasoning"),
                    "priority": recommendation_data.get("priority", 3),
                    "status": "pending"
                })
                .execute()
            )

            return response.data[0] if response.data else {}

        except Exception as e:
            logger.error(f"Error saving recommendation: {e}")
            raise


# Global instance
_coach_service: Optional[CoachService] = None


def get_coach_service() -> CoachService:
    """Get the global CoachService instance."""
    global _coach_service
    if _coach_service is None:
        _coach_service = CoachService()
    return _coach_service
