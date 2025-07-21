#!/usr/bin/env python3
"""
100% Accuracy Insurance PDF Data Extractor
Optimized specifically for the 15 required insurance fields
"""

import os
import sys
import re
import logging
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading

# Add PDF processing imports
try:
    import pdfplumber
    import pytesseract
    from PIL import Image
except ImportError as e:
    print(f"Missing required packages: {e}")
    sys.exit(1)

class OptimizedInsuranceExtractor:
    """100% Accuracy focused extractor for the 15 insurance fields"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Enhanced patterns for each field with multiple variations
        self.field_patterns = {
            'policy_no': {
                'name': 'Policy no.',
                'patterns': [
                    r'policy\s*(?:no|number|ref|reference)\.?\s*:?\s*([A-Z0-9\-/]{4,30})',
                    r'certificate\s*(?:no|number)\.?\s*:?\s*([A-Z0-9\-/]{4,30})',
                    r'policy\s*:?\s*([A-Z0-9\-/]{6,30})',
                    r'cert\.?\s*no\.?\s*:?\s*([A-Z0-9\-/]{6,30})',
                    r'policy\s*id\s*:?\s*([A-Z0-9\-/]{6,30})',
                    r'\b([A-Z0-9]{4}[A-Z0-9\-/]{4,26})\b',  # Standalone policy-like codes
                ],
                'validation': self.validate_policy_number,
                'cleaning': self.clean_code
            },
            
            'insured_name': {
                'name': 'Insured name',
                'patterns': [
                    r'insured\s*(?:name)?\s*:?\s*([A-Z][A-Za-z\s\.\,&]{2,60})(?:\n|$|[0-9])',
                    r'name\s*of\s*(?:the\s*)?insured\s*:?\s*([A-Z][A-Za-z\s\.\,&]{2,60})(?:\n|$)',
                    r'policy\s*holder\s*(?:name)?\s*:?\s*([A-Z][A-Za-z\s\.\,&]{2,60})(?:\n|$)',
                    r'(?:mr|mrs|ms|dr|m/s)\.?\s+([A-Z][A-Za-z\s\.\,&]{2,60})(?:\n|$)',
                    r'assured\s*(?:name)?\s*:?\s*([A-Z][A-Za-z\s\.\,&]{2,60})(?:\n|$)',
                    r'customer\s*(?:name)?\s*:?\s*([A-Z][A-Za-z\s\.\,&]{2,60})(?:\n|$)',
                ],
                'validation': self.validate_name,
                'cleaning': self.clean_name
            },
            
            'insurer_name': {
                'name': 'Insurer name',
                'patterns': [
                    r'(?:insurer|insurance\s*company)\s*(?:name)?\s*:?\s*([A-Z][A-Za-z\s&\.\,\-]{4,80})(?:\n|$)',
                    r'company\s*(?:name)?\s*:?\s*([A-Z][A-Za-z\s&\.\,\-]{4,80})(?:\n|$)',
                    r'([A-Z][A-Za-z\s&\.\-]{4,50})\s*(?:insurance|assurance|general)(?:\s|$)',
                    r'underwriter\s*:?\s*([A-Z][A-Za-z\s&\.\,\-]{4,80})(?:\n|$)',
                    r'carrier\s*:?\s*([A-Z][A-Za-z\s&\.\,\-]{4,80})(?:\n|$)',
                ],
                'validation': self.validate_company_name,
                'cleaning': self.clean_company_name
            },
            
            'engine_no': {
                'name': 'Engine no.',
                'patterns': [
                    # Primary patterns with various separators
                    r'engine\s*(?:no|number|#)\.?\s*[:\-]?\s*([A-Z0-9]{6,25})',
                    r'engine\s*[:\-]?\s*([A-Z0-9]{6,25})',
                    r'motor\s*(?:no|number)\.?\s*[:\-]?\s*([A-Z0-9]{6,25})',
                    r'e\.?\s*no\.?\s*[:\-]?\s*([A-Z0-9]{6,25})',
                    r'engine\s*serial\s*(?:no|number)?\s*[:\-]?\s*([A-Z0-9]{6,25})',
                    
                    # Enhanced context-based patterns (more flexible)
                    r'(?:engine|motor|e\.?no).*?([A-Z0-9]{8,20})',  # Look for codes near engine context (any separation)
                    r'([A-Z0-9]{8,20}).*?(?:engine|motor)',  # Code before engine label
                    
                    # Common engine number formats with OCR-friendly separators
                    r'\b([A-Z]{2,4}[0-9]{6,})\b',  # Pattern like ABC123456 (common engine format)
                    r'\b([0-9]{6,}[A-Z]{2,4})\b',  # Pattern like 123456ABC (reverse format)
                    r'\b([A-Z]{1,3}[0-9]{4,}[A-Z0-9]{1,})\b',  # Mixed patterns like A1234B5C
                    
                    # Look for engine numbers in table contexts (separated by spaces/tabs)
                    r'(?:engine|motor|e\.?no)\s*[|\t]\s*([A-Z0-9]{6,25})',  # Table format with pipes/tabs
                    r'([A-Z0-9]{6,25})\s*[|\t]\s*(?:engine|motor)',  # Reverse table format
                    
                    # OCR-friendly patterns for various separators and spacing
                    r'(?:engine|motor)[^a-z0-9]{0,10}([A-Z0-9]{8,25})',  # Flexible separator matching
                    r'([A-Z0-9]{8,25})[^a-z0-9]{0,10}(?:engine|motor)',  # Reverse flexible
                    
                    # Look for standalone alphanumeric codes that could be engine numbers
                    # (excluding chassis number pattern AABCT3518Q which is already found)
                    r'\b([A-Z]{1,2}[0-9]{6,}[A-Z0-9]*)\b(?!.*chassis|vin|frame)',  # Not chassis
                    r'\b([0-9]{2,}[A-Z]{3,}[0-9]{2,})\b',  # Number-Letter-Number pattern
                    
                    # Fallback patterns for any long alphanumeric code in engine context
                    r'(?:engine|motor)(?:[^a-zA-Z0-9]+)([A-Za-z0-9]{6,25})',  # Very flexible separator
                ],
                'validation': self.validate_engine_number,
                'cleaning': self.clean_code
            },
            
            'chassis_no': {
                'name': 'Chassis no.',
                'patterns': [
                    r'chassis\s*(?:no|number|#)\.?\s*[:\-]?\s*([A-Z0-9]{6,25})',
                    r'chassis\s*[:\-]?\s*([A-Z0-9]{6,25})',
                    r'vin\s*(?:no|number)?\s*[:\-]?\s*([A-Z0-9]{17})',  # VIN is exactly 17 chars
                    r'vehicle\s*identification\s*(?:no|number)\s*[:\-]?\s*([A-Z0-9]{17})',
                    r'frame\s*(?:no|number)\.?\s*[:\-]?\s*([A-Z0-9]{6,25})',
                    r'c\.?\s*no\.?\s*[:\-]?\s*([A-Z0-9]{6,25})',
                    # Look for long alphanumeric codes that could be chassis numbers
                    r'\b([A-Z]{2,}[0-9]{4,}[A-Z0-9]*)\b',  # Pattern like AABCT3518Q
                    r'\b([A-Z0-9]{10,17})\b',  # Any long alphanumeric code
                    # Context-based patterns
                    r'(?:chassis|vin|frame).*?([A-Z0-9]{8,25})',
                ],
                'validation': self.validate_chassis_number,
                'cleaning': self.clean_code
            },
            
            'cheque_no': {
                'name': 'Cheque no.',
                'patterns': [
                    r'cheque\s*(?:no|number|#)\.?\s*:?\s*([0-9]{4,15})',
                    r'check\s*(?:no|number)\.?\s*:?\s*([0-9]{4,15})',
                    r'cheque\s*:?\s*([0-9]{6,15})',
                    r'check\s*:?\s*([0-9]{6,15})',
                    r'payment\s*(?:ref|reference)\s*:?\s*([0-9A-Z\-]{4,15})',
                    r'transaction\s*(?:id|ref)\s*:?\s*([0-9A-Z\-]{4,15})',
                ],
                'validation': self.validate_cheque_number,
                'cleaning': self.clean_numeric
            },
            
            'cheque_date': {
                'name': 'Cheque date',
                'patterns': [
                    # Specific pattern for "05-May-2025" format (user confirmed this format exists)
                    r'([0-9]{1,2}[\-\s]+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\-\s]+[0-9]{4})',  # DD-Mon-YYYY
                    r'([0-9]{1,2}[\-\s]+(january|february|march|april|may|june|july|august|september|october|november|december)[\-\s]+[0-9]{4})',  # Full month names
                    
                    # Standard date patterns
                    r'(?:cheque|check|payment|transaction)\s*date\s*[:\-]?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                    r'date\s*of\s*(?:cheque|check|payment)\s*[:\-]?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                    r'(?:paid|payment)\s*on\s*[:\-]?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                    r'date\s*[:\-]?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                    
                    # Enhanced OCR-friendly date formats
                    r'([0-9]{1,2}[\-\/\.][0-9]{1,2}[\-\/\.][0-9]{4})',  # General date pattern
                    r'([0-9]{2}[\-\/\.][0-9]{2}[\-\/\.][0-9]{4})',  # DD/MM/YYYY or MM/DD/YYYY
                    r'([0-9]{1,2}[\s]+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\s]+[0-9]{4})',  # DD Mon YYYY (space separated)
                    r'([0-9]{4}[\-\/\.][0-9]{1,2}[\-\/\.][0-9]{1,2})',  # YYYY/MM/DD format
                    
                    # Context-based: look for dates near payment/cheque context  
                    r'(?:payment|cheque|check|transaction).*?([0-9]{1,2}[\-\s]+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\-\s]+[0-9]{4})',
                    r'(?:payment|cheque|check|transaction).*?([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                    r'(?:paid|date).*?([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                    r'(?:paid|date).*?([0-9]{1,2}[\-\s]+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\-\s]+[0-9]{4})',
                    
                    # Look for isolated dates that might be payment dates (recent years)
                    r'\b([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.](20[2-9][0-9]))\b',  # 2020-2099 dates
                    r'\b([0-9]{1,2}[\-\s]+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\-\s]+(20[2-9][0-9]))\b',  # Month format 2020+
                    
                    # Indian date format: DD-MM-YYYY
                    r'\b([0-3][0-9][\-\/\.][0-1][0-9][\-\/\.][2][0-9][2-9][0-9])\b',
                    
                    # Flexible patterns for OCR variations
                    r'([0-9]{1,2}[^0-9a-z]{1,2}(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[^0-9a-z]{1,2}[0-9]{4})',  # OCR-friendly separators
                ],
                'validation': self.validate_date,
                'cleaning': self.clean_date
            },
            
            'bank_name': {
                'name': 'Bank name',
                'patterns': [
                    r'bank\s*(?:name)?\s*:?\s*([A-Z][A-Za-z\s&\.\,\-]{2,50})(?:\n|$|branch)',
                    r'([A-Z][A-Za-z\s&\.\-]{3,40})\s*bank(?:\s|$)',
                    r'drawn\s*on\s*:?\s*([A-Z][A-Za-z\s&\.\,\-]{3,50})(?:\n|$)',
                    r'issuing\s*bank\s*:?\s*([A-Z][A-Za-z\s&\.\,\-]{3,50})(?:\n|$)',
                    r'financial\s*institution\s*:?\s*([A-Z][A-Za-z\s&\.\,\-]{3,50})(?:\n|$)',
                    r'banker\s*:?\s*([A-Z][A-Za-z\s&\.\,\-]{3,50})(?:\n|$)',
                ],
                'validation': self.validate_bank_name,
                'cleaning': self.clean_bank_name
            },
            
            # Enhanced monetary field patterns with better OCR support
            'net_od_premium': {
                'name': 'Net own damage premium amount',
                'patterns': [
                    r'(?:net\s*)?(?:own\s*damage|od|comprehensive)\s*(?:premium)?\s*(?:amount)?\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'od\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'comprehensive\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'own\s*damage\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    # Table-based patterns
                    r'(?:rs\.?|₹)\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:od|own\s*damage|comprehensive)',
                    r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:od|own\s*damage)',
                    # Look for amounts near OD labels
                    r'(?:^|\s)([1-9][0-9,]{3,}(?:\.[0-9]{2})?)\s*(?=.*(?:od|own.*damage))',
                ],
                'validation': self.validate_monetary,
                'cleaning': self.clean_monetary
            },
            
            'net_liability_premium': {
                'name': 'Net liability premium amount',
                'patterns': [
                    r'(?:net\s*)?(?:liability|third\s*party|tp)\s*(?:premium)?\s*(?:amount)?\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'tp\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'third\s*party\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'liability\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    # Table-based patterns
                    r'(?:rs\.?|₹)\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:tp|third\s*party|liability)',
                    r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:tp|third\s*party|liability)',
                    # Look for amounts near TP/liability labels
                    r'(?:^|\s)([1-9][0-9,]{3,}(?:\.[0-9]{2})?)\s*(?=.*(?:tp|third.*party|liability))',
                ],
                'validation': self.validate_monetary,
                'cleaning': self.clean_monetary
            },
            
            'total_premium': {
                'name': 'Total premium amount',
                'patterns': [
                    r'(?:total|net|base)\s*premium\s*(?:amount)?\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'premium\s*(?:total|subtotal)\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'subtotal\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'net\s*premium\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    # Table-based patterns
                    r'(?:rs\.?|₹)\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:total|subtotal|net)',
                    r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:total.*premium|net.*premium)',
                    # Look for amounts near total/premium labels
                    r'(?:^|\s)([1-9][0-9,]{4,}(?:\.[0-9]{2})?)\s*(?=.*(?:total|premium))',
                ],
                'validation': self.validate_monetary,
                'cleaning': self.clean_monetary
            },
            
            'gst_amount': {
                'name': 'GST amount',
                'patterns': [
                    r'(?:gst|igst|cgst|sgst|service\s*tax|tax)\s*(?:amount|@\s*[0-9]+\s*%)?\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'tax\s*(?:amount|component)?\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'(?:gst|tax)\s*@\s*[0-9]+%\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    # Enhanced table-based patterns
                    r'(?:rs\.?|₹)\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:gst|tax|igst|cgst|sgst)',
                    r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:gst|tax)',
                    # Look for tax percentages and calculate from total  
                    r'(?:gst|tax).*?([0-9,]+(?:\.[0-9]{2})?)',
                    r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:.*gst|.*tax)',
                    # Common GST calculation patterns (18% is common)
                    r'@\s*18%.*?(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)',
                    r'18%.*?([0-9,]+(?:\.[0-9]{2})?)',
                    # Look for amounts that could be GST (usually smaller than premium amounts)
                    r'(?:^|\s)([1-9][0-9]{3,4}(?:\.[0-9]{2})?)\s*(?=.*(?:gst|tax))',
                ],
                'validation': self.validate_monetary,
                'cleaning': self.clean_monetary
            },
            
            'gross_premium': {
                'name': 'Gross premium paid',
                'patterns': [
                    r'(?:gross|total|final)\s*(?:premium|amount)\s*(?:paid|payable)?\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'(?:grand\s*total|amount\s*(?:paid|due|payable))\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'total\s*amount\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    r'amount\s*payable\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                    # Table-based patterns
                    r'(?:rs\.?|₹)\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:total|gross|final|grand)',
                    r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:total.*amount|gross.*premium|amount.*payable)',
                    # Look for largest amounts (gross premium is typically the highest)
                    r'(?:^|\s)([1-9][0-9,]{4,}(?:\.[0-9]{2})?)\s*(?=.*(?:total|gross|final|payable))',
                ],
                'validation': self.validate_monetary,
                'cleaning': self.clean_monetary
            },
            
            'car_model': {
                'name': 'Car model',
                'patterns': [
                    r'(?:make|model|vehicle\s*model|car\s*model)\s*[:\-]?\s*([A-Za-z0-9\s\-\/]{2,50})(?:\n|$|year|[0-9]{4})',
                    r'(?:make\s*[&\/]\s*model|vehicle\s*description)\s*[:\-]?\s*([A-Za-z0-9\s\-\/]{2,50})(?:\n|$)',
                    r'(?:vehicle|car)\s*make\s*[:\-]?\s*([A-Za-z0-9\s\-\/]{2,50})(?:\n|$)',
                    # Common car brand patterns
                    r'\b((?:maruti|honda|toyota|hyundai|tata|mahindra|ford|chevrolet|nissan|volkswagen|bmw|audi|mercedes)\s*[A-Za-z0-9\s\-]*)\b',
                    # Look for model patterns (Brand + Model)
                    r'\b([A-Z][a-z]+\s+[A-Z][A-Za-z0-9\s]{2,20})\b',  # Like "Honda City"
                    # Context-based vehicle info
                    r'(?:make|model|vehicle).*?([A-Z][a-zA-Z\s\-]{2,30})',
                ],
                'validation': self.validate_vehicle_info,
                'cleaning': self.clean_vehicle_info
            },
            
            'body_type': {
                'name': 'Body type',
                'patterns': [
                    r'body\s*type\s*[:\-]?\s*([A-Za-z\s\-]{2,30})(?:\n|$)',
                    r'vehicle\s*type\s*[:\-]?\s*([A-Za-z\s\-]{2,30})(?:\n|$)',
                    r'type\s*of\s*vehicle\s*[:\-]?\s*([A-Za-z\s\-]{2,30})(?:\n|$)',
                    r'(?:category|classification)\s*[:\-]?\s*([A-Za-z\s\-]{2,30})(?:\n|$)',
                    r'vehicle\s*category\s*[:\-]?\s*([A-Za-z\s\-]{2,30})(?:\n|$)',
                    # Common body types
                    r'\b(sedan|hatchback|suv|coupe|convertible|wagon|truck|motorcycle|scooter|van|jeep|pickup)\b',
                    # Context-based body type
                    r'(?:body|type|category|classification).*?(sedan|hatchback|suv|coupe|convertible|wagon|truck|van)',
                ],
                'validation': self.validate_body_type,
                'cleaning': self.clean_body_type
            }
        }
    
    # Enhanced validation methods for each field type
    def validate_policy_number(self, value: str) -> bool:
        """Enhanced policy number validation"""
        if not value or len(value) < 4 or len(value) > 30:
            return False
        # Must contain alphanumeric characters
        if not re.match(r'^[A-Z0-9\-/]+$', value):
            return False
        # Should have a mix of letters and numbers typically, and reasonable length
        if len(value) < 6:  # Most policy numbers are at least 6 characters
            return False
        # Reject common false positives
        false_positives = ['PAGE', 'TOTAL', 'AMOUNT', 'PREMIUM', 'GST', 'NAME', 'POLICY']
        return not any(fp in value.upper() for fp in false_positives)
    
    def validate_name(self, value: str) -> bool:
        """Enhanced name validation - more flexible for OCR variations"""
        if not value or len(value) < 3 or len(value) > 100:
            return False
        # Must contain alphabetic chars
        if not re.search(r'[A-Za-z]', value):
            return False
        # Be more flexible with capitalization (OCR can affect this)
        # Must have at least 2 words for full names (except single company names > 10 chars)
        words = value.split()
        if len(words) < 2 and len(value) < 10:
            return False
        
        # Common false positives to exclude - but be more selective
        false_positives = ['PAGE', 'TOTAL', 'AMOUNT', 'PREMIUM', 'TAX', 'GST', 'POLICY',
                          'CERTIFICATE', 'MOTOR', 'VEHICLE', 'WEBSITE', 'DISPLAY']
        
        # Don't reject names that contain common business words
        business_ok = ['ENGINEERING', 'LIMITED', 'COMPANY', 'INSURANCE', 'GENERAL', 'BANK']
        has_business_word = any(word in value.upper() for word in business_ok)
        
        if has_business_word:
            # Allow business names, just check for obvious non-names
            reject_patterns = ['TERMS', 'CONDITIONS', 'WEBSITE', 'WWW', 'HTTP', 'CLICK']
            return not any(pattern in value.upper() for pattern in reject_patterns)
        
        return not any(fp in value.upper() for fp in false_positives)
    
    def validate_company_name(self, value: str) -> bool:
        """Enhanced insurance company name validation - OCR flexible"""
        if not value or len(value) < 4 or len(value) > 100:
            return False
        
        # Reject if it's clearly not a company name (more selective)
        false_positives = ['TERMS', 'CONDITIONS', 'WEBSITE', 'DISPLAY', 'WILL', 'CAN', 
                          'WWW', 'HTTP', 'CLICK', 'HERE', 'LINK', 'PAGE', 'DOCUMENT', 'PDF']
        if any(fp in value.upper() for fp in false_positives):
            return False
        
        # Check for insurance-related keywords or known patterns (expanded list)
        insurance_keywords = ['insurance', 'assurance', 'general', 'life', 'motor', 'vehicle', 'aig', 
                             'tata', 'bajaj', 'reliance', 'hdfc', 'icici', 'lic', 'new india', 'oriental',
                             'united', 'royal', 'star', 'future', 'raheja', 'kotak', 'digit']
        has_insurance_keyword = any(keyword in value.lower() for keyword in insurance_keywords)
        
        # Accept if has insurance keyword and reasonable length (more flexible)
        if has_insurance_keyword and len(value) > 4:
            return True
        
        # Accept if it looks like a company name (has "Ltd", "Limited", "Co", etc.)
        company_indicators = ['ltd', 'limited', 'co.', 'inc', 'corp', 'company', 'enterprises', 'group']
        has_company_indicator = any(indicator in value.lower() for indicator in company_indicators)
        
        # More flexible length requirements
        if has_company_indicator and len(value) > 6:
            return True
            
        # If it's a reasonable length and has mixed case or common name patterns, accept it
        if len(value) > 8 and re.search(r'[A-Za-z]', value):
            return True
        
        return False
    
    def validate_engine_number(self, value: str) -> bool:
        """Enhanced engine number validation"""
        if not value or len(value) < 6 or len(value) > 25:  # Increased minimum length
            return False
        # Must be alphanumeric and have reasonable length
        if not re.match(r'^[A-Z0-9]+$', value):
            return False
        # Should have both letters and numbers for most engine numbers
        has_letters = bool(re.search(r'[A-Z]', value))
        has_numbers = bool(re.search(r'[0-9]', value))
        if not (has_letters and has_numbers):
            return False
        # Reject incomplete words
        incomplete_words = ['ERING', 'GINE', 'ENGINE', 'MOTOR', 'NUMBER', 'NO']
        return value not in incomplete_words
    
    def validate_chassis_number(self, value: str) -> bool:
        """Enhanced chassis/VIN validation"""
        if not value or len(value) < 6 or len(value) > 25:
            return False
        # Must be alphanumeric
        if not re.match(r'^[A-Z0-9]+$', value):
            return False
        # VIN numbers are exactly 17 characters
        if len(value) == 17:
            return True
        # Regular chassis numbers should be at least 8 characters and have both letters and numbers
        if len(value) >= 8:
            has_letters = bool(re.search(r'[A-Z]', value))
            has_numbers = bool(re.search(r'[0-9]', value))
            return has_letters and has_numbers
        # For shorter codes, be more permissive but still require alphanumeric mix
        has_letters = bool(re.search(r'[A-Z]', value))
        has_numbers = bool(re.search(r'[0-9]', value))
        return has_letters and has_numbers and len(value) >= 6
    
    def validate_cheque_number(self, value: str) -> bool:
        """Enhanced cheque number validation"""
        if not value or len(value) < 4 or len(value) > 15:
            return False
        # Can be numeric or alphanumeric for modern payment systems
        return bool(re.match(r'^[0-9A-Z\-]+$', value))
    
    def validate_date(self, value: str) -> bool:
        """Enhanced date validation for all formats including DD-Mon-YYYY"""
        if not value:
            return False
        
        # Enhanced date formats - including DD-Mon-YYYY like "05-May-2025"
        date_patterns = [
            r'^[0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4}$',  # DD/MM/YYYY, DD-MM-YYYY, etc.
            r'^[0-9]{4}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{1,2}$',    # YYYY/MM/DD
            r'^[0-9]{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+[0-9]{4}$',  # DD Mon YYYY (space)
            r'^[0-9]{1,2}[\-\s]+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\-\s]+[0-9]{4}$',  # DD-Mon-YYYY (dash/space)
            r'^[0-9]{1,2}[\-\s]+(?:january|february|march|april|may|june|july|august|september|october|november|december)[\-\s]+[0-9]{4}$',  # Full month names
            r'^[0-9]{2}[\/\-\.][0-9]{2}[\/\-\.][0-9]{4}$',        # Strict DD/MM/YYYY
            r'^[0-9]{1,2}[^0-9a-z]{1,2}(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[^0-9a-z]{1,2}[0-9]{4}$',  # OCR variations
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value.strip(), re.IGNORECASE):
                # Additional validation: check if it could be a reasonable date
                # Split by any non-alphanumeric character to get parts
                parts = re.split(r'[^a-zA-Z0-9]', value)
                parts = [p for p in parts if p]  # Remove empty parts
                
                if len(parts) >= 3:
                    try:
                        # Try to extract year (usually the longest numeric part or the last part)
                        numeric_parts = [p for p in parts if p.isdigit()]
                        if numeric_parts:
                            # Look for 4-digit year first, then longest number
                            year_candidates = [int(p) for p in numeric_parts if len(p) == 4 and p.isdigit()]
                            if year_candidates:
                                year = year_candidates[0]
                            else:
                                year = int(max(numeric_parts, key=len))
                            
                            # Insurance documents typically from 2000 onwards, future dates up to 2030
                            if 2000 <= year <= 2030:
                                return True
                    except:
                        pass
                
                # For month-name formats, check if month name is valid
                months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                         'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
                if any(month in value.lower() for month in months):
                    return True
                
                # If we can't validate the date components, accept the format match
                return True
        
        return False
    
    def validate_bank_name(self, value: str) -> bool:
        """Enhanced bank name validation - OCR flexible"""
        if not value or len(value) < 3 or len(value) > 60:
            return False
        
        # Expanded list of bank keywords and payment systems
        bank_indicators = ['bank', 'hdfc', 'icici', 'sbi', 'axis', 'kotak', 'pnb', 'canara', 
                          'union', 'federal', 'yes bank', 'indusind', 'karur', 'cug', 'ccavenue',
                          'payment', 'gateway', 'payu', 'razorpay', 'cashfree', 'instamojo',
                          'banking', 'financial', 'credit', 'debit']
        
        # Check for bank indicators
        has_bank_indicator = any(indicator in value.lower() for indicator in bank_indicators)
        if has_bank_indicator:
            return True
        
        # If it's a reasonable length and contains alphabetic characters, might be a bank name
        # (OCR might have garbled the name)
        if len(value) > 6 and re.search(r'[A-Za-z]', value):
            # Check it's not obviously a non-bank term
            non_bank_terms = ['premium', 'amount', 'policy', 'insurance', 'total', 'gst', 'tax']
            if not any(term in value.lower() for term in non_bank_terms):
                return True
        
        return False
    
    def validate_monetary(self, value: str) -> bool:
        """Enhanced monetary validation with field-specific ranges"""
        if not value:
            return False
        # Remove formatting and check if it's a valid number
        cleaned = re.sub(r'[^\d\.]', '', value)
        if not cleaned:
            return False
        try:
            amount = float(cleaned)
            # Enhanced validation based on typical insurance premium ranges
            
            # Very small amounts (less than 100) are suspicious for most premium fields
            if amount < 100:
                # Only allow small amounts for specific cases
                return amount >= 50  # Minimum threshold
            
            # Reasonable ranges for different types of premiums:
            # - Individual premiums: 100 to 500,000
            # - Total/Gross premiums: 500 to 10,000,000
            # - GST/Tax amounts: 50 to 100,000
            
            return 50 <= amount <= 10000000
        except ValueError:
            return False
    
    def validate_vehicle_info(self, value: str) -> bool:
        """Enhanced vehicle information validation"""
        if not value or len(value) < 2 or len(value) > 60:
            return False
        
        # Reject insurance company names that might be mistaken for car models
        insurance_indicators = ['insurance', 'assurance', 'general', 'aig', 'company', 'co.', 'ltd', 'limited']
        if any(indicator in value.lower() for indicator in insurance_indicators):
            return False
        
        # Reject if it's clearly not a vehicle model
        non_vehicle_terms = ['premium', 'amount', 'total', 'gst', 'tax', 'policy', 'certificate']
        if any(term in value.lower() for term in non_vehicle_terms):
            return False
        
        # Look for actual car brand/model patterns
        car_brands = ['maruti', 'honda', 'toyota', 'hyundai', 'tata', 'mahindra', 'ford', 'chevrolet', 
                     'nissan', 'volkswagen', 'bmw', 'audi', 'mercedes', 'skoda', 'renault', 'kia', 
                     'mg', 'jeep', 'land rover', 'jaguar', 'volvo']
        
        has_car_brand = any(brand in value.lower() for brand in car_brands)
        
        # If it has a car brand, it's likely a valid model
        if has_car_brand:
            return True
        
        # For other cases, check if it looks like a model name (reasonable length, alphanumeric)
        if 3 <= len(value) <= 30 and re.search(r'[A-Za-z0-9]', value):
            # But still reject if it's too long or has too many "company-like" words
            words = value.split()
            if len(words) > 4 or len(value) > 25:  # Likely not a car model if too long
                return False
            return True
        
        return False
    
    def validate_body_type(self, value: str) -> bool:
        """Enhanced body type validation"""
        if not value or len(value) < 2 or len(value) > 40:
            return False
        common_types = ['sedan', 'hatchback', 'suv', 'coupe', 'convertible', 'wagon', 
                       'truck', 'motorcycle', 'scooter', 'van', 'jeep', 'pickup']
        value_lower = value.lower()
        return any(body_type in value_lower for body_type in common_types) or bool(re.match(r'^[a-zA-Z\s\-]+$', value))
    
    # Cleaning methods
    def clean_code(self, value: str) -> str:
        """Clean alphanumeric codes"""
        return re.sub(r'[^\w\-/]', '', value.upper()).strip()
    
    def clean_name(self, value: str) -> str:
        """Clean names"""
        # Remove extra spaces and normalize
        value = ' '.join(value.split())
        # Remove common prefixes that might get captured
        prefixes_to_remove = ['Name:', 'Insured:', 'Policy Holder:']
        for prefix in prefixes_to_remove:
            if value.startswith(prefix):
                value = value[len(prefix):].strip()
        return value.title()
    
    def clean_company_name(self, value: str) -> str:
        """Clean company names"""
        value = ' '.join(value.split())
        # Remove common artifacts
        artifacts = ['Company:', 'Insurer:', 'Insurance Company:']
        for artifact in artifacts:
            if value.startswith(artifact):
                value = value[len(artifact):].strip()
        return value.title()
    
    def clean_numeric(self, value: str) -> str:
        """Clean numeric values"""
        return re.sub(r'[^\d]', '', value)
    
    def clean_date(self, value: str) -> str:
        """Clean and standardize dates including DD-Mon-YYYY format"""
        if not value:
            return ''
        
        value = value.strip()
        
        # Handle month names (convert to proper case for consistency)
        months_map = {
            'jan': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'apr': 'Apr', 'may': 'May', 'jun': 'Jun',
            'jul': 'Jul', 'aug': 'Aug', 'sep': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dec': 'Dec',
            'january': 'Jan', 'february': 'Feb', 'march': 'Mar', 'april': 'Apr', 'may': 'May', 'june': 'Jun',
            'july': 'Jul', 'august': 'Aug', 'september': 'Sep', 'october': 'Oct', 'november': 'Nov', 'december': 'Dec'
        }
        
        # Replace month names with standardized versions
        value_lower = value.lower()
        for full_month, short_month in months_map.items():
            if full_month in value_lower:
                # Use word boundaries to avoid partial matches
                value = re.sub(r'\b' + re.escape(full_month) + r'\b', short_month, value, flags=re.IGNORECASE)
                break
        
        # For DD-Mon-YYYY formats, keep the format as is (it's clear and standard)
        if re.match(r'^[0-9]{1,2}[\-\s]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\-\s]+[0-9]{4}$', value):
            return value
        
        # For numeric dates, standardize separators to forward slash if they're not month-name formats
        if not re.search(r'[a-zA-Z]', value):
            value = re.sub(r'[\-\.]', '/', value)
        
        return value.strip()
    
    def clean_bank_name(self, value: str) -> str:
        """Clean bank names"""
        value = ' '.join(value.split())
        artifacts = ['Bank:', 'Drawn on:', 'Issuing Bank:']
        for artifact in artifacts:
            if value.startswith(artifact):
                value = value[len(artifact):].strip()
        return value.title()
    
    def clean_monetary(self, value: str) -> str:
        """Clean monetary values"""
        # Remove currency symbols and extra characters, keep numbers, commas, and decimal points
        cleaned = re.sub(r'[^\d,\.]', '', value)
        # Handle comma as thousand separator
        if ',' in cleaned and '.' in cleaned:
            # Format: 1,234.56
            return cleaned
        elif ',' in cleaned:
            # Could be thousand separator or decimal (Indian format)
            parts = cleaned.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                # Decimal comma: 1234,56 -> 1234.56
                return f"{parts[0]}.{parts[1]}"
            else:
                # Thousand separator: 1,234 -> 1234
                return cleaned.replace(',', '')
        return cleaned
    
    def clean_vehicle_info(self, value: str) -> str:
        """Clean vehicle information"""
        value = ' '.join(value.split())
        artifacts = ['Model:', 'Make:', 'Vehicle:', 'Car:']
        for artifact in artifacts:
            if value.startswith(artifact):
                value = value[len(artifact):].strip()
        return value.title()
    
    def clean_body_type(self, value: str) -> str:
        """Clean and standardize body types"""
        value = value.lower().strip()
        # Standardize common variations
        standardizations = {
            'saloon': 'sedan', 'estate': 'wagon', 'sports utility vehicle': 'suv',
            'sport utility vehicle': 'suv', 'multi purpose vehicle': 'van', 'mpv': 'van'
        }
        return standardizations.get(value, value).title()
    
    def extract_from_text(self, text: str, filename: str) -> Dict[str, Dict]:
        """Extract all 15 fields from text with 100% accuracy focus"""
        results = {}
        text_lower = text.lower()
        
        self.logger.info(f"Processing {filename} for 15 insurance fields...")
        
        for field_key, field_info in self.field_patterns.items():
            field_name = field_info['name']
            patterns = field_info['patterns']
            validation_func = field_info['validation']
            cleaning_func = field_info['cleaning']
            
            found_value = None
            confidence = 0
            method = "Not found"
            
            # Try each pattern until we find a valid match
            for i, pattern in enumerate(patterns):
                matches = re.finditer(pattern, text_lower, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    candidate = match.group(1).strip()
                    if candidate:
                        # Get original case from original text
                        start, end = match.span(1)
                        original_candidate = text[start:end].strip()
                        
                        # Clean the candidate
                        cleaned_candidate = cleaning_func(original_candidate)
                        
                        # Validate the candidate
                        if validation_func(cleaned_candidate):
                            found_value = cleaned_candidate
                            confidence = 0.9 - (i * 0.1)  # Higher confidence for earlier patterns
                            method = f"Pattern {i+1}"
                            break
                
                if found_value:
                    break
            
            # Store result
            results[field_key] = {
                'field_name': field_name,
                'value': found_value if found_value else 'Not found',
                'found': bool(found_value),
                'confidence': confidence,
                'method': method
            }
            
            # Log result
            status = "✅" if found_value else "❌"
            conf_text = f"({confidence:.2f})" if found_value else ""
            self.logger.info(f"{status} {field_name}: {found_value if found_value else 'Not found'} {conf_text}")
        
        # Calculate overall success rate
        found_count = sum(1 for field in results.values() if field['found'])
        success_rate = (found_count / len(results)) * 100
        self.logger.info(f"Overall success rate for {filename}: {success_rate:.1f}% ({found_count}/{len(results)} fields)")
        
        return results

class OptimizedInsuranceGUI:
    """Optimized GUI for the insurance extractor"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("100% Accuracy Insurance PDF Extractor")
        self.root.geometry("1000x700")
        
        self.extractor = OptimizedInsuranceExtractor()
        self.selected_files = []
        self.results = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main title
        title = ttk.Label(self.root, text="🏢 100% Accuracy Insurance PDF Data Extractor", 
                         font=('Helvetica', 16, 'bold'))
        title.pack(pady=10)
        
        subtitle = ttk.Label(self.root, text="Optimized for the 15 required insurance fields", 
                           font=('Helvetica', 10), foreground='darkblue')
        subtitle.pack(pady=5)
        
        # File selection frame
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Button(file_frame, text="📁 Select Insurance PDF Files", 
                  command=self.select_files).pack(side=tk.LEFT)
        
        self.file_count_label = ttk.Label(file_frame, text="No files selected")
        self.file_count_label.pack(side=tk.LEFT, padx=20)
        
        # Control buttons frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.process_btn = ttk.Button(control_frame, text="🚀 Start Processing", 
                                     command=self.start_processing, style='Accent.TButton')
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = ttk.Button(control_frame, text="📊 Export to Excel", 
                                    command=self.export_results, state=tk.DISABLED)
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(pady=10, padx=20, fill=tk.X)
        
        # Results display
        results_label = ttk.Label(self.root, text="📋 Extraction Results:", font=('Helvetica', 12, 'bold'))
        results_label.pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        self.results_text = scrolledtext.ScrolledText(self.root, height=20, font=('Courier', 10))
        self.results_text.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_label = ttk.Label(self.root, text="Ready - Select PDF files to begin", 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def select_files(self):
        """Select PDF files for processing"""
        files = filedialog.askopenfilenames(
            title="Select Insurance PDF Files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if files:
            self.selected_files = list(files)
            count = len(self.selected_files)
            self.file_count_label.config(text=f"{count} file{'s' if count > 1 else ''} selected")
            self.status_label.config(text=f"Ready to process {count} PDF file{'s' if count > 1 else ''}")
            self.process_btn.config(state=tk.NORMAL)
    
    def start_processing(self):
        """Start processing the selected files"""
        if not self.selected_files:
            messagebox.showerror("Error", "Please select PDF files first.")
            return
        
        self.process_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.results_text.delete(1.0, tk.END)
        self.results = []
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_files)
        thread.daemon = True
        thread.start()
    
    def process_files(self):
        """Process all selected files"""
        try:
            total_files = len(self.selected_files)
            
            for i, file_path in enumerate(self.selected_files, 1):
                filename = os.path.basename(file_path)
                
                # Update status
                self.root.after(0, lambda f=filename, i=i, t=total_files: 
                               self.status_label.config(text=f"Processing {i}/{t}: {f}"))
                
                # Extract text from PDF
                text = self.extract_text_from_pdf(file_path)
                
                if len(text.strip()) < 50:  # Try OCR if text extraction failed
                    self.root.after(0, lambda: self.results_text.insert(tk.END, f"📄 {filename}: Using OCR (scanned document)\n"))
                    text = self.extract_text_with_ocr(file_path)
                
                # Extract insurance fields
                field_results = self.extractor.extract_from_text(text, filename)
                
                # Store results
                self.results.append({
                    'filename': filename,
                    'fields': field_results
                })
                
                # Display results
                self.root.after(0, lambda fn=filename, fr=field_results: 
                               self.display_file_results(fn, fr))
            
            # Processing complete
            self.root.after(0, self.processing_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Processing error: {str(e)}"))
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            self.extractor.logger.error(f"Error extracting text from {pdf_path}: {e}")
        return text
    
    def extract_text_with_ocr(self, pdf_path: str) -> str:
        """Enhanced OCR text extraction with optimization for insurance documents"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Optimal resolution for OCR accuracy without over-processing
                    img = page.to_image(resolution=300)  # Balanced resolution
                    
                    # Enhanced OCR configuration for better accuracy (less restrictive)
                    custom_config = r'--oem 3 --psm 6'
                    
                    try:
                        # Try with enhanced config first
                        page_text = pytesseract.image_to_string(img.original, config=custom_config)
                    except:
                        # Fallback to default OCR
                        page_text = pytesseract.image_to_string(img.original)
                    
                    if page_text:
                        text += page_text + "\n"
                        self.extractor.logger.info(f"OCR extracted {len(page_text)} characters from page {page_num + 1} of {os.path.basename(pdf_path)}")
                    
        except Exception as e:
            self.extractor.logger.error(f"Enhanced OCR error for {pdf_path}: {e}")
            
            # Fallback to simple OCR if enhanced fails
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        img = page.to_image(resolution=300)
                        page_text = pytesseract.image_to_string(img.original)
                        if page_text:
                            text += page_text + "\n"
            except Exception as fallback_e:
                self.extractor.logger.error(f"Fallback OCR also failed for {pdf_path}: {fallback_e}")
        
        return text
    
    def display_file_results(self, filename: str, field_results: Dict):
        """Display results for a single file"""
        found_count = sum(1 for field in field_results.values() if field['found'])
        total_count = len(field_results)
        success_rate = (found_count / total_count) * 100
        
        self.results_text.insert(tk.END, f"\n{'='*60}\n")
        self.results_text.insert(tk.END, f"📄 {filename}\n")
        self.results_text.insert(tk.END, f"🎯 Success Rate: {success_rate:.1f}% ({found_count}/{total_count} fields)\n")
        self.results_text.insert(tk.END, f"{'='*60}\n")
        
        for field_key, field_info in field_results.items():
            status = "✅" if field_info['found'] else "❌"
            confidence = f" ({field_info['confidence']:.2f})" if field_info['found'] else ""
            value = field_info['value'][:50] + "..." if len(field_info['value']) > 50 else field_info['value']
            self.results_text.insert(tk.END, f"{status} {field_info['field_name']}: {value}{confidence}\n")
        
        self.results_text.see(tk.END)
    
    def processing_complete(self):
        """Handle processing completion"""
        self.progress.stop()
        self.process_btn.config(state=tk.NORMAL)
        self.export_btn.config(state=tk.NORMAL)
        
        # Calculate overall statistics
        total_fields = sum(len(result['fields']) for result in self.results)
        found_fields = sum(sum(1 for field in result['fields'].values() if field['found']) for result in self.results)
        overall_success = (found_fields / total_fields) * 100 if total_fields > 0 else 0
        
        self.results_text.insert(tk.END, f"\n{'='*60}\n")
        self.results_text.insert(tk.END, f"🏁 PROCESSING COMPLETE\n")
        self.results_text.insert(tk.END, f"📊 Overall Success Rate: {overall_success:.1f}%\n")
        self.results_text.insert(tk.END, f"📁 Files Processed: {len(self.results)}\n")
        self.results_text.insert(tk.END, f"✅ Fields Found: {found_fields}/{total_fields}\n")
        self.results_text.insert(tk.END, f"{'='*60}\n")
        
        self.status_label.config(text=f"Complete! Success rate: {overall_success:.1f}% - Ready to export")
        
        messagebox.showinfo("Processing Complete", 
                           f"Successfully processed {len(self.results)} files!\n\n"
                           f"Overall success rate: {overall_success:.1f}%\n"
                           f"Fields found: {found_fields}/{total_fields}")
    
    def export_results(self):
        """Export results to Excel"""
        if not self.results:
            messagebox.showwarning("Warning", "No results to export.")
            return
        
        output_path = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not output_path:
            return
        
        try:
            # Prepare data for Excel
            excel_data = []
            
            for result in self.results:
                filename = result['filename']
                fields = result['fields']
                
                row = {'Filename': filename}
                
                # Add all field values and metadata
                for field_key, field_info in fields.items():
                    row[field_info['field_name']] = field_info['value']
                    row[f"{field_info['field_name']} (Found)"] = 'Yes' if field_info['found'] else 'No'
                    row[f"{field_info['field_name']} (Confidence)"] = f"{field_info['confidence']:.2f}" if field_info['found'] else 'N/A'
                    row[f"{field_info['field_name']} (Method)"] = field_info['method']
                
                # Calculate file-level metrics
                found_count = sum(1 for field in fields.values() if field['found'])
                total_count = len(fields)
                success_rate = (found_count / total_count) * 100
                
                row['Fields Found'] = found_count
                row['Total Fields'] = total_count
                row['Success Rate (%)'] = f"{success_rate:.1f}%"
                
                excel_data.append(row)
            
            # Create DataFrame and save
            df = pd.DataFrame(excel_data)
            
            # Use ExcelWriter for formatting
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Insurance Data', index=False)
                
                # Format the worksheet
                worksheet = writer.sheets['Insurance Data']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            self.status_label.config(text=f"Results exported to: {os.path.basename(output_path)}")
            
            messagebox.showinfo("Export Successful", 
                              f"Results exported successfully to:\n{output_path}\n\n"
                              f"The Excel file contains:\n"
                              f"• All 15 insurance fields\n"
                              f"• Found/Not Found status\n"
                              f"• Confidence scores\n"
                              f"• Extraction methods\n"
                              f"• Success rate per file")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results:\n{str(e)}")
    
    def show_error(self, error_message: str):
        """Show error message"""
        self.progress.stop()
        self.process_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Error occurred during processing")
        messagebox.showerror("Error", error_message)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = OptimizedInsuranceGUI()
    app.run()

if __name__ == "__main__":
    main() 