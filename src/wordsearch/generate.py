"""
Word search puzzle generator module.

This module provides the WordSearch class for generating word search puzzles
with configurable grid sizes and word placement strategies.
"""

import logging
import random
import string
from enum import Enum, auto

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


class Direction(Enum):
    """Enumeration for word placement directions in the word search puzzle."""

    HORIZONTAL_LEFT_TO_RIGHT = auto()
    HORIZONTAL_RIGHT_TO_LEFT = auto()
    VERTICAL_TOP_TO_BOTTOM = auto()
    VERTICAL_BOTTOM_TO_TOP = auto()
    DIAGONAL_TOP_LEFT_TO_BOTTOM_RIGHT = auto()
    DIAGONAL_BOTTOM_LEFT_TO_TOP_RIGHT = auto()
    DIAGONAL_TOP_RIGHT_TO_BOTTOM_LEFT = auto()
    DIAGONAL_BOTTOM_RIGHT_TO_TOP_LEFT = auto()
    UNKNOWN = auto()


def parse_solution_entry(word, pos_str):
    """Parse a solution entry string into a structured dictionary.
    Args:
        word (str): The word being placed.
        pos_str (str): The position string in the format "row,col,dr,dc".
    Returns:
        dict: A dictionary with word, start position, direction, and length.
    """
    row, col, dr, dc = map(int, pos_str.split(","))
    # Infer direction as a string
    if dr == 0 and dc == 1:
        direction = Direction.HORIZONTAL_LEFT_TO_RIGHT
    elif dr == 0 and dc == -1:
        direction = Direction.HORIZONTAL_RIGHT_TO_LEFT
    elif dr == 1 and dc == 0:
        direction = Direction.VERTICAL_TOP_TO_BOTTOM
    elif dr == -1 and dc == 0:
        direction = Direction.VERTICAL_BOTTOM_TO_TOP
    elif dr == 1 and dc == 1:
        direction = Direction.DIAGONAL_TOP_LEFT_TO_BOTTOM_RIGHT
    elif dr == -1 and dc == 1:
        direction = Direction.DIAGONAL_BOTTOM_LEFT_TO_TOP_RIGHT
    elif dr == 1 and dc == -1:
        direction = Direction.DIAGONAL_TOP_RIGHT_TO_BOTTOM_LEFT
    elif dr == -1 and dc == -1:
        direction = Direction.DIAGONAL_BOTTOM_RIGHT_TO_TOP_LEFT
    else:
        direction = Direction.UNKNOWN
    return {
        "word": word,
        "start": (row, col),
        "direction": direction.name.lower(),
        "length": len(word),
    }


