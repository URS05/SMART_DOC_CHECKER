# 🚀 Quick Start Guide

## How to Run Smart Doc Checker Agent

### Option 1: Python Launcher (Recommended)
```bash
python run_app.py
```

### Option 2: Direct Streamlit Command
```bash
python -m streamlit run ui/app.py
```

### Option 3: Using Main Script
```bash
python main.py
```

### Option 4: Run Demo First (Test the system)
```bash
python demo.py
```

## What Each Command Does

### 🎯 `python run_app.py`
- **Best for beginners**
- Launches the full web interface
- Opens automatically in your browser
- Shows clear startup messages

### 🌐 `python -m streamlit run ui/app.py`
- Direct Streamlit command
- Most reliable method
- Manual browser navigation to http://localhost:8501

### 📄 `python main.py`
- Uses the main entry point
- Same as Option 2 but through main.py

### 🎮 `python demo.py`
- **Start here to test the system**
- Analyzes sample documents
- Shows system capabilities
- Generates sample reports
- No browser required

## Installation Steps (If needed)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download AI Model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Verify Installation**
   ```bash
   python verify_structure.py
   ```

## Troubleshooting

### If Streamlit doesn't start:
- Make sure you have all dependencies installed
- Try running `python demo.py` first
- Check if port 8501 is available
- Try a different port: `streamlit run ui/app.py --server.port=8502`

### If you see import errors:
- Run `pip install -r requirements.txt`
- Make sure you're in the project directory

### If the browser doesn't open:
- Manually navigate to http://localhost:8501
- Check your firewall settings

## Features Available

✅ **Upload multiple documents** (PDF, DOCX, HTML, TXT)  
✅ **AI-powered contradiction detection**  
✅ **Beautiful web interface**  
✅ **Detailed reports generation**  
✅ **Cross-document analysis**  
✅ **Interactive visualizations**  

## Need Help?

1. Run `python demo.py` to see the system in action
2. Check `reports/` directory for sample outputs
3. Open an issue on GitHub if problems persist

---
**Made with ❤️ for document analysis**
