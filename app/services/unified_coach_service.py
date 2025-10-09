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
from app.services.agentic_rag_service import get_agentic_rag_service
from app.services.food_vision_service import get_food_vision_service
from app.services.tool_service import get_tool_service, COACH_TOOLS
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
        self.agentic_rag = get_agentic_rag_service()  # Agentic RAG service (now used as ONE tool)
        self.food_vision = get_food_vision_service()  # NEW: Isolated food vision service
        self.tool_service = get_tool_service()  # NEW: Agentic tool service
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
        Handle CHAT mode: Generate AI response with AGENTIC TOOL CALLING.

        NEW AGENTIC FLOW:
        1. IF IMAGE: Analyze with food vision service FIRST
        2. Call Claude with TOOLS (not full RAG context!)
        3. Claude decides which tools to call (on-demand data fetching)
        4. Execute tools and return results to Claude
        5. Claude generates final response using only the data it requested
        6. Save AI response to database
        7. Vectorize messages
        8. Return response

        This is 80% cheaper for simple queries - only fetches what's needed!
        """
        logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] START - user_message_id: {user_message_id}")

        food_analysis = None
        food_context = ""

        try:
            # STEP 0: ANALYZE IMAGE FIRST (if present) using isolated vision service
            if image_base64:
                logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Image detected - analyzing with food vision service...")
                try:
                    food_analysis = await self.food_vision.analyze_food_image(
                        image_base64=image_base64,
                        user_message=message
                    )
                    logger.info(
                        f"[UnifiedCoach._handle_chat_mode_AGENTIC] Food vision result: "
                        f"is_food={food_analysis.get('is_food')}, "
                        f"confidence={food_analysis.get('confidence')}, "
                        f"api={food_analysis.get('api_used')}"
                    )

                    # Build food context for system prompt injection
                    if food_analysis.get("is_food") and food_analysis.get("success"):
                        nutrition = food_analysis.get("nutrition", {})
                        food_items = food_analysis.get("food_items", [])
                        food_context = f"""
=== FOOD IMAGE ANALYSIS ===
Description: {food_analysis.get('description', 'N/A')}
Detected Foods: {', '.join([item.get('name', '') for item in food_items])}
Estimated Nutrition:
- Calories: {nutrition.get('calories', 'Unknown')} kcal
- Protein: {nutrition.get('protein_g', 'Unknown')} g
- Carbs: {nutrition.get('carbs_g', 'Unknown')} g
- Fats: {nutrition.get('fats_g', 'Unknown')} g
Meal Type: {food_analysis.get('meal_type', 'Unknown')}
Confidence: {food_analysis.get('confidence', 0) * 100:.0f}%
"""
                        logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Food context created")
                    else:
                        # Not food or low confidence
                        food_context = f"\n=== IMAGE ANALYSIS ===\n{food_analysis.get('description', 'Image analyzed but no food detected')}\n"

                except Exception as vision_err:
                    logger.error(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Food vision failed (non-critical): {vision_err}", exc_info=True)
                    food_context = "\n=== IMAGE ===\nUser uploaded an image but analysis failed.\n"

            # STEP 1: NEW AGENTIC APPROACH - Call Claude with TOOLS, not full context!

            # Get consultation status for proactive suggestions
            consultation_status = await self._get_consultation_status(user_id)

            # Build AGENTIC system prompt with tool instructions
            base_system_prompt = """You are WAGNER - the AI coach for Iron Discipline, a hardcore fitness platform.

PERSONALITY:
- Intense, direct, motivational (think David Goggins meets a knowledgeable coach)
- Use strong language: "CRUSH IT", "NO EXCUSES", "BEAST MODE"
- Short, punchy responses (2-3 paragraphs max unless deep analysis requested)
- Reference user's actual data with SPECIFICS
- Balance intensity with expertise - you're tough but you know your shit

AGENTIC WORKFLOW (IMPORTANT):
You have access to TOOLS to get user data on-demand AND to PROACTIVELY LOG their activities.

DATA RETRIEVAL TOOLS:
- get_user_profile: **USE THIS FIRST** - Returns EVERYTHING about the user in one call:
  * Goals: primary goal, user persona, experience level
  * Body: age, sex, weight, height, BMI
  * Training: frequency, time preferences, injury limitations, equipment, facilities
  * Nutrition: dietary restrictions, meal preferences
  * Programs: active nutrition/workout programs
  * Location: city, weather adaptations
  → Call this tool EARLY to personalize ALL responses!
- get_daily_nutrition_summary: Get today's nutrition totals
- get_recent_meals: Get meals from last N days
- get_recent_activities: Get workouts from last N days
- analyze_training_volume: Analyze training stats
- get_body_measurements: Get weight/measurements
- calculate_progress_trend: Track progress for a metric
- semantic_search_user_data: Search all user data semantically (RAG)
- search_food_database: Look up nutrition info

