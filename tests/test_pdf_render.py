from wordsearch import pdf_render


def test_render_wordsearch_pdf(tmp_path):

    # Minimal grid and word list: names of people
    grid = [
        ["A", "L", "I", "C", "E", "X", "X", "F"],
        ["B", "I", "L", "L", "X", "V", "R", "C"],
        ["D", "X", "X", "X", "X", "A", "E", "A"],
        ["I", "X", "X", "X", "N", "C", "X", "R"],
        ["V", "D", "X", "K", "A", "X", "X", "L"],
        ["A", "X", "I", "R", "X", "X", "X", "X"],
        ["D", "X", "G", "E", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "H", "X", "X", "X"],
    ]
    words = [
        # names
        "Alice",
        "Bill",
        "Carl",
        "David",
        "Eve",
        "Frank",
        "Grace",
        "Heidi",
    ]
    # fmt: off
    # pylint: disable=line-too-long
    highlights = [
        {"word": "Alice", "start": (0, 0), "direction": "horizontal_left_to_right", "length": 5},
        {"word": "Bill" , "start": (1, 0), "direction": "horizontal_left_to_right", "length": 4},
        {"word": "Carl" , "start": (1, 7), "direction": "vertical_top_to_bottom", "length": 4},
        {"word": "David", "start": (6, 0), "direction": "vertical_bottom_to_top", "length": 5},
        {"word": "Eve"  , "start": (0, 4), "direction": "diagonal_top_left_to_bottom_right", "length": 3},
        {"word": "Frank", "start": (0, 7), "direction": "diagonal_top_right_to_bottom_left", "length": 5},
        {"word": "Grace", "start": (6, 2), "direction": "diagonal_bottom_left_to_top_right", "length": 5},
        {"word": "Heidi", "start": (7, 4), "direction": "diagonal_bottom_right_to_top_left", "length": 5},
    ]
    # fmt: on
    # pylint: enable=line-too-long

    puzzle_pdf = tmp_path / "test_wordsearch_puzzle.pdf"
    solution_pdf = tmp_path / "test_wordsearch_solution.pdf"
    combined_pdf = tmp_path / "test_wordsearch_combined.pdf"

    try:
        pdf_render.render_wordsearch_pdf(
            str(puzzle_pdf),
            "Test Puzzle",
            grid,
            words,
            highlights=highlights,
            solution_output=str(solution_pdf),
        )
        pdf_render.render_wordsearch_pdf(
            str(combined_pdf),
            "Test Puzzle",
            grid,
            words,
            highlights=highlights,
            solution_output=None,
        )
    except Exception as e:
        print(f"Error during PDF generation: {e}")
        raise

    assert puzzle_pdf.exists()
    assert solution_pdf.exists()
    assert combined_pdf.exists()

    # to see the generated files paths,
    # - uncomment the following lines
    # - and run pytest with option '-s'

    # print(f"Puzzle PDF: {puzzle_pdf}")
    # print(f"Solution PDF: {solution_pdf}")
    # print(f"Combined PDF: {combined_pdf}")
