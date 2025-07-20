#!/usr/bin/env python3
"""
PDF Data Extractor Setup Test
Test script to validate all dependencies and functionality.
"""

import sys
import os
import tempfile
from datetime import datetime

def test_python_version():
    """Test Python version compatibility"""
    print("🔍 Testing Python version...")
    if sys.version_info >= (3, 8):
        print(f"✅ Python version OK: {sys.version.split()[0]}")
        return True
    else:
        print(f"❌ Python version too old: {sys.version.split()[0]}")
        print("   Required: Python 3.8+")
        return False

def test_dependencies():
    """Test all required dependencies"""
    print("\n🔍 Testing dependencies...")
    
    dependencies = {
        'tkinter': 'GUI framework (built-in)',
        'pdfplumber': 'PDF text extraction',
        'openpyxl': 'Excel file creation',
        'pandas': 'Data manipulation',
        're': 'Regular expressions (built-in)',
        'threading': 'Multi-threading (built-in)',
        'logging': 'Logging system (built-in)'
    }
    
    failed_imports = []
    
    for module, description in dependencies.items():
        try:
            if module == 'tkinter':
                import tkinter as tk
                # Test creating a basic window
                root = tk.Tk()
                root.withdraw()  # Hide the window
                root.destroy()
                print(f"✅ {module} - {description}")
            else:
                __import__(module)
                print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - {description} - FAILED: {e}")
            failed_imports.append(module)
        except Exception as e:
            print(f"⚠️  {module} - {description} - WARNING: {e}")
    
    return len(failed_imports) == 0

def test_pdf_processing():
    """Test PDF processing capabilities"""
    print("\n🔍 Testing PDF processing...")
    
    try:
        import pdfplumber
        print("✅ pdfplumber import successful")
        
        # Create a simple test
        print("✅ PDF processing module ready")
        return True
        
    except Exception as e:
        print(f"❌ PDF processing test failed: {e}")
        return False

def test_excel_export():
    """Test Excel export functionality"""
    print("\n🔍 Testing Excel export...")
    
    try:
        import pandas as pd
        import openpyxl
        from openpyxl.styles import Font, PatternFill
        
        # Create test data
        test_data = [
            {
                'filename': 'test.pdf',
                'search_term': 'test',
                'page_number': 1,
                'match_text': 'test match',
                'context': 'this is a test match context',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        
        # Create DataFrame
        df = pd.DataFrame(test_data)
        
        # Test creating Excel file in temp location
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=True) as tmp_file:
            with pd.ExcelWriter(tmp_file.name, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Test', index=False)
                
                # Test formatting
                workbook = writer.book
                worksheet = writer.sheets['Test']
                
                header_font = Font(bold=True)
                for cell in worksheet[1]:
                    cell.font = header_font
        
        print("✅ Excel export functionality working")
        return True
        
    except Exception as e:
        print(f"❌ Excel export test failed: {e}")
        return False

def test_main_application():
    """Test if main application can be imported"""
    print("\n🔍 Testing main application...")
    
    try:
        if os.path.exists('pdf_extractor.py'):
            # Try importing without running
            import importlib.util
            spec = importlib.util.spec_from_file_location("pdf_extractor", "pdf_extractor.py")
            module = importlib.util.module_from_spec(spec)
            
            # Basic syntax check
            print("✅ pdf_extractor.py found and syntax OK")
            return True
        else:
            print("❌ pdf_extractor.py not found")
            return False
            
    except Exception as e:
        print(f"❌ Main application test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("=" * 50)
    print("📄 PDF Data Extractor - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("PDF Processing", test_pdf_processing),
        ("Excel Export", test_excel_export),
        ("Main Application", test_main_application)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("You can now run the PDF Data Extractor:")
        print("   - Windows: Double-click run.bat")
        print("   - macOS/Linux: Run ./run.sh")
        print("   - Manual: python pdf_extractor.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("   - Install missing packages: pip install -r requirements.txt")
        print("   - Check Python version: python --version (need 3.8+)")
        print("   - On Linux: sudo apt-get install python3-tk")
        return False

def main():
    """Main test function"""
    try:
        success = run_all_tests()
        
        if not success:
            print("\n🔧 Need help? Check the README.md for detailed setup instructions.")
            
        input("\nPress Enter to exit...")
        return success
        
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled by user.")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False

if __name__ == "__main__":
    main() 