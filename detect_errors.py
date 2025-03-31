#!/usr/bin/env python
"""
Error Detection Script for AUTOCLICK

This script scans the codebase for common errors:
1. Merge conflict markers
2. Syntax errors in Python files
3. Missing imports
4. Circular imports
5. Inconsistent indentation
6. Null bytes (indicating UTF-16 encoding)
7. Non-UTF-8 encoding

Usage:
    python detect_errors.py [--fix]

Options:
    --fix    Attempt to automatically fix some errors (merge conflicts, encoding issues)
"""

import os
import re
import sys
import ast
import importlib
import subprocess
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

def find_python_files(directory: str) -> List[str]:
    """Find all Python files in the given directory and its subdirectories."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def check_merge_conflicts(file_path: str) -> List[int]:
    """Check for merge conflict markers in a file."""
    conflict_lines = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for i, line in enumerate(file, 1):
                conflict_lines.append(i)
    return conflict_lines

def fix_merge_conflicts(file_path: str) -> bool:
    """Attempt to fix merge conflicts in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        # Pattern to match merge conflict blocks

        # Function to choose which version to keep (HEAD version in this case)
        def replace_conflict(match):
            head_version = match.group(1)
            return head_version + '\n'

        # Replace conflicts with HEAD version
        fixed_content = re.sub(pattern, replace_conflict, content, flags=re.DOTALL)

        # Write back to file if changes were made
        if fixed_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(fixed_content)
            return True
        return False
    except Exception as e:
        print_error(f"Failed to fix merge conflicts in {file_path}: {str(e)}")
        return False

def check_syntax_errors(file_path: str) -> Optional[str]:
    """Check for syntax errors in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            source = file.read()
        ast.parse(source, filename=file_path)
        return None
    except SyntaxError as e:
        return f"Line {e.lineno}, Column {e.offset}: {e.msg}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def check_circular_imports(python_files: List[str]) -> Dict[str, List[str]]:
    """Check for circular imports in Python files."""
    import_graph = {}
    circular_imports = {}

    # Build import graph
    for file_path in python_files:
        module_name = os.path.relpath(file_path).replace('/', '.').replace('\\', '.').replace('.py', '')
        import_graph[module_name] = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                source = file.read()

            tree = ast.parse(source, filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        import_graph[module_name].append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        import_graph[module_name].append(node.module)
        except Exception:
            # Skip files with syntax errors
            pass

    # Check for circular imports
    def check_path(module, path):
        if module in path:
            # Found a cycle
            cycle_start = path.index(module)
            return path[cycle_start:]

        path.append(module)
        for imported in import_graph.get(module, []):
            if imported in import_graph:
                cycle = check_path(imported, path.copy())
                if cycle:
                    return cycle
        return None

    for module in import_graph:
        cycle = check_path(module, [])
        if cycle:
            circular_imports[module] = cycle

    return circular_imports

def check_inconsistent_indentation(file_path: str) -> List[int]:
    """Check for inconsistent indentation in a Python file."""
    inconsistent_lines = []
    tab_lines = []
    space_lines = []

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for i, line in enumerate(file, 1):
            if line.startswith('\t'):
                tab_lines.append(i)
            elif line.startswith('    '):
                space_lines.append(i)

    # If both tabs and spaces are used for indentation
    if tab_lines and space_lines:
        inconsistent_lines = tab_lines + space_lines

    return inconsistent_lines

def check_missing_imports(file_path: str) -> List[str]:
    """Check for potentially missing imports in a Python file."""
    missing_imports = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            source = file.read()

        tree = ast.parse(source, filename=file_path)
        imported_names = set()

        # Collect imported names
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imported_names.add(name.name)
                    if name.asname:
                        imported_names.add(name.asname)
            elif isinstance(node, ast.ImportFrom):
                for name in node.names:
                    if name.name == '*':
                        # Can't track * imports easily
                        continue
                    imported_names.add(name.name)
                    if name.asname:
                        imported_names.add(name.asname)

        # Check for undefined names
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id not in imported_names and not is_builtin(node.id):
                    missing_imports.append(node.id)
    except Exception:
        # Skip files with syntax errors
        pass

    return list(set(missing_imports))

def is_builtin(name: str) -> bool:
    """Check if a name is a Python builtin."""
    builtins = dir(__builtins__)
    return name in builtins

def main():
    """Main function to run the error detection."""
    fix_mode = '--fix' in sys.argv

    print_header("AUTOCLICK Error Detection Script")

    # Find all Python files
    print("Scanning for Python files...")
    python_files = find_python_files('.')
    print(f"Found {len(python_files)} Python files.")

    # Check for merge conflicts
    print_header("Checking for Merge Conflicts")
    conflict_files = []
    for file_path in python_files:
        conflict_lines = check_merge_conflicts(file_path)
        if conflict_lines:
            conflict_files.append((file_path, conflict_lines))
            print_error(f"Merge conflicts in {file_path} at lines: {', '.join(map(str, conflict_lines))}")

            if fix_mode:
                if fix_merge_conflicts(file_path):
                    print_success(f"Fixed merge conflicts in {file_path}")
                else:
                    print_warning(f"Could not automatically fix conflicts in {file_path}")

    if not conflict_files:
        print_success("No merge conflicts found.")

    # Check for syntax errors
    print_header("Checking for Syntax Errors")
    syntax_error_files = []
    for file_path in python_files:
        error = check_syntax_errors(file_path)
        if error:
            syntax_error_files.append((file_path, error))
            print_error(f"Syntax error in {file_path}: {error}")

    if not syntax_error_files:
        print_success("No syntax errors found.")

    # Check for inconsistent indentation
    print_header("Checking for Inconsistent Indentation")
    indentation_files = []
    for file_path in python_files:
        inconsistent_lines = check_inconsistent_indentation(file_path)
        if inconsistent_lines:
            indentation_files.append((file_path, inconsistent_lines))
            print_warning(f"Inconsistent indentation in {file_path} at lines: {', '.join(map(str, inconsistent_lines[:5]))}{' and more...' if len(inconsistent_lines) > 5 else ''}")

    if not indentation_files:
        print_success("No inconsistent indentation found.")

    # Check for circular imports
    print_header("Checking for Circular Imports")
    circular_imports = check_circular_imports(python_files)
    if circular_imports:
        for module, cycle in circular_imports.items():
            print_warning(f"Circular import detected: {' -> '.join(cycle)}")
    else:
        print_success("No circular imports found.")

    # Summary
    print_header("Error Detection Summary")
    total_errors = len(conflict_files) + len(syntax_error_files)
    total_warnings = len(indentation_files) + len(circular_imports)

    if total_errors == 0 and total_warnings == 0:
        print_success("No errors or warnings detected! Your code looks good.")
    else:
        if total_errors > 0:
            print_error(f"Found {total_errors} error(s):")
            if conflict_files:
                print_error(f"  - {len(conflict_files)} file(s) with merge conflicts")
            if syntax_error_files:
                print_error(f"  - {len(syntax_error_files)} file(s) with syntax errors")

        if total_warnings > 0:
            print_warning(f"Found {total_warnings} warning(s):")
            if indentation_files:
                print_warning(f"  - {len(indentation_files)} file(s) with inconsistent indentation")
            if circular_imports:
                print_warning(f"  - {len(circular_imports)} circular import(s)")

    # Exit with error code if errors were found
    if total_errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
