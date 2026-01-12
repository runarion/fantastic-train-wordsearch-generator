"""Cover image generation for wordsearch puzzles.
This module provides functionality to render word search puzzles
with the first 3 words highlighted as PNG images suitable for book covers.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

from wordsearch import direction_to_delta, HighlightStyle


# pylint: disable=too-many-arguments,too-many-locals,too-many-statements
def render_wordsearch_cover(
    output_path,
    grid,
    highlights=None,
    highlight_style=HighlightStyle.RECT,
    image_size=(1200, 1200),
    background_color=(255, 255, 255),
    grid_color=(0, 0, 0),
    # set the color to #E1AD01
    highlight_color=(225, 173, 1),
    max_highlights=4,
):
    """
    Render a wordsearch puzzle with highlighted words as a PNG cover image.

    Args:
        output_path (str): File path to save the PNG image.
        grid (list of list of str): The letter grid.
        highlights (list of dict): Optional. Each dict: {'word',
            'start', 'direction', 'length'}. Only the first
            max_highlights words will be shown.
        highlight_style (HighlightStyle): Style for highlighting
            solution words. HighlightStyle.RECT for rectangle outline,
            HighlightStyle.FILL for filled background.
        image_size (tuple): Size of the output image (width, height).
        background_color (tuple): RGB color for background.
        grid_color (tuple): RGB color for grid letters and border.
        highlight_color (tuple): RGB color for highlights.
        max_highlights (int): Maximum number of words to highlight
            (default: 3).
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Create image
    img_width, img_height = image_size
    img = Image.new("RGB", (img_width, img_height), background_color)
    draw = ImageDraw.Draw(img, "RGBA")

    # Calculate grid dimensions
    grid_size = len(grid)
    margin = int(min(img_width, img_height) * 0.1)  # 10% margin
    available_size = min(img_width, img_height) - 2 * margin
    cell_size = available_size / grid_size
    grid_width = cell_size * grid_size
    grid_height = cell_size * grid_size

    # Center the grid
    start_x = (img_width - grid_width) / 2
    start_y = (img_height - grid_height) / 2

    # Draw highlights first (so they appear behind the letters)
    if highlights:
        # Limit to first max_highlights words
        limited_highlights = highlights[:max_highlights]

        for h in limited_highlights:
            start_r, start_c = h["start"]
            dr, dc = direction_to_delta(h["direction"])
            length = h["length"]

            if highlight_style == HighlightStyle.RECT:
                _draw_rect_highlight(
                    draw,
                    start_x,
                    start_y,
                    cell_size,
                    start_r,
                    start_c,
                    dr,
                    dc,
                    length,
                    highlight_color,
                )
            elif highlight_style == HighlightStyle.FILL:
                _draw_fill_highlight(
                    draw,
                    start_x,
                    start_y,
                    cell_size,
                    start_r,
                    start_c,
                    dr,
                    dc,
                    length,
                    highlight_color,
                )

    # Draw outer border
    border_width = max(2, int(cell_size * 0.05))
    draw.rectangle(
        [start_x, start_y, start_x + grid_width, start_y + grid_height],
        outline=grid_color,
        width=border_width,
    )

    # Draw letters
    font_size = int(cell_size * 0.6)
    try:
        # Try to use a bold font
        font = ImageFont.truetype(
            "/System/Library/Fonts/Helvetica.ttc", font_size
        )
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default()

    for r, row in enumerate(grid):
        for c, cell_letter in enumerate(row):
            x = start_x + c * cell_size + cell_size / 2
            y = start_y + r * cell_size + cell_size / 2
            text = cell_letter.upper()

            # Center text using textbbox
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            draw.text(
                (x - text_width / 2, y - text_height / 2),
                text,
                fill=grid_color,
                font=font,
            )

    # Crop the image to just the grid area
    crop_box = (
        int(start_x),
        int(start_y),
        int(start_x + grid_width),
        int(start_y + grid_height),
    )
    img = img.crop(crop_box)

    # Save the image
    img.save(output_path, "PNG")


