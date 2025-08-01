#!/usr/bin/env python3
"""
Meow2Text Setup Script
This script helps you set up and run the Meow2Text application.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_virtual_environment():
    """Check if virtual environment is activated."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
        return True
    else:
        print("❌ Virtual environment is not activated")
        print("Please run: source venv/bin/activate")
        return False

def check_env_file():
    """Check if .env file exists and has OpenAI API key."""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("Creating .env file...")
        create_env_file()
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        if 'your_openai_api_key_here' in content:
            print("❌ Please add your OpenAI API key to .env file")
            print("Edit .env and replace 'your_openai_api_key_here' with your actual API key")
            return False
    
    print("✅ .env file configured")
    return True

def create_env_file():
    """Create .env file with template."""
    env_content = """# OpenAI API Key - Replace with your actual API key
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
"""
    with open(".env", "w") as f:
        f.write(env_content)
    print("✅ .env file created")

def check_dependencies():
    """Check if all dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import langchain
        import openai
        import librosa
        print("✅ All Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_frontend():
    """Check if frontend dependencies are installed."""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("❌ Frontend dependencies not installed")
        print("Please run: cd frontend && npm install")
        return False
    
    print("✅ Frontend dependencies are installed")
    return True

def run_backend():
    """Start the backend server."""
    print("\n🚀 Starting backend server...")
    print("Backend will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n✅ Backend server stopped")

def run_frontend():
    """Start the frontend development server."""
    print("\n🚀 Starting frontend server...")
    print("Frontend will be available at: http://localhost:3000")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run(["npm", "start"], cwd="frontend")
    except KeyboardInterrupt:
        print("\n✅ Frontend server stopped")

def main():
    """Main setup function."""
    print("🐱 Meow2Text Setup Script")
    print("=" * 40)
    
    # Check requirements
    checks = [
        check_python_version(),
        check_virtual_environment(),
        check_dependencies(),
        check_env_file(),
        check_frontend()
    ]
    
    if not all(checks):
        print("\n❌ Setup incomplete. Please fix the issues above.")
        return
    
    print("\n✅ All checks passed!")
    print("\n🎯 What would you like to do?")
    print("1. Start backend server")
    print("2. Start frontend server")
    print("3. Start both servers (in separate terminals)")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_backend()
            break
        elif choice == "2":
            run_frontend()
            break
        elif choice == "3":
            print("\n📝 To run both servers:")
            print("Terminal 1: python setup.py (choose option 1)")
            print("Terminal 2: python setup.py (choose option 2)")
            break
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main() 