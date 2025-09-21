#!/usr/bin/env python3
"""
Simple launcher for Smart Doc Checker Agent
This script provides an easy way to start the application
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Smart Doc Checker Agent"""
    
    print("🚀 Smart Doc Checker Agent Launcher")
    print("=" * 50)
    
    # Get the project root
    project_root = Path(__file__).parent
    app_file = project_root / "ui" / "app.py"
    
    if not app_file.exists():
        print("❌ Error: UI app file not found!")
        print(f"Looking for: {app_file}")
        return 1
    
    print(f"📄 Found app file: {app_file}")
    print(f"🌐 Starting Streamlit server...")
    print(f"💻 The app will open in your default browser")
    print(f"🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Launch streamlit
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_file),
            "--server.port=8501",
            "--server.address=localhost"
        ], cwd=str(project_root))
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
