"""Simple Streamlit UI for Smart Doc Checker Agent

This is a clean, working version without complex CSS that might cause issues.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
import tempfile
import logging

# Import our modules
from extractor import DocumentExtractor
from nlp import NLPProcessor, ContradictionAnalyzer
from reports import ReportGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Smart Doc Checker",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables."""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'extracted_texts' not in st.session_state:
        st.session_state.extracted_texts = {}

def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.title("🚀 Smart Doc Checker")
    st.markdown("**AI-Powered Document Contradiction Detection System**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        model_option = st.selectbox(
            "🧠 NLI Model",
            ["roberta-large-mnli", "facebook-bart-large-mnli"],
            help="Choose the Natural Language Inference model"
        )
        
        threshold = st.slider(
            "🎯 Contradiction Threshold",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Minimum score to consider statements as contradictory"
        )
        
        st.subheader("🔧 Analysis Options")
        include_cross_document = st.checkbox(
            "🔄 Cross-Document Analysis",
            value=True,
            help="Compare statements across different documents"
        )
        
        min_sentence_length = st.number_input(
            "📏 Min Sentence Length",
            min_value=10,
            max_value=100,
            value=20,
            help="Minimum character length for sentences"
        )
        
        # Store settings in session state
        st.session_state['model_option'] = model_option
        st.session_state['threshold'] = threshold
        st.session_state['include_cross_document'] = include_cross_document
        st.session_state['min_sentence_length'] = min_sentence_length
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Upload Documents", 
        "🔍 Run Analysis", 
        "📊 View Results", 
        "📄 Generate Reports"
    ])
    
    with tab1:
        upload_documents_tab()
    
    with tab2:
        analysis_tab()
    
    with tab3:
        results_tab()
    
    with tab4:
        reports_tab()

