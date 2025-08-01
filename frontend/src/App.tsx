import React, { useState } from 'react';
import './App.css';
import AudioRecorder from './components/AudioRecorder';
import PersonalitySelector from './components/PersonalitySelector';
import TranslationResult from './components/TranslationResult';
import { TranslationData } from './types';

function App() {
  const [translationData, setTranslationData] = useState<TranslationData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedPersonality, setSelectedPersonality] = useState('chill');

  const handleTranslationComplete = (data: TranslationData) => {
    setTranslationData(data);
    setError(null);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setTranslationData(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🐱 Meow2Text 🐱</h1>
        <p>Translate your cat's meows to sassy text!</p>
      </header>

      <main className="App-main">
        <div className="container">
          <div className="section">
            <AudioRecorder 
              onTranslationComplete={handleTranslationComplete}
              onError={handleError}
              selectedPersonality={selectedPersonality}
            />
          </div>

          <div className="section">
            <h2>🎭 Choose Cat Personality</h2>
            <PersonalitySelector 
              selectedPersonality={selectedPersonality}
              onPersonalityChange={setSelectedPersonality}
            />
          </div>

          {error && (
            <div className="section">
              <div className="error">
                <p>❌ {error}</p>
              </div>
            </div>
          )}

          {translationData && (
            <div className="section">
              <h2>🐾 Translation Result</h2>
              <TranslationResult data={translationData} />
            </div>
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>Made with ❤️ for cat lovers everywhere</p>
        <p>Powered by LangChain & OpenAI</p>
      </footer>
    </div>
  );
}

export default App;
