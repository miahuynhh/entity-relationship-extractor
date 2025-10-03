"""
Entity Extraction Module

This module handles the extraction of named entities from text using spaCy.
"""

import spacy
from typing import List, Dict, Any


class EntityExtractor:
    """
    A class to extract named entities from text using spaCy's en_core_web_sm model.
    """
    
    def __init__(self):
        """Initialize the entity extractor with spaCy model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError(
                "spaCy model 'en_core_web_sm' not found. "
                "Please install it using: python -m spacy download en_core_web_sm"
            )
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from the input text.
        
        Args:
            text (str): The input text to extract entities from
            
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing entity information
            Each dictionary contains:
                - text: the entity text span
                - label: the entity type (PERSON, GPE, ORG, etc.)
                - start: start character position
                - end: end character position
        """
        if not text or not text.strip():
            return []
        
        # Process the text with spaCy
        doc = self.nlp(text)
        
        entities = []
        for ent in doc.ents:
            entity_info = {
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            }
            entities.append(entity_info)
        
        return entities
    
    def get_entity_types(self) -> List[str]:
        """
        Get the list of entity types that spaCy can identify.
        
        Returns:
            List[str]: List of entity type labels
        """
        return list(self.nlp.get_pipe("ner").labels)


def main():
    """Test the entity extractor with sample text."""
    extractor = EntityExtractor()
    
    # Sample text for testing
    sample_text = "Alan Turing was a pioneering mathematician and computer scientist from the United Kingdom."
    
    print("Sample text:", sample_text)
    print("\nExtracted entities:")
    
    entities = extractor.extract_entities(sample_text)
    for i, entity in enumerate(entities, 1):
        print(f"{i}. {entity['text']} ({entity['label']}) - positions {entity['start']}-{entity['end']}")
    
    print(f"\nAvailable entity types: {extractor.get_entity_types()}")


if __name__ == "__main__":
    main()

