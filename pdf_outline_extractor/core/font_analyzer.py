"""
Font analysis module for PDF outline extraction.
"""

from functools import lru_cache
from typing import Optional

class FontAnalyzer:
    """Analyzes font properties in PDF documents."""
    
    def __init__(self):
        # Bold text indicators
        self.bold_keywords = [
            # Western font weight indicators
            'bold', 'heavy', 'black', 'demi', 'medium',
            # Japanese/Asian font weight indicators
            'gothic', 'maru', 'futogo', 'futomin', 'hei', 'kai', 'song', 'mincho'
        ]
        
    @lru_cache(maxsize=1024)
    def is_bold(self, font: Optional[str]) -> bool:
        """Check if a font is likely bold based on its name."""
        if not font or not isinstance(font, str):
            return False
            
        font_lower = font.lower()
        return any(keyword in font_lower for keyword in self.bold_keywords) 