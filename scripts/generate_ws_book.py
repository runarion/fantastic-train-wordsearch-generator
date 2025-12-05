"""
Script to generate a complete word search book PDF from a set of puzzles.

This script reads a JSON file containing multiple word search puzzle
definitions, generates each puzzle and its solution, and compiles them into
a single PDF book with a title page, puzzle pages, and solution pages.
"""

import argparse
import json
import os
import tempfile

from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from wordsearch import generate
from wordsearch import pdf_render


def create_blank_page(output_pdf):
    """
    Creates a blank page PDF.
    """
    page_width, page_height = letter
    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.showPage()
    c.save()


def create_title_page(output_pdf, page_title):
    """
    Creates a title page PDF with the given title.
    """
    page_width, page_height = letter
    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.setFont("Helvetica-Bold", 36)

    upper_title = page_title.upper().replace("_", " ")
    c.drawCentredString(page_width / 2, page_height / 2, upper_title)
    c.showPage()
    c.save()


def create_solution_page(solutions_chunk, output_pdf):
    """
    Draws up to 4 solution grids on a single page and saves as PDF.
    """

    page_width, page_height = letter
    margin = 36
    grid_area = (page_width - 2 * margin) / 2  # 2 columns
    grid_positions = [
        (margin, page_height / 2 + margin / 2),  # Top-left
        (page_width / 2 + margin / 2, page_height / 2 + margin / 2),  # Top-right
        (margin, margin),  # Bottom-left
        (page_width / 2 + margin / 2, margin),  # Bottom-right
    ]

    c = canvas.Canvas(output_pdf, pagesize=letter)
    for position, (sol_title, sol_grid, sol_highlights) in enumerate(solutions_chunk):
        grid_size = len(sol_grid)
        cell_size = grid_area / grid_size
        pos_x, pos_y = grid_positions[position]

        pdf_render.draw_solution_grid_for_book(
            c, pos_x, pos_y, sol_grid, sol_highlights, cell_size, sol_title
        )
    c.showPage()
    c.save()


if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file, json format")
    parser.add_argument("output", help="output folder")
    parser.add_argument(
        "-n", "--name", help="name of the output book (without extension)", default=None
    )

    args = parser.parse_args()

    # Read input data
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    puzzle_name = os.path.splitext(os.path.basename(args.input))[0]
    if args.name:
        puzzle_name = args.name
    args.output = os.path.join(args.output, f"{puzzle_name}_book.pdf")
s
    puzzles = []
    solutions = []

    # Generate puzzles and solutions
    for item in data["puzzles"]:
        size = item.get("size", 15)
        puzzle = generate.generate_puzzle(
            item["title"],
            item["words"],
            grid_size=size,
            use_basic=False,
            verbose=False,
        )

        if puzzle is None:
            continue
        puzzles.append((item["title"], puzzle.grid, puzzle.words))
        solutions.append((item["title"], puzzle.grid, puzzle.get_highlights()))

        # Use a temp directory for intermediate PDFs
    with tempfile.TemporaryDirectory() as tmpdir:
        merger = PdfMerger()

        # --- Blank page ---
        blank_pdf = os.path.join(tmpdir, "blank.pdf")
        create_blank_page(blank_pdf)
        merger.append(blank_pdf)

        # --- Title page ---
        title_pdf = os.path.join(tmpdir, "title.pdf")
        create_title_page(title_pdf, puzzle_name)
        merger.append(title_pdf)

        # --- Another blank page ---
        merger.append(blank_pdf)

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
            )
            merger.append(puzzle_pdf)

        # --- Solutions title page ---
        solutions_title_pdf = os.path.join(tmpdir, "solutions_title.pdf")
        create_title_page(solutions_title_pdf, "Solutions")
        merger.append(solutions_title_pdf)

        # --- Solutions: 4 per page ---
        for i in range(0, len(solutions), 4):
            chunk = solutions[i : i + 4]
            solution_pdf = os.path.join(tmpdir, f"solution_{i//4}.pdf")
            create_solution_page(chunk, solution_pdf)
            merger.append(solution_pdf)

        # Write the merged PDF
        merger.write(args.output)
        merger.close()
        print(f"Book PDF generated: {args.output}")
