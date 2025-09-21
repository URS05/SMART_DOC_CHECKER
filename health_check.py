"""
Health check script for deployment monitoring
This ensures the app stays alive and healthy
"""

import requests
import time
import os
from datetime import datetime

def ping_app():
    """Ping the deployed app to keep it alive."""
    app_url = os.getenv('STREAMLIT_APP_URL', 'http://localhost:8501')
    
    try:
        response = requests.get(f"{app_url}/_stcore/health", timeout=10)
        if response.status_code == 200:
            print(f"✅ {datetime.now()}: App is healthy")
            return True
        else:
            print(f"⚠️ {datetime.now()}: App returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {datetime.now()}: Health check failed: {e}")
        return False

if __name__ == "__main__":
    # Simple health check
    ping_app()
