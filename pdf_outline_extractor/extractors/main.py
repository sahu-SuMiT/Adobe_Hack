"""
Main entry point for PDF outline extraction.
"""

from typing import Dict, Any

from pdf_outline_extractor.extractors.standard import StandardOutlineExtractor

class PDFOutlineExtractor:
    """Main class for extracting outlines from PDF documents."""
    
    def __init__(self):
        self.standard_extractor = StandardOutlineExtractor()
    
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """Extract outline from a PDF file."""
        return self.standard_extractor.extract_outline(pdf_path) 