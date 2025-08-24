#!/bin/bash

# setup.sh

echo "--- 🤖 Setting up GitHub Repo Analyzer Agent ---"

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Please install Python and pip first."
    exit
fi

# Install required Python packages
echo "--- Installing Python packages from requirements.txt ---"
pip install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null
then
    echo "--- WARNING: Ollama is not installed or not in the system's PATH.---"
    echo "Please install Ollama from https://ollama.com/ to run the application."
    exit
fi

# Pull the default LLM
echo "--- Pulling the default LLM (llama3:8b) from Ollama... ---"
ollama pull llama3:8b

echo "--- ✅ Setup complete! ---"
echo "You can now run the application with: python app_core.py"