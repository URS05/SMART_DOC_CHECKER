"""
Configuration file for Smart Doc Checker Agent
"""

# Default settings
DEFAULT_SETTINGS = {
    # NLI Model settings
    "nli_model": "roberta-large-mnli",
    "contradiction_threshold": 0.7,
    
    # Text processing settings
    "min_sentence_length": 20,
    "max_sentence_length": 500,
    
    # Analysis settings
    "include_cross_document": True,
    "batch_size": 32,
    
    # Report settings
    "default_report_format": "both",  # "markdown", "html", or "both"
    "include_recommendations": True,
    
    # UI settings
    "streamlit_port": 8501,
    "streamlit_host": "localhost",
    
    # File settings
    "max_file_size_mb": 50,
    "supported_formats": [".pdf", ".docx", ".html", ".htm", ".txt"],
    
    # Logging settings
    "log_level": "INFO",
    "log_file": "smart_doc_checker.log"
}

# Model configurations
MODEL_CONFIGS = {
    "roberta-large-mnli": {
        "description": "RoBERTa Large MNLI - Best accuracy, slower processing",
        "max_length": 512,
        "batch_size": 8
    },
    "facebook-bart-large-mnli": {
        "description": "BART Large MNLI - Good balance of speed and accuracy",
        "max_length": 512,
        "batch_size": 16
    },
    "microsoft/deberta-large-mnli": {
        "description": "DeBERTa Large MNLI - Alternative high-accuracy model",
        "max_length": 512,
        "batch_size": 8
    }
}

# Severity levels for contradictions
SEVERITY_LEVELS = {
    "Very High": {"min_score": 0.8, "color": "#ff4444", "description": "Strong evidence of contradiction"},
    "High": {"min_score": 0.6, "color": "#ff8844", "description": "Good evidence of contradiction"},
    "Medium": {"min_score": 0.4, "color": "#ffaa44", "description": "Moderate evidence of contradiction"},
    "Low": {"min_score": 0.2, "color": "#ffcc44", "description": "Weak evidence of contradiction"},
    "Very Low": {"min_score": 0.0, "color": "#ffee44", "description": "Minimal evidence of contradiction"}
}

# Confidence levels
CONFIDENCE_LEVELS = {
    "Very High": {"min_score": 0.8, "description": "Very confident prediction"},
    "High": {"min_score": 0.6, "description": "Confident prediction"},
    "Medium": {"min_score": 0.4, "description": "Moderately confident prediction"},
    "Low": {"min_score": 0.2, "description": "Low confidence prediction"},
    "Very Low": {"min_score": 0.0, "description": "Very low confidence prediction"}
}
