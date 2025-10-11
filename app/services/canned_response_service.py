"""
Canned Response Service

Provides instant, pre-written responses for trivial queries.

Cost: FREE ($0.00)
Latency: 0ms (instant)

Use Cases:
- Greetings ("hi", "hello", "hey")
- Thanks ("thanks", "thank you")
- Acknowledgments ("ok", "cool", "nice")
- Simple confirmations ("yes", "no")

This is the ultimate optimization - zero cost, zero latency!
"""

import logging
import re
import random
from typing import Optional

logger = logging.getLogger(__name__)


class CannedResponseService:
    """
    Handle trivial queries with pre-written responses.

    Features:
    - Pattern-based matching
    - Random response selection for variety
    - On-brand (motivational, intense)
    - Multilingual support (English, Portuguese, Spanish)
    """

    def __init__(self):
        # Response templates organized by category
        self.responses = {
            "greeting_en": [
                "What's up! Ready to CRUSH IT today? 💪",
                "Let's GO! What are we training today? 🔥",
                "Hey! Time to make some GAINS! 💯",
                "Yo! Ready to DOMINATE? Let's work! 🦾",
                "What's good! Time to GET AFTER IT! ⚡",
            ],
            "greeting_pt": [
                "E aí! Pronto para ARRASAR hoje? 💪",
                "Vamos NESSA! O que vamos treinar hoje? 🔥",
                "Opa! Hora de fazer GANHOS! 💯",
                "Fala! Pronto para DOMINAR? Bora! 🦾",
            ],
            "greeting_es": [
                "¡Qué pasa! ¿Listo para ARRASAR hoy? 💪",
                "¡Vamos! ¿Qué vamos a entrenar hoy? 🔥",
                "¡Hey! ¡Hora de hacer GANANCIAS! 💯",
            ],
            "thanks_en": [
                "You got it! Now GO WORK! 💪",
                "No problem! Keep CRUSHING IT! 🔥",
                "Hell yeah! Now execute! 💯",
                "Anytime! Stay HUNGRY! 🦾",
                "For sure! Keep GRINDING! ⚡",
            ],
            "thanks_pt": [
                "Tranquilo! Agora VAI TRABALHAR! 💪",
                "Sem problema! Continue ARRASANDO! 🔥",
                "Isso aí! Agora é executar! 💯",
                "Sempre! Mantenha a FOME! 🦾",
            ],
            "thanks_es": [
                "¡Por supuesto! ¡Ahora A TRABAJAR! 💪",
                "¡No hay problema! ¡Sigue ARRASANDO! 🔥",
                "¡Claro! ¡Ahora ejecuta! 💯",
            ],
            "acknowledgment_en": [
                "Got it! What's next? 💪",
                "Heard! Let's keep going! 🔥",
                "Solid! What else? 💯",
                "Perfect! Keep moving! 🦾",
                "Cool! What now? ⚡",
            ],
            "acknowledgment_pt": [
                "Entendi! O que mais? 💪",
                "Beleza! Vamos continuar! 🔥",
                "Massa! E agora? 💯",
                "Perfeito! Segue o jogo! 🦾",
            ],
            "acknowledgment_es": [
                "¡Entendido! ¿Qué sigue? 💪",
                "¡Escuchado! ¡Sigamos! 🔥",
                "¡Perfecto! ¿Qué más? 💯",
            ],
            "yes_en": [
                "LET'S GO! 💪",
                "HELL YEAH! 🔥",
                "THAT'S THE SPIRIT! 💯",
                "DAMN RIGHT! 🦾",
            ],
            "yes_pt": [
                "BORA! 💪",
                "ISSO AÍ! 🔥",
                "ESSA É A ATITUDE! 💯",
            ],
            "yes_es": [
                "¡VAMOS! 💪",
                "¡ESO ES! 🔥",
                "¡ESA ES LA ACTITUD! 💯",
            ],
            "no_en": [
                "Alright! What can I help with? 💪",
                "No problem! What do you need? 🔥",
                "Got it! How can I assist? 💯",
            ],
            "no_pt": [
                "Beleza! Como posso ajudar? 💪",
                "Sem problema! O que você precisa? 🔥",
                "Entendi! Em que posso ajudar? 💯",
            ],
            "no_es": [
                "¡De acuerdo! ¿En qué puedo ayudar? 💪",
                "¡No hay problema! ¿Qué necesitas? 🔥",
            ],
            "goodbye_en": [
                "Later! GO CRUSH IT! 💪",
                "See you! STAY HUNGRY! 🔥",
                "Bye! KEEP GRINDING! 💯",
            ],
            "goodbye_pt": [
                "Até! VAI ARRASAR! 💪",
                "Tchau! MANTENHA A FOME! 🔥",
                "Falou! CONTINUE NA LUTA! 💯",
            ],
            "goodbye_es": [
                "¡Hasta luego! ¡A ARRASAR! 💪",
                "¡Nos vemos! ¡MANTÉN EL HAMBRE! 🔥",
            ],
        }

        # Language detection patterns
        self.language_patterns = {
            "pt": [
                r'\b(oi|olá|e aí|fala|beleza|valeu|obrigad|bora|massa)\b',
                r'\b(sim|não|tá|bem|certo)\b'
            ],
            "es": [
                r'\b(hola|qué pasa|gracias|vale|claro|bueno)\b',
                r'\b(sí|no|está|bien)\b'
            ]
        }

    def get_response(self, message: str) -> str:
        """
        Get a canned response for trivial queries.

        Args:
            message: User's message

        Returns:
            Pre-written response matching the message type and language
        """
        message_lower = message.lower().strip()

        # Detect language
        lang = self._detect_language(message_lower)
        logger.info(f"[CannedResponse] Detected language: {lang} for message: {message[:50]}")

        # Greeting patterns
        if re.match(r'^(hi|hello|hey|sup|yo|heya|howdy|oi|olá|e aí|fala|hola|qué pasa)\b', message_lower, re.IGNORECASE):
            return self._get_random_response(f"greeting_{lang}")

        # Thanks patterns
        if re.match(r'^(thanks|thank you|thx|ty|valeu|obrigad|gracias)\b', message_lower, re.IGNORECASE):
            return self._get_random_response(f"thanks_{lang}")

        # Yes patterns
        if re.match(r'^(yes|yeah|yep|yup|sure|sim|sí|claro)\b', message_lower, re.IGNORECASE):
            return self._get_random_response(f"yes_{lang}")

        # No patterns
        if re.match(r'^(no|nope|nah|não|nada)\b', message_lower, re.IGNORECASE):
            return self._get_random_response(f"no_{lang}")

        # Goodbye patterns
        if re.match(r'^(bye|goodbye|see you|later|cya|tchau|até|adiós|hasta luego)\b', message_lower, re.IGNORECASE):
            return self._get_random_response(f"goodbye_{lang}")

        # Acknowledgment patterns (ok, cool, nice, etc.)
        if re.match(r'^(ok|okay|cool|nice|great|awesome|perfect|got it|alright|beleza|massa|tá|está|bueno|vale)\b', message_lower, re.IGNORECASE):
            return self._get_random_response(f"acknowledgment_{lang}")

        # Fallback (shouldn't reach here, but just in case)
        logger.warning(f"[CannedResponse] No pattern matched for: {message}")
        return "Let's GO! 💪"

    def _detect_language(self, message_lower: str) -> str:
        """
        Detect message language (en, pt, es).

        Returns 'en' by default.
        """
        # Check Portuguese patterns
        for pattern in self.language_patterns.get("pt", []):
            if re.search(pattern, message_lower, re.IGNORECASE):
                return "pt"

        # Check Spanish patterns
        for pattern in self.language_patterns.get("es", []):
            if re.search(pattern, message_lower, re.IGNORECASE):
                return "es"

        # Default to English
        return "en"

    def _get_random_response(self, category: str) -> str:
        """
        Get a random response from the specified category.

        Args:
            category: Response category (e.g., "greeting_en")

        Returns:
            Random response from that category
        """
        responses = self.responses.get(category, self.responses.get(category.replace("_pt", "_en").replace("_es", "_en"), []))

        if not responses:
            logger.warning(f"[CannedResponse] No responses for category: {category}")
            return "Let's GO! 💪"

        return random.choice(responses)


# Singleton instance
_canned_response: Optional[CannedResponseService] = None


def get_canned_response() -> CannedResponseService:
    """Get the global CannedResponseService instance."""
    global _canned_response
    if _canned_response is None:
        _canned_response = CannedResponseService()
    return _canned_response
