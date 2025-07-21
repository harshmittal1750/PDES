#!/bin/bash

# 🔄 REBALANCED OPTIMIZED Insurance PDF Extractor - Fix Regressions + Keep Gains
echo "🔄 REBALANCED OPTIMIZED Insurance PDF Data Extractor"
echo "================================================="
echo "🎯 TARGET: 93%+ Accuracy (14/15 fields) - Fix Regressions"
echo ""
echo "📊 CURRENT ANALYSIS:"
echo "  ✅ GAINED: Engine no. + Cheque date (2 fields)"
echo "  ❌ LOST:   Insured name + Insurer name + Bank name (3 fields)"  
echo "  📈 NET:    80% (same rate, different fields)"
echo ""
echo "🔧 REBALANCING FIXES APPLIED:"
echo ""
echo "📝 VALIDATION FLEXIBILITY:"
echo "  ✅ Name validation: More flexible for OCR variations"
echo "  ✅ Company validation: Accept more insurance company patterns"
echo "  ✅ Bank validation: Include payment gateways (CUG HDFC CCAVENUE)"
echo "  ✅ Capitalization: Less strict requirements for OCR text"
echo ""
echo "⚡ OCR OPTIMIZATION:"
echo "  ✅ Resolution: Balanced 300 DPI (not over-processed)"
echo "  ✅ Configuration: Less restrictive character filtering"
echo "  ✅ Maintained: Enhanced engine/date patterns"
echo ""
echo "🎯 EXPECTED IMPROVEMENTS:"
echo "  ✅ Insured name: 'Gensol Engineering Limited' ← RESTORED"
echo "  ✅ Insurer name: 'Tata Aig General' ← RESTORED" 
echo "  ✅ Bank name: 'Cug Hdfc Ccavenue' ← RESTORED"
echo "  ✅ Engine no.: 'XPRESTXM4EV' ← MAINTAINED"
echo "  ✅ Cheque date: '05-May-2023' ← MAINTAINED"
echo ""
echo "🎯 Target Fields (15 Total):"
echo "1. Policy no.              9. Net own damage premium amount"
echo "2. Insured name ←FIXING    10. Net liability premium amount" 
echo "3. Insurer name ←FIXING    11. Total premium amount"
echo "4. Engine no. ←KEEPING     12. GST amount"
echo "5. Chassis no.            13. Gross premium paid"
echo "6. Cheque no.             14. Car model"
echo "7. Cheque date ←KEEPING    15. Body type"
echo "8. Bank name ←FIXING"
echo ""
echo "📦 Activating virtual environment..."

# Check if virtual environment exists
if [ ! -d "pdf_extractor_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source pdf_extractor_env/bin/activate

echo "✅ Virtual environment activated"
echo "🚀 Launching REBALANCED Insurance Extractor..."
echo ""
echo "🎯 Expected Final Result:"
echo "  📊 Success Rate: 93%+ (14/15 fields)"
echo "  ✅ All previous fields RESTORED"
echo "  ✅ New gains MAINTAINED"  
echo "  ✅ Best of both optimizations"
echo ""
echo "⚡ Processing with balanced accuracy and recall..."
echo ""

python optimized_insurance_extractor.py 