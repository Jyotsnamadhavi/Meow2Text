#!/usr/bin/env python3
"""
Test script for local LLM setup.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def test_local_llm():
    """Test local LLM functionality."""
    try:
        print("🤖 Testing local LLM setup...")
        
        # Test Ollama connection
        llm = OllamaLLM(model="mistral:latest", temperature=0.8)
        
        # Simple test prompt
        prompt = PromptTemplate(
            input_variables=["meow_type"],
            template="Translate this cat meow into funny text: {meow_type}"
        )
        
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Test with a simple meow
        result = chain.run({"meow_type": "hungry meow"})
        
        print("✅ Local LLM is working!")
        print(f"Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Local LLM test failed: {str(e)}")
        print("💡 Make sure Ollama is running and llama2:7b model is downloaded")
        return False

if __name__ == "__main__":
    test_local_llm() 