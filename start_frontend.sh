#!/bin/bash

echo "🐱 Meow2Text Frontend"
echo "====================="

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found. Please run this from the project root."
    exit 1
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start frontend
echo "🚀 Starting frontend development server..."
echo "Frontend will be available at: http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""

cd frontend
npm start 