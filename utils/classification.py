import numpy as np
from typing import Dict, List, Tuple
import random

# Cat meow categories and their characteristics
MEOW_CATEGORIES = {
    "hungry": {
        "description": "Hungry cat meow",
        "characteristics": {
            "pitch_range": (200, 800),  # Hz
            "duration_range": (0.5, 2.0),  # seconds
            "loudness_range": (0.1, 0.8),
            "tempo_range": (60, 120)
        }
    },
    "angry": {
        "description": "Angry/aggressive cat meow",
        "characteristics": {
            "pitch_range": (300, 1000),
            "duration_range": (0.3, 1.5),
            "loudness_range": (0.3, 1.0),
            "tempo_range": (80, 150)
        }
    },
    "playful": {
        "description": "Playful/excited cat meow",
        "characteristics": {
            "pitch_range": (150, 600),
            "duration_range": (0.2, 1.0),
            "loudness_range": (0.2, 0.7),
            "tempo_range": (100, 180)
        }
    },
    "sleepy": {
        "description": "Sleepy/tired cat meow",
        "characteristics": {
            "pitch_range": (100, 400),
            "duration_range": (0.8, 3.0),
            "loudness_range": (0.05, 0.4),
            "tempo_range": (40, 80)
        }
    },
    "attention": {
        "description": "Attention-seeking cat meow",
        "characteristics": {
            "pitch_range": (250, 700),
            "duration_range": (0.5, 2.5),
            "loudness_range": (0.2, 0.9),
            "tempo_range": (70, 130)
        }
    }
}

def classify_meow(audio_features: np.ndarray) -> Dict:
    """
    Classify cat meow based on audio features
    
    Args:
        audio_features: Preprocessed audio features
        
    Returns:
        Classification result with category and confidence
    """
    try:
        # For now, we'll use a simple rule-based classification
        # In a real implementation, you'd use a trained model
        
        # Extract basic features from the audio features
        # This is a simplified approach - in reality you'd extract these from the audio
        features = extract_features_from_array(audio_features)
        
        # Calculate similarity scores for each category
        scores = {}
        for category, info in MEOW_CATEGORIES.items():
            score = calculate_category_similarity(features, info["characteristics"])
            scores[category] = score
        
        # Get the best matching category
        best_category = max(scores, key=scores.get)
        confidence = scores[best_category]
        
        # Add some randomness for demo purposes
        if confidence < 0.3:
            # If confidence is low, randomly assign a category
            best_category = random.choice(list(MEOW_CATEGORIES.keys()))
            confidence = random.uniform(0.4, 0.7)
        
        return {
            "category": best_category,
            "confidence": round(confidence, 3),
            "description": MEOW_CATEGORIES[best_category]["description"],
            "all_scores": {k: round(v, 3) for k, v in scores.items()},
            "features": features
        }
        
    except Exception as e:
        # Fallback classification
        return {
            "category": "playful",
            "confidence": 0.5,
            "description": "Playful cat meow",
            "all_scores": {"playful": 0.5},
            "features": {},
            "error": str(e)
        }

def extract_features_from_array(audio_features: np.ndarray) -> Dict:
    """
    Extract interpretable features from audio feature array
    
    Args:
        audio_features: Preprocessed audio features
        
    Returns:
        Dictionary of extracted features
    """
    try:
        # This is a simplified feature extraction
        # In reality, you'd extract these from the actual audio
        
        # Simulate feature extraction based on the array
        mfcc_mean = np.mean(audio_features[:13], axis=1)
        mel_mean = np.mean(audio_features[13:], axis=1)
        
        # Estimate features from the processed array
        estimated_pitch = 300 + np.std(mfcc_mean) * 100  # Hz
        estimated_loudness = np.mean(np.abs(mel_mean))
        estimated_duration = 1.0 + np.std(mel_mean) * 2  # seconds
        estimated_tempo = 80 + np.std(mfcc_mean) * 50  # BPM
        
        return {
            "pitch": estimated_pitch,
            "loudness": estimated_loudness,
            "duration": estimated_duration,
            "tempo": estimated_tempo,
            "mfcc_variance": np.var(mfcc_mean),
            "mel_variance": np.var(mel_mean)
        }
        
    except Exception:
        # Return default features if extraction fails
        return {
            "pitch": 400,
            "loudness": 0.5,
            "duration": 1.0,
            "tempo": 100,
            "mfcc_variance": 0.1,
            "mel_variance": 0.1
        }

def calculate_category_similarity(features: Dict, category_characteristics: Dict) -> float:
    """
    Calculate similarity between extracted features and category characteristics
    
    Args:
        features: Extracted audio features
        category_characteristics: Expected characteristics for the category
        
    Returns:
        Similarity score between 0 and 1
    """
    try:
        score = 0.0
        total_weight = 0.0
        
        # Pitch similarity
        if "pitch" in features:
            pitch = features["pitch"]
            pitch_range = category_characteristics["pitch_range"]
            pitch_score = 1.0 - min(abs(pitch - (pitch_range[0] + pitch_range[1]) / 2) / 500, 1.0)
            score += pitch_score * 0.3
            total_weight += 0.3
        
        # Loudness similarity
        if "loudness" in features:
            loudness = features["loudness"]
            loudness_range = category_characteristics["loudness_range"]
            loudness_score = 1.0 - min(abs(loudness - (loudness_range[0] + loudness_range[1]) / 2) / 0.5, 1.0)
            score += loudness_score * 0.3
            total_weight += 0.3
        
        # Duration similarity
        if "duration" in features:
            duration = features["duration"]
            duration_range = category_characteristics["duration_range"]
            duration_score = 1.0 - min(abs(duration - (duration_range[0] + duration_range[1]) / 2) / 2.0, 1.0)
            score += duration_score * 0.2
            total_weight += 0.2
        
        # Tempo similarity
        if "tempo" in features:
            tempo = features["tempo"]
            tempo_range = category_characteristics["tempo_range"]
            tempo_score = 1.0 - min(abs(tempo - (tempo_range[0] + tempo_range[1]) / 2) / 100, 1.0)
            score += tempo_score * 0.2
            total_weight += 0.2
        
        return score / total_weight if total_weight > 0 else 0.5
        
    except Exception:
        return 0.5

def get_meow_characteristics(category: str) -> Dict:
    """
    Get characteristics for a specific meow category
    
    Args:
        category: Meow category
        
    Returns:
        Category characteristics
    """
    return MEOW_CATEGORIES.get(category, MEOW_CATEGORIES["playful"]) 