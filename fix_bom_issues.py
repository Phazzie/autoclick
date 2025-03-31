#!/usr/bin/env python
"""
BOM (Byte Order Mark) Fixer for AUTOCLICK

This script detects and removes BOM characters from Python files.

Usage:
    python fix_bom_issues.py
"""
import os
import sys

# BOM (Byte Order Mark) character
BOM = '\ufeff'

def find_python_files(directory='.'):
    """Find all Python files in the directory."""
    python_files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                python_files.append(os.path.join(root, filename))
    return python_files

def has_bom(content):
    """Check if the content has a BOM character."""
    return content.startswith(BOM)

def remove_bom(content):
    """Remove BOM character from the content."""
    if has_bom(content):
        return content[1:]
    return content

def fix_file(file_path):
    """Fix BOM in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read {file_path}: {e}")
        return False

    if has_bom(content):
        fixed_content = remove_bom(content)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Removed BOM from: {file_path}")
            return True
        except Exception as e:
            print(f"ERROR: Could not write to {file_path}: {e}")
            return False
    
    return False

def main():
    """Main function to run the BOM fixer."""
    print("\n" + "=" * 80)
    print("AUTOCLICK BOM Fixer".center(80))
    print("=" * 80 + "\n")
    
    # Find all Python files
    print("Scanning for Python files...")
    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files.")
    
    # Fix BOM
    print("\nRemoving BOM characters...")
    fixed_count = 0
    for file_path in python_files:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\nRemoved BOM from {fixed_count} file(s)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
