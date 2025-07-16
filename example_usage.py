#!/usr/bin/env python3
"""
Example script demonstrating how to use the modular components of the PDF Outline Extractor.
This shows how to use individual components or the complete extractor.
"""

import os
import json
import sys

# Add the current directory to sys.path if needed
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from pdf_outline_extractor import (
    FontAnalyzer, 
    TextCleaner, 
    HeadingDetector, 
    PDFPageProcessor,
    StandardOutlineExtractor,
    FastOutlineExtractor,
    PDFOutlineExtractor
)

def example_using_main_extractor(pdf_path, output_path):
    """
    Example using the main PDFOutlineExtractor class.
    This is the simplest way to use the library.
    """
    print(f"\n=== Using main PDFOutlineExtractor on {pdf_path} ===")
    
    # Create the extractor
    extractor = PDFOutlineExtractor()
    
    # Extract outline
    outline = extractor.extract_outline(pdf_path)
    
    # Print the result
    print(f"Title: {outline['title']}")
    print(f"Found {len(outline['outline'])} headings")
    
    # Save the result
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(outline, f, ensure_ascii=False, indent=2)
    
    print(f"Saved outline to {output_path}")

def example_using_specific_extractor(pdf_path, output_path, use_fast=False):
    """
    Example using a specific extractor (Standard or Fast).
    This gives you more control over which extraction strategy to use.
    """
    extractor_name = "FastOutlineExtractor" if use_fast else "StandardOutlineExtractor"
    print(f"\n=== Using {extractor_name} on {pdf_path} ===")
    
    # Create the appropriate extractor
    if use_fast:
        font_analyzer = FontAnalyzer()
        text_cleaner = TextCleaner()
        extractor = FastOutlineExtractor(font_analyzer, text_cleaner)
    else:
        extractor = StandardOutlineExtractor()
    
    # Extract outline
    outline = extractor.extract_outline(pdf_path)
    
    # Print the result
    print(f"Title: {outline['title']}")
    print(f"Found {len(outline['outline'])} headings")
    
    # Save the result
    output_name = os.path.splitext(output_path)[0]
    output_path = f"{output_name}_{extractor_name}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(outline, f, ensure_ascii=False, indent=2)
    
    print(f"Saved outline to {output_path}")

def example_using_individual_components(text):
    """
    Example using individual components.
    This demonstrates how to use the components separately.
    """
    print(f"\n=== Using individual components ===")
    
    # Create components
    font_analyzer = FontAnalyzer()
    text_cleaner = TextCleaner()
    heading_detector = HeadingDetector(font_analyzer, text_cleaner)
    
    # Example font analysis
    font_name = "Arial-Bold"
    is_bold = font_analyzer.is_bold(font_name)
    print(f"Is '{font_name}' bold? {is_bold}")
    
    # Example text cleaning
    clean_text = text_cleaner.clean_heading(text)
    print(f"Original text: '{text}'")
    print(f"Cleaned text: '{clean_text}'")
    
    # Example heading detection
    size_ratio = 1.4
    is_bold = True
    heading_level = heading_detector.detect_heading_level(size_ratio, is_bold)
    print(f"Text with size ratio {size_ratio} and bold={is_bold} is a {heading_level} heading")

def main():
    # Create test directory if it doesn't exist
    os.makedirs("test_output", exist_ok=True)
    
    # Example PDF path - replace with an actual PDF path for testing
    pdf_path = "input/sample.pdf"
    if not os.path.exists(pdf_path):
        print(f"Warning: {pdf_path} does not exist. Please provide a valid PDF path.")
        pdf_path = input("Enter path to a PDF file: ")
    
    # Run examples
    example_using_main_extractor(pdf_path, "test_output/outline_main.json")
    example_using_specific_extractor(pdf_path, "test_output/outline_specific.json", use_fast=False)
    example_using_specific_extractor(pdf_path, "test_output/outline_specific.json", use_fast=True)
    example_using_individual_components("1.2.3 Introduction to PDF Processing")

if __name__ == "__main__":
    main() 