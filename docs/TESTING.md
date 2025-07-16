# Testing Guide

This document provides instructions for testing the PDF Outline Extractor solution.

## Prerequisites

- Docker installed and configured
- Git (to clone the repository)
- Sample PDF files for testing

## Basic Testing

### 1. Setup Test Environment

Create test directories:

```bash
mkdir -p test/input test/output
```

### 2. Prepare Test Files

Place test PDF files in the `test/input` directory. For comprehensive testing, include:

- Simple document (few pages, clear headings)
- Complex document (many pages, varied formatting)
- Multilingual document (including non-Latin characters)
- Japanese document (if available)

### 3. Run the Solution

```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:test .
docker run --rm -v $(pwd)/test/input:/app/input -v $(pwd)/test/output:/app/output --network none pdf-outline-extractor:test
```

### 4. Validate Results

Check the output JSON files in the `test/output` directory:

- Verify that each input PDF has a corresponding JSON file
- Check that the JSON structure matches the expected format
- Validate that titles and headings are correctly identified

## Advanced Testing

### Performance Testing

To test performance with large documents:

1. Generate or obtain a large PDF (50 pages)
2. Time the execution:

```bash
time docker run --rm -v $(pwd)/test/input:/app/input -v $(pwd)/test/output:/app/output --network none pdf-outline-extractor:test
```

3. Verify that processing completes within 10 seconds

### Resource Usage Testing

Monitor resource usage during execution:

```bash
docker stats $(docker run -d --rm -v $(pwd)/test/input:/app/input -v $(pwd)/test/output:/app/output --network none pdf-outline-extractor:test)
```

### Offline Testing

To verify that the solution works without internet access:

```bash
docker run --rm --network none -v $(pwd)/test/input:/app/input -v $(pwd)/test/output:/app/output pdf-outline-extractor:test
```

## Automated Testing

### Unit Tests

You can run unit tests for the core components:

```python
import unittest
from extract_outline import PDFOutlineExtractor

class TestPDFOutlineExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = PDFOutlineExtractor()
    
    def test_is_bold(self):
        self.assertTrue(self.extractor.is_bold("Arial-Bold"))
        self.assertFalse(self.extractor.is_bold("Arial-Regular"))
    
    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
```

Save this as `test_extract_outline.py` and run:

```bash
python test_extract_outline.py
```

### Integration Tests

Create a script to validate output against expected results:

```python
import json
import os
import sys

def validate_output(output_dir, expected_dir):
    success = True
    for filename in os.listdir(expected_dir):
        if not filename.endswith('.json'):
            continue
            
        output_path = os.path.join(output_dir, filename)
        expected_path = os.path.join(expected_dir, filename)
        
        if not os.path.exists(output_path):
            print(f"FAIL: Missing output file {filename}")
            success = False
            continue
            
        with open(output_path, 'r') as f:
            output_data = json.load(f)
        
        with open(expected_path, 'r') as f:
            expected_data = json.load(f)
            
        # Check title
        if output_data['title'] != expected_data['title']:
            print(f"FAIL: Title mismatch in {filename}")
            success = False
            
        # Check outline length
        if len(output_data['outline']) != len(expected_data['outline']):
            print(f"FAIL: Outline length mismatch in {filename}")
            success = False
            
        # Check headings
        for i, (output_heading, expected_heading) in enumerate(zip(output_data['outline'], expected_data['outline'])):
            if output_heading != expected_heading:
                print(f"FAIL: Heading mismatch at index {i} in {filename}")
                success = False
                
    return success

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python validate_output.py output_dir expected_dir")
        sys.exit(1)
        
    output_dir = sys.argv[1]
    expected_dir = sys.argv[2]
    
    if validate_output(output_dir, expected_dir):
        print("All tests passed!")
        sys.exit(0)
    else:
        print("Some tests failed.")
        sys.exit(1)
```

Save this as `validate_output.py` and run:

```bash
python validate_output.py test/output test/expected
```

## Troubleshooting Tests

If tests fail, check:

1. PDF compatibility - ensure PDFs are valid and not corrupted
2. Font extraction - verify that fonts are properly embedded in the PDF
3. Processing time - for large documents, check if the fast fallback algorithm is being triggered

## Reporting Issues

When reporting issues, include:

1. The input PDF file
2. The generated JSON output
3. Expected output
4. Docker and system information
5. Any error messages from the logs 