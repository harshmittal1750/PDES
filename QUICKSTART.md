# Quick Start Guide 🚀

Get up and running with PDF Data Extractor in 2 minutes!

## Installation & First Run

### Windows Users

1. **Double-click** `run.bat`
2. Follow any installation prompts
3. The application will start automatically

### macOS/Linux Users

1. **Double-click** `run.sh` or run in terminal:
   ```bash
   ./run.sh
   ```
2. Follow any installation prompts
3. The application will start automatically

### Manual Installation (All Platforms)

```bash
pip install -r requirements.txt
python pdf_extractor.py
```

---

## First Time Setup (30 seconds)

1. **Launch the application** using one of the methods above
2. **Test with sample files** - try with 1-2 PDF files first
3. **Enter simple search terms** like:
   - `Invoice`
   - `Total`
   - `Date`
4. **Click "Extract Data"** and wait for results
5. **Export to Excel** to see the output format

---

## Common Use Cases & Examples

### 📋 Invoice Processing

**Search Terms:**

```
Invoice Number
Invoice Date
Total Amount
Due Date
```

### 📄 Contract Analysis

**Search Terms:**

```
Contract Date
Party
Term
Effective Date
```

### 📊 Financial Reports

**Search Terms:**

```
Revenue
Profit
Loss
Quarter
Year
```

---

## Pro Tips for Best Results

✅ **Start Small**: Test with 5-10 files before processing thousands  
✅ **Use Exact Terms**: Search for exact text you see in PDFs  
✅ **Enable Context**: Keep "Include Context" checked for better results  
✅ **Case Insensitive**: Usually works better than case-sensitive  
✅ **Whole Words**: Use for cleaner results (e.g., "Total" not "total amount")

---

## Troubleshooting (30-second fixes)

**Application won't start?**

- Install Python from [python.org](https://python.org/downloads/)
- Run: `pip install -r requirements.txt`

**No results found?**

- Check spelling of search terms
- Try partial words (e.g., "Inv" instead of "Invoice Number")
- Disable "Case Sensitive" option

**Excel export fails?**

- Close Excel if it's open
- Try saving to Desktop
- Check if you have write permissions

---

## Need Help?

1. **Check the full [README.md](README.md)** for detailed instructions
2. **Test with simple PDFs first** to verify everything works
3. **Start with basic searches** before trying complex patterns

---

**Ready to extract data from 4000 PDFs? You've got this! 💪**
