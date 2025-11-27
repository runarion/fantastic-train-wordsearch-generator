"""Wordsearch package utilities."""


def direction_to_delta(direction):
    """
    Map direction string to (dr, dc)
    """
    mapping = {
        "horizontal_left_to_right": (0, 1),
        "horizontal_right_to_left": (0, -1),
        "vertical_top_to_bottom": (1, 0),
        "vertical_bottom_to_top": (-1, 0),
        "diagonal_top_left_to_bottom_right": (1, 1),
        "diagonal_bottom_left_to_top_right": (-1, 1),
        "diagonal_top_right_to_bottom_left": (1, -1),
        "diagonal_bottom_right_to_top_left": (-1, -1),
    }
    return mapping.get(direction, (0, 1))