def upload_documents_tab():
    """Document upload tab."""
    st.header("📁 Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose documents to analyze",
        type=['pdf', 'docx', 'html', 'htm', 'txt'],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX, HTML, TXT"
    )
    
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        
        # Display file information
        st.subheader("📋 Uploaded Files")
        
        file_info = []
        total_size = 0
        for file in uploaded_files:
            file_info.append({
                'Name': file.name,
                'Size (KB)': f"{file.size / 1024:.1f}",
                'Type': file.name.split('.')[-1].upper()
            })
            total_size += file.size
        
        df = pd.DataFrame(file_info)
        st.dataframe(df, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Files", len(uploaded_files))
        with col2:
            st.metric("Total Size", f"{total_size/1024:.1f} KB")
        with col3:
            st.metric("Status", "✅ Ready")
        
        # Extract text button
        if st.button("🔍 Extract Text from Documents", type="primary"):
            extract_texts()

def extract_texts():
    """Extract text from uploaded files."""
    if not st.session_state.uploaded_files:
        st.error("No files uploaded!")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    extractor = DocumentExtractor()
    extracted_texts = {}
    
    for i, uploaded_file in enumerate(st.session_state.uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name
        
        try:
            # Extract text
            result = extractor.extract_text(tmp_path)
            extracted_texts[uploaded_file.name] = result
            
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
        
        progress_bar.progress((i + 1) / len(st.session_state.uploaded_files))
    
    st.session_state.extracted_texts = extracted_texts
    status_text.success(f"✅ Successfully extracted text from {len(extracted_texts)} documents!")
    
    # Display extraction results
    if extracted_texts:
        st.subheader("📝 Extraction Results")
        
        total_chars = sum(len(data['text']) for data in extracted_texts.values())
        total_sentences = sum(len(data['sentences']) for data in extracted_texts.values())
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Characters", f"{total_chars:,}")
        with col2:
            st.metric("Total Sentences", total_sentences)
        
        # Show preview for each document
        for filename, data in extracted_texts.items():
            with st.expander(f"📄 {filename} - {len(data['sentences'])} sentences"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Characters:** {len(data['text']):,}")
                    st.write(f"**Sentences:** {len(data['sentences'])}")
                    st.write(f"**File Size:** {data['metadata']['file_size']:,} bytes")
                
                with col2:
                    st.write("**Preview:**")
                    preview = data['text'][:200] + "..." if len(data['text']) > 200 else data['text']
                    st.text(preview)

def analysis_tab():
    """Analysis tab."""
    st.header("🔍 Run Analysis")
    
    if not st.session_state.extracted_texts:
        st.info("📁 Please upload and extract text from documents first.")
        st.markdown("Go to the **Upload Documents** tab to get started.")
        return
    
    st.success(f"✅ Ready to analyze {len(st.session_state.extracted_texts)} documents")
    
    # Show current settings
    st.subheader("⚙️ Current Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Model:** {st.session_state.get('model_option', 'roberta-large-mnli')}")
        st.write(f"**Threshold:** {st.session_state.get('threshold', 0.7)}")
    
    with col2:
        st.write(f"**Cross-document:** {st.session_state.get('include_cross_document', True)}")
        st.write(f"**Min length:** {st.session_state.get('min_sentence_length', 20)}")
    
    # Run analysis button
    if st.button("🚀 Run Contradiction Analysis", type="primary"):
        run_analysis()

def run_analysis():
    """Run contradiction analysis."""
    if not st.session_state.extracted_texts:
        st.error("No extracted texts available!")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize processors
        status_text.text("🧠 Loading AI models...")
        nlp_processor = NLPProcessor()
        analyzer = ContradictionAnalyzer()
        progress_bar.progress(0.2)
        
        status_text.text("📄 Processing documents...")
        
        # Extract statements from each document
        documents = {}
        for filename, data in st.session_state.extracted_texts.items():
            statements = nlp_processor.extract_statements(
                data['text'], 
                min_length=st.session_state.get('min_sentence_length', 20)
            )
            documents[filename] = statements
        
        progress_bar.progress(0.6)
        status_text.text("🔍 Analyzing contradictions...")
        
        # Run analysis
        results = analyzer.analyze_documents(
            documents,
            threshold=st.session_state.get('threshold', 0.7),
            include_cross_document=st.session_state.get('include_cross_document', True)
        )
        
        st.session_state.analysis_results = results
        progress_bar.progress(1.0)
        status_text.success("✅ Analysis completed successfully!")
        
        # Show quick summary
        summary = results['summary']
        st.balloons()  # Celebration animation
        
        st.subheader("📊 Quick Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Documents", summary['total_documents'])
        with col2:
            st.metric("Statements", summary['total_statements'])
        with col3:
            st.metric("Contradictions", summary['total_contradictions'])
        with col4:
            consistency = summary['overall_consistency_score'] * 100
            st.metric("Consistency", f"{consistency:.1f}%")
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        logger.error(f"Analysis error: {str(e)}")

def results_tab():
    """Results display tab."""
    st.header("📊 Analysis Results")
    
    if not st.session_state.analysis_results:
        st.info("🔍 Please run the analysis first to see results.")
        st.markdown("Go to the **Run Analysis** tab to start.")
        return
    
    results = st.session_state.analysis_results
    summary = results['summary']
    
    # Overall summary
    st.subheader("📈 Overall Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Documents Analyzed", summary['total_documents'])
    with col2:
        st.metric("Total Statements", summary['total_statements'])
    with col3:
        st.metric("Contradictions Found", summary['total_contradictions'])
    with col4:
        consistency_score = summary['overall_consistency_score'] * 100
        st.metric("Consistency Score", f"{consistency_score:.1f}%")
    
    # Status indicator
    if summary['total_contradictions'] == 0:
        st.success("✅ **Excellent!** No contradictions found. All documents appear to be consistent.")
    else:
        st.warning(f"⚠️ **Found {summary['total_contradictions']} contradictions** that need attention.")
    
    # Individual document results
    st.subheader("📄 Individual Document Results")
    
    for doc_name, doc_results in results['individual_documents'].items():
        with st.expander(f"📄 {doc_name} ({doc_results['contradictions_found']} contradictions)"):
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Statements:** {doc_results['total_statements']}")
                st.write(f"**Consistency Score:** {doc_results['consistency_score'] * 100:.1f}%")
            
            with col2:
                st.write(f"**Pairs Checked:** {doc_results['total_pairs_checked']}")
                st.write(f"**Contradiction Rate:** {doc_results['contradiction_rate'] * 100:.1f}%")
            
            # Show contradictions
            if doc_results['contradictions']:
                st.write("**🔍 Contradictions Found:**")
                for i, contradiction in enumerate(doc_results['contradictions'], 1):
                    st.write(f"**Contradiction {i}** (Score: {contradiction['contradiction_score']:.3f})")
                    st.write(f"📝 **Statement 1:** {contradiction['statement1']['text']}")
                    st.write(f"📝 **Statement 2:** {contradiction['statement2']['text']}")
                    st.write(f"🎯 **Confidence:** {contradiction['confidence']:.3f}")
                    st.divider()
    
    # Cross-document contradictions
    if results['cross_document_contradictions']:
        st.subheader("🔄 Cross-Document Contradictions")
        
        for i, contradiction in enumerate(results['cross_document_contradictions'], 1):
            with st.expander(f"Cross-Contradiction {i} (Score: {contradiction['contradiction_score']:.3f})"):
                st.write(f"**📄 Documents:** {contradiction['document1']} ↔ {contradiction['document2']}")
                st.write(f"**🎯 Confidence:** {contradiction['confidence']:.3f}")
                st.write(f"**{contradiction['document1']}:** {contradiction['statement1']['text']}")
                st.write(f"**{contradiction['document2']}:** {contradiction['statement2']['text']}")

def reports_tab():
    """Reports generation tab."""
    st.header("📄 Generate Reports")
    
    if not st.session_state.analysis_results:
        st.info("🔍 Please run the analysis first to generate reports.")
        st.markdown("Go to the **Run Analysis** tab to start.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Report Options")
        report_format = st.selectbox(
            "Report Format",
            ["markdown", "html", "both"],
            help="Choose the format for the generated report"
        )
        
        include_recommendations = st.checkbox(
            "Include Recommendations",
            value=True,
            help="Include actionable recommendations in the report"
        )
    
    with col2:
        st.subheader("🚀 Generate Report")
        if st.button("📄 Generate Report", type="primary"):
            generate_report(report_format)
    
    # Display existing reports
    reports_dir = Path("reports")
    if reports_dir.exists():
        report_files = list(reports_dir.glob("*.md")) + list(reports_dir.glob("*.html"))
        
        if report_files:
            st.subheader("📁 Available Reports")
            
            # Show most recent 5 reports
            recent_reports = sorted(report_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
            
            for report_file in recent_reports:
                with st.expander(f"📄 {report_file.name}"):
                    file_stats = report_file.stat()
                    st.write(f"**Created:** {pd.to_datetime(file_stats.st_mtime, unit='s')}")
                    st.write(f"**Size:** {file_stats.st_size} bytes")
                    
                    # Download button
                    with open(report_file, 'rb') as f:
                        file_data = f.read()
                    
                    st.download_button(
                        label=f"📥 Download {report_file.name}",
                        data=file_data,
                        file_name=report_file.name,
                        mime="text/markdown" if report_file.suffix == '.md' else "text/html"
                    )

def generate_report(format_type: str):
    """Generate report in specified format."""
    try:
        generator = ReportGenerator()
        results = st.session_state.analysis_results
        
        with st.spinner("📄 Generating report..."):
            # Generate reports
            report_files = generator.generate_detailed_report(
                results,
                format=format_type,
                output_dir="reports"
            )
        
        st.success("✅ Report generated successfully!")
        
        # Show download links
        for format_name, file_path in report_files.items():
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            st.download_button(
                label=f"📥 Download {format_name.title()} Report",
                data=file_data,
                file_name=Path(file_path).name,
                mime="text/markdown" if format_name == "markdown" else "text/html"
            )
    
    except Exception as e:
        st.error(f"❌ Error generating report: {str(e)}")
        logger.error(f"Report generation error: {str(e)}")

if __name__ == "__main__":
    main()
