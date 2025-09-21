"""
Smart Doc Checker Agent - Main Deployment Entry Point

Optimized for always-on deployment with memory management.
Uses the simple_app.py which works reliably without CSS issues.
"""

import sys
import os
import gc
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Memory optimization for always-on deployment
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['OMP_NUM_THREADS'] = '2'
os.environ['MKL_NUM_THREADS'] = '2'

# Import and run the working simple app
if __name__ == "__main__":
    from simple_app import main
    main()
else:
    # For deployment platforms that import the module
    from simple_app import *
