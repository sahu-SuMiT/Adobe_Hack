# Troubleshooting Guide

## Common Issues and Solutions

### Docker-related Issues

#### Issue: Docker build fails
**Possible causes and solutions:**
- Incompatible architecture: Ensure you're using the `--platform=linux/amd64` flag
- Network issues: If building in an environment with internet, check your connection
- Insufficient disk space: Free up disk space and try again

#### Issue: Container exits immediately
**Possible causes and solutions:**
- Input directory not mounted correctly: Check your volume mount syntax
- Permission issues: Ensure the mounted directories have appropriate permissions
- Missing PDF files: Verify that PDF files exist in the input directory

### PDF Processing Issues

#### Issue: Missing headings in output
**Possible causes and solutions:**
- Non-standard fonts: The PDF may use custom fonts that don't follow naming conventions
- Scanned PDF: The PDF might be a scanned image without proper text layers
- Complex formatting: Highly complex layouts may confuse the heading detection

**Adjustments:**
1. You can modify the font size thresholds in `extract_outline.py`:
   ```python
   self.title_min_size_ratio = 1.5  # Try lowering to 1.3
   self.h1_min_size_ratio = 1.3     # Try lowering to 1.2
   self.h2_min_size_ratio = 1.15    # Try lowering to 1.1
   self.h3_min_size_ratio = 1.05    # Try lowering to 1.02
   ```

#### Issue: Incorrect title detection
**Possible causes and solutions:**
- Title not formatted distinctly: The PDF may not have a clearly formatted title
- Multiple large text elements: Multiple elements with large font sizes may confuse detection

**Adjustments:**
1. Check the first few lines of the document manually
2. If needed, you can hardcode the title for specific documents

#### Issue: Processing time exceeds 10 seconds
**Possible causes and solutions:**
- Very large PDF (>50 pages): The solution is optimized for up to 50 pages
- Complex PDF with many elements: PDFs with many text elements per page take longer
- System resource constraints: Ensure your system has sufficient resources

**Adjustments:**
1. Increase the early timeout threshold:
   ```python
   # Change from 8 to 5 seconds to switch to fast mode earlier
   if time.time() - start_time > 5:
   ```

### Multilingual Document Issues

#### Issue: Japanese/Chinese headings not detected
**Possible causes and solutions:**
- Font detection not matching: Add additional font keywords for Asian fonts
- Character encoding issues: Ensure the PDF uses standard Unicode encoding

**Adjustments:**
1. Add additional Asian font indicators to the `bold_keywords` list:
   ```python
   # Add more Asian font indicators
   self.bold_keywords.extend(['hei', 'kai', 'song', 'mincho'])
   ```

#### Issue: Incorrect numbering removal
**Possible causes and solutions:**
- Custom numbering system: The document may use a custom numbering system
- Mixed numbering styles: The document might mix different numbering styles

**Adjustments:**
1. Modify the regular expressions for numbering detection:
   ```python
   # Add or modify patterns as needed
   self.western_numbering_re = re.compile(r'^\d+(\.\d+)*\s*|^[A-Z][\.\)]\s*')
   ```

## Performance Tuning

### For Faster Processing
- Reduce the number of processes for smaller systems:
  ```python
  # Change from 8 to 4 for systems with fewer cores
  num_processes = min(4, len(pdf.pages))
  ```

### For Better Accuracy
- Increase the detail level in the fast extraction mode:
  ```python
  # Sample more pages for better coverage
  step = len(pdf.pages) // 20  # Change from 10 to 20
  ```

## Logging and Debugging

To get more detailed logs, change the logging level:
```python
# Change from INFO to DEBUG
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

## Contact and Support

For additional support or to report issues, please open an issue in the GitHub repository or contact the maintainer. 