"""
Message Classifier Service

Classifies user messages as CHAT or LOG using cheap Groq model.
Critical for routing messages to correct handler in unified Coach interface.
"""

import logging
from typing import Dict, Any, Optional
from app.services.groq_service_v2 import get_groq_service_v2

logger = logging.getLogger(__name__)


class MessageClassifierService:
    """
    Classifies user messages into CHAT or LOG categories.

    CHAT: Questions, comments, general conversation
    LOG: Meals, workouts, measurements that should be recorded
    """

    def __init__(self):
        self.groq_service = get_groq_service_v2()

    async def classify_message(
        self,
        message: str,
        has_image: bool = False,
        has_audio: bool = False
    ) -> Dict[str, Any]:
        """
        Classify if message is CHAT or LOG.

        Uses Groq Llama 3.3 70B ($0.05/M tokens) for speed & cost.

        Args:
            message: User's message text
            has_image: Whether message includes an image
            has_audio: Whether message includes audio

        Returns:
            {
                "is_log": bool,
                "is_chat": bool,
                "log_type": "meal" | "workout" | "activity" | "measurement" | None,
                "confidence": 0.0-1.0,
                "reasoning": "brief explanation"
            }
        """
        logger.info(f"[Classifier] Classifying message: '{message[:100]}...'")

        system_prompt = """You are a message classifier for a fitness coaching app.

Your job: Determine if a user message is a FITNESS LOG or a CHAT message.

FITNESS LOG indicators:
- Past tense about eating/food ("I ate...", "Had lunch", "Just finished breakfast")
- Past tense about exercise ("Did 10 pushups", "Ran 5K", "Completed workout")
- Mentions measurements with values ("Weight is 175 lbs", "Body fat 15%", "Weighed myself")
- Specific quantities and foods together ("3 eggs", "chicken breast with rice")
- Declarative statements about activities ("bench pressed 185 lbs")
- Photos of food/meals (if has_image=true and food-related text)

CHAT indicators:
- Questions ("What should I eat?", "How many calories do I need?", "Is this enough protein?")
- Requests for advice ("Can you help me with...", "I need suggestions for...")
- Greetings or conversation ("Hi", "Hello", "How's it going?", "Thanks!")
- Future tense ("What if I eat...", "Should I do...", "Planning to...")
- Hypothetical ("If I...", "Would it be better to...")
- General statements without specific data ("I'm feeling tired", "Having a good day")

Examples:

INPUT: "I ate 3 eggs and oatmeal for breakfast"
OUTPUT: {"is_log": true, "is_chat": false, "log_type": "meal", "confidence": 0.95, "reasoning": "Past tense eating with specific foods and quantities"}

INPUT: "What should I eat for breakfast?"
OUTPUT: {"is_log": false, "is_chat": true, "log_type": null, "confidence": 0.98, "reasoning": "Future-oriented question asking for advice"}

INPUT: "Just finished a 5K run in 30 minutes"
OUTPUT: {"is_log": true, "is_chat": false, "log_type": "activity", "confidence": 0.92, "reasoning": "Past tense activity with specific distance and time"}

INPUT: "How many calories should I eat?"
OUTPUT: {"is_log": false, "is_chat": true, "log_type": null, "confidence": 0.97, "reasoning": "Question seeking information/advice"}

INPUT: "Did 3 sets of 10 pushups"
OUTPUT: {"is_log": true, "is_chat": false, "log_type": "workout", "confidence": 0.94, "reasoning": "Past tense exercise with specific sets and reps"}

INPUT: "Weight is 175.5 lbs this morning"
OUTPUT: {"is_log": true, "is_chat": false, "log_type": "measurement", "confidence": 0.96, "reasoning": "Current weight measurement with specific value"}

INPUT: "I'm feeling tired today"
OUTPUT: {"is_log": false, "is_chat": true, "log_type": null, "confidence": 0.85, "reasoning": "General feeling statement without specific data to log"}

INPUT: "Thanks for the help!"
OUTPUT: {"is_log": false, "is_chat": true, "log_type": null, "confidence": 0.99, "reasoning": "Conversational acknowledgment"}

IMPORTANT:
- Default to CHAT if ambiguous (safer to ask than to auto-log incorrectly)
- If message is both (e.g., "I ate eggs. Was that enough protein?"), classify as LOG with note
- Confidence should be high (>0.9) for clear cases
- Lower confidence (0.7-0.9) for ambiguous cases

Return ONLY valid JSON (no markdown, no explanation):
{
    "is_log": true/false,
    "is_chat": true/false,
    "log_type": "meal"|"workout"|"activity"|"measurement"|null,
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation",
    "has_question": true/false  // Does message contain a question to answer?
}
"""

        # Add context about multimodal input
        context_notes = []
        if has_image:
            context_notes.append("User included an image")
            # If image + food-related text, likely meal log
            food_keywords = ['ate', 'eating', 'meal', 'breakfast', 'lunch', 'dinner', 'snack', 'food', 'calories', 'protein']
            if any(keyword in message.lower() for keyword in food_keywords):
                context_notes.append("Image likely shows food/meal (food-related text detected)")
            elif len(message.strip()) < 20:  # Short message with image
                context_notes.append("Image might be primary content (minimal text)")
        if has_audio:
            context_notes.append("User used voice input")

        user_prompt = f"""Classify this message:

Message: "{message}"

{f"Context: {', '.join(context_notes)}" if context_notes else ""}

IMPORTANT: If user includes an image with minimal text or food-related text, it's likely a meal log.

Return JSON classification."""

        try:
            # Call Groq client directly for classification
            import json
            response = self.groq_service.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for consistent classification
                max_tokens=150
            )

            # Parse JSON response
            response_text = response.choices[0].message.content.strip()
            classification = json.loads(response_text)

            logger.info(f"[Classifier] Result: is_log={classification['is_log']}, confidence={classification['confidence']}")

            return classification

        except Exception as e:
            logger.error(f"[Classifier] Classification failed: {e}", exc_info=True)

            # Fallback: Default to CHAT mode (safer)
            return {
                "is_log": False,
                "is_chat": True,
                "log_type": None,
                "confidence": 0.5,
                "reasoning": "Classification failed, defaulting to chat mode",
                "has_question": "?" in message
            }

    def should_show_log_preview(self, classification: Dict[str, Any]) -> bool:
        """
        Determine if we should show log preview card to user.

        Only show preview if:
        - Classified as log
        - High confidence (>0.8)
        - Has valid log_type
        """
        return (
            classification.get("is_log", False) and
            classification.get("confidence", 0) > 0.8 and
            classification.get("log_type") is not None
        )


# Global instance
_classifier_service: Optional[MessageClassifierService] = None


def get_message_classifier() -> MessageClassifierService:
    """Get the global MessageClassifierService instance."""
    global _classifier_service
    if _classifier_service is None:
        _classifier_service = MessageClassifierService()
    return _classifier_service
