#!/usr/bin/env python3
"""
Script to validate output JSON files against expected results.
"""

import json
import os
import sys

def validate_output(output_dir, expected_dir):
    """
    Validate the output JSON files against expected results.
    
    Args:
        output_dir: Directory containing the output JSON files
        expected_dir: Directory containing the expected JSON files
        
    Returns:
        bool: True if all tests pass, False otherwise
    """
    success = True
    
    # Check if directories exist
    if not os.path.isdir(output_dir):
        print(f"Error: Output directory {output_dir} does not exist")
        return False
        
    if not os.path.isdir(expected_dir):
        print(f"Error: Expected directory {expected_dir} does not exist")
        return False
    
    # Get list of expected files
    expected_files = [f for f in os.listdir(expected_dir) if f.endswith('.json')]
    
    if not expected_files:
        print(f"Warning: No JSON files found in {expected_dir}")
        return False
    
    print(f"Found {len(expected_files)} expected JSON files to validate")
    
    # Check each expected file
    for filename in expected_files:
        output_path = os.path.join(output_dir, filename)
        expected_path = os.path.join(expected_dir, filename)
        
        # Check if output file exists
        if not os.path.exists(output_path):
            print(f"FAIL: Missing output file {filename}")
            success = False
            continue
        
        # Load JSON files
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                output_data = json.load(f)
            
            with open(expected_path, 'r', encoding='utf-8') as f:
                expected_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"FAIL: Invalid JSON in file {filename}: {e}")
            success = False
            continue
        except Exception as e:
            print(f"FAIL: Error reading file {filename}: {e}")
            success = False
            continue
        
        # Validate structure
        if 'title' not in output_data or 'outline' not in output_data:
            print(f"FAIL: Invalid structure in {filename}")
            success = False
            continue
        
        # Check title
        if output_data['title'] != expected_data['title']:
            print(f"FAIL: Title mismatch in {filename}")
            print(f"  Expected: {expected_data['title']}")
            print(f"  Got: {output_data['title']}")
            success = False
        
        # Check outline length
        if len(output_data['outline']) != len(expected_data['outline']):
            print(f"FAIL: Outline length mismatch in {filename}")
            print(f"  Expected: {len(expected_data['outline'])} headings")
            print(f"  Got: {len(output_data['outline'])} headings")
            success = False
            
            # Continue with partial validation
            min_length = min(len(output_data['outline']), len(expected_data['outline']))
            print(f"  Continuing validation with first {min_length} headings")
            
            # Truncate outlines for comparison
            output_outline = output_data['outline'][:min_length]
            expected_outline = expected_data['outline'][:min_length]
        else:
            output_outline = output_data['outline']
            expected_outline = expected_data['outline']
        
        # Check each heading
        for i, (output_heading, expected_heading) in enumerate(zip(output_outline, expected_outline)):
            # Check heading structure
            if not all(key in output_heading for key in ['level', 'text', 'page']):
                print(f"FAIL: Invalid heading structure at index {i} in {filename}")
                success = False
                continue
                
            # Check heading level
            if output_heading['level'] != expected_heading['level']:
                print(f"FAIL: Heading level mismatch at index {i} in {filename}")
                print(f"  Expected: {expected_heading['level']}")
                print(f"  Got: {output_heading['level']}")
                success = False
            
            # Check heading text
            if output_heading['text'] != expected_heading['text']:
                print(f"FAIL: Heading text mismatch at index {i} in {filename}")
                print(f"  Expected: {expected_heading['text']}")
                print(f"  Got: {output_heading['text']}")
                success = False
            
            # Check page number
            if output_heading['page'] != expected_heading['page']:
                print(f"FAIL: Page number mismatch at index {i} in {filename}")
                print(f"  Expected: {expected_heading['page']}")
                print(f"  Got: {output_heading['page']}")
                success = False
        
        # Report success for this file
        if success:
            print(f"PASS: {filename}")
    
    return success

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python validate_output.py output_dir expected_dir")
        sys.exit(1)
        
    output_dir = sys.argv[1]
    expected_dir = sys.argv[2]
    
    print(f"Validating output in {output_dir} against expected results in {expected_dir}")
    
    if validate_output(output_dir, expected_dir):
        print("All tests passed!")
        sys.exit(0)
    else:
        print("Some tests failed.")
        sys.exit(1) 