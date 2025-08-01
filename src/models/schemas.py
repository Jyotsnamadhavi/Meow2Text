"""
Pydantic schemas for API requests and responses.
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ClassificationResult(BaseModel):
    """Schema for meow classification result."""
    category: str = Field(..., description="Meow category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Classification confidence")
    description: str = Field(..., description="Category description")
    all_scores: Dict[str, float] = Field(..., description="Scores for all categories")
    features: Dict[str, float] = Field(default_factory=dict, description="Audio features")


class TranslationRequest(BaseModel):
    """Schema for translation request."""
    personality: str = Field(..., description="Cat personality")


class TranslationResponse(BaseModel):
    """Schema for translation response."""
    classification: ClassificationResult
    translation: str = Field(..., description="Translated cat text")
    personality: str = Field(..., description="Used personality")


class PersonalityInfo(BaseModel):
    """Schema for personality information."""
    id: str = Field(..., description="Personality ID")
    name: str = Field(..., description="Personality name")
    description: str = Field(..., description="Personality description")
    emoji: str = Field(..., description="Personality emoji")


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details") 