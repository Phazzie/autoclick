#!/usr/bin/env python
"""
Circular Dependency Analyzer and Fixer for AUTOCLICK

This script:
1. Detects circular dependencies in the codebase
2. Provides detailed information about each circular dependency
3. Suggests potential fixes

Usage:
    python fix_circular_dependencies.py
"""
import os
import sys
import ast
import importlib.util
from collections import defaultdict, deque

def find_python_files(directory='.'):
    """Find all Python files in the directory."""
    python_files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                python_files.append(os.path.join(root, filename))
    return python_files

def module_path_to_name(file_path):
    """Convert a file path to a module name."""
    # Remove .py extension
    if file_path.endswith('.py'):
        file_path = file_path[:-3]

    # Replace directory separators with dots
    module_name = file_path.replace(os.path.sep, '.')

    # Remove leading dots
    if module_name.startswith('.'):
        module_name = module_name[1:]

    return module_name

def get_imports(file_path):
    """Extract all imports from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        tree = ast.parse(content)
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append(name.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    # Handle relative imports
                    if node.level > 0:
                        # Get the directory of the current file
                        current_dir = os.path.dirname(file_path)

                        # Go up by node.level directories
                        for _ in range(node.level):
                            current_dir = os.path.dirname(current_dir)

                        # Construct the full module name
                        if current_dir:
                            module_name = current_dir.replace(os.path.sep, '.') + '.' + node.module
                        else:
                            module_name = node.module
                    else:
                        module_name = node.module

                    # Add the full import path for each imported name
                    for name in node.names:
                        if name.name != '*':
                            full_import = f"{module_name}.{name.name}"
                            imports.append(full_import)
                        else:
                            imports.append(module_name)

        return imports
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return []

def build_dependency_graph(python_files):
    """Build a dependency graph from Python files."""
    graph = defaultdict(set)
    file_to_module = {}

    # Map file paths to module names
    for file_path in python_files:
        module_name = module_path_to_name(file_path)
        file_to_module[file_path] = module_name

    # Build the graph
    for file_path in python_files:
        module_name = file_to_module[file_path]
        imports = get_imports(file_path)

        for imported_module in imports:
            # Check if the imported module is in our codebase
            for other_module in file_to_module.values():
                if imported_module == other_module or imported_module.startswith(other_module + '.'):
                    graph[module_name].add(other_module)

    return graph, file_to_module

def find_cycles(graph):
    """Find all cycles in the dependency graph."""
    cycles = []
    visited = set()

    def dfs(node, path, start_node):
        if node in path:
            # Found a cycle
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return

        if node in visited:
            return

        visited.add(node)
        path.append(node)

        for neighbor in graph[node]:
            if neighbor == start_node or neighbor not in path:
                dfs(neighbor, path.copy(), start_node)

    for node in graph:
        dfs(node, [], node)

    # Remove duplicates
    unique_cycles = []
    for cycle in cycles:
        # Normalize the cycle by rotating to start with the smallest node
        min_index = cycle.index(min(cycle))
        normalized_cycle = cycle[min_index:] + cycle[:min_index]

        # Check if this normalized cycle is already in unique_cycles
        if normalized_cycle not in unique_cycles:
            unique_cycles.append(normalized_cycle)

    return unique_cycles

def suggest_fixes(cycles, graph, file_to_module):
    """Suggest fixes for circular dependencies."""
    suggestions = []

    for cycle in cycles:
        # Find the module with the most dependencies
        max_deps = 0
        max_deps_module = None

        for module in cycle:
            deps = len(graph[module])
            if deps > max_deps:
                max_deps = deps
                max_deps_module = module

        # Find the file path for this module
        module_file = None
        for file_path, module_name in file_to_module.items():
            if module_name == max_deps_module:
                module_file = file_path
                break

        # Suggest moving the import inside a function or method
        suggestion = {
            "cycle": cycle,
            "problematic_module": max_deps_module,
            "file_path": module_file,
            "fix": "Consider moving the import inside a function or method, or create a new module to break the cycle."
        }

        suggestions.append(suggestion)

    return suggestions

def main():
    """Main function to run the circular dependency analyzer."""
    print("\n" + "=" * 80)
    print("AUTOCLICK Circular Dependency Analyzer".center(80))
    print("=" * 80 + "\n")

    # Find all Python files
    print("Scanning for Python files...")
    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files.")

    # Build dependency graph
    print("\nBuilding dependency graph...")
    graph, file_to_module = build_dependency_graph(python_files)
    print(f"Found {len(graph)} modules with dependencies.")

    # Find cycles
    print("\nAnalyzing circular dependencies...")
    cycles = find_cycles(graph)
    print(f"Found {len(cycles)} circular dependencies.")

    if cycles:
        # Suggest fixes
        print("\nSuggested fixes:")
        suggestions = suggest_fixes(cycles, graph, file_to_module)

        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. Circular dependency: {' -> '.join(suggestion['cycle'])}")
            print(f"   Problematic module: {suggestion['problematic_module']}")
            print(f"   File path: {suggestion['file_path']}")
            print(f"   Suggested fix: {suggestion['fix']}")
    else:
        print("\nNo circular dependencies found. Your codebase is clean!")

    return 0

if __name__ == "__main__":
    sys.exit(main())
