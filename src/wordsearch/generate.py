"""
Word search puzzle generator module.

This module provides the WordSearch class for generating word search puzzles
with configurable grid sizes and word placement strategies.
"""
import logging
import random
import string

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


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
            (1, 1),  # diagonal down-right
            (-1, -1),  # diagonal up-left
            (1, -1),  # diagonal down-left
            (-1, 1),  # diagonal up-right
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
        for solution in self.solution:
            print(f"\t{solution}")


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

    return wordsearch


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
    BASIC = True

    generate_puzzle(TITLE, WORDS, SIZE, BASIC, verbose=True)
