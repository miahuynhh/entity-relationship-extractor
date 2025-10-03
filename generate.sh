#!/bin/bash

# Generate script for entity relationship extraction
# Usage: ./generate.sh --input ./input.txt --output ./output.txt

# Check if input and output arguments are provided
if [ "$1" != "--input" ] || [ "$3" != "--output" ]; then
    echo "Usage: $0 --input <input_file> --output <output_file>"
    exit 1
fi

INPUT_FILE="$2"
OUTPUT_FILE="$4"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found"
    exit 1
fi

# Run the main Python script
echo "Running entity relationship extraction..."
python src/main.py --input "$INPUT_FILE" --output "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "Generation completed successfully!"
else
    echo "Generation failed!"
    exit 1
fi

