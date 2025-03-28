"""Example demonstrating the use of ExecutionContext"""
import os
import sys
from typing import Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.context.execution_context import ExecutionContext
from src.core.context.execution_state import ExecutionStateEnum
from src.core.context.variable_storage import VariableScope


def print_context_info(context: ExecutionContext, indent: str = "") -> None:
    """
    Print information about a context

    Args:
        context: Context to print information about
        indent: Indentation string for formatting
    """
    print(f"{indent}Context ID: {context.id}")
    print(f"{indent}State: {context.state.current_state.name}")
    
    # Print variables
    print(f"{indent}Variables:")
    all_vars = context.variables.get_all()
    if all_vars:
        for name, value in all_vars.items():
            scope = context.variables.get_scope(name)
            print(f"{indent}  {name} = {value} ({scope.name if scope else 'unknown'})")
    else:
        print(f"{indent}  No variables")
    
    # Print children
    if context._children:
        print(f"{indent}Children:")
        for child in context._children:
            print_context_info(child, indent + "  ")
    else:
        print(f"{indent}No children")


def on_state_change(event):
    """
    Handle state change events

    Args:
        event: State change event
    """
    print(f"State changed: {event.old_state.name} -> {event.new_state.name}")


def on_variable_change(event):
    """
    Handle variable change events

    Args:
        event: Variable change event
    """
    print(f"Variable changed: {event.scope.name}.{event.name} = {event.new_value}")


def main() -> None:
    """Main function"""
    print("Creating root context...")
    root = ExecutionContext()
    
    # Add event listeners
    root.state.add_state_change_listener(on_state_change)
    root.variables.add_variable_change_listener(on_variable_change)
    
    # Set some variables
    print("\nSetting variables...")
    root.variables.set("global_var", "global value", VariableScope.GLOBAL)
    root.variables.set("workflow_var", "workflow value", VariableScope.WORKFLOW)
    root.variables.set("local_var", "local value", VariableScope.LOCAL)
    
    # Change state
    print("\nChanging state...")
    root.state.transition_to(ExecutionStateEnum.RUNNING)
    
    # Create a child context
    print("\nCreating child context...")
    child = root.create_child()
    child.variables.set("child_var", "child value", VariableScope.WORKFLOW)
    
    # Print context information
    print("\nContext Information:")
    print_context_info(root)
    
    # Modify variables
    print("\nModifying variables...")
    root.variables.set("workflow_var", "modified workflow value")
    
    # Transition to completed
    print("\nCompleting execution...")
    root.state.transition_to(ExecutionStateEnum.COMPLETED)
    
    # Serialize and deserialize
    print("\nSerializing and deserializing context...")
    serialized = root.to_dict(include_children=True)
    deserialized = ExecutionContext.from_dict(serialized)
    
    print("\nDeserialized Context Information:")
    print_context_info(deserialized)
    
    # Clean up
    print("\nDisposing contexts...")
    root.dispose()


if __name__ == "__main__":
    main()
