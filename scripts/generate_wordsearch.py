"""
Script to generate word search puzzles from JSON input files.

This module provides a command-line interface for creating wordsearch puzzles
using the wordsearch library. It accepts JSON files containing puzzle
definitions and outputs the generated puzzles to the console.
"""

import argparse
import json
import logging
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

# pylint: disable=wrong-import-position,import-error
from wordsearch import generate
from wordsearch import docx_export

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file, json format")
    parser.add_argument("-o", "--output", help="output folder")
    parser.add_argument(
        "-b",
        "--basic",
        action="store_true",
        help=(
            "only basic directions: left to right, top to bottom, "
            "diagonal from top left to bottom right"
        ),
    )
    args = parser.parse_args()

    # [TO DO]: handle output folder
    # if args.output is None :
    #     args.output = os.path.join(
    #         os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    #         "out",
    #     )

    # if not os.path.exists(args.output):
    #     try:
    #         os.makedirs(args.output)
    #     except Exception as e:
    #         logging.error(f"Failed to create output directory: {e}")
    #         exit(1)

    # get input file data
    input_file = os.path.join(os.getcwd(), args.input)
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
        logging.error("Failed to read input file: %s", e)
        sys.exit(1)

    for j, item in enumerate(data["puzzles"]):
        # default size
        size = 15
        puzzle = None

        if {"title", "words"} <= item.keys():
            if "size" in item:
                size = item["size"]

            puzzle = generate.generate_puzzle(
                item["title"],
                item["words"],
                size,
                args.basic,
                verbose=True,
            )

        # Save DOCX with grid and solution
        if puzzle and args.output:
            output_docx = f"{item['title'].lower().replace(' ', '_')}_wordsearch.docx"
            output_docx = os.path.join(args.output, output_docx)
            docx_export.save_wordsearch_to_docx(
                output_docx, item["title"], puzzle.grid, puzzle.words, puzzle.solution
            )
