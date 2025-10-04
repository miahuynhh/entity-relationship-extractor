# Entity Relationship Visualizer with Knowledge Graph Integration

An interactive web application with Python backend that allows users to explore entities and relationships in free-form text using Wikidata knowledge graph integration.

## Core Features

### ✅ Required Functionality (Graded)
- **Entity Extraction**: Uses spaCy with `en_core_web_sm` model to extract named entities from text
- **Knowledge Graph Integration**: Queries Wikidata API to retrieve entity labels and relationships
- **Graph Visualization**: Creates directed graphs with labeled nodes and edges
- **Directed Relationships**: Each relationship is a subject-predicate-object triplet with clear direction
- **Entity Type Labeling**: Nodes display entity types (PERSON, ORG, GPE, etc.)
- **Relationship Type Labeling**: Edges display relationship types (predicates)

### ✅ Additional Functionality (Bonus)
- **Interactive Web Interface**: Two-panel layout with text input and dynamic visualization
- **Smart Entity Recognition**: Handles complex entity names and provides intelligent corrections
- **Node Sizing by Popularity**: Adjusts node sizes based on in-degree (popularity)
- **Interactive Filtering**: Filter nodes and edges by type
- **Professional Visualization**: D3.js-based interactive graph with hover effects, drag-and-drop, zoom/pan

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

### Command Line Interface (Core Functionality)
```bash
# Basic usage - generates output.txt with relationship triplets
./generate.sh --input ./input.txt --output ./output.txt

# With static graph visualization
python src/main.py --input ./input.txt --output ./output.txt --visualize --viz-output ./graph.png
```

### Web Application (Interactive Interface)
```bash
# Start the web server
python src/app.py

# Open browser to http://localhost:8080
# Enter text in left panel, click "Analyze Text" to see interactive graph in right panel
```

## Output Format

The application generates JSON-formatted relationship triplets:

```json
{'subject': 'Casey Stengel', 'subject_qid': 'Q1047261', 'predicate': 'member of sports team', 'predicate_pid': 'P54', 'object': 'New York Yankees', 'object_qid': 'Q213417', 'subject_in_degree': 0, 'object_in_degree': 1}
```

## Project Structure

```
a1/
├── src/                           # Source code (all modules in sub-modules)
│   ├── entity_extractor.py                    # Basic entity extraction
│   ├── smart_entity_extractor.py             # Enhanced entity extraction
│   ├── wikidata_client.py                    # Wikidata API integration
│   ├── enhanced_relationship_extractor.py    # Main relationship logic
│   ├── graph_visualizer.py                   # Static graph visualization
│   ├── main.py                               # Command-line interface
│   └── app.py                                # Web server (Flask)
├── templates/                     # Web application templates
│   └── index.html                            # Main web interface
├── static/                       # Web application static files
│   ├── app.js                                # Frontend JavaScript
│   ├── graph.js                              # D3.js visualization
│   └── styles.css                            # CSS styling
├── input.txt                    # Example input file
├── output.txt                   # Example output file
├── generate.sh                  # Main execution script (required by spec)
├── install.sh                   # Installation script (required by spec)
└── requirements.txt             # Python dependencies
```

## Dependencies

### Core Dependencies (Required by Specification)
- Python 3.7+
- spaCy with `en_core_web_sm` model
- NetworkX
- Matplotlib
- requests

### Web Application Dependencies
- Flask
- Flask-CORS

### Installation
All dependencies are automatically installed by the `install.sh` script, which:
1. Installs Python packages from `requirements.txt`
2. Downloads the spaCy English model
3. Sets up the environment for both CLI and web interfaces

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

## Testing and Verification

### Verify Core Functionality
```bash
# Test the main generate script (required by specification)
./generate.sh --input ./input.txt --output ./output.txt

# Verify output format matches specification
cat output.txt
```

### Verify Web Application
```bash
# Start web server
python src/app.py

# Open http://localhost:8080 in browser
# Test with sample text: "Alan Turing was a mathematician from the United Kingdom."
# Verify interactive graph displays with labeled nodes and edges
```

## Requirements Compliance

### ✅ Core Functionality (Graded)
- **Entity Extraction**: Uses spaCy `en_core_web_sm` ✓
- **Knowledge Graph Integration**: Queries Wikidata API ✓
- **Relationship Discovery**: Finds shortest relationship labels ✓
- **Graph Visualization**: Displays entities as nodes, relationships as directed edges ✓
- **Type Labeling**: Each node and edge labeled with its type ✓

### ✅ Submission Requirements
- **File Structure**: All code in `src/` directory ✓
- **Required Files**: `input.txt`, `output.txt`, `generate.sh`, `install.sh` ✓
- **Output Format**: JSON strings with single quotes ✓
- **Additional Features**: Node sizing by in-degree included ✓

### ✅ Technical Requirements
- **Sub-modules**: Application designed in separate, manageable components ✓
- **Package Requirements**: Documented in `requirements.txt` ✓
- **Reproducible**: `generate.sh` can reproduce results ✓

## License

This project is part of CSE 490A2 coursework at the University of Washington.
