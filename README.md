# Meow2Text: Translate Your Cat's Meows to Text

A fun AI-powered application that translates cat meows into sassy, personality-driven text using audio classification and LangChain.

## 🎉 Current Status

✅ **Backend**: FastAPI server with audio processing and LangChain integration  
✅ **Frontend**: React application with audio recording and personality selection  
✅ **Audio Processing**: librosa-based audio preprocessing  
✅ **Classification**: Rule-based meow classification system  
✅ **Translation**: LangChain-powered personality-based translation  
✅ **Setup Scripts**: Automated setup and quick start scripts  

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- OpenAI API key

### Option 1: Automated Setup (Recommended)

1. **Add your OpenAI API key**:
   ```bash
   # Edit .env file and replace 'your_openai_api_key_here' with your actual key
   nano .env
   ```

2. **Start the backend**:
   ```bash
   ./quick_start.sh
   ```

3. **In a new terminal, start the frontend**:
   ```bash
   ./start_frontend.sh
   ```

### Option 2: Manual Setup

1. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Start backend**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Start frontend** (in new terminal):
   ```bash
   cd frontend && npm start
   ```

## 🌐 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎯 How to Use

1. **Record Audio**: Click the microphone button and record your cat's meow
2. **Choose Personality**: Select from Diva 👑, Chill 😎, or Old Man 👴
3. **Get Translation**: View the sassy cat translation with analysis

## 🧪 Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get personalities
curl http://localhost:8000/personalities

# Test with audio file
curl -X POST -F "file=@your_audio.wav" http://localhost:8000/translate
```

## 📁 Project Structure

```
Meow2Text/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── setup.py               # Interactive setup script
├── quick_start.sh         # Backend startup script
├── start_frontend.sh      # Frontend startup script
├── utils/                 # Backend utilities
│   ├── audio.py          # Audio processing
│   ├── classification.py # Meow classification
│   └── translation.py    # LangChain translation
├── frontend/             # React application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API services
│   │   └── types.ts      # TypeScript types
│   └── package.json      # Node.js dependencies
└── README.md             # This file
```

## 🔧 Configuration

Create a `.env` file with:
```env
OPENAI_API_KEY=your_actual_api_key_here
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 🎭 Features

- **Audio Recording**: Browser-based audio recording
- **Meow Classification**: 5 categories (hungry, angry, playful, sleepy, attention)
- **Personality System**: 3 distinct cat personalities
- **LangChain Integration**: AI-powered translation
- **Modern UI**: Responsive design with cat-themed styling

## 🐛 Troubleshooting

1. **"uvicorn not found"**: Activate virtual environment with `source venv/bin/activate`
2. **"npm not found"**: Install Node.js from https://nodejs.org/
3. **API key errors**: Add your OpenAI API key to `.env` file
4. **Port conflicts**: Change port in `.env` or kill existing processes

## 📝 Development

- **Backend**: FastAPI with async endpoints
- **Frontend**: React with TypeScript
- **Audio**: librosa for processing, Web Audio API for recording
- **AI**: LangChain with OpenAI GPT for translations

## 🚀 Next Steps

1. **Add your OpenAI API key** to `.env` file
2. **Start both servers** using the quick start scripts
3. **Test with real cat meows**!
4. **Improve the model** with more training data
5. **Add features** like conversation memory, multiple cats, etc.

## 📄 License

MIT License - Have fun with it! 😸

---

**Ready to translate some meows? Start with `./quick_start.sh`! 🐱✨** 