@echo off
title PDF Data Extractor
echo.
echo ================================================
echo  PDF Data Extractor - Secure Local Tool
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo Please install Python 3.8+ from: https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist "pdf_extractor_env" (
    echo 🔧 Setting up virtual environment...
    python -m venv pdf_extractor_env
    
    echo 📦 Installing dependencies...
    call pdf_extractor_env\Scripts\activate
    pip install -r requirements.txt
    
    echo ✅ Setup complete!
    echo.
)

REM Activate virtual environment and run
echo 🚀 Starting PDF Data Extractor...
echo.
call pdf_extractor_env\Scripts\activate
python pdf_extractor.py

echo.
echo Press any key to close...
pause >nul 