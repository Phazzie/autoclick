"""
Script to fix dependency injection imports.

This script updates imports to avoid circular dependencies.
"""
import sys
import os
import re
from typing import List, Tuple

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def find_files_with_import(import_pattern: str, directory: str) -> List[str]:
    """
    Find files that contain a specific import pattern.
    
    Args:
        import_pattern: Regular expression pattern to match imports
        directory: Directory to search
        
    Returns:
        List of file paths
    """
    matching_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    if re.search(import_pattern, content):
                        matching_files.append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
    
    return matching_files

def update_imports(file_path: str) -> Tuple[bool, str]:
    """
    Update imports in a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Tuple of (success, message)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace imports
        new_content = re.sub(
            r"from\s+src\.infrastructure\.di\s+import\s+configure_container",
            "from src.infrastructure.di.config import configure_container",
            content
        )
        
        # Write the updated content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        return True, f"Updated imports in {file_path}"
    except Exception as e:
        return False, f"Error updating {file_path}: {str(e)}"

def main():
    """Main function to fix dependency injection imports."""
    print("Fixing dependency injection imports...")
    
    # Find files with the problematic import
    print("\nFinding files with problematic imports...")
    files = find_files_with_import(
        r"from\s+src\.infrastructure\.di\s+import\s+configure_container",
        "src"
    )
    
    if not files:
        print("No files found with problematic imports.")
        return True
    
    print(f"Found {len(files)} files with problematic imports:")
    for file in files:
        print(f"  {file}")
    
    # Update imports
    print("\nUpdating imports...")
    success_count = 0
    for file in files:
        success, message = update_imports(file)
        print(f"  {'✓' if success else '✗'} {message}")
        if success:
            success_count += 1
    
    # Print summary
    print(f"\nUpdated {success_count}/{len(files)} files.")
    
    return success_count == len(files)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
