#!/usr/bin/env python3
"""
Build script for PDF Data Extractor standalone application - Windows Version
Creates a bundled executable with OCR support for Windows
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def find_tesseract_path_windows():
    """Find Tesseract installation path on Windows"""
    try:
        # Try common Windows locations
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\%USERNAME%\AppData\Local\Tesseract-OCR\tesseract.exe",
            r"C:\tesseract\tesseract.exe",
        ]
        
        for path in possible_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                return expanded_path
        
        # Try using where command (Windows equivalent of which)
        try:
            result = subprocess.run(["where", "tesseract"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
            
    except Exception as e:
        print(f"Error finding tesseract: {e}")
    
    return None

def find_tesseract_data_windows():
    """Find Tesseract data directory on Windows"""
    try:
        # Get tessdata directory from tesseract
        result = subprocess.run(["tesseract", "--print-parameters"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'tessdata' in line and 'prefix' in line.lower():
                    # Extract path from parameter line
                    parts = line.split()
                    for part in parts:
                        if 'tessdata' in part and os.path.exists(part):
                            return part
        
        # Try common Windows data locations
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tessdata",
            r"C:\Program Files (x86)\Tesseract-OCR\tessdata",
            r"C:\Users\%USERNAME%\AppData\Local\Tesseract-OCR\tessdata",
            r"C:\tesseract\tessdata",
        ]
        
        for path in possible_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                return expanded_path
                
    except Exception as e:
        print(f"Error finding tessdata: {e}")
    
    return None

def create_spec_file_windows():
    """Create PyInstaller spec file with proper configuration for Windows"""
    
    tesseract_bin = find_tesseract_path_windows()
    tessdata_dir = find_tesseract_data_windows()
    
    print(f"Tesseract binary: {tesseract_bin}")
    print(f"Tessdata directory: {tessdata_dir}")
    
    if not tesseract_bin:
        print("⚠️  Warning: Tesseract binary not found. OCR may not work in bundled app.")
        print("💡 Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
    
    if not tessdata_dir:
        print("⚠️  Warning: Tessdata directory not found. OCR may not work in bundled app.")
    
    # Build the spec file content for Windows
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Additional files to include
added_files = []

# Add tesseract binary if found
tesseract_bin = r"{tesseract_bin}"
if tesseract_bin and tesseract_bin != "None" and tesseract_bin != "r\\"None\\"":
    added_files.append((tesseract_bin, 'tesseract/'))

# Add tessdata directory if found  
tessdata_dir = r"{tessdata_dir}"
if tessdata_dir and tessdata_dir != "None" and tessdata_dir != "r\\"None\\"":
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
    icon=None,  # Add .ico file here if you have one
)
'''
    
    # Write spec file
    with open('pdf_extractor_windows.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created pdf_extractor_windows.spec file")
    return True

def build_application_windows():
    """Build the standalone application for Windows"""
    print("\n🔨 Building Windows standalone application...")
    
    try:
        # Clean previous builds
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        
        # Build with PyInstaller
        cmd = ["pyinstaller", "--clean", "pdf_extractor_windows.spec"]
        result = subprocess.run(cmd, check=True, shell=True)
        
        print("✅ Build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_launcher_batch():
    """Create a Windows batch launcher script"""
    launcher_content = '''@echo off
REM PDF Data Extractor Launcher for Windows
echo Starting PDF Data Extractor...

REM Get the directory of this script
set "DIR=%~dp0"

REM Set TESSDATA_PREFIX for OCR
set "TESSDATA_PREFIX=%DIR%tessdata\\"

REM Launch the application
"%DIR%PDF_Data_Extractor.exe"

REM Keep window open if there's an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application encountered an error. Press any key to close.
    pause >nul
)
'''
    
    os.makedirs('dist', exist_ok=True)
    with open('dist/launch_pdf_extractor.bat', 'w') as f:
        f.write(launcher_content)
    
    print("✅ Created Windows launcher script")

def create_installer_script():
    """Create NSIS installer script for professional Windows distribution"""
    installer_content = '''# PDF Data Extractor Windows Installer
# Generated by build system

!define APP_NAME "PDF Data Extractor"
!define COMP_NAME "PDF Processing Tools"
!define WEB_SITE "https://github.com/yourrepo/pdf-extractor"
!define VERSION "1.0.0.0"
!define COPYRIGHT "© 2025 PDF Processing Tools"
!define DESCRIPTION "Extract and search data from PDF files with OCR support"
!define INSTALLER_NAME "PDF_Data_Extractor_Setup.exe"
!define MAIN_APP_EXE "PDF_Data_Extractor.exe"
!define INSTALL_TYPE "SetShellVarContext current"
!define REG_ROOT "HKCU"
!define REG_APP_PATH "Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\${MAIN_APP_EXE}"
!define UNINSTALL_PATH "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}"

!include "MUI2.nsh"

VIProductVersion  "${VERSION}"
VIAddVersionKey "ProductName"  "${APP_NAME}"
VIAddVersionKey "CompanyName"  "${COMP_NAME}"
VIAddVersionKey "LegalCopyright"  "${COPYRIGHT}"
VIAddVersionKey "FileDescription"  "${DESCRIPTION}"
VIAddVersionKey "FileVersion"  "${VERSION}"

SetCompressor ZLIB
Name "${APP_NAME}"
Caption "${APP_NAME}"
OutFile "${INSTALLER_NAME}"
BrandingText "${APP_NAME}"
XPStyle on
InstallDir "C:\\Program Files\\${APP_NAME}"

# Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "app.ico"
!define MUI_UNICON "app.ico"

# Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

# Languages
!insertmacro MUI_LANGUAGE "English"

Section -MainProgram
${INSTALL_TYPE}
SetOverwrite ifnewer
SetOutPath "$INSTDIR"
File "dist\\PDF_Data_Extractor.exe"
File "dist\\launch_pdf_extractor.bat"
File /r "dist\\*"
SectionEnd

Section -Icons_Reg
SetOutPath "$INSTDIR"
WriteUninstaller "$INSTDIR\\uninstall.exe"

# Start Menu
!ifdef REG_START_MENU
!insertmacro MUI_STARTMENU_WRITE_BEGIN Application
CreateDirectory "$SMPROGRAMS\\$SM_Folder"
CreateShortCut "$SMPROGRAMS\\$SM_Folder\\${APP_NAME}.lnk" "$INSTDIR\\${MAIN_APP_EXE}"
CreateShortCut "$DESKTOP\\${APP_NAME}.lnk" "$INSTDIR\\${MAIN_APP_EXE}"
CreateShortCut "$SMPROGRAMS\\$SM_Folder\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
!insertmacro MUI_STARTMENU_WRITE_END
!endif

# Registry
WriteRegStr ${REG_ROOT} "${REG_APP_PATH}" "" "$INSTDIR\\${MAIN_APP_EXE}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayName" "${APP_NAME}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "UninstallString" "$INSTDIR\\uninstall.exe"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayIcon" "$INSTDIR\\${MAIN_APP_EXE}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayVersion" "${VERSION}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "Publisher" "${COMP_NAME}"
SectionEnd

Section Uninstall
${INSTALL_TYPE}
Delete "$INSTDIR\\${MAIN_APP_EXE}"
Delete "$INSTDIR\\launch_pdf_extractor.bat"
Delete "$INSTDIR\\uninstall.exe"

RmDir /r "$INSTDIR"

DeleteRegKey ${REG_ROOT} "${REG_APP_PATH}"
DeleteRegKey ${REG_ROOT} "${UNINSTALL_PATH}"
SectionEnd
'''
    
    with open('installer.nsi', 'w') as f:
        f.write(installer_content)
    
    print("✅ Created NSIS installer script")

def create_readme_windows():
    """Create README for Windows distribution"""
    readme_content = '''# PDF Data Extractor - Windows Version

## 🚀 Quick Start

### Windows 10/11:
1. Double-click "PDF_Data_Extractor.exe" 
   OR
2. Run "launch_pdf_extractor.bat"

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
- Try running "launch_pdf_extractor.bat"
- Check that Windows didn't block the executable
- Run as Administrator if needed

**Windows Security Warning?**
- Click "More info" → "Run anyway"
- The app is safe but not digitally signed

**OCR not working?**
- OCR engine is bundled and should work automatically
- Check that input PDFs contain readable text/images

**Slow processing?**
- OCR takes longer than normal text extraction
- Progress bar shows current status
- Large batches with many scanned PDFs will take time

## 📞 Support

For issues or questions, refer to the full documentation included.

---
**Built with security in mind - all processing happens locally on your machine.**
'''
    
    with open('dist/README_Windows.txt', 'w') as f:
        f.write(readme_content)
    
    print("✅ Created Windows distribution README")

def main():
    """Main build process for Windows"""
    print("🏗️  PDF Data Extractor - Windows Standalone App Builder")
    print("=" * 50)
    
    # Check platform
    if platform.system() != "Windows":
        print("⚠️  Warning: Building on non-Windows platform.")
        print("💡 For best results, run this script on Windows with:")
        print("   1. Python 3.8+ installed")
        print("   2. PyInstaller installed (pip install pyinstaller)")
        print("   3. Tesseract OCR installed")
        print("   4. All project dependencies installed")
        print()
    
    # Check if we're in the right directory
    if not os.path.exists('pdf_extractor.py'):
        print("❌ Error: pdf_extractor.py not found. Run this script from the project directory.")
        return False
    
    # Step 1: Create spec file
    if not create_spec_file_windows():
        return False
    
    # Step 2: Build application
    if not build_application_windows():
        return False
    
    # Step 3: Create additional files
    create_launcher_batch()
    create_installer_script()
    create_readme_windows()
    
    # Step 4: Show results
    print("\n🎉 Windows standalone application created successfully!")
    print("\n📁 Distribution files:")
    if os.path.exists('dist'):
        for item in os.listdir('dist'):
            print(f"   📄 {item}")
    
    print(f"\n🚀 Your Windows app is ready:")
    print(f"   📍 Location: ./dist/")
    print(f"   🖥️  Run: ./dist/PDF_Data_Extractor.exe")
    print(f"   📋 Or: ./dist/launch_pdf_extractor.bat")
    
    print("\n💼 To distribute to Windows users:")
    print("   1. Zip the entire 'dist' folder")
    print("   2. Users extract and double-click the .exe file")
    print("   3. No Python or dependencies needed!")
    print("   4. Optional: Use installer.nsi to create professional installer")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 