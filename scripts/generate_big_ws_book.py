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
from wordsearch import cover_image


def draw_page_number(c, page_num):
    """
    Draws a page number at the bottom center of a PDF page.

    Args:
        c: ReportLab canvas object
        page_num: Page number to display
    """
    page_width, page_height = letter
    c.setFont("Helvetica", 10)
    # 0.5 inch from bottom
    c.drawCentredString(page_width / 2, 0.5 * 72, str(page_num))


def create_solution_page(solutions_chunk, output_pdf, page_num=None):
    """
    Draws up to 4 solution grids on a single page and saves as PDF.
    """

    page_width, page_height = letter
    margin = 36
    # 2 columns, scaled down by 0.85 for more spacing
    grid_area = ((page_width - 2 * margin) / 2) * 0.85
    left_margin_offset = 30  # Additional left margin to center grids better
    vertical_offset = 40  # Move all grids up for better vertical centering
    grid_positions = [
        # Top-left
        (margin + left_margin_offset, page_height / 2 + margin / 2 + vertical_offset),
        # Top-right
        (page_width / 2 + margin / 2, page_height / 2 + margin / 2 + vertical_offset),
        # Bottom-left (moved up)
        (margin + left_margin_offset, margin + 50 + vertical_offset),
        (page_width / 2 + margin / 2, margin + 50 + vertical_offset),  # Bottom-right (moved up)
    ]

    c = canvas.Canvas(output_pdf, pagesize=letter)
    for position, (sol_title, sol_grid, sol_highlights) in enumerate(
        solutions_chunk
    ):
        grid_size = len(sol_grid)
        cell_size = grid_area / grid_size
        pos_x, pos_y = grid_positions[position]

        pdf_render.draw_solution_grid_for_book(
            c, pos_x, pos_y, sol_grid, sol_highlights, cell_size, sol_title, grey_highlights=True
        )

    # Add page number if provided
    if page_num is not None:
        draw_page_number(c, page_num)

    c.showPage()
    c.save()


def save_puzzle_data_to_json(
    puzzles,
    solutions,
    output_path,
    puzzle_name,
    cover_color,
    content_descriptions=None):
    """
    Saves the generated puzzles and solutions to a JSON file with metadata.
    """
    puzzle_data = {
        "metadata": {
            "title": puzzle_name,
            "color": cover_color
        },
        "puzzles": [],
        "solutions": []
    }

    for title, grid, words in puzzles:
        puzzle_data["puzzles"].append({
            "title": title,
            "grid": grid,
            "words": words
        })

    for title, grid, highlights in solutions:
        puzzle_data["solutions"].append({
            "title": title,
            "grid": grid,
            "highlights": highlights
        })

    if content_descriptions:
        puzzle_data["metadata"]["content_descriptions"] = content_descriptions
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(puzzle_data, f, indent=4)


def load_puzzle_data_from_json(input_path):
    """
    Loads previously generated puzzles and solutions from a JSON file.
    Returns: (puzzles, solutions, puzzle_name, cover_color)
    """
    with open(input_path, "r", encoding="utf-8") as f:
        puzzle_data = json.load(f)

    # Extract metadata
    metadata = puzzle_data.get("metadata", {})
    puzzle_name = metadata.get("title", "wordsearch_book")
    cover_color = metadata.get("color", "#1E90FF")

    # Reconstruct puzzles list
    puzzles = []
    for p in puzzle_data["puzzles"]:
        puzzles.append((p["title"], p["grid"], p["words"]))

    # Reconstruct solutions list
    solutions = []
    for s in puzzle_data["solutions"]:
        solutions.append((s["title"], s["grid"], s["highlights"]))

    return puzzles, solutions, puzzle_name, cover_color


if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file, json format")
    parser.add_argument("output", help="output folder")
    parser.add_argument(
        "-n",
        "--name",
        help="name of the output book (without extension)",
        default=None,
    )
    parser.add_argument(
        "-c",
        "--copies",
        type=int,
        help="number of copies per puzzle (default: 4)",
        default=4,
    )
    parser.add_argument(
        "-t",
        "--input-type",
        choices=["wordlist", "puzzles"],
        default="wordlist",
        help="type of input file: 'wordlist' for puzzle definitions (generates new puzzles), 'puzzles' for previously generated puzzle data (reuses puzzles)",
    )

    args = parser.parse_args()

    output_dir = args.output
    puzzles = []
    solutions = []
    cover_color = "#1E90FF"  # default blue
    content_descriptions = []

    if args.input_type == "puzzles":
        # Load previously generated puzzle data
        print(f"Loading puzzle data from {args.input}...")
        puzzles, solutions, puzzle_name, cover_color = load_puzzle_data_from_json(args.input)
        
        # Override puzzle name if specified
        if args.name:
            puzzle_name = args.name
        
        #get content descriptions from metadata if available
        with open(args.input, "r", encoding="utf-8") as f:
            puzzle_data = json.load(f)
            metadata = puzzle_data.get("metadata", {})
            content_descriptions = metadata.get("content_descriptions", [])
        
        print(f"Loaded {len(puzzles)} puzzles from data file")
    
    else:
        # Generate new puzzles from word lists (original behavior)
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)

        puzzle_name = (
            data.get("title", os.path.splitext(os.path.basename(args.input))[0])
            .replace(" ", "_")
            .lower()
        )
        if args.name:
            puzzle_name = args.name

        base_puzzle_count = len(data["puzzles"])
        total_puzzle_count = base_puzzle_count * args.copies
        print(
            f"Generating book with {total_puzzle_count} puzzles "
            f"({base_puzzle_count} themes × {args.copies} variations)..."
        )

        # Get cover color from the json, default to blue
        cover_color = data.get("color", "#1E90FF")

        # Generate puzzles and solutions - create multiple variations for
        # each theme
        for item in data["puzzles"]:
            size = item.get("size", 15)
            count = item.get("count", 20)
            base_title = item["title"]

            # Append the puzzle "title" to descriptions, only first 6 titles
            if len(content_descriptions) < 6:
                content_descriptions.append(base_title)

            # Generate multiple variations of each puzzle
            for variation in range(1, args.copies + 1):
                # pick different random list of count words from
                # item["words"]

            # if there are not enough words, just take all of them
                if len(item["words"]) <= count:
                    selected_words = item["words"]
                else:
                    selected_words = random.sample(item["words"], count)

                # if there are failed words, try to generate again 3 times
                puzzle = None
                for attempt in range(5):
                    puzzle = generate.generate_puzzle(
                        base_title,
                        selected_words,
                        grid_size=size,
                        use_basic=False,
                        verbose=False,
                    )
                    if not puzzle.failed_words:
                        if attempt > 0:
                            ordinal = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th'}[attempt + 1]
                            print(
                                f"Puzzle '{base_title} {variation}' generated at the {ordinal} attempt"
                            )
                        break  # success, exit retry loop

                # print failed_words if any
                if puzzle.failed_words:
                    print(
                        f"Warning: Could not place the following words "
                        f"in puzzle '{base_title} {variation}': "
                        f"{puzzle.failed_words}"
                    )
     
                if puzzle is None:
                    continue

                # Add variation number to title
                numbered_title = f"{base_title} {variation}"
                puzzles.append((numbered_title, puzzle.grid, puzzle.words))
                solutions.append(
                    (numbered_title, puzzle.grid, puzzle.get_highlights())
                )
       
        print(f"Successfully generated {len(puzzles)} puzzles")

        # Save JSON with puzzles and solutions
        save_puzzle_data_to_json(
            puzzles, solutions, 
            os.path.join(output_dir, f"{puzzle_name}_data.json"),
            puzzle_name,
            cover_color,
            content_descriptions
        )
        print(f"JSON saved: {os.path.join(output_dir, f'{puzzle_name}_data.json')}")

    pdf_output_path = os.path.join(output_dir, f"{puzzle_name}_book.pdf")

    # generate the cover image in the output folder only for the first puzzle
    cover_image_path = os.path.join(
        output_dir, f"{puzzle_name}_cover_grid.png"
    )
    
    cover_image.render_wordsearch_cover(
        output_path=cover_image_path,
        grid=puzzles[0][1],
        highlights=solutions[0][2],
        highlight_color=tuple(int(cover_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)),  # convert hex to RGB
    )
    print(f"Cover image generated: {cover_image_path}")

    # Use a temp directory for intermediate PDFs
    with tempfile.TemporaryDirectory() as tmpdir:
        merger = PdfMerger()

        # --- Create intro pages ---
        create_intro_pages(merger, tmpdir, puzzle_name, len(puzzles), about_content=content_descriptions)

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
                grey_highlights=True,
            )
            merger.append(puzzle_pdf)
            current_page += 1

        # --- Solutions title page ---
        solutions_title_pdf = os.path.join(
            tmpdir, "solutions_title.pdf"
        )
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
        merger.write(pdf_output_path)
        merger.close()
        print(f"Book PDF generated: {pdf_output_path}")
