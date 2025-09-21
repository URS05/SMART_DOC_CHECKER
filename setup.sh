#!/bin/bash

# Create .streamlit directory
mkdir -p ~/.streamlit/

# Create Streamlit config for Heroku
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
" > ~/.streamlit/config.toml

# Download spaCy model
python -m spacy download en_core_web_sm

# Create reports directory
mkdir -p reports
