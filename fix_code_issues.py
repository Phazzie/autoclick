#!/usr/bin/env python
"""
Code Issue Fixer for AUTOCLICK

This script detects and fixes common issues in the codebase:
1. Merge conflict markers
2. Null bytes in files
3. Syntax errors (detection only)

Usage:
    python fix_code_issues.py [--check-only]

Options:
    --check-only    Only check for issues without fixing them
"""

import os
import re
import sys
import ast
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Set, Optional

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_error(text: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}{Colors.BOLD}ERROR: {text}{Colors.ENDC}")

def print_warning(text: str) -> None:
    """Print a warning message."""
    print(f"{Colors.YELLOW}WARNING: {text}{Colors.ENDC}")

def print_success(text: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}{text}{Colors.ENDC}")

def print_info(text: str) -> None:
    """Print an info message."""
    print(f"{Colors.BLUE}{text}{Colors.ENDC}")

def find_files(directory: str, extensions: List[str]) -> List[str]:
    """Find all files with the given extensions in the directory and its subdirectories."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, filename))
    return files

def check_merge_conflicts(file_path: str) -> List[int]:
    """Check for merge conflict markers in a file."""
    conflict_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for i, line in enumerate(file, 1):
                if line.startswith('<<<<<<<') or line.startswith('=======') or line.startswith('>>>>>>>'):
                    conflict_lines.append(i)
    except Exception as e:
        print_error(f"Error reading {file_path}: {str(e)}")
    return conflict_lines

def fix_merge_conflicts(file_path: str) -> bool:
    """Fix merge conflicts in a file by keeping the HEAD version."""
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        # Check if there are merge conflicts
        if '<<<<<<<' not in content:
            return False

        # Process the content line by line to handle merge conflicts
        lines = content.split('\n')
        fixed_lines = []
        in_conflict = False
        keep_lines = []
        skip_lines = False

        for line in lines:
            if line.startswith('<<<<<<<'):
                in_conflict = True
                skip_lines = False
                continue
            elif line.startswith('======='):
                skip_lines = True
                continue
            elif line.startswith('>>>>>>>'):
                in_conflict = False
                skip_lines = False
                continue

            if not skip_lines:
                fixed_lines.append(line)

        # Write the fixed content back to the file
        fixed_content = '\n'.join(fixed_lines)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(fixed_content)

        return True
    except Exception as e:
        print_error(f"Failed to fix merge conflicts in {file_path}: {str(e)}")
        return False

def check_null_bytes(file_path: str) -> bool:
    """Check if a file contains null bytes."""
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            return b'\x00' in content
    except Exception as e:
        print_error(f"Error reading {file_path}: {str(e)}")
        return False

def fix_null_bytes(file_path: str) -> bool:
    """Fix null bytes in a file by removing them."""
    try:
        # Read file content in binary mode
        with open(file_path, 'rb') as file:
            content = file.read()

        # Check if there are null bytes
        if b'\x00' not in content:
            return False

        # Remove null bytes
        fixed_content = content.replace(b'\x00', b'')

        # Write the fixed content back to the file
        with open(file_path, 'wb') as file:
            file.write(fixed_content)

        return True
    except Exception as e:
        print_error(f"Failed to fix null bytes in {file_path}: {str(e)}")
        return False

def check_syntax(file_path: str) -> Optional[str]:
    """Check for syntax errors in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        # Try to parse the file
        ast.parse(content, filename=file_path)
        return None
    except SyntaxError as e:
        return f"Line {e.lineno}, Column {e.offset}: {e.msg}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def main():
    """Main function to run the code issue fixer."""
    parser = argparse.ArgumentParser(description='Fix common code issues in the AUTOCLICK codebase.')
    parser.add_argument('--check-only', action='store_true', help='Only check for issues without fixing them')
    args = parser.parse_args()

    check_only = args.check_only

    print_header("AUTOCLICK Code Issue Fixer")

    # Find all relevant files
    print_info("Scanning for files...")
    python_files = find_files('.', ['.py'])
    print_info(f"Found {len(python_files)} Python files.")

    # Check and fix merge conflicts
    print_header("Checking for Merge Conflicts")
    conflict_files = []
    fixed_conflict_files = []

    for file_path in python_files:
        conflict_lines = check_merge_conflicts(file_path)
        if conflict_lines:
            conflict_files.append((file_path, conflict_lines))
            print_error(f"Merge conflicts in {file_path} at lines: {', '.join(map(str, conflict_lines))}")

            if not check_only:
                if fix_merge_conflicts(file_path):
                    fixed_conflict_files.append(file_path)
                    print_success(f"Fixed merge conflicts in {file_path}")
                else:
                    print_warning(f"Could not fix merge conflicts in {file_path}")

    if not conflict_files:
        print_success("No merge conflicts found.")

    # Check and fix null bytes
    print_header("Checking for Null Bytes")
    null_byte_files = []
    fixed_null_byte_files = []

    for file_path in python_files:
        if check_null_bytes(file_path):
            null_byte_files.append(file_path)
            print_error(f"Null bytes found in {file_path}")

            if not check_only:
                if fix_null_bytes(file_path):
                    fixed_null_byte_files.append(file_path)
                    print_success(f"Fixed null bytes in {file_path}")
                else:
                    print_warning(f"Could not fix null bytes in {file_path}")

    if not null_byte_files:
        print_success("No null bytes found.")

    # Check for syntax errors
    print_header("Checking for Syntax Errors")
    syntax_error_files = []

    for file_path in python_files:
        error = check_syntax(file_path)
        if error:
            syntax_error_files.append((file_path, error))
            print_error(f"Syntax error in {file_path}: {error}")

    if not syntax_error_files:
        print_success("No syntax errors found.")

    # Summary
    print_header("Issue Fixing Summary")

    if check_only:
        print_info("Check-only mode: No fixes were applied.")

    total_issues = len(conflict_files) + len(null_byte_files) + len(syntax_error_files)
    total_fixed = len(fixed_conflict_files) + len(fixed_null_byte_files)

    if total_issues == 0:
        print_success("No issues found! Your code looks good.")
    else:
        print_info(f"Found {total_issues} issue(s):")
        if conflict_files:
            print_info(f"  - {len(conflict_files)} file(s) with merge conflicts")
        if null_byte_files:
            print_info(f"  - {len(null_byte_files)} file(s) with null bytes")
        if syntax_error_files:
            print_info(f"  - {len(syntax_error_files)} file(s) with syntax errors")

        if not check_only:
            print_info(f"Fixed {total_fixed} issue(s):")
            if fixed_conflict_files:
                print_success(f"  - Fixed merge conflicts in {len(fixed_conflict_files)} file(s)")
            if fixed_null_byte_files:
                print_success(f"  - Fixed null bytes in {len(fixed_null_byte_files)} file(s)")

            remaining_issues = total_issues - total_fixed
            if remaining_issues > 0:
                print_warning(f"{remaining_issues} issue(s) could not be fixed automatically.")
                print_warning("Please fix these issues manually.")

    # Exit with error code if issues were found and not all were fixed
    if total_issues > 0 and (check_only or total_fixed < total_issues):
        sys.exit(1)

if __name__ == "__main__":
    main()
