"""
Document Extractors Module

This module provides functionality to extract text from various document formats
including PDF, DOCX, HTML, and TXT files.
"""

from .document_extractor import DocumentExtractor, get_file_type

__all__ = ['DocumentExtractor', 'get_file_type']
