#!/bin/bash

# Install script for the entity relationship extraction project
# This script installs the necessary Python dependencies and spaCy model

echo "Installing Python dependencies..."

# Install Python packages
pip install -r requirements.txt

echo "Downloading spaCy English model..."
# Download the spaCy English model
python -m spacy download en_core_web_sm

echo "Installation complete!"
echo "You can now run the project using: ./generate.sh --input ./input.txt --output ./output.txt"

