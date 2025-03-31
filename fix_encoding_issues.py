#!/usr/bin/env python
"""
Encoding Fixer for AUTOCLICK

This script detects and fixes encoding issues in Python files by converting them to UTF-8.

Usage:
    python fix_encoding_issues.py
"""
import os
import sys
import codecs

def find_python_files(directory='.'):
    """Find all Python files in the directory."""
    python_files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                python_files.append(os.path.join(root, filename))
    return python_files

def detect_encoding(file_path):
    """Detect the encoding of a file."""
    encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue
    
    return None

def fix_file(file_path):
    """Fix encoding issues in a file by converting to UTF-8."""
    # Detect the current encoding
    encoding = detect_encoding(file_path)
    
    if encoding is None:
        print(f"ERROR: Could not detect encoding for {file_path}")
        return False
    
    if encoding == 'utf-8':
        # Already UTF-8, no need to fix
        return False
    
    try:
        # Read with detected encoding
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        
        # Write with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Converted {file_path} from {encoding} to UTF-8")
        return True
    except Exception as e:
        print(f"ERROR: Could not convert {file_path}: {e}")
        return False

def main():
    """Main function to run the encoding fixer."""
    print("\n" + "=" * 80)
    print("AUTOCLICK Encoding Fixer".center(80))
    print("=" * 80 + "\n")
    
    # Find all Python files
    print("Scanning for Python files...")
    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files.")
    
    # Fix encoding issues
    print("\nFixing encoding issues...")
    fixed_count = 0
    for file_path in python_files:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\nFixed encoding in {fixed_count} file(s)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
