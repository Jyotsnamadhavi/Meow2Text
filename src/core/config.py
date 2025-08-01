"""
Configuration settings for Meow2Text application.
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    app_name: str = "Meow2Text API"
    app_version: str = "1.0.0"
    app_description: str = "Translate your cat's meows to sassy text!"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"
    openai_temperature: float = 0.8
    openai_max_tokens: int = 150
    
    # CORS Configuration
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Audio Configuration
    max_audio_size: int = 10 * 1024 * 1024  # 10MB
    supported_audio_formats: str = ".wav,.mp3,.m4a,.flac"
    audio_sample_rate: int = 16000
    audio_max_duration: float = 10.0  # seconds
    
    # Classification Configuration
    confidence_threshold: float = 0.3
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 