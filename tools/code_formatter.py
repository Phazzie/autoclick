"""Code formatter tool to automatically fix common code quality issues"""
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Set


def find_python_files(directory: Path) -> List[Path]:
    """Find all Python files in the given directory and its subdirectories"""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)
    return python_files


def fix_trailing_whitespace(file_path: Path) -> bool:
    """Remove trailing whitespace from a file"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove trailing whitespace
    new_content = re.sub(r"[ \t]+$", "", content, flags=re.MULTILINE)

    # Ensure file ends with a newline
    if not new_content.endswith("\n"):
        new_content += "\n"

    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def run_black(file_paths: List[Path]) -> bool:
    """Run black on the given files"""
    try:
        # Run black on each file individually to avoid encoding issues
        for file_path in file_paths:
            try:
                subprocess.run(
                    ["black", str(file_path)], capture_output=True, check=False
                )
            except Exception as e:
                print(f"Warning: Could not format {file_path}: {e}")
        return True
    except Exception as e:
        print(f"Error running black: {e}")
        return False


def run_isort(file_paths: List[Path]) -> bool:
    """Run isort on the given files to fix import order"""
    try:
        # Run isort on each file individually to avoid encoding issues
        for file_path in file_paths:
            try:
                subprocess.run(
                    ["isort", str(file_path)], capture_output=True, check=False
                )
            except Exception as e:
                print(f"Warning: Could not fix imports in {file_path}: {e}")
        return True
    except Exception as e:
        print(f"Error running isort: {e}")
        return False


def format_code() -> bool:
    """Format all Python files in the project"""
    project_root = Path(__file__).parent.parent
    print(f"Formatting code in: {project_root}")

    # Find all Python files
    python_files = find_python_files(project_root / "src")
    python_files.extend(find_python_files(project_root / "tests"))
    python_files.extend(find_python_files(project_root / "tools"))

    # Add root Python files
    for file in project_root.glob("*.py"):
        python_files.append(file)

    # Fix trailing whitespace and ensure final newline
    fixed_whitespace_count = 0
    for file in python_files:
        if fix_trailing_whitespace(file):
            fixed_whitespace_count += 1

    if fixed_whitespace_count > 0:
        print(f"✅ Fixed trailing whitespace in {fixed_whitespace_count} files")

    # Fix import order with isort
    if run_isort(python_files):
        print("✅ Fixed import order with isort")
    else:
        print("❌ Failed to fix import order")

    # Format code with black
    if run_black(python_files):
        print("✅ Formatted code with black")
    else:
        print("❌ Failed to format code with black")

    print("\n✅ Code formatting complete!")
    return True


if __name__ == "__main__":
    success = format_code()
    sys.exit(0 if success else 1)
