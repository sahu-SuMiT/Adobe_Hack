"""
Page processing module for PDF outline extraction.
"""

import logging
from typing import Optional, Tuple, Any

from pdf_outline_extractor.core.font_analyzer import FontAnalyzer

logger = logging.getLogger(__name__)

class PDFPageProcessor:
    """Processes individual PDF pages to extract text and font information."""
    
    def __init__(self, font_analyzer: FontAnalyzer):
        self.font_analyzer = font_analyzer
    
    def process_page(self, page_data: Tuple) -> Optional[Tuple]:
        """
        Process a single page to extract font information and text.
        
        Args:
            page_data: Tuple containing (page, page_index)
            
        Returns:
            Tuple containing (font_sizes, page_info) or None if processing fails
        """
        page, page_index = page_data
        try:
            page_chars = page.chars
            if not page_chars:
                return None
            
            # Extract font sizes
            page_font_sizes = [char['size'] for char in page_chars if 'size' in char]
            
            # Extract text
            extracted = page.extract_text(x_tolerance=3, y_tolerance=3)
            if not extracted:
                return page_font_sizes, None
            
            page_info = {
                'page_num': page_index + 1,
                'text': extracted,
                'chars': page_chars
            }
            
            return page_font_sizes, page_info
            
        except Exception as e:
            logger.warning(f"Error processing page {page_index + 1}: {str(e)}")
            return None 