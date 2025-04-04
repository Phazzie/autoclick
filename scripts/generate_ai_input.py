#!/usr/bin/env python
"""
Script to generate a comprehensive input file for an AI to analyze and fix problematic components.

This script:
1. Extracts information about problematic components from our analysis
2. Includes the actual code of these components
3. Describes the specific issues with each component
4. Suggests potential fixes or approaches
5. Outputs everything to a single text file that can be uploaded to an AI
"""

import os
import json
import datetime
from typing import Dict, List, Set

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

# Define issues with each component
COMPONENT_ISSUES = {
    'src/core/workflow/workflow_engine.py': [
        "Missing implementation of abstract methods",
        "Overly rigid validation rules",
        "Doesn't handle different workflow structures",
        "Caused the application to fail"
    ],
    'src/core/workflow/engine/workflow_validator.py': [
        "Too strict validation rules (requiring End nodes)",
        "Doesn't handle different workflow structures",
        "Not flexible enough for real-world use",
        "Creates poor user experience"
    ],
    'src/core/workflow/workflow_engine_interface.py': [
        "Too complex with too many responsibilities",
        "Violates Interface Segregation Principle",
        "Has methods that aren't needed in all implementations",
        "Led to implementation difficulties"
    ],
    'src/core/workflow/workflow_validation_service.py': [
        "Duplicates functionality already in the validator",
        "Not properly integrated with the architecture",
        "Creates confusion about where validation logic should live",
        "Adds complexity without clear benefits"
    ],
    'src/ui/views/workflow_view.py': [
        "Direct dependencies on workflow service implementation",
        "Mixes presentation and business logic",
        "Complex event handling that's difficult to test",
        "Tightly coupled to specific UI framework"
    ],
    'src/ui/presenters/workflow_presenter.py': [
        "Directly references backend services",
        "Doesn't use proper dependency injection",
        "Handles too many responsibilities",
        "Difficult to test in isolation"
    ],
    'src/ui/views/action_view.py': [
        "Tightly coupled to specific action implementations",
        "Doesn't use proper abstraction",
        "UI logic mixed with business logic",
        "Difficult to extend with new action types"
    ],
    'src/core/workflow/workflow_serializer.py': [
        "Overly complex serialization/deserialization",
        "Different formats for storage vs. memory",
        "Multiple conversion steps",
        "Potential for bugs and inconsistencies"
    ],
    'src/core/errors/error_handler.py': [
        "Different error handling patterns",
        "Mixes exceptions and return codes",
        "Unclear error messages",
        "Difficult to debug"
    ],
    'src/core/errors/error_reporter.py': [
        "Inconsistent reporting format",
        "Tightly coupled to specific UI framework",
        "Difficult to configure for different environments",
        "Not properly integrated with logging system"
    ],
}

