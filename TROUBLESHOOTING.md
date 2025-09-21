# 🛠️ Troubleshooting Guide - Smart Doc Checker Agent

## 🚨 Common Issues and Solutions

### 1. "Runtime instance already exists!" Error

**Problem**: You see this error when trying to start the web interface.

**Solution**:
```cmd
# Option 1: Use the stop script (PowerShell)
.\stop_streamlit.bat

# Option 2: Kill processes manually
taskkill /F /IM python.exe
```

**Prevention**: The updated batch files now automatically check for and stop existing processes.

### 2. "Python not found" Error

**Problem**: Python is not installed or not in PATH.

**Solution**:
1. Download Python from [python.org](https://python.org)
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Restart your command prompt/terminal
4. Verify: `python --version`

### 3. "Dependencies not found" Error

**Problem**: Required Python packages are not installed.

**Solution**:
```cmd
# Run setup
setup.bat

# Or manually
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. "Port already in use" Error

**Problem**: Port 8501 is already being used.

**Solution**:
```cmd
# Stop all Streamlit processes
stop_streamlit.bat

# Or find and kill the process using port 8501
netstat -aon | find ":8501"
taskkill /F /PID <PID_NUMBER>
```

### 5. "Model not found" Error

**Problem**: spaCy English model is not downloaded.

**Solution**:
```cmd
python -m spacy download en_core_web_sm
```

### 6. Slow Performance

**Problem**: Analysis takes too long or uses too much memory.

**Solutions**:
- **Reduce document size**: Split large documents
- **Increase threshold**: Use 0.8 instead of 0.7
- **Close other applications**: Free up RAM
- **Use smaller model**: Try `facebook-bart-large-mnli`

### 7. Import Errors

**Problem**: Python can't import required modules.

**Solution**:
```cmd
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Or install individually
pip install streamlit pandas numpy plotly
pip install pdfminer.six python-docx beautifulsoup4
pip install spacy transformers torch
pip install jinja2 python-magic chardet tqdm
```

## 🔧 Advanced Troubleshooting

### Check Python Installation
```cmd
python --version
python -c "import sys; print(sys.executable)"
```

### Check Installed Packages
```cmd
pip list | findstr streamlit
pip list | findstr spacy
pip list | findstr transformers
```

### Verify spaCy Model
```cmd
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully')"
```

### Test Individual Components
```cmd
# Test document extraction
python -c "from extractor import DocumentExtractor; print('Extractor OK')"

# Test NLP processing
python -c "from nlp import NLPProcessor; print('NLP OK')"

# Test Streamlit
python -c "import streamlit; print('Streamlit OK')"
```

## 🚀 Quick Fixes

### Complete Reset
```cmd
# 1. Stop everything
stop_streamlit.bat

# 2. Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# 3. Download models
python -m spacy download en_core_web_sm

# 4. Verify
python verify_structure.py

# 5. Test
python demo.py
```

### Fresh Start
```cmd
# Delete Python cache
rmdir /s /q __pycache__
rmdir /s /q extractor\__pycache__
rmdir /s /q nlp\__pycache__
rmdir /s /q reports\__pycache__
rmdir /s /q ui\__pycache__

# Run setup
setup.bat
```

## 📋 Diagnostic Commands

### System Information
```cmd
# Python version
python --version

# Installed packages
pip list

# System info
systeminfo | findstr "OS Name"
systeminfo | findstr "Total Physical Memory"
```

### Network Check
```cmd
# Check if port 8501 is free
netstat -an | find ":8501"

# Check localhost
ping localhost
```

### File Permissions
```cmd
# Check if you can write to the directory
echo test > test.txt
del test.txt
```

## 🆘 Emergency Solutions

### If Nothing Works
1. **Restart your computer**
2. **Run as Administrator**:
   - Right-click Command Prompt
   - Select "Run as administrator"
   - Navigate to project folder
   - Run `setup.bat`

### Alternative Installation
```cmd
# Create virtual environment
python -m venv smart_doc_env
smart_doc_env\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Manual Streamlit Start
```cmd
# If batch files don't work
cd "C:\drive D\experiment_curser\smart_doc_checker"
streamlit run ui\app.py --server.port=8501 --server.address=localhost
```

## 📞 Getting Help

### Before Asking for Help
1. **Run diagnostic commands** above
2. **Check error messages** carefully
3. **Try the quick fixes** first
4. **Restart your computer**

### Information to Provide
- **Operating System**: Windows version
- **Python Version**: `python --version`
- **Error Message**: Exact text
- **Steps Taken**: What you tried
- **System Specs**: RAM, CPU

### Common Solutions Summary
| Problem | Quick Fix |
|---------|-----------|
| Runtime exists | `stop_streamlit.bat` |
| Python not found | Install Python with PATH |
| Dependencies missing | `setup.bat` |
| Port in use | `stop_streamlit.bat` |
| Model missing | `python -m spacy download en_core_web_sm` |
| Slow performance | Increase threshold to 0.8 |
| Import errors | `pip install -r requirements.txt` |

---

**Most issues can be solved by running `stop_streamlit.bat` followed by `setup.bat`!** 🚀
