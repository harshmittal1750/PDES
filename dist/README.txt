# PDF Data Extractor - Standalone Application

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