def _draw_rect_highlight(
    draw, start_x, start_y, cell_size, start_r, start_c, dr, dc, length, color
):
    """
    Draw a rectangular highlight around a word.

    Args:
        draw: PIL ImageDraw object.
        start_x (float): X position of the grid.
        start_y (float): Y position of the grid.
        cell_size (float): Size of each cell.
        start_r (int): Starting row of the word.
        start_c (int): Starting column of the word.
        dr (int): Row direction delta.
        dc (int): Column direction delta.
        length (int): Length of the word.
        color (tuple): RGB color for the highlight.
    """
    rect_width_factor = 0.6

    # Compute rectangle parameters
    if dr == 0:  # Horizontal
        rect_width = cell_size * length
        rect_height = cell_size * rect_width_factor
        angle = 0
    elif dc == 0:  # Vertical
        rect_width = cell_size * rect_width_factor
        rect_height = cell_size * length
        angle = 0
    else:  # Diagonal
        rect_width = (cell_size * length * 1.42) - (cell_size * 0.4)
        rect_height = cell_size * rect_width_factor
        # Angle in degrees: atan2(dr, dc)
        angle = math.degrees(math.atan2(dr, dc))

    # Center of the rectangle (middle of the word)
    mid_r = start_r + dr * (length - 1) / 2
    mid_c = start_c + dc * (length - 1) / 2
    center_x = start_x + (mid_c + 0.5) * cell_size
    center_y = start_y + (mid_r + 0.5) * cell_size

    # Create a rotated rectangle with rounded corners
    radius = int(cell_size * 0.35)
    line_width = max(3, int(cell_size * 0.08))

    if abs(angle) < 0.1:  # No rotation needed
        draw.rounded_rectangle(
            [
                center_x - rect_width / 2,
                center_y - rect_height / 2,
                center_x + rect_width / 2,
                center_y + rect_height / 2,
            ],
            radius=radius,
            outline=color,
            width=line_width,
        )
    else:
        # For rotated rectangles, create a temporary image and rotate it
        # Calculate the size needed for the temporary image (with
        # padding for rotation)
        max_dim = int(max(rect_width, rect_height) * 1.5)
        temp_img = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)

        # Draw rounded rectangle in the center of temp image
        temp_center = max_dim / 2
        temp_draw.rounded_rectangle(
            [
                temp_center - rect_width / 2,
                temp_center - rect_height / 2,
                temp_center + rect_width / 2,
                temp_center + rect_height / 2,
            ],
            radius=radius,
            outline=color + (255,),  # Add alpha channel
            width=line_width,
        )

        # Rotate the temporary image
        rotated_img = temp_img.rotate(
            -angle, expand=False, resample=Image.BICUBIC
        )

        # Paste the rotated image onto the main image
        paste_x = int(center_x - max_dim / 2)
        paste_y = int(center_y - max_dim / 2)

        # Get the original image from the draw object
        base_img = draw._image
        base_img.paste(rotated_img, (paste_x, paste_y), rotated_img)


def _draw_fill_highlight(
    draw, start_x, start_y, cell_size, start_r, start_c, dr, dc, length, color
):
    """
    Draw a filled highlight for each letter of a word.

    Args:
        draw: PIL ImageDraw object.
        start_x (float): X position of the grid.
        start_y (float): Y position of the grid.
        cell_size (float): Size of each cell.
        start_r (int): Starting row of the word.
        start_c (int): Starting column of the word.
        dr (int): Row direction delta.
        dc (int): Column direction delta.
        length (int): Length of the word.
        color (tuple): RGB color for the highlight.
    """
    # Add alpha channel for transparency
    fill_color = color + (76,)  # ~30% opacity (76/255)

    for i in range(length):
        rr = start_r + dr * i
        cc = start_c + dc * i
        lx = start_x + cc * cell_size
        ly = start_y + rr * cell_size
        draw.rectangle(
            [lx, ly, lx + cell_size, ly + cell_size],
            fill=fill_color,
        )


if __name__ == "__main__":
    # Example usage
    EXAMPLE_TITLE = "Sample Wordsearch: Colors"
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
            os.path.dirname(__file__), "..", "..", "out", "cover_image.png"
        )
    )

    render_wordsearch_cover(
        output_path=example_puzzle_output,
        grid=example_wordsearch_result["grid"],
        highlights=example_highlights,
        highlight_style=HighlightStyle.RECT,
    )
