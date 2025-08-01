# 🐱 Meow2Text Setup Guide

This guide will help you set up and run the Meow2Text application step by step.

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Node.js 14+** and npm installed
- **OpenAI API key** (get one from [OpenAI Platform](https://platform.openai.com/api-keys))

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd Meow2Text
   ```

2. **Run the setup script**:
   ```bash
   python setup.py
   ```

3. **Follow the interactive prompts** to configure and start the application.

### Option 2: Manual Setup

#### Step 1: Backend Setup

1. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**:
   ```bash
   cp env.example .env
   ```

4. **Add your OpenAI API key**:
   Edit `.env` file and replace `your_openai_api_key_here` with your actual API key.

5. **Start the backend server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Step 2: Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the frontend development server**:
   ```bash
   npm start
   ```

## 🌐 Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🧪 Testing the Application

### Test Backend Endpoints

1. **Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Get Personalities**:
   ```bash
   curl http://localhost:8000/personalities
   ```

3. **Test Classification** (with audio file):
   ```bash
   curl -X POST -F "file=@your_audio_file.wav" http://localhost:8000/classify
   ```

### Test Frontend

1. Open http://localhost:3000 in your browser
2. Click the microphone button to record audio
3. Choose a personality (Diva, Chill, or Old Man)
4. View the translation results

## 📁 Project Structure

```
Meow2Text/
├── main.py                 # FastAPI main application
├── requirements.txt        # Python dependencies
├── setup.py               # Automated setup script
├── .env                   # Environment variables (create this)
├── env.example            # Environment template
├── utils/                 # Backend utilities
│   ├── audio.py          # Audio processing
│   ├── classification.py # Meow classification
│   └── translation.py    # LangChain translation
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API services
│   │   └── types.ts      # TypeScript types
│   └── package.json      # Node.js dependencies
└── README.md             # Project documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required: Your OpenAI API key
OPENAI_API_KEY=your_actual_api_key_here

# Optional: Server configuration
HOST=0.0.0.0
PORT=8000

# Optional: CORS settings
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /personalities` - Get available personalities
- `POST /classify` - Classify audio file
- `POST /translate` - Translate audio with personality

## 🐛 Troubleshooting

### Common Issues

1. **"uvicorn not found"**:
   - Make sure virtual environment is activated: `source venv/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

2. **"OpenAI API key not found"**:
   - Create `.env` file: `cp env.example .env`
   - Add your API key to `.env` file

3. **"npm command not found"**:
   - Install Node.js from https://nodejs.org/
   - Verify installation: `node --version && npm --version`

4. **"Port already in use"**:
   - Change port in `.env` file or kill existing process
   - Use different port: `uvicorn main:app --port 8001`

5. **"CORS errors"**:
   - Check `ALLOWED_ORIGINS` in `.env` file
   - Ensure frontend is running on correct port

### Getting Help

1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure virtual environment is activated
4. Check that both servers are running

## 🎯 Next Steps

Once the application is running:

1. **Test with real cat meows** - Record your cat's meows
2. **Try different personalities** - Experiment with Diva, Chill, and Old Man
3. **Improve the model** - Add more training data for better classification
4. **Add features** - Implement conversation memory, multiple cats, etc.

## 📝 Development

### Adding New Features

1. **Backend**: Add new endpoints in `main.py`
2. **Frontend**: Create new components in `frontend/src/components/`
3. **Audio Processing**: Extend `utils/audio.py`
4. **Classification**: Improve `utils/classification.py`
5. **Translation**: Enhance `utils/translation.py`

### Code Style

- **Python**: Follow PEP 8 guidelines
- **TypeScript**: Use strict mode and proper typing
- **React**: Use functional components with hooks
- **API**: Follow RESTful conventions

## 🚀 Deployment

For production deployment:

1. **Build frontend**: `cd frontend && npm run build`
2. **Set up production server** (nginx, Apache, etc.)
3. **Use production WSGI server** (gunicorn, uvicorn workers)
4. **Set up environment variables** securely
5. **Configure SSL certificates**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy coding! 🐱✨** 