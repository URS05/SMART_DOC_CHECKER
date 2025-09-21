"""
Contradiction Detection Module

This module provides functionality to detect contradictions between statements
using Natural Language Inference (NLI) models from Hugging Face.
"""

import logging
from typing import Dict, List, Tuple, Optional
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContradictionDetector:
    """Detects contradictions between statements using NLI models."""
    
    def __init__(self, model_name: str = "roberta-large-mnli"):
        """
        Initialize the contradiction detector.
        
        Args:
            model_name: Name of the Hugging Face model to use
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_model()
    
    def _load_model(self):
        """Load the tokenizer and model."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Successfully loaded model on {self.device}")
        except Exception as e:
            logger.error(f"Error loading model {self.model_name}: {str(e)}")
            raise
    
    def predict_contradiction(self, premise: str, hypothesis: str) -> Dict[str, float]:
        """
        Predict contradiction between premise and hypothesis.
        
        Args:
            premise: The premise statement
            hypothesis: The hypothesis statement
            
        Returns:
            Dictionary with prediction scores
        """
        if not self.tokenizer or not self.model:
            raise RuntimeError("Model not loaded")
        
        # Tokenize inputs
        inputs = self.tokenizer(
            premise, hypothesis,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=-1)
        
        # Map to labels (MNLI labels: contradiction, entailment, neutral)
        labels = ["contradiction", "entailment", "neutral"]
        scores = {}
        
        for i, label in enumerate(labels):
            scores[label] = float(probabilities[0][i])
        
        return scores
    
    def detect_contradictions(self, statements: List[Dict], threshold: float = 0.7) -> List[Dict]:
        """
        Detect contradictions between pairs of statements.
        
        Args:
            statements: List of statement dictionaries
            threshold: Minimum contradiction score threshold
            
        Returns:
            List of contradiction dictionaries
        """
        contradictions = []
        
        logger.info(f"Analyzing {len(statements)} statements for contradictions...")
        
        for i in tqdm(range(len(statements)), desc="Checking contradictions"):
            for j in range(i + 1, len(statements)):
                stmt1 = statements[i]
                stmt2 = statements[j]
                
                try:
                    # Check both directions
                    scores1 = self.predict_contradiction(stmt1['text'], stmt2['text'])
                    scores2 = self.predict_contradiction(stmt2['text'], stmt1['text'])
                    
                    # Use the maximum contradiction score
                    contradiction_score = max(scores1['contradiction'], scores2['contradiction'])
                    
                    if contradiction_score >= threshold:
                        contradiction = {
                            'statement1': stmt1,
                            'statement2': stmt2,
                            'contradiction_score': contradiction_score,
                            'entailment_score': max(scores1['entailment'], scores2['entailment']),
                            'neutral_score': max(scores1['neutral'], scores2['neutral']),
                            'scores_direction1': scores1,
                            'scores_direction2': scores2,
                            'confidence': self._calculate_confidence(scores1, scores2)
                        }
                        contradictions.append(contradiction)
                        
                except Exception as e:
                    logger.warning(f"Error processing statements {i} and {j}: {str(e)}")
                    continue
        
        # Sort by contradiction score
        contradictions.sort(key=lambda x: x['contradiction_score'], reverse=True)
        
        logger.info(f"Found {len(contradictions)} contradictions above threshold {threshold}")
        return contradictions
    
    def _calculate_confidence(self, scores1: Dict, scores2: Dict) -> float:
        """Calculate confidence score for the contradiction prediction."""
        # Average the contradiction scores
        avg_contradiction = (scores1['contradiction'] + scores2['contradiction']) / 2
        
        # Calculate how much contradiction dominates other labels
        avg_entailment = (scores1['entailment'] + scores2['entailment']) / 2
        avg_neutral = (scores1['neutral'] + scores2['neutral']) / 2
        
        # Confidence is based on how much contradiction exceeds other labels
        confidence = avg_contradiction - max(avg_entailment, avg_neutral)
        return max(0, confidence)
    
    def analyze_document_consistency(self, document_statements: List[Dict], 
                                   threshold: float = 0.7) -> Dict:
        """
        Analyze overall document consistency.
        
        Args:
            document_statements: Statements from a single document
            threshold: Contradiction threshold
            
        Returns:
            Consistency analysis results
        """
        contradictions = self.detect_contradictions(document_statements, threshold)
        
        total_pairs = len(document_statements) * (len(document_statements) - 1) // 2
        contradiction_rate = len(contradictions) / total_pairs if total_pairs > 0 else 0
        
        return {
            'total_statements': len(document_statements),
            'total_pairs_checked': total_pairs,
            'contradictions_found': len(contradictions),
            'contradiction_rate': contradiction_rate,
            'consistency_score': 1 - contradiction_rate,
            'contradictions': contradictions
        }
    
    def batch_analyze_documents(self, documents: Dict[str, List[Dict]], 
                              threshold: float = 0.7) -> Dict[str, Dict]:
        """
        Analyze multiple documents for contradictions.
        
        Args:
            documents: Dictionary mapping document names to statement lists
            threshold: Contradiction threshold
            
        Returns:
            Dictionary mapping document names to analysis results
        """
        results = {}
        
        for doc_name, statements in documents.items():
            logger.info(f"Analyzing document: {doc_name}")
            results[doc_name] = self.analyze_document_consistency(statements, threshold)
        
        return results
    
    def find_cross_document_contradictions(self, documents: Dict[str, List[Dict]], 
                                         threshold: float = 0.7) -> List[Dict]:
        """
        Find contradictions between statements from different documents.
        
        Args:
            documents: Dictionary mapping document names to statement lists
            threshold: Contradiction threshold
            
        Returns:
            List of cross-document contradictions
        """
        cross_contradictions = []
        doc_names = list(documents.keys())
        
        logger.info("Checking for cross-document contradictions...")
        
        for i in range(len(doc_names)):
            for j in range(i + 1, len(doc_names)):
                doc1_name = doc_names[i]
                doc2_name = doc_names[j]
                statements1 = documents[doc1_name]
                statements2 = documents[doc2_name]
                
                logger.info(f"Comparing {doc1_name} with {doc2_name}")
                
                for stmt1 in tqdm(statements1, desc=f"{doc1_name} vs {doc2_name}"):
                    for stmt2 in statements2:
                        try:
                            scores1 = self.predict_contradiction(stmt1['text'], stmt2['text'])
                            scores2 = self.predict_contradiction(stmt2['text'], stmt1['text'])
                            
                            contradiction_score = max(scores1['contradiction'], scores2['contradiction'])
                            
                            if contradiction_score >= threshold:
                                cross_contradiction = {
                                    'document1': doc1_name,
                                    'document2': doc2_name,
                                    'statement1': stmt1,
                                    'statement2': stmt2,
                                    'contradiction_score': contradiction_score,
                                    'entailment_score': max(scores1['entailment'], scores2['entailment']),
                                    'neutral_score': max(scores1['neutral'], scores2['neutral']),
                                    'confidence': self._calculate_confidence(scores1, scores2)
                                }
                                cross_contradictions.append(cross_contradiction)
                                
                        except Exception as e:
                            logger.warning(f"Error processing cross-document statements: {str(e)}")
                            continue
        
        # Sort by contradiction score
        cross_contradictions.sort(key=lambda x: x['contradiction_score'], reverse=True)
        
        logger.info(f"Found {len(cross_contradictions)} cross-document contradictions")
        return cross_contradictions


class ContradictionAnalyzer:
    """High-level analyzer for contradiction detection."""
    
    def __init__(self, model_name: str = "roberta-large-mnli"):
        """Initialize the analyzer."""
        self.detector = ContradictionDetector(model_name)
    
    def analyze_documents(self, documents: Dict[str, List[Dict]], 
                         threshold: float = 0.7,
                         include_cross_document: bool = True) -> Dict:
        """
        Comprehensive analysis of document contradictions.
        
        Args:
            documents: Dictionary mapping document names to statement lists
            threshold: Contradiction threshold
            include_cross_document: Whether to check cross-document contradictions
            
        Returns:
            Complete analysis results
        """
        results = {
            'individual_documents': {},
            'cross_document_contradictions': [],
            'summary': {}
        }
        
        # Analyze individual documents
        results['individual_documents'] = self.detector.batch_analyze_documents(
            documents, threshold
        )
        
        # Find cross-document contradictions
        if include_cross_document and len(documents) > 1:
            results['cross_document_contradictions'] = self.detector.find_cross_document_contradictions(
                documents, threshold
            )
        
        # Generate summary
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def _generate_summary(self, results: Dict) -> Dict:
        """Generate summary statistics."""
        individual_results = results['individual_documents']
        cross_contradictions = results['cross_document_contradictions']
        
        total_statements = sum(r['total_statements'] for r in individual_results.values())
        total_contradictions = sum(r['contradictions_found'] for r in individual_results.values())
        total_cross_contradictions = len(cross_contradictions)
        
        return {
            'total_documents': len(individual_results),
            'total_statements': total_statements,
            'total_contradictions': total_contradictions + total_cross_contradictions,
            'intra_document_contradictions': total_contradictions,
            'cross_document_contradictions': total_cross_contradictions,
            'overall_consistency_score': 1 - (total_contradictions + total_cross_contradictions) / max(total_statements, 1)
        }


# Example usage
if __name__ == "__main__":
    analyzer = ContradictionAnalyzer()
    
    # Sample statements
    statements1 = [
        {'id': 'stmt_1', 'text': 'The company reported record profits this quarter.'},
        {'id': 'stmt_2', 'text': 'The company is facing financial difficulties.'}
    ]
    
    statements2 = [
        {'id': 'stmt_3', 'text': 'The CEO announced plans for expansion.'},
        {'id': 'stmt_4', 'text': 'The company is considering layoffs.'}
    ]
    
    documents = {
        'document1': statements1,
        'document2': statements2
    }
    
    results = analyzer.analyze_documents(documents)
    print(f"Found {results['summary']['total_contradictions']} contradictions")
