#!/usr/bin/env python3
"""
Performance test script for PDF outline extraction.
"""

import time
import os
from pdf_outline_extractor import PDFOutlineExtractor

def test_performance():
    """Test the performance of PDF extraction."""
    
    # Initialize extractor
    extractor = PDFOutlineExtractor()
    
    # Test with the current PDF
    pdf_path = os.path.join("input", "Core_Features_Portal_System.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        return
    
    print(f"Testing performance with: {pdf_path}")
    
    # Run extraction multiple times to test consistency
    times = []
    for i in range(3):
        start_time = time.time()
        result = extractor.extract_outline(pdf_path)
        elapsed = time.time() - start_time
        times.append(elapsed)
        
        print(f"Run {i+1}: {elapsed:.3f}s - Found {len(result['outline'])} headings")
    
    avg_time = sum(times) / len(times)
    print(f"Average time: {avg_time:.3f}s")
    
    # Check if under 10s constraint
    if avg_time < 10.0:
        print("✅ Performance constraint met (< 10s)")
    else:
        print("❌ Performance constraint exceeded (>= 10s)")
    
    return result

if __name__ == "__main__":
    test_performance()
