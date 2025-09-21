"""
NLP Module

This module provides natural language processing functionality for the
Smart Doc Checker Agent.
"""

from .processor import NLPProcessor, TextChunker
from .contradiction_detector import ContradictionDetector, ContradictionAnalyzer

__all__ = ['NLPProcessor', 'TextChunker', 'ContradictionDetector', 'ContradictionAnalyzer']
