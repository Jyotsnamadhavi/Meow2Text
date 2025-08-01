"""
Custom exceptions for Meow2Text application.
"""


class Meow2TextError(Exception):
    """Base exception for Meow2Text application."""
    pass


class AudioProcessingError(Meow2TextError):
    """Raised when audio processing fails."""
    pass


class ClassificationError(Meow2TextError):
    """Raised when meow classification fails."""
    pass


class TranslationError(Meow2TextError):
    """Raised when translation fails."""
    pass


class ConfigurationError(Meow2TextError):
    """Raised when configuration is invalid."""
    pass


class ValidationError(Meow2TextError):
    """Raised when input validation fails."""
    pass 