"""
Text cleaning module for PDF outline extraction.
"""

import re

class TextCleaner:
    """Handles text cleaning operations for heading detection."""
    
    def __init__(self):
        # Precompile regular expressions for better performance
        self.western_numbering_re = re.compile(r'^\d+(\.\d+)*\s*')
        # For Asian numbering, only match if it's at the beginning of the text
        self.asian_numbering_re = re.compile(r'^[一二三四五六七八九十百千]+[、\.\s]')
        
        # Patterns for heading level detection - Fixed hierarchy levels
        self.h1_single_number_re = re.compile(r'^\d+\.\s+')  # Single number (like "1. ")
        self.h2_double_number_re = re.compile(r'^\d+\.\d+\s+')  # X.Y pattern (like 4.1, 4.2)
        self.h3_triple_number_re = re.compile(r'^\d+\.\d+\.\d+\s+')  # X.Y.Z pattern (like 4.1.2)
        self.h4_quad_number_re = re.compile(r'^\d+\.\d+\.\d+\.\d+\s+')  # X.Y.Z.W pattern (like 4.1.2.3)
        self.h5_quint_number_re = re.compile(r'^\d+\.\d+\.\d+\.\d+\.\d+\s+')  # X.Y.Z.W.V pattern (like 4.1.2.3.5)
        self.h6_hex_number_re = re.compile(r'^\d+\.\d+\.\d+\.\d+\.\d+\.\d+\s+')  # X.Y.Z.W.V.U pattern (like 4.1.2.3.5.6)
        
        # Roman numerals and alphabetic markers
        self.h1_roman_numeral_re = re.compile(r'^[IVX]+\.\s+')  # Roman numerals (I., II., etc)
        self.h2_alpha_marker_re = re.compile(r'^[A-Za-z]\.\s+')  # Alphabetic markers (A., B., etc)
        
        # Enhanced patterns
        self.h3_letter_number_re = re.compile(r'^[A-Za-z]\d+\.\s+')  # Letter+number (like A1., B2.) - now H3
        self.h2_bullet_re = re.compile(r'^[•■◦○●]\s+')  # Bullet points
        self.h3_dash_re = re.compile(r'^[-–—]\s+')  # Dashes
        self.h2_parenthesized_re = re.compile(r'^\([A-Za-z0-9]+\)\s+')  # (1), (A), etc. - includes letters
        self.h2_brackets_re = re.compile(r'^\[\d+\]\s+')  # [1], [2], etc.
        
        # Extended hierarchy patterns
        self.h5_lowercase_alpha_re = re.compile(r'^[a-z]\)\s+')  # a), b), etc. - now H5
        self.h6_roman_lowercase_re = re.compile(r'^[ivx]+\)\s+')  # i), ii), etc. - now H6
        self.h5_asterisk_re = re.compile(r'^\*\s+')  # * (asterisk) - now H5
        
        # Expanded Roman numeral support
        self.roman_numeral_full_re = re.compile(r'^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})\.\s+')
    
    def clean_heading(self, text: str) -> str:
        """Clean heading text by removing numbering patterns."""
        # Check for mixed case: western numbering followed by Asian characters
        match = self.western_numbering_re.match(text)
        if match:
            # If there are Asian characters after the western numbering, only remove the western part
            if any(ord(c) > 0x3000 for c in text[match.end():]):
                return text[match.end():].strip()
        
        # Handle X. pattern (single number with period)
        single_match = self.h1_single_number_re.match(text)
        if single_match:
            return text[single_match.end():].strip()
            
        # Handle X.Y pattern
        xy_match = self.h2_double_number_re.match(text)
        if xy_match:
            return text[xy_match.end():].strip()
            
        # Handle X.Y.Z pattern
        xyz_match = self.h3_triple_number_re.match(text)
        if xyz_match:
            return text[xyz_match.end():].strip()
            
        # Handle X.Y.Z.W pattern
        xyzw_match = self.h4_quad_number_re.match(text)
        if xyzw_match:
            return text[xyzw_match.end():].strip()
            
        # Handle X.Y.Z.W.V pattern (H5)
        h5_match = self.h5_quint_number_re.match(text)
        if h5_match:
            return text[h5_match.end():].strip()
            
        # Handle X.Y.Z.W.V.U pattern (H6)
        h6_match = self.h6_hex_number_re.match(text)
        if h6_match:
            return text[h6_match.end():].strip()
            
        # Handle Roman numerals
        roman_match = self.h1_roman_numeral_re.match(text)
        if roman_match:
            return text[roman_match.end():].strip()
            
        # Handle expanded Roman numerals
        roman_full_match = self.roman_numeral_full_re.match(text)
        if roman_full_match:
            return text[roman_full_match.end():].strip()
            
        # Handle alphabetic markers
        alpha_match = self.h2_alpha_marker_re.match(text)
        if alpha_match:
            return text[alpha_match.end():].strip()
            
        # Handle letter+number
        letter_num_match = self.h3_letter_number_re.match(text)
        if letter_num_match:
            return text[letter_num_match.end():].strip()
            
        # Handle bullets
        bullet_match = self.h2_bullet_re.match(text)
        if bullet_match:
            return text[bullet_match.end():].strip()
            
        # Handle dashes
        dash_match = self.h3_dash_re.match(text)
        if dash_match:
            return text[dash_match.end():].strip()
            
        # Handle parenthesized numbers or letters
        paren_match = self.h2_parenthesized_re.match(text)
        if paren_match:
            return text[paren_match.end():].strip()
            
        # Handle bracketed numbers
        bracket_match = self.h2_brackets_re.match(text)
        if bracket_match:
            return text[bracket_match.end():].strip()
            
        # Handle lowercase letters with parenthesis (a), b), etc.)
        lowercase_alpha_match = self.h5_lowercase_alpha_re.match(text)
        if lowercase_alpha_match:
            return text[lowercase_alpha_match.end():].strip()
            
        # Handle lowercase roman numerals with parenthesis (i), ii), etc.)
        roman_lowercase_match = self.h6_roman_lowercase_re.match(text)
        if roman_lowercase_match:
            return text[roman_lowercase_match.end():].strip()
            
        # Handle asterisks
        asterisk_match = self.h5_asterisk_re.match(text)
        if asterisk_match:
            return text[asterisk_match.end():].strip()
            
        # Asian numbering (一二三) - only if it's at the beginning
        if self.asian_numbering_re.match(text):
            return self.asian_numbering_re.sub('', text).strip()
            
        return text.strip()
    
    def detect_heading_level_from_pattern(self, original_text: str) -> str:
        """Detect heading level based on numbering patterns."""
        # X.Y.Z.W.V.U pattern (like 4.1.2.3.5.6) - H6
        if self.h6_hex_number_re.match(original_text):
            return "H6"
            
        # X.Y.Z.W.V pattern (like 4.1.2.3.5) - H5
        if self.h5_quint_number_re.match(original_text):
            return "H5"
            
        # X.Y.Z.W pattern (like 4.1.2.3) - H4
        if self.h4_quad_number_re.match(original_text):
            return "H4"
            
        # X.Y.Z pattern (like 4.1.2, 4.2.1) - H3
        if self.h3_triple_number_re.match(original_text):
            return "H3"
            
        # X.Y pattern (like 4.1, 4.2) - H2
        if self.h2_double_number_re.match(original_text):
            return "H2"
        
        # Single number with dot (like "1. Introduction")
        if self.h1_single_number_re.match(original_text):
            return "H1"
            
        # Roman numerals (I, II, III, IV)
        if self.h1_roman_numeral_re.match(original_text) or self.roman_numeral_full_re.match(original_text):
            return "H1"
            
        # Alphabetic markers (A, B, C or a, b, c)
        if self.h2_alpha_marker_re.match(original_text):
            return "H2"
            
        # Letter+number (A1., B2.) - Changed to H3
        if self.h3_letter_number_re.match(original_text):
            return "H3"
            
        # DISABLED: Bullet points are not headings in this document
        # if self.h2_bullet_re.match(original_text):
        #    return "H2"
            
        # DISABLED: Dashes are not headings in this document
        # if self.h3_dash_re.match(original_text):
        #    return "H3"
            
        # Parenthesized numbers or letters
        if self.h2_parenthesized_re.match(original_text):
            return "H2"
            
        # Bracketed numbers
        if self.h2_brackets_re.match(original_text):
            return "H2"
            
        # Lowercase letters with parenthesis (a), b), etc.) - Changed to H5
        if self.h5_lowercase_alpha_re.match(original_text):
            return "H5"
            
        # Lowercase roman numerals with parenthesis (i), ii), etc.) - Changed to H6
        if self.h6_roman_lowercase_re.match(original_text):
            return "H6"
            
        # DISABLED: Asterisks are not headings in this document
        # if self.h5_asterisk_re.match(original_text):
        #    return "H5"
        
        return None  # No pattern detected 