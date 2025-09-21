# 🚀 Deployment Guide

This guide covers multiple deployment options for the Smart Doc Checker Agent.

## 📋 Pre-requisites

- Python 3.11+
- All dependencies installed (`pip install -r requirements.txt`)
- spaCy English model (`python -m spacy download en_core_web_sm`)

## 🌐 Deployment Options

### 1. **Streamlit Cloud** (Recommended - Free)

**Steps:**
1. Push your code to GitHub (already done!)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository: `smart-doc-checker`
5. Set main file path: `app.py`
6. Click "Deploy"

**Advantages:**
- ✅ Free hosting
- ✅ Automatic deployments from GitHub
- ✅ Built-in SSL
- ✅ Easy to use

**Configuration:**
- Main file: `app.py`
- Python version: 3.11
- Requirements: `requirements.txt`
- Advanced settings: None needed

---

### 2. **Railway** (Easy, Paid)

**Steps:**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect the configuration

**Advantages:**
- ✅ Simple deployment
- ✅ Automatic HTTPS
- ✅ Custom domains
- ✅ Good performance

**Cost:** ~$5/month

---

### 3. **Heroku** (Traditional, Paid)

**Steps:**
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Push: `git push heroku main`

**Commands:**
```bash
heroku create smart-doc-checker-app
git push heroku main
heroku open
```

**Cost:** ~$7/month (Eco Dyno)

---

### 4. **Docker + Any Cloud** (Advanced)

**Local testing:**
```bash
docker build -t smart-doc-checker .
docker run -p 8501:8501 smart-doc-checker
```

**Deploy to:**
- Google Cloud Run
- AWS ECS
- Azure Container Instances
- DigitalOcean App Platform

---

### 5. **Replit** (Quick & Free)

**Steps:**
1. Go to [replit.com](https://replit.com)
2. Click "Import from GitHub"
3. Enter your repository URL
4. Click "Import from GitHub"
5. Run the project

---

## 🔧 Environment Variables

For cloud deployments, you might need:

```bash
PYTHONPATH=/app
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
```

## 📊 Resource Requirements

**Minimum:**
- RAM: 1GB
- CPU: 0.5 vCPU
- Storage: 2GB

**Recommended:**
- RAM: 2GB
- CPU: 1 vCPU
- Storage: 5GB

## 🐛 Troubleshooting

### Common Issues:

**1. spaCy model not found:**
```bash
python -m spacy download en_core_web_sm
```

**2. Port binding issues:**
```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**3. Memory issues:**
- Use smaller model variants
- Reduce batch sizes in config.py

**4. Timeout during deployment:**
- Increase build timeout settings
- Use lighter requirements if possible

## 📈 Performance Optimization

**For production:**
1. Use CPU-optimized instances
2. Enable caching in Streamlit
3. Optimize model loading
4. Use CDN for static assets

## 🔐 Security Notes

- The app processes uploaded documents locally
- No data is stored permanently
- All processing happens in memory
- Reports are temporary

## 📞 Support

If you encounter issues:
1. Check the logs in your deployment platform
2. Verify all files are committed to Git
3. Ensure requirements.txt is up to date
4. Test locally first with `streamlit run app.py`

---

**Happy Deploying! 🎉**
