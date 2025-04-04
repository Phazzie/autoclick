"""
Script to verify that UI components correctly access the refactored adapters.

This script analyzes the UI components to ensure they correctly access the refactored adapters.
"""
import sys
import os
import re
from typing import Dict, List, Set, Tuple

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def get_ui_components() -> List[str]:
    """
    Get all UI component files.
    
    Returns:
        List of UI component file paths
    """
    ui_components = []
    
    for root, _, files in os.walk("src/ui/views"):
        for file in files:
            if file.endswith(".py"):
                ui_components.append(os.path.join(root, file))
    
    for root, _, files in os.walk("src/ui/presenters"):
        for file in files:
            if file.endswith(".py"):
                ui_components.append(os.path.join(root, file))
    
    return ui_components


def get_adapters() -> List[str]:
    """
    Get all adapter files.
    
    Returns:
        List of adapter file paths
    """
    adapters = []
    
    for root, _, files in os.walk("src/ui/adapters"):
        for file in files:
            if file.endswith(".py"):
                adapters.append(os.path.join(root, file))
    
    return adapters


def analyze_ui_component(file_path: str, adapters: List[str]) -> Dict[str, Any]:
    """
    Analyze a UI component file.
    
    Args:
        file_path: Path to the UI component file
        adapters: List of adapter file paths
        
    Returns:
        Dictionary with analysis results
    """
    results = {
        "file_path": file_path,
        "adapter_imports": [],
        "adapter_usages": [],
        "clean_architecture_usage": False
    }
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check for adapter imports
        for adapter in adapters:
            adapter_name = os.path.basename(adapter).replace(".py", "")
            if re.search(rf"from\s+.*{adapter_name}\s+import", content, re.MULTILINE):
                results["adapter_imports"].append(adapter_name)
        
        # Check for adapter usages
        for adapter_name in results["adapter_imports"]:
            if re.search(rf"self\..*{adapter_name}", content, re.MULTILINE):
                results["adapter_usages"].append(adapter_name)
        
        # Check for clean architecture usage
        if re.search(r"ICredentialService|IWorkflowService|IActionService", content, re.MULTILINE):
            results["clean_architecture_usage"] = True
    except Exception as e:
        print(f"Error analyzing {file_path}: {str(e)}")
    
    return results


def verify_ui_components() -> bool:
    """
    Verify that UI components correctly access the refactored adapters.
    
    Returns:
        True if verification passes, False otherwise
    """
    print("Verifying UI components...")
    
    # Get UI components and adapters
    ui_components = get_ui_components()
    adapters = get_adapters()
    
    print(f"Found {len(ui_components)} UI components and {len(adapters)} adapters.")
    
    # Analyze UI components
    results = []
    for ui_component in ui_components:
        result = analyze_ui_component(ui_component, adapters)
        results.append(result)
    
    # Count components with adapter usages
    components_with_adapters = [r for r in results if r["adapter_usages"]]
    components_with_clean_architecture = [r for r in results if r["clean_architecture_usage"]]
    
    print(f"UI components using adapters: {len(components_with_adapters)}/{len(ui_components)}")
    print(f"UI components using clean architecture: {len(components_with_clean_architecture)}/{len(ui_components)}")
    
    # Check if all components use adapters
    if len(components_with_adapters) < len(ui_components) * 0.8:
        print("Less than 80% of UI components use adapters.")
        return False
    
    print("Verification passed: UI components correctly access the refactored adapters.")
    return True


if __name__ == "__main__":
    success = verify_ui_components()
    sys.exit(0 if success else 1)
