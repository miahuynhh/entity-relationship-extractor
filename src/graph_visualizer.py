"""
Graph Visualization Module

This module handles the visualization of entities and their relationships
as a directed graph using NetworkX and Matplotlib.
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional, Tuple
import json


class GraphVisualizer:
    """
    A class to visualize entities and relationships as a directed graph.
    """
    
    def __init__(self):
        """Initialize the graph visualizer."""
        self.graph = nx.DiGraph()
        self.node_colors = {}
        self.edge_colors = {}
        
        # Color mapping for different entity types
        self.entity_type_colors = {
            'PERSON': '#FF6B6B',      # Red
            'GPE': '#4ECDC4',         # Teal
            'ORG': '#45B7D1',         # Blue
            'FAC': '#96CEB4',         # Green
            'LOC': '#FFEAA7',         # Yellow
            'EVENT': '#DDA0DD',       # Plum
            'PRODUCT': '#98D8C8',     # Mint
            'WORK_OF_ART': '#F7DC6F', # Light Yellow
            'LAW': '#BB8FCE',         # Light Purple
            'LANGUAGE': '#85C1E9',    # Light Blue
            'MONEY': '#F8C471',       # Light Orange
            'CARDINAL': '#F1948A',    # Light Red
            'DATE': '#82E0AA',        # Light Green
            'TIME': '#D7BDE2',        # Light Purple
            'PERCENT': '#F9E79F',     # Light Yellow
            'ORDINAL': '#AED6F1',     # Light Blue
            'QUANTITY': '#A9DFBF',    # Light Green
            'NORP': '#FADBD8'         # Light Pink
        }
    
    def add_entities(self, entities: List[Dict[str, Any]]) -> None:
        """
        Add entities as nodes to the graph.
        
        Args:
            entities (List[Dict[str, Any]]): List of entities with Wikidata information
        """
        for entity in entities:
            node_id = entity['qid']
            node_label = entity['wikidata_label']
            entity_type = entity['label']
            
            # Add node with attributes
            self.graph.add_node(
                node_id,
                label=node_label,
                entity_type=entity_type,
                qid=node_id
            )
            
            # Store color for this node
            self.node_colors[node_id] = self.entity_type_colors.get(
                entity_type, '#CCCCCC'  # Default gray color
            )
    
    def add_relationships(self, relationships: List[Dict[str, Any]]) -> None:
        """
        Add relationships as directed edges to the graph.
        
        Args:
            relationships (List[Dict[str, Any]]): List of relationship triplets
        """
        for rel in relationships:
            subject_qid = rel['subject_qid']
            object_qid = rel['object_qid']
            predicate = rel['predicate']
            predicate_pid = rel['predicate_pid']
            
            # Add directed edge with attributes
            self.graph.add_edge(
                subject_qid,
                object_qid,
                predicate=predicate,
                predicate_pid=predicate_pid,
                label=predicate
            )
            
            # Store edge color (can be customized based on relationship type)
            self.edge_colors[(subject_qid, object_qid)] = '#333333'  # Dark gray
    
    def visualize(self, 
                  title: str = "Entity Relationship Graph",
                  figsize: Tuple[int, int] = (12, 8),
                  save_path: Optional[str] = None) -> None:
        """
        Create and display the graph visualization.
        
        Args:
            title (str): Title for the graph
            figsize (Tuple[int, int]): Figure size (width, height)
            save_path (Optional[str]): Path to save the graph image
        """
        if self.graph.number_of_nodes() == 0:
            print("No nodes to visualize")
            return
        
        # Create figure
        plt.figure(figsize=figsize)
        
        # Use spring layout for better node positioning
        pos = nx.spring_layout(self.graph, k=3, iterations=50)
        
        # Draw nodes
        node_colors_list = [self.node_colors.get(node, '#CCCCCC') for node in self.graph.nodes()]
        nx.draw_networkx_nodes(
            self.graph, 
            pos, 
            node_color=node_colors_list,
            node_size=2000,
            alpha=0.8
        )
        
        # Draw edges
        edge_colors_list = [self.edge_colors.get(edge, '#333333') for edge in self.graph.edges()]
        nx.draw_networkx_edges(
            self.graph,
            pos,
            edge_color=edge_colors_list,
            arrows=True,
            arrowsize=20,
            arrowstyle='->',
            alpha=0.6,
            width=2
        )
        
        # Draw node labels
        node_labels = {node: data['label'] for node, data in self.graph.nodes(data=True)}
        nx.draw_networkx_labels(
            self.graph,
            pos,
            labels=node_labels,
            font_size=8,
            font_weight='bold'
        )
        
        # Draw edge labels
        edge_labels = {(u, v): data['label'] for u, v, data in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(
            self.graph,
            pos,
            edge_labels=edge_labels,
            font_size=6,
            font_color='darkred'
        )
        
        # Set title and remove axes
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save or show the graph
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Graph saved to: {save_path}")
        else:
            plt.show()
    
    def get_graph_info(self) -> Dict[str, Any]:
        """
        Get information about the current graph.
        
        Returns:
            Dict[str, Any]: Graph statistics and information
        """
        return {
            'num_nodes': self.graph.number_of_nodes(),
            'num_edges': self.graph.number_of_edges(),
            'nodes': list(self.graph.nodes(data=True)),
            'edges': list(self.graph.edges(data=True)),
            'is_directed': self.graph.is_directed()
        }
    
    def clear(self) -> None:
        """Clear the current graph."""
        self.graph.clear()
        self.node_colors.clear()
        self.edge_colors.clear()


def main():
    """Test the graph visualizer with sample data."""
    visualizer = GraphVisualizer()
    
    # Sample entities
    entities = [
        {'qid': 'Q7251', 'wikidata_label': 'Alan Turing', 'label': 'PERSON'},
        {'qid': 'Q145', 'wikidata_label': 'United Kingdom', 'label': 'GPE'},
        {'qid': 'Q312', 'wikidata_label': 'Apple Inc.', 'label': 'ORG'},
        {'qid': 'Q19837', 'wikidata_label': 'Steve Jobs', 'label': 'PERSON'}
    ]
    
    # Sample relationships
    relationships = [
        {
            'subject': 'Alan Turing',
            'subject_qid': 'Q7251',
            'predicate': 'country of citizenship',
            'predicate_pid': 'P27',
            'object': 'United Kingdom',
            'object_qid': 'Q145'
        },
        {
            'subject': 'Apple Inc.',
            'subject_qid': 'Q312',
            'predicate': 'founded by',
            'predicate_pid': 'P112',
            'object': 'Steve Jobs',
            'object_qid': 'Q19837'
        }
    ]
    
    print("Testing Graph Visualization")
    print("=" * 50)
    
    # Add entities and relationships
    visualizer.add_entities(entities)
    visualizer.add_relationships(relationships)
    
    # Get graph info
    info = visualizer.get_graph_info()
    print(f"Graph has {info['num_nodes']} nodes and {info['num_edges']} edges")
    print(f"Is directed: {info['is_directed']}")
    
    # Create visualization
    visualizer.visualize(
        title="Sample Entity Relationship Graph",
        save_path="sample_graph.png"
    )


if __name__ == "__main__":
    main()

