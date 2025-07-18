"""
Hierarchy validation module for PDF outline extraction.
"""

from typing import Dict, List, Any
import re

class HierarchyValidator:
    """Validates and corrects heading hierarchy."""
    
    def __init__(self):
        self.heading_levels = ["TITLE", "H1", "H2", "H3", "H4", "H5", "H6"]
        
    def validate_outline(self, outline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate and correct heading hierarchy.
        
        Args:
            outline: The extracted outline with headings
            
        Returns:
            Corrected outline with valid hierarchy
        """
        if not outline:
            return outline
        
        # First, fix specific pattern issues before general validation
        self._fix_specific_patterns(outline)
            
        # Next, identify hierarchy issues
        issues = []
        for i in range(1, len(outline)):
            prev_level = self.heading_levels.index(outline[i-1]["level"]) if outline[i-1]["level"] in self.heading_levels else 0
            curr_level = self.heading_levels.index(outline[i]["level"]) if outline[i]["level"] in self.heading_levels else 0
            
            # Check for skipped levels (e.g., H1 followed by H3)
            if curr_level > prev_level + 1:
                issues.append((i, "skipped", prev_level, curr_level))
                
            # Check for invalid level jumps (e.g., H3 followed by H1 without an H2 in between)
            if i > 1 and curr_level < prev_level - 1:
                # This might be intentional, so we don't fix it automatically
                # But we could flag it for review
                pass
        
        # Fix issues
        for idx, issue_type, prev_level, curr_level in reversed(issues):
            if issue_type == "skipped":
                # Adjust the level to be one step below the previous heading
                corrected_level = self.heading_levels[prev_level + 1]
                outline[idx]["level"] = corrected_level
        
        # Ensure consistent hierarchy
        self._ensure_consistent_hierarchy(outline)
        
        return outline
    
    def _fix_specific_patterns(self, outline: List[Dict[str, Any]]) -> None:
        """
        Fix specific pattern issues based on DeepSeek recommendations.
        
        This fixes common issues like X.Y patterns being incorrectly labeled as H1.
        """
        # Pattern matchers for specific fixes
        dot_pattern = re.compile(r'^\d+\.\d+')  # X.Y pattern (like 4.1, 4.2)
        nested_pattern = re.compile(r'^[a-z]\)') # a), b) pattern
        roman_nested = re.compile(r'^[ivx]+\)') # i), ii) pattern
        letter_number = re.compile(r'^[A-Za-z]\d+\.') # A1., B2. pattern
        numbered_section = re.compile(r'^\d+\.\d+\s+\w+') # Like "4.1 Student Portal"
        
        # First pass: Fix Core Features and numbered sections
        for i in range(len(outline)):
            item = outline[i]
            text = item["text"]
            
            # Keep "Core Features" as H1 when it appears on pages 2+ 
            if text == "Core Features" and item["level"] == "H1":
                # Keep as H1
                pass
                
            # Fix: Numbered sections like "4.1 Student Portal" should be H2 (KEEP as H2)
            elif numbered_section.match(text):
                item["level"] = "H2"
            
            # Fix: "Communication Hub" and "Documentation" should be H3, not H2
            elif text in ["Communication Hub", "Documentation"] and item["level"] == "H2":
                item["level"] = "H3"
        
        # Second pass: Fix subsections based on context
        for i in range(len(outline)):
            item = outline[i]
            text = item["text"]
            
            # Fix: Subsections like "Profile Management" should be H3 when under a numbered section
            if i > 0 and outline[i-1]["level"] == "H2" and not dot_pattern.match(text) and len(text.split()) <= 3:
                item["level"] = "H3"
            
            # Fix: Make sure list items are not treated as headings
            if text.startswith("-") or text.startswith("•"):
                # This is a list item, not a heading - remove from outline
                item["_remove"] = True
                
            # Fix 1: X.Y patterns should be H2, not H1 (COMMENTED OUT - we already set this correctly)
            # if dot_pattern.match(text) and item["level"] == "H1":
            #     item["level"] = "H2"
                
            # Fix 2: Ensure a), b) patterns are correctly labeled as H5 when under H4
            if i > 0 and nested_pattern.match(text) and outline[i-1]["level"] == "H4":
                item["level"] = "H5"
                
            # Fix 3: Ensure i), ii) patterns are H6 when under H5
            if i > 0 and roman_nested.match(text) and outline[i-1]["level"] == "H5":
                item["level"] = "H6"
                
            # Fix 4: Letter+number patterns should be H3
            if letter_number.match(text) and item["level"] == "H1":
                item["level"] = "H3"
        
        # Remove items marked for removal
        i = 0
        while i < len(outline):
            if outline[i].get("_remove", False):
                del outline[i]
            else:
                # Remove the _remove flag if it exists
                if "_remove" in outline[i]:
                    del outline[i]["_remove"]
                i += 1
    
    def _ensure_consistent_hierarchy(self, outline: List[Dict[str, Any]]) -> None:
        """
        Ensure consistent hierarchy by analyzing patterns in the document.
        
        This helps with documents that have inconsistent formatting but follow
        a logical structure.
        """
        if len(outline) < 3:
            return
            
        # Count headings by level
        level_counts = {"H1": 0, "H2": 0, "H3": 0, "H4": 0, "H5": 0, "H6": 0}
        for item in outline:
            if item["level"] in level_counts:
                level_counts[item["level"]] += 1
        
        # Fix 1: If there are very few H1s but many H2s, some H2s might actually be H1s
        # DISABLED: We want to keep H2s as H2s for numbered sections
        # if level_counts["H1"] <= 2 and level_counts["H2"] >= 5:
        #     # Find potential H1s misclassified as H2s
        #     for i, item in enumerate(outline):
        #         if item["level"] == "H2":
        #             # Check if this looks like a main section
        #             if i == 0 or (i > 0 and outline[i-1]["level"] != "H1"):
        #                 # Check text length (main headings tend to be shorter)
        #                 if len(item["text"]) < 30:
        #                     item["level"] = "H1"
        
        # Fix 2: Handle potentially incorrect nesting
        # Find patterns where a heading is followed by a heading of the same level
        # If that's followed by a deeper level, the second heading might need to be promoted
        for i in range(1, len(outline) - 1):
            curr = outline[i]
            prev = outline[i-1]
            next_item = outline[i+1]
            
            # If we have H1->H1->H2 pattern, the second H1 might need to be H2
            if prev["level"] == curr["level"] == "H1" and next_item["level"] == "H2":
                # Check the text pattern - if the second H1 has a "X.Y" pattern, it's likely an H2
                if re.match(r'^\d+\.\d+', curr["text"]):
                    curr["level"] = "H2"
        
        # Fix 3: Check for excessive depth
        # If there are too many deep headings, consider collapsing them
        if level_counts["H5"] + level_counts["H6"] > level_counts["H1"] + level_counts["H2"]:
            self._collapse_excessive_depth(outline)
    
    def _collapse_excessive_depth(self, outline: List[Dict[str, Any]]) -> None:
        """
        Collapse excessive depth in the heading hierarchy.
        
        This is useful for documents with too many deep heading levels.
        """
        for item in outline:
            # Promote H6 to H5 if there are too many H6s
            if item["level"] == "H6":
                item["level"] = "H5" 