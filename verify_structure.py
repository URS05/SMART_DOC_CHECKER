"""
Project Structure Verification Script

This script verifies that the Smart Doc Checker Agent project structure is correct
and all necessary files are in place.
"""

import os
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and report status."""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ Missing {description}: {file_path}")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and report status."""
    if Path(dir_path).is_dir():
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ Missing {description}: {dir_path}")
        return False

def main():
    """Main verification function."""
    print("🔍 Smart Doc Checker Agent - Project Structure Verification")
    print("=" * 60)
    
    # Project root
    project_root = Path(__file__).parent
    
    # Check main files
    print("\n📄 Main Files:")
    main_files = [
        ("main.py", "Main application entry point"),
        ("demo.py", "Demo script"),
        ("setup.py", "Setup script"),
        ("requirements.txt", "Python dependencies"),
        ("README.md", "Project documentation"),
        ("config.py", "Configuration file"),
        (".gitignore", "Git ignore file")
    ]
    
    main_files_ok = True
    for file_path, description in main_files:
        if not check_file_exists(file_path, description):
            main_files_ok = False
    
    # Check directories
    print("\n📁 Directories:")
    directories = [
        ("extractor", "Document extraction module"),
        ("nlp", "Natural language processing module"),
        ("ui", "Streamlit user interface module"),
        ("reports", "Report generation module"),
        ("templates", "Jinja2 templates directory"),
        ("sample_docs", "Sample documents directory")
    ]
    
    directories_ok = True
    for dir_path, description in directories:
        if not check_directory_exists(dir_path, description):
            directories_ok = False
    
    # Check module files
    print("\n🔧 Module Files:")
    module_files = [
        ("extractor/__init__.py", "Extractor module init"),
        ("extractor/document_extractor.py", "Document extractor implementation"),
        ("nlp/__init__.py", "NLP module init"),
        ("nlp/processor.py", "NLP processor implementation"),
        ("nlp/contradiction_detector.py", "Contradiction detector implementation"),
        ("ui/__init__.py", "UI module init"),
        ("ui/app.py", "Streamlit application"),
        ("reports/__init__.py", "Reports module init"),
        ("reports/generator.py", "Report generator implementation")
    ]
    
    module_files_ok = True
    for file_path, description in module_files:
        if not check_file_exists(file_path, description):
            module_files_ok = False
    
    # Check sample files
    print("\n📄 Sample Files:")
    sample_files = [
        ("sample_docs/company_report_q3.txt", "Q3 company report sample"),
        ("sample_docs/company_report_q4.txt", "Q4 company report sample"),
        ("sample_docs/product_launch.html", "Product launch HTML sample"),
        ("sample_docs/product_delay_notice.txt", "Product delay notice sample")
    ]
    
    sample_files_ok = True
    for file_path, description in sample_files:
        if not check_file_exists(file_path, description):
            sample_files_ok = False
    
    # Summary
    print("\n📊 Summary:")
    print("-" * 30)
    
    all_ok = main_files_ok and directories_ok and module_files_ok and sample_files_ok
    
    if all_ok:
        print("🎉 All files and directories are in place!")
        print("\n📋 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Download spaCy model: python -m spacy download en_core_web_sm")
        print("   3. Run demo: python demo.py")
        print("   4. Start web interface: streamlit run main.py")
    else:
        print("❌ Some files or directories are missing!")
        print("   Please check the errors above and ensure all files are created.")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
