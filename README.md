# 🚆📚 Fantastic Train - Wordsearch Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python library for generating professional wordsearch puzzles and puzzle books. Perfect for creating educational materials, activity books, or recreational puzzle collections.

## ✨ Features

- [x] 🎯 **Customizable Grid Sizes** - Generate puzzles from small (10x10) to large (30x30) grids
- [x] 📝 **Flexible Word Lists** - Import words from files or provide them programmatically
- [ ] 🎨 **Multiple Difficulty Levels** - Control word placement directions and patterns
- [x] 📚 **Batch Generation** - Create multiple puzzles for complete puzzle books
- [x] 🖨️ **Basic Export** - Output the puzzles to DOCX
- [ ] 🖨️ **Export Formats** - Output to various formats (DOCX, PDF, PNG, SVG)
- [ ] 🔀 **Smart Word Placement** - Intelligent algorithm ensures optimal word distribution
- [x] 🎲 **Randomization** - Generate unique puzzles from the same word list
- [x] ✅ **Solution Keys** - Automatically generate answer keys

## 🚀 Installation

### From Source

Clone the repository:

```bash
git clone https://github.com/runarion/fantastic-train-wordsearch-generator.git
cd fantastic-train-wordsearch-generator
```

Install in development mode with all dependencies:

```bash
pip install -e ".[dev,docx]"
```

Or install just the base package:

```bash
pip install -e .
```

### Requirements

- Python 3.8 or higher
- Dependencies are managed through `pyproject.toml`

## 📖 Usage

### Basic Example

To generate a wordsearch puzzle using an input JSON file, run the following command:

```bash
python -m scripts.generate_wordsearch data/input.json
```

### Input JSON Format

The input file should follow this structure:

```json
{
    "puzzles": [
        {
            "title": "Animals",
            "words": [
                "ELEPHANT",
                "GIRAFFE",
                "KANGAROO"
            ],
            "size": 15
        }
    ]
}
```

**Fields:**

- `title` (required): Name of the puzzle
- `words` (required): Array of words to place in the puzzle
- `size` (optional): Grid size (default: 15)

A sample file is provided in `data/input.json`.

### Advanced Usage

Use the `--basic` flag to restrict word placement to simpler directions only (horizontal left-to-right, vertical top-to-bottom, and diagonal top-left to bottom-right):

```bash
python -m scripts.generate_wordsearch data/input.json --basic
```

Without the `--basic` flag, words can be placed in all 8 directions including backwards and reverse diagonals.

### Output

The generated puzzles will be displayed in the console output, showing:

- The puzzle grid with letters
- The solution coordinates for each word
- Any words that couldn't be placed (if grid is too small)

### Configuration Options

To see the option run the command:

```bash
python -m scripts.generate_wordsearch --help 
```

## 🏗️ Project Structure

```txt
data/               # Sample input files
scripts/            # Script to generate wordsearch puzzles
src/wordsearch/     # Main package code
tests/              # Unit tests
docs/               # Documentation
LICENSE             # Apache 2.0 license
README.md           # This file
```

## 🧪 Running Tests

```bash
pytest tests/
```

## 📋 Roadmap

- [ ] PDF generation with customizable styling
- [ ] PNG/SVG export functionality
- [ ] Theme support (colors, fonts, borders)
- [ ] Multi-language support
- [ ] Web API interface
- [ ] GUI application
- [ ] Pre-made word list collections

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
- Built with Python and love for puzzles

---

Made with ❤️ for puzzle enthusiasts everywhere!
