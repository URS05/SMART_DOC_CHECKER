"""Streamlit UI Module

This module provides a web interface for the Smart Doc Checker Agent
using Streamlit.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
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
    layout="wide"
)

# Modern CSS with dark theme and beautiful gradients
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Global Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 75%, #533483 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
        color: #ffffff;
        position: relative;
    }
    
    /* Background Pattern Overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 25% 25%, #ff6b6b15 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, #4ecdc415 0%, transparent 50%),
            radial-gradient(circle at 50% 10%, #45b7d115 0%, transparent 40%),
            radial-gradient(circle at 10% 80%, #96ceb415 0%, transparent 40%),
            linear-gradient(45deg, transparent 49%, rgba(255,255,255,0.03) 50%, transparent 51%);
        background-size: 300px 300px, 400px 400px, 250px 250px, 350px 350px, 20px 20px;
        z-index: -1;
    }
    
    /* Main container with dark glassmorphism */
    .main-container {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Hero Section with Dark Gradient */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, 
            #2D1B69 0%, #11998e 25%, #38ef7d 50%, #ee5a52 75%, #f093fb 100%);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        border-radius: 25px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 25px;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        animation: slideInDown 1s ease-out;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
        animation: slideInUp 1s ease-out 0.2s both;
    }
    
    /* Floating action button */
    .fab {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1000;
        animation: pulse 2s infinite;
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 35px rgba(0,0,0,0.4);
    }
    
    /* Dark Card Styles */
    .glass-card {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
        color: white;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .gradient-card {
        background: linear-gradient(135deg, #2D1B69, #11998e);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        margin: 1rem 0;
        animation: fadeInLeft 0.8s ease-out;
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .gradient-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
        pointer-events: none;
    }
    
    /* Dark Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #2D1B69, #ee5a52);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        animation: slideInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .metric-card:nth-child(2) {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        animation-delay: 0.2s;
    }
    
    .metric-card:nth-child(3) {
        background: linear-gradient(135deg, #ee5a52, #f093fb);
        animation-delay: 0.4s;
    }
    
    .metric-card:nth-child(4) {
        background: linear-gradient(135deg, #f093fb, #2D1B69);
        animation-delay: 0.6s;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .metric-label {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Contradiction Cards */
    .contradiction-card {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        animation: slideInRight 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .success-card {
        background: linear-gradient(135deg, #51cf66, #40c057);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Upload Zone */
    .upload-zone {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border: 2px dashed rgba(255,255,255,0.3);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeIn 1s ease-out;
    }
    
    .upload-zone:hover {
        border-color: rgba(255,255,255,0.6);
        background: rgba(255,255,255,0.15);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(15px);
    }
    
    /* Animations */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    @keyframes patternMove {
        0% { background-position: 0% 0%, 0% 0%, 0% 0%, 0% 0%, 0% 0%; }
        100% { background-position: 100% 100%, -100% -100%, 50% 50%, -50% -50%, 25% 25%; }
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 25px;
        padding: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 1rem 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        min-width: 200px;
        text-align: center;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.1rem;
        }
        .main-container {
            margin: 0.5rem;
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

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
    
    # Stunning Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🚀 Smart Doc Checker</h1>
        <p class="hero-subtitle">
            AI-Powered Document Contradiction Detection System<br>
            Analyze multiple documents with state-of-the-art Natural Language Processing
        </p>
        <div style="margin-top: 2rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0.5rem;">
                📄 Multi-Format Support
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0.5rem;">
                🤖 AI-Powered Analysis
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0.5rem;">
                📊 Beautiful Reports
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with modern styling
    with st.sidebar:
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: white; text-align: center; margin-bottom: 2rem;">⚙️ Configuration</h2>
        """, unsafe_allow_html=True)
        
        # Store settings in session state
        st.session_state['model_option'] = st.selectbox(
            "🧠 NLI Model",
            ["roberta-large-mnli", "facebook-bart-large-mnli"],
            help="Choose the Natural Language Inference model for contradiction detection",
            key="model_select"
        )
        
        st.session_state['threshold'] = st.slider(
            "🎯 Contradiction Threshold",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Minimum score to consider statements as contradictory",
            key="threshold_slider"
        )
        
        st.markdown("### 🔧 Analysis Options")
        st.session_state['include_cross_document'] = st.checkbox(
            "🔄 Cross-Document Analysis",
            value=True,
            help="Compare statements across different documents",
            key="cross_doc_check"
        )
        
        st.session_state['min_sentence_length'] = st.number_input(
            "📏 Min Sentence Length",
            min_value=10,
            max_value=100,
            value=20,
            help="Minimum character length for sentences to be analyzed",
            key="min_length_input"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick stats if analysis is available
        if st.session_state.analysis_results:
            st.markdown("""
            <div class="gradient-card" style="margin-top: 2rem;">
                <h3 style="text-align: center;">📊 Quick Stats</h3>
            """, unsafe_allow_html=True)
            
            summary = st.session_state.analysis_results['summary']
            st.write(f"📄 **Documents:** {summary['total_documents']}")
            st.write(f"📝 **Statements:** {summary['total_statements']}")
            st.write(f"⚠️ **Contradictions:** {summary['total_contradictions']}")
            st.write(f"✅ **Consistency:** {summary['overall_consistency_score']*100:.1f}%")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Modern navigation with beautiful tabs
    st.markdown("""
    <div style="margin: 2rem 0; text-align: center;">
        <h2 style="color: white; font-weight: 300; margin-bottom: 1rem;">Choose Your Journey</h2>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Upload & Process", 
        "🔍 AI Analysis", 
        "📊 Visual Insights", 
        "📄 Generate Reports"
    ])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        upload_documents_tab()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        analysis_results_tab()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        visualizations_tab()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        reports_tab()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Floating action button for quick demo
    st.markdown("""
    <div class="fab" onclick="window.scrollTo(0,0);" title="Back to Top">
        ⬆️
    </div>
    """, unsafe_allow_html=True)

def upload_documents_tab():
    """Document upload tab."""
    # Beautiful upload section
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 1rem;">📁 Upload & Process Documents</h1>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.2rem;">
            Upload your documents and let AI extract meaningful insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload with modern styling
    st.markdown("""
    <div class="upload-zone">
        <h3 style="color: white; margin-bottom: 1rem;">📤 Drop Your Documents Here</h3>
        <p style="color: rgba(255,255,255,0.7); margin-bottom: 2rem;">
            Supported formats: PDF, DOCX, HTML, TXT
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose documents to analyze",
        type=['pdf', 'docx', 'html', 'htm', 'txt'],
        accept_multiple_files=True,
        help="Drag and drop or click to browse files",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        
        # Beautiful file display with metrics
        st.markdown("""
        <div style="margin: 2rem 0;">
            <h2 style="color: white; text-align: center; margin-bottom: 2rem;">📋 Uploaded Files Overview</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # File metrics in beautiful cards
        total_size = sum(file.size for file in uploaded_files)
        file_types = set(file.name.split('.')[-1].upper() for file in uploaded_files)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(uploaded_files)}</div>
                <div class="metric-label">Files Uploaded</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_size/1024:.1f}</div>
                <div class="metric-label">KB Total Size</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(file_types)}</div>
                <div class="metric-label">File Types</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">🚀</div>
                <div class="metric-label">Ready to Process</div>
            </div>
            """, unsafe_allow_html=True)
        
        # File details table
        st.markdown("### 📄 File Details")
        file_info = []
        for file in uploaded_files:
            file_info.append({
                '📄 Name': file.name,
                '📏 Size': f"{file.size / 1024:.1f} KB",
                '🏷️ Type': file.name.split('.')[-1].upper(),
                '✅ Status': 'Ready'
            })
        
        df = pd.DataFrame(file_info)
        st.dataframe(df, use_container_width=True)
        
        # Extract text button with animation
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Extract Text & Analyze Documents", type="primary"):
                extract_texts()
    
    # Display extracted texts with beautiful cards
    if st.session_state.extracted_texts:
        st.markdown("""
        <div style="margin: 3rem 0 2rem 0;">
            <h2 style="color: white; text-align: center;">📝 Extracted Content Preview</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats about extracted content
        total_text_length = sum(len(data['text']) for data in st.session_state.extracted_texts.values())
        total_sentences = sum(len(data['sentences']) for data in st.session_state.extracted_texts.values())
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_text_length:,}</div>
                <div class="metric-label">Characters Extracted</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_sentences}</div>
                <div class="metric-label">Sentences Found</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">✅</div>
                <div class="metric-label">Ready for AI Analysis</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Document content preview
        for filename, data in st.session_state.extracted_texts.items():
            with st.expander(f"📄 {filename} - {len(data['sentences'])} sentences"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📊 Statistics:**")
                    st.write(f"• **Characters:** {len(data['text']):,}")
                    st.write(f"• **Sentences:** {len(data['sentences'])}")
                    st.write(f"• **File Size:** {data['metadata']['file_size']:,} bytes")
                
                with col2:
                    st.markdown("**📝 Content Preview:**")
                    preview_text = data['text'][:300] + "..." if len(data['text']) > 300 else data['text']
                    st.markdown(f"*{preview_text}*")

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
    status_text.text("✅ Text extraction completed!")
    st.success(f"Successfully extracted text from {len(extracted_texts)} documents!")

def analysis_results_tab():
    """Analysis results tab."""
    st.header("🔍 Analysis Results")
    
    if not st.session_state.extracted_texts:
        st.info("Please upload and extract text from documents first.")
        return
    
    # Run analysis button
    if st.button("🚀 Run Contradiction Analysis", type="primary"):
        run_analysis()
    
    # Display results
    if st.session_state.analysis_results:
        display_analysis_results()

def run_analysis():
    """Run contradiction analysis."""
    if not st.session_state.extracted_texts:
        st.error("No extracted texts available!")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize processors
        nlp_processor = NLPProcessor()
        analyzer = ContradictionAnalyzer()
        
        status_text.text("Processing documents...")
        progress_bar.progress(0.2)
        
        # Extract statements from each document
        documents = {}
        for filename, data in st.session_state.extracted_texts.items():
            statements = nlp_processor.extract_statements(
                data['text'], 
                min_length=st.session_state.get('min_sentence_length', 20)
            )
            documents[filename] = statements
        
        status_text.text("Analyzing contradictions...")
        progress_bar.progress(0.6)
        
        # Run analysis
        results = analyzer.analyze_documents(
            documents,
            threshold=st.session_state.get('threshold', 0.7),
            include_cross_document=st.session_state.get('include_cross_document', True)
        )
        
        st.session_state.analysis_results = results
        progress_bar.progress(1.0)
        status_text.text("✅ Analysis completed!")
        
        st.success("Contradiction analysis completed successfully!")
        
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        logger.error(f"Analysis error: {str(e)}")

def display_analysis_results():
    """Display analysis results."""
    results = st.session_state.analysis_results
    summary = results['summary']
    
    # Summary metrics
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
    
    # Overall status
    if summary['total_contradictions'] == 0:
        st.markdown('<div class="success-card">✅ <strong>No contradictions found!</strong> All documents appear to be consistent.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="contradiction-card">⚠️ <strong>{summary["total_contradictions"]} contradictions found</strong> - Review the details below.</div>', unsafe_allow_html=True)
    
    # Individual document results
    st.subheader("📄 Document Analysis")
    
    for doc_name, doc_results in results['individual_documents'].items():
        with st.expander(f"📄 {doc_name} - {doc_results['contradictions_found']} contradictions"):
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Statements:** {doc_results['total_statements']}")
                st.write(f"**Consistency Score:** {doc_results['consistency_score'] * 100:.1f}%")
            
            with col2:
                st.write(f"**Pairs Checked:** {doc_results['total_pairs_checked']}")
                st.write(f"**Contradiction Rate:** {doc_results['contradiction_rate'] * 100:.1f}%")
            
            # Show contradictions
            if doc_results['contradictions']:
                st.write("**Contradictions Found:**")
                for i, contradiction in enumerate(doc_results['contradictions'], 1):
                    st.write(f"**Contradiction {i}** (Score: {contradiction['contradiction_score']:.3f})")
                    st.write(f"- Statement 1: {contradiction['statement1']['text']}")
                    st.write(f"- Statement 2: {contradiction['statement2']['text']}")
                    st.write(f"- Confidence: {contradiction['confidence']:.3f}")
                    st.divider()
    
    # Cross-document contradictions
    if results['cross_document_contradictions']:
        st.subheader("🔄 Cross-Document Contradictions")
        
        for i, contradiction in enumerate(results['cross_document_contradictions'], 1):
            with st.expander(f"Cross-Document Contradiction {i} (Score: {contradiction['contradiction_score']:.3f})"):
                st.write(f"**Documents:** {contradiction['document1']} ↔ {contradiction['document2']}")
                st.write(f"**Confidence:** {contradiction['confidence']:.3f}")
                st.write(f"**{contradiction['document1']}:** {contradiction['statement1']['text']}")
                st.write(f"**{contradiction['document2']}:** {contradiction['statement2']['text']}")

def visualizations_tab():
    """Visualizations tab."""
    st.header("📊 Visualizations")
    
    if not st.session_state.analysis_results:
        st.info("Please run the analysis first to see visualizations.")
        return
    
    results = st.session_state.analysis_results
    summary = results['summary']
    
    # Consistency score gauge
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Overall Consistency Score")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = summary['overall_consistency_score'] * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Consistency (%)"},
            delta = {'reference': 100},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Contradiction Breakdown")
        contradiction_data = {
            'Type': ['Intra-Document', 'Cross-Document'],
            'Count': [
                summary['intra_document_contradictions'],
                summary['cross_document_contradictions']
            ]
        }
        df = pd.DataFrame(contradiction_data)
        fig = px.pie(df, values='Count', names='Type', title="Contradiction Types")
        st.plotly_chart(fig, use_container_width=True)
    
    # Document consistency comparison
    st.subheader("Document Consistency Comparison")
    doc_data = []
    for doc_name, doc_results in results['individual_documents'].items():
        doc_data.append({
            'Document': doc_name,
            'Consistency Score': doc_results['consistency_score'] * 100,
            'Contradictions': doc_results['contradictions_found'],
            'Statements': doc_results['total_statements']
        })
    
    if doc_data:
        df = pd.DataFrame(doc_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(df, x='Document', y='Consistency Score', 
                        title="Consistency Score by Document")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(df, x='Document', y='Contradictions', 
                        title="Contradictions by Document")
            st.plotly_chart(fig, use_container_width=True)

def reports_tab():
    """Reports tab."""
    st.header("📄 Generate Reports")
    
    if not st.session_state.analysis_results:
        st.info("Please run the analysis first to generate reports.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Report Options")
        report_format = st.selectbox(
            "Report Format",
            ["Markdown", "HTML", "Both"],
            help="Choose the format for the generated report"
        )
        
        include_recommendations = st.checkbox(
            "Include Recommendations",
            value=True,
            help="Include actionable recommendations in the report"
        )
    
    with col2:
        st.subheader("Generate Report")
        if st.button("📄 Generate Report", type="primary"):
            generate_report(report_format.lower())
    
    # Display existing reports
    reports_dir = Path("reports")
    if reports_dir.exists():
        report_files = list(reports_dir.glob("*.md")) + list(reports_dir.glob("*.html"))
        
        if report_files:
            st.subheader("📁 Available Reports")
            for report_file in sorted(report_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                with st.expander(f"📄 {report_file.name}"):
                    st.write(f"**Created:** {pd.to_datetime(report_file.stat().st_mtime, unit='s')}")
                    st.write(f"**Size:** {report_file.stat().st_size} bytes")
                    
                    if report_file.suffix == '.html':
                        with open(report_file, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        st.components.v1.html(html_content, height=400, scrolling=True)
                    else:
                        with open(report_file, 'r', encoding='utf-8') as f:
                            md_content = f.read()
                        st.markdown(md_content)

def generate_report(format_type: str):
    """Generate report in specified format."""
    try:
        generator = ReportGenerator()
        results = st.session_state.analysis_results
        
        # Generate reports
        report_files = generator.generate_detailed_report(
            results,
            format=format_type,
            output_dir="reports"
        )
        
        st.success("Report generated successfully!")
        
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
        st.error(f"Error generating report: {str(e)}")
        logger.error(f"Report generation error: {str(e)}")

if __name__ == "__main__":
    main()
