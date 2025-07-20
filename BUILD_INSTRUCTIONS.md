# 🏗️ **Building for Windows & macOS**

This guide shows how to create **standalone executable files** for both Windows and macOS platforms.

## 🎯 **What You'll Create**

### 🪟 **Windows Version**

- **`PDF_Data_Extractor.exe`** - Standalone Windows executable
- **`PDF_Data_Extractor_vXXXX_Windows.zip`** - Distribution package
- **`PDF_Data_Extractor_Setup.exe`** - Professional installer (optional)

### 🍎 **macOS Version**

- **`PDF Data Extractor.app`** - macOS application bundle
- **`PDF_Data_Extractor_vXXXX_macOS.dmg`** - Professional disk image
- **`PDF_Data_Extractor_vXXXX_macOS.zip`** - Universal package

---

## 🪟 **Building for Windows**

### **Prerequisites (Windows Only)**

1. **Windows 10/11** (32-bit or 64-bit)
2. **Python 3.8+** installed from [python.org](https://python.org)
3. **Tesseract OCR** installed from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### **Step 1: Setup Environment (Windows)**

```cmd
# Clone/download your project files
cd C:\your-project-folder

# Create virtual environment
python -m venv pdf_extractor_env

# Activate environment
pdf_extractor_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### **Step 2: Install Tesseract (Windows)**

```cmd
# Download and install from:
# https://github.com/UB-Mannheim/tesseract/wiki

# Default install location:
# C:\Program Files\Tesseract-OCR\tesseract.exe

# Verify installation
tesseract --version
```

### **Step 3: Build Windows Executable**

```cmd
# Activate environment
pdf_extractor_env\Scripts\activate

# Build the application
python build_app_windows.py

# This creates:
# - dist\PDF_Data_Extractor.exe
# - dist\launch_pdf_extractor.bat
# - Various supporting files
```

### **Step 4: Create Windows Distribution**

```cmd
# Create distribution packages
python create_distribution_windows.py

# This creates:
# - PDF_Data_Extractor_vXXXX_Windows.zip
# - Windows user guide
# - Cross-platform README
```

### **Step 5: Optional - Create Windows Installer**

```cmd
# Install NSIS from: https://nsis.sourceforge.io/
# Then run:
makensis installer.nsi

# This creates:
# - PDF_Data_Extractor_Setup.exe
```

---

## 🍎 **Building for macOS**

### **Prerequisites (macOS Only)**

1. **macOS 10.14+** (Intel or Apple Silicon)
2. **Python 3.8+** via Homebrew
3. **Tesseract OCR** via Homebrew

### **Step 1: Setup Environment (macOS)**

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and dependencies
brew install python python-tk tesseract

# Navigate to project
cd ~/your-project-folder

# Create virtual environment
python3 -m venv pdf_extractor_env

# Activate environment
source pdf_extractor_env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### **Step 2: Build macOS Application**

```bash
# Activate environment
source pdf_extractor_env/bin/activate

# Build the application
python build_app.py

# This creates:
# - dist/PDF Data Extractor.app
# - dist/launch_pdf_extractor.sh
# - Various supporting files
```

### **Step 3: Create macOS Distribution**

```bash
# Create distribution packages
python create_distribution.py

# This creates:
# - PDF_Data_Extractor_vXXXX_macOS.dmg
# - PDF_Data_Extractor_vXXXX_macOS.zip
# - User guide and documentation
```

---

## 🌐 **Cross-Platform Building Strategy**

### **Option 1: Build on Each Platform (Recommended)**

- Use **Windows PC** to build `.exe` files
- Use **Mac** to build `.app` files
- **Best compatibility** and **smallest file sizes**

### **Option 2: Cloud/CI Building**

- Use **GitHub Actions** or **similar CI service**
- Build both platforms automatically
- Requires setup but **automated releases**

### **Option 3: Virtual Machines**

- Run **Windows VM on Mac** (or vice versa)
- Build both platforms from one machine
- **More complex** but **single-machine solution**

---

## 📋 **Build Checklist**

### **Before Building:**

- [ ] All source files present (`pdf_extractor.py`, etc.)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] OCR engine installed and working
- [ ] Virtual environment activated
- [ ] PyInstaller installed (`pip install pyinstaller`)

### **Windows Build:**

- [ ] `python build_app_windows.py` completed successfully
- [ ] `dist\PDF_Data_Extractor.exe` exists and runs
- [ ] `python create_distribution_windows.py` completed
- [ ] ZIP package created and tested

### **macOS Build:**

- [ ] `python build_app.py` completed successfully
- [ ] `dist/PDF Data Extractor.app` exists and runs
- [ ] `python create_distribution.py` completed
- [ ] DMG/ZIP packages created and tested

### **Distribution Ready:**

- [ ] Windows ZIP file tested on clean Windows PC
- [ ] macOS DMG tested on clean Mac
- [ ] User guides included
- [ ] Documentation complete
- [ ] Security warnings documented

---

## 🛠️ **Troubleshooting**

### **Common Windows Issues:**

**"Tesseract not found"**

```cmd
# Install from: https://github.com/UB-Mannheim/tesseract/wiki
# Or manually set path:
set PATH=%PATH%;C:\Program Files\Tesseract-OCR
```

**"PyInstaller failed"**

```cmd
# Try these fixes:
pip install --upgrade pyinstaller
# Or:
pip install pyinstaller==5.13.2
```

**"DLL load failed"**

```cmd
# Install Visual C++ Redistributable:
# https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist
```

### **Common macOS Issues:**

**"Tesseract not found"**

```bash
# Install via Homebrew:
brew install tesseract

# Or set path manually:
export PATH="/opt/homebrew/bin:$PATH"  # Apple Silicon
export PATH="/usr/local/bin:$PATH"     # Intel
```

**"Python not found"**

```bash
# Install Python via Homebrew:
brew install python python-tk

# Use python3 explicitly:
python3 build_app.py
```

**"App won't start"**

```bash
# Check console for errors:
open -a Console
# Look for PDF Data Extractor entries
```

---

## 🚀 **Distribution Best Practices**

### **For Windows:**

1. **Test on clean Windows 10/11** (fresh VM if possible)
2. **Include clear instructions** for security warnings
3. **Provide both ZIP and installer** options
4. **Test with Windows Defender** active

### **For macOS:**

1. **Test on both Intel and Apple Silicon** Macs
2. **Include Gatekeeper bypass** instructions
3. **Provide both DMG and ZIP** options
4. **Test on latest macOS version**

### **For Both:**

1. **Document security warnings** - apps are safe but unsigned
2. **Include comprehensive user guides**
3. **Provide troubleshooting steps**
4. **Test with real PDF files** including scanned ones
5. **Verify OCR functionality** works in bundled apps

---

## 💼 **Ready for Production!**

Following these instructions will give you:

- ✅ **Professional standalone executables** for both platforms
- ✅ **Complete distribution packages** ready to upload
- ✅ **User-friendly installers** with documentation
- ✅ **Cross-platform compatibility**
- ✅ **Zero dependencies** for end users
- ✅ **OCR support** built-in and working

**Your PDF processing tool is ready for the world! 🌍**
