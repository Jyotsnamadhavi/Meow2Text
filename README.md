# Meow2Text 🐱

Translate your cat's meows into sassy text using AI!

## Features

- 🎤 **Record Cat Meows**: Upload or record audio files
- 🧠 **AI Translation**: Uses local LLM (Mistral) for translation
- 😸 **Personality Modes**: Diva, Chill, and Old Man personalities
- 💬 **Conversation Memory**: Each personality remembers past meows
- 🎯 **Smart Detection**: Detects silent audio and invalid files

## Quick Start

### Backend Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up local LLM** (Ollama):
   ```bash
   # Install Ollama (if not already installed)
   brew install ollama
   
   # Start Ollama and pull model
   ollama serve &
   ollama pull mistral:latest
   ```

3. **Start backend**:
   ```bash
   python app.py
   ```
   Backend runs on `http://localhost:3001`

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start frontend**:
   ```bash
   npm start
   ```
   Frontend runs on `http://localhost:3002`

## API Endpoints

- `POST /api/v1/translate` - Translate cat meow to text
- `POST /api/v1/classify` - Classify meow type
- `GET /api/v1/personalities` - Get available personalities
- `GET /api/v1/memory/stats` - Get conversation memory stats

## Tech Stack

- **Backend**: FastAPI, LangChain, librosa, Ollama
- **Frontend**: React, TypeScript, MediaRecorder API
- **AI**: Mistral 7B (local LLM)

## Project Structure

```
Meow2Text/
├── backend/
│   └── src/
│       ├── api/          # FastAPI routes
│       ├── core/         # Configuration & exceptions
│       ├── models/       # Pydantic schemas
│       └── services/     # Audio, classification, translation
├── frontend/
│   └── src/
│       ├── components/   # React components
│       ├── services/     # API calls
│       └── types/        # TypeScript interfaces
└── requirements.txt
```

## Environment Variables

Create `.env` file:
```env
LLM_PROVIDER=local
LOCAL_MODEL=mistral:latest
HOST=0.0.0.0
PORT=3001
```

## License

MIT License 