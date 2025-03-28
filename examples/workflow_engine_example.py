"""Example demonstrating the use of WorkflowEngine"""
import os
import sys
import time
from typing import Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.click_action import ClickAction
from src.core.context.execution_context import ExecutionContext
from src.core.context.variable_storage import VariableScope
from src.core.workflow.workflow_engine import WorkflowEngine
from src.core.workflow.workflow_event import WorkflowEvent, WorkflowEventType


# Create a custom action for the example
class PrintAction(BaseAction):
    """Action that prints a message"""

    def __init__(self, description: str, message: str, action_id: str = None):
        """
        Initialize the print action

        Args:
            description: Human-readable description of the action
            message: Message to print
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.message = message

    @property
    def type(self) -> str:
        """Get the action type"""
        return "print"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        print(f"PrintAction: {self.message}")
        return ActionResult.create_success(f"Printed: {self.message}")


class SetVariableAction(BaseAction):
    """Action that sets a variable in the context"""

    def __init__(self, description: str, variable_name: str, variable_value: Any, action_id: str = None):
        """
        Initialize the set variable action

        Args:
            description: Human-readable description of the action
            variable_name: Name of the variable to set
            variable_value: Value to set
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.variable_name = variable_name
        self.variable_value = variable_value

    @property
    def type(self) -> str:
        """Get the action type"""
        return "set_variable"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        print(f"SetVariableAction: {self.variable_name} = {self.variable_value}")
        return ActionResult.create_success(
            f"Set variable: {self.variable_name}",
            {self.variable_name: self.variable_value}
        )


class GetVariableAction(BaseAction):
    """Action that gets a variable from the context"""

    def __init__(self, description: str, variable_name: str, action_id: str = None):
        """
        Initialize the get variable action

        Args:
            description: Human-readable description of the action
            variable_name: Name of the variable to get
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.variable_name = variable_name

    @property
    def type(self) -> str:
        """Get the action type"""
        return "get_variable"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        if self.variable_name not in context:
            return ActionResult.create_failure(f"Variable not found: {self.variable_name}")

        value = context[self.variable_name]
        print(f"GetVariableAction: {self.variable_name} = {value}")
        return ActionResult.create_success(
            f"Got variable: {self.variable_name}",
            {"value": value}
        )


def on_workflow_event(event: WorkflowEvent) -> None:
    """
    Handle workflow events

    Args:
        event: Workflow event
    """
    print(f"Event: {event.event_type.name} at {event.timestamp}")


def main() -> None:
    """Main function"""
    # Create a workflow engine
    engine = WorkflowEngine()

    # Add event listeners
    engine.add_event_listener(WorkflowEventType.WORKFLOW_STARTED, on_workflow_event)
    engine.add_event_listener(WorkflowEventType.WORKFLOW_COMPLETED, on_workflow_event)
    engine.add_event_listener(WorkflowEventType.ACTION_STARTED, on_workflow_event)
    engine.add_event_listener(WorkflowEventType.ACTION_COMPLETED, on_workflow_event)

    # Create an execution context
    context = ExecutionContext()
    context.variables.set("initial_value", "Hello, World!", VariableScope.WORKFLOW)

    # Create a list of actions
    actions = [
        PrintAction("Print welcome message", "Welcome to the workflow engine example!"),
        GetVariableAction("Get initial value", "initial_value"),
        SetVariableAction("Set counter", "counter", 1),
        PrintAction("Print counter", "Counter is set to 1"),
        SetVariableAction("Increment counter", "counter", 2),
        PrintAction("Print final message", "Workflow completed successfully!")
    ]

    # Execute the workflow
    print("\nExecuting workflow...")
    result = engine.execute_workflow(actions, context, "example-workflow")

    # Print the result
    print("\nWorkflow result:")
    print(f"  Success: {result['success']}")
    print(f"  Message: {result['message']}")
    print(f"  Completed: {result['completed']}")
    print(f"  Workflow ID: {result['workflow_id']}")

    # Get workflow status
    status = engine.get_workflow_status(result["workflow_id"])
    print("\nWorkflow status:")
    for key, value in status.items():
        print(f"  {key}: {value}")

    # Get workflow statistics
    stats = engine.get_workflow_statistics(result["workflow_id"])
    print("\nWorkflow statistics:")
    stats_dict = stats.to_dict()
    for key, value in stats_dict.items():
        print(f"  {key}: {value}")

    # Print final context variables
    print("\nContext variables:")
    for name in context.variables.get_names():
        value = context.variables.get(name)
        scope = context.variables.get_scope(name)
        print(f"  {name} = {value} ({scope.name})")


if __name__ == "__main__":
    main()
