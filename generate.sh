#!/bin/bash

# Generate script for entity relationship extraction
# Usage: ./generate.sh --input ./input.txt

# Check if input argument is provided
if [ "$1" != "--input" ] || [ -z "$2" ]; then
    echo "Usage: $0 --input <input_file>"
    exit 1
fi

INPUT_FILE="$2"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found" >&2
    exit 1
fi

# Run the main Python script and output to stdout
python src/main.py --input "$INPUT_FILE" --stdout

if [ $? -ne 0 ]; then
    echo "Generation failed!" >&2
    exit 1
fi

