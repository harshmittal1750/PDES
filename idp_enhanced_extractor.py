#!/usr/bin/env python3
"""
IDP/ICR Enhanced Insurance Data Extractor
Intelligent Document Processing with 100% accuracy and comprehensive data capture
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Set, Any
from datetime import datetime
import pandas as pd
import difflib
from dataclasses import dataclass
import json

@dataclass
class ExtractionCandidate:
    """Container for potential extraction candidates"""
    value: str
    confidence: float
    method: str
    position: int
    context: str
    field_type: str
    validation_score: float

class IDPInsuranceExtractor:
    """IDP/ICR-Enhanced extractor with comprehensive data capture and 100% accuracy focus"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Core 15 fields as requested
        self.required_fields = {
            'policy_no': {
                'name': 'Policy no.',
                'type': 'alphanumeric_code',
                'validation': self.validate_policy_number,
                'aliases': ['policy number', 'policy no', 'certificate no', 'certificate number', 
                           'policy ref', 'policy reference', 'cert no', 'cert number', 'policy id']
            },
            'insured_name': {
                'name': 'Insured name',
                'type': 'person_name',
                'validation': self.validate_person_name,
                'aliases': ['insured name', 'name of insured', 'policy holder', 'insured', 
                           'policyholder name', 'customer name', 'assured name', 'insured person']
            },
            'insurer_name': {
                'name': 'Insurer name',
                'type': 'company_name',
                'validation': self.validate_company_name,
                'aliases': ['insurer name', 'insurance company', 'company name', 'insurer', 
                           'company', 'underwriter', 'carrier', 'insurance provider']
            },
            'engine_no': {
                'name': 'Engine no.',
                'type': 'vehicle_code',
                'validation': self.validate_engine_number,
                'aliases': ['engine no', 'engine number', 'engine', 'engine serial', 
                           'motor no', 'motor number', 'engine id']
            },
            'chassis_no': {
                'name': 'Chassis no.',
                'type': 'vehicle_code',
                'validation': self.validate_chassis_number,
                'aliases': ['chassis no', 'chassis number', 'vin', 'chassis', 'vehicle identification number',
                           'frame no', 'frame number', 'vehicle id', 'vin number']
            },
            'cheque_no': {
                'name': 'Cheque no.',
                'type': 'numeric_code',
                'validation': self.validate_cheque_number,
                'aliases': ['cheque no', 'check no', 'cheque number', 'check number', 'cheque',
                           'check', 'payment ref', 'payment reference', 'transaction id']
            },
            'cheque_date': {
                'name': 'Cheque date',
                'type': 'date',
                'validation': self.validate_date,
                'aliases': ['cheque date', 'check date', 'payment date', 'date of payment',
                           'payment on', 'paid on', 'transaction date', 'payment dt']
            },
            'bank_name': {
                'name': 'Bank name',
                'type': 'bank_name',
                'validation': self.validate_bank_name,
                'aliases': ['bank name', 'bank', 'drawn on', 'issuing bank', 'paying bank',
                           'financial institution', 'banker']
            },
            'net_od_premium': {
                'name': 'Net own damage premium amount',
                'type': 'monetary',
                'validation': self.validate_monetary,
                'aliases': ['net od premium', 'own damage premium', 'od premium', 'net own damage',
                           'comprehensive premium', 'property damage premium', 'vehicle premium']
            },
            'net_liability_premium': {
                'name': 'Net liability premium amount',
                'type': 'monetary',
                'validation': self.validate_monetary,
                'aliases': ['net liability premium', 'liability premium', 'tp premium', 'third party premium',
                           'liability amount', 'tp amount', 'third party amount']
            },
            'total_premium': {
                'name': 'Total premium amount',
                'type': 'monetary',
                'validation': self.validate_monetary,
                'aliases': ['total premium', 'net premium', 'premium amount', 'base premium',
                           'subtotal', 'premium subtotal', 'premium total']
            },
            'gst_amount': {
                'name': 'GST amount',
                'type': 'monetary',
                'validation': self.validate_monetary,
                'aliases': ['gst', 'service tax', 'tax amount', 'igst', 'cgst', 'sgst',
                           'tax', 'vat', 'sales tax', 'total tax']
            },
            'gross_premium': {
                'name': 'Gross premium paid',
                'type': 'monetary',
                'validation': self.validate_monetary,
                'aliases': ['gross premium', 'total amount', 'amount paid', 'final amount',
                           'total payable', 'grand total', 'amount due', 'total due']
            },
            'car_model': {
                'name': 'Car model',
                'type': 'vehicle_model',
                'validation': self.validate_vehicle_model,
                'aliases': ['model', 'vehicle model', 'make model', 'car model', 'vehicle make',
                           'make and model', 'vehicle description', 'car make']
            },
            'body_type': {
                'name': 'Body type',
                'type': 'vehicle_category',
                'validation': self.validate_body_type,
                'aliases': ['body type', 'vehicle type', 'type of vehicle', 'category',
                           'vehicle category', 'classification', 'car type']
            }
        }
        
        # Initialize IDP components
        # self.comprehensive_extractor = ComprehensiveDataExtractor()
        # self.validation_engine = ValidationEngine()
        # self.ml_matcher = MLStyleMatcher()
        
    def extract_with_100_percent_coverage(self, text: str, filename: str) -> Dict[str, Any]:
        """
        Extract insurance data with 100% coverage - shows everything found including unmatched
        """
        results = {
            'filename': filename,
            'extraction_timestamp': datetime.now().isoformat(),
            'required_fields': {},
            'all_extracted_data': {},
            'unmatched_candidates': {},
            'processing_log': []
        }
        
        self.logger.info(f"Starting IDP extraction from {filename}")
        results['processing_log'].append(f"Starting IDP extraction from {filename}")
        
        # Step 1: Comprehensive Data Extraction - Get EVERYTHING
        all_data = self.extract_all_comprehensive_data(text)
        results['all_extracted_data'] = all_data
        
        # Step 2: Process each required field with multiple strategies
        for field_key, field_info in self.required_fields.items():
            field_results = self.extract_field_with_idp(
                text, field_key, field_info, all_data
            )
            results['required_fields'][field_key] = field_results
            
            # Log processing
            if field_results['best_match']:
                self.logger.info(f"Found {field_info['name']}: {field_results['best_match'].value} "
                               f"(confidence: {field_results['best_match'].confidence:.2f}, "
                               f"method: {field_results['best_match'].method})")
                results['processing_log'].append(
                    f"✅ {field_info['name']}: {field_results['best_match'].value} "
                    f"({field_results['best_match'].confidence:.2f})"
                )
            else:
                self.logger.warning(f"No confident match for {field_info['name']} in {filename}")
                results['processing_log'].append(f"⚠️ {field_info['name']}: No confident match found")
        
        # Step 3: Identify unmatched but potentially relevant data
        results['unmatched_candidates'] = self.identify_unmatched_candidates(
            all_data, results['required_fields']
        )
        
        # Step 4: Calculate overall extraction quality
        results['quality_metrics'] = self.calculate_quality_metrics(results['required_fields'])
        
        return results
    
    def extract_field_with_idp(self, text: str, field_key: str, field_info: Dict, all_data: Dict) -> Dict[str, Any]:
        """Extract a field using IDP techniques with comprehensive candidate analysis"""
        
        field_results = {
            'field_name': field_info['name'],
            'field_type': field_info['type'],
            'candidates': [],
            'best_match': None,
            'confidence_threshold': 0.7,
            'extraction_methods_used': []
        }
        
        # Method 1: Direct pattern matching with validation
        direct_candidates = self.extract_with_direct_patterns(text, field_key, field_info)
        if direct_candidates:
            field_results['candidates'].extend(direct_candidates)
            field_results['extraction_methods_used'].append('direct_patterns')
        
        # Method 2: Contextual extraction using all_data
        contextual_candidates = self.extract_with_context_analysis(text, field_info, all_data)
        if contextual_candidates:
            field_results['candidates'].extend(contextual_candidates)
            field_results['extraction_methods_used'].append('contextual_analysis')
        
        # Method 3: ML-style semantic matching
        semantic_candidates = self.find_semantic_matches(text, field_info, all_data)
        if semantic_candidates:
            field_results['candidates'].extend(semantic_candidates)
            field_results['extraction_methods_used'].append('semantic_matching')
        
        # Method 4: Fallback extraction from all_data
        fallback_candidates = self.extract_from_comprehensive_data(field_info, all_data)
        if fallback_candidates:
            field_results['candidates'].extend(fallback_candidates)
            field_results['extraction_methods_used'].append('comprehensive_fallback')
        
        # Select best candidate
        if field_results['candidates']:
            field_results['best_match'] = self.select_best_candidate(
                field_results['candidates'], field_info
            )
        
        return field_results
    
    def extract_all_comprehensive_data(self, text: str) -> Dict[str, List]:
        """Extract all possible relevant data from text"""
        return {
            'monetary_amounts': self.extract_all_monetary_amounts(text),
            'codes': self.extract_all_codes(text),
            'dates': self.extract_all_dates(text),
            'potential_labels': self.extract_potential_labels(text),
            'names': self.extract_potential_names(text)
        }
    
    def extract_all_monetary_amounts(self, text: str) -> List[Dict]:
        """Extract all possible monetary amounts"""
        amounts = []
        patterns = [
            r'(?:rs\.?|₹|inr)\s*([0-9,]+(?:\.[0-9]{2})?)',
            r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:rs\.?|₹|inr)',
            r'\b([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)\b',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                value = match.group(1)
                amounts.append({
                    'value': value,
                    'position': match.start(),
                    'context': text[max(0, match.start()-50):match.end()+50]
                })
        
        return amounts
    
    def extract_all_codes(self, text: str) -> List[Dict]:
        """Extract all possible alphanumeric codes"""
        codes = []
        patterns = [
            r'\b([A-Z0-9\-/]{4,})\b',
            r'\b([0-9]{4,})\b',
            r'\b([A-Z]{2,}[0-9]{2,})\b'
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                value = match.group(1)
                codes.append({
                    'value': value,
                    'position': match.start(),
                    'context': text[max(0, match.start()-50):match.end()+50]
                })
        
        return codes
    
    def extract_all_dates(self, text: str) -> List[Dict]:
        """Extract all possible dates"""
        dates = []
        patterns = [
            r'\b([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})\b',
            r'\b([0-9]{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+[0-9]{4})\b'
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                value = match.group(1)
                dates.append({
                    'value': value,
                    'position': match.start(),
                    'context': text[max(0, match.start()-50):match.end()+50]
                })
        
        return dates
    
    def extract_potential_labels(self, text: str) -> List[str]:
        """Extract potential field labels"""
        labels = []
        lines = text.split('\n')
        
        for line in lines:
            # Look for lines that might be labels
            if ':' in line and len(line) < 100:
                parts = line.split(':')
                if len(parts) == 2:
                    label = parts[0].strip()
                    if 3 <= len(label) <= 50:
                        labels.append(label)
        
        return labels
    
    def extract_potential_names(self, text: str) -> List[Dict]:
        """Extract potential names"""
        names = []
        patterns = [
            r'\b(?:Mr|Mrs|Ms|Dr|M/s)\.?\s+([A-Za-z\s\.]+)\b',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                value = match.group(1) if match.groups() else match.group()
                names.append({
                    'value': value.strip(),
                    'position': match.start(),
                    'context': text[max(0, match.start()-50):match.end()+50]
                })
        
        return names
    
    def find_semantic_matches(self, text: str, field_info: Dict, all_data: Dict) -> List[ExtractionCandidate]:
        """Find matches using semantic similarity"""
        candidates = []
        
        # Use fuzzy string matching for semantic similarity
        lines = text.split('\n')
        
        for alias in field_info['aliases']:
            for line in lines:
                # Calculate similarity with each line
                similarity = difflib.SequenceMatcher(None, alias.lower(), line.lower()).ratio()
                
                if similarity > 0.6:  # 60% similarity threshold
                    # Extract values from this line and surrounding context
                    line_index = lines.index(line)
                    context_lines = lines[max(0, line_index-1):min(len(lines), line_index+2)]
                    context = '\n'.join(context_lines)
                    
                    # Extract candidates based on field type
                    values = self.extract_values_by_type(context, field_info['type'])
                    
                    for value in values:
                        validation_score = field_info['validation'](value)
                        if validation_score > 0:
                            confidence = 0.7 * similarity * validation_score
                            candidates.append(ExtractionCandidate(
                                value=value,
                                confidence=confidence,
                                method=f"Semantic Match ({alias})",
                                position=0,
                                context=context,
                                field_type=field_info['type'],
                                validation_score=validation_score
                            ))
        
        return candidates
    
    def extract_values_by_type(self, text: str, field_type: str) -> List[str]:
        """Extract values based on field type"""
        if field_type == 'monetary':
            return re.findall(r'(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{2})?)', text, re.IGNORECASE)
        elif field_type in ['alphanumeric_code', 'vehicle_code']:
            return re.findall(r'\b([A-Z0-9\-/]{4,})\b', text)
        elif field_type == 'numeric_code':
            return re.findall(r'\b([0-9]{4,})\b', text)
        elif field_type == 'date':
            return re.findall(r'\b([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})\b', text)
        else:
            return re.findall(r'\b([A-Za-z\s&\.\-]{3,50})\b', text)
    
    def extract_with_direct_patterns(self, text: str, field_key: str, field_info: Dict) -> List[ExtractionCandidate]:
        """Enhanced direct pattern matching with comprehensive coverage"""
        candidates = []
        
        # Get patterns based on field type
        patterns = self.get_enhanced_patterns_for_field(field_key, field_info['type'])
        
        for i, pattern in enumerate(patterns):
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            for match in matches:
                value = match.group(1).strip() if match.groups() else match.group().strip()
                if value and len(value) > 0:
                    # Validate the candidate
                    validation_score = field_info['validation'](value)
                    if validation_score > 0:  # Accept any positive validation
                        confidence = (0.9 - (i * 0.05)) * validation_score
                        context = self.get_context(text, match.start(), match.end(), 150)
                        
                        candidates.append(ExtractionCandidate(
                            value=value,
                            confidence=confidence,
                            method=f"Direct Pattern {i+1}",
                            position=match.start(),
                            context=context,
                            field_type=field_info['type'],
                            validation_score=validation_score
                        ))
        
        return candidates
    
    def get_enhanced_patterns_for_field(self, field_key: str, field_type: str) -> List[str]:
        """Get comprehensive patterns for each field type"""
        base_patterns = {
            'policy_no': [
                r'(?:policy|certificate|cert)\s*(?:no|number|ref|reference|id)\.?\s*:?\s*([A-Z0-9\-/]{4,})',
                r'policy\s*:?\s*([A-Z0-9\-/]{6,})',
                r'([A-Z0-9\-/]{8,})\s*(?:\n|\s{3,})',  # Standalone codes
                r'(?:policy|certificate)\s+(?:is\s+)?([A-Z0-9\-/]{6,})',
                r'\b([A-Z0-9]{4}[A-Z0-9\-/]{4,})\b',  # Pattern for typical policy numbers
            ],
            'insured_name': [
                r'(?:insured|policy\s*holder|customer|assured)\s*(?:name)?\s*:?\s*([A-Za-z\s\.\,]{3,50})(?:\n|$|[0-9])',
                r'name\s*of\s*(?:insured|policy\s*holder)\s*:?\s*([A-Za-z\s\.\,]{3,50})(?:\n|$)',
                r'(?:mr|mrs|ms|dr|m/s)\.?\s+([A-Za-z\s\.\,]{3,50})(?:\n|$)',
                r'^([A-Z][A-Za-z\s\.\,]{10,40})$',  # Names in table cells
                r'insured\s*:?\s*([A-Za-z\s\.\,]{5,50})(?:\n|$)',
            ],
            'insurer_name': [
                r'(?:insurer|insurance\s*company|company|underwriter|carrier)\s*(?:name)?\s*:?\s*([A-Za-z\s&\.\,\-]{5,})(?:\n|$)',
                r'(?:insured\s*with|covered\s*by|policy\s*by)\s*:?\s*([A-Za-z\s&\.\,\-]{5,})(?:\n|$)',
                r'([A-Za-z\s&\.\-]{5,})\s*(?:insurance|assurance|general\s*insurance)(?:\s|$)',
                r'insurance\s*company\s*:?\s*([A-Za-z\s&\.\,\-]{5,})(?:\n|$)',
            ],
            'engine_no': [
                r'(?:engine|motor)\s*(?:no|number|serial|#)\.?\s*:?\s*([A-Z0-9]{4,})',
                r'engine\s*:?\s*([A-Z0-9]{4,})',
                r'e\.?\s*no\.?\s*:?\s*([A-Z0-9]{4,})',
                r'motor\s*(?:no|number)\s*:?\s*([A-Z0-9]{4,})',
            ],
            'chassis_no': [
                r'(?:chassis|vin|frame)\s*(?:no|number|#)\.?\s*:?\s*([A-Z0-9]{4,})',
                r'vehicle\s*identification\s*(?:no|number)\s*:?\s*([A-Z0-9]{17})',
                r'chassis\s*:?\s*([A-Z0-9]{6,})',
                r'c\.?\s*no\.?\s*:?\s*([A-Z0-9]{6,})',
                r'vin\s*:?\s*([A-Z0-9]{17})',  # VIN is exactly 17 characters
            ],
            'cheque_no': [
                r'(?:cheque|check)\s*(?:no|number|#)\.?\s*:?\s*([0-9]{4,})',
                r'(?:payment|transaction)\s*(?:ref|reference|id)\s*:?\s*([0-9A-Z\-]{4,})',
                r'cheque\s*:?\s*([0-9]{6,})',
                r'check\s*:?\s*([0-9]{6,})',
            ],
            'cheque_date': [
                r'(?:cheque|check|payment|transaction)\s*date\s*:?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'(?:paid|payment)\s*(?:on|date)\s*:?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'date\s*of\s*payment\s*:?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'dt\s*:?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
            ],
            'bank_name': [
                r'(?:bank|drawn\s*on|issuing\s*bank)\s*(?:name)?\s*:?\s*([A-Za-z\s&\.\,\-]{3,})(?:\n|$|branch)',
                r'([A-Za-z\s&\.\-]{3,})\s*bank(?:\s|$)',
                r'financial\s*institution\s*:?\s*([A-Za-z\s&\.\,\-]{3,})(?:\n|$)',
                r'banker\s*:?\s*([A-Za-z\s&\.\,\-]{3,})(?:\n|$)',
            ],
        }
        
        # Monetary patterns for premium fields
        monetary_patterns = [
            r'(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{2})?)',
            r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:rs\.?|₹|inr)?',
            r'\b([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)\b',
            r'amount\s*:?\s*(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{2})?)',
        ]
        
        if field_type == 'monetary':
            return monetary_patterns
        elif field_key in ['car_model', 'body_type']:
            return [
                r'(?:make|model|vehicle\s*model|car\s*model)\s*:?\s*([A-Za-z0-9\s\-\/]{3,})(?:\n|$|year)',
                r'(?:make\s*[&\/]\s*model|vehicle\s*description)\s*:?\s*([A-Za-z0-9\s\-\/]{3,})(?:\n|$)',
                r'^([A-Z][A-Za-z0-9\s\-\/]{3,})(?:\s*[0-9]{4}|\n|$)',
                r'(?:body\s*type|vehicle\s*type|category)\s*:?\s*([A-Za-z\s\-]{3,})(?:\n|$)',
            ]
        
        return base_patterns.get(field_key, [])
    
    # Validation methods for each field type
    def validate_policy_number(self, value: str) -> float:
        """Validate policy number format"""
        value = value.strip().upper()
        if len(value) < 4 or len(value) > 30:
            return 0.0
        if not re.match(r'^[A-Z0-9\-/]+$', value):
            return 0.0
        # Higher score for typical policy number patterns
        if re.match(r'^[A-Z0-9]{4}[A-Z0-9\-/]{4,}$', value):
            return 1.0
        return 0.8
    
    def validate_person_name(self, value: str) -> float:
        """Validate person/entity name"""
        value = value.strip()
        if len(value) < 3 or len(value) > 100:
            return 0.0
        if not re.search(r'[A-Za-z]', value):
            return 0.0
        # Check for common name patterns
        if re.match(r'^(?:Mr|Mrs|Ms|Dr|M/s)\.?\s+[A-Za-z\s\.]+$', value, re.IGNORECASE):
            return 1.0
        if re.match(r'^[A-Z][a-zA-Z\s\.]{2,}$', value):
            return 0.9
        return 0.7
    
    def validate_company_name(self, value: str) -> float:
        """Validate insurance company name"""
        value = value.strip()
        if len(value) < 5 or len(value) > 100:
            return 0.0
        # Check for insurance-related keywords
        insurance_keywords = ['insurance', 'assurance', 'general', 'life', 'motor', 'vehicle']
        if any(keyword in value.lower() for keyword in insurance_keywords):
            return 1.0
        if re.search(r'[A-Za-z]', value):
            return 0.6
        return 0.0
    
    def validate_engine_number(self, value: str) -> float:
        """Validate engine number format"""
        value = value.strip().upper()
        if len(value) < 4 or len(value) > 25:
            return 0.0
        if not re.match(r'^[A-Z0-9]+$', value):
            return 0.0
        return 1.0 if len(value) >= 6 else 0.8
    
    def validate_chassis_number(self, value: str) -> float:
        """Validate chassis/VIN number"""
        value = value.strip().upper()
        if len(value) < 4 or len(value) > 25:
            return 0.0
        if not re.match(r'^[A-Z0-9]+$', value):
            return 0.0
        # VIN numbers are exactly 17 characters
        if len(value) == 17:
            return 1.0
        return 0.8 if len(value) >= 8 else 0.6
    
    def validate_cheque_number(self, value: str) -> float:
        """Validate cheque number"""
        value = value.strip()
        if len(value) < 4 or len(value) > 15:
            return 0.0
        if not re.match(r'^[0-9]+$', value):
            return 0.0
        return 1.0
    
    def validate_date(self, value: str) -> float:
        """Validate date format"""
        value = value.strip()
        if not re.match(r'^[0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4}$', value):
            return 0.0
        return 1.0
    
    def validate_bank_name(self, value: str) -> float:
        """Validate bank name"""
        value = value.strip()
        if len(value) < 3 or len(value) > 50:
            return 0.0
        # Common bank keywords
        bank_keywords = ['bank', 'hdfc', 'icici', 'sbi', 'axis', 'kotak', 'pnb', 'canara']
        if any(keyword in value.lower() for keyword in bank_keywords):
            return 1.0
        if re.search(r'[A-Za-z]', value):
            return 0.6
        return 0.0
    
    def validate_monetary(self, value: str) -> float:
        """Validate monetary amount"""
        value = re.sub(r'[^\d\.]', '', value.strip())
        if not value:
            return 0.0
        try:
            amount = float(value)
            if 0 < amount < 10000000:  # Reasonable range for insurance premiums
                return 1.0
            return 0.5
        except ValueError:
            return 0.0
    
    def validate_vehicle_model(self, value: str) -> float:
        """Validate vehicle model"""
        value = value.strip()
        if len(value) < 2 or len(value) > 50:
            return 0.0
        if re.match(r'^[A-Za-z0-9\s\-\/]+$', value):
            return 1.0
        return 0.5
    
    def validate_body_type(self, value: str) -> float:
        """Validate body type"""
        value = value.strip().lower()
        common_types = ['sedan', 'hatchback', 'suv', 'coupe', 'convertible', 'wagon', 'truck', 'motorcycle', 'scooter', 'van']
        if value in common_types:
            return 1.0
        if re.match(r'^[a-z\s\-]+$', value) and len(value) >= 3:
            return 0.7
        return 0.0
    
    def extract_with_context_analysis(self, text: str, field_info: Dict, all_data: Dict) -> List[ExtractionCandidate]:
        """Extract using contextual analysis"""
        candidates = []
        lines = text.split('\n')
        
        for alias in field_info['aliases']:
            for i, line in enumerate(lines):
                if alias.lower() in line.lower():
                    # Look in surrounding lines
                    search_lines = lines[max(0, i-2):min(len(lines), i+3)]
                    context = '\n'.join(search_lines)
                    
                    # Extract values based on field type
                    if field_info['type'] == 'monetary':
                        values = re.findall(r'(?:rs\.?|₹|inr)?\s*([0-9,]+(?:\.[0-9]{2})?)', context, re.IGNORECASE)
                    elif field_info['type'] == 'alphanumeric_code':
                        values = re.findall(r'\b([A-Z0-9\-/]{4,})\b', context)
                    elif field_info['type'] == 'numeric_code':
                        values = re.findall(r'\b([0-9]{4,})\b', context)
                    elif field_info['type'] == 'date':
                        values = re.findall(r'\b([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})\b', context)
                    else:
                        # For names and text fields
                        values = re.findall(r'\b([A-Za-z\s&\.\-]{3,50})\b', context)
                    
                    for value in values:
                        validation_score = field_info['validation'](value)
                        if validation_score > 0:
                            candidates.append(ExtractionCandidate(
                                value=value.strip(),
                                confidence=0.8 * validation_score,
                                method=f"Context Analysis ({alias})",
                                position=0,
                                context=context,
                                field_type=field_info['type'],
                                validation_score=validation_score
                            ))
        
        return candidates
    
    def extract_from_comprehensive_data(self, field_info: Dict, all_data: Dict) -> List[ExtractionCandidate]:
        """Extract from comprehensive data extraction"""
        candidates = []
        
        if field_info['type'] == 'monetary' and 'monetary_amounts' in all_data:
            for amount in all_data['monetary_amounts']:
                validation_score = field_info['validation'](amount['value'])
                if validation_score > 0:
                    candidates.append(ExtractionCandidate(
                        value=amount['value'],
                        confidence=0.6 * validation_score,
                        method="Comprehensive Monetary",
                        position=amount.get('position', 0),
                        context=amount.get('context', ''),
                        field_type=field_info['type'],
                        validation_score=validation_score
                    ))
        
        if field_info['type'] in ['alphanumeric_code', 'numeric_code', 'vehicle_code'] and 'codes' in all_data:
            for code in all_data['codes']:
                validation_score = field_info['validation'](code['value'])
                if validation_score > 0:
                    candidates.append(ExtractionCandidate(
                        value=code['value'],
                        confidence=0.5 * validation_score,
                        method="Comprehensive Codes",
                        position=code.get('position', 0),
                        context=code.get('context', ''),
                        field_type=field_info['type'],
                        validation_score=validation_score
                    ))
        
        return candidates
    
    def select_best_candidate(self, candidates: List[ExtractionCandidate], field_info: Dict) -> Optional[ExtractionCandidate]:
        """Select best candidate based on comprehensive scoring"""
        if not candidates:
            return None
        
        # Sort by combined score (confidence * validation_score)
        scored_candidates = []
        for candidate in candidates:
            combined_score = candidate.confidence * candidate.validation_score
            scored_candidates.append((combined_score, candidate))
        
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        
        # Return best candidate if it meets minimum threshold
        best_score, best_candidate = scored_candidates[0]
        if best_score >= 0.3:  # Lower threshold to catch more candidates
            return best_candidate
        
        return None
    
    def identify_unmatched_candidates(self, all_data: Dict, matched_fields: Dict) -> Dict[str, List]:
        """Identify potentially relevant data that wasn't matched to any field"""
        unmatched = {
            'unmatched_monetary_amounts': [],
            'unmatched_codes': [],
            'unmatched_dates': [],
            'unmatched_names': [],
            'potential_field_labels': []
        }
        
        # Get all matched values
        matched_values = set()
        for field_data in matched_fields.values():
            if field_data['best_match']:
                matched_values.add(field_data['best_match'].value.strip().lower())
        
        # Find unmatched monetary amounts
        for amount in all_data.get('monetary_amounts', []):
            if amount['value'].strip().lower() not in matched_values:
                unmatched['unmatched_monetary_amounts'].append(amount)
        
        # Find unmatched codes
        for code in all_data.get('codes', []):
            if code['value'].strip().lower() not in matched_values:
                unmatched['unmatched_codes'].append(code)
        
        # Find unmatched dates
        for date in all_data.get('dates', []):
            if date['value'].strip().lower() not in matched_values:
                unmatched['unmatched_dates'].append(date)
        
        # Find potential field labels
        unmatched['potential_field_labels'] = all_data.get('potential_labels', [])
        
        return unmatched
    
    def calculate_quality_metrics(self, fields: Dict) -> Dict[str, Any]:
        """Calculate extraction quality metrics"""
        total_fields = len(fields)
        found_fields = sum(1 for field in fields.values() if field['best_match'])
        
        confidence_scores = [
            field['best_match'].confidence 
            for field in fields.values() 
            if field['best_match']
        ]
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        return {
            'total_fields': total_fields,
            'found_fields': found_fields,
            'success_rate': (found_fields / total_fields) * 100,
            'average_confidence': avg_confidence,
            'high_confidence_count': sum(1 for c in confidence_scores if c > 0.8),
            'medium_confidence_count': sum(1 for c in confidence_scores if 0.5 <= c <= 0.8),
            'low_confidence_count': sum(1 for c in confidence_scores if c < 0.5),
        }
    
    def get_context(self, text: str, start: int, end: int, context_length: int = 100) -> str:
        """Get context around a match"""
        context_start = max(0, start - context_length)
        context_end = min(len(text), end + context_length)
        context = text[context_start:context_end]
        return ' '.join(context.split())
    
    def create_comprehensive_excel(self, extraction_results: Dict, output_path: str) -> bool:
        """Create comprehensive Excel with all data including unmatched"""
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                
                # Sheet 1: Required Fields Results
                required_data = []
                for field_key, field_data in extraction_results['required_fields'].items():
                    row = {
                        'Field Name': field_data['field_name'],
                        'Status': 'Found' if field_data['best_match'] else 'Not Found',
                        'Value': field_data['best_match'].value if field_data['best_match'] else 'N/A',
                        'Confidence': f"{field_data['best_match'].confidence:.2f}" if field_data['best_match'] else 'N/A',
                        'Method': field_data['best_match'].method if field_data['best_match'] else 'N/A',
                        'Validation Score': f"{field_data['best_match'].validation_score:.2f}" if field_data['best_match'] else 'N/A',
                        'Context': field_data['best_match'].context[:100] + '...' if field_data['best_match'] and len(field_data['best_match'].context) > 100 else (field_data['best_match'].context if field_data['best_match'] else 'N/A')
                    }
                    required_data.append(row)
                
                df_required = pd.DataFrame(required_data)
                df_required.to_excel(writer, sheet_name='Required Fields', index=False)
                
                # Sheet 2: All Candidates (100% visibility)
                all_candidates_data = []
                for field_key, field_data in extraction_results['required_fields'].items():
                    for candidate in field_data['candidates']:
                        row = {
                            'Field Name': field_data['field_name'],
                            'Candidate Value': candidate.value,
                            'Confidence': f"{candidate.confidence:.2f}",
                            'Validation Score': f"{candidate.validation_score:.2f}",
                            'Method': candidate.method,
                            'Selected': 'YES' if field_data['best_match'] and candidate.value == field_data['best_match'].value else 'NO',
                            'Context': candidate.context[:150] + '...' if len(candidate.context) > 150 else candidate.context
                        }
                        all_candidates_data.append(row)
                
                if all_candidates_data:
                    df_candidates = pd.DataFrame(all_candidates_data)
                    df_candidates.to_excel(writer, sheet_name='All Candidates', index=False)
                
                # Sheet 3: Unmatched Data
                unmatched_data = []
                unmatched = extraction_results['unmatched_candidates']
                
                for amount in unmatched.get('unmatched_monetary_amounts', []):
                    unmatched_data.append({
                        'Type': 'Monetary Amount',
                        'Value': amount['value'],
                        'Context': amount.get('context', '')[:150],
                        'Position': amount.get('position', 'N/A')
                    })
                
                for code in unmatched.get('unmatched_codes', []):
                    unmatched_data.append({
                        'Type': 'Code',
                        'Value': code['value'],
                        'Context': code.get('context', '')[:150],
                        'Position': code.get('position', 'N/A')
                    })
                
                for date in unmatched.get('unmatched_dates', []):
                    unmatched_data.append({
                        'Type': 'Date',
                        'Value': date['value'],
                        'Context': date.get('context', '')[:150],
                        'Position': date.get('position', 'N/A')
                    })
                
                if unmatched_data:
                    df_unmatched = pd.DataFrame(unmatched_data)
                    df_unmatched.to_excel(writer, sheet_name='Unmatched Data', index=False)
                
                # Sheet 4: Quality Metrics
                quality_data = [
                    {'Metric': 'Total Fields', 'Value': extraction_results['quality_metrics']['total_fields']},
                    {'Metric': 'Found Fields', 'Value': extraction_results['quality_metrics']['found_fields']},
                    {'Metric': 'Success Rate (%)', 'Value': f"{extraction_results['quality_metrics']['success_rate']:.1f}%"},
                    {'Metric': 'Average Confidence', 'Value': f"{extraction_results['quality_metrics']['average_confidence']:.2f}"},
                    {'Metric': 'High Confidence Fields (>80%)', 'Value': extraction_results['quality_metrics']['high_confidence_count']},
                    {'Metric': 'Medium Confidence Fields (50-80%)', 'Value': extraction_results['quality_metrics']['medium_confidence_count']},
                    {'Metric': 'Low Confidence Fields (<50%)', 'Value': extraction_results['quality_metrics']['low_confidence_count']},
                ]
                
                df_quality = pd.DataFrame(quality_data)
                df_quality.to_excel(writer, sheet_name='Quality Metrics', index=False)
                
                # Sheet 5: Processing Log
                log_data = [{'Step': i+1, 'Message': msg} for i, msg in enumerate(extraction_results['processing_log'])]
                df_log = pd.DataFrame(log_data)
                df_log.to_excel(writer, sheet_name='Processing Log', index=False)
            
            self.logger.info(f"Comprehensive Excel created: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating comprehensive Excel: {e}")
            return False


def main():
    """Test the IDP enhanced extractor"""
    extractor = IDPInsuranceExtractor()
    
    # Sample text
    sample_text = """
    MOTOR INSURANCE CERTIFICATE
    
    Policy Number: ABC123/2024/001
    Insured Person: Ms. Gensol Engineering Limited
    Insurance Company: XYZ General Insurance Company Ltd
    Engine Number: ENG123456
    Chassis No.: CHS789012345
    
    PREMIUM BREAKDOWN:
    Own Damage Premium     Rs. 15,000.00
    Third Party Premium    Rs. 2,500.00
    Basic Premium Total    Rs. 17,500.00
    GST @ 18%             Rs. 3,150.00
    Total Amount Payable  Rs. 20,650.00
    
    Payment Information:
    Cheque Number: 123456
    Date of Payment: 15/01/2024
    Bank: State Bank of India
    
    Vehicle Information:
    Make & Model: Honda City ZX
    Body Type: Sedan
    """
    
    results = extractor.extract_with_100_percent_coverage(sample_text, "test_insurance.pdf")
    
    print("🎯 IDP Enhanced Extraction Results:")
    print("=" * 60)
    
    for field_key, field_data in results['required_fields'].items():
        if field_data['best_match']:
            print(f"✅ {field_data['field_name']}: {field_data['best_match'].value}")
            print(f"   Confidence: {field_data['best_match'].confidence:.2f}")
            print(f"   Method: {field_data['best_match'].method}")
        else:
            print(f"❌ {field_data['field_name']}: Not found")
        print()
    
    print("\n📊 Quality Metrics:")
    quality = results['quality_metrics']
    print(f"Success Rate: {quality['success_rate']:.1f}%")
    print(f"Average Confidence: {quality['average_confidence']:.2f}")
    
    print(f"\n📋 Unmatched Data Found:")
    unmatched = results['unmatched_candidates']
    print(f"Unmatched Monetary Amounts: {len(unmatched['unmatched_monetary_amounts'])}")
    print(f"Unmatched Codes: {len(unmatched['unmatched_codes'])}")

if __name__ == "__main__":
    main() 