"""
Fast implementation of PDF outline extraction for large documents.
"""

import logging
import time
from pathlib import Path
from typing import Dict, Any

import pdfplumber

from pdf_outline_extractor.extractors.base import OutlineExtractorBase
from pdf_outline_extractor.core.font_analyzer import FontAnalyzer
from pdf_outline_extractor.core.text_cleaner import TextCleaner

logger = logging.getLogger(__name__)

class FastOutlineExtractor(OutlineExtractorBase):
    """Fast implementation of PDF outline extraction for large documents."""
    
    def __init__(self, font_analyzer: FontAnalyzer, text_cleaner: TextCleaner):
        self.font_analyzer = font_analyzer
        self.text_cleaner = text_cleaner
    
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """Extract outline using a simplified approach for large documents."""
        logger.info(f"Using fast extraction mode for: {pdf_path}")
        
        result = {
            "title": "",
            "outline": []
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Process only first few pages for title and initial headings
                first_pages = min(5, len(pdf.pages))
                
                # Try to extract title from first page
                if len(pdf.pages) > 0:
                    first_page = pdf.pages[0]
                    text = first_page.extract_text(x_tolerance=3, y_tolerance=3)
                    if text:
                        lines = text.split('\n')
                        if lines:
                            result["title"] = lines[0].strip()
                
                # If no title found, use filename
                if not result["title"] and hasattr(pdf, '_stream') and hasattr(pdf._stream, 'name'):
                    result["title"] = Path(pdf._stream.name).stem
                
                # Sample pages throughout document to find headings
                sample_indices = [0]  # Always include first page
                
                # Add some pages throughout the document
                if len(pdf.pages) > 10:
                    step = len(pdf.pages) // 10
                    sample_indices.extend([i for i in range(step, len(pdf.pages), step)])
                
                # Process sample pages
                for i in sample_indices:
                    if i >= len(pdf.pages):
                        continue
                        
                    page = pdf.pages[i]
                    text = page.extract_text(x_tolerance=3, y_tolerance=3)
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line or len(line) < 5:
                            continue
                        
                        # First check for pattern-based heading levels
                        heading_level = self.text_cleaner.detect_heading_level_from_pattern(line)
                        
                        # If no pattern detected, use simple heuristics
                        if not heading_level:
                            # Simple heuristic: lines with less than 50 chars might be headings
                            if len(line) < 50:
                                # Determine heading level based on simple heuristics
                                if line.isupper() or line.endswith(':'):
                                    heading_level = "H1"
                                elif i == 0:  # First page headings are likely higher level
                                    heading_level = "H2"
                                else:
                                    heading_level = "H3"
                            else:
                                continue  # Likely not a heading
                        
                        # Clean numbering
                        clean_line = self.text_cleaner.clean_heading(line)
                        
                        # Add to outline
                        result["outline"].append({
                            "level": heading_level,
                            "text": clean_line,
                            "page": i + 1
                        })
                
                return result
                
        except Exception as e:
            logger.error(f"Error in fast extraction: {str(e)}")
            return result 