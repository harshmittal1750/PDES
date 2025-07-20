#!/usr/bin/env python3
"""
PDF Data Extractor Launcher
Simple launcher script that checks dependencies and starts the application.
"""

import sys
import subprocess
import importlib
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        print("\nPlease install Python 3.8+ from: https://python.org/downloads/")
        return False
    print(f"✅ Python version OK: {sys.version.split()[0]}")
    return True

def check_and_install_dependencies():
    """Check if required packages are installed, install if missing"""
    required_packages = {
        'pdfplumber': 'pdfplumber==0.11.0',
        'openpyxl': 'openpyxl==3.1.2', 
        'pandas': 'pandas==2.2.2',
        'tkinter': None  # Built-in, just check
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            if package == 'tkinter':
                import tkinter
                print(f"✅ {package} is available")
            else:
                importlib.import_module(package)
                print(f"✅ {package} is installed")
        except ImportError:
            if package == 'tkinter':
                print(f"❌ {package} is not available. Please install tkinter for your system.")
                print("On Ubuntu/Debian: sudo apt-get install python3-tk")
                print("On CentOS/RHEL: sudo yum install tkinter")
                print("On macOS: tkinter should be included with Python")
                return False
            else:
                print(f"⚠️  {package} is missing")
                missing_packages.append(pip_name)
    
    if missing_packages:
        print("\n🔧 Installing missing packages...")
        try:
            for package in missing_packages:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("\nTry running manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    print("✅ All dependencies are ready!")
    return True

def run_application():
    """Run the main PDF extractor application"""
    try:
        print("\n🚀 Starting PDF Data Extractor...")
        
        # Import and run the main application
        if os.path.exists('pdf_extractor.py'):
            import pdf_extractor
            pdf_extractor.main()
        else:
            print("❌ Error: pdf_extractor.py not found!")
            print("Make sure you're running this script from the correct directory.")
            return False
            
    except KeyboardInterrupt:
        print("\n\n👋 Application closed by user.")
        return True
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\nTry running the application directly:")
        print("python pdf_extractor.py")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("=" * 50)
    print("📄 PDF Data Extractor - Secure Local Tool")
    print("=" * 50)
    print()
    
    # Check Python version
    if not check_python_version():
        input("\nPress Enter to exit...")
        return
    
    # Check and install dependencies
    print("\n🔍 Checking dependencies...")
    if not check_and_install_dependencies():
        input("\nPress Enter to exit...")
        return
    
    # Run the application
    if not run_application():
        input("\nPress Enter to exit...")
        return
    
    print("\n✅ Application finished successfully.")

if __name__ == "__main__":
    main() 