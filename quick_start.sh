#!/bin/bash

echo "🐱 Meow2Text Quick Start"
echo "========================"

# Check if .env exists and has API key
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Creating it..."
    cp env.example .env
fi

# Check if API key is set
if grep -q "your_openai_api_key_here" .env; then
    echo "❌ Please add your OpenAI API key to .env file"
    echo "Edit .env and replace 'your_openai_api_key_here' with your actual API key"
    echo ""
    echo "You can get an API key from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Press Enter after you've added your API key..."
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Start backend
echo "🚀 Starting backend server..."
echo "Backend will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py 