import React, { useState, useRef } from 'react';
import { translateAudio } from '../services/api';
import { TranslationData } from '../types';

interface AudioRecorderProps {
  onTranslationComplete: (data: TranslationData) => void;
  onError: (error: string) => void;
  selectedPersonality: string;
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({
  onTranslationComplete,
  onError,
  selectedPersonality
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Try to use a more compatible audio format
      const mimeType = MediaRecorder.isTypeSupported('audio/webm') 
        ? 'audio/webm' 
        : MediaRecorder.isTypeSupported('audio/mp4') 
        ? 'audio/mp4' 
        : 'audio/wav';
      
      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: mimeType });
        setAudioBlob(audioBlob);
        const audioUrl = URL.createObjectURL(audioBlob);
        setAudioUrl(audioUrl);
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
        console.log('Audio blob type:', audioBlob.type);
console.log('Audio blob size:', audioBlob.size);
console.log('Selected personality:', selectedPersonality);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      onError('Failed to access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleTranslate = async () => {
    if (!audioBlob) return;

    setIsProcessing(true);
    try {
      // Create a proper audio file with correct MIME type
      const audioFile = new File([audioBlob], 'meow.wav', { 
        type: audioBlob.type || 'audio/wav',
        lastModified: Date.now()
      });
      
      const formData = new FormData();
      formData.append('file', audioFile);
      formData.append('personality', selectedPersonality);

      const translationData = await translateAudio(formData);
      onTranslationComplete(translationData);
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Translation failed');
    } finally {
      setIsProcessing(false);
    }
  };

  const handlePlayback = () => {
    if (audioUrl) {
      const audio = new Audio(audioUrl);
      audio.play();
    }
  };

  const handleNewRecording = () => {
    setAudioBlob(null);
    setAudioUrl(null);
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
    }
  };

  return (
    <div className="audio-recorder">
      <h2>🎤 Record Your Cat's Meow</h2>
      
      {!audioBlob ? (
        <div className="recording-section">
          <button
            className={`record-button ${isRecording ? 'recording' : ''}`}
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isProcessing}
          >
            {isRecording ? '⏹️ Stop Recording' : '🎤 Start Recording'}
          </button>
          
          {isRecording && (
            <div className="recording-indicator">
              <span className="pulse">🔴 Recording...</span>
            </div>
          )}
        </div>
      ) : (
        <div className="playback-section">
          <h3>✅ Recording Complete!</h3>
          
          <div className="audio-controls">
            <button onClick={handlePlayback} className="play-button">
              ▶️ Play Recording
            </button>
            
            <button onClick={handleNewRecording} className="new-recording-button">
              🎤 New Recording
            </button>
          </div>
          
          <button
            onClick={handleTranslate}
            disabled={isProcessing}
            className="translate-button"
          >
            {isProcessing ? '🔄 Translating...' : '🐱 Translate Meow'}
          </button>
        </div>
      )}
      
      {isProcessing && (
        <div className="processing-indicator">
          <p>Processing your cat's meow...</p>
        </div>
      )}
    </div>
  );
};

export default AudioRecorder; 