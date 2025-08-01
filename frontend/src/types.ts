export interface TranslationData {
  classification: {
    category: string;
    confidence: number;
    description: string;
    all_scores: Record<string, number>;
    features: Record<string, any>;
  };
  translation: string;
  personality: string;
}

export interface Personality {
  id: string;
  name: string;
  description: string;
  emoji: string;
}

export interface ClassificationResult {
  category: string;
  confidence: number;
  description: string;
  all_scores: Record<string, number>;
  features: Record<string, any>;
} 