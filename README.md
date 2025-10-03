# Entity Relationship Extractor

An interactive web application with Python backend that allows users to explore entities and relationships in free-form text using Wikidata knowledge graph integration.

## Features

- **Entity Extraction**: Uses spaCy with `en_core_web_sm` model to extract named entities from text
- **Knowledge Graph Integration**: Queries Wikidata API to retrieve entity labels and relationships
- **Graph Visualization**: Creates directed graphs with labeled nodes and edges using NetworkX and Matplotlib
- **Smart Entity Recognition**: Handles complex entity names and provides intelligent corrections
- **Relationship Discovery**: Finds meaningful relationships between all entity pairs

## Installation

1. Clone the repository:
```bash
git clone git@github.com:miahuynhh/entity-relationship-extractor.git
cd entity-relationship-extractor
```

2. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

## Usage

### Basic Usage
```bash
./generate.sh --input ./input.txt --output ./output.txt
```

### With Visualization
```bash
python src/main.py --input ./input.txt --output ./output.txt --visualize --viz-output ./graph.png
```

## Output Format

The application generates JSON-formatted relationship triplets:

```json
{'subject': 'Casey Stengel', 'subject_qid': 'Q1047261', 'predicate': 'member of sports team', 'predicate_pid': 'P54', 'object': 'New York Yankees', 'object_qid': 'Q213417', 'subject_in_degree': 0, 'object_in_degree': 1}
```

## Project Structure

```
a1/
├── src/                    # Source code
│   ├── entity_extractor.py              # Basic entity extraction
│   ├── smart_entity_extractor.py        # Enhanced entity extraction
│   ├── wikidata_client.py               # Wikidata API integration
│   ├── enhanced_relationship_extractor.py # Main relationship logic
│   ├── graph_visualizer.py              # Graph visualization
│   └── main.py                          # Command-line interface
├── input.txt              # Example input file
├── output.txt             # Example output file
├── generate.sh            # Main execution script
├── install.sh             # Installation script
└── requirements.txt       # Python dependencies
```

## Dependencies

- Python 3.7+
- spaCy with `en_core_web_sm` model
- NetworkX
- Matplotlib
- requests

## Example

Input text:
```
Charles Dillon "Casey" Stengel was an American professional baseball player and manager in Major League Baseball. He played for the New York Yankees and New York Mets.
```

Output relationships:
- Casey Stengel → Major League Baseball (league or competition)
- Casey Stengel → New York Yankees (member of sports team)
- Casey Stengel → New York Mets (member of sports team)
- New York Yankees → Major League Baseball (league or competition)
- New York Mets → Major League Baseball (league or competition)

## License

This project is part of CSE 490A2 coursework at the University of Washington.
