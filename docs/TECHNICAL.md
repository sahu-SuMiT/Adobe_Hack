# Technical Documentation: PDF Outline Extractor

## Architecture Overview

The PDF Outline Extractor is designed to efficiently extract structured outlines from PDF documents using font analysis and formatting detection. The solution is containerized using Docker and optimized for performance on 8-core CPU systems.

## Modular Design

The solution follows a modular design pattern with clear separation of concerns:

### Component Architecture

```
PDFOutlineExtractor
    │
    ├── StandardOutlineExtractor
    │   ├── FontAnalyzer
    │   ├── TextCleaner
    │   ├── HeadingDetector
    │   └── PDFPageProcessor
    │
    └── FastOutlineExtractor
        ├── FontAnalyzer
        └── TextCleaner
```

Each module has a single responsibility:

- **PDFOutlineExtractor**: Main entry point that delegates to appropriate extractors
- **StandardOutlineExtractor**: Detailed extraction for normal-sized documents
- **FastOutlineExtractor**: Simplified extraction for large documents
- **FontAnalyzer**: Analyzes font properties like weight and style
- **TextCleaner**: Handles text normalization and cleaning
- **HeadingDetector**: Determines heading levels based on formatting
- **PDFPageProcessor**: Processes individual PDF pages

## Core Components

### 1. PDF Processing Engine

The core of the solution is built around `pdfplumber`, a Python library that provides detailed access to PDF content including text, fonts, and positioning information. This allows us to:

- Extract text with precise positioning
- Access font information (size, name, style)
- Process documents page by page

### 2. Heading Detection Algorithm

The heading detection algorithm uses multiple signals to identify headings:

#### Font Size Analysis
- Calculates median font size across the document
- Identifies headings based on relative size ratios:
  - Title: ≥ 1.5× median size
  - H1: ≥ 1.3× median size
  - H2: ≥ 1.15× median size
  - H3: ≥ 1.05× median size

#### Font Style Detection
- Identifies bold text through font name analysis
- Uses keywords like 'bold', 'heavy', 'black', etc.
- Includes Japanese font indicators ('gothic', 'maru', etc.)

#### Pattern-based Detection
- Recognizes common heading numbering patterns:
  - X.Y format (e.g., "4.1 Student Portal") → H1
  - X.Y.Z format (e.g., "4.1.2 Features") → H2
  - Single numbers (e.g., "1. Introduction") → H1
  - Roman numerals (e.g., "I. Overview") → H1
  - Alphabetic markers (e.g., "A. Details") → H2
- Takes precedence over font-based detection when patterns are found
- Uses regular expressions for efficient pattern matching

#### Numbering Pattern Recognition
- Detects and removes Western numbering patterns (e.g., "1.2.3")
- Handles Asian numbering systems (e.g., "一二三")
- Special handling for mixed patterns (e.g., Western numbering followed by Asian characters)

### 3. Detection Priority

The system prioritizes detection methods in the following order:
1. Pattern-based detection (if a known pattern is found)
2. Font size analysis
3. Font style detection (bold text)

This prioritization ensures that documents with clear heading patterns are processed correctly, while still handling documents with unconventional formatting.

### 4. Parallel Processing

For documents with more than 10 pages, the solution employs parallel processing:

- Uses Python's `multiprocessing` module
- Dynamically adjusts to available CPU cores (up to 8)
- Processes pages in chunks for optimal performance

### 5. Adaptive Processing

The solution includes an adaptive processing mechanism:

- Monitors execution time during processing
- If processing time exceeds 8 seconds, switches to a faster algorithm
- The fast algorithm samples pages throughout the document instead of processing every page

## Performance Optimizations

### CPU Utilization
- Environment variables set to optimize numerical libraries:
  - `OMP_NUM_THREADS=8`
  - `OPENBLAS_NUM_THREADS=8`
  - `MKL_NUM_THREADS=8`
  - `VECLIB_MAXIMUM_THREADS=8`
  - `NUMEXPR_NUM_THREADS=8`

### Memory Efficiency
- Uses LRU cache for font detection to reduce repeated calculations
- Precompiles regular expressions for better performance
- Processes pages in chunks to manage memory usage

### Time Complexity
- O(n) where n is the number of pages for small documents
- For large documents, complexity is reduced through sampling

## Multilingual Support

The solution is designed to handle multilingual documents:

- Western languages: Uses standard font analysis
- Japanese/Chinese: Additional font style detection and numbering patterns
- Unicode support: Properly handles non-Latin characters

## Error Handling

- Graceful degradation when processing large documents
- Fallback mechanisms for title detection
- Exception handling for problematic pages

## Size Constraints

- Total solution size is under 200MB
- No external model dependencies
- No network requirements

## Docker Configuration

The solution is containerized with specific optimizations:

- Base image: python:3.9-slim (AMD64 compatible)
- Environment variables for numerical library optimization
- Volume mounts for input/output directories

## Design Patterns

The solution implements several design patterns:

- **Strategy Pattern**: Different extraction strategies (Standard vs Fast)
- **Composition**: Components are composed rather than inherited
- **Single Responsibility Principle**: Each class has a single, well-defined responsibility
- **Dependency Injection**: Components receive their dependencies through constructors 