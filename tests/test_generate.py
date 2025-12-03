from wordsearch.generate import generate_puzzle


def test_generate_wordsearch():
    # Minimal test to generate a wordsearch and verify the solution
    title = "Test Puzzle"
    words = [
        "Alpha",
        "Bravo",
        "Charlie",
        "Delta",
        "Echo",
        "Foxtrot",
        "Golf",
        "Hotel",
        "VeryVeryLongWord",
    ]
    size = 12
    basic = False

    puzzle = generate_puzzle(title, words, size, basic, verbose=True)

    # remove the words that failed to be placed and convert to uppercase
    valid_words = [w.upper() for w in words if w not in puzzle.failed_words]

    # verify that all valid words are in the solution
    for word in valid_words:
        word_found = False
        # iterate through solutions to find this word
        for word_solution in puzzle.solution:
            if word not in word_solution:
                continue

            # split the solution entry into numbers
            data = word_solution[word]
            r, c, row_delta, col_delta = map(int, data.split(","))

            # verify each letter in the grid matches the word
            for char in word:
                if puzzle.grid[r][c] != char:
                    raise AssertionError(
                        f"Letter '{char}' of word '{word}' does not "
                        f"match grid at position ({r}, {c})"
                    )
                # move to the next letter position
                r += row_delta
                c += col_delta

            word_found = True
            break

        assert word_found, f"Word '{word}' not found in solution"
