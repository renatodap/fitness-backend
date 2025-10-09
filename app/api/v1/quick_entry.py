"""
Quick Entry API - Ultra-Optimized Multimodal Input

Handles text, voice, images, PDFs with FREE models
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
import logging
import base64

from app.services.quick_entry_service import get_quick_entry_service
from app.services.auth_service import get_current_user
from app.api.middleware.rate_limit import quick_entry_rate_limit

router = APIRouter(prefix="/quick-entry", tags=["quick-entry"])
logger = logging.getLogger(__name__)


class QuickEntryTextRequest(BaseModel):
    """Text-only quick entry request"""
    text: str
    metadata: Optional[dict] = None


class QuickEntryResponse(BaseModel):
    """Quick entry response"""
    success: bool
    entry_type: str
    confidence: float
    data: dict
    entry_id: Optional[str] = None
    suggestions: list[str] = []
    extracted_text: Optional[str] = None
    error: Optional[str] = None


@router.post("/text", response_model=QuickEntryResponse)
@quick_entry_rate_limit()
async def quick_entry_text(
    request: QuickEntryTextRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Process text-only quick entry.

    OPTIMIZED: Uses FREE DeepSeek V3 or Llama-4 Scout
    """
    service = get_quick_entry_service()

    try:
        result = await service.process_entry(
            user_id=current_user["id"],
            text=request.text,
            metadata=request.metadata
        )

        return QuickEntryResponse(**result)

    except Exception as e:
        logger.error(f"Quick entry text processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/multimodal", response_model=QuickEntryResponse)
@quick_entry_rate_limit()
async def quick_entry_multimodal(
    text: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),  # User feelings/notes
    manual_type: Optional[str] = Form(None),  # Manual type override (meal, activity, workout, note)
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
    pdf: Optional[UploadFile] = File(None),
    metadata: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Process multimodal quick entry (text + image + audio + PDF).

    OPTIMIZED:
    - Images: FREE Meta Llama-4 Scout or Yi-Vision
    - Audio: Speech-to-text (Whisper or similar)
    - PDF: OCR/text extraction
    - Text: FREE DeepSeek V3

    Handles ALL combinations of inputs.
    """
    service = get_quick_entry_service()

    try:
        # Convert uploads to base64
        image_base64 = None
        audio_base64 = None
        pdf_base64 = None

        if image:
            image_bytes = await image.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            logger.info(f"Image received: {len(image_bytes)} bytes")

        if audio:
            audio_bytes = await audio.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            logger.info(f"Audio received: {len(audio_bytes)} bytes")

        if pdf:
            pdf_bytes = await pdf.read()
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            logger.info(f"PDF received: {len(pdf_bytes)} bytes")

        # Parse metadata
        import json
        parsed_metadata = json.loads(metadata) if metadata else {}

        # Add notes and manual_type to metadata if provided
        if notes:
            parsed_metadata['notes'] = notes
        if manual_type:
            parsed_metadata['manual_type'] = manual_type

        # Process entry
        result = await service.process_entry(
            user_id=current_user["id"],
            text=text,
            image_base64=image_base64,
            audio_base64=audio_base64,
            pdf_base64=pdf_base64,
            metadata=parsed_metadata
        )

        return QuickEntryResponse(**result)

    except Exception as e:
        logger.error(f"Quick entry multimodal processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image", response_model=QuickEntryResponse)
async def quick_entry_image(
    image: UploadFile = File(...),
    caption: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Process image-only quick entry (food photo, workout screenshot, etc.).

    OPTIMIZED: Uses FREE Meta Llama-4 Scout (512k context, vision support)
    """
    service = get_quick_entry_service()

    try:
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        result = await service.process_entry(
            user_id=current_user["id"],
            text=caption,
            image_base64=image_base64
        )

        return QuickEntryResponse(**result)

    except Exception as e:
        logger.error(f"Quick entry image processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preview", response_model=QuickEntryResponse)
