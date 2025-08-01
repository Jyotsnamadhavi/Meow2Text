import React, { useState, useRef } from 'react';
import { AudioRecorder as VoiceRecorder } from 'react-audio-voice-recorder';
import { TranslationData } from '../types';
import { translateAudio } from '../services/api';

interface AudioRecorderProps {
  onTranslationComplete: (data: TranslationData) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
  selectedPersonality: string;
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({
  onTranslationComplete,
  onError,
  onLoading,
  selectedPersonality
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const audioRef = useRef<HTMLAudioElement>(null);

  const handleRecordingComplete = async (blob: Blob) => {
    setAudioBlob(blob);
    setIsRecording(false);
    
    try {
      onLoading(true);
      
      // Create form data for file upload
      const formData = new FormData();
      formData.append('file', blob, 'cat_meow.wav');
      formData.append('personality', selectedPersonality);
      
      // Call translation API
      const result = await translateAudio(formData);
      onTranslationComplete(result);
      
    } catch (error) {
      console.error('Translation error:', error);
      onError(error instanceof Error ? error.message : 'Failed to translate meow');
    } finally {
      onLoading(false);
    }
  };

  const handleRecordingStart = () => {
    setIsRecording(true);
    onError(''); // Clear any previous errors
  };

  const handleRecordingStop = () => {
    setIsRecording(false);
  };

  const playAudio = () => {
    if (audioBlob && audioRef.current) {
      const url = URL.createObjectURL(audioBlob);
      audioRef.current.src = url;
      audioRef.current.play();
    }
  };

  return (
    <div className="audio-recorder">
      <div className="recorder-container">
        <VoiceRecorder
          onRecordingComplete={handleRecordingComplete}
          audioTrackConstraints={{
            noiseSuppression: true,
            echoCancellation: true,
          }}
          downloadOnSavePress={false}
          downloadFileExtension="wav"
        />
        
        {isRecording && (
          <div className="recording-indicator">
            <div className="recording-dot"></div>
            <span>Recording... Speak clearly!</span>
          </div>
        )}
      </div>

      {audioBlob && (
        <div className="audio-playback">
          <h3>🎵 Your Cat's Meow</h3>
          <button 
            className="play-button"
            onClick={playAudio}
            disabled={isRecording}
          >
            ▶️ Play Recording
          </button>
          <audio ref={audioRef} controls style={{ display: 'none' }} />
        </div>
      )}

      <div className="instructions">
        <h3>📝 Instructions</h3>
        <ul>
          <li>Click the microphone button to start recording</li>
          <li>Record your cat's meow (1-5 seconds is ideal)</li>
          <li>Click stop when finished</li>
          <li>Choose a personality below for the translation style</li>
        </ul>
      </div>
    </div>
  );
};

export default AudioRecorder; 