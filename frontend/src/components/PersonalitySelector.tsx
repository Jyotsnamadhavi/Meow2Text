import React from 'react';
import { Personality } from '../types';

interface PersonalitySelectorProps {
  selectedPersonality: string;
  onPersonalityChange: (personality: string) => void;
}

const personalities: Personality[] = [
  {
    id: 'diva',
    name: 'Diva',
    description: 'Dramatic and demanding cat',
    emoji: '👑'
  },
  {
    id: 'chill',
    name: 'Chill',
    description: 'Laid-back and philosophical cat',
    emoji: '😎'
  },
  {
    id: 'old_man',
    name: 'Old Man',
    description: 'Grumpy and wise cat',
    emoji: '👴'
  }
];

const PersonalitySelector: React.FC<PersonalitySelectorProps> = ({
  selectedPersonality,
  onPersonalityChange
}) => {
  return (
    <div className="personality-selector">
      <div className="personality-grid">
        {personalities.map((personality) => (
          <div
            key={personality.id}
            className={`personality-card ${selectedPersonality === personality.id ? 'selected' : ''}`}
            onClick={() => onPersonalityChange(personality.id)}
          >
            <div className="personality-emoji">{personality.emoji}</div>
            <h3>{personality.name}</h3>
            <p>{personality.description}</p>
            {selectedPersonality === personality.id && (
              <div className="selected-indicator">✓ Selected</div>
            )}
          </div>
        ))}
      </div>
      
      <div className="personality-info">
        <h3>🎭 Personality Styles</h3>
        <ul>
          <li><strong>Diva 👑:</strong> Dramatic, demanding, and entitled responses</li>
          <li><strong>Chill 😎:</strong> Laid-back, philosophical, and relaxed responses</li>
          <li><strong>Old Man 👴:</strong> Grumpy, wise, and nostalgic responses</li>
        </ul>
      </div>
    </div>
  );
};

export default PersonalitySelector; 