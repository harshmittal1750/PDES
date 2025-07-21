#!/usr/bin/env python3
"""
Simple Distribution Creator for PDF Data Extractor Suite
Creates a ZIP bundle ready for GitHub release
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_release_bundle():
    """Create a simple release ZIP bundle"""
    version = "2025.07.22"
    date_stamp = datetime.now().strftime("%Y.%m.%d")
    zip_name = f"PDF_Data_Extractor_Suite_v{version}_macOS_{date_stamp}.zip"
    
    print("🚀 Creating PDF Data Extractor Suite Release Bundle")
    print("=" * 60)
    print(f"📦 Package: {zip_name}")
    print(f"🎯 100% Accuracy Insurance Extractor Ready!")
    
    # Essential files to include
    essential_files = {
        # Core insurance extractor (100% accuracy)
        'optimized_insurance_extractor.py': 'Insurance_Extractor_100_Percent/optimized_insurance_extractor.py',
        'launch_rebalanced_optimized.sh': 'Insurance_Extractor_100_Percent/launch_rebalanced_optimized.sh',
        
        # Universal PDF extractor
        'pdf_extractor.py': 'Core/pdf_extractor.py',
        'insurance_extractor_mode.py': 'Core/insurance_extractor_mode.py',
        'run.py': 'Core/run.py',
        
        # Simple extractor
        'simple_insurance_extractor.py': 'Simple_Extractor/simple_insurance_extractor.py',
        
        # Other launchers  
        'launch_idp_extractor.sh': 'Scripts/launch_idp_extractor.sh',
        
        # Requirements and setup
        'requirements.txt': 'Requirements/requirements.txt',
        'test_setup.py': 'Setup/test_setup.py',
        
        # Documentation
        'README.md': 'Documentation/README.md',
        'QUICKSTART.md': 'Documentation/QUICKSTART.md',
        'INSTALL.md': 'Documentation/INSTALL.md',
        'OCR_GUIDE.md': 'Documentation/OCR_GUIDE.md',
        'PROJECT_SUMMARY.md': 'Documentation/PROJECT_SUMMARY.md',
        'COMPLETE_SOLUTION_SUMMARY.md': 'Documentation/COMPLETE_SOLUTION_SUMMARY.md',
        'INSURANCE_MODE_GUIDE.md': 'Documentation/INSURANCE_MODE_GUIDE.md',
        'ENHANCED_ACCURACY_GUIDE.md': 'Documentation/ENHANCED_ACCURACY_GUIDE.md',
        'ACCURACY_IMPROVEMENTS_SUMMARY.md': 'Documentation/ACCURACY_IMPROVEMENTS_SUMMARY.md',
        'FINAL_RELEASE_NOTES.md': 'Documentation/FINAL_RELEASE_NOTES.md',
        'PDF_Data_Extractor_User_Guide.txt': 'Documentation/PDF_Data_Extractor_User_Guide.txt',
        
        # Scripts
        'run.sh': 'Scripts/run.sh',
        'run.bat': 'Scripts/run.bat'
    }
    
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
            files_added = 0
            
            for source_file, zip_path in essential_files.items():
                if os.path.exists(source_file):
                    zipf.write(source_file, f"PDF_Data_Extractor_Suite/{zip_path}")
                    files_added += 1
                    print(f"✅ Added: {source_file} → {zip_path}")
                else:
                    print(f"⚠️ Missing: {source_file}")
            
            print(f"\n📊 Bundle Statistics:")
            print(f"  📁 Files included: {files_added}")
            print(f"  📄 Total files attempted: {len(essential_files)}")
        
        # Get file size
        file_size = os.path.getsize(zip_name) / (1024 * 1024)  # Convert to MB
        
        print(f"\n🎉 SUCCESS!")
        print(f"📦 Created: {zip_name}")
        print(f"💾 Size: {file_size:.1f} MB")
        print(f"🎯 100% Accuracy Insurance Extractor Bundled!")
        
        print(f"\n✅ Ready for GitHub Release!")
        print("📋 Next steps:")
        print("  1. Test the ZIP bundle")
        print("  2. Create GitHub release") 
        print("  3. Upload the ZIP file")
        print("  4. Tag the release as v1.0.0")
        
        return zip_name
        
    except Exception as e:
        print(f"❌ Error creating bundle: {e}")
        return None

if __name__ == "__main__":
    create_release_bundle() 