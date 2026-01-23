# 🚆📚 Fantastic Train - Wordsearch Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python library for generating professional wordsearch puzzles and puzzle books. Perfect for creating educational materials, activity books, or recreational puzzle collections.

## ✨ Features

- [x] 🎯 **Customizable Grid Sizes** - Generate puzzles from small (8x8) to large (30x30) grids
- [x] 📝 **Flexible Word Lists** - Import words from JSON files or provide them programmatically
- [x] 🎨 **Multiple Difficulty Levels** - Control word placement directions (8-directional or basic 3-directional)
- [x] 📚 **Batch Generation** - Create multiple puzzles for complete puzzle books
- [x] 🖨️ **Export Formats** - Output puzzles to PDF and DOCX formats
- [x] 📖 **Complete Book Generation** - Generate full PDF books with cover pages, intro pages, and solutions
- [x] 🎲 **Randomization** - Generate unique puzzles from the same word list
- [x] ✅ **Solution Keys** - Automatically generate answer keys with highlighted words
- [x] 📦 **Pre-made Collections** - Includes ready-to-use word lists (Animals, Travel, Food, Jobs)
- [ ] 🌟 **Future Formats** - PNG/SVG export (planned)

## 🚀 Installation

### From Source

Clone the repository:

```bash
git clone https://github.com/runarion/fantastic-train-wordsearch-generator.git
cd fantastic-train-wordsearch-generator
```

Install the package with dependencies:

```bash
pip install -e .
```

### Requirements

- Python 3.8 or higher
- Dependencies:
  - `python-docx>=1.2.0` - DOCX export
  - `reportlab>=4.4.5` - PDF generation
  - `PyPDF2>=3.0.1` - PDF manipulation
- Development dependencies (optional):
  - `pytest>=9.0.0` - Testing
  - `pylint>=4.0.0` - Code linting
  - `black>=25.0.0` - Code formatting
  - `isort>=7.0.0` - Import sorting
  - `flake8>=7.3.0` - Style checking

Install with development dependencies:

```bash
pip install -e ".[dev]"
```

## 📖 Usage

The project includes three main scripts for different use cases:

### 1. Generate Single Page Puzzles

Generate individual puzzle pages with solutions.

```bash
python -m scripts.generate_ws_page data/input_page.json -o output/ --pdf
```

**Options:**
- `-o, --output` - Output folder for generated files (required for PDF/DOCX)
- `--pdf` - Generate PDF output
- `--docx` - Generate DOCX output
- `-b, --basic` - Use basic directions only (horizontal left-to-right, vertical top-to-bottom, diagonal top-left to bottom-right)

**Input JSON Format:**

```json
{
    "puzzles": [
        {
            "title": "Animals",
            "words": ["ELEPHANT", "GIRAFFE", "KANGAROO"],
            "size": 18
        }
    ]
}
```

Sample file: [`data/input_page.json`](data/input_page.json)

### 2. Generate Complete Puzzle Books

Generate a complete PDF book with title page, puzzles, and solutions section.

```bash
python -m scripts.generate_ws_book data/input_book.json -o output/book.pdf
```

**Options:**
- `-o, --output` - Output PDF file path (required)
- `-b, --basic` - Use basic directions only
- `--no-cover` - Skip cover page generation

**Input Format:** Same as single page, with a book `title` at the root level.

Sample file: [`data/input_book.json`](data/input_book.json)

### 3. Generate Large Puzzle Books with Variations

Generate a large puzzle book with multiple variations of each puzzle theme.

```bash
python -m scripts.generate_big_ws_book data/books/01_animals_20_lists.json -o output/big_book.pdf -n 4
```

**Options:**
- `-o, --output` - Output PDF file path (required)
- `-n, --num-variations` - Number of variations per puzzle (default: 4)
- `-b, --basic` - Use basic directions only
- `--no-cover` - Skip cover page generation

**Input Format:** Each puzzle includes a `count` field specifying how many words to use per variation.

**Pre-made Books:**
- [`data/books/01_animals_20_lists.json`](data/books/01_animals_20_lists.json) - 20 animal-themed puzzles
- [`data/books/02_travel&cities_20_lists.json`](data/books/02_travel&cities_20_lists.json) - 20 travel and cities puzzles
- [`data/books/03_food&drinks_20_lists.json`](data/books/03_food&drinks_20_lists.json) - 20 food and drinks puzzles
- [`data/books/04_jobs&professions_20_lists.json`](data/books/04_jobs&professions_20_lists.json) - 20 jobs and professions puzzles

### Validation

Validate your JSON puzzle files before generation:

```bash
python -m scripts.validate_books data/books/
```

## 🏗️ Project Structure

```txt
fantastic-train-wordsearch-generator/
├── data/                       # Input data files
│   ├── input_page.json        # Sample single page input
│   ├── input_book.json        # Sample book input
│   └── books/                 # Pre-made puzzle collections
│       ├── 01_animals_20_lists.json
│       ├── 02_travel&cities_20_lists.json
│       ├── 03_food&drinks_20_lists.json
│       └── 04_jobs&professions_20_lists.json
├── scripts/                   # Executable scripts
│   ├── generate_ws_page.py   # Single page generator
│   ├── generate_ws_book.py   # Book generator
│   ├── generate_big_ws_book.py # Large book with variations
│   └── validate_books.py     # JSON validation tool
├── src/                       # Source code
│   ├── wordsearch/           # Core puzzle generation
│   │   ├── generate.py       # Puzzle generation algorithm
│   │   ├── pdf_render.py     # PDF rendering
│   │   ├── docx_export.py    # DOCX export
│   │   └── cover_image.py    # Cover page generation
│   └── intro/                # Book intro pages
│       └── pages.py          # Intro page templates
├── tests/                     # Unit tests
│   ├── test_basic.py
│   ├── test_generate.py
│   └── test_pdf_render.py
├── docs/                      # Documentation
├── releases/                  # Generated release files
├── pyproject.toml            # Project configuration
├── LICENSE                   # Apache 2.0 license
└── README.md                 # This file
```

## 🧪 Running Tests

Run all tests:

```bash
pytest tests/
```

Run specific test files:

```bash
pytest tests/test_generate.py
pytest tests/test_pdf_render.py
```

Run tests with verbose output:

```bash
pytest tests/ -v
```

## 📋 Roadmap

- [x] PDF generation with customizable styling
- [x] DOCX export functionality
- [x] Complete book generation with cover pages
- [x] Multiple puzzle variations from same word list
- [x] Pre-made word list collections (Animals, Travel, Food, Jobs)
- [x] Solution highlighting in PDF/DOCX
- [ ] PNG/SVG export functionality
- [ ] Theme support (colors, fonts, borders)
- [ ] Multi-language support
- [ ] Web API interface
- [ ] GUI application
- [ ] Interactive puzzle solving mode

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Runarion**

- GitHub: [@runarion](https://github.com/runarion)

## 🙏 Acknowledgments

- Inspired by classic wordsearch puzzle books
- Built with Python and ReportLab for professional PDF generation
- Special thanks to all contributors

## 📚 Example Output

The generator creates professional-quality puzzle books with:
- Custom cover pages with title and imagery
- Introduction pages explaining puzzle rules
- One puzzle per page with word lists
- Dedicated solutions section with highlighted answers
- Page numbering throughout
- Consistent formatting and styling

---

Made with ❤️ for puzzle enthusiasts everywhere!
