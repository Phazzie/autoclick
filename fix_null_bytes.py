#!/usr/bin/env python
"""
Null Byte Fixer for AUTOCLICK

This script detects and removes null bytes from Python files.

Usage:
    python fix_null_bytes.py
"""
import os
import sys

def find_python_files(directory='.'):
    """Find all Python files in the directory."""
    python_files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                python_files.append(os.path.join(root, filename))
    return python_files

def has_null_bytes(content):
    """Check if the content has null bytes."""
    return '\0' in content

def remove_null_bytes(content):
    """Remove null bytes from the content."""
    return content.replace('\0', '')

def fix_file(file_path):
    """Fix null bytes in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read {file_path}: {e}")
        return False

    if has_null_bytes(content):
        fixed_content = remove_null_bytes(content)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Removed null bytes from: {file_path}")
            return True
        except Exception as e:
            print(f"ERROR: Could not write to {file_path}: {e}")
            return False
    
    return False

def main():
    """Main function to run the null byte fixer."""
    print("\n" + "=" * 80)
    print("AUTOCLICK Null Byte Fixer".center(80))
    print("=" * 80 + "\n")
    
    # Find all Python files
    print("Scanning for Python files...")
    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files.")
    
    # Fix null bytes
    print("\nRemoving null bytes...")
    fixed_count = 0
    for file_path in python_files:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\nRemoved null bytes from {fixed_count} file(s)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
