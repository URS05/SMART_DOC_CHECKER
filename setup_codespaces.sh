#!/bin/bash

echo "🚀 Setting up Smart Doc Checker in GitHub Codespaces..."
echo "================================================"

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo "🧠 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Create reports directory
mkdir -p reports

echo "✅ Setup complete!"
echo ""
echo "🌐 Now run: streamlit run app.py --server.port 8501"
echo "📱 The app will be available at the forwarded port URL"
