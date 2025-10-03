"""
Main Application Script

This script processes input text files and generates relationship output files.
"""

import argparse
import sys
from pathlib import Path
import sys
sys.path.append('src')
from enhanced_relationship_extractor import EnhancedRelationshipExtractor


def main():
    """Main function to process input and generate output."""
    parser = argparse.ArgumentParser(description='Extract entities and relationships from text')
    parser.add_argument('--input', required=True, help='Input text file path')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--visualize', action='store_true', help='Create graph visualization')
    parser.add_argument('--viz-output', help='Path to save visualization image')
    
    args = parser.parse_args()
    
    # Read input file
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    if not text:
        print("Error: Input file is empty")
        sys.exit(1)
    
    print(f"Processing text: {text}")
    print("=" * 50)
    
    # Extract relationships using enhanced extractor
    extractor = EnhancedRelationshipExtractor()
    relationships = extractor.extract_relationships(text)
    
    # Create visualization if requested
    if args.visualize:
        viz_path = args.viz_output or "graph_visualization.png"
        print(f"\nCreating graph visualization...")
        extractor.create_visualization(text, viz_path)
    
    # Format output
    output_lines = extractor.format_output(relationships)
    
    # Write output file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            for line in output_lines:
                f.write(line + '\n')
        print(f"\nOutput written to: {args.output}")
        print(f"Found {len(relationships)} relationships")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
