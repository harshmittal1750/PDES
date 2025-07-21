#!/bin/bash

# IDP Enhanced PDF Data Extractor Launcher
# This script automatically activates the virtual environment and launches the application

echo "🎯 Launching IDP Enhanced PDF Data Extractor..."
echo "📦 Activating virtual environment..."

# Check if virtual environment exists
if [ ! -d "pdf_extractor_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment and run application
source pdf_extractor_env/bin/activate

echo "✅ Virtual environment activated"
echo "🚀 Starting PDF Data Extractor with IDP/ICR capabilities..."
echo ""
echo "Available modes:"
echo "  🏢 Insurance Mode: Enhanced extraction for 15 insurance fields"
echo "  🎯 IDP Mode: 100% Accuracy + Shows all unmatched data"
echo "  📄 Normal Mode: Traditional search functionality"
echo ""
echo "Application starting..."

python pdf_extractor.py 