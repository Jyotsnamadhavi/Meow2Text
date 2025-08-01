import librosa
import numpy as np
import os
from typing import Tuple, Optional

def preprocess_audio(audio_path: str) -> np.ndarray:
    """
    Preprocess audio file for classification
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Preprocessed audio features
    """
    try:
        # Load audio file
        y, sr = librosa.load(audio_path, sr=16000, duration=5.0)
        
        # Normalize audio
        y = librosa.util.normalize(y)
        
        # Extract MFCC features (commonly used for audio classification)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # Extract mel-spectrogram features
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Combine features
        features = np.concatenate([mfcc, mel_spec_db[:13]], axis=0)
        
        return features
        
    except Exception as e:
        raise Exception(f"Audio preprocessing failed: {str(e)}")

def extract_audio_features(audio_path: str) -> dict:
    """
    Extract various audio features for analysis
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Dictionary of audio features
    """
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=16000, duration=5.0)
        
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
        raise Exception(f"Feature extraction failed: {str(e)}")

def validate_audio_file(audio_path: str) -> bool:
    """
    Validate audio file format and properties
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        True if valid, False otherwise
    """
    try:
        # Check if file exists
        if not os.path.exists(audio_path):
            return False
        
        # Check file size (max 10MB)
        file_size = os.path.getsize(audio_path)
        if file_size > 10 * 1024 * 1024:  # 10MB
            return False
        
        # Try to load audio
        y, sr = librosa.load(audio_path, sr=None, duration=1.0)
        
        # Check duration (between 0.5 and 10 seconds)
        duration = librosa.get_duration(y=y, sr=sr)
        if duration < 0.5 or duration > 10:
            return False
        
        return True
        
    except Exception:
        return False 