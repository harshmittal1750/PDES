#!/bin/bash

# PDF Data Extractor Launcher
echo "Starting PDF Data Extractor..."

# Get the directory of this script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set TESSDATA_PREFIX for OCR
export TESSDATA_PREFIX="$DIR/tessdata/"

# Launch the application
"$DIR/PDF_Data_Extractor"
