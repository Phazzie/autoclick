"""Example demonstrating workflow serialization and deserialization"""
import os
import sys
import json
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.actions.click_action import ClickAction
from src.core.actions.if_then_else_action import IfThenElseAction
from src.core.conditions.element_exists_condition import ElementExistsCondition
from src.core.context.execution_context import ExecutionContext
from src.core.workflow.workflow_serializer import WorkflowSerializer


def create_sample_workflow() -> List[Any]:
    """
    Create a sample workflow with various action types

    Returns:
        List of actions in the workflow
    """
    # Create a condition
    condition = ElementExistsCondition(
        selector="#login-form",
        description="Check if login form exists"
    )

    # Create actions for the if branch
    if_actions = [
        ClickAction(
            description="Enter username",
            selector="#username"
        ),
        ClickAction(
            description="Enter password",
            selector="#password"
        ),
        ClickAction(
            description="Click login button",
            selector="#login-button"
        )
    ]

    # Create actions for the else branch
    else_actions = [
        ClickAction(
            description="Click guest login",
            selector="#guest-login"
        )
    ]

    # Create an if-then-else action
    if_then_else = IfThenElseAction(
        description="Login as user or guest",
        condition=condition,
        if_actions=if_actions,
        else_actions=else_actions
    )

    # Create the main workflow
    workflow = [
        ClickAction(
            description="Navigate to login page",
            selector="#nav-login"
        ),
        if_then_else,
        ClickAction(
            description="Click dashboard link",
            selector="#dashboard-link"
        )
    ]

    return workflow


def main() -> None:
    """Main function"""
    print("Creating sample workflow...")
    workflow = create_sample_workflow()
    
    # Create a context
    context = ExecutionContext()
    context.variables.set("username", "testuser")
    context.variables.set("password", "password123")
    
    # Create metadata
    metadata = {
        "name": "Login Workflow",
        "description": "A workflow that logs in as a user or guest",
        "author": "Example User",
        "tags": ["login", "authentication"]
    }
    
    # Create a serializer
    serializer = WorkflowSerializer()
    
    # Serialize the workflow
    print("Serializing workflow...")
    workflow_dict = serializer.serialize_workflow(workflow, context, metadata)
    
    # Print the serialized workflow (pretty-printed)
    print("\nSerialized Workflow:")
    print(json.dumps(workflow_dict, indent=2))
    
    # Save the workflow to a file
    output_path = os.path.join(os.path.dirname(__file__), "sample_workflow.json")
    print(f"\nSaving workflow to {output_path}...")
    serializer.save_workflow_to_file(output_path, workflow, context, metadata)
    
    # Load the workflow from the file
    print(f"\nLoading workflow from {output_path}...")
    loaded = serializer.load_workflow_from_file(output_path)
    
    # Print information about the loaded workflow
    print("\nLoaded Workflow:")
    print(f"  Metadata: {loaded['metadata']}")
    print(f"  Actions: {len(loaded['actions'])} actions")
    for i, action in enumerate(loaded['actions']):
        print(f"    {i+1}. {action.description} (Type: {action.type})")
    
    print("\nWorkflow serialization example completed successfully!")


if __name__ == "__main__":
    main()
