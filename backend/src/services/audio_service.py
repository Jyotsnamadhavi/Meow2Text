"""
Audio processing service for Meow2Text.
"""
import librosa
import numpy as np
import os
from typing import Dict, Tuple
from pathlib import Path

from backend.src.core.exceptions import AudioProcessingError, ValidationError
from backend.src.core.config import settings


class AudioService:
    """Service for audio processing operations."""
    
    def __init__(self):
        self.supported_formats = settings.supported_audio_formats.split(",")
        self.max_size = settings.max_audio_size
        self.sample_rate = settings.audio_sample_rate
        self.max_duration = settings.audio_max_duration
    
    def validate_audio_file(self, file_path: str) -> bool:
        """
        Validate audio file format and properties.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValidationError: If file is invalid
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise ValidationError(f"File not found: {file_path}")
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > self.max_size:
                raise ValidationError(f"File too large: {file_size} bytes (max: {self.max_size})")
            
            # Check file extension
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in self.supported_formats:
                raise ValidationError(f"Unsupported format: {file_ext}")
            
            # Try to load audio
            y, sr = librosa.load(file_path, sr=None, duration=1.0)
            
            # Check duration
            duration = librosa.get_duration(y=y, sr=sr)
            if duration < 0.5 or duration > self.max_duration:
                raise ValidationError(f"Invalid duration: {duration}s (must be 0.5-{self.max_duration}s)")
            
            return True
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Audio validation failed: {str(e)}")
    
    def preprocess_audio(self, audio_path: str) -> np.ndarray:
        """
        Preprocess audio file for classification.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Preprocessed audio features
            
        Raises:
            AudioProcessingError: If processing fails
        """
        try:
            # Validate file first
            self.validate_audio_file(audio_path)
            
            # Load audio file
            y, sr = librosa.load(audio_path, sr=self.sample_rate, duration=self.max_duration)
            
            # Normalize audio
            y = librosa.util.normalize(y)
            
            # Extract MFCC features
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # Extract mel-spectrogram features
            mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
            
            # Combine features
            features = np.concatenate([mfcc, mel_spec_db[:13]], axis=0)
            
            return features
            
        except Exception as e:
            raise AudioProcessingError(f"Audio preprocessing failed: {str(e)}")
    
    def extract_audio_features(self, audio_path: str) -> Dict[str, float]:
        """
        Extract various audio features for analysis.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary of audio features
            
        Raises:
            AudioProcessingError: If feature extraction fails
        """
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=self.sample_rate, duration=self.max_duration)
            
            # Basic features
            duration = librosa.get_duration(y=y, sr=sr)
            rms = np.sqrt(np.mean(y**2))  # Root mean square (loudness)
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            
            # Pitch features
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_mean = np.mean(pitches[magnitudes > 0.1])
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            
            return {
                "duration": duration,
                "loudness": rms,
                "spectral_centroid_mean": np.mean(spectral_centroids),
                "spectral_rolloff_mean": np.mean(spectral_rolloff),
                "pitch_mean": pitch_mean,
                "tempo": tempo,
                "sample_rate": sr
            }
            
        except Exception as e:
            raise AudioProcessingError(f"Feature extraction failed: {str(e)}")


# Global audio service instance
audio_service = AudioService() 