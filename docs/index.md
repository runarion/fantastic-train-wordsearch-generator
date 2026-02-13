# 🚆📚 Fantastic Train - Wordsearch Generator Documentation

> 🚧 **Work in Progress** - This project is under active development. Documentation will be expanded as features are implemented.

Welcome to the comprehensive documentation for the Fantastic Train Wordsearch Generator! This tool helps you create professional wordsearch puzzles and complete puzzle books with ease.

## 📑 Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [CLI Reference](#cli-reference)
- [Advanced Features](#advanced-features)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)

---

## Overview

The Fantastic Train Wordsearch Generator is a Python library and CLI tool for generating high-quality wordsearch puzzles and complete puzzle books. It is ideal for educators, publishers, and puzzle enthusiasts who want to create professional, customizable wordsearch content.

### Key Capabilities

- Generate wordsearch puzzles with customizable grid sizes (8x8 to 30x30)
- Import word lists from JSON files or provide them programmatically
- Batch-generate puzzles for books or collections
- Export puzzles and solutions to PDF and DOCX formats
- Create full puzzle books with cover, intro, puzzles, and solutions
- Randomize puzzle layouts for unique variations
- Use pre-made word list collections (Animals, Travel, Food, etc.)

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

#### Install from Source

```bash
# Clone the repository
git clone https://github.com/runarion/fantastic-train-wordsearch-generator.git
cd fantastic-train-wordsearch-generator
```

### Quick Start
Generate a sample puzzle page as PDF:

```bash
python -m scripts.generate_ws_page data/input_page.json -o output/ --pdf
```

Find your generated PDF in the `output/` folder.

---

## Basic Usage

### Creating a Simple Puzzle
To generate a single puzzle page with solutions:

```bash
python -m scripts.generate_ws_page data/input_page.json -o output/ --pdf
```

To generate a complete puzzle book:

```bash
python -m scripts.generate_ws_book data/input_book.json -o output/book.pdf --pdf
```

To generate a large book with multiple variations:

```bash
python -m scripts.generate_big_ws_book data/books/01_animals_20_lists.json -o output/big_book.pdf -n 4 --pdf
```

See the [README.md](../README.md) for more details and sample input files.

---

## CLI Reference

### Command Line Options

### generate_ws_page

Generate a single puzzle page:

```bash
python -m scripts.generate_ws_page <input_json> -o <output_folder> [--pdf] [--docx] [--basic]
```

- `<input_json>`: Path to input JSON file (see below for format)
- `-o, --output`: Output folder for generated files
- `--pdf`: Generate PDF output
- `--docx`: Generate DOCX output
- `--basic`: Use basic directions only (horizontal, vertical, diagonal)

### generate_ws_book

Generate a complete puzzle book:

```bash
python -m scripts.generate_ws_book <input_json> -o <output_file> [--pdf] [--docx] [-n <name>]
```

- `<input_json>`: Path to input JSON file (see below for format)
- `-o, --output`: Output PDF/DOCX file path
- `-n, --name`: Name of the output book (optional)

### generate_big_ws_book

Generate a large puzzle book with variations:

```bash
python -m scripts.generate_big_ws_book <input_json> -o <output_file> -n <copies> [--pdf] [--input-type <type>] [--html-description]
```

- `<input_json>`: Path to input JSON file (see below for format)
- `-o, --output`: Output PDF file path
- `-n, --name`: Name of the output book
- `-c, --copies`: Number of copies per puzzle (default: 4)
- `-t, --input-type`: 'wordlist' (default) or 'puzzles'
- `-d, --html-description`: Generate HTML description (optional)

### Input JSON Format

#### For Single Page or Book

```json
{
	"title": "Animals Book", // Only for books
	"puzzles": [
		{
			"title": "Animals",
			"words": ["ELEPHANT", "GIRAFFE", "KANGAROO"],
			"size": 18
		}
	]
}
```

#### For Big Book (wordlist mode)

```json
[
	{
		"title": "Animals",
		"words": ["ELEPHANT", "GIRAFFE", "KANGAROO"],
		"size": 18
	},
	...
]
```

See [data/input_page.json](../data/input_page.json) and [data/input_book.json](../data/input_book.json) for examples.

---

## Advanced Features

### Difficulty Levels

... TBD

### Batch Generation

... TBD

### Custom Styling

... TBD

---

## FAQ

### How many words can I add to a puzzle?

... TBD

### Can I use phrases or words with spaces?

... TBD

---

## Troubleshooting

... TBD

---

## Additional Resources

- [GitHub Repository](https://github.com/runarion/fantastic-train-wordsearch-generator)
- [Issue Tracker](https://github.com/runarion/fantastic-train-wordsearch-generator/issues)
- [Contributing Guidelines](https://github.com/runarion/fantastic-train-wordsearch-generator/blob/main/CONTRIBUTING.md)

---

*Documentation last updated: November 21, 2025*