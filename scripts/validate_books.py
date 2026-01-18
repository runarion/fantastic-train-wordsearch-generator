#!/usr/bin/env python3
"""
validate_books.py

Script to validate all JSON files in the data/books directory and its subfolders.
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
        if 'title' not in data:
            errors.append("Missing 'title' key.")
        if 'puzzles' not in data:
            errors.append("Missing 'puzzles' key.")
    # Add more rules here as needed
    
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


def main(books_dir=None):
    """Main function to validate JSON files in the specified directory."""
    if books_dir is None:
        books_dir = Path(__file__).parent.parent / 'data' / 'books'
    json_files = find_json_files(books_dir)
    if not json_files:
        print(f"No JSON files found in {books_dir}")
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
    if all_ok:
        print("\nAll files passed validation.")
        sys.exit(0)
    else:
        print("\nSome files failed validation.")
        sys.exit(2)

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    # pass input folder as argument
    parser.add_argument("input_folder", help="input folder containing JSON files")
    args = parser.parse_args()
    
    main(args.input_folder)