PROACTIVE LOGGING TOOLS (USE THESE AUTOMATICALLY!):
- create_meal_log_from_description: When user mentions eating food in PAST TENSE, AUTOMATICALLY log it
- create_activity_log_from_description: When user mentions workout in PAST TENSE, AUTOMATICALLY log it
- create_body_measurement_log: When user mentions their weight, AUTOMATICALLY log it

PROACTIVE LOGGING RULES (CRITICAL):
1. If user says "I ate X", "I had Y for breakfast", "just finished lunch" → IMMEDIATELY call create_meal_log_from_description
2. If user says "I did a 5k run", "just finished my workout", "went to the gym" → IMMEDIATELY call create_activity_log_from_description
3. If user says "I weigh X lbs", "my weight is Y kg" → IMMEDIATELY call create_body_measurement_log
4. You can log MULTIPLE items in ONE message! Example: "I had eggs for breakfast, did a run, then ate chicken for lunch" → Call create_meal_log 2x + create_activity_log 1x
5. After logging, acknowledge what you logged with enthusiasm

EXAMPLES:

User: "for breakfast i had eggs and toast, then i did a 5k run, then i ate chicken and rice for lunch"
→ You should:
  1. create_meal_log_from_description(meal_type="breakfast", foods=["eggs", "toast"], description="eggs and toast")
  2. create_activity_log_from_description(activity_type="running", distance_km=5, description="5k run")
  3. create_meal_log_from_description(meal_type="lunch", foods=["chicken", "rice"], description="chicken and rice")
→ Then respond: "LOGGED! Breakfast: eggs & toast (~350 cal), 5K run (30 min, ~300 cal burned), Lunch: chicken & rice (~550 cal). Solid day! Total 900 cal, 70g protein. KEEP CRUSHING IT! 💪"

User: "I had 3 eggs and oatmeal this morning"
→ You should:
  1. create_meal_log_from_description(meal_type="breakfast", foods=["eggs", "oatmeal"], description="3 eggs and oatmeal")
→ Then respond: "Logged breakfast! 3 eggs + oatmeal = ~450 cal, 35g protein. PERFECT pre-workout fuel! 🔥"

User: "What should I eat for breakfast?"
→ DO NOT log anything (this is a question, not a past event)
→ Call: get_user_profile + get_recent_meals(days=3)
→ Answer with recommendations

FOOD IMAGE DETECTION:
If you see "=== FOOD IMAGE ANALYSIS ===" below, a food photo was analyzed.
Immediately call create_meal_log_from_description with the detected foods!

