"""
Script to generate a large word search book PDF from a set of puzzles.

This script reads a JSON file containing multiple word search puzzle
definitions, generates 4 variations of each puzzle, and compiles them into
a single PDF book with a title page, puzzle pages, and solution pages.
Each puzzle definition results in 4 unique puzzles (e.g., "Jungle Animals 1",
"Jungle Animals 2", "Jungle Animals 3", "Jungle Animals 4").
"""

import argparse
import json
import os
import random
import tempfile

from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from intro import create_intro_pages, create_solution_intro_pages
from wordsearch import generate
from wordsearch import pdf_render


def draw_page_number(c, page_num):
    """
    Draws a page number at the bottom center of a PDF page.
    
    Args:
        c: ReportLab canvas object
        page_num: Page number to display
    """
    page_width, page_height = letter
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_width / 2, 0.5 * 72, str(page_num))  # 0.5 inch from bottom


def create_solution_page(solutions_chunk, output_pdf, page_num=None):
    """
    Draws up to 4 solution grids on a single page and saves as PDF.
    """

    page_width, page_height = letter
    margin = 36
    grid_area = (page_width - 2 * margin) / 2  # 2 columns
    grid_positions = [
        (margin, page_height / 2 + margin / 2),  # Top-left
        (page_width / 2 + margin / 2,
         page_height / 2 + margin / 2),  # Top-right
        (margin, margin + 50),  # Bottom-left (moved up)
        (page_width / 2 + margin / 2,
         margin + 50),  # Bottom-right (moved up)
    ]

    c = canvas.Canvas(output_pdf, pagesize=letter)
    for position, (sol_title, sol_grid, sol_highlights) in enumerate(
            solutions_chunk
    ):
        grid_size = len(sol_grid)
        cell_size = grid_area / grid_size
        pos_x, pos_y = grid_positions[position]

        pdf_render.draw_solution_grid_for_book(
            c, pos_x, pos_y, sol_grid, sol_highlights, cell_size, sol_title
        )
    
    # Add page number if provided
    if page_num is not None:
        draw_page_number(c, page_num)
    
    c.showPage()
    c.save()


if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file, json format")
    parser.add_argument("output", help="output folder")
    parser.add_argument(
        "-n",
        "--name",
        help="name of the output book (without extension)",
        default=None
    )
    parser.add_argument(
        "-c",
        "--copies",
        type=int,
        help="number of copies per puzzle (default: 4)",
        default=4
    )

    args = parser.parse_args()

    # Read input data
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    puzzle_name = data.get("title", os.path.splitext(os.path.basename(args.input))[0]).replace(" ", "_").lower()
    if args.name:
        puzzle_name = args.name
    args.output = os.path.join(args.output, f"{puzzle_name}_book.pdf")

    puzzles = []
    solutions = []
    base_puzzle_count = len(data["puzzles"])
    total_puzzle_count = base_puzzle_count * args.copies
    print(f"Generating book with {total_puzzle_count} puzzles ({base_puzzle_count} themes × {args.copies} variations)...")

    # Generate puzzles and solutions - create multiple variations for each theme
    for item in data["puzzles"]:
        size = item.get("size", 15)
        count = item.get("count", 20)
        base_title = item["title"]
        
        # Generate multiple variations of each puzzle
        for variation in range(1, args.copies + 1):
            # pick different random list of count words from item["words"]
            selected_words = random.sample(item["words"], count)
            puzzle = generate.generate_puzzle(
                base_title,
                selected_words,
                grid_size=size,
                use_basic=False,
                verbose=False,
            )

            if puzzle is None:
                continue
            
            # Add variation number to title
            numbered_title = f"{base_title} {variation}"
            puzzles.append((numbered_title, puzzle.grid, puzzle.words))
            solutions.append((numbered_title, puzzle.grid, puzzle.get_highlights()))

    print(f"Successfully generated {len(puzzles)} puzzles")

    # Use a temp directory for intermediate PDFs
    with tempfile.TemporaryDirectory() as tmpdir:
        merger = PdfMerger()

        # --- Create intro pages ---
        create_intro_pages(merger, tmpdir, puzzle_name, len(puzzles))
        
        # Track current page number (intro has 4 pages)
        current_page = 5

        # --- Puzzles: one per page ---
        for idx, (title, grid, words) in enumerate(puzzles):
            puzzle_pdf = os.path.join(tmpdir, f"puzzle_{idx}.pdf")
            pdf_render.render_wordsearch_pdf(
                puzzle_output=puzzle_pdf,
                title=title,
                grid=grid,
                word_list=words,
                highlights=None,
                solution_output=None,
                page_num=current_page,
            )
            merger.append(puzzle_pdf)
            current_page += 1

        # --- Solutions title page ---
        solutions_title_pdf = os.path.join(tmpdir, "solutions_title.pdf")
        create_solution_intro_pages(solutions_title_pdf, "Solutions")
        merger.append(solutions_title_pdf)
        current_page += 1  # Solutions title page

        # --- Solutions: 4 per page ---
        for i in range(0, len(solutions), 4):
            # fmt: off
            chunk = solutions[i:i + 4]
            # fmt: on
            solution_pdf = os.path.join(tmpdir, f"solution_{i//4}.pdf")
            create_solution_page(chunk, solution_pdf, page_num=current_page)
            merger.append(solution_pdf)
            current_page += 1

        # Write the merged PDF
        merger.write(args.output)
        merger.close()
        print(f"Book PDF generated: {args.output}")
