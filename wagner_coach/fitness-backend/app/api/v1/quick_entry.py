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
