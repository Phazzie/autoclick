"""Example demonstrating the use of ActionFactory"""
import os
import sys
from typing import Dict, Any, List
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.actions.action_factory import ActionFactory
from src.core.actions.click_action import ClickAction  # This will register the action with the factory


def load_workflow_from_json(json_file: str) -> List[Dict[str, Any]]:
    """
    Load a workflow from a JSON file

    Args:
        json_file: Path to the JSON file

    Returns:
        List of action configurations
    """
    with open(json_file, 'r') as f:
        return json.load(f)


def execute_workflow(actions_data: List[Dict[str, Any]], context: Dict[str, Any]) -> None:
    """
    Execute a workflow of actions

    Args:
        actions_data: List of action configurations
        context: Execution context
    """
    factory = ActionFactory.get_instance()

    for action_data in actions_data:
        print(f"Executing action: {action_data.get('description')}")

        # Create the action using the factory
        action = factory.create_action(action_data)

        # Execute the action
        result = action.execute(context)

        # Print the result
        if result.success:
            print(f"  Success: {result.message}")
        else:
            print(f"  Failure: {result.message}")
            # In a real application, you might want to handle failures differently
            # For example, stop the workflow or try recovery strategies


def main() -> None:
    """Main function"""
    # In a real application, this would be loaded from a file
    # For this example, we'll create it inline
    workflow_data = [
        {
            "type": "click",
            "description": "Click login button",
            "selector": "#login-button"
        },
        {
            "type": "click",
            "description": "Click submit button",
            "selector": "#submit-button"
        }
    ]

    # In a real application, this would include a browser driver
    # For this example, we'll create a mock driver
    class MockDriver:
        def find_element_by_css_selector(self, selector: str) -> Any:
            print(f"  Finding element: {selector}")

            class MockElement:
                def click(self) -> None:
                    print(f"  Clicking element: {selector}")

            return MockElement()

    context = {
        "driver": MockDriver()
    }

    # Execute the workflow
    execute_workflow(workflow_data, context)


if __name__ == "__main__":
    main()
