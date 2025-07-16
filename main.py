#!/usr/bin/env python3
"""
Main script for PDF outline extraction.
"""

import os
import sys
import logging
import multiprocessing
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the PDF outline extractor
try:
    from pdf_outline_extractor import PDFOutlineExtractor
except ImportError:
    logger.error("PDF Outline Extractor package not found. Make sure it's installed.")
    sys.exit(1)

def process_pdf_directory(input_dir: str, output_dir: str) -> None:
    """Process all PDFs in the input directory and save results to output directory."""
    # Create the extractor
    extractor = PDFOutlineExtractor()
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all PDF files
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {input_dir}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF
    for pdf_file in pdf_files:
        input_path = os.path.join(input_dir, pdf_file)
        output_path = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}.json")
        
        # Extract outline
        outline = extractor.extract_outline(input_path)
        
        # Write output JSON
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(outline, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved outline to {output_path}")

def main() -> None:
    """Main entry point for the script."""
    # Set multiprocessing start method
    if sys.platform == 'darwin':  # macOS
        multiprocessing.set_start_method('spawn')
    
    # Default directories - use local paths instead of Docker paths
    input_dir = os.path.join(os.getcwd(), "input")
    output_dir = os.path.join(os.getcwd(), "output")
    
    # Allow overriding directories for testing
    if len(sys.argv) > 2:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
    
    # Ensure input directory exists
    if not os.path.exists(input_dir):
        logger.error(f"Input directory not found: {input_dir}")
        logger.info(f"Creating input directory: {input_dir}")
        os.makedirs(input_dir, exist_ok=True)
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        logger.info(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
    
    logger.info(f"Starting PDF outline extraction: {input_dir} -> {output_dir}")
    process_pdf_directory(input_dir, output_dir)
    logger.info("Processing complete")

if __name__ == "__main__":
    main() 