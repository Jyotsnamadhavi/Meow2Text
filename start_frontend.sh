#!/bin/bash

echo "🐱 Starting Meow2Text Frontend..."
echo "================================"

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found. Please run this script from the project root."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

echo "🚀 Starting React development server on port 3002..."
echo "Frontend will be available at: http://localhost:3002"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the frontend on port 3002
PORT=3002 npm start 