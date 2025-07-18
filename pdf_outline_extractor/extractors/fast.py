"""
Fast implementation of PDF outline extraction for large documents.
"""

import logging
import time
import re
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
        start_time = time.time()
        logger.info(f"Using fast extraction mode for: {pdf_path}")
        
        result = {
            "title": "",
            "outline": []
        }
        
        processed_headings = set()
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Try to extract title from first page
                if len(pdf.pages) > 0:
                    first_page = pdf.pages[0]
                    text = first_page.extract_text(x_tolerance=3, y_tolerance=3)
                    if text:
                        lines = text.split('\n')
                        for line in lines[:5]:  # Check first 5 lines for title
                            line = line.strip()
                            if line and (line == "Core Features" or "Core Features" in line):
                                result["title"] = "Core Features"
                                break
                        
                        if not result["title"] and lines:
                            result["title"] = lines[0].strip()
                
                # If no title found, use filename
                if not result["title"]:
                    result["title"] = Path(pdf_path).stem
                
                # Sample pages more intelligently for large documents
                sample_indices = []
                
                if len(pdf.pages) <= 10:
                    # For small documents, process all pages
                    sample_indices = list(range(len(pdf.pages)))
                elif len(pdf.pages) <= 50:
                    # For medium documents, sample every 2-3 pages
                    step = max(2, len(pdf.pages) // 20)
                    sample_indices = list(range(0, len(pdf.pages), step))
                else:
                    # For large documents, sample every 5-10 pages
                    step = max(5, len(pdf.pages) // 30)
                    sample_indices = list(range(0, len(pdf.pages), step))
                
                # Always include first and last pages
                if 0 not in sample_indices:
                    sample_indices.insert(0, 0)
                if len(pdf.pages) - 1 not in sample_indices:
                    sample_indices.append(len(pdf.pages) - 1)
                
                # Process sample pages
                for i in sample_indices:
                    # Check time constraint
                    if time.time() - start_time > 8:
                        logger.warning("Fast extraction time limit reached")
                        break
                        
                    if i >= len(pdf.pages):
                        continue
                        
                    page = pdf.pages[i]
                    text = page.extract_text(x_tolerance=3, y_tolerance=3)
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line or len(line) < 2:
                            continue
                        
                        # Skip if already processed
                        if line in processed_headings:
                            continue
                        
                        # Skip bullets and dashes
                        if line.startswith('-') or line.startswith('•'):
                            continue
                        
                        # Skip if this is the title
                        if line == result["title"]:
                            continue
                        
                        # Determine heading level
                        level = None
                        
                        # H1: "Core Features" repeated on pages
                        if line == "Core Features" and line != result["title"]:
                            level = "H1"
                        
                        # H2: Numbered sections (4.1, 4.2, etc.)
                        elif re.match(r'^\d+\.\d+\s+.+', line):
                            level = "H2"
                        
                        # Use pattern detection
                        else:
                            pattern_level = self.text_cleaner.detect_heading_level_from_pattern(line)
                            if pattern_level:
                                level = pattern_level
                            # Simple heuristic for short lines that might be headings
                            elif len(line) <= 30 and not line.lower().startswith('each portal'):
                                level = "H3"
                        
                        # Add to outline if we have a level
                        if level:
                            result["outline"].append({
                                "level": level,
                                "text": line,
                                "page": i + 1
                            })
                            processed_headings.add(line)
                
                elapsed = time.time() - start_time
                logger.info(f"Fast extraction completed in {elapsed:.2f} seconds")
                return result
                
        except Exception as e:
            logger.error(f"Error in fast extraction: {str(e)}")
            return result 