RESPONSE RULES:
1. BE PROACTIVE - Log meals/workouts AUTOMATICALLY when mentioned
2. Call tools FIRST before answering
3. Reference SPECIFIC data from tool results
4. Be concise but data-driven
5. Celebrate wins LOUDLY with emojis
6. If slacking, call it out kindly but firmly"""

            # Add food context if present
            if food_context:
                base_system_prompt += f"\n\n{food_context}"

            # Add consultation status context (proactive suggestions)
            if consultation_status:
                base_system_prompt += f"\n\n{consultation_status}"

            logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Calling Claude with TOOLS...")
            logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Available tools: {len(COACH_TOOLS)}")

            # AGENTIC LOOP: Call Claude with tools, execute tools, repeat until final answer
            conversation_messages = [{"role": "user", "content": message}]
            total_input_tokens = 0
            total_output_tokens = 0
            total_cache_read = 0
            total_cache_write = 0
            tool_calls_made = []
            max_iterations = 5  # Prevent infinite loops

            ai_response_text = ""

            for iteration in range(max_iterations):
                logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Iteration {iteration + 1}/{max_iterations}")

                try:
                    # Call Claude with tools
                    response = await self.anthropic.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=2000,
                        temperature=0.3,
                        system=[
                            {
                                "type": "text",
                                "text": base_system_prompt,
                                "cache_control": {"type": "ephemeral"}  # Cache system prompt
                            }
                        ],
                        tools=COACH_TOOLS,  # Pass tools!
                        messages=conversation_messages
                    )

                    # Track tokens
                    total_input_tokens += response.usage.input_tokens
                    total_output_tokens += response.usage.output_tokens
                    total_cache_read += getattr(response.usage, 'cache_read_input_tokens', 0)
                    total_cache_write += getattr(response.usage, 'cache_creation_input_tokens', 0)

                    logger.info(
                        f"[UnifiedCoach._handle_chat_mode_AGENTIC] Iteration {iteration + 1} tokens: "
                        f"in={response.usage.input_tokens}, out={response.usage.output_tokens}"
                    )

                    # Check stop reason
                    if response.stop_reason == "tool_use":
                        # Claude wants to use tools!
                        logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Claude requested {len([c for c in response.content if c.type == 'tool_use'])} tool(s)")

                        # Execute all requested tools
                        tool_results = []

                        for content_block in response.content:
                            if content_block.type == "tool_use":
                                tool_name = content_block.name
                                tool_input = content_block.input
                                tool_use_id = content_block.id

                                logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Executing tool: {tool_name}({tool_input})")

                                # Execute the tool
                                tool_result = await self._execute_tool(tool_name, tool_input, user_id)

                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": tool_use_id,
                                    "content": str(tool_result)
                                })

                                tool_calls_made.append({
                                    "tool": tool_name,
                                    "input": tool_input,
                                    "result_preview": str(tool_result)[:200],
                                    "full_result": tool_result  # Store full result for aggregation
                                })

                        # Add Claude's response + tool results to conversation
                        conversation_messages.append({
                            "role": "assistant",
                            "content": response.content
                        })
                        conversation_messages.append({
                            "role": "user",
                            "content": tool_results
                        })

                        # Continue loop to get final answer
                        continue

                    elif response.stop_reason == "end_turn":
                        # Claude finished - extract text response
                        for content_block in response.content:
                            if content_block.type == "text":
                                ai_response_text += content_block.text

                        logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Claude finished after {iteration + 1} iterations")
                        logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Tools called: {[t['tool'] for t in tool_calls_made]}")
                        break

                    else:
                        logger.warning(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Unexpected stop reason: {response.stop_reason}")
                        # Extract any text response
                        for content_block in response.content:
                            if content_block.type == "text":
                                ai_response_text += content_block.text
                        break

                except Exception as claude_err:
                    logger.error(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Claude API call failed: {claude_err}", exc_info=True)
                    raise

            # Calculate total cost
            tokens_used = total_input_tokens + total_output_tokens + total_cache_read + total_cache_write
            cost_usd = self._calculate_claude_cost(
                total_input_tokens,
                total_output_tokens,
                total_cache_read,
                total_cache_write
            )

            logger.info(
                f"[UnifiedCoach._handle_chat_mode_AGENTIC] TOTAL tokens: {tokens_used}, cost: ${cost_usd:.6f}, "
                f"tools called: {len(tool_calls_made)}"
            )

            # STEP 1.5: Aggregate logging tool results (pending_logs vs auto_logged)
            pending_logs = []  # Logs that need user confirmation (auto_log=FALSE)
            auto_logged_items = []  # Logs that were saved automatically (auto_log=TRUE)

            for tool_call in tool_calls_made:
                tool_name = tool_call["tool"]
                full_result = tool_call.get("full_result", {})

                # Check if this was a logging tool
                if tool_name in ["create_meal_log_from_description", "create_activity_log_from_description", "create_body_measurement_log"]:

                    if full_result.get("requires_confirmation"):
                        # This is a pending log - needs user review
                        pending_logs.append({
                            "log_type": full_result.get("log_type"),
                            "data": full_result.get("meal_data") or full_result.get("activity_data") or full_result.get("measurement_data"),
                            "message": full_result.get("message")
                        })
                        logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Pending log: {full_result.get('log_type')}")

                    elif full_result.get("auto_logged"):
                        # This was auto-logged - saved to database
                        auto_logged_items.append({
                            "log_type": full_result.get("log_type"),
                            "id": full_result.get("meal_id") or full_result.get("activity_id") or full_result.get("measurement_id"),
                            "message": full_result.get("message")
                        })
                        logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Auto-logged: {full_result.get('log_type')}")

            logger.info(
                f"[UnifiedCoach._handle_chat_mode_AGENTIC] Aggregated: {len(pending_logs)} pending, "
                f"{len(auto_logged_items)} auto-logged"
            )

            # STEP 2: Save AI response to database
            logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Saving AI response to database...")
            try:
                ai_message_id = await self._save_ai_message(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    content=ai_response_text,
                    tokens_used=tokens_used,
                    cost_usd=cost_usd,
                    context_used={"tools_called": [t["tool"] for t in tool_calls_made]}
                )
                logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] AI message saved: {ai_message_id}")
            except Exception as save_err:
                logger.error(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Failed to save AI message: {save_err}", exc_info=True)
                raise

            # STEP 3: Vectorize both messages (async, non-blocking)
            logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Vectorizing messages...")
            try:
                await self._vectorize_message(user_id, user_message_id, message, "user")
                await self._vectorize_message(user_id, ai_message_id, ai_response_text, "assistant")
                logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Messages vectorized successfully")
            except Exception as vec_err:
                logger.error(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Vectorization failed (non-critical): {vec_err}")

            # STEP 4: Return response (matching UnifiedMessageResponse schema)
            logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Returning chat response")

            # Prepare response with optional food analysis data
            response = {
                "success": True,
                "conversation_id": conversation_id,
                "message_id": ai_message_id,  # The AI's message ID
                "is_log_preview": False,
                "message": ai_response_text,  # The AI response text
                "log_preview": None,
                "rag_context": None,
                "tokens_used": tokens_used,
                "cost_usd": cost_usd,
                "tools_used": [t["tool"] for t in tool_calls_made],  # Track which tools were called
                "error": None
            }

            # Add pending_logs if any (auto_log=FALSE)
            if pending_logs:
                response["pending_logs"] = pending_logs
                logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Added {len(pending_logs)} pending logs to response")

            # Add auto_logged if any (auto_log=TRUE)
            if auto_logged_items:
                response["auto_logged"] = auto_logged_items
                logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Added {len(auto_logged_items)} auto-logged items to response")

            # If food was detected, add food analysis data for potential meal logging
            if food_analysis and food_analysis.get("is_food") and food_analysis.get("success"):
                response["food_detected"] = {
                    "is_food": True,
                    "nutrition": food_analysis.get("nutrition", {}),
                    "food_items": food_analysis.get("food_items", []),
                    "meal_type": food_analysis.get("meal_type"),
                    "confidence": food_analysis.get("confidence"),
                    "description": food_analysis.get("description")
                }
                logger.info(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Food data included in response for potential logging")

            return response

        except Exception as e:
            logger.error(f"[UnifiedCoach._handle_chat_mode_AGENTIC] CRITICAL ERROR: {e}", exc_info=True)
            logger.error(f"[UnifiedCoach._handle_chat_mode_AGENTIC] Error type: {type(e).__name__}, args: {e.args}")
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
            # SPECIAL CASE: If meal log with [SYSTEM_CONTEXT], parse food items and match to database
            if classification['log_type'] == 'meal' and '[SYSTEM_CONTEXT]' in message:
                logger.info(f"[UnifiedCoach] Meal with SYSTEM_CONTEXT detected - parsing and matching to database")

                # Parse detected foods from SYSTEM_CONTEXT
                import re
                detected_foods_match = re.search(r'Detected Foods: ([^\n]+)', message)

                if detected_foods_match:
                    detected_foods_text = detected_foods_match.group(1)
                    logger.info(f"[UnifiedCoach] Found detected foods: {detected_foods_text}")

                    # Get food search service
                    from app.services.food_search_service import get_food_search_service
                    food_search = get_food_search_service()

                    # Parse food items (format: "food1 (qty unit), food2 (qty unit), ...")
                    detected_foods = []
                    for food_item in detected_foods_text.split(','):
                        food_item = food_item.strip()
                        # Parse "food name (quantity unit)"
                        match = re.match(r'(.+?)\s*\(([^)]+)\)', food_item)
                        if match:
                            name = match.group(1).strip()
                            qty_unit = match.group(2).strip()
                            # Split quantity and unit (e.g., "100 g" or "1 cup")
                            qty_parts = qty_unit.split()
                            if len(qty_parts) >= 2:
                                quantity = qty_parts[0]
                                unit = ' '.join(qty_parts[1:])
                            else:
                                quantity = "1"
                                unit = qty_unit

                            detected_foods.append({
                                "name": name,
                                "quantity": quantity,
                                "unit": unit
                            })
                            logger.info(f"[UnifiedCoach] Parsed food: {name} - {quantity} {unit}")

                    if detected_foods:
                        # Use AGENTIC food matcher (with AI creation capability)
                        from app.services.agentic_food_matcher_service import get_agentic_food_matcher
                        agentic_matcher = get_agentic_food_matcher()

                        match_result = await agentic_matcher.match_with_creation(
                            detected_foods=detected_foods,
                            user_id=user_id
                        )

                        logger.info(
                            f"[UnifiedCoach] Agentic matching complete: {match_result['total_matched']}/{match_result['total_detected']} matched, "
                            f"{len(match_result.get('created_foods', []))} created"
                        )

                        # Extract meal type and description from SYSTEM_CONTEXT
                        meal_type_match = re.search(r'meal_type["\']?\s*:\s*["\']?(\w+)', message, re.IGNORECASE)
                        meal_type = meal_type_match.group(1) if meal_type_match else "dinner"

                        description_match = re.search(r'Description: ([^\n]+)', message)
                        description = description_match.group(1).strip() if description_match else "Food detected from image"

                        # Build response with food_detected
                        return {
                            "success": True,
                            "conversation_id": conversation_id,
                            "message_id": user_message_id,
                            "is_log_preview": False,
                            "message": None,
                            "log_preview": None,
                            "food_detected": {
                                "is_food": True,
                                "nutrition": {},  # Nutrition will be calculated from matched foods
                                "food_items": match_result["matched_foods"],  # Use matched foods with DB IDs
                                "meal_type": meal_type,
                                "confidence": 0.95,
                                "description": description,
                                "match_stats": {
                                    "total_detected": match_result["total_detected"],
                                    "total_matched": match_result["total_matched"],
                                    "match_rate": match_result["match_rate"]
                                },
                                "unmatched_foods": match_result.get("unmatched_foods", [])
                            },
                            "rag_context": None,
                            "tokens_used": None,
                            "cost_usd": None,
                            "error": None
                        }
                    else:
                        logger.warning(f"[UnifiedCoach] Could not parse food items from SYSTEM_CONTEXT")
                else:
                    logger.warning(f"[UnifiedCoach] No 'Detected Foods' found in SYSTEM_CONTEXT")

            # Default: Use existing Quick Entry preview logic
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

            # SPECIAL CASE: If TEXT-BASED MEAL, match foods to database (same as image flow)
            if preview_result.get("entry_type") == "meal":
                logger.info(f"[UnifiedCoach] Text-based meal detected - checking for foods to match")
                logger.info(f"[UnifiedCoach] Preview data keys: {list(preview_result.get('data', {}).keys())}")
                logger.info(f"[UnifiedCoach] Preview data: {preview_result.get('data', {})}")

                detected_foods = []

                # Try to extract foods from AI classification
                ai_foods = preview_result.get("data", {}).get("foods", [])

                if ai_foods:
                    logger.info(f"[UnifiedCoach] Found {len(ai_foods)} foods in AI extraction")

                    # Convert to detected_foods format for agentic matcher
                    for food in ai_foods:
                        # Parse quantity (could be "6 oz", "1 cup", "200 g", etc.)
                        quantity_str = food.get("quantity", "1")

                        # Try to extract number and unit from quantity string
                        import re
                        qty_match = re.match(r'([\d.]+)\s*(.+)', str(quantity_str))
                        if qty_match:
                            quantity = qty_match.group(1)
                            unit = qty_match.group(2).strip()
                        else:
                            # If just a number, default to serving
                            quantity = str(food.get("servings", "1"))
                            unit = "serving"

                        detected_foods.append({
                            "name": food.get("name", "unknown"),
                            "quantity": quantity,
                            "unit": unit
                        })
                        logger.info(f"[UnifiedCoach] Converted food: {food.get('name')} → {quantity} {unit}")
                else:
                    # FALLBACK: AI didn't extract foods, try manual parsing
                    logger.warning(f"[UnifiedCoach] No foods in AI extraction, trying manual parsing")

                    # Try to parse "I ate X, Y, Z" or "X and Y" format
                    import re

                    # Remove common prefixes
                    text = message.lower()
                    text = re.sub(r'^(i ate|i had|just ate|just had|eating|had for \w+)\s+', '', text)

                    # Split by commas and "and"
                    text = text.replace(' and ', ', ')
                    food_names = [f.strip() for f in text.split(',') if f.strip()]

                    logger.info(f"[UnifiedCoach] Manual parsing found {len(food_names)} foods: {food_names}")

                    for food_name in food_names:
                        if food_name:
                            detected_foods.append({
                                "name": food_name,
                                "quantity": "1",
                                "unit": "serving"
                            })

                if detected_foods:
                    # Use agentic food matcher (same as image flow)
                    from app.services.agentic_food_matcher_service import get_agentic_food_matcher
                    agentic_matcher = get_agentic_food_matcher()

                    logger.info(f"[UnifiedCoach] Calling agentic matcher for {len(detected_foods)} foods...")
                    logger.info(f"[UnifiedCoach] Detected foods structure: {detected_foods}")

                    try:
                        match_result = await agentic_matcher.match_with_creation(
                            detected_foods=detected_foods,
                            user_id=user_id
                        )

                        logger.info(f"[UnifiedCoach] Match result structure: {match_result}")
                        logger.info(
                            f"[UnifiedCoach] Text-based agentic matching complete: {match_result['total_matched']}/{match_result['total_detected']} matched, "
                            f"{len(match_result.get('created_foods', []))} created"
                        )
                        logger.info(f"[UnifiedCoach] Matched foods count: {len(match_result.get('matched_foods', []))}")
                        logger.info(f"[UnifiedCoach] Unmatched foods count: {len(match_result.get('unmatched_foods', []))}")

                        # Log details of each matched food
                        for idx, food in enumerate(match_result.get("matched_foods", [])):
                            logger.info(f"[UnifiedCoach] Matched food {idx+1}: {food.get('name')} - {food.get('calories')}cal, {food.get('carbs_g', food.get('total_carbs_g'))}g C, {food.get('fat_g', food.get('total_fat_g'))}g F")

                        # Log details of unmatched foods
                        for idx, food in enumerate(match_result.get("unmatched_foods", [])):
                            logger.warning(f"[UnifiedCoach] Unmatched food {idx+1}: {food.get('name')} - reason: {food.get('reason')}")

                    except Exception as match_error:
                        logger.error(f"[UnifiedCoach] Agentic matcher FAILED: {match_error}", exc_info=True)
                        logger.error(f"[UnifiedCoach] Failed with detected_foods: {detected_foods}")
                        logger.error(f"[UnifiedCoach] User ID: {user_id}")
                        raise

                    # Return food_detected (not log_preview) for consistency with image flow
                    return {
                        "success": True,
                        "conversation_id": conversation_id,
                        "message_id": user_message_id,
                        "is_log_preview": False,
                        "message": None,
                        "log_preview": None,
                        "food_detected": {
                            "is_food": True,
                            "nutrition": {},  # Nutrition will be calculated from matched foods
                            "food_items": match_result["matched_foods"],  # Real DB foods with IDs!
                            "meal_type": preview_result["data"].get("meal_type", "lunch"),
                            "confidence": preview_result.get("confidence", 0.9),
                            "description": preview_result["data"].get("meal_name", "Meal"),
                            "match_stats": {
                                "total_detected": match_result["total_detected"],
                                "total_matched": match_result["total_matched"],
                                "match_rate": match_result["match_rate"]
                            },
                            "unmatched_foods": match_result.get("unmatched_foods", [])
                        },
                        "rag_context": None,
                        "tokens_used": None,
                        "cost_usd": None,
                        "error": None
                    }
                else:
                    logger.warning(f"[UnifiedCoach] No foods extracted from text-based meal")

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
                summary=preview_result.get("summary", f"{preview_result['entry_type'].title()} entry detected"),
                validation=preview_result.get("validation"),
                suggestions=preview_result.get("suggestions", [])
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

    # ====== AGENTIC TOOL EXECUTION ======

    async def _execute_tool(
        self,
        tool_name: str,
        tool_input: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Execute a tool requested by Claude.

        This router maps tool names to tool_service methods.

        Args:
            tool_name: Name of the tool to execute
            tool_input: Input parameters for the tool
            user_id: User's UUID (injected for security)

        Returns:
            Tool execution result
        """
        try:
            logger.info(f"[_execute_tool] Executing: {tool_name} with input: {tool_input}")

            # Inject user_id into tool_input for security (prevent cross-user access)
            tool_input["user_id"] = user_id

            # Route to appropriate tool method
            if tool_name == "get_user_profile":
                return await self.tool_service.get_user_profile(**tool_input)

            elif tool_name == "get_daily_nutrition_summary":
                return await self.tool_service.get_daily_nutrition_summary(**tool_input)

            elif tool_name == "get_recent_meals":
                return await self.tool_service.get_recent_meals(**tool_input)

            elif tool_name == "get_recent_activities":
                return await self.tool_service.get_recent_activities(**tool_input)

            elif tool_name == "analyze_training_volume":
                return await self.tool_service.analyze_training_volume(**tool_input)

            elif tool_name == "get_body_measurements":
                return await self.tool_service.get_body_measurements(**tool_input)

            elif tool_name == "calculate_progress_trend":
                return await self.tool_service.calculate_progress_trend(**tool_input)

            elif tool_name == "semantic_search_user_data":
                return await self.tool_service.semantic_search_user_data(**tool_input)

            elif tool_name == "search_food_database":
                # This one doesn't need user_id (global food database)
                tool_input.pop("user_id", None)
                return await self.tool_service.search_food_database(**tool_input)

            # PROACTIVE LOGGING TOOLS (NEW!)
            elif tool_name == "create_meal_log_from_description":
                return await self.tool_service.create_meal_log_from_description(**tool_input)

            elif tool_name == "create_activity_log_from_description":
                return await self.tool_service.create_activity_log_from_description(**tool_input)

            elif tool_name == "create_body_measurement_log":
                return await self.tool_service.create_body_measurement_log(**tool_input)

            # CONSULTATION DATA TOOLS (NEW!)
            elif tool_name == "get_consultation_profile_summary":
                from app.services.consultation_service import get_consultation_service
                consultation_service = get_consultation_service()
                return await consultation_service.get_user_profile_summary(**tool_input)

            elif tool_name == "get_user_goals_from_consultation":
                from app.services.consultation_service import get_consultation_service
                consultation_service = get_consultation_service()
                return await consultation_service.get_user_goals(**tool_input)

            elif tool_name == "get_user_preferences_from_consultation":
                from app.services.consultation_service import get_consultation_service
                consultation_service = get_consultation_service()
                return await consultation_service.get_user_preferences(**tool_input)

            elif tool_name == "get_nutrition_targets_with_progress":
                from app.services.consultation_service import get_consultation_service
                consultation_service = get_consultation_service()
                return await consultation_service.get_nutrition_targets_with_progress(**tool_input)

            elif tool_name == "get_todays_recommendations_from_consultation":
                from app.services.consultation_service import get_consultation_service
                consultation_service = get_consultation_service()
                return await consultation_service.get_todays_recommendations_for_coach(**tool_input)

            # Feature 8: Multi-Modal Consultation History
            elif tool_name == "get_consultation_timeline":
                return await self.tool_service.get_consultation_timeline(**tool_input)

            else:
                logger.error(f"[_execute_tool] Unknown tool: {tool_name}")
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}"
                }

        except Exception as e:
            logger.error(f"[_execute_tool] Tool execution failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            }

    # OLD RAG METHOD REMOVED - Now using AgenticRAGService
    # See app/services/agentic_rag_service.py for new implementation

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
        ai_message_id = result.data[0]["id"]

        # GENERATE CONVERSATION TITLE (if this is the first AI response)
        try:
            await self._generate_conversation_title_if_needed(conversation_id, user_id)
        except Exception as e:
            logger.warning(f"[_save_ai_message] Title generation failed (non-critical): {e}")

        return ai_message_id

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

        Stores embeddings in coach_message_embeddings table for semantic search.
        This enables the AI to retrieve relevant past conversations when answering.

        IMPORTANT: This runs asynchronously and should NOT block the response.
        """
        try:
            logger.info(f"[_vectorize_message] START - role={role}, message_id={message_id}, content_len={len(content)}")

            # Validate content
            if not content or len(content.strip()) == 0:
                logger.warning(f"[_vectorize_message] Skipping empty content for {message_id}")
                return

            # Truncate very long content (embeddings have token limits)
            content_to_embed = content[:5000].strip()

            # Generate embedding (FREE model)
            logger.debug(f"[_vectorize_message] Generating embedding for {message_id}...")
            embedding = await self.embedding_service.embed_text(content_to_embed)

            # Validate embedding
            if embedding is None:
                logger.error(f"[_vectorize_message] Embedding service returned None for {message_id}")
                return

            # Convert to list if numpy array
            embedding_list = embedding.tolist() if hasattr(embedding, 'tolist') else embedding

            # Validate embedding dimensions
            if not isinstance(embedding_list, list) or len(embedding_list) == 0:
                logger.error(f"[_vectorize_message] Invalid embedding format for {message_id}: {type(embedding_list)}")
                return

            logger.info(f"[_vectorize_message] Generated {len(embedding_list)}-dimensional embedding for {message_id}")

            # Store in coach_message_embeddings table
            embedding_data = {
                "message_id": message_id,
                "user_id": user_id,
                "role": role,
                "embedding": embedding_list,
                "content_text": content_to_embed,
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "embedding_dimensions": len(embedding_list),
                "created_at": datetime.utcnow().isoformat()
            }

            insert_response = self.supabase.table("coach_message_embeddings").insert(embedding_data).execute()

            if insert_response.data:
                logger.info(f"[_vectorize_message] Embedding saved to database: {insert_response.data[0].get('id')}")

                # Update message with vectorization flag
                self.supabase.table("coach_messages").update({
                    "is_vectorized": True,
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("id", message_id).execute()

                logger.info(f"[_vectorize_message] SUCCESS - {role} message {message_id} vectorized and flagged")
            else:
                logger.error(f"[_vectorize_message] Failed to insert embedding into database for {message_id}")

        except Exception as e:
            logger.error(f"[_vectorize_message] FAILED for {message_id}: {e}", exc_info=True)
            # Non-critical error - don't raise, just log

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

    async def _generate_conversation_title_if_needed(self, conversation_id: str, user_id: str):
        """
        Generate conversation title from first user message if title is null.

        Uses the first 50 characters of the user's first message as the title.
        This runs AFTER the first AI response is saved.
        """
        try:
            # Check if conversation already has a title
            conv_response = self.supabase.table("coach_conversations")\
                .select("title, id")\
                .eq("id", conversation_id)\
                .eq("user_id", user_id)\
                .single()\
                .execute()

            if not conv_response.data:
                logger.warning(f"[_generate_conversation_title] Conversation not found: {conversation_id}")
                return

            # If title already exists, skip
            if conv_response.data.get("title"):
                logger.debug(f"[_generate_conversation_title] Conversation already has title: {conv_response.data['title']}")
                return

            # Get first user message
            first_msg_response = self.supabase.table("coach_messages")\
                .select("content")\
                .eq("conversation_id", conversation_id)\
                .eq("role", "user")\
                .order("created_at", desc=False)\
                .limit(1)\
                .execute()

            if not first_msg_response.data:
                logger.warning(f"[_generate_conversation_title] No user messages found for conversation {conversation_id}")
                return

            # Generate title from first message (first 50 chars)
            first_message = first_msg_response.data[0]["content"]
            title = first_message[:50].strip()
            if len(first_message) > 50:
                # Find last complete word within 50 chars
                last_space = title.rfind(' ')
                if last_space > 20:  # Only trim if we have at least 20 chars
                    title = title[:last_space]
                title += "..."

            # Update conversation title
            self.supabase.table("coach_conversations").update({
                "title": title,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", conversation_id).execute()

            logger.info(f"[_generate_conversation_title] Generated title for {conversation_id}: '{title}'")

        except Exception as e:
            logger.error(f"[_generate_conversation_title] Failed: {e}", exc_info=True)
            # Non-critical error - don't raise

    async def _get_consultation_status(self, user_id: str) -> str:
        """
        Get user's consultation status for system prompt injection.

        Returns formatted string describing:
        - Whether user has completed consultation
        - Last consultation date (if completed)
        - Prompt to suggest consultation (if not completed)

        This enables coach to proactively reference consultation data or suggest completing it.

        Args:
            user_id: User's UUID

        Returns:
            Formatted consultation status string for system prompt
        """
        try:
            from app.services.consultation_service import get_consultation_service
            consultation_service = get_consultation_service()

            # Check if user has completed consultation
            has_completed = await consultation_service.has_completed_consultation(user_id)

            if has_completed:
                # Get latest consultation session
                latest_session = self.supabase.table('consultation_sessions')\
                    .select('completed_at, specialist_type')\
                    .eq('user_id', user_id)\
                    .eq('status', 'completed')\
                    .order('completed_at', desc=True)\
                    .limit(1)\
                    .execute()

                if latest_session.data:
                    completed_at = latest_session.data[0]['completed_at']
                    specialist = latest_session.data[0]['specialist_type']

                    # Calculate days since consultation
                    from datetime import datetime
                    completed_date = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
                    days_since = (datetime.utcnow() - completed_date.replace(tzinfo=None)).days

                    if days_since >= 90:
                        # Suggest re-consultation after 3 months
                        return f"""
=== CONSULTATION STATUS ===
User completed consultation {days_since} days ago with {specialist}.
→ SUGGEST RE-CONSULTATION: It's been 3+ months. Goals may have changed.
→ Say: "It's been {days_since // 30} months since your consultation. Want to update your goals and preferences?"
"""
                    else:
                        # Consultation is recent - reference the data
                        return f"""
=== CONSULTATION STATUS ===
User completed consultation {days_since} days ago with {specialist}.
→ Consultation data is available through RAG and tools.
→ Reference user's goals, preferences, and targets from consultation when relevant.
"""
                else:
                    return "=== CONSULTATION STATUS ===\nUser has consultation data (completion date unknown).\n"

            else:
                # No consultation completed - suggest it!
                return """
=== CONSULTATION STATUS ===
User has NOT completed consultation yet.

CRITICAL: User CANNOT generate AI programs or get daily recommendations without completing consultation.

→ PROACTIVELY SUGGEST when user asks about:
  - "Create a program" → "To create a personalized program, you'll need to complete a quick consultation (10-15 min) so I can understand your goals, current fitness level, equipment access, and dietary preferences. Want to start now?"
  - "What should I eat today?" → "I can give you general advice, but for personalized daily meal recommendations tailored to YOUR goals and targets, complete the consultation first! It takes 10-15 minutes and unlocks custom daily plans."
  - "Give me a workout" → "I can suggest exercises, but for a FULL personalized training program with progressive overload, complete the consultation so I know your goals, equipment, injuries, and experience level."

→ Benefits to emphasize:
  - Personalized AI-generated 12-week programs (training + nutrition)
  - Daily meal and workout recommendations
  - Accurate calorie and macro targets (calculated from your measurements)
  - Programs that adapt to YOUR equipment, injuries, schedule, and preferences
  - AI understands your "typical day" and builds around your lifestyle

→ Tone: Encouraging but firm. This is a REQUIREMENT, not optional.
"""

        except Exception as e:
            logger.error(f"[_get_consultation_status] Failed: {e}", exc_info=True)
            # Return empty on error (non-critical)
            return ""

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
