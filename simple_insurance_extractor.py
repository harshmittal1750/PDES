#!/usr/bin/env python3
"""
Simple Insurance PDF Data Extractor
Focuses on extracting the 15 required insurance fields with straightforward approach
"""

import os
import sys
import pdfplumber
import pytesseract
import pandas as pd
import re
from typing import Dict, List, Optional
import logging
from datetime import datetime

class SimpleInsuranceExtractor:
    """Simple and reliable extractor for the 15 required insurance fields"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # The 15 required fields with simple patterns
        self.insurance_fields = {
            'policy_no': {
                'name': 'Policy no.',
                'patterns': [
                    r'(?:policy|certificate)\s*(?:no|number)\.?\s*:?\s*([A-Z0-9\-/]{4,})',
                    r'policy\s*:?\s*([A-Z0-9\-/]{6,})',
                ]
            },
            'insured_name': {
                'name': 'Insured name',
                'patterns': [
                    r'insured\s*(?:name)?\s*:?\s*([A-Za-z\s\.\,]{3,50})',
                    r'(?:mr|mrs|ms|dr|m/s)\.?\s+([A-Za-z\s\.\,]{3,50})',
                ]
            },
            'insurer_name': {
                'name': 'Insurer name',
                'patterns': [
                    r'(?:insurer|insurance\s*company)\s*:?\s*([A-Za-z\s&\.\,\-]{5,})',
                    r'([A-Za-z\s&\.\-]{5,})\s*insurance',
                ]
            },
            'engine_no': {
                'name': 'Engine no.',
                'patterns': [
                    r'engine\s*(?:no|number)\.?\s*:?\s*([A-Z0-9]{4,})',
                    r'engine\s*:?\s*([A-Z0-9]{6,})',
                ]
            },
            'chassis_no': {
                'name': 'Chassis no.',
                'patterns': [
                    r'chassis\s*(?:no|number)\.?\s*:?\s*([A-Z0-9]{4,})',
                    r'vin\s*:?\s*([A-Z0-9]{17})',
                ]
            },
            'cheque_no': {
                'name': 'Cheque no.',
                'patterns': [
                    r'cheque\s*(?:no|number)\.?\s*:?\s*([0-9]{4,})',
                    r'check\s*:?\s*([0-9]{6,})',
                ]
            },
            'cheque_date': {
                'name': 'Cheque date',
                'patterns': [
                    r'(?:cheque|payment)\s*date\s*:?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                    r'paid\s*on\s*:?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                ]
            },
            'bank_name': {
                'name': 'Bank name',
                'patterns': [
                    r'bank\s*(?:name)?\s*:?\s*([A-Za-z\s&\.\,\-]{3,})',
                    r'([A-Za-z\s&\.\-]{3,})\s*bank',
                ]
            },
            'net_od_premium': {
                'name': 'Net own damage premium amount',
                'patterns': [
                    r'(?:own\s*damage|od)\s*premium\s*:?\s*(?:rs\.?)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                    r'od\s*:?\s*(?:rs\.?)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                ]
            },
            'net_liability_premium': {
                'name': 'Net liability premium amount',
                'patterns': [
                    r'(?:liability|tp|third\s*party)\s*premium\s*:?\s*(?:rs\.?)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                    r'tp\s*:?\s*(?:rs\.?)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                ]
            },
            'total_premium': {
                'name': 'Total premium amount',
                'patterns': [
                    r'total\s*premium\s*:?\s*(?:rs\.?)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                    r'premium\s*total\s*:?\s*(?:rs\.?)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                ]
            },
            'gst_amount': {
                'name': 'GST amount',
                'patterns': [
                    r'gst\s*:?\s*(?:rs\.?)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                    r'tax\s*:?\s*(?:rs\.?)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                ]
            },
            'gross_premium': {
                'name': 'Gross premium paid',
                'patterns': [
                    r'gross\s*premium\s*:?\s*(?:rs\.?)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                    r'total\s*amount\s*:?\s*(?:rs\.?)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                ]
            },
            'car_model': {
                'name': 'Car model',
                'patterns': [
                    r'(?:make|model|vehicle)\s*:?\s*([A-Za-z0-9\s\-\/]{3,})',
                    r'make\s*[&\/]\s*model\s*:?\s*([A-Za-z0-9\s\-\/]{3,})',
                ]
            },
            'body_type': {
                'name': 'Body type',
                'patterns': [
                    r'body\s*type\s*:?\s*([A-Za-z\s\-]{3,})',
                    r'vehicle\s*type\s*:?\s*([A-Za-z\s\-]{3,})',
                ]
            }
        }
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, str]:
        """Extract the 15 required fields from a PDF"""
        results = {}
        
        try:
            # First try direct text extraction
            text = self.extract_text_from_pdf(pdf_path)
            
            # If text is too short, try OCR
            if len(text.strip()) < 100:
                self.logger.info(f"Text extraction yielded little content, trying OCR for {pdf_path}")
                text = self.extract_text_with_ocr(pdf_path)
            
            # Extract each field
            for field_key, field_info in self.insurance_fields.items():
                value = self.extract_field(text, field_info)
                results[field_key] = {
                    'field_name': field_info['name'],
                    'value': value if value else 'Not found',
                    'found': bool(value)
                }
                
                status = "✅" if value else "❌"
                self.logger.info(f"{status} {field_info['name']}: {value if value else 'Not found'}")
        
        except Exception as e:
            self.logger.error(f"Error processing {pdf_path}: {e}")
            # Initialize empty results
            for field_key, field_info in self.insurance_fields.items():
                results[field_key] = {
                    'field_name': field_info['name'],
                    'value': 'Error',
                    'found': False
                }
        
        return results
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text directly from PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            self.logger.error(f"Error extracting text from {pdf_path}: {e}")
        
        return text
    
    def extract_text_with_ocr(self, pdf_path: str) -> str:
        """Extract text using OCR"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    # Convert page to image and OCR
                    img = page.to_image(resolution=300)
                    page_text = pytesseract.image_to_string(img.original)
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            self.logger.error(f"Error with OCR for {pdf_path}: {e}")
        
        return text
    
    def extract_field(self, text: str, field_info: Dict) -> Optional[str]:
        """Extract a single field using its patterns"""
        text_lower = text.lower()
        
        for pattern in field_info['patterns']:
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.MULTILINE)
            if matches:
                # Return the first match, cleaned
                value = matches[0].strip()
                return self.clean_value(value)
        
        return None
    
    def clean_value(self, value: str) -> str:
        """Clean and format extracted values"""
        if not value:
            return ''
        
        # Remove extra whitespace
        value = ' '.join(value.split())
        
        # Basic cleaning
        value = value.replace('\n', ' ').replace('\r', ' ')
        
        return value.strip()
    
    def create_excel(self, results_list: List[Dict], output_path: str) -> bool:
        """Create Excel file with results"""
        try:
            excel_data = []
            
            for file_result in results_list:
                filename = file_result['filename']
                data = file_result['data']
                
                row = {'Filename': filename}
                
                for field_key, field_info in data.items():
                    row[field_info['field_name']] = field_info['value']
                    row[f"{field_info['field_name']} (Found)"] = 'Yes' if field_info['found'] else 'No'
                
                excel_data.append(row)
            
            df = pd.DataFrame(excel_data)
            df.to_excel(output_path, index=False)
            
            self.logger.info(f"Excel file created: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating Excel file: {e}")
            return False


