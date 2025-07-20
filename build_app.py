#!/usr/bin/env python3
"""
Build script for PDF Data Extractor standalone application
Creates a bundled executable with OCR support
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def find_tesseract_path():
    """Find Tesseract installation path"""
    try:
        # Try common locations
        possible_paths = [
            "/opt/homebrew/bin/tesseract",  # Apple Silicon Homebrew
            "/usr/local/bin/tesseract",     # Intel Homebrew
            "/usr/bin/tesseract",           # System install
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Try using which command
        result = subprocess.run(["which", "tesseract"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
            
    except Exception as e:
        print(f"Error finding tesseract: {e}")
    
    return None

def find_tesseract_data():
    """Find Tesseract data directory"""
    try:
        # Get tessdata directory from tesseract
        result = subprocess.run(["tesseract", "--print-parameters"], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'tessdata' in line and 'prefix' in line:
                    # Extract path from parameter line
                    parts = line.split()
                    for part in parts:
                        if 'tessdata' in part and os.path.exists(part):
                            return part
        
        # Try common data locations
        possible_paths = [
            "/opt/homebrew/share/tessdata",     # Apple Silicon Homebrew
            "/usr/local/share/tessdata",        # Intel Homebrew  
            "/usr/share/tessdata",              # System install
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
    except Exception as e:
        print(f"Error finding tessdata: {e}")
    
    return None

def create_spec_file():
    """Create PyInstaller spec file with proper configuration"""
    
    tesseract_bin = find_tesseract_path()
    tessdata_dir = find_tesseract_data()
    
    print(f"Tesseract binary: {tesseract_bin}")
    print(f"Tessdata directory: {tessdata_dir}")
    
    if not tesseract_bin:
        print("⚠️  Warning: Tesseract binary not found. OCR may not work in bundled app.")
    
    if not tessdata_dir:
        print("⚠️  Warning: Tessdata directory not found. OCR may not work in bundled app.")
    
    # Build the spec file content
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Additional files to include
added_files = []

# Add tesseract binary if found
tesseract_bin = "{tesseract_bin}"
if tesseract_bin and tesseract_bin != "None":
    added_files.append((tesseract_bin, 'tesseract/'))

# Add tessdata directory if found  
tessdata_dir = "{tessdata_dir}"
if tessdata_dir and tessdata_dir != "None":
    added_files.append((tessdata_dir, 'tessdata/'))

a = Analysis(
    ['pdf_extractor.py'],
    pathex=[],
    binaries=added_files,
    datas=[
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('OCR_GUIDE.md', '.'),
    ],
    hiddenimports=[
        'pdfplumber',
        'openpyxl', 
        'pandas',
        'pytesseract',
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        '_tkinter',
        'pkg_resources.py2_warn',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF_Data_Extractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Create app bundle for macOS
app = BUNDLE(
    exe,
    name='PDF Data Extractor.app',
    icon=None,
    bundle_identifier='com.pdfextractor.app',
)
'''
    
    # Write spec file
    with open('pdf_extractor.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created pdf_extractor.spec file")
    return True

def build_application():
    """Build the standalone application"""
    print("\n🔨 Building standalone application...")
    
    try:
        # Clean previous builds
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        
        # Build with PyInstaller
        cmd = ["pyinstaller", "--clean", "pdf_extractor.spec"]
        result = subprocess.run(cmd, check=True)
        
        print("✅ Build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_launcher_script():
    """Create a simple launcher script"""
    launcher_content = '''#!/bin/bash

# PDF Data Extractor Launcher
echo "Starting PDF Data Extractor..."

# Get the directory of this script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set TESSDATA_PREFIX for OCR
export TESSDATA_PREFIX="$DIR/tessdata/"

# Launch the application
"$DIR/PDF_Data_Extractor"
'''
    
    with open('dist/launch_pdf_extractor.sh', 'w') as f:
        f.write(launcher_content)
    
    os.chmod('dist/launch_pdf_extractor.sh', 0o755)
    print("✅ Created launcher script")

def create_readme():
    """Create README for the distribution"""
    readme_content = '''# PDF Data Extractor - Standalone Application

## 🚀 Quick Start

### macOS:
1. Double-click "PDF Data Extractor.app" 
   OR
2. Run "./launch_pdf_extractor.sh" in terminal

### Features:
- ✅ Extract text from any PDF (normal or scanned)
- ✅ OCR support for image-based PDFs  
- ✅ Batch process thousands of files
- ✅ Export to Excel with formatting
- ✅ 100% local processing (secure)

### No Installation Required!
This is a self-contained application with everything bundled:
- Python runtime
- All dependencies
- OCR engine (Tesseract)
- GUI components

## 📖 How to Use

1. **Select PDF files** - Click "Browse Files"
2. **Enter search terms** - One per line in the text box
3. **Configure options** - Case sensitive, OCR settings, etc.
4. **Extract data** - Click "Extract Data" and wait
5. **Export results** - Click "Export to Excel"

## 🔍 OCR Support

The application automatically detects scanned PDFs and uses OCR when needed:
- **Auto OCR** ✅ - Recommended for mixed files
- **Force OCR** - Use for all PDFs (slower but thorough)

## 🛠️ Troubleshooting

**App won't start?**
- Try running from terminal: `./launch_pdf_extractor.sh`
- Check console output for error messages

**OCR not working?**
- OCR engine is bundled and should work automatically
- Check that input PDFs contain readable text/images

**Slow processing?**
- OCR takes longer than normal text extraction
- Progress bar shows current status
- Large batches with many scanned PDFs will take time

## 📞 Support

For issues or questions, refer to the full documentation included with the source code.

---
**Built with security in mind - all processing happens locally on your machine.**
'''
    
    with open('dist/README.txt', 'w') as f:
        f.write(readme_content)
    
    print("✅ Created distribution README")

def main():
    """Main build process"""
    print("🏗️  PDF Data Extractor - Standalone App Builder")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('pdf_extractor.py'):
        print("❌ Error: pdf_extractor.py not found. Run this script from the project directory.")
        return False
    
    # Step 1: Create spec file
    if not create_spec_file():
        return False
    
    # Step 2: Build application
    if not build_application():
        return False
    
    # Step 3: Create additional files
    create_launcher_script()
    create_readme()
    
    # Step 4: Show results
    print("\n🎉 Standalone application created successfully!")
    print("\n📁 Distribution files:")
    if os.path.exists('dist'):
        for item in os.listdir('dist'):
            print(f"   📄 {item}")
    
    print(f"\n🚀 Your standalone app is ready:")
    print(f"   📍 Location: ./dist/")
    print(f"   🖥️  Run: ./dist/PDF\\ Data\\ Extractor.app")
    print(f"   📋 Or: ./dist/launch_pdf_extractor.sh")
    
    print("\n💼 To distribute to users:")
    print("   1. Zip the entire 'dist' folder")
    print("   2. Users extract and double-click the .app file")
    print("   3. No Python or dependencies needed!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 