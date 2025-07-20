# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Additional files to include
added_files = []

# Add tesseract binary if found
tesseract_bin = "/opt/homebrew/bin/tesseract"
if tesseract_bin and tesseract_bin != "None":
    added_files.append((tesseract_bin, 'tesseract/'))

# Add tessdata directory if found  
tessdata_dir = "/opt/homebrew/share/tessdata"
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
    hooksconfig={},
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