def read_file_content(file_path: str) -> str:
    """Read the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_file_info(file_path: str) -> Dict:
    """Get information about a file."""
    try:
        stats = os.stat(file_path)
        created = datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modified = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        size = stats.st_size
        return {
            "path": file_path,
            "created": created,
            "modified": modified,
            "size": size
        }
    except Exception as e:
        return {
            "path": file_path,
            "error": str(e)
        }

def generate_ai_input(output_file: str) -> None:
    """Generate a comprehensive input file for an AI."""
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("# AUTOCLICK Project Analysis for AI\n\n")
        f.write("This document provides a comprehensive analysis of the AUTOCLICK project, ")
        f.write("focusing on problematic components that need to be fixed or replaced.\n\n")
        
        # Write project overview
        f.write("## Project Overview\n\n")
        f.write("AUTOCLICK is an application that loads credentials from a file, performs click sequences, ")
        f.write("takes screenshots, logs out, and repeats with the next set of credentials. The project ")
        f.write("is implementing clean architecture with domain, application, infrastructure, and UI layers.\n\n")
        
        f.write("### Key Requirements\n\n")
        f.write("- Strict adherence to SOLID, KISS, DRY principles\n")
        f.write("- Test-Driven Development (TDD) mandatory\n")
        f.write("- Single Responsibility Principle (SRP) focus\n")
        f.write("- Proper dependency injection\n")
        f.write("- Clean separation of concerns\n\n")
        
        # Write problematic components section
        f.write("## Problematic Components\n\n")
        f.write("The following components have significant issues and need to be fixed or replaced.\n\n")
        
        # Process each problematic component
        for component in COMPONENTS_TO_DISCARD:
            if os.path.exists(component):
                file_info = get_file_info(component)
                content = read_file_content(component)
                
                f.write(f"### {component}\n\n")
                f.write(f"**Created:** {file_info.get('created', 'Unknown')}\n")
                f.write(f"**Modified:** {file_info.get('modified', 'Unknown')}\n")
                f.write(f"**Size:** {file_info.get('size', 'Unknown')} bytes\n\n")
                
                f.write("**Issues:**\n\n")
                for issue in COMPONENT_ISSUES.get(component, ["Unknown issues"]):
                    f.write(f"- {issue}\n")
                f.write("\n")
                
                f.write("**Code:**\n\n")
                f.write("```python\n")
                f.write(content)
                f.write("\n```\n\n")
        
        # Write components for discussion
        f.write("## Components for Discussion\n\n")
        f.write("The following components have both strengths and weaknesses and require further analysis.\n\n")
        
        for component in COMPONENTS_FOR_DISCUSSION:
            if os.path.exists(component):
                file_info = get_file_info(component)
                content = read_file_content(component)
                
                f.write(f"### {component}\n\n")
                f.write(f"**Created:** {file_info.get('created', 'Unknown')}\n")
                f.write(f"**Modified:** {file_info.get('modified', 'Unknown')}\n")
                f.write(f"**Size:** {file_info.get('size', 'Unknown')} bytes\n\n")
                
                f.write("**Code:**\n\n")
                f.write("```python\n")
                f.write(content)
                f.write("\n```\n\n")
        
        # Write components to keep as reference
        f.write("## Reference Components (Working Correctly)\n\n")
        f.write("The following components are working correctly and can be used as reference for the design patterns and architecture.\n\n")
        
        for component in COMPONENTS_TO_KEEP:
            if os.path.exists(component):
                file_info = get_file_info(component)
                
                f.write(f"### {component}\n\n")
                f.write(f"**Created:** {file_info.get('created', 'Unknown')}\n")
                f.write(f"**Modified:** {file_info.get('modified', 'Unknown')}\n")
                f.write(f"**Size:** {file_info.get('size', 'Unknown')} bytes\n\n")
        
        # Write instructions for the AI
        f.write("## Instructions for AI\n\n")
        f.write("1. **Analyze the problematic components** and identify specific issues\n")
        f.write("2. **Propose fixes or replacements** that adhere to SOLID, KISS, DRY principles\n")
        f.write("3. **Provide complete implementations** for each component that needs to be fixed\n")
        f.write("4. **Ensure proper integration** with the existing architecture\n")
        f.write("5. **Include unit tests** for all new or modified components\n")
        f.write("6. **Explain your reasoning** for each change or decision\n\n")
        
        f.write("### Key Principles to Follow\n\n")
        f.write("- **Single Responsibility Principle**: Each class should have only one reason to change\n")
        f.write("- **Open/Closed Principle**: Classes should be open for extension but closed for modification\n")
        f.write("- **Liskov Substitution Principle**: Subtypes must be substitutable for their base types\n")
        f.write("- **Interface Segregation Principle**: Clients shouldn't depend on interfaces they don't use\n")
        f.write("- **Dependency Inversion Principle**: Depend on abstractions, not concretions\n")
        f.write("- **Keep It Simple, Stupid (KISS)**: Avoid unnecessary complexity\n")
        f.write("- **Don't Repeat Yourself (DRY)**: Avoid code duplication\n")
        f.write("- **Test-Driven Development (TDD)**: Write tests before implementation\n\n")
        
        f.write("Thank you for your assistance in improving the AUTOCLICK project!")

def main():
    """Main entry point."""
    project_root = os.getcwd()
    output_file = os.path.join(project_root, "docs", "AUTOCLICK_AI_Input.md")
    
    generate_ai_input(output_file)
    
    print(f"AI input file generated: {output_file}")
    print(f"File size: {os.path.getsize(output_file)} bytes")

if __name__ == "__main__":
    main()