async def quick_entry_preview(
    text: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    manual_type: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
    pdf: Optional[UploadFile] = File(None),
    metadata: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Preview quick entry - process and classify WITHOUT saving to database.

    This endpoint:
    1. Extracts text from all inputs (text, image, audio, pdf)
    2. Classifies entry type and extracts structured data via LLM
    3. Returns classification for user confirmation
    4. Does NOT save to database or vectorize

    User must call /confirm endpoint to actually save.
    """
    logger.info("=" * 80)
    logger.info("[API] 🚀 QUICK ENTRY PREVIEW REQUEST")
    logger.info(f"[API] User ID: {current_user.get('id')}")
    logger.info(f"[API] User email: {current_user.get('email')}")
    logger.info(f"[API] Text input: '{text[:100] if text else 'None'}...'")
    logger.info(f"[API] Notes: '{notes[:50] if notes else 'None'}'")
    logger.info(f"[API] Manual type: {manual_type}")
    logger.info(f"[API] Has image: {image is not None}")
    logger.info(f"[API] Has audio: {audio is not None}")
    logger.info(f"[API] Has PDF: {pdf is not None}")
    logger.info("=" * 80)

    service = get_quick_entry_service()

    try:
        # Convert uploads to base64
        image_base64 = None
        audio_base64 = None
        pdf_base64 = None

        if image:
            image_bytes = await image.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            logger.info(f"Image received: {len(image_bytes)} bytes")

        if audio:
            audio_bytes = await audio.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            logger.info(f"Audio received: {len(audio_bytes)} bytes")

        if pdf:
            pdf_bytes = await pdf.read()
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            logger.info(f"PDF received: {len(pdf_bytes)} bytes")

        # Parse metadata
        import json
        parsed_metadata = json.loads(metadata) if metadata else {}

        if notes:
            parsed_metadata['notes'] = notes
        if manual_type:
            parsed_metadata['manual_type'] = manual_type

        # Process entry WITHOUT saving (preview only)
        logger.info("[API] ⚙️  Calling service.process_entry_preview()...")
        result = await service.process_entry_preview(
            user_id=current_user["id"],
            text=text,
            image_base64=image_base64,
            audio_base64=audio_base64,
            pdf_base64=pdf_base64,
            metadata=parsed_metadata
        )

        logger.info(f"[API] ✅ Service returned: success={result.get('success')}, type={result.get('entry_type')}, confidence={result.get('confidence')}")
        logger.info(f"[API] Response data keys: {list(result.get('data', {}).keys())}")
        logger.info(f"[API] Suggestions: {result.get('suggestions')}")
        logger.info("=" * 80)

        return QuickEntryResponse(**result)

    except Exception as e:
        logger.error("=" * 80)
        logger.error("[API] ❌ QUICK ENTRY PREVIEW FAILED")
        logger.error(f"[API] Error type: {type(e).__name__}")
        logger.error(f"[API] Error message: {str(e)}")
        import traceback
        logger.error(f"[API] Full traceback:\n{traceback.format_exc()}")
        logger.error("=" * 80)
        raise HTTPException(status_code=500, detail=str(e))


class ConfirmEntryRequest(BaseModel):
    """Confirm entry request after user approval"""
    entry_type: str
    data: dict
    original_text: str
    extracted_text: Optional[str] = None
    image_base64: Optional[str] = None


@router.post("/confirm", response_model=QuickEntryResponse)
async def quick_entry_confirm(
    request: ConfirmEntryRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Confirm and save quick entry after user approval.

    This endpoint:
    1. Takes LLM-classified data (possibly edited by user)
    2. Saves to appropriate database table
    3. Vectorizes for RAG
    4. Returns success confirmation

    Only called after user explicitly confirms via UI.
    """
    service = get_quick_entry_service()

    try:
        result = await service.confirm_and_save_entry(
            user_id=current_user["id"],
            entry_type=request.entry_type,
            data=request.data,
            original_text=request.original_text,
            extracted_text=request.extracted_text,
            image_base64=request.image_base64
        )

        return QuickEntryResponse(**result)

    except Exception as e:
        logger.error(f"Quick entry confirm failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
