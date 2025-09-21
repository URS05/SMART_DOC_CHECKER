"""
Smart Doc Checker Agent - Main Deployment Entry Point

This is the main entry point for deployment platforms.
It uses the simple_app.py which works reliably without CSS issues.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the working simple app
if __name__ == "__main__":
    from simple_app import main
    main()
else:
    # For deployment platforms that import the module
    from simple_app import *
