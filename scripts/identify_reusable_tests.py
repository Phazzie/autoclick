#!/usr/bin/env python
"""
Script to identify which tests can be kept based on the components we're keeping.

This script analyzes the test files in the project and matches them to their
corresponding implementation files, then categorizes them based on our
"keep/discard/maybe" analysis.
"""

import os
import re
import json
from typing import Dict, List, Tuple, Set

# Define the components we're keeping, discarding, and discussing
COMPONENTS_TO_KEEP = [
    'src/core/models.py',
    'src/core/workflow/interfaces.py',
    'src/core/workflow/workflow_engine_new.py',
    'src/core/workflow/workflow_validator.py',
    'src/core/events/event_bus.py',
    'src/core/events/workflow_events.py',
    'src/core/workflow/exceptions.py',
    'src/core/workflow/execution_result.py',
]

COMPONENTS_TO_DISCARD = [
    'src/core/workflow/workflow_engine.py',
    'src/core/workflow/engine/workflow_validator.py',
    'src/core/workflow/workflow_engine_interface.py',
    'src/core/workflow/workflow_validation_service.py',
    'src/ui/views/workflow_view.py',
    'src/ui/presenters/workflow_presenter.py',
    'src/ui/views/action_view.py',
    'src/core/workflow/workflow_serializer.py',
    'src/core/errors/error_handler.py',
    'src/core/errors/error_reporter.py',
]

COMPONENTS_FOR_DISCUSSION = [
    'src/core/workflow/workflow_storage_service.py',
    'src/core/credentials/credential_manager.py',
    'src/core/context/variable_storage.py',
    'src/core/actions/action_factory.py',
    'src/core/workflow/workflow_service.py',
    'src/core/context/execution_context.py',
]

def find_test_files(project_root: str) -> List[str]:
    """Find all test files in the project."""
    test_files = []
    for root, _, files in os.walk(project_root):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                test_files.append(os.path.join(root, file))
    return test_files

def extract_imports(file_path: str) -> Set[str]:
    """Extract all imports from a file."""
    imports = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all import statements
    import_patterns = [
        r'from\s+([\w.]+)\s+import',  # from X import Y
        r'import\s+([\w.]+)'          # import X
    ]
    
    for pattern in import_patterns:
        for match in re.finditer(pattern, content):
            imports.add(match.group(1))
    
    return imports

def match_test_to_implementation(test_file: str, imports: Set[str]) -> List[str]:
    """Match a test file to its implementation files based on imports."""
    matched_files = []
    
    # Convert module paths to file paths
    for imp in imports:
        # Skip standard library imports
        if not imp.startswith('src'):
            continue
        
        # Convert dots to path separators
        file_path = imp.replace('.', '/') + '.py'
        
        # Check if the file exists
        if os.path.exists(file_path):
            matched_files.append(file_path)
    
    return matched_files

def categorize_test(test_file: str, matched_files: List[str]) -> str:
    """Categorize a test file based on the components it tests."""
    # If it tests any component we're keeping, keep the test
    for file in matched_files:
        if file in COMPONENTS_TO_KEEP:
            return "keep"
    
    # If it only tests components we're discarding, discard the test
    if all(file in COMPONENTS_TO_DISCARD for file in matched_files):
        return "discard"
    
    # If it tests any component for discussion, mark it for discussion
    for file in matched_files:
        if file in COMPONENTS_FOR_DISCUSSION:
            return "discuss"
    
    # If we can't determine, mark it for discussion
    return "discuss"

def analyze_tests(project_root: str) -> Dict[str, List[Dict]]:
    """Analyze all test files and categorize them."""
    test_files = find_test_files(project_root)
    results = {
        "keep": [],
        "discard": [],
        "discuss": []
    }
    
    for test_file in test_files:
        imports = extract_imports(test_file)
        matched_files = match_test_to_implementation(test_file, imports)
        category = categorize_test(test_file, matched_files)
        
        results[category].append({
            "test_file": test_file,
            "tests_components": matched_files
        })
    
    return results

def generate_report(results: Dict[str, List[Dict]], output_file: str) -> None:
    """Generate a markdown report of the analysis."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# AUTOCLICK Test Analysis\n\n")
        f.write("This document analyzes which tests can be kept, which should be discarded, and which require further discussion.\n\n")
        
        # Tests to keep
        f.write("## Tests to Keep\n\n")
        if results["keep"]:
            for test in results["keep"]:
                f.write(f"### {os.path.basename(test['test_file'])}\n\n")
                f.write(f"**Path:** `{test['test_file']}`\n\n")
                f.write("**Tests Components:**\n\n")
                for component in test['tests_components']:
                    f.write(f"- `{component}`\n")
                f.write("\n")
        else:
            f.write("No tests identified to keep.\n\n")
        
        # Tests to discard
        f.write("## Tests to Discard\n\n")
        if results["discard"]:
            for test in results["discard"]:
                f.write(f"### {os.path.basename(test['test_file'])}\n\n")
                f.write(f"**Path:** `{test['test_file']}`\n\n")
                f.write("**Tests Components:**\n\n")
                for component in test['tests_components']:
                    f.write(f"- `{component}`\n")
                f.write("\n")
        else:
            f.write("No tests identified to discard.\n\n")
        
        # Tests for discussion
        f.write("## Tests for Discussion\n\n")
        if results["discuss"]:
            for test in results["discuss"]:
                f.write(f"### {os.path.basename(test['test_file'])}\n\n")
                f.write(f"**Path:** `{test['test_file']}`\n\n")
                f.write("**Tests Components:**\n\n")
                for component in test['tests_components']:
                    f.write(f"- `{component}`\n")
                f.write("\n")
        else:
            f.write("No tests identified for discussion.\n\n")

def main():
    """Main entry point."""
    project_root = os.getcwd()
    results = analyze_tests(project_root)
    
    # Generate report
    output_file = os.path.join(project_root, "docs", "AUTOCLICK_Test_Analysis.md")
    generate_report(results, output_file)
    
    print(f"Analysis complete. Report saved to {output_file}")
    
    # Also save the raw results as JSON for further processing
    json_output = os.path.join(project_root, "docs", "test_analysis_results.json")
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Raw results saved to {json_output}")

if __name__ == "__main__":
    main()
