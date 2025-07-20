# PDF Data Extractor

A secure, local desktop application for extracting specific data from PDF files and exporting results to Excel. Perfect for processing large batches of PDFs while maintaining complete data privacy and security.

## 🔒 Security Features

- **100% Local Processing**: All operations happen on your machine - no data is sent to external servers
- **No Internet Required**: Works completely offline once installed
- **Private and Confidential**: Your PDF contents never leave your computer
- **No Data Storage**: Application doesn't store or cache your files

## ✨ Key Features

- **Batch Processing**: Handle up to 4000+ PDF files simultaneously
- **Flexible Search**: Support for exact text, whole words, case-sensitive, and regex patterns
- **Context Extraction**: Capture surrounding text around matches for better understanding
- **Excel Export**: Professional Excel output with formatting and summary sheets
- **Progress Tracking**: Real-time progress updates for large batches
- **Error Handling**: Robust error handling with detailed logging
- **User-Friendly GUI**: Intuitive interface built with modern design principles

## 📋 System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: 4GB minimum (8GB+ recommended for large batches)
- **Storage**: 100MB for installation + space for your PDF files

## 🚀 Installation

### Option 1: Quick Setup (Recommended)

1. **Clone or Download** this repository:

   ```bash
   git clone <repository-url>
   cd pdf-data-extractor
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python pdf_extractor.py
   ```

### Option 2: Virtual Environment (Best Practice)

