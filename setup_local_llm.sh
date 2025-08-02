#!/bin/bash

echo "🤖 Setting up Local LLM for Meow2Text..."
echo "========================================"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Installing..."
    brew install ollama
else
    echo "✅ Ollama is already installed"
fi

# Start Ollama service
echo "🚀 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
sleep 5

# Check if model is already downloaded
echo "📦 Checking for llama2:7b model..."
if ollama list | grep -q "llama2:7b"; then
    echo "✅ llama2:7b model is already downloaded"
else
    echo "📥 Downloading llama2:7b model (this may take a while)..."
    ollama pull llama2:7b
fi

# Test the setup
echo "🧪 Testing local LLM setup..."
source venv/bin/activate
python test_local_llm.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Local LLM setup complete!"
    echo "You can now run the application without an OpenAI API key."
    echo ""
    echo "To start the backend:"
    echo "  source venv/bin/activate && python app.py"
    echo ""
    echo "To start the frontend:"
    echo "  cd frontend && PORT=3002 npm start"
else
    echo ""
    echo "❌ Setup failed. Please check the error messages above."
fi

# Clean up
kill $OLLAMA_PID 2>/dev/null 