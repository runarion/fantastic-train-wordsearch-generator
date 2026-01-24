#!/usr/bin/env python3
"""
validate_books.py

Script to validate JSON book files.
Can validate either:
- All JSON files in a directory (and its subfolders)
- A single JSON file

Validation rules can be added to the validate_json_data() function.
"""
import argparse
import os
import sys
import json
from pathlib import Path

show_info = True  # Set to True to print the number of words in each puzzle

def find_json_files(root_dir):
    """Recursively find all .json files under root_dir."""
    return list(Path(root_dir).rglob('*.json'))

def validate_json_data(data, file_path):
    """
    Placeholder for validation rules.
    Return a list of error messages (empty if valid).
    """
    errors = []
    # Example rule: file must be a dict with 'title' and 'puzzles' keys
    if not isinstance(data, dict):
        errors.append("Root element is not a JSON object.")
    else:
        # get the version number if present, otherwise assume version 0.0
        version = data.get('version', 0.0)
        if not isinstance(version, (int, float)):
            errors.append("'version' is not a number.")
        if 'title' not in data:
            errors.append("Missing 'title' key.")
        if 'puzzles' not in data:
            errors.append("Missing 'puzzles' key.")
    # Add more rules here as needed
    
        if version >= 1.0:
            # check if color is a valid hex color code
            if 'color' in data:
                color = data['color']
                if not isinstance(color, str) or not color.startswith('#') or len(color) not in [4, 7]:
                    errors.append("'color' is not a valid hex color code.")
                else:
                    hex_digits = color[1:]
                    if len(hex_digits) == 3:
                        hex_digits = ''.join([c*2 for c in hex_digits])
                    if not all(c in '0123456789abcdefABCDEF' for c in hex_digits):
                        errors.append("'color' contains invalid hex digits.")
            else:
                errors.append("Missing 'color' key for version >= 1.0.")

        # For each puzzle in 'puzzles', check required fields
        if 'puzzles' in data:
            if not isinstance(data['puzzles'], list):
                errors.append("'puzzles' is not a list.")
            else:
                for i, puzzle in enumerate(data['puzzles']):
                    if not isinstance(puzzle, dict):
                        errors.append(f"Puzzle at index {i} is not an object.")
                        continue
                    if 'words' not in puzzle:
                        errors.append(f"Puzzle at index {i} missing 'words' key.")
                    else:
                        if not isinstance(puzzle['words'], list):
                            errors.append(f"'words' in puzzle at index {i} is not a list.")
                        #check that words has no repetitions
                        if len(puzzle['words']) != len(set(puzzle['words'])):
                            # show repeated words
                            repeated_words = set([word for word in puzzle['words'] if puzzle['words'].count(word) > 1])
                            errors.append(f"'words' in puzzle at index {i} contains duplicate words: {', '.join(repeated_words)}.")
                    if 'size' not in puzzle:
                        errors.append(f"Puzzle at index {i} missing 'size' key.")
                    else:
                        if not isinstance(puzzle['size'], int):
                            errors.append(f"'size' in puzzle at index {i} is not an integer.")
                    
                    # check that all words fit in the puzzle size
                    if 'words' in puzzle and 'size' in puzzle:
                        for word in puzzle['words']:
                            # do not count white space-only characters
                            word = word.replace(" ", "")
                            if len(word) > puzzle['size']:
                                errors.append(f"Word '{word}' in puzzle at index {i} exceeds puzzle size {puzzle['size']}.")
    
    if show_info and not errors:
        # print the file being processed
        print(f"Info for {file_path}:")
        #print number of puzzles
        num_puzzles = len(data.get('puzzles', []))
        print(f"Number of puzzles: {num_puzzles}")
        # print the size of words for each puzzle 
        for i, puzzle in enumerate(data.get('puzzles', [])):
            if 'words' in puzzle:
                title = puzzle.get('title', f"Puzzle at index {i}")
                print(f"{title} has {len(puzzle['words'])} words.")
        # print a separator
        print("-" * 40)

    return errors


def main(input_path=None):
    """
    Main function to validate JSON file(s).
    
    Args:
        input_path: Can be either:
                   - A directory path: validates all .json files in that directory and subdirectories
                   - A file path: validates only that specific .json file
                   - None: defaults to data/books directory
    """
    if input_path is None:
        input_path = Path(__file__).parent.parent / 'data' / 'books'
    
    input_path = Path(input_path)
    
    # Determine if input is a file or directory
    if input_path.is_file():
        # Validate single file
        if not input_path.suffix == '.json':
            print(f"Error: {input_path} is not a JSON file.")
            sys.exit(1)
        json_files = [input_path]
    elif input_path.is_dir():
        # Validate all files in directory
        json_files = find_json_files(input_path)
        if not json_files:
            print(f"No JSON files found in {input_path}")
            sys.exit(1)
    else:
        print(f"Error: {input_path} does not exist.")
        sys.exit(1)
    
    all_ok = True
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"[FAIL] {file_path}: Could not parse JSON: {e}")
            all_ok = False
            continue
        errors = validate_json_data(data, file_path)
        if errors:
            print(f"[FAIL] {file_path}:")
            for err in errors:
                print(f"   - {err}")
            all_ok = False
        else:
            print(f"[OK]   {file_path}")
            print()
    if all_ok:
        print("\nAll files passed validation.")
        sys.exit(0)
    else:
        print("\nSome files failed validation.")
        sys.exit(2)

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser(
        description="Validate JSON book files. Can validate a single file or all files in a directory."
    )
    # pass input path as argument (can be either a file or a folder)
    parser.add_argument(
        "input_path", 
        help="Path to either a JSON file or a folder containing JSON files"
    )
    args = parser.parse_args()
    
    main(args.input_path)
