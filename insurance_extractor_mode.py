#!/usr/bin/env python3
"""
Insurance PDF Data Extractor - Specialized Mode
Automatically extracts specific insurance policy fields from PDFs
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import pandas as pd

class InsuranceExtractor:
    """Specialized extractor for insurance policy documents"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Define the fields we're looking for
        self.insurance_fields = {
            'policy_no': 'Policy no.',
            'insured_name': 'Insured name',
            'insurer_name': 'Insurer name', 
            'engine_no': 'Engine no.',
            'chassis_no': 'Chassis no.',
            'cheque_no': 'Cheque no.',
            'cheque_date': 'Cheque date',
            'bank_name': 'Bank name',
            'net_od_premium': 'Net own damage premium amount',
            'net_liability_premium': 'Net liability premium amount',
            'total_premium': 'Total premium amount',
            'gst_amount': 'GST amount',
            'gross_premium': 'Gross premium paid',
            'car_model': 'Car model',
            'body_type': 'Body type'
        }
        
        # Create search patterns for each field
        self.search_patterns = self.create_search_patterns()
    
    def create_search_patterns(self) -> Dict[str, List[str]]:
        """Create comprehensive search patterns for insurance fields"""
        patterns = {
            'policy_no': [
                r'policy\s*no\.?\s*:?\s*([A-Z0-9\-/]+)',
                r'policy\s*number\s*:?\s*([A-Z0-9\-/]+)',
                r'certificate\s*no\.?\s*:?\s*([A-Z0-9\-/]+)',
                r'policy\s*:?\s*([A-Z0-9\-/]{6,})',
            ],
            
            'insured_name': [
                r'insured\s*name\s*:?\s*([A-Za-z\s\.]+)(?:\n|$)',
                r'name\s*of\s*insured\s*:?\s*([A-Za-z\s\.]+)(?:\n|$)',
                r'policy\s*holder\s*:?\s*([A-Za-z\s\.]+)(?:\n|$)',
                r'insured\s*:?\s*([A-Za-z\s\.]{3,})(?:\n|$)',
            ],
            
            'insurer_name': [
                r'insurer\s*name\s*:?\s*([A-Za-z\s&\.]+)(?:\n|$)',
                r'insurance\s*company\s*:?\s*([A-Za-z\s&\.]+)(?:\n|$)',
                r'company\s*:?\s*([A-Za-z\s&\.]{3,})(?:\n|$)',
            ],
            
            'engine_no': [
                r'engine\s*no\.?\s*:?\s*([A-Z0-9]+)',
                r'engine\s*number\s*:?\s*([A-Z0-9]+)',
                r'engine\s*:?\s*([A-Z0-9]{6,})',
            ],
            
            'chassis_no': [
                r'chassis\s*no\.?\s*:?\s*([A-Z0-9]+)',
                r'chassis\s*number\s*:?\s*([A-Z0-9]+)',
                r'vin\s*:?\s*([A-Z0-9]{17})',
                r'chassis\s*:?\s*([A-Z0-9]{6,})',
            ],
            
            'cheque_no': [
                r'cheque\s*no\.?\s*:?\s*([0-9]+)',
                r'check\s*no\.?\s*:?\s*([0-9]+)',
                r'cheque\s*number\s*:?\s*([0-9]+)',
                r'cheque\s*:?\s*([0-9]{6,})',
            ],
            
            'cheque_date': [
                r'cheque\s*date\s*:?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'check\s*date\s*:?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'date\s*of\s*payment\s*:?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
            ],
            
            'bank_name': [
                r'bank\s*name\s*:?\s*([A-Za-z\s&\.]+?)(?:\n|$)',
                r'drawn\s*on\s*:?\s*([A-Za-z\s&\.]+?)(?:\n|$)',
                r'bank\s*:?\s*([A-Za-z\s&\.]{3,})(?:\n|$)',
            ],
            
            'net_od_premium': [
                r'net\s*(?:own\s*damage|od)\s*premium\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'own\s*damage\s*premium\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'od\s*premium\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
            ],
            
            'net_liability_premium': [
                r'net\s*liability\s*premium\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'liability\s*premium\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'tp\s*premium\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
            ],
            
            'total_premium': [
                r'total\s*premium\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'net\s*premium\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'premium\s*amount\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
            ],
            
            'gst_amount': [
                r'gst\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'service\s*tax\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'tax\s*amount\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'igst\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
            ],
            
            'gross_premium': [
                r'gross\s*premium\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'total\s*amount\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
                r'amount\s*paid\s*:?\s*(?:rs\.?|₹)?\s*([0-9,]+\.?[0-9]*)',
            ],
            
            'car_model': [
                r'model\s*:?\s*([A-Za-z0-9\s\-]+)(?:\n|$)',
                r'vehicle\s*model\s*:?\s*([A-Za-z0-9\s\-]+)(?:\n|$)',
                r'make\s*&?\s*model\s*:?\s*([A-Za-z0-9\s\-]+)(?:\n|$)',
            ],
            
            'body_type': [
                r'body\s*type\s*:?\s*([A-Za-z\s]+)(?:\n|$)',
                r'vehicle\s*type\s*:?\s*([A-Za-z\s]+)(?:\n|$)',
                r'type\s*of\s*vehicle\s*:?\s*([A-Za-z\s]+)(?:\n|$)',
            ],
        }
        
        return patterns
    
    def extract_insurance_data(self, text: str, filename: str) -> Dict[str, str]:
        """Extract all insurance fields from the text"""
        results = {}
        text_lower = text.lower()
        
        self.logger.info(f"Extracting insurance data from {filename}")
        
        for field_key, field_name in self.insurance_fields.items():
            value = self.extract_field(text_lower, field_key)
            results[field_key] = {
                'field_name': field_name,
                'value': value if value else 'Not found',
                'found': bool(value)
            }
            
            if value:
                self.logger.info(f"Found {field_name}: {value}")
            else:
                self.logger.warning(f"Could not find {field_name} in {filename}")
        
        return results
    
    def extract_field(self, text: str, field_key: str) -> Optional[str]:
        """Extract a specific field using multiple patterns"""
        patterns = self.search_patterns.get(field_key, [])
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                value = match.group(1).strip()
                if value and len(value) > 1:  # Basic validation
                    # Clean up the value
                    value = self.clean_value(value, field_key)
                    if value:  # If still valid after cleaning
                        return value
        
        return None
    
    def clean_value(self, value: str, field_key: str) -> str:
        """Clean and validate extracted values"""
        # Remove extra whitespace
        value = re.sub(r'\s+', ' ', value.strip())
        
        # Specific cleaning for different field types
        if field_key in ['net_od_premium', 'net_liability_premium', 'total_premium', 'gst_amount', 'gross_premium']:
            # Clean monetary values
            value = re.sub(r'[^\d,\.]', '', value)  # Keep only digits, commas, and dots
            value = value.replace(',', '')  # Remove commas
            
        elif field_key in ['cheque_date']:
            # Standardize date format
            value = re.sub(r'[^\d\/\-\.]', '', value)
            
        elif field_key in ['policy_no', 'engine_no', 'chassis_no', 'cheque_no']:
            # Clean alphanumeric codes
            value = re.sub(r'[^\w\-/]', '', value)
        
        elif field_key in ['insured_name', 'insurer_name', 'bank_name', 'car_model', 'body_type']:
            # Clean names and text fields
            value = re.sub(r'[^A-Za-z0-9\s&\.\-]', '', value)
            value = value.title()  # Title case for names
        
        return value.strip() if value else ''
    
    def create_insurance_excel(self, extracted_data: List[Dict], output_path: str) -> bool:
        """Create a specialized Excel file for insurance data"""
        try:
            # Prepare data for DataFrame
            excel_data = []
            
            for file_data in extracted_data:
                filename = file_data['filename']
                extraction_method = file_data.get('extraction_method', 'Unknown')
                fields = file_data['insurance_data']
                
                row = {
                    'Filename': filename,
                    'Extraction Method': extraction_method,
                    'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Add all insurance fields
                for field_key, field_info in fields.items():
                    row[field_info['field_name']] = field_info['value']
                    row[f"{field_info['field_name']} (Found)"] = 'Yes' if field_info['found'] else 'No'
                
                excel_data.append(row)
            
            # Create DataFrame
            df = pd.DataFrame(excel_data)
            
            # Create Excel writer with multiple sheets
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Main data sheet
                df.to_excel(writer, sheet_name='Insurance Data', index=False)
                
                # Summary sheet
                summary_data = self.create_summary_stats(extracted_data)
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Format the sheets
                self.format_excel_sheets(writer, df, summary_df)
            
            self.logger.info(f"Insurance Excel file created: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating insurance Excel file: {e}")
            return False
    
    def create_summary_stats(self, extracted_data: List[Dict]) -> List[Dict]:
        """Create summary statistics for the extraction"""
        total_files = len(extracted_data)
        field_stats = {}
        
        # Initialize field statistics
        for field_key, field_name in self.insurance_fields.items():
            field_stats[field_key] = {
                'field_name': field_name,
                'found_count': 0,
                'missing_count': 0,
                'success_rate': 0
            }
        
        # Count found vs missing for each field
        for file_data in extracted_data:
            fields = file_data['insurance_data']
            for field_key, field_info in fields.items():
                if field_info['found']:
                    field_stats[field_key]['found_count'] += 1
                else:
                    field_stats[field_key]['missing_count'] += 1
        
        # Calculate success rates
        summary_rows = []
        for field_key, stats in field_stats.items():
            success_rate = (stats['found_count'] / total_files) * 100 if total_files > 0 else 0
            stats['success_rate'] = round(success_rate, 1)
            
            summary_rows.append({
                'Field Name': stats['field_name'],
                'Found in Files': stats['found_count'],
                'Missing in Files': stats['missing_count'],
                'Success Rate (%)': stats['success_rate'],
                'Total Files': total_files
            })
        
        return summary_rows
    
    def format_excel_sheets(self, writer, main_df, summary_df):
        """Format the Excel sheets for better readability"""
        try:
            from openpyxl.styles import Font, PatternFill, Alignment
            from openpyxl.utils.dataframe import dataframe_to_rows
            
            # Format main data sheet
            ws_main = writer.sheets['Insurance Data']
            
            # Header formatting
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_font = Font(color="FFFFFF", bold=True)
            
            for cell in ws_main[1]:  # First row (headers)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")
            
            # Auto-adjust column widths
            for column in ws_main.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 50)
                ws_main.column_dimensions[column_letter].width = adjusted_width
            
            # Format summary sheet
            ws_summary = writer.sheets['Summary']
            
            for cell in ws_summary[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")
            
            for column in ws_summary.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 30)
                ws_summary.column_dimensions[column_letter].width = adjusted_width
            
        except Exception as e:
            self.logger.warning(f"Could not format Excel sheets: {e}")


def main():
    """Test the insurance extractor"""
    extractor = InsuranceExtractor()
    
    # Sample insurance text for testing
    sample_text = """
    INSURANCE CERTIFICATE
    
    Policy No: ABC123/2024/001
    Insured Name: John Doe
    Insurer Name: XYZ Insurance Company Ltd
    Engine No: ENG123456
    Chassis No: CHS789012345
    
    Premium Details:
    Net OD Premium: Rs. 15,000.00
    Net Liability Premium: Rs. 2,500.00
    Total Premium: Rs. 17,500.00
    GST: Rs. 3,150.00
    Gross Premium Paid: Rs. 20,650.00
    
    Payment Details:
    Cheque No: 123456
    Cheque Date: 15/01/2024
    Bank Name: State Bank of India
    
    Vehicle Details:
    Car Model: Honda City
    Body Type: Sedan
    """
    
    results = extractor.extract_insurance_data(sample_text, "test_insurance.pdf")
    
    print("Extraction Results:")
    for field_key, field_info in results.items():
        status = "✅" if field_info['found'] else "❌"
        print(f"{status} {field_info['field_name']}: {field_info['value']}")

if __name__ == "__main__":
    main() 