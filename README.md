# 🚀 Smart Doc Checker Agent

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

> **AI-Powered Document Contradiction Detection System**  
> Automatically detect contradictions and inconsistencies across multiple documents using state-of-the-art Natural Language Processing.

## ⚡ One-Click Setup & Launch

**For Windows users, it's incredibly simple:**

1. **Download/Clone** this repository
2. **Double-click** `LAUNCH_SMART_DOC_CHECKER.bat`  
3. **That's it!** ✨

The bat file will automatically:
- ✅ Check your Python installation
- ✅ Set up a virtual environment
- ✅ Install all dependencies (including AI models)
- ✅ Launch the application with a user-friendly menu

## 🎯 Quick Start

```bash
# Method 1: Clone the repository
git clone https://github.com/YOUR_USERNAME/smart-doc-checker.git
cd smart-doc-checker

# Method 2: Download ZIP and extract

# Then simply run:
LAUNCH_SMART_DOC_CHECKER.bat
```

## 🌟 Features

- 🔍 **Multi-Format Support**: PDF, DOCX, HTML, and TXT files
- 🤖 **AI-Powered Analysis**: Uses RoBERTa-large-mnli for contradiction detection
- 🌐 **Web Interface**: Beautiful Streamlit-based UI
- 📊 **Detailed Reports**: HTML and Markdown reports with confidence scores
- 🔗 **Cross-Document Analysis**: Finds contradictions between different files
- 🎯 **High Accuracy**: State-of-the-art Natural Language Inference models
- 💻 **Easy Setup**: One-click installation and launch

## 📸 Screenshots

### Web Interface
![Web Interface](screenshots/web_interface.png)

### Analysis Results
![Analysis Results](screenshots/results.png)

### Generated Reports
![Reports](screenshots/reports.png)

## 🎮 Demo

The application comes with sample documents that demonstrate contradiction detection:

- **Financial Reports**: Detects inconsistencies in quarterly reports
- **Product Updates**: Finds conflicts in product launch information
- **Cross-Document**: Identifies contradictions between different documents

Run the demo to see **243 contradictions** detected across 4 sample documents!

## 🛠️ What It Does

1. **Document Processing**: Extracts text from multiple file formats
2. **AI Analysis**: Uses advanced NLP models to understand content
3. **Contradiction Detection**: Identifies conflicting statements with confidence scores
4. **Report Generation**: Creates comprehensive reports with actionable insights
5. **Cross-Document Comparison**: Finds inconsistencies across different files

## 📋 System Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended for large documents)
- **Storage**: 2GB free space (for AI models)
- **Internet**: Required for initial setup and model downloads

## 🚀 Usage Examples

### Web Interface (Recommended)
1. Run `LAUNCH_SMART_DOC_CHECKER.bat`
2. Choose option 1 (Web Interface)
3. Upload your documents
4. Click "Analyze"
5. View results and download reports

### Command Line Demo
1. Run `LAUNCH_SMART_DOC_CHECKER.bat`
2. Choose option 2 (Run Demo)
3. See analysis of sample documents
4. Check the `reports/` folder for outputs

## 📊 Understanding Results

### Contradiction Scores
- **0.0-0.3**: Low contradiction likelihood
- **0.3-0.6**: Medium contradiction likelihood  
- **0.6-0.8**: High contradiction likelihood
- **0.8-1.0**: Very high contradiction likelihood

### Report Components
- **Executive Summary**: Overall statistics
- **Document Analysis**: Individual document results
- **Cross-Document Contradictions**: Conflicts between files
- **Recommendations**: Actionable suggestions

## 🔧 Advanced Configuration

The system supports various AI models and settings:

- **Models**: `roberta-large-mnli`, `facebook-bart-large-mnli`
- **Thresholds**: Adjustable contradiction sensitivity (0.5-0.9)
- **Batch Processing**: Handle multiple documents simultaneously
- **Report Formats**: Markdown, HTML, or both

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🐛 Troubleshooting

### Common Issues

**Python not found?**
- Install Python 3.8+ from [python.org](https://python.org)
- Make sure to check "Add Python to PATH"

**Installation fails?**
- Run as Administrator
- Check your internet connection
- Ensure you have 2GB+ free space

**Slow processing?**
- This is normal on first run (downloads AI models)
- Large documents take more time to process
- Consider using a lower threshold for faster results

**Still having issues?**
- Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
- Create an issue on GitHub
- Include your error message and system info

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face**: For providing transformer models
- **spaCy**: For natural language processing
- **Streamlit**: For the web interface framework
- **All contributors**: Who help make this project better

## 📈 Roadmap

- [ ] Support for more document formats
- [ ] Multi-language support
- [ ] API endpoints
- [ ] Cloud deployment options
- [ ] Real-time collaboration features

## ⭐ Show Your Support

If this project helped you, please consider:
- ⭐ Starring the repository
- 🍴 Forking for your own use
- 🐛 Reporting bugs or requesting features
- 📢 Sharing with others who might benefit

---

**Made with ❤️ for the open source community**

> 🚀 **Ready to detect contradictions in your documents?**  
> Just run `LAUNCH_SMART_DOC_CHECKER.bat` and get started!
