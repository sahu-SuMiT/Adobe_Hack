"""
Heading detection module for PDF outline extraction.
"""

from typing import Optional

from pdf_outline_extractor.core.font_analyzer import FontAnalyzer
from pdf_outline_extractor.core.text_cleaner import TextCleaner

class HeadingDetector:
    """Detects headings based on font size and formatting."""
    
    def __init__(self, font_analyzer: FontAnalyzer, text_cleaner: TextCleaner):
        self.font_analyzer = font_analyzer
        self.text_cleaner = text_cleaner
        
        # Font size thresholds for heading detection
        self.title_min_size_ratio = 1.5  # Title is typically larger than most text
        self.h1_min_size_ratio = 1.3
        self.h2_min_size_ratio = 1.15
        self.h3_min_size_ratio = 1.05
        self.h4_min_size_ratio = 1.02
        self.h5_min_size_ratio = 1.01
        self.h6_min_size_ratio = 1.0
    
    def detect_heading_level(self, size_ratio: float, is_bold: bool, original_text: Optional[str] = None,
                            previous_heading: Optional[str] = None, line_position: Optional[float] = None) -> Optional[str]:
        """
        Determine the heading level based on pattern, size ratio and formatting.
        
        Args:
            size_ratio: Font size ratio compared to median size
            is_bold: Whether the text is bold
            original_text: Original text with potential numbering patterns
            previous_heading: The previous heading level (for context)
            line_position: Position of the line on the page (top lines more likely to be headings)
            
        Returns:
            Heading level (TITLE, H1, H2, H3, H4, H5, H6) or None if not a heading
        """
        # First check for patterns if original text is provided
        if original_text:
            pattern_level = self.text_cleaner.detect_heading_level_from_pattern(original_text)
            if pattern_level:
                return pattern_level
        
        # Consider position on page (top of page more likely to be heading)
        position_boost = 0
        if line_position is not None and line_position < 0.2:  # Top 20% of page
            position_boost = 0.1  # Boost size ratio for top-of-page text
        
        # Consider bold text as stronger signal
        bold_boost = 0.15 if is_bold else 0
        
        # Apply boosts to size ratio
        effective_ratio = size_ratio + position_boost + bold_boost
        
        # Consider context from previous heading for better hierarchy
        if previous_heading and effective_ratio >= 1.0:
            # If previous was TITLE, this is likely H1
            if previous_heading == "TITLE" and effective_ratio >= self.h1_min_size_ratio * 0.9:
                return "H1"
            # If previous was H1, this could be H2 with slightly lower threshold
            elif previous_heading == "H1" and effective_ratio >= self.h2_min_size_ratio * 0.9:
                return "H2"
            # If previous was H2, this could be H3 with slightly lower threshold
            elif previous_heading == "H2" and effective_ratio >= self.h3_min_size_ratio * 0.9:
                return "H3"
            # If previous was H3, this could be H4 with slightly lower threshold
            elif previous_heading == "H3" and effective_ratio >= self.h4_min_size_ratio * 0.9:
                return "H4"
            # If previous was H4, this could be H5 with slightly lower threshold
            elif previous_heading == "H4" and effective_ratio >= self.h5_min_size_ratio * 0.9:
                return "H5"
            # If previous was H5, this could be H6 with slightly lower threshold
            elif previous_heading == "H5" and effective_ratio >= self.h6_min_size_ratio * 0.9:
                return "H6"
        
        # Fall back to size-based detection
        if effective_ratio >= self.title_min_size_ratio:
            return "TITLE"
        elif effective_ratio >= self.h1_min_size_ratio:
            return "H1"
        elif effective_ratio >= self.h2_min_size_ratio:
            return "H2" 
        elif effective_ratio >= self.h3_min_size_ratio:
            return "H3"
        elif effective_ratio >= self.h4_min_size_ratio:
            return "H4"
        elif effective_ratio >= self.h5_min_size_ratio:
            return "H5"
        elif effective_ratio >= self.h6_min_size_ratio and is_bold:  # H6 needs to be bold
            return "H6"
        else:
            return None  # Not a heading