class WordSearch:
    """
    Generate a word search puzzle with words placed in various directions.

    Attributes:
        title (str): The title of the puzzle.
        words (list): List of words to place in the puzzle.
        size (int): The grid size (size x size).
        failed_words (list): Words that could not be placed in the grid.
        solution (list): List of word positions and directions.
        grid (list): 2D list representing the puzzle grid.
    """

    def __init__(self, puzzle_title, word_list, grid_size, use_basic=True):
        """
        Initialize a WordSearch puzzle.

        Args:
            puzzle_title (str): The title of the puzzle.
            word_list (list): List of words to place in the puzzle.
            grid_size (int): The size of the grid (grid_size x grid_size).
            use_basic (bool): If True, use only basic directions (horizontal,
                            vertical, diagonal). If False, allow all 8 directions.
        """
        self.title = puzzle_title
        self.words = word_list
        self.size = grid_size
        self.failed_words = []
        self.solution = []

        self.grid = self.create_grid()

        # Sort words by length (longest first)
        sorted_words = sorted(word_list, key=lambda w: -len(w.replace(" ", "")))

        # [TO-DO]: add a check for not alphebetical characters, e.g. "-" ...
        for word in sorted_words:
            word_clean = word.upper().replace(" ", "")
            placed = False
            if use_basic:
                placed = self.place_word_in_grid_basic(word_clean)
            else:
                placed = self.place_word_in_grid_advanced(word_clean)
            if not placed:
                # logging.warning("Could not place the word '%s' in puzzle '%s'.",
                #                word, self.title)
                self.failed_words.append(word)

        self.fill_empty_spaces(self.grid)

    def create_grid(self):
        """Create an empty grid filled with spaces."""
        return [[" " for _ in range(self.size)] for _ in range(self.size)]

    def place_word_in_grid_basic(self, word):
        """
        Place word using basic directions only.

        Args:
            word (str): The word to place in the grid.

        Returns:
            bool: True if word was placed successfully, False otherwise.
        """
        directions = [
            (0, 1),  # horizontal
            (1, 0),  # vertical
            (1, 1),  # diagonal
        ]
        return self._find_best_position(word, directions)

    def place_word_in_grid_advanced(self, word):
        """
        Place word using all 8 directions.

        Args:
            word (str): The word to place in the grid.

        Returns:
            bool: True if word was placed successfully, False otherwise.
        """
        directions = [
            (0, 1),  # horizontal left->right
            (0, -1),  # horizontal right->left
            (1, 0),  # vertical top->bottom
            (-1, 0),  # vertical bottom->top
            (1, 1),  # diagonal top-left->bottom-right
            (-1, -1),  # diagonal bottom-right->top-left
            (1, -1),  # diagonal bottom-left->top-right
            (-1, 1),  # diagonal top-right->bottom-left
        ]
        return self._find_best_position(word, directions)

    # pylint: disable=too-many-locals,too-many-branches,too-many-nested-blocks
    def _find_best_position(self, word, directions):
        """
        Find the best position to place a word in the grid.

        Tries to maximize overlap with existing letters while ensuring the word fits.

        Args:
            word (str): The word to place.
            directions (list): List of (row_delta, col_delta) tuples for directions.

        Returns:
            bool: True if word was placed successfully, False otherwise.
        """
        best_positions = []
        max_overlap = -1
        word_length = len(word)

        for dr, dc in directions:
            for row in range(self.size):
                for col in range(self.size):
                    # Check if word fits
                    end_row = row + dr * (word_length - 1)
                    end_col = col + dc * (word_length - 1)
                    if not (0 <= end_row < self.size and 0 <= end_col < self.size):
                        continue

                    overlap = 0
                    fits = True
                    for i in range(word_length):
                        r = row + dr * i
                        c = col + dc * i
                        cell = self.grid[r][c]
                        if cell in (" ", word[i]):
                            if cell == word[i]:
                                overlap += 1
                        else:
                            fits = False
                            break
                    if fits:
                        if overlap > max_overlap:
                            best_positions = [(row, col, dr, dc)]
                            max_overlap = overlap
                        elif overlap == max_overlap:
                            best_positions.append((row, col, dr, dc))

        if not best_positions:
            return False

        # Randomly choose among best positions
        row, col, dr, dc = random.choice(best_positions)
        solution = {word: f"{row},{col},{dr},{dc}"}
        self.solution.append(solution)
        for i in range(word_length):
            r = row + dr * i
            c = col + dc * i
            self.grid[r][c] = word[i]
        return True

    def fill_empty_spaces(self, grid):
        """Fill empty cells in the grid with random letters."""
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] == " ":
                    grid[row][col] = random.choice(string.ascii_uppercase)

    def show_grid(self, show_failed_words=True):
        """Print the puzzle grid to console."""
        print("\nGrid:")
        print(f"\t{self.title} - {self.size}x{self.size}")
        for row in self.grid:
            print("\t" + " ".join(row))

        if show_failed_words and self.failed_words:
            print("\nFailed words:")
            for word in self.failed_words:
                print(f"\t{word}")

    def show_solution(self):
        """Print the solution (word positions) to console."""
        print("\nSolution:")
        highlights = self.get_highlights()
        for entry in highlights:
            word = entry["word"]
            start = entry["start"]
            direction = entry["direction"]
            arrows = direction_to_arrow(direction)
            length = entry["length"]
            print(
                f"\tWord: {word}, Start: {start}, Direction: {arrows}, Length: {length}"
            )

    def get_highlights(self):
        """Return solution highlights in the expected format for PDF rendering."""
        highlights = []
        for entry in self.solution:
            for word, pos_str in entry.items():
                highlights.append(parse_solution_entry(word, pos_str))
        return highlights


def generate_puzzle(puzzle_title, word_list, grid_size, use_basic, verbose=False):
    """
    Generate a word search puzzle.

    Args:
        puzzle_title (str): The title of the puzzle.
        word_list (list): List of words to include in the puzzle.
        grid_size (int): The size of the grid (grid_size x grid_size).
        use_basic (bool): If True, use only basic directions.
        verbose (bool): If True, print the grid and solution to console.

    Returns:
        WordSearch: The generated word search puzzle object.
    """
    if verbose:
        logging.info(
            "Generating puzzle '%s' with size %dx%d", puzzle_title, grid_size, grid_size
        )
    try:
        wordsearch = WordSearch(puzzle_title, word_list, grid_size, use_basic)
    except ValueError as ve:
        logging.warning("Puzzle '%s' skipped: %s", puzzle_title, ve)
        wordsearch = None
    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error("Unexpected error creating puzzle '%s': %s", puzzle_title, e)
        wordsearch = None

    if verbose and wordsearch:
        wordsearch.show_grid()
        wordsearch.show_solution()

    if verbose:
        logging.info("Puzzle '%s' generation completed.\n", puzzle_title)

    return wordsearch


def direction_to_arrow(direction):
    """Map direction string to arrow character."""
    arrows = {
        "horizontal_left_to_right": "\u2192",  # →
        "horizontal_right_to_left": "\u2190",  # ←
        "vertical_top_to_bottom": "\u2193",  # ↓
        "vertical_bottom_to_top": "\u2191",  # ↑
        "diagonal_top_left_to_bottom_right": "\u2198",  # ↘
        "diagonal_bottom_right_to_top_left": "\u2196",  # ↖
        "diagonal_top_right_to_bottom_left": "\u2199",  # ↙
        "diagonal_bottom_left_to_top_right": "\u2197",  # ↗
    }
    return arrows.get(direction, "?")


if __name__ == "__main__":

    TITLE = "Fruits"
    WORDS = [
        "Apple",
        "banana",
        "CHERRY",
        "strawberry",
        "grape",
        "yellow watermellon",
        "Jack Fruit",
    ]
    SIZE = 12
    BASIC = False

    generate_puzzle(TITLE, WORDS, SIZE, BASIC, verbose=True)
