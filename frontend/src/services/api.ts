import axios from 'axios';
import { TranslationData, ClassificationResult } from '../types';

const API_BASE_URL = 'http://localhost:3001/api/v1';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for audio processing
});

export const translateAudio = async (formData: FormData): Promise<TranslationData> => {
  try {
    const response = await api.post('/translate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response?.status === 400) {
        throw new Error('Invalid audio file. Please try again.');
      } else if (error.response?.status === 500) {
        throw new Error('Server error. Please try again later.');
      } else {
        throw new Error(error.response?.data?.detail || 'Failed to translate audio');
      }
    }
    throw new Error('Network error. Please check your connection.');
  }
};

export const classifyAudio = async (formData: FormData): Promise<ClassificationResult> => {
  try {
    const response = await api.post('/classify', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to classify audio');
    }
    throw new Error('Network error. Please check your connection.');
  }
};

export const getPersonalities = async () => {
  try {
    const response = await api.get('/personalities');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch personalities:', error);
    return [];
  }
};

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Backend is not available');
  }
}; 