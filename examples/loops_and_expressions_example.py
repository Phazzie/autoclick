"""Example demonstrating the use of loops and expressions"""
import os
import sys
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.set_variable_action import SetVariableAction
from src.core.actions.for_each_action import ForEachAction
from src.core.actions.while_loop_action import WhileLoopAction
from src.core.actions.loop_control_actions import BreakAction, ContinueAction
from src.core.conditions.comparison_condition import ComparisonCondition, ComparisonOperator
from src.core.workflow.workflow_engine import WorkflowEngine
from src.core.expressions.expression_parser import parse_expression, parse_template


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
        # Parse the message template
        parsed_message = parse_template(self.message, context)
        print(f"PrintAction: {parsed_message}")
        return ActionResult.create_success(f"Printed: {parsed_message}")


def main() -> None:
    """Main function"""
    # Create a workflow engine
    engine = WorkflowEngine()

    # Create a context
    context = {
        "counter": 0,
        "items": ["apple", "banana", "cherry", "date", "elderberry"],
        "user": {
            "name": "John Doe",
            "age": 30,
            "preferences": {
                "theme": "dark",
                "notifications": True
            }
        }
    }

    print("\n=== Variable Expression Example ===")
    # Demonstrate variable expressions
    expressions = [
        "${counter}",
        "${items[0]}",
        "${user.name}",
        "${user.preferences.theme}",
        "Hello, ${user.name}! You are ${user.age} years old.",
        "Your preferred theme is ${user.preferences.theme}."
    ]

    for expr in expressions:
        result = parse_expression(expr, context)
        print(f"Expression: {expr} => {result}")

    print("\n=== For-Each Loop Example ===")
    # Create a for-each loop action
    for_each_actions = [
        PrintAction("Print item", "Current item: ${item} (index: ${loop_index})"),
        SetVariableAction(
            "Increment counter",
            "counter",
            "${counter + 1}",
            evaluate_expression=True
        )
    ]

    for_each_action = ForEachAction(
        "Iterate over items",
        "items",
        "item",
        for_each_actions
    )

    # Execute the for-each loop
    result = engine.execute_action(for_each_action, context)
    print(f"For-each result: {result.success} - {result.message}")
    print(f"Counter after for-each: {context['counter']}")

    print("\n=== While Loop Example ===")
    # Reset counter
    context["counter"] = 0

    # Create a while loop action
    while_condition = ComparisonCondition(
        "${counter}",
        ComparisonOperator.LESS_THAN,
        5
    )

    while_actions = [
        PrintAction("Print counter", "Counter value: ${counter}"),
        SetVariableAction(
            "Increment counter",
            "counter",
            "${counter + 1}",
            evaluate_expression=True
        ),
        # Add a conditional break
        PrintAction("Check for break", "Checking if counter is 3..."),
        SetVariableAction(
            "Set loop_break if counter is 3",
            "loop_break",
            "${counter == 3}",
            evaluate_expression=True
        )
    ]

    while_loop_action = WhileLoopAction(
        "Count to 5",
        while_condition,
        while_actions,
        max_iterations=10  # Safety limit
    )

    # Execute the while loop
    result = engine.execute_action(while_loop_action, context)
    print(f"While loop result: {result.success} - {result.message}")
    print(f"Counter after while loop: {context['counter']}")


if __name__ == "__main__":
    main()
