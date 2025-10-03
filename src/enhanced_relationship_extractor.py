"""
Enhanced Relationship Extraction Module

This module combines entity extraction with Wikidata knowledge graph integration
and graph visualization to discover and visualize relationships between entities.
"""

from typing import List, Dict, Any, Optional
from smart_entity_extractor import SmartEntityExtractor
from wikidata_client import WikidataClient
from graph_visualizer import GraphVisualizer
import networkx as nx


class EnhancedRelationshipExtractor:
    """
    An enhanced class that extracts entities and their relationships from text,
    and provides graph visualization capabilities.
    """
    
    def __init__(self):
        """Initialize the enhanced relationship extractor."""
        self.entity_extractor = SmartEntityExtractor()
        self.wikidata_client = WikidataClient()
        self.graph_visualizer = GraphVisualizer()
    
    def extract_relationships(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities and their relationships from text.
        
        Args:
            text (str): The input text to analyze
            
        Returns:
            List[Dict[str, Any]]: List of relationship triplets with in-degree information
        """
        # Step 1: Extract entities from text
        entities = self.entity_extractor.extract_entities(text)
        if len(entities) < 2:
            print("Need at least 2 entities to find relationships")
            return []
        
        print(f"Found {len(entities)} entities: {[e['text'] for e in entities]}")
        
        # Step 2: Get Wikidata information for entities
        processed_entities = self.wikidata_client.process_entities(entities)
        if len(processed_entities) < 2:
            print("Need at least 2 entities with Wikidata information")
            return []
        
        print(f"Found Wikidata info for {len(processed_entities)} entities")
        
        # Step 3: Find relationships between all pairs of entities
        relationships = []
        
        for i in range(len(processed_entities)):
            for j in range(i + 1, len(processed_entities)):
                subject = processed_entities[i]
                object_entity = processed_entities[j]
                
                print(f"Checking relationships between '{subject['text']}' and '{object_entity['text']}'")
                
                # Check both directions: subject -> object and object -> subject
                rels_forward = self.wikidata_client.get_relationships(
                    subject['qid'], object_entity['qid']
                )
                rels_backward = self.wikidata_client.get_relationships(
                    object_entity['qid'], subject['qid']
                )
                
                # Process forward relationships
                if rels_forward:
                    shortest_rel = self.wikidata_client.get_shortest_relationship(rels_forward)
                    if shortest_rel:
                        relationship = {
                            'subject': subject['wikidata_label'],
                            'subject_qid': subject['qid'],
                            'predicate': shortest_rel['predicate'],
                            'predicate_pid': shortest_rel['predicate_pid'],
                            'object': object_entity['wikidata_label'],
                            'object_qid': object_entity['qid']
                        }
                        relationships.append(relationship)
                        print(f"  Found: {relationship['subject']} --[{relationship['predicate']}]--> {relationship['object']}")
                
                # Process backward relationships
                if rels_backward:
                    shortest_rel = self.wikidata_client.get_shortest_relationship(rels_backward)
                    if shortest_rel:
                        relationship = {
                            'subject': object_entity['wikidata_label'],
                            'subject_qid': object_entity['qid'],
                            'predicate': shortest_rel['predicate'],
                            'predicate_pid': shortest_rel['predicate_pid'],
                            'object': subject['wikidata_label'],
                            'object_qid': subject['qid']
                        }
                        relationships.append(relationship)
                        print(f"  Found: {relationship['subject']} --[{relationship['predicate']}]--> {relationship['object']}")
                
                if not rels_forward and not rels_backward:
                    print(f"  No relationships found")
        
        # Step 4: Add in-degree information for visualization
        relationships_with_degrees = self._add_in_degree_info(relationships, processed_entities)
        
        return relationships_with_degrees
    
    def _add_in_degree_info(self, relationships: List[Dict[str, Any]], 
                           entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add in-degree information to relationships for visualization.
        
        Args:
            relationships (List[Dict[str, Any]]): List of relationships
            entities (List[Dict[str, Any]]): List of entities with Wikidata info
            
        Returns:
            List[Dict[str, Any]]: Relationships with in-degree information added
        """
        # Create a temporary graph to calculate in-degrees
        temp_graph = nx.DiGraph()
        
        # Add all entities as nodes
        for entity in entities:
            temp_graph.add_node(entity['qid'])
        
        # Add all relationships as edges
        for rel in relationships:
            temp_graph.add_edge(rel['subject_qid'], rel['object_qid'])
        
        # Add in-degree information to relationships
        relationships_with_degrees = []
        for rel in relationships:
            rel_copy = rel.copy()
            rel_copy['subject_in_degree'] = temp_graph.in_degree(rel['subject_qid'])
            rel_copy['object_in_degree'] = temp_graph.in_degree(rel['object_qid'])
            relationships_with_degrees.append(rel_copy)
        
        return relationships_with_degrees
    
    def create_visualization(self, text: str, save_path: Optional[str] = None) -> None:
        """
        Create a graph visualization of entities and relationships.
        
        Args:
            text (str): The input text to analyze
            save_path (Optional[str]): Path to save the visualization
        """
        # Extract entities and relationships
        entities = self.entity_extractor.extract_entities(text)
        processed_entities = self.wikidata_client.process_entities(entities)
        relationships = self.extract_relationships(text)
        
        if not processed_entities:
            print("No entities found for visualization")
            return
        
        # Clear previous graph
        self.graph_visualizer.clear()
        
        # Add entities and relationships to graph
        self.graph_visualizer.add_entities(processed_entities)
        self.graph_visualizer.add_relationships(relationships)
        
        # Create visualization
        title = f"Entity Relationship Graph: {text[:50]}{'...' if len(text) > 50 else ''}"
        self.graph_visualizer.visualize(title=title, save_path=save_path)
    
    def format_output(self, relationships: List[Dict[str, Any]]) -> List[str]:
        """
        Format relationships as JSON strings for output file.
        
        Args:
            relationships (List[Dict[str, Any]]): List of relationship dictionaries
            
        Returns:
            List[str]: List of JSON-formatted strings
        """
        output_lines = []
        
        for rel in relationships:
            # Convert to single-quoted JSON format as required
            json_str = str(rel).replace('"', "'")
            output_lines.append(json_str)
        
        return output_lines


def main():
    """Test the enhanced relationship extractor with sample text."""
    extractor = EnhancedRelationshipExtractor()
    
    # Test with the sample text
    sample_text = "Alan Turing was a pioneering mathematician and computer scientist from the United Kingdom."
    
    print("Testing Enhanced Relationship Extraction")
    print("=" * 50)
    print(f"Input text: {sample_text}")
    print()
    
    relationships = extractor.extract_relationships(sample_text)
    
    print(f"\nFound {len(relationships)} relationships:")
    for i, rel in enumerate(relationships, 1):
        print(f"{i}. {rel}")
    
    # Create visualization
    print("\nCreating graph visualization...")
    extractor.create_visualization(sample_text, "enhanced_graph.png")
    
    # Format for output
    output_lines = extractor.format_output(relationships)
    print(f"\nFormatted output:")
    for line in output_lines:
        print(line)


if __name__ == "__main__":
    main()
