#!/usr/bin/env python3
"""
Setup script for Smart Doc Checker Agent
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="smart-doc-checker",
    version="1.0.0",
    description="AI-Powered Document Contradiction Detection System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Smart Doc Checker Team",
    author_email="contact@smartdocchecker.com",
    url="https://github.com/yourusername/smart-doc-checker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "smart-doc-checker=main:main",
            "smart-doc-demo=demo:run_demo",
        ],
    },
    include_package_data=True,
    package_data={
        "templates": ["*.html", "*.md"],
        "sample_docs": ["*.txt", "*.html"],
    },
    keywords="nlp, contradiction-detection, document-analysis, ai, streamlit",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/smart-doc-checker/issues",
        "Source": "https://github.com/yourusername/smart-doc-checker",
        "Documentation": "https://github.com/yourusername/smart-doc-checker#readme",
    },
)
