"""
Demo Streamlit UI Module

This is a standalone demo version showcasing the beautiful dark-themed interface.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
import time

# Page configuration
st.set_page_config(
    page_title="Smart Doc Checker Agent - Demo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    
    /* Dark Metric Cards */
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
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
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
        
        model_option = st.selectbox(
            "🧠 NLI Model",
            ["roberta-large-mnli", "facebook-bart-large-mnli"],
            help="Choose the Natural Language Inference model for contradiction detection"
        )
        
        threshold = st.slider(
            "🎯 Contradiction Threshold",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Minimum score to consider statements as contradictory"
        )
        
        st.markdown("### 🔧 Analysis Options")
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
            help="Minimum character length for sentences to be analyzed"
        )
        
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
        upload_demo_tab()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        analysis_demo_tab()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        visualizations_demo_tab()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        reports_demo_tab()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Floating action button
    st.markdown("""
    <div class="fab" onclick="window.scrollTo(0,0);" title="Back to Top">
        ⬆️
    </div>
    """, unsafe_allow_html=True)

def upload_demo_tab():
    """Demo upload tab."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 1rem;">📁 Upload & Process Documents</h1>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.2rem;">
            Upload your documents and let AI extract meaningful insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload zone
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
        # Beautiful file display with metrics
        st.markdown("""
        <div style="margin: 2rem 0;">
            <h2 style="color: white; text-align: center; margin-bottom: 2rem;">📋 Uploaded Files Overview</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # File metrics
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
        
        # Extract button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Extract Text & Analyze Documents", type="primary"):
                with st.spinner("Processing files..."):
                    time.sleep(2)
                    st.success("✅ Text extraction completed!")

def analysis_demo_tab():
    """Demo analysis tab."""
    st.header("🔍 Analysis Results")
    
    # Demo metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Documents Analyzed", "3", "2")
    
    with col2:
        st.metric("Total Statements", "247", "45")
    
    with col3:
        st.metric("Contradictions Found", "4", "-1")
    
    with col4:
        st.metric("Consistency Score", "96.8%", "2.1%")
    
    if st.button("🚀 Run Contradiction Analysis", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text('Processing documents...')
            elif i < 70:
                status_text.text('Running AI analysis...')
            else:
                status_text.text('Generating results...')
            time.sleep(0.02)
        
        st.success("✅ Analysis completed successfully!")

def visualizations_demo_tab():
    """Demo visualizations tab."""
    st.header("📊 Visualizations")
    
    # Sample data for demo
    consistency_score = 96.8
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Overall Consistency Score")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = consistency_score,
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
            'Count': [3, 1]
        }
        df = pd.DataFrame(contradiction_data)
        fig = px.pie(df, values='Count', names='Type', title="Contradiction Types")
        st.plotly_chart(fig, use_container_width=True)

def reports_demo_tab():
    """Demo reports tab."""
    st.header("📄 Generate Reports")
    
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
            with st.spinner("Generating report..."):
                time.sleep(2)
                st.success("✅ Report generated successfully!")
                st.download_button(
                    label="📥 Download Report",
                    data="# Smart Doc Checker Report\n\nThis is a demo report showing the beautiful interface!",
                    file_name="demo_report.md",
                    mime="text/markdown"
                )

if __name__ == "__main__":
    main()
