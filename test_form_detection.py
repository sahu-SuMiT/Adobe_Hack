#!/usr/bin/env python3
"""
Test script to verify form detection works correctly.
"""

from pdf_outline_extractor.extractors.standard import StandardOutlineExtractor

def test_form_detection():
    """Test form detection logic."""
    extractor = StandardOutlineExtractor()
    
    # Test 1: Form document
    form_result = {
        "title": "Application form for grant of LTC advance",
        "outline": []
    }
    
    form_page_text = [{
        "text": """Application form for grant of LTC advance
1. Name of the Government Servant
2. Designation  
3. Date of entering the Central Government Service
I declare that the particulars furnished above are true
I undertake to refund the entire advance""",
        "page_num": 1,
        "chars": []
    }]
    
    is_form = extractor._is_form_document(form_result, form_page_text)
    print(f"Form document detection: {is_form} (should be True)")
    
    # Test 2: Content document
    content_result = {
        "title": "Core Features",
        "outline": []
    }
    
    content_page_text = [{
        "text": """Core Features
4.1 Student Portal
Profile Management
Job Search
Application Tracking
4.2 College Portal
Student Management""",
        "page_num": 1,
        "chars": []
    }]
    
    is_content = extractor._is_form_document(content_result, content_page_text)
    print(f"Content document detection: {is_content} (should be False)")

if __name__ == "__main__":
    test_form_detection()
