"""
API routes for Meow2Text application.
"""
import os
import tempfile
import shutil
from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse

from backend.src.core.config import settings
from backend.src.core.exceptions import Meow2TextError, ValidationError
from backend.src.models.schemas import (
    ClassificationResult, 
    TranslationResponse, 
    PersonalityInfo, 
    HealthResponse,
    ErrorResponse
)
from backend.src.services.audio_service import audio_service
from backend.src.services.classification_service import classification_service
from backend.src.services.translation_service import translation_service

# Create router
router = APIRouter()


@router.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}! 🐱",
        "version": settings.app_version,
        "description": settings.app_description
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="Meow2Text is running! 😸",
        version=settings.app_version
    )


@router.post("/classify", response_model=ClassificationResult)
async def classify_audio(file: UploadFile = File(...)):
    """
    Classify uploaded cat meow audio into categories.
    
    Args:
        file: Audio file to classify
        
    Returns:
        Classification result with category and confidence
        
    Raises:
        HTTPException: If classification fails
    """
    try:
        # Validate file type - be more flexible with audio content types
        valid_audio_types = [
            'audio/wav', 'audio/mp3', 'audio/mpeg', 'audio/mp4', 
            'audio/webm', 'audio/ogg', 'audio/flac', 'audio/m4a'
        ]
        
        if not file.content_type or file.content_type not in valid_audio_types:
            # Check file extension as fallback
            file_ext = file.filename.lower().split('.')[-1] if file.filename else ''
            valid_extensions = ['wav', 'mp3', 'm4a', 'flac', 'webm', 'mp4']
            if file_ext not in valid_extensions:
                raise ValidationError(f"File must be an audio file. Supported formats: {', '.join(valid_extensions)}")
        
        # Save uploaded file temporarily with correct extension
        # Determine file extension from content type
        content_type_to_ext = {
            'audio/wav': '.wav',
            'audio/mp3': '.mp3',
            'audio/mpeg': '.mp3',
            'audio/mp4': '.mp4',
            'audio/webm': '.webm',
            'audio/ogg': '.ogg',
            'audio/flac': '.flac',
            'audio/m4a': '.m4a'
        }
        
        file_ext = content_type_to_ext.get(file.content_type, '.wav')
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        try:
            # Preprocess audio
            processed_audio = audio_service.preprocess_audio(temp_path)
            
            # Classify meow
            classification = classification_service.classify_meow(processed_audio)
            
            return ClassificationResult(**classification)
            
        finally:
            # Clean up temp file
            os.unlink(temp_path)
            
    except Meow2TextError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


@router.post("/translate", response_model=TranslationResponse)
async def translate_audio(
    file: UploadFile = File(...),
    personality: str = Form("chill")
):
    """
    Translate cat meow to text with specified personality.
    
    Args:
        file: Audio file to translate
        personality: Cat personality (diva, chill, old_man)
        
    Returns:
        Translation result with classification and translated text
        
    Raises:
        HTTPException: If translation fails
    """
    try:
        # Validate file type - be more flexible with audio content types
        valid_audio_types = [
            'audio/wav', 'audio/mp3', 'audio/mpeg', 'audio/mp4', 
            'audio/webm', 'audio/ogg', 'audio/flac', 'audio/m4a'
        ]
        
        if not file.content_type or file.content_type not in valid_audio_types:
            # Check file extension as fallback
            file_ext = file.filename.lower().split('.')[-1] if file.filename else ''
            valid_extensions = ['wav', 'mp3', 'm4a', 'flac', 'webm', 'mp4']
            if file_ext not in valid_extensions:
                raise ValidationError(f"File must be an audio file. Supported formats: {', '.join(valid_extensions)}")
        
        # Validate personality
        valid_personalities = ["diva", "chill", "old_man"]
        if personality not in valid_personalities:
            raise ValidationError(f"Personality must be one of: {valid_personalities}")
        
        # Save uploaded file temporarily with correct extension
        # Determine file extension from content type
        content_type_to_ext = {
            'audio/wav': '.wav',
            'audio/mp3': '.mp3',
            'audio/mpeg': '.mp3',
            'audio/mp4': '.mp4',
            'audio/webm': '.webm',
            'audio/ogg': '.ogg',
            'audio/flac': '.flac',
            'audio/m4a': '.m4a'
        }
        
        file_ext = content_type_to_ext.get(file.content_type, '.wav')
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        try:
            # Preprocess audio
            processed_audio = audio_service.preprocess_audio(temp_path)
            
            # Classify meow
            classification = classification_service.classify_meow(processed_audio)
            
            # Translate with personality
            translation = translation_service.translate_meow(classification, personality)
            
            return TranslationResponse(
                classification=ClassificationResult(**classification),
                translation=translation,
                personality=personality
            )
            
        finally:
            # Clean up temp file
            os.unlink(temp_path)
            
    except Meow2TextError as e:
        print(f"Meow2Text Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.get("/personalities", response_model=List[PersonalityInfo])
async def get_personalities():
    """
    Get available personality options.
    
    Returns:
        List of available personalities
    """
    personalities = [
        PersonalityInfo(
            id="diva",
            name="Diva",
            description="Dramatic and demanding cat",
            emoji="👑"
        ),
        PersonalityInfo(
            id="chill",
            name="Chill",
            description="Laid-back and philosophical cat",
            emoji="😎"
        ),
        PersonalityInfo(
            id="old_man",
            name="Old Man",
            description="Grumpy and wise cat",
            emoji="👴"
        )
    ]
    
    return personalities


@router.get("/config")
async def get_config():
    """
    Get application configuration (non-sensitive).
    
    Returns:
        Application configuration
    """
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "supported_audio_formats": settings.supported_audio_formats.split(","),
        "max_audio_size_mb": settings.max_audio_size // (1024 * 1024),
        "audio_max_duration": settings.audio_max_duration,
        "confidence_threshold": settings.confidence_threshold
    }


@router.get("/memory/stats")
async def get_memory_stats():
    """
    Get memory statistics for all personalities.
    
    Returns:
        Memory statistics for each personality
    """
    stats = translation_service.get_memory_stats()
    return {
        "memory_stats": stats,
        "total_conversations": sum(stats.values())
    }


@router.get("/memory/history/{personality}")
async def get_conversation_history(personality: str):
    """
    Get conversation history for a specific personality.
    
    Args:
        personality: Cat personality (diva, chill, old_man)
        
    Returns:
        Conversation history
    """
    valid_personalities = ["diva", "chill", "old_man"]
    if personality not in valid_personalities:
        raise HTTPException(status_code=400, detail=f"Personality must be one of: {valid_personalities}")
    
    history = translation_service.get_conversation_history(personality)
    return {
        "personality": personality,
        "conversation_history": history,
        "message_count": len(history.split('\n')) if history else 0
    }


@router.delete("/memory/clear")
async def clear_memory(personality: str = None):
    """
    Clear conversation memory for a specific personality or all personalities.
    
    Args:
        personality: Specific personality to clear (optional)
        
    Returns:
        Confirmation message
    """
    if personality:
        valid_personalities = ["diva", "chill", "old_man"]
        if personality not in valid_personalities:
            raise HTTPException(status_code=400, detail=f"Personality must be one of: {valid_personalities}")
    
    translation_service.clear_memory(personality)
    
    if personality:
        return {"message": f"Memory cleared for {personality} personality"}
    else:
        return {"message": "Memory cleared for all personalities"} 