import React from 'react';
import { TranslationData } from '../types';

interface TranslationResultProps {
  data: TranslationData;
}

const TranslationResult: React.FC<TranslationResultProps> = ({ data }) => {
  const { classification, translation, personality } = data;

  const getPersonalityEmoji = (personality: string) => {
    const emojis: Record<string, string> = {
      'diva': '👑',
      'chill': '😎',
      'old_man': '👴'
    };
    return emojis[personality] || '🐱';
  };

  const getCategoryEmoji = (category: string) => {
    const emojis: Record<string, string> = {
      'hungry': '🍽️',
      'angry': '😾',
      'playful': '🎾',
      'sleepy': '😴',
      'attention': '👀'
    };
    return emojis[category] || '🐱';
  };

  return (
    <div className="translation-result">
      <div className="result-card">
        <div className="result-header">
          <h3>🐾 Cat's Message</h3>
          <div className="personality-badge">
            {getPersonalityEmoji(personality)} {personality.charAt(0).toUpperCase() + personality.slice(1)}
          </div>
        </div>
        
        <div className="translation-text">
          <p>"{translation}"</p>
        </div>
      </div>

      <div className="classification-details">
        <h3>🔍 Meow Analysis</h3>
        <div className="classification-grid">
          <div className="classification-item">
            <span className="label">Category:</span>
            <span className="value">
              {getCategoryEmoji(classification.category)} {classification.category}
            </span>
          </div>
          
          <div className="classification-item">
            <span className="label">Confidence:</span>
            <span className="value">
              {(classification.confidence * 100).toFixed(1)}%
            </span>
          </div>
          
          <div className="classification-item">
            <span className="label">Description:</span>
            <span className="value">{classification.description}</span>
          </div>
          
          {classification.actual_duration && (
            <div className="classification-item">
              <span className="label">Duration:</span>
              <span className="value">⏱️ {classification.actual_duration.toFixed(2)}s</span>
            </div>
          )}
        </div>

        <div className="confidence-scores">
          <h4>All Category Scores:</h4>
          <div className="scores-grid">
            {Object.entries(classification.all_scores).map(([category, score]) => (
              <div 
                key={category} 
                className={`score-item ${category === classification.category ? 'top-score' : ''}`}
              >
                <span className="category-name">
                  {getCategoryEmoji(category)} {category}
                </span>
                <span className="score-value">
                  {(score * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="share-section">
        <h3>📤 Share This Translation</h3>
        <button 
          className="share-button"
          onClick={() => {
            const text = `My cat said: "${translation}" (${classification.category} meow, ${personality} personality)`;
            navigator.clipboard.writeText(text);
            alert('Translation copied to clipboard!');
          }}
        >
          📋 Copy to Clipboard
        </button>
      </div>
    </div>
  );
};

export default TranslationResult; 