"""PDF rendering for wordsearch puzzles.
This module provides functionality to render word search puzzles
and their solutions to PDF format using the ReportLab library.
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from wordsearch import direction_to_delta


# pylint: disable=too-many-arguments,too-many-locals,too-many-statements,too-many-positional-arguments
def render_wordsearch_pdf(
    puzzle_output,
    title,
    grid,
    word_list,
    highlights=None,
    solution_output=None,
):
    """
    Render a wordsearch puzzle and its solution to a PDF file.

    Args:
        puzzle_output (str): File to save the PDF.
        title (str): Puzzle title.
        grid (list of list of str): The letter grid.
        word_list (list of str): List of words.
        highlights (list of dict): Optional. Each dict: {'word', 'start',
            'direction', 'length'}. If None, no solution is drawn.
        solution_output (str): Optional. File to save the solution PDF.
            If None, solution is added as a second page in the puzzle PDF.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(puzzle_output), exist_ok=True)

    # Create the PDF document
    doc = SimpleDocTemplate(puzzle_output, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    # Title in uppercase and centered
    elements.append(Paragraph(title.upper(), styles["Title"]))
    elements.append(Spacer(1, 24))  # Increased space after title

    # Calculate grid size for spacer
    page_width, page_height = letter
    margin = 36
    grid_size = len(grid)
    available_width = (page_width - 2 * margin) * 0.8
    available_height = (page_height - 2 * margin - 100) * 0.8
    cell_size = min(available_width, available_height) / grid_size
    grid_height = cell_size * grid_size
    # Add enough space for the grid and a little extra
    elements.append(Spacer(1, grid_height + 48))

    # Prepare word list in multiple columns, uppercase
    num_columns = 3
    words_upper = [w.upper() for w in word_list]
    rows = (len(words_upper) + num_columns - 1) // num_columns
    word_table_data = []
    for i in range(rows):
        row = []
        for j in range(num_columns):
            idx = i + j * rows
            if idx < len(words_upper):
                row.append(words_upper[idx])
            else:
                row.append("")
        word_table_data.append(row)
    # Set column widths to spread the table across the page
    col_width = (page_width - 2 * margin) / num_columns
    word_table = Table(
        word_table_data, colWidths=[col_width] * num_columns, hAlign="CENTER"
    )
    word_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center text in each cell
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(word_table)

    # Custom grid drawing (fit to page, only outer border)
    def draw_grid(canvas, doc):  # pylint: disable=unused-argument
        page_width, page_height = letter
        margin = 36  # 0.5 inch
        grid_size = len(grid)
        available_width = (page_width - 2 * margin) * 0.8
        available_height = (page_height - 2 * margin - 100) * 0.8
        cell_size = min(available_width, available_height) / grid_size
        grid_width = cell_size * grid_size
        grid_height = cell_size * grid_size
        start_x = (page_width - grid_width) / 2
        start_y = page_height - margin - grid_height - 84  # leave space for title

        # Draw outer border
        canvas.setLineWidth(2)
        canvas.rect(start_x, start_y, grid_width, grid_height)

        # Draw letters
        canvas.setFont("Helvetica-Bold", int(cell_size * 0.6))
        for r, row in enumerate(grid):
            for c, cell_letter in enumerate(row):
                x = start_x + c * cell_size + cell_size / 2
                y = (
                    start_y
                    + (grid_size - r - 1) * cell_size
                    + cell_size / 2
                    - cell_size * 0.2
                )
                canvas.drawCentredString(x, y, cell_letter.upper())

    # --- Solution Page/PDF ---
    if highlights:
        # Custom drawing for solution grid with highlights
        def draw_solution_grid(canvas, doc):  # pylint: disable=unused-argument
            grid_size = len(grid)
            cell_size = 20
            margin_x = 72
            margin_y = 500 - grid_size * cell_size

            # Draw grid letters
            for r, row in enumerate(grid):
                for c, cell_letter in enumerate(row):
                    x = margin_x + c * cell_size
                    y = margin_y + (grid_size - r - 1) * cell_size
                    canvas.rect(x, y, cell_size, cell_size)
                    canvas.drawCentredString(
                        x + cell_size / 2, y + cell_size / 2 - 4, cell_letter
                    )

            # Draw highlights if provided
            if highlights:
                for h in highlights:
                    start_r, start_c = h["start"]
                    dr, dc = direction_to_delta(h["direction"])
                    for i in range(h["length"]):
                        rr = start_r + dr * i
                        cc = start_c + dc * i
                        x = margin_x + cc * cell_size
                        y = margin_y + (grid_size - rr - 1) * cell_size
                        canvas.setFillColorRGB(1, 1, 0, alpha=0.3)  # Yellow highlight
                        canvas.rect(x, y, cell_size, cell_size, fill=1, stroke=0)
                canvas.setFillColor(colors.black)  # Reset color

        if solution_output is None:
            # Add solution as a second page in the same PDF
            elements.append(PageBreak())
            elements.append(Paragraph(f"{title} - Solution", styles["Title"]))
            elements.append(Spacer(1, 200))  # Reserve space for the grid

            doc.build(elements, onFirstPage=draw_grid, onLaterPages=draw_solution_grid)
        else:
            # Create separate solution PDF
            doc.build(elements, onFirstPage=draw_grid)

            os.makedirs(os.path.dirname(solution_output), exist_ok=True)
            doc_sol = SimpleDocTemplate(solution_output, pagesize=letter)
            elements_sol = []
            elements_sol.append(Paragraph(f"{title} - Solution", styles["Title"]))
            elements_sol.append(Spacer(1, 200))  # Reserve space for the grid

            doc_sol.build(
                elements_sol,
                onFirstPage=draw_solution_grid,
            )
    else:
        # No solution, just build the puzzle
        doc.build(elements, onFirstPage=draw_grid)


if __name__ == "__main__":
    # Example usage
    example_title = "Sample Wordsearch: Colors"
    # fmt: off
    example_wordsearch_result = {
        "grid": [
            ["C", "R", "Y", "V", "C", "F", "U", "T", "S", "S", "B", "U"],
            ["C", "X", "P", "U", "M", "J", "Q", "I", "V", "L", "E", "F"],
            ["C", "J", "K", "C", "I", "B", "Y", "I", "U", "R", "Q", "Z"],
            ["W", "A", "R", "T", "X", "I", "O", "E", "F", "X", "C", "W"],
            ["Y", "W", "E", "I", "A", "L", "I", "G", "L", "A", "Y", "K"],
            ["X", "I", "G", "U", "E", "N", "O", "N", "I", "L", "W", "K"],
            ["W", "X", "V", "T", "P", "V", "P", "A", "B", "D", "O", "O"],
            ["M", "A", "Z", "U", "T", "K", "G", "R", "E", "E", "N", "W"],
            ["M", "I", "B", "Q", "K", "D", "C", "O", "E", "R", "L", "I"],
            ["A", "V", "H", "B", "S", "S", "V", "M", "X", "O", "W", "M"],
            ["L", "C", "M", "F", "K", "H", "Z", "O", "X", "M", "X", "P"],
            ["Q", "G", "A", "H", "M", "G", "B", "G", "S", "R", "Z", "E"],
        ],
        "words": ["ORANGE", "YELLOW", "INDIGO", "VIOLET", "GREEN", "BLUE"],
    }
    # fmt: on

    example_highlights = [
        {
            "word": "ORANGE",
            "start": (8, 7),
            "direction": "vertical_bottom_to_top",
            "length": 6,
        },
        {
            "word": "YELLOW",
            "start": (2, 6),
            "direction": "diagonal_top_left_to_bottom_right",
            "length": 6,
        },
        {
            "word": "INDIGO",
            "start": (8, 11),
            "direction": "diagonal_bottom_right_to_top_left",
            "length": 6,
        },
        {
            "word": "VIOLET",
            "start": (1, 8),
            "direction": "diagonal_top_right_to_bottom_left",
            "length": 6,
        },
        {
            "word": "GREEN",
            "start": (7, 6),
            "direction": "horizontal_left_to_right",
            "length": 5,
        },
        {
            "word": "BLUE",
            "start": (0, 10),
            "direction": "diagonal_top_right_to_bottom_left",
            "length": 4,
        },
        {
            "word": "RED",
            "start": (8, 9),
            "direction": "vertical_bottom_to_top",
            "length": 3,
        },
    ]

    example_puzzle_output = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "out", "wordsearch_puzzle.pdf"
        )
    )
    example_solution_output = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "out", "wordsearch_solution.pdf"
        )
    )
    example_combined_output = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "out", "wordsearch_combined.pdf"
        )
    )

    # Example 1: Separate puzzle and solution PDFs
    render_wordsearch_pdf(
        puzzle_output=example_puzzle_output,
        title=example_title,
        grid=example_wordsearch_result["grid"],
        word_list=example_wordsearch_result["words"],
        highlights=example_highlights,
        solution_output=example_solution_output,  # Solution in different file
    )

    # Example 2: Combined puzzle and solution in one PDF
    render_wordsearch_pdf(
        puzzle_output=example_combined_output,
        title=example_title,
        grid=example_wordsearch_result["grid"],
        word_list=example_wordsearch_result["words"],
        highlights=example_highlights,
        solution_output=None,  # Solution in same file
    )
