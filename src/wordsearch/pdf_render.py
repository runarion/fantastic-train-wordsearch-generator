"""PDF rendering for wordsearch puzzles.
This module provides functionality to render word search puzzles
and their solutions to PDF format using the ReportLab library.
"""

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


def render_wordsearch_pdf(
    output_path,
    title,
    grid,
    word_list,
    highlights=None,
):
    """
    Render a wordsearch puzzle and its solution to a PDF file.

    Args:
        output_path (str): Path to save the PDF.
        title (str): Puzzle title.
        grid (list of list of str): The letter grid.
        word_list (list of str): List of words.
        highlights (list of dict): Optional. Each dict: {'word', 'start', 'direction', 'length'}
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # --- Puzzle Page ---
    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 12))

    # Render grid as a Table
    table_data = [list(row) for row in grid]
    table = Table(table_data)
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Word list
    elements.append(Paragraph("Words:", styles["Heading2"]))
    words_str = ", ".join(word_list)
    elements.append(Paragraph(words_str, styles["Normal"]))

    elements.append(PageBreak())

    # --- Solution Page ---
    elements.append(Paragraph(f"{title} - Solution", styles["Title"]))
    elements.append(Spacer(1, 12))

    # We'll draw the solution grid with highlights using a custom canvas
    # pylint: disable=too-many-locals
    def draw_solution_grid(canvas, _doc):
        # Calculate cell size and margins
        grid_size = len(grid)
        cell_size = 20
        margin_x = 72
        margin_y = 500 - grid_size * cell_size  # Adjust for page center

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

    # Add the solution grid as a custom drawing
    elements.append(Spacer(1, 200))  # Reserve space for the grid

    # Build the document with or without the custom solution page
    if highlights:
        doc.build(
            elements,
            onLaterPages=draw_solution_grid,
        )
    else:
        doc.build(elements)


def direction_to_delta(direction):
    """
    Map direction string to (dr, dc)
    """
    mapping = {
        "horizontal": (0, 1),
        "horizontal_rev": (0, -1),
        "vertical": (1, 0),
        "vertical_rev": (-1, 0),
        "diagonal_down": (1, 1),
        "diagonal_up": (-1, 1),
        "diagonal_down_rev": (1, -1),
        "diagonal_up_rev": (-1, -1),
    }
    return mapping.get(direction, (0, 1))