1. **Create Virtual Environment**:

   ```bash
   python -m venv pdf_extractor_env

   # Activate (Windows)
   pdf_extractor_env\Scripts\activate

   # Activate (macOS/Linux)
   source pdf_extractor_env/bin/activate
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application**:
   ```bash
   python pdf_extractor.py
   ```

## 📖 How to Use

### Step 1: Select PDF Files

- Click **"Browse Files"** to select one or multiple PDF files
- You can select up to 4000 files at once
- Files will be listed in the selection box
- Use **"Clear"** to remove all selected files

### Step 2: Enter Search Terms

- Enter your search terms in the text box (one per line)
- Examples:
  ```
  Invoice Number
  Total Amount
  Customer Name
  Contract Date
  ```

### Step 3: Configure Search Options

- **Case Sensitive**: Match exact letter case
- **Whole Words Only**: Find complete words, not partial matches
- **Regular Expressions**: Use advanced pattern matching
- **Include Context**: Capture surrounding text (recommended)
- **Auto OCR**: Automatically use OCR for scanned/image-based PDFs ⭐ **NEW**
- **Force OCR**: Force OCR processing for all PDFs ⭐ **NEW**
- **Context chars**: Number of characters around matches (default: 100)

### Step 4: Process Files

- Click **"Extract Data"** to start processing
- Monitor progress with the progress bar
- View real-time status updates
- Processing runs in background - UI remains responsive

### Step 5: Review Results

- Results appear in the "Results" section
- Organized by file and search term
- Shows page numbers and context for each match
- Summary statistics at the bottom

### Step 6: Export to Excel

- Click **"Export to Excel"** when processing is complete
- Choose save location and filename
- Excel file includes:
  - **Main Data Sheet**: All extracted data with columns for filename, search term, page number, match text, and context
  - **Summary Sheet**: Statistics by file and search term
  - **Professional Formatting**: Headers, colors, and auto-sized columns

## 📊 Excel Output Format

### Main Data Sheet Columns:

- **filename**: Name of the PDF file
- **filepath**: Full path to the PDF file
- **search_term**: The search term that was found
- **page_number**: Page where the match was found
- **match_text**: The exact text that matched
- **context**: Surrounding text (if enabled)
- **timestamp**: When the extraction was performed

### Summary Sheet:

- Statistics by file (number of matches per file)
- Statistics by search term (how many times each term was found)

## 🎯 Use Cases

### Business Applications

- **Invoice Processing**: Extract invoice numbers, amounts, dates
- **Contract Analysis**: Find key terms, dates, parties
- **Financial Reports**: Extract figures, ratios, trends
- **Legal Documents**: Search for clauses, references, terms
- **Medical Records**: Find patient info, diagnoses, treatments

### Research Applications

- **Academic Papers**: Extract citations, data points, conclusions
- **Survey Analysis**: Find responses, patterns, statistics
- **Literature Review**: Search for keywords, themes, authors

### Personal Use

- **Document Organization**: Categorize and index documents
- **Information Retrieval**: Find specific information across multiple files
- **Archive Search**: Locate documents with specific criteria

## ⚡ Performance Tips

### For Large Batches (1000+ files):

1. **Increase RAM**: Close other applications to free memory
2. **Use SSD Storage**: Faster file access improves performance
3. **Limit Search Terms**: Fewer terms = faster processing
4. **Disable Context**: Turn off context extraction for maximum speed
5. **Process in Chunks**: Split very large batches into smaller groups

### Optimize Search Patterns:

- Use **exact text** for fastest results
- **Whole words** is faster than partial matches
- **Case sensitive** searches are slightly faster
- **Regex patterns** are slowest but most powerful

## 🛠️ Troubleshooting

### Common Issues:

**Application won't start:**

- Check Python version: `python --version` (needs 3.8+)
- Install missing dependencies: `pip install -r requirements.txt`
- Try running with: `python -m pdf_extractor`

**PDF files not processing:**

- Ensure PDFs are not password-protected
- Check file permissions (read access required)
- Verify PDFs contain extractable text (not just images)

**Out of memory errors:**

- Process fewer files at once
- Close other applications
- Increase system RAM if possible
- Use "whole words" instead of partial matches

**No matches found:**

- Check spelling of search terms
- Try case-insensitive search
- Use partial words instead of whole words
- Test with a known PDF first

**Excel export fails:**

- Ensure Excel file isn't already open
- Check write permissions to save location
- Try saving to a different folder
- Verify available disk space

## 🔧 Advanced Features

### Regular Expression Examples:

```regex
\d{4}-\d{2}-\d{2}        # Find dates (YYYY-MM-DD)
\$[\d,]+\.?\d*           # Find dollar amounts
[A-Z]{2,3}-\d{3,6}       # Find reference numbers
\b[A-Z][a-z]+\s[A-Z][a-z]+ # Find names (First Last)
```

### Batch Processing Tips:

- Process similar document types together
- Use consistent search terms across batches
- Save results with descriptive filenames
- Keep backups of original PDFs

## 📝 Technical Details

### Dependencies:

- **pdfplumber**: Advanced PDF text extraction
- **openpyxl**: Excel file creation and formatting
- **pandas**: Data manipulation and analysis
- **tkinter**: Native GUI framework (included with Python)

### Supported PDF Types:

- Text-based PDFs (most common)
- Mixed text and image PDFs
- Scanned PDFs with OCR text layers
- **Image-based/Scanned PDFs (with OCR)** ⭐ **NEW**
- Password-protected PDFs (if password provided)

### OCR Capabilities (NEW): ⭐

- **Handles Scanned PDFs**: Automatically detects and processes image-based PDFs
- **High Accuracy**: Uses Tesseract OCR engine with optimized settings
- **Smart Processing**: Tries normal text extraction first, falls back to OCR when needed
- **Manual Control**: Force OCR for all files or let the system auto-detect
- **Progress Tracking**: Real-time OCR progress updates

### Limitations:

- Very large individual PDFs (>500 pages) may be slow
- OCR processing takes longer than normal text extraction
- Heavily formatted tables might not extract perfectly
- OCR accuracy depends on scan quality and image resolution

## 🤝 Support

### Getting Help:

1. **Check this README** for common solutions
2. **Review log files** for error details
3. **Test with sample PDFs** to isolate issues
4. **Check system requirements** and dependencies

### Reporting Issues:

When reporting problems, please include:

- Operating system and version
- Python version
- Error messages (copy exact text)
- PDF file characteristics (if possible)
- Steps to reproduce the issue

## 📄 License

This software is provided as-is for personal and commercial use. No warranty is provided. Users are responsible for ensuring compliance with applicable laws and regulations when processing documents.

---

**Built for Security, Designed for Efficiency** 🔒⚡
