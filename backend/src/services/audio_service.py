"""
Audio processing service for Meow2Text.
"""
import librosa
import numpy as np
import os
import tempfile
from typing import Dict, Tuple, Optional
from pathlib import Path
from pydub import AudioSegment

from backend.src.core.exceptions import AudioProcessingError, ValidationError
from backend.src.core.config import settings


class AudioService:
    """Service for audio processing operations."""
    
    def __init__(self):
        self.supported_formats = settings.supported_audio_formats.split(",")
        self.max_size = settings.max_audio_size
        self.sample_rate = settings.audio_sample_rate
        self.max_duration = settings.audio_max_duration
    
    def _convert_audio_for_librosa(self, file_path: str) -> str:
        """
        Convert audio file to WAV format for librosa processing.
        
        Args:
            file_path: Path to input audio file
            
        Returns:
            Path to converted WAV file
        """
        try:
            # Load audio with pydub
            audio = AudioSegment.from_file(file_path)
            
            # Export as WAV
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            audio.export(temp_wav.name, format='wav')
            
            return temp_wav.name
        except Exception as e:
            print(f"Audio conversion failed: {str(e)}")
            raise AudioProcessingError(f"Failed to convert audio: {str(e)}")
    
    def validate_audio_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate audio file format and properties.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False, f"File not found: {file_path}"
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return False, "Audio file is empty"
            if file_size > self.max_size:
                return False, f"File too large: {file_size} bytes (max: {self.max_size})"
            
            # Check file extension
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in self.supported_formats:
                return False, f"Unsupported format: {file_ext}"
            
            # Try to load audio with conversion if needed
            converted_path = None
            try:
                y, sr = librosa.load(file_path, sr=None, duration=1.0)
            except Exception as load_error:
                print(f"Librosa load failed: {str(load_error)}")
                # Try converting the audio file
                try:
                    converted_path = self._convert_audio_for_librosa(file_path)
                    y, sr = librosa.load(converted_path, sr=None, duration=1.0)
                    print(f"Successfully converted and loaded audio")
                except Exception as convert_error:
                    print(f"Audio conversion also failed: {str(convert_error)}")
                    return False, f"Failed to load audio: {str(load_error)}"
            
            # Check duration
            duration = librosa.get_duration(y=y, sr=sr)
            if duration < 0.5 or duration > self.max_duration:
                return False, f"Invalid duration: {duration}s (must be 0.5-{self.max_duration}s)"
            
            # Clean up converted file if it was created
            if converted_path and os.path.exists(converted_path):
                os.unlink(converted_path)
            
            return True, None
            
        except Exception as e:
            print(f"Audio validation error: {str(e)}")
            print(f"File path: {file_path}")
            print(f"File exists: {os.path.exists(file_path)}")
            if os.path.exists(file_path):
                print(f"File size: {os.path.getsize(file_path)} bytes")
            return False, f"Audio validation failed: {str(e)}"
    
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
            is_valid, error_msg = self.validate_audio_file(audio_path)
            if not is_valid:
                raise AudioProcessingError(error_msg)
            
            # Load audio file with conversion if needed
            converted_path = None
            try:
                y, sr = librosa.load(audio_path, sr=self.sample_rate, duration=self.max_duration)
            except Exception as load_error:
                print(f"Librosa load failed for preprocessing: {str(load_error)}")
                # Try converting the audio file
                try:
                    converted_path = self._convert_audio_for_librosa(audio_path)
                    y, sr = librosa.load(converted_path, sr=self.sample_rate, duration=self.max_duration)
                    print(f"Successfully converted and loaded audio for preprocessing")
                except Exception as convert_error:
                    print(f"Audio conversion failed for preprocessing: {str(convert_error)}")
                    raise load_error
            
            # Normalize audio
            y = librosa.util.normalize(y)
            
            # Extract MFCC features
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # Extract mel-spectrogram features
            mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
            
            # Combine features
            features = np.concatenate([mfcc, mel_spec_db[:13]], axis=0)
            
            # Clean up converted file if it was created
            if converted_path and os.path.exists(converted_path):
                os.unlink(converted_path)
            
            return features
            
        except Exception as e:
            print(f"Audio preprocessing error: {str(e)}")
            print(f"Audio path: {audio_path}")
            import traceback
            traceback.print_exc()
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