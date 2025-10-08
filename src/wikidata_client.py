"""
Wikidata Knowledge Graph Integration Module

This module handles querying the Wikidata API to retrieve entity labels
and relationships between entities.
"""

import requests
import time
from typing import List, Dict, Any, Optional, Tuple
import json


class WikidataClient:
    """
    A client for querying the Wikidata Knowledge Graph API.
    """
    
    def __init__(self):
        """Initialize the Wikidata client."""
        self.base_url = "https://www.wikidata.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EntityRelationshipExtractor/1.0 (Educational Project)'
        })
    
    def search_entity(self, entity_text: str) -> Optional[str]:
        """
        Search for an entity in Wikidata and return its QID if found.
        
        Args:
            entity_text (str): The text of the entity to search for
            
        Returns:
            Optional[str]: The QID (e.g., "Q7251") if found, None otherwise
        """
        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': entity_text,
            'limit': 1
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'search' in data and data['search']:
                return data['search'][0]['id']
            return None
            
        except requests.RequestException as e:
            print(f"Error searching for entity '{entity_text}': {e}")
            return None
    
    def get_entity_label(self, qid: str) -> Optional[str]:
        """
        Get the label for a Wikidata entity by its QID.
        
        Args:
            qid (str): The QID of the entity (e.g., "Q7251")
            
        Returns:
            Optional[str]: The entity label if found, None otherwise
        """
        params = {
            'action': 'wbgetentities',
            'format': 'json',
            'ids': qid,
            'props': 'labels',
            'languages': 'en'
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'entities' in data and qid in data['entities']:
                entity = data['entities'][qid]
                if 'labels' in entity and 'en' in entity['labels']:
                    return entity['labels']['en']['value']
            return None
            
        except requests.RequestException as e:
            print(f"Error getting label for QID '{qid}': {e}")
            return None
    
    def get_relationships(self, subject_qid: str, object_qid: str) -> List[Dict[str, str]]:
        """
        Get relationships between two entities.
        
        Args:
            subject_qid (str): QID of the subject entity
            object_qid (str): QID of the object entity
            
        Returns:
            List[Dict[str, str]]: List of relationship dictionaries with 'predicate' and 'predicate_pid' keys
        """
        params = {
            'action': 'wbgetentities',
            'format': 'json',
            'ids': f"{subject_qid}|{object_qid}",
            'props': 'claims'
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            relationships = []
            
            if 'entities' in data and subject_qid in data['entities']:
                subject_claims = data['entities'][subject_qid].get('claims', {})
                
                # Look for relationships where subject points to object
                for pid, claims in subject_claims.items():
                    for claim in claims:
                        if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
                            datavalue = claim['mainsnak']['datavalue']
                            if datavalue.get('type') == 'wikibase-entityid':
                                target_qid = datavalue['value']['id']
                                if target_qid == object_qid:
                                    # Get the predicate label
                                    predicate_label = self.get_property_label(pid)
                                    if predicate_label:
                                        relationships.append({
                                            'predicate': predicate_label,
                                            'predicate_pid': pid
                                        })
            
            return relationships
            
        except requests.RequestException as e:
            print(f"Error getting relationships between {subject_qid} and {object_qid}: {e}")
            return []
    
    def get_property_label(self, pid: str) -> Optional[str]:
        """
        Get the label for a Wikidata property by its PID.
        
        Args:
            pid (str): The PID of the property (e.g., "P27")
            
        Returns:
            Optional[str]: The property label if found, None otherwise
        """
        params = {
            'action': 'wbgetentities',
            'format': 'json',
            'ids': pid,
            'props': 'labels',
            'languages': 'en'
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'entities' in data and pid in data['entities']:
                entity = data['entities'][pid]
                if 'labels' in entity and 'en' in entity['labels']:
                    return entity['labels']['en']['value']
            return None
            
        except requests.RequestException as e:
            print(f"Error getting property label for PID '{pid}': {e}")
            return None
    
    def get_shortest_relationship(self, relationships: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
        """
        Get the relationship with the shortest predicate label.
        
        Args:
            relationships (List[Dict[str, str]]): List of relationship dictionaries
            
        Returns:
            Optional[Dict[str, str]]: The relationship with shortest predicate, or None if empty
        """
        if not relationships:
            return None
        
        return min(relationships, key=lambda x: len(x['predicate']))
    
    def process_entities(self, entities: List[Dict[str, Any]], quiet: bool = False) -> List[Dict[str, Any]]:
        """
        Process a list of entities to get their Wikidata information.
        
        Args:
            entities (List[Dict[str, Any]]): List of entities from entity extraction
            quiet (bool): If True, suppress debug output
            
        Returns:
            List[Dict[str, Any]]: List of entities with Wikidata information added
        """
        processed_entities = []
        
        for entity in entities:
            entity_text = entity['text']
            if not quiet:
                print(f"Processing entity: {entity_text}")
            
            # Search for the entity in Wikidata
            qid = self.search_entity(entity_text)
            if qid:
                label = self.get_entity_label(qid)
                if label:
                    processed_entity = entity.copy()
                    processed_entity['qid'] = qid
                    processed_entity['wikidata_label'] = label
                    processed_entities.append(processed_entity)
                    if not quiet:
                        print(f"  Found: {label} ({qid})")
                else:
                    if not quiet:
                        print(f"  Found QID {qid} but no label")
            else:
                if not quiet:
                    print(f"  Not found in Wikidata")
            
            # Add small delay to be respectful to the API
            time.sleep(0.1)
        
        return processed_entities


def main():
    """Test the Wikidata client with sample entities."""
    client = WikidataClient()
    
    # Test with sample entities
    test_entities = [
        {'text': 'Alan Turing', 'label': 'PERSON'},
        {'text': 'United Kingdom', 'label': 'GPE'},
        {'text': 'Mount Rainier', 'label': 'FAC'}
    ]
    
    print("Testing Wikidata Integration")
    print("=" * 50)
    
    processed_entities = client.process_entities(test_entities)
    
    print(f"\nProcessed {len(processed_entities)} entities:")
    for entity in processed_entities:
        print(f"- {entity['text']} -> {entity['wikidata_label']} ({entity['qid']})")
    
    # Test relationship finding
    if len(processed_entities) >= 2:
        print(f"\nTesting relationship between {processed_entities[0]['text']} and {processed_entities[1]['text']}")
        relationships = client.get_relationships(
            processed_entities[0]['qid'], 
            processed_entities[1]['qid']
        )
        
        if relationships:
            shortest_rel = client.get_shortest_relationship(relationships)
            print(f"Found relationship: {shortest_rel}")
        else:
            print("No relationships found")


if __name__ == "__main__":
    main()

