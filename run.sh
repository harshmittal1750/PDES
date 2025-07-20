#!/bin/bash

echo ""
echo "================================================"
echo " PDF Data Extractor - Secure Local Tool"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed."
    echo "Please install Python 3.8+ from: https://python.org/downloads/"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "On macOS, you can also install via Homebrew:"
        echo "brew install python"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "On Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-tk"
        echo "On CentOS/RHEL: sudo yum install python3 python3-pip tkinter"
    fi
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "pdf_extractor_env" ]; then
    echo "🔧 Setting up virtual environment..."
    python3 -m venv pdf_extractor_env
    
    echo "📦 Installing dependencies..."
    source pdf_extractor_env/bin/activate
    pip install -r requirements.txt
    
    echo "✅ Setup complete!"
    echo ""
fi

# Activate virtual environment and run
echo "🚀 Starting PDF Data Extractor..."
echo ""
source pdf_extractor_env/bin/activate
python pdf_extractor.py

echo ""
echo "Press Enter to close..."
read -r 