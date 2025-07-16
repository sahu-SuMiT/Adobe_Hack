# PDF Outline Extractor

This solution extracts structured outlines from PDF documents, identifying the title and headings (H1-H6) along with their page numbers.

## Features

- Processes PDF files up to 50 pages
- Extracts document title and hierarchical headings (up to 6 levels deep)
- Outputs structured JSON format
- Works completely offline (no internet required)
- Runs efficiently on CPU (no GPU needed)
- Supports multilingual documents (including Japanese)
- Optimized for 8-core CPU systems
- Modular architecture for easy extension and customization
- Advanced pattern-based hierarchy detection for various heading formats
- Contextual heading level validation and correction

## Output Format

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "First Heading", "page": 1 },
    { "level": "H2", "text": "Subheading", "page": 2 },
    { "level": "H3", "text": "Sub-subheading", "page": 3 },
    { "level": "H4", "text": "Deep Heading", "page": 4 },
    { "level": "H5", "text": "Deeper Heading", "page": 5 },
    { "level": "H6", "text": "Deepest Heading", "page": 6 }
  ]
}
```

## Project Structure

```
pdf_outline_extractor/     # Main package
├── core/                  # Core components
│   ├── font_analyzer.py   # Font analysis
│   ├── text_cleaner.py    # Text cleaning
│   ├── heading_detector.py # Heading detection
│   ├── hierarchy_validator.py # Heading hierarchy validation
│   └── page_processor.py  # PDF page processing
└── extractors/            # Extraction strategies
    ├── base.py            # Base extractor interface
    ├── standard.py        # Standard extraction
    ├── fast.py            # Fast extraction for large docs
    └── main.py            # Main entry point

docs/                      # Documentation
tests/                     # Test files
```

## How to Run

### Building the Docker Image

```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

### Running the Container

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor:latest
```

Place your PDF files in the `input` directory, and the corresponding JSON files will be generated in the `output` directory.

## Installation

### Using Docker (Recommended)

See the "How to Run" section above.

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-outline-extractor.git
cd pdf-outline-extractor

# Install the package
pip install -e .
```

## Using as a Library

You can use the extractor as a library in your own Python code:

```python
from pdf_outline_extractor import PDFOutlineExtractor

# Create the extractor
extractor = PDFOutlineExtractor()

# Extract outline from a PDF file
outline = extractor.extract_outline("path/to/your/document.pdf")

# Access the extracted information
title = outline["title"]
headings = outline["outline"]

# Process the headings
for heading in headings:
    level = heading["level"]  # H1-H6
    text = heading["text"]    # Heading text
    page = heading["page"]    # Page number
    print(f"{level} - {text} (page {page})")
```

For more advanced usage, see the `example_usage.py` file.

## Heading Detection

The extractor uses two complementary approaches to identify headings:

1. **Pattern-based Detection**: Recognizes common heading numbering patterns
   - X. format (like "1.", "2.") → H1
   - X.Y format (like "1.1", "4.2") → H2
   - X.Y.Z format (like "1.1.1", "4.1.2") → H3
   - X.Y.Z.W format (like "1.1.1.1") → H4
   - X.Y.Z.W.V format (like "1.1.1.1.1") → H5
   - X.Y.Z.W.V.U format (like "1.1.1.1.1.1") → H6
   - Roman numerals (like "I.", "II.") → H1
   - Alphabetic markers (like "A.", "B.") → H2
   - Letter+number (like "A1.", "B2.") → H3
   - Bullet points (•, ■, etc.) → H2
   - Dashes (-, –, —) → H3
   - Parenthesized (like "(1)", "(A)") → H2
   - Bracketed (like "[1]", "[2]") → H2
   - Lowercase letters with parenthesis (like "a)", "b)") → H5
   - Lowercase roman numerals (like "i)", "ii)") → H6
   - Asterisks (*) → H5

2. **Font-based Detection**: Analyzes font sizes and styles
   - Larger fonts → Higher heading levels
   - Bold text → Likely a heading
   - Relative size compared to document median
   - Position on page (top of page more likely to be headings)

3. **Contextual Validation**: Ensures logical heading structure
   - Validates heading hierarchy to avoid skipped levels
   - Uses document context to correct inconsistent formatting
   - Applies pattern-specific fixes for common issues

This advanced hybrid approach ensures accurate heading detection even in documents with complex structure and inconsistent formatting.

## Technical Details

- Uses pdfplumber for PDF parsing
- Uses font size analysis and formatting cues to identify headings
- Optimized for performance (<10 seconds for a 50-page PDF)
- Total solution size <200MB
- Parallel processing for faster extraction on multi-core systems
- Handles various numbering systems (Western and Asian)
- Intelligent heading hierarchy validation

## Testing

You can test the solution locally by running:

```bash
# Run the main script
python main.py /path/to/input/dir /path/to/output/dir

# Run the unit tests
python -m tests.test_extract_outline

# Try the example usage
python example_usage.py
```

## Documentation

Additional documentation can be found in the `docs/` directory:

- `TECHNICAL.md` - Detailed technical documentation
- `TROUBLESHOOTING.md` - Troubleshooting guide
- `BENCHMARK.md` - Performance benchmarks
- `TESTING.md` - Testing guide