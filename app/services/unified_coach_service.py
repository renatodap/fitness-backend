"""
Unified Coach Service

Handles ALL user interactions in one chat interface:
- CHAT MODE: Questions, conversations, advice (with RAG context)
- LOG MODE: Meal/workout/measurement logging (with confirmation)

This replaces separate AI Chat and Quick Entry features.
"""

import logging
import uuid
from typing import Dict, Any, Optional, AsyncGenerator
from datetime import datetime

from app.services.message_classifier_service import get_message_classifier
from app.services.quick_entry_service import get_quick_entry_service
from app.services.supabase_service import get_service_client
from app.services.multimodal_embedding_service import get_multimodal_service
from anthropic import AsyncAnthropic
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class UnifiedCoachService:
    """
    Unified Coach handles both chat and logging in one interface.

    User experience:
    1. User sends message (text, voice, image)
    2. System classifies: CHAT or LOG?
    3. If CHAT: Generate AI response with RAG context
    4. If LOG: Show preview card for confirmation
    5. All messages stored and vectorized for RAG
    """

    def __init__(self):
        self.supabase = get_service_client()
        self.classifier = get_message_classifier()
        self.quick_entry = get_quick_entry_service()
        self.embedding_service = get_multimodal_service()
        self.anthropic = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None,
        image_base64: Optional[str] = None,
        audio_base64: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process ANY user message and route appropriately.

        Args:
            user_id: User's UUID
            message: User's message text
            conversation_id: Optional conversation thread ID
            image_base64: Optional base64 encoded image
            audio_base64: Optional base64 encoded audio
            metadata: Optional metadata (e.g., manual_type override)

        Returns:
            {
                "mode": "chat" | "log_preview",
                "conversation_id": "...",
                "message_id": "...",
                # For CHAT mode:
                "response": "..." or "streaming_url": "...",
                # For LOG mode:
                "log_preview": {...extracted data...},
                "log_type": "meal" | "workout" | "measurement"
            }
        """
        logger.info(f"[UnifiedCoach.process_message] START - user_id: {user_id}")
        logger.info(f"[UnifiedCoach.process_message] Message length: {len(message)}, conversation_id: {conversation_id}")

        try:
            # Create or reuse conversation
            if not conversation_id:
                # Create new conversation in database
                logger.info(f"[UnifiedCoach.process_message] Creating new conversation for user {user_id}")
                try:
                    conversation_id = await self._create_conversation(user_id)
                    logger.info(f"[UnifiedCoach.process_message] Created conversation: {conversation_id}")
                except Exception as conv_err:
                    logger.error(f"[UnifiedCoach.process_message] Failed to create conversation: {conv_err}", exc_info=True)
                    raise
            else:
                # Verify conversation exists
                logger.info(f"[UnifiedCoach.process_message] Verifying existing conversation: {conversation_id}")
                try:
                    existing = self.supabase.table("coach_conversations")\
                        .select("id")\
                        .eq("id", conversation_id)\
                        .eq("user_id", user_id)\
                        .execute()

                    if not existing.data:
                        # Conversation doesn't exist or doesn't belong to user
                        logger.warning(f"[UnifiedCoach.process_message] Conversation {conversation_id} not found, creating new one")
                        conversation_id = await self._create_conversation(user_id)
                    else:
                        logger.info(f"[UnifiedCoach.process_message] Conversation verified: {conversation_id}")
                except Exception as verify_err:
                    logger.error(f"[UnifiedCoach.process_message] Failed to verify conversation: {verify_err}", exc_info=True)
                    raise

            # Save user message to database
            logger.info(f"[UnifiedCoach.process_message] Saving user message to conversation {conversation_id}")
            try:
                user_message_id = await self._save_user_message(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    content=message,
                    image_base64=image_base64,
                    audio_base64=audio_base64
                )
                logger.info(f"[UnifiedCoach.process_message] User message saved: {user_message_id}")
            except Exception as save_err:
                logger.error(f"[UnifiedCoach.process_message] Failed to save user message: {save_err}", exc_info=True)
                raise

            # STEP 1: Classify message type
            logger.info(f"[UnifiedCoach.process_message] Classifying message...")
            try:
                classification = await self.classifier.classify_message(
                    message=message,
                    has_image=image_base64 is not None,
                    has_audio=audio_base64 is not None
                )
                logger.info(f"[UnifiedCoach.process_message] Classification: is_log={classification['is_log']}, confidence={classification['confidence']}, log_type={classification.get('log_type')}")
            except Exception as class_err:
                logger.error(f"[UnifiedCoach.process_message] Classification failed: {class_err}", exc_info=True)
                raise

            # Check for manual override
            if metadata and metadata.get('manual_type'):
                logger.info(f"[UnifiedCoach.process_message] Manual override: {metadata['manual_type']}")
                classification['is_log'] = True
                classification['log_type'] = metadata['manual_type']
                classification['confidence'] = 1.0

            # STEP 2: Route to appropriate handler
            if classification['is_log'] and self.classifier.should_show_log_preview(classification):
                # LOG MODE
                logger.info(f"[UnifiedCoach.process_message] Routing to LOG MODE (type: {classification['log_type']})")
                return await self._handle_log_mode(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    user_message_id=user_message_id,
                    message=message,
                    image_base64=image_base64,
                    audio_base64=audio_base64,
                    classification=classification,
                    metadata=metadata
                )
            else:
                # CHAT MODE
                logger.info(f"[UnifiedCoach.process_message] Routing to CHAT MODE")
                return await self._handle_chat_mode(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    user_message_id=user_message_id,
                    message=message,
                    image_base64=image_base64,
                    classification=classification
                )

        except Exception as e:
            logger.error(f"[UnifiedCoach.process_message] CRITICAL ERROR: {e}", exc_info=True)
            logger.error(f"[UnifiedCoach.process_message] Error type: {type(e).__name__}, args: {e.args}")
            raise

    async def _handle_chat_mode(
        self,
        user_id: str,
        conversation_id: str,
        user_message_id: str,
        message: str,
        image_base64: Optional[str],
        classification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle CHAT mode: Generate AI response with RAG context.

        Flow:
        1. Build RAG context from ALL user data
        2. Generate Claude response (streaming)
        3. Save AI response to database
        4. Vectorize both user message and AI response
        5. Return response
        """
        logger.info(f"[UnifiedCoach._handle_chat_mode] START - user_message_id: {user_message_id}")

        try:
            # STEP 1: Build RAG context
            logger.info(f"[UnifiedCoach._handle_chat_mode] Building RAG context for user {user_id}...")
            try:
                rag_context = await self._build_rag_context(user_id, message)
                logger.info(f"[UnifiedCoach._handle_chat_mode] RAG context built: {len(rag_context)} chars")
            except Exception as rag_err:
                logger.error(f"[UnifiedCoach._handle_chat_mode] RAG context build failed: {rag_err}", exc_info=True)
                # Use empty context if RAG fails (non-critical)
                rag_context = "No previous user data available."
                logger.warning(f"[UnifiedCoach._handle_chat_mode] Using empty RAG context due to error")

            # STEP 2: Generate AI response (Claude with streaming + caching)

            # Build Iron Discipline system prompt (cached for cost savings)
            base_system_prompt = """You are WAGNER - the AI coach for Iron Discipline, a hardcore fitness platform.

PERSONALITY:
- Intense, direct, motivational (think David Goggins meets a knowledgeable coach)
- Use strong language: "CRUSH IT", "NO EXCUSES", "BEAST MODE"
- Short, punchy responses (2-3 paragraphs max unless deep analysis requested)
- Reference user's actual data with SPECIFICS
- Balance intensity with expertise - you're tough but you know your shit

RESPONSE RULES:
1. ALWAYS reference their actual data when relevant
2. Be specific: "Based on your 3 workouts this week..." not "Based on your data..."
3. Push them hard but stay supportive
4. If they're slacking, call it out (kindly but firmly)
5. Celebrate wins LOUDLY: "🔥🔥🔥 NEW PR! LET'S GOOOOO!"
6. Link nutrition to performance: "That 450cal breakfast before your run? PERFECT for endurance"

EXAMPLE TONE:
User: "What should I eat for breakfast?"
Wagner: "Looking at your training schedule, you've got solid workouts this week. You need FUEL.

Aim for 450-550 calories with 35-40g protein. Think:
- 3 whole eggs + oatmeal + banana
- Greek yogurt (200g) + granola + berries + protein scoop
- Protein pancakes (3) + peanut butter + honey

Based on your recent meals, you're averaging good protein. Keep crushing it. 💪"

Now respond to the user with this energy and specificity."""

            logger.info(f"[UnifiedCoach._handle_chat_mode] Calling Claude API with caching...")
            logger.info(f"[UnifiedCoach._handle_chat_mode] Base prompt length: {len(base_system_prompt)}")
            logger.info(f"[UnifiedCoach._handle_chat_mode] RAG context length: {len(rag_context)}")
            logger.info(f"[UnifiedCoach._handle_chat_mode] User message length: {len(message)}")

            # Create message for Claude
            ai_response_text = ""
            response_chunks = []
            tokens_used = 0
            cost_usd = 0.0

            try:
                # Use Claude streaming WITH PROMPT CACHING (90% cost savings!)
                async with self.anthropic.messages.stream(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    temperature=0.3,  # Lower temp for more factual coaching (was 0.7)
                    system=[
                        {
                            "type": "text",
                            "text": base_system_prompt,
                            "cache_control": {"type": "ephemeral"}  # Cache base prompt!
                        },
                        {
                            "type": "text",
                            "text": f"\n\n=== USER DATA ===\n{rag_context}",
                            "cache_control": {"type": "ephemeral"}  # Cache RAG context too!
                        }
                    ],
                    messages=[
                        {"role": "user", "content": message}
                    ]
                ) as stream:
                    logger.info(f"[UnifiedCoach._handle_chat_mode] Claude stream started")
                    async for text in stream.text_stream:
                        ai_response_text += text
                        response_chunks.append(text)
                    logger.info(f"[UnifiedCoach._handle_chat_mode] Claude stream completed")

                # Get usage stats (includes cache metrics!)
                logger.info(f"[UnifiedCoach._handle_chat_mode] Getting usage stats...")
                usage = await stream.get_final_message()

                # Extract all token types (including cache)
                input_tokens = usage.usage.input_tokens
                output_tokens = usage.usage.output_tokens
                cache_read_tokens = getattr(usage.usage, 'cache_read_input_tokens', 0)
                cache_write_tokens = getattr(usage.usage, 'cache_creation_input_tokens', 0)

                tokens_used = input_tokens + output_tokens + cache_read_tokens + cache_write_tokens
                cost_usd = self._calculate_claude_cost(
                    input_tokens,
                    output_tokens,
                    cache_read_tokens,
                    cache_write_tokens
                )

                logger.info(
                    f"[UnifiedCoach._handle_chat_mode] Token usage: "
                    f"input={input_tokens}, output={output_tokens}, "
                    f"cache_read={cache_read_tokens}, cache_write={cache_write_tokens}"
                )

                logger.info(f"[UnifiedCoach._handle_chat_mode] AI response generated: {len(ai_response_text)} chars, {tokens_used} tokens, ${cost_usd:.6f}")
            except Exception as claude_err:
                logger.error(f"[UnifiedCoach._handle_chat_mode] Claude API call failed: {claude_err}", exc_info=True)
                logger.error(f"[UnifiedCoach._handle_chat_mode] Claude error type: {type(claude_err).__name__}")
                raise

            # STEP 3: Save AI response to database
            logger.info(f"[UnifiedCoach._handle_chat_mode] Saving AI response to database...")
            try:
                ai_message_id = await self._save_ai_message(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    content=ai_response_text,
                    tokens_used=tokens_used,
                    cost_usd=cost_usd,
                    context_used={"rag_sources": "quick_entry_embeddings"}
                )
                logger.info(f"[UnifiedCoach._handle_chat_mode] AI message saved: {ai_message_id}")
            except Exception as save_err:
                logger.error(f"[UnifiedCoach._handle_chat_mode] Failed to save AI message: {save_err}", exc_info=True)
                raise

            # STEP 4: Vectorize both messages (async, non-blocking)
            logger.info(f"[UnifiedCoach._handle_chat_mode] Vectorizing messages...")
            try:
                await self._vectorize_message(user_id, user_message_id, message, "user")
                await self._vectorize_message(user_id, ai_message_id, ai_response_text, "assistant")
                logger.info(f"[UnifiedCoach._handle_chat_mode] Messages vectorized successfully")
            except Exception as vec_err:
                logger.error(f"[UnifiedCoach._handle_chat_mode] Vectorization failed (non-critical): {vec_err}")

            # STEP 5: Return response (matching UnifiedMessageResponse schema)
            logger.info(f"[UnifiedCoach._handle_chat_mode] Returning chat response")
            return {
                "success": True,
                "conversation_id": conversation_id,
                "message_id": ai_message_id,  # The AI's message ID
                "is_log_preview": False,
                "message": ai_response_text,  # The AI response text
                "log_preview": None,
                "rag_context": None,  # TODO: Add RAG context stats
                "tokens_used": tokens_used,
                "cost_usd": cost_usd,
                "error": None
            }

        except Exception as e:
            logger.error(f"[UnifiedCoach._handle_chat_mode] CRITICAL ERROR: {e}", exc_info=True)
            logger.error(f"[UnifiedCoach._handle_chat_mode] Error type: {type(e).__name__}, args: {e.args}")
            # Return error response matching schema
            return {
                "success": False,
                "conversation_id": conversation_id,
                "message_id": user_message_id,  # Return the user message ID on error
                "is_log_preview": False,
                "message": None,
                "log_preview": None,
                "rag_context": None,
                "tokens_used": None,
                "cost_usd": None,
                "error": "Failed to generate response. Please try again."
            }

    async def _handle_log_mode(
        self,
        user_id: str,
        conversation_id: str,
        user_message_id: str,
        message: str,
        image_base64: Optional[str],
        audio_base64: Optional[str],
        classification: Dict[str, Any],
        metadata: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Handle LOG mode: Extract structured data and show preview.

        Flow:
        1. Use Quick Entry service to extract structured data
        2. Save as log_preview message in conversation
        3. Return preview data for UI to display
        4. User will confirm later via confirm_log()
        """
        logger.info(f"[UnifiedCoach] LOG MODE: {classification['log_type']}")

        try:
            # Use existing Quick Entry preview logic
            preview_result = await self.quick_entry.process_entry_preview(
                user_id=user_id,
                text=message,
                image_base64=image_base64,
                audio_base64=audio_base64,
                metadata=metadata
            )

            if not preview_result.get("success"):
                # Failed to extract - fall back to chat mode
                logger.warning(f"[UnifiedCoach] Log extraction failed, falling back to chat")
                return await self._handle_chat_mode(
                    user_id, conversation_id, user_message_id, message, image_base64, classification
                )

            # Update user message type to log_preview
            self.supabase.table("coach_messages").update({
                "message_type": "log_preview",
                "metadata": {
                    "log_type": preview_result["entry_type"],
                    "extracted_data": preview_result["data"],
                    "confidence": preview_result["confidence"]
                }
            }).eq("id", user_message_id).execute()

            logger.info(f"[UnifiedCoach] Log preview created: {preview_result['entry_type']}")

            # Build LogPreview object matching schema
            from app.api.v1.schemas.unified_coach_schemas import LogPreview, LogType

            log_preview = LogPreview(
                log_type=LogType(preview_result["entry_type"]),
                confidence=preview_result["confidence"],
                data=preview_result["data"],
                reasoning=preview_result.get("reasoning", "AI detected this as a log entry"),
                summary=preview_result.get("summary", f"{preview_result['entry_type'].title()} entry detected")
            )

            return {
                "success": True,
                "conversation_id": conversation_id,
                "message_id": user_message_id,  # The user's message ID
                "is_log_preview": True,
                "message": None,
                "log_preview": log_preview.model_dump(),  # Convert to dict
                "rag_context": None,
                "tokens_used": None,
                "cost_usd": None,
                "error": None
            }

        except Exception as e:
            logger.error(f"[UnifiedCoach] Log mode failed: {e}", exc_info=True)
            return {
                "success": False,
                "conversation_id": conversation_id,
                "message_id": user_message_id,
                "is_log_preview": False,
                "message": None,
                "log_preview": None,
                "rag_context": None,
                "tokens_used": None,
                "cost_usd": None,
                "error": "Failed to process log. Please try again."
            }

    async def confirm_log(
        self,
        user_id: str,
        conversation_id: str,
        user_message_id: str,
        log_type: str,
        log_data: Dict[str, Any],
        original_text: str
    ) -> Dict[str, Any]:
        """
        User confirmed the log preview - save it to structured tables.

        Flow:
        1. Use Quick Entry service to save log
        2. Update message type to log_confirmed
        3. Add success message to conversation
        4. Vectorize the log
        """
        logger.info(f"[UnifiedCoach] Confirming log: {log_type}")

        try:
            # Save log using Quick Entry service
            save_result = await self.quick_entry.confirm_and_save_entry(
                user_id=user_id,
                entry_type=log_type,
                data=log_data,
                original_text=original_text
            )

            if not save_result.get("success"):
                return {
                    "success": False,
                    "error": save_result.get("error", "Failed to save log")
                }

            # Update user message to log_confirmed
            self.supabase.table("coach_messages").update({
                "message_type": "log_confirmed",
                "quick_entry_log_id": save_result.get("quick_entry_log_id"),
                "metadata": {
                    "log_type": log_type,
                    "entry_id": save_result.get("entry_id")
                }
            }).eq("id", user_message_id).execute()

            # Add success system message
            success_message = self._build_success_message(log_type, log_data)
            system_message_id = await self._save_system_message(
                user_id=user_id,
                conversation_id=conversation_id,
                content=success_message
            )

            logger.info(f"[UnifiedCoach] Log confirmed and saved: {save_result.get('entry_id')}")

            return {
                "success": True,
                "conversation_id": conversation_id,
                "entry_id": save_result.get("entry_id"),
                "system_message_id": system_message_id,
                "message": success_message
            }

        except Exception as e:
            logger.error(f"[UnifiedCoach] Log confirmation failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": "Failed to save log. Please try again."
            }

    async def get_conversation_history(
        self,
        user_id: str,
        conversation_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get conversation history for user.

        Args:
            user_id: User's UUID
            conversation_id: Optional specific conversation ID
            limit: Number of messages to return
            offset: Offset for pagination

        Returns:
            {
                "conversations": [list of conversations],
                "messages": [list of messages],
                "total": int
            }
        """
        try:
            if conversation_id:
                # Get specific conversation
                messages = self.supabase.table("coach_messages")\
                    .select("*")\
                    .eq("user_id", user_id)\
                    .eq("conversation_id", conversation_id)\
                    .order("created_at", desc=False)\
                    .limit(limit)\
                    .offset(offset)\
                    .execute()

                return {
                    "conversation_id": conversation_id,
                    "messages": messages.data,
                    "total": len(messages.data)
                }
            else:
                # Get all conversations (grouped by conversation_id)
                conversations = self.supabase.rpc(
                    "get_user_conversations",
                    {"p_user_id": user_id, "p_limit": limit, "p_offset": offset}
                ).execute()

                return {
                    "conversations": conversations.data,
                    "total": len(conversations.data)
                }

        except Exception as e:
            logger.error(f"[UnifiedCoach] Failed to get conversation history: {e}")
            return {
                "conversations": [],
                "messages": [],
                "total": 0
            }

    async def _build_rag_context(self, user_id: str, query: str, max_tokens: int = 3000) -> str:
        """
        Build comprehensive RAG context using HYBRID SEARCH.

        Strategy:
        1. Semantic search (embedding similarity)
        2. Recency boost (recent entries weighted higher)
        3. Diversity (avoid redundant results)
        4. Re-ranking by final score

        Returns formatted context string optimized for Claude.
        """
        try:
            # Generate query embedding
            query_embedding = await self.embedding_service.embed_text(query)
            embedding_list = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else query_embedding

            # SEARCH MULTIPLE SOURCES (get more candidates for re-ranking)
            quick_entries = await self.supabase.rpc(
                "search_quick_entry_embeddings",
                {
                    "query_embedding": embedding_list,
                    "user_id_filter": user_id,
                    "match_threshold": 0.5,  # Lower threshold to get more candidates
                    "match_count": 20  # Get 20 candidates, then re-rank
                }
            ).execute()

            # Also get RECENT entries for temporal context
            recent_entries = await self.supabase.table("quick_entry_logs")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("logged_at", desc=True)\
                .limit(10)\
                .execute()

            # HYBRID SCORING: Combine similarity + recency + diversity
            scored_results = []

            if quick_entries.data:
                for entry in quick_entries.data:
                    similarity_score = entry.get('similarity', 0.7)  # From pgvector
                    recency_score = self._calculate_recency_score(
                        entry.get('logged_at') or entry.get('created_at')
                    )
                    diversity_score = self._calculate_diversity_score(entry, scored_results)

                    final_score = (
                        similarity_score * 0.5 +      # 50% similarity
                        recency_score * 0.3 +         # 30% recency
                        diversity_score * 0.2         # 20% diversity
                    )

                    scored_results.append({
                        "entry": entry,
                        "score": final_score,
                        "similarity": similarity_score,
                        "recency": recency_score,
                        "source": "quick_entry"
                    })

            # Sort by score and take top 10
            scored_results.sort(key=lambda x: x['score'], reverse=True)
            top_results = scored_results[:10]

            # BUILD CONTEXT STRING with source attribution
            context_parts = []
            context_parts.append("=== USER'S RELEVANT DATA ===\n")

            for i, result in enumerate(top_results, 1):
                entry = result['entry']
                classification = entry.get('source_classification', 'entry')
                summary = entry.get('content_summary', entry.get('content_text', '')[:150])
                logged_at = entry.get('logged_at', entry.get('created_at'))

                context_parts.append(
                    f"{i}. [{classification.upper()} - {self._format_relative_time(logged_at)}]\n"
                    f"   {summary}\n"
                )

            # Add recent activity summary (always include for temporal context)
            if recent_entries.data:
                context_parts.append("\n=== RECENT ACTIVITY (Last 7 Days) ===")
                context_parts.append(self._summarize_recent_activity(recent_entries.data))

            full_context = "\n".join(context_parts)

            # Truncate to max_tokens if needed (rough estimate: 4 chars = 1 token)
            max_chars = max_tokens * 4
            if len(full_context) > max_chars:
                full_context = full_context[:max_chars] + "\n\n[Context truncated due to length]"

            if not top_results:
                return "No previous user data available."

            return full_context

        except Exception as e:
            logger.error(f"[UnifiedCoach] RAG context building failed: {e}", exc_info=True)
            return "Unable to retrieve user history."

    def _calculate_recency_score(self, timestamp: str) -> float:
        """
        Calculate recency score (1.0 for today, decays to 0.1 for 30+ days ago).
        Uses exponential decay with 3-day half-life.
        """
        if not timestamp:
            return 0.1

        try:
            now = datetime.utcnow()
            entry_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00').replace('+00:00', ''))
            days_ago = (now - entry_time).total_seconds() / 86400

            # Exponential decay with 3-day half-life
            return max(0.1, 1.0 / (1 + days_ago / 3))
        except Exception as e:
            logger.warning(f"Failed to calculate recency score: {e}")
            return 0.5

    def _calculate_diversity_score(self, entry: dict, existing_results: list) -> float:
        """
        Penalize entries that are too similar to already-selected results.
        Promotes variety in RAG context.
        """
        if not existing_results:
            return 1.0

        entry_type = entry.get('source_classification', 'unknown')

        # Count how many existing results share this type
        same_type_count = sum(
            1 for r in existing_results
            if r['entry'].get('source_classification') == entry_type
        )

        # Penalize if we already have 3+ of this type
        if same_type_count >= 3:
            return 0.3
        elif same_type_count >= 2:
            return 0.6
        else:
            return 1.0

    def _format_relative_time(self, timestamp: str) -> str:
        """Format timestamp as relative time (e.g., '2 hours ago', 'yesterday')."""
        if not timestamp:
            return "unknown time"

        try:
            now = datetime.utcnow()
            entry_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00').replace('+00:00', ''))
            delta = now - entry_time

            if delta.days == 0:
                hours = delta.seconds // 3600
                if hours == 0:
                    minutes = delta.seconds // 60
                    return f"{minutes}min ago" if minutes > 0 else "just now"
                return f"{hours}h ago"
            elif delta.days == 1:
                return "yesterday"
            elif delta.days < 7:
                return f"{delta.days}d ago"
            else:
                return f"{delta.days // 7}w ago"
        except Exception as e:
            logger.warning(f"Failed to format relative time: {e}")
            return "recently"

    def _summarize_recent_activity(self, entries: list) -> str:
        """Generate quick summary of recent activity by type."""
        if not entries:
            return "No activity logged in past 7 days."

        by_type = {}
        for entry in entries:
            entry_type = entry.get('source_classification', 'other')
            by_type.setdefault(entry_type, []).append(entry)

        summary_parts = []
        for entry_type, items in by_type.items():
            summary_parts.append(f"- {len(items)} {entry_type}(s)")

        return "\n".join(summary_parts)

    async def _create_conversation(self, user_id: str) -> str:
        """
        Create a new conversation in coach_conversations table.

        Returns:
            conversation_id (UUID string)
        """
        conversation_data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "title": None,  # Will be set after first AI response
            "message_count": 0,
            "archived": False,
            "last_message_at": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.supabase.table("coach_conversations").insert(conversation_data).execute()
        conversation_id = result.data[0]["id"]

        logger.info(f"[UnifiedCoach] Created new conversation: {conversation_id}")
        return conversation_id

    async def _save_user_message(
        self,
        user_id: str,
        conversation_id: str,
        content: str,
        image_base64: Optional[str] = None,
        audio_base64: Optional[str] = None
    ) -> str:
        """Save user message to coach_messages table."""
        message_data = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "role": "user",
            "content": content,
            "message_type": "chat",  # Default, may be updated to log_preview
            "metadata": {
                "has_image": image_base64 is not None,
                "has_audio": audio_base64 is not None
            },
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.supabase.table("coach_messages").insert(message_data).execute()
        return result.data[0]["id"]

    async def _save_ai_message(
        self,
        user_id: str,
        conversation_id: str,
        content: str,
        tokens_used: int,
        cost_usd: float,
        context_used: Dict[str, Any]
    ) -> str:
        """Save AI response to coach_messages table."""
        message_data = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": content,
            "message_type": "chat",
            "tokens_used": tokens_used,
            "cost_usd": cost_usd,
            "context_used": context_used,
            "ai_provider": "anthropic",
            "ai_model": "claude-3-5-sonnet-20241022",
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.supabase.table("coach_messages").insert(message_data).execute()
        return result.data[0]["id"]

    async def _save_system_message(
        self,
        user_id: str,
        conversation_id: str,
        content: str
    ) -> str:
        """Save system message (e.g., log confirmation) to coach_messages table."""
        message_data = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "role": "system",
            "content": content,
            "message_type": "system",
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.supabase.table("coach_messages").insert(message_data).execute()
        return result.data[0]["id"]

    async def _vectorize_message(
        self,
        user_id: str,
        message_id: str,
        content: str,
        role: str
    ):
        """
        Vectorize message for RAG (both user and AI messages).

        Stores in a new coach_message_embeddings table.
        """
        try:
            # Generate embedding
            embedding = await self.embedding_service.embed_text(content)

            # Store in coach_message_embeddings
            embedding_data = {
                "message_id": message_id,
                "user_id": user_id,
                "role": role,
                "embedding": embedding.tolist() if hasattr(embedding, 'tolist') else embedding,
                "content_text": content[:5000],
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "created_at": datetime.utcnow().isoformat()
            }

            self.supabase.table("coach_message_embeddings").insert(embedding_data).execute()

            # Update message with vectorization flag
            self.supabase.table("coach_messages").update({
                "is_vectorized": True
            }).eq("id", message_id).execute()

            logger.info(f"[UnifiedCoach] Vectorized {role} message: {message_id}")

        except Exception as e:
            logger.error(f"[UnifiedCoach] Vectorization failed for {message_id}: {e}")

    def _build_success_message(self, log_type: str, log_data: Dict[str, Any]) -> str:
        """Build success message for confirmed log."""
        if log_type == "meal":
            calories = log_data.get("calories", "?")
            protein = log_data.get("protein_g", "?")
            meal_name = log_data.get("meal_name", "Meal")
            return f"✅ {meal_name} logged! {calories} calories, {protein}g protein"

        elif log_type == "workout":
            workout_name = log_data.get("workout_name", "Workout")
            exercises = len(log_data.get("exercises", []))
            return f"✅ {workout_name} logged! {exercises} exercises completed"

        elif log_type == "activity":
            activity_name = log_data.get("activity_name", "Activity")
            duration = log_data.get("duration_minutes", "?")
            return f"✅ {activity_name} logged! {duration} minutes"

        elif log_type == "measurement":
            weight = log_data.get("weight_lbs", "?")
            return f"✅ Body measurement logged! Weight: {weight} lbs"

        else:
            return f"✅ {log_type} logged successfully!"

    def _calculate_claude_cost(self, input_tokens: int, output_tokens: int, cache_read_tokens: int = 0, cache_write_tokens: int = 0) -> float:
        """
        Calculate Claude 3.5 Sonnet cost with prompt caching.

        Prompt caching pricing:
        - Cache writes: $3.75/M tokens (25% more than regular input)
        - Cache reads: $0.30/M tokens (90% cheaper than regular input!)
        - Regular input: $3.00/M tokens
        - Output: $15.00/M tokens
        """
        # Regular pricing
        input_cost = (input_tokens / 1_000_000) * 3.00
        output_cost = (output_tokens / 1_000_000) * 15.00

        # Caching pricing (massive savings!)
        cache_write_cost = (cache_write_tokens / 1_000_000) * 3.75  # Slightly more to write
        cache_read_cost = (cache_read_tokens / 1_000_000) * 0.30    # 90% cheaper to read!

        total = input_cost + output_cost + cache_write_cost + cache_read_cost

        logger.debug(
            f"[Cost] Input: ${input_cost:.6f}, Output: ${output_cost:.6f}, "
            f"Cache Write: ${cache_write_cost:.6f}, Cache Read: ${cache_read_cost:.6f}, "
            f"Total: ${total:.6f}"
        )

        return total


# Global instance
_unified_coach_service: Optional[UnifiedCoachService] = None


def get_unified_coach_service() -> UnifiedCoachService:
    """Get the global UnifiedCoachService instance."""
    global _unified_coach_service
    if _unified_coach_service is None:
        _unified_coach_service = UnifiedCoachService()
    return _unified_coach_service
