#!/usr/bin/env python
"""
Script to check for potentially problematic imports in the codebase.

This script scans all Python files in the project and identifies import statements
that might be importing from outdated or incorrect modules.
"""

import os
import re
import sys
from typing import List, Dict, Set, Tuple

# Define patterns to look for
PROBLEMATIC_IMPORTS = [
    # Format: (pattern, suggested_replacement, description)
    (r"from src\.core\.workflow import WorkflowEngine", 
     "from src.core.workflow.workflow_engine_new import WorkflowEngine", 
     "Using abstract WorkflowEngine class instead of concrete implementation"),
    
    (r"from src\.core\.workflow\.workflow_engine import WorkflowEngine", 
     "from src.core.workflow.workflow_engine_new import WorkflowEngine", 
     "Using old WorkflowEngine implementation instead of new one"),
    
    (r"from src\.core\.workflow import WorkflowService, WorkflowValidationError", 
     "from src.core.workflow.workflow_service import WorkflowService\nfrom src.core.workflow.exceptions import WorkflowValidationError", 
     "Importing WorkflowValidationError from wrong module"),
    
    (r"from src\.core\.workflow\.workflow_service import .*WorkflowValidationError", 
     "from src.core.workflow.exceptions import WorkflowValidationError", 
     "Importing WorkflowValidationError from wrong module"),
    
    # Add more patterns as needed
]

def scan_file(file_path: str) -> List[Tuple[int, str, str, str]]:
    """
    Scan a file for problematic imports.
    
    Args:
        file_path: Path to the file to scan
        
    Returns:
        List of tuples (line_number, line, suggested_replacement, description)
    """
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            line_number = i + 1
            for pattern, replacement, description in PROBLEMATIC_IMPORTS:
                if re.search(pattern, line):
                    issues.append((line_number, line.strip(), replacement, description))
    except Exception as e:
        print(f"Error scanning {file_path}: {e}")
    
    return issues

def scan_directory(directory: str) -> Dict[str, List[Tuple[int, str, str, str]]]:
    """
    Recursively scan a directory for problematic imports.
    
    Args:
        directory: Directory to scan
        
    Returns:
        Dictionary mapping file paths to lists of issues
    """
    all_issues = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                issues = scan_file(file_path)
                if issues:
                    all_issues[file_path] = issues
    
    return all_issues

def main():
    """Main entry point."""
    # Get the project root directory
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()
    
    print(f"Scanning {project_root} for problematic imports...")
    
    # Scan the project
    issues = scan_directory(project_root)
    
    # Report issues
    if issues:
        print("\nPotentially problematic imports found:")
        print("=====================================\n")
        
        for file_path, file_issues in issues.items():
            print(f"\n{file_path}:")
            print("-" * len(file_path))
            
            for line_number, line, replacement, description in file_issues:
                print(f"Line {line_number}: {line}")
                print(f"Issue: {description}")
                print(f"Suggested replacement: {replacement}")
                print()
        
        print(f"\nTotal files with issues: {len(issues)}")
        total_issues = sum(len(file_issues) for file_issues in issues.values())
        print(f"Total issues found: {total_issues}")
    else:
        print("\nNo problematic imports found.")

if __name__ == "__main__":
    main()
