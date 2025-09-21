"""
Setup script for deployment environments
This script downloads the required spaCy model if not present
"""

import subprocess
import sys
import os

def setup_spacy_model():
    """Download spaCy model if not already present."""
    try:
        import spacy
        # Try to load the model
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model already available")
            return True
        except OSError:
            print("📥 Downloading spaCy model...")
            subprocess.check_call([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm"
            ])
            print("✅ spaCy model downloaded successfully")
            return True
    except Exception as e:
        print(f"❌ Error setting up spaCy model: {e}")
        return False

if __name__ == "__main__":
    setup_spacy_model()
