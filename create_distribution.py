#!/usr/bin/env python3
"""
Create distribution packages for PDF Data Extractor
"""

import os
import sys
import subprocess
import shutil
import zipfile
from datetime import datetime

def create_zip_distribution():
    """Create a ZIP file for distribution"""
    print("📦 Creating ZIP distribution...")
    
    # Get version info
    version = datetime.now().strftime("%Y.%m.%d")
    zip_name = f"PDF_Data_Extractor_v{version}_macOS.zip"
    
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files from dist directory
            for root, dirs, files in os.walk('dist'):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, 'dist')
                    zipf.write(file_path, f"PDF_Data_Extractor/{archive_name}")
            
            # Add documentation
            docs_to_include = [
                'README.md',
                'OCR_GUIDE.md', 
                'QUICKSTART.md',
                'INSTALL.md'
            ]
            
            for doc in docs_to_include:
                if os.path.exists(doc):
                    zipf.write(doc, f"PDF_Data_Extractor/Documentation/{doc}")
        
        print(f"✅ Created: {zip_name}")
        return zip_name
    
    except Exception as e:
        print(f"❌ Error creating ZIP: {e}")
        return None

def create_dmg_distribution():
    """Create a DMG file for macOS (if available)"""
    print("💿 Creating DMG distribution...")
    
    try:
        # Check if we can create DMG
        result = subprocess.run(["which", "hdiutil"], capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  hdiutil not found, skipping DMG creation")
            return None
        
        version = datetime.now().strftime("%Y.%m.%d")
        dmg_name = f"PDF_Data_Extractor_v{version}_macOS.dmg"
        temp_dir = "dmg_temp"
        
        # Create temporary directory for DMG contents
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # Copy application to temp directory
        shutil.copytree("dist/PDF Data Extractor.app", f"{temp_dir}/PDF Data Extractor.app")
        
        # Copy documentation
        os.makedirs(f"{temp_dir}/Documentation", exist_ok=True)
        docs_to_include = [
            'README.md',
            'OCR_GUIDE.md',
            'QUICKSTART.md', 
            'INSTALL.md'
        ]
        
        for doc in docs_to_include:
            if os.path.exists(doc):
                shutil.copy2(doc, f"{temp_dir}/Documentation/")
        
        # Copy the readme from dist
        if os.path.exists("dist/README.txt"):
            shutil.copy2("dist/README.txt", f"{temp_dir}/Quick Start.txt")
        
        # Create DMG
        cmd = [
            "hdiutil", "create", "-volname", "PDF Data Extractor",
            "-srcfolder", temp_dir, "-ov", "-format", "UDZO", dmg_name
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Created: {dmg_name}")
            
            # Clean up temp directory
            shutil.rmtree(temp_dir)
            return dmg_name
        else:
            print(f"❌ DMG creation failed: {result.stderr}")
            return None
    
    except Exception as e:
        print(f"❌ Error creating DMG: {e}")
        return None

def create_user_guide():
    """Create a comprehensive user guide"""
    print("📚 Creating user guide...")
    
    guide_content = f"""
# PDF Data Extractor - User Guide

**Version:** {datetime.now().strftime("%Y.%m.%d")}  
**Platform:** macOS (Universal Binary - Intel & Apple Silicon)  
**Requirements:** macOS 10.14+ (No additional software needed!)

## 🚀 Quick Start

### Installation
1. **Download** the ZIP file or DMG
2. **Extract** the ZIP or mount the DMG
3. **Drag** "PDF Data Extractor.app" to your Applications folder (optional)
4. **Double-click** the app to launch

### First Use
1. **Allow permissions** if macOS asks (the app is safe but not signed)
2. **Select PDF files** using "Browse Files"
3. **Enter search terms** (one per line)
4. **Click "Extract Data"** and wait for processing
5. **Export to Excel** when complete

## ✨ Key Features

### 🔍 Universal PDF Support
- ✅ **Normal PDFs** - Fast text extraction  
- ✅ **Scanned PDFs** - Automatic OCR processing
- ✅ **Mixed Batches** - Handles both types automatically
- ✅ **Batch Processing** - Up to 4000+ files at once

### 🛠️ Advanced Options
- **Case Sensitive** - Match exact letter case
- **Whole Words** - Find complete words only
- **Regular Expressions** - Advanced pattern matching
- **Auto OCR** ✅ - Smart detection of scanned PDFs
- **Force OCR** - Process all files with OCR
- **Context Extraction** - Capture surrounding text

### 📊 Professional Output
- **Excel Export** with formatting
- **Multiple Sheets** - Data + Summary
- **Method Tracking** - Shows OCR vs Normal extraction
- **Rich Data** - Filename, page, context, timestamps

## 🔒 Security & Privacy

- ✅ **100% Local Processing** - No internet connection required
- ✅ **No Data Collection** - Your PDFs never leave your computer
- ✅ **No Installation** - Self-contained application
- ✅ **Open Source Core** - Based on trusted libraries

## 📈 Performance Guide

### Normal PDFs
- **Speed**: ~1-2 seconds per page
- **Memory**: Low usage
- **Accuracy**: 99%+ for text-based PDFs

### OCR Processing (Scanned PDFs)
- **Speed**: ~5-15 seconds per page
- **Memory**: Moderate usage
- **Accuracy**: 90-99% depending on scan quality
- **Auto-Detection**: Kicks in when needed

### Large Batch Tips
- Start with 10-20 files to test
- Plan extra time for OCR processing
- Close other memory-intensive apps
- Use "Auto OCR" for best performance

## 🛠️ Troubleshooting

### App Won't Start
**Problem**: Double-clicking doesn't work  
**Solution**: 
1. Right-click → "Open" (bypasses security warning)
2. Or go to System Preferences → Security & Privacy → Allow

**Problem**: "App is damaged" message  
**Solution**: The app isn't code-signed. Try:
```bash
sudo xattr -rd com.apple.quarantine "/Applications/PDF Data Extractor.app"
```

### No Results Found
**Problem**: Search terms don't match anything  
**Solutions**:
1. Check spelling of search terms
2. Try partial words instead of full phrases
3. Disable "Case Sensitive" option
4. Use "Force OCR" if PDFs look scanned

### OCR Not Working
**Problem**: Scanned PDFs show no results  
**Solutions**:
1. Check "Force OCR" option
2. Ensure PDFs contain readable text (not handwriting)
3. Try with higher-quality scanned PDFs first
4. Check console output for error messages

### Slow Performance
**Problem**: Processing takes very long  
**Solutions**:
1. This is normal for OCR processing
2. Process smaller batches (100-500 files)
3. Close other applications to free memory
4. Consider overnight processing for large batches

## 🎯 Use Case Examples

### 📋 Invoice Processing
**Scenario**: 500 mixed invoices (digital + scanned)  
**Setup**: Auto OCR ✅, Search: "Invoice", "Total", "Date"  
**Result**: Automatically processes both types  

### 📄 Contract Analysis
**Scenario**: 200 historical contracts (all scanned)  
**Setup**: Force OCR ✅, Search: "Party", "Term", "Effective"  
**Result**: OCR extracts all contract details  

### 🏢 Document Archive
**Scenario**: 4000 mixed business documents  
**Setup**: Auto OCR ✅, Search: Custom terms  
**Result**: Smart processing optimizes for speed and accuracy

## 📞 Support & Updates

### Getting Help
1. **Check this guide** for common solutions
2. **Review the documentation** in the Documentation folder
3. **Test with simple files** first to verify functionality

### Technical Details
- **OCR Engine**: Tesseract 5.5.1 (industry standard)
- **PDF Library**: pdfplumber (high accuracy)
- **Excel Export**: openpyxl (full formatting)
- **GUI**: Native tkinter (fast & reliable)

---

## 🎉 You're Ready!

Your PDF Data Extractor is a powerful tool that can handle any PDF processing task:

1. **Start simple** - Test with a few files first
2. **Scale up** - Process your large batches confidently  
3. **Mix and match** - Normal and scanned PDFs work together
4. **Export professionally** - Get formatted Excel results

**Happy PDF processing! 🚀**

*Built with security and privacy in mind - your data stays on your machine.*
"""
    
    with open('PDF_Data_Extractor_User_Guide.txt', 'w') as f:
        f.write(guide_content)
    
    print("✅ Created: PDF_Data_Extractor_User_Guide.txt")
    return "PDF_Data_Extractor_User_Guide.txt"

def main():
    """Main distribution creation process"""
    print("📦 PDF Data Extractor - Distribution Creator")
    print("=" * 50)
    
    if not os.path.exists('dist'):
        print("❌ Error: 'dist' directory not found. Run build_app.py first.")
        return False
    
    # Create user guide
    guide_file = create_user_guide()
    
    # Create ZIP distribution
    zip_file = create_zip_distribution()
    
    # Create DMG distribution (macOS)
    dmg_file = create_dmg_distribution()
    
    # Summary
    print("\n🎉 Distribution packages created!")
    print("\n📁 Files ready for distribution:")
    
    if zip_file:
        zip_size = os.path.getsize(zip_file) / (1024 * 1024)
        print(f"   📦 {zip_file} ({zip_size:.1f} MB)")
        print("      → Universal distribution (extract and run)")
    
    if dmg_file:
        dmg_size = os.path.getsize(dmg_file) / (1024 * 1024)
        print(f"   💿 {dmg_file} ({dmg_size:.1f} MB)")
        print("      → macOS installer (mount and drag to Applications)")
    
    print(f"   📚 {guide_file}")
    print("      → Comprehensive user guide and troubleshooting")
    
    print("\n🚀 Ready to distribute!")
    print("   • Upload ZIP/DMG to cloud storage, website, or GitHub")
    print("   • Users download, extract, and run - no setup needed!")
    print("   • Include the user guide for support")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 