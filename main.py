"""
Smart Doc Checker Agent

Main application entry point for the Smart Doc Checker Agent.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main application entry point."""
    try:
        import streamlit.web.cli as stcli
        
        # Set the app file path
        app_file = project_root / "ui" / "app.py"
        
        print(f"🚀 Starting Smart Doc Checker Agent...")
        print(f"📄 Loading app from: {app_file}")
        print(f"🌐 Server will be available at: http://localhost:8501")
        print(f"⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run the Streamlit app
        sys.argv = [
            "streamlit",
            "run",
            str(app_file),
            "--server.port=8501",
            "--server.address=localhost",
            "--server.headless=false"
        ]
        
        stcli.main()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting application: {str(e)}")
        print("\n🔧 Try running: python demo.py to test the system")
        sys.exit(1)

if __name__ == "__main__":
    main()
