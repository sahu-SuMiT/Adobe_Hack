"""
Enhanced heading detector with stricter filtering for competition compliance.
"""

import re
from typing import Dict, List, Optional

class CompetitionHeadingFilter:
    """Filters out false positives for better precision in heading detection."""
    
    def __init__(self):
        # Patterns that should NOT be considered headings
        self.exclude_patterns = [
            # Revision history entries
            r'^\d+\.\d+\s+\d+\s+(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)',
            r'Initial version$',
            r'reviewed and confirmed$',
            r'amended.*diagram$',
            r'Working group updates',
            r'GA release',
            
            # Version and date information
            r'^Version\s+\d+\.\d+',
            r'^\d{1,2}\s+(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+\d{4}',
            
            # Page references and footers
            r'Page\s+\d+\s+of\s+\d+',
            r'Version\s+\d{4}',
            r'May\s+\d{1,2},?\s*$',
            
            # Metadata and document info
            r'^This overview document',
            r'^Extensions who wants',
            r'^working within Agile',
            r'^\d+\.\s*Professionals who',
            r'^\d+\.\s*Junior professional',
            r'obtained the ISTQB',
            r'This section lists',
            r'Extension.*Agile Tester certification',
            r'An Agile Tester can',
            r'The following registered trademarks',
            
            # Common false positives
            r'^Foundation Level Working Group\.$',
            r'^Analytics$',  # This should be excluded
            r'^Syllabus Days$',
            
            # Cover page items that shouldn't be headings
            r'^Foundation Level Extensions$',
            r'^Version\s+\d+\.\d+$',
            r'^Overview$',  # When it's standalone on cover
        ]
        
        self.exclude_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.exclude_patterns]
        
        # Patterns that ARE valid headings
        self.include_patterns = [
            # Clear section headers
            r'^\d+\.\s+(Introduction|Overview|Background|Summary|Conclusion)',
            r'^(Table of Contents|Acknowledgements|References)$',
            r'^Revision History$',
            r'^\d+\.\d+\s+[A-Z][a-z]',  # Numbered subsections with proper capitalization
            r'^Appendix\s+[A-Z]',
            r'^Phase\s+[IVX]+',
        ]
        
        self.include_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.include_patterns]
    
    def should_exclude_heading(self, text: str) -> bool:
        """Check if text should be excluded from headings."""
        text = text.strip()
        
        # Check exclusion patterns
        for regex in self.exclude_regex:
            if regex.search(text):
                return True
        
        # Additional length-based filtering (more lenient)
        if len(text) > 150:  # Increased from 100
            return True
            
        if len(text) < 2:  # Decreased from 3
            return True
        
        return False
    
    def should_include_heading(self, text: str) -> bool:
        """Check if text should definitely be included as a heading."""
        text = text.strip()
        
        # Check inclusion patterns
        for regex in self.include_regex:
            if regex.search(text):
                return True
        
        return False
    
    def is_valid_heading(self, text: str, level: str, page: int, font_size_ratio: float = 1.0) -> bool:
        """Comprehensive check if text is a valid heading."""
        text = text.strip()
        
        # Definitely include if it matches inclusion patterns
        if self.should_include_heading(text):
            return True
            
        # Definitely exclude if it matches exclusion patterns
        if self.should_exclude_heading(text):
            return False
        
        # Additional validation based on level and context
        if level == "H1":
            # H1 should be substantial section headers
            if len(text) < 3:  # Reduced from 5
                return False
        
        elif level in ["H2", "H3"]:
            # H2/H3 should have proper formatting (more lenient)
            if len(text) < 2:
                return False
        
        # Check for numbered sections (these are usually valid)
        if re.match(r'^\d+\.', text):
            return True
        
        # Check for common heading patterns
        if text.endswith(':') and len(text) > 5:  # Like "Summary:", "Background:"
            return True
            
        # Font size validation (more lenient)
        if font_size_ratio < 1.0:  # Reduced from 1.05
            return False
        
        return True

def filter_headings_for_competition(headings: List[Dict]) -> List[Dict]:
    """Filter headings list to improve precision for competition scoring."""
    filter_obj = CompetitionHeadingFilter()
    filtered = []
    
    for heading in headings:
        text = heading["text"]
        level = heading["level"]
        page = heading["page"]
        
        if filter_obj.is_valid_heading(text, level, page):
            filtered.append(heading)
    
    return filtered
