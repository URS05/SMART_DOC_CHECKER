"""
NLP Processing Module

This module provides natural language processing functionality including
sentence segmentation, entity recognition, and text preprocessing.
"""

import logging
from typing import Dict, List, Optional, Tuple
import spacy
from spacy import displacy
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NLPProcessor:
    """Natural Language Processing processor using spaCy."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize the NLP processor.
        
        Args:
            model_name: Name of the spaCy model to use
        """
        self.model_name = model_name
        self.nlp = None
        self._load_model()
    
    def _load_model(self):
        """Load the spaCy model."""
        try:
            self.nlp = spacy.load(self.model_name)
            logger.info(f"Successfully loaded spaCy model: {self.model_name}")
        except OSError:
            logger.warning(f"Model {self.model_name} not found. Installing...")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "spacy", "download", self.model_name])
            self.nlp = spacy.load(self.model_name)
            logger.info(f"Successfully installed and loaded spaCy model: {self.model_name}")
    
    def process_text(self, text: str) -> Dict:
        """
        Process text and extract linguistic features.
        
        Args:
            text: Input text to process
            
        Returns:
            Dictionary containing processed text information
        """
        if not text or not self.nlp:
            return {
                'sentences': [],
                'entities': [],
                'tokens': [],
                'lemmas': [],
                'pos_tags': []
            }
        
        doc = self.nlp(text)
        
        return {
            'sentences': [sent.text.strip() for sent in doc.sents if sent.text.strip()],
            'entities': self._extract_entities(doc),
            'tokens': [token.text for token in doc],
            'lemmas': [token.lemma_ for token in doc],
            'pos_tags': [(token.text, token.pos_) for token in doc],
            'doc': doc  # Keep the spaCy doc object for advanced processing
        }
    
    def _extract_entities(self, doc) -> List[Dict]:
        """Extract named entities from the document."""
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'description': spacy.explain(ent.label_)
            })
        return entities
    
    def extract_statements(self, text: str, min_length: int = 20) -> List[Dict]:
        """
        Extract logical statements from text.
        
        Args:
            text: Input text
            min_length: Minimum length for a statement
            
        Returns:
            List of statement dictionaries
        """
        processed = self.process_text(text)
        statements = []
        
        for i, sentence in enumerate(processed['sentences']):
            if len(sentence) >= min_length:
                # Extract entities in this sentence
                sent_doc = self.nlp(sentence)
                entities = self._extract_entities(sent_doc)
                
                statements.append({
                    'id': f"stmt_{i}",
                    'text': sentence,
                    'entities': entities,
                    'length': len(sentence),
                    'word_count': len(sentence.split()),
                    'source_sentence_index': i
                })
        
        return statements
    
    def preprocess_for_nli(self, text: str) -> str:
        """
        Preprocess text for Natural Language Inference.
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text)
        
        # Ensure proper sentence ending
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def extract_key_phrases(self, text: str, max_phrases: int = 10) -> List[str]:
        """
        Extract key phrases from text using noun phrases.
        
        Args:
            text: Input text
            max_phrases: Maximum number of phrases to extract
            
        Returns:
            List of key phrases
        """
        if not text or not self.nlp:
            return []
        
        doc = self.nlp(text)
        phrases = []
        
        for chunk in doc.noun_chunks:
            phrase = chunk.text.strip()
            if len(phrase) > 3 and len(phrase.split()) <= 5:  # Reasonable phrase length
                phrases.append(phrase)
        
        # Remove duplicates and sort by frequency
        phrase_counts = {}
        for phrase in phrases:
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
        
        sorted_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)
        return [phrase for phrase, count in sorted_phrases[:max_phrases]]
    
    def find_similar_statements(self, statements: List[Dict], threshold: float = 0.7) -> List[Tuple[int, int, float]]:
        """
        Find similar statements using spaCy's similarity.
        
        Args:
            statements: List of statement dictionaries
            threshold: Similarity threshold
            
        Returns:
            List of tuples (index1, index2, similarity_score)
        """
        if not self.nlp or len(statements) < 2:
            return []
        
        similar_pairs = []
        
        for i in range(len(statements)):
            for j in range(i + 1, len(statements)):
                stmt1 = self.nlp(statements[i]['text'])
                stmt2 = self.nlp(statements[j]['text'])
                
                similarity = stmt1.similarity(stmt2)
                
                if similarity >= threshold:
                    similar_pairs.append((i, j, similarity))
        
        return similar_pairs
    
    def visualize_entities(self, text: str, output_file: Optional[str] = None) -> str:
        """
        Create entity visualization.
        
        Args:
            text: Input text
            output_file: Optional output file path
            
        Returns:
            HTML string for entity visualization
        """
        if not text or not self.nlp:
            return ""
        
        doc = self.nlp(text)
        html = displacy.render(doc, style="ent", jupyter=False)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
        
        return html


class TextChunker:
    """Utility class for chunking text into logical segments."""
    
    @staticmethod
    def chunk_by_sentences(text: str, chunk_size: int = 5) -> List[str]:
        """
        Chunk text by sentences.
        
        Args:
            text: Input text
            chunk_size: Number of sentences per chunk
            
        Returns:
            List of text chunks
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        for i in range(0, len(sentences), chunk_size):
            chunk = '. '.join(sentences[i:i + chunk_size])
            if chunk:
                chunks.append(chunk + '.')
        
        return chunks
    
    @staticmethod
    def chunk_by_paragraphs(text: str) -> List[str]:
        """
        Chunk text by paragraphs.
        
        Args:
            text: Input text
            
        Returns:
            List of paragraph chunks
        """
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]
    
    @staticmethod
    def chunk_by_length(text: str, max_length: int = 500) -> List[str]:
        """
        Chunk text by character length.
        
        Args:
            text: Input text
            max_length: Maximum length per chunk
            
        Returns:
            List of text chunks
        """
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > max_length and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks


# Example usage
if __name__ == "__main__":
    processor = NLPProcessor()
    
    sample_text = """
    The company reported record profits this quarter. 
    However, the CEO mentioned concerns about future growth. 
    The stock price increased by 15% following the announcement.
    """
    
    statements = processor.extract_statements(sample_text)
    print(f"Extracted {len(statements)} statements:")
    for stmt in statements:
        print(f"- {stmt['text']}")