def main():
    """Simple command line interface"""
    import tkinter as tk
    from tkinter import filedialog, messagebox
    
    # Simple GUI for file selection
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    print("🏢 Simple Insurance PDF Data Extractor")
    print("Select PDF files to process...")
    
    # Select PDF files
    file_paths = filedialog.askopenfilenames(
        title="Select Insurance PDF Files",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    
    if not file_paths:
        print("No files selected. Exiting.")
        return
    
    # Initialize extractor
    extractor = SimpleInsuranceExtractor()
    
    # Process files
    results = []
    print(f"\nProcessing {len(file_paths)} files...")
    
    for i, pdf_path in enumerate(file_paths, 1):
        filename = os.path.basename(pdf_path)
        print(f"\n[{i}/{len(file_paths)}] Processing: {filename}")
        
        data = extractor.extract_from_pdf(pdf_path)
        results.append({
            'filename': filename,
            'data': data
        })
    
    # Ask for output location
    output_path = filedialog.asksaveasfilename(
        title="Save Excel Results",
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")]
    )
    
    if output_path:
        success = extractor.create_excel(results, output_path)
        if success:
            print(f"\n✅ Results saved to: {output_path}")
            messagebox.showinfo("Success", f"Results saved to:\n{output_path}")
        else:
            print("❌ Error saving results")
            messagebox.showerror("Error", "Failed to save results")
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main() 