"""
Demo Script for Smart Doc Checker Agent

This script demonstrates the functionality of the Smart Doc Checker Agent
by analyzing sample documents and generating a report.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from extractor import DocumentExtractor
from nlp import NLPProcessor, ContradictionAnalyzer
from reports import ReportGenerator

def run_demo():
    """Run the demo analysis on sample documents."""
    print("🚀 Smart Doc Checker Agent - Demo")
    print("=" * 50)
    
    # Initialize components
    print("📁 Initializing components...")
    extractor = DocumentExtractor()
    nlp_processor = NLPProcessor()
    analyzer = ContradictionAnalyzer()
    report_generator = ReportGenerator()
    
    # Sample documents directory
    sample_dir = project_root / "sample_docs"
    
    if not sample_dir.exists():
        print("❌ Sample documents directory not found!")
        return
    
    # Get sample files
    sample_files = list(sample_dir.glob("*.txt")) + list(sample_dir.glob("*.html"))
    
    if not sample_files:
        print("❌ No sample files found!")
        return
    
    print(f"📄 Found {len(sample_files)} sample documents")
    
    # Extract text from documents
    print("\n🔍 Extracting text from documents...")
    extracted_texts = {}
    
    for file_path in sample_files:
        try:
            result = extractor.extract_text(file_path)
            extracted_texts[file_path.name] = result
            print(f"✅ Extracted text from {file_path.name}")
        except Exception as e:
            print(f"❌ Error extracting from {file_path.name}: {str(e)}")
    
    if not extracted_texts:
        print("❌ No text extracted from documents!")
        return
    
    # Process documents and extract statements
    print("\n🧠 Processing documents and extracting statements...")
    documents = {}
    
    for filename, data in extracted_texts.items():
        statements = nlp_processor.extract_statements(data['text'], min_length=20)
        documents[filename] = statements
        print(f"📝 Extracted {len(statements)} statements from {filename}")
    
    # Run contradiction analysis
    print("\n🔍 Running contradiction analysis...")
    try:
        results = analyzer.analyze_documents(
            documents,
            threshold=0.7,
            include_cross_document=True
        )
        
        summary = results['summary']
        print(f"📊 Analysis completed!")
        print(f"   - Documents analyzed: {summary['total_documents']}")
        print(f"   - Total statements: {summary['total_statements']}")
        print(f"   - Contradictions found: {summary['total_contradictions']}")
        print(f"   - Overall consistency: {summary['overall_consistency_score'] * 100:.1f}%")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return
    
    # Generate reports
    print("\n📄 Generating reports...")
    try:
        # Create reports directory
        reports_dir = project_root / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        # Generate both markdown and HTML reports
        report_files = report_generator.generate_detailed_report(
            results,
            format="both",
            output_dir=str(reports_dir)
        )
        
        print("✅ Reports generated successfully!")
        for format_name, file_path in report_files.items():
            print(f"   - {format_name.title()} report: {file_path}")
        
    except Exception as e:
        print(f"❌ Error generating reports: {str(e)}")
    
    # Display sample contradictions
    print("\n🔍 Sample Contradictions Found:")
    print("-" * 40)
    
    contradiction_count = 0
    
    # Show intra-document contradictions
    for doc_name, doc_results in results['individual_documents'].items():
        if doc_results['contradictions']:
            print(f"\n📄 {doc_name}:")
            for i, contradiction in enumerate(doc_results['contradictions'][:2], 1):
                contradiction_count += 1
                print(f"   Contradiction {i} (Score: {contradiction['contradiction_score']:.3f}):")
                print(f"   - Statement 1: {contradiction['statement1']['text'][:100]}...")
                print(f"   - Statement 2: {contradiction['statement2']['text'][:100]}...")
                print()
    
    # Show cross-document contradictions
    if results['cross_document_contradictions']:
        print(f"\n🔄 Cross-Document Contradictions:")
        for i, contradiction in enumerate(results['cross_document_contradictions'][:2], 1):
            contradiction_count += 1
            print(f"   Cross-Contradiction {i} (Score: {contradiction['contradiction_score']:.3f}):")
            print(f"   - {contradiction['document1']}: {contradiction['statement1']['text'][:80]}...")
            print(f"   - {contradiction['document2']}: {contradiction['statement2']['text'][:80]}...")
            print()
    
    if contradiction_count == 0:
        print("✅ No contradictions found in the sample documents!")
    
    print("\n🎉 Demo completed successfully!")
    print("📄 Check the 'reports' directory for detailed analysis reports.")
    print("🌐 Run 'streamlit run main.py' to use the web interface.")

if __name__ == "__main__":
    run_demo()
