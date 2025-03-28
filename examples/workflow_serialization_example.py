"""Example demonstrating workflow serialization"""
import os
import sys
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.click_action import ClickAction
from src.core.actions.if_then_else_action import IfThenElseAction
from src.core.conditions.element_exists_condition import ElementExistsCondition
from src.core.workflow.workflow_serializer import WorkflowSerializer


# Create a simple action for the example
class PrintAction(BaseAction):
    """Action that prints a message"""

    def __init__(self, description: str, message: str, action_id: str = None):
        """Initialize the print action"""
        super().__init__(description, action_id)
        self.message = message

    @property
    def type(self) -> str:
        """Get the action type"""
        return "print"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        print(f"[PrintAction] {self.message}")
        return ActionResult.create_success(f"Printed message: {self.message}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data["message"] = self.message
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PrintAction':
        """Create an action from a dictionary"""
        return cls(
            description=data.get("description", ""),
            message=data.get("message", ""),
            action_id=data.get("id")
        )


def create_example_workflow() -> List[BaseAction]:
    """Create an example workflow"""
    # Create a condition
    condition = ElementExistsCondition("#login-button")

    # Create actions for the then branch
    then_actions = [
        PrintAction(
            description="Print login message",
            message="Login button found, clicking it..."
        ),
        ClickAction(
            description="Click login button",
            selector="#login-button"
        )
    ]

    # Create actions for the else branch
    else_actions = [
        PrintAction(
            description="Print error message",
            message="Login button not found!"
        )
    ]

    # Create an if-then-else action
    if_action = IfThenElseAction(
        description="Check for login button",
        condition=condition,
        then_actions=then_actions,
        else_actions=else_actions
    )

    # Create the main workflow
    workflow = [
        PrintAction(
            description="Print start message",
            message="Starting workflow..."
        ),
        if_action,
        PrintAction(
            description="Print end message",
            message="Workflow completed!"
        )
    ]

    return workflow


def main() -> None:
    """Main function"""
    # Create an example workflow
    workflow = create_example_workflow()

    # Create metadata
    metadata = {
        "name": "Login Workflow",
        "description": "A workflow that logs into a website",
        "author": "Example Script",
        "version": "1.0.0",
        "tags": ["login", "example"]
    }

    # Create a workflow serializer
    serializer = WorkflowSerializer()

    # Create a file path
    file_path = os.path.join(os.path.dirname(__file__), "login_workflow.json")

    # Save the workflow
    print(f"Saving workflow to {file_path}...")
    serializer.save_workflow_to_file(file_path, workflow, metadata)

    # Load the workflow data
    print(f"Loading workflow from {file_path}...")
    workflow_data = serializer.load_workflow_from_file(file_path)

    # Print the workflow data
    print("\nWorkflow Data:")
    print(f"  Name: {workflow_data['metadata']['name']}")
    print(f"  Description: {workflow_data['metadata']['description']}")
    print(f"  Author: {workflow_data['metadata']['author']}")
    print(f"  Version: {workflow_data['metadata']['version']}")
    print(f"  Tags: {', '.join(workflow_data['metadata']['tags'])}")
    print(f"  Actions: {len(workflow_data['actions'])}")

    # Register the PrintAction with the ActionFactory
    from src.core.actions.action_factory import ActionFactory
    ActionFactory.register("print")(PrintAction)

    # Register the ElementExistsCondition with the ConditionFactory
    from src.core.conditions.condition_factory import ConditionFactoryClass
    ConditionFactoryClass.register("element_exists")(ElementExistsCondition)

    # Deserialize the workflow
    print("\nDeserializing workflow...")
    actions, metadata = serializer.deserialize_workflow(workflow_data, use_factory=True)

    # Print information about the deserialized workflow
    print(f"  Deserialized {len(actions)} actions")
    print(f"  First action: {actions[0].description}")
    print(f"  Last action: {actions[-1].description}")

    # Pretty print the workflow structure
    print("\nWorkflow Structure:")
    print_workflow_structure(actions)


def print_workflow_structure(actions: List[BaseAction], indent: int = 0) -> None:
    """
    Print the structure of a workflow

    Args:
        actions: List of actions in the workflow
        indent: Indentation level
    """
    for action in actions:
        # Print the action with indentation
        print(f"{'  ' * indent}- {action.type}: {action.description}")

        # Handle nested actions
        if isinstance(action, IfThenElseAction):
            print(f"{'  ' * (indent + 1)}Then branch:")
            print_workflow_structure(action.then_actions, indent + 2)
            print(f"{'  ' * (indent + 1)}Else branch:")
            print_workflow_structure(action.else_actions, indent + 2)


if __name__ == "__main__":
    main()
