"""Example demonstrating conditional actions"""
import os
import sys
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.if_then_else_action import IfThenElseAction
from src.core.actions.switch_case_action import SwitchCaseAction, CaseBranch
from src.core.actions.set_variable_action import SetVariableAction
from src.core.conditions.comparison_condition import ComparisonCondition, ComparisonOperator
from src.core.conditions.element_exists_condition import ElementExistsCondition
from src.core.conditions.text_contains_condition import TextContainsCondition
from src.core.conditions.composite_conditions import AndCondition, OrCondition, NotCondition
from src.core.workflow.workflow_engine import WorkflowEngine
from src.core.workflow.workflow_serializer import WorkflowSerializer


# Simple action for printing messages
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
        # Print the message
        print(f"[PrintAction] {self.message}")
        return ActionResult.create_success(f"Printed message: {self.message}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data["message"] = self.message
        return data


def create_if_then_else_example() -> List[BaseAction]:
    """
    Create an example workflow with if-then-else actions

    Returns:
        List of actions in the workflow
    """
    # Create a condition to check if the user is logged in
    is_logged_in_condition = ComparisonCondition(
        left_value="${is_logged_in}",
        operator=ComparisonOperator.EQUALS,
        right_value=True,
        description="Check if user is logged in"
    )

    # Create actions for the if branch (user is logged in)
    if_actions = [
        PrintAction(
            description="Print welcome message",
            message="Welcome back, ${username}!"
        ),
        PrintAction(
            description="Show dashboard",
            message="Displaying dashboard for ${username}"
        )
    ]

    # Create actions for the else branch (user is not logged in)
    else_actions = [
        PrintAction(
            description="Show login form",
            message="Please log in to continue"
        ),
        SetVariableAction(
            description="Set username",
            variable_name="username",
            value="guest"
        ),
        SetVariableAction(
            description="Set is_logged_in",
            variable_name="is_logged_in",
            value=True
        ),
        PrintAction(
            description="Show guest message",
            message="Logged in as guest"
        )
    ]

    # Create an if-then-else action
    if_then_else = IfThenElseAction(
        description="Handle login state",
        condition=is_logged_in_condition,
        then_actions=if_actions,
        else_actions=else_actions
    )

    # Create the main workflow
    workflow = [
        SetVariableAction(
            description="Initialize username",
            variable_name="username",
            value="John"
        ),
        SetVariableAction(
            description="Initialize login state",
            variable_name="is_logged_in",
            value=False
        ),
        PrintAction(
            description="Start workflow",
            message="Starting workflow..."
        ),
        if_then_else,
        PrintAction(
            description="End workflow",
            message="Workflow completed for user: ${username}"
        )
    ]

    return workflow


def create_switch_case_example() -> List[BaseAction]:
    """
    Create an example workflow with switch-case actions

    Returns:
        List of actions in the workflow
    """
    # Create conditions for different user roles
    is_admin_condition = ComparisonCondition(
        left_value="${role}",
        operator=ComparisonOperator.EQUALS,
        right_value="admin",
        description="Check if user is admin"
    )

    is_editor_condition = ComparisonCondition(
        left_value="${role}",
        operator=ComparisonOperator.EQUALS,
        right_value="editor",
        description="Check if user is editor"
    )

    is_viewer_condition = ComparisonCondition(
        left_value="${role}",
        operator=ComparisonOperator.EQUALS,
        right_value="viewer",
        description="Check if user is viewer"
    )

    # Create case branches for different user roles
    admin_case = CaseBranch(
        condition=is_admin_condition,
        actions=[
            PrintAction(
                description="Show admin panel",
                message="Welcome, Admin! Here's your admin panel."
            ),
            PrintAction(
                description="Show admin options",
                message="You have full access to all features."
            )
        ],
        description="Admin Role"
    )

    editor_case = CaseBranch(
        condition=is_editor_condition,
        actions=[
            PrintAction(
                description="Show editor panel",
                message="Welcome, Editor! Here's your content management panel."
            ),
            PrintAction(
                description="Show editor options",
                message="You can create and edit content."
            )
        ],
        description="Editor Role"
    )

    viewer_case = CaseBranch(
        condition=is_viewer_condition,
        actions=[
            PrintAction(
                description="Show viewer panel",
                message="Welcome, Viewer! Here's your dashboard."
            ),
            PrintAction(
                description="Show viewer options",
                message="You can view and comment on content."
            )
        ],
        description="Viewer Role"
    )

    # Create default actions for unknown roles
    default_actions = [
        PrintAction(
            description="Show unknown role message",
            message="Unknown role: ${role}. Please contact an administrator."
        ),
        SetVariableAction(
            description="Set default role",
            variable_name="role",
            value="guest"
        ),
        PrintAction(
            description="Show guest options",
            message="You have limited access as a guest."
        )
    ]

    # Create a switch-case action
    switch_case = SwitchCaseAction(
        description="Handle user role",
        cases=[admin_case, editor_case, viewer_case],
        default_actions=default_actions
    )

    # Create the main workflow
    workflow = [
        SetVariableAction(
            description="Initialize username",
            variable_name="username",
            value="John"
        ),
        SetVariableAction(
            description="Initialize role",
            variable_name="role",
            value="unknown"  # Will trigger the default case
        ),
        PrintAction(
            description="Start workflow",
            message="Starting role-based workflow..."
        ),
        switch_case,
        PrintAction(
            description="End workflow",
            message="Role-based workflow completed for ${username} (${role})"
        )
    ]

    return workflow


def create_complex_condition_example() -> List[BaseAction]:
    """
    Create an example workflow with complex conditions

    Returns:
        List of actions in the workflow
    """
    # Create complex conditions using AND, OR, and NOT
    complex_condition = AndCondition(
        # User must be logged in
        ComparisonCondition(
            left_value="${is_logged_in}",
            operator=ComparisonOperator.EQUALS,
            right_value=True,
            description="Check if user is logged in"
        ),
        # AND (user is admin OR user has premium subscription)
        OrCondition(
            ComparisonCondition(
                left_value="${role}",
                operator=ComparisonOperator.EQUALS,
                right_value="admin",
                description="Check if user is admin"
            ),
            ComparisonCondition(
                left_value="${has_premium}",
                operator=ComparisonOperator.EQUALS,
                right_value=True,
                description="Check if user has premium"
            ),
            description="Check if user is admin or has premium"
        ),
        # AND user is not in restricted mode
        NotCondition(
            ComparisonCondition(
                left_value="${restricted_mode}",
                operator=ComparisonOperator.EQUALS,
                right_value=True,
                description="Check if user is in restricted mode"
            ),
            description="Check if user is not in restricted mode"
        ),
        description="Complex access condition"
    )

    # Create actions for the if branch (condition is true)
    if_actions = [
        PrintAction(
            description="Show premium content",
            message="Welcome, ${username}! Here's your premium content."
        ),
        PrintAction(
            description="Show premium options",
            message="You have access to all premium features."
        )
    ]

    # Create actions for the else branch (condition is false)
    else_actions = [
        PrintAction(
            description="Show restricted message",
            message="Sorry, ${username}. This content is only available to premium users or admins."
        ),
        PrintAction(
            description="Show upgrade options",
            message="Would you like to upgrade to premium?"
        )
    ]

    # Create an if-then-else action with the complex condition
    if_then_else = IfThenElseAction(
        description="Handle premium content access",
        condition=complex_condition,
        then_actions=if_actions,
        else_actions=else_actions
    )

    # Create the main workflow
    workflow = [
        SetVariableAction(
            description="Initialize username",
            variable_name="username",
            value="John"
        ),
        SetVariableAction(
            description="Initialize login state",
            variable_name="is_logged_in",
            value=True
        ),
        SetVariableAction(
            description="Initialize role",
            variable_name="role",
            value="user"  # Not admin
        ),
        SetVariableAction(
            description="Initialize premium status",
            variable_name="has_premium",
            value=False  # No premium
        ),
        SetVariableAction(
            description="Initialize restricted mode",
            variable_name="restricted_mode",
            value=False  # Not in restricted mode
        ),
        PrintAction(
            description="Start workflow",
            message="Starting premium content workflow..."
        ),
        if_then_else,
        PrintAction(
            description="End workflow",
            message="Premium content workflow completed for ${username}"
        )
    ]

    return workflow


def run_workflow(workflow: List[BaseAction], title: str) -> None:
    """
    Run a workflow with the workflow engine

    Args:
        workflow: List of actions to execute
        title: Title of the workflow
    """
    print(f"\n{'=' * 50}")
    print(f"Running {title}")
    print(f"{'=' * 50}")

    # Create a workflow engine
    engine = WorkflowEngine()

    # Create an execution context
    context = {}

    # Execute the workflow
    result = engine.execute_workflow(workflow, context)

    # Print the result
    print(f"\nWorkflow result: {'Success' if result['success'] else 'Failure'}")
    print(f"Message: {result['message']}")
    print(f"{'=' * 50}\n")


def save_and_load_workflow(workflow: List[BaseAction], title: str) -> None:
    """
    Save a workflow to a file and load it back

    Args:
        workflow: List of actions to save
        title: Title of the workflow
    """
    print(f"\n{'=' * 50}")
    print(f"Saving and loading {title}")
    print(f"{'=' * 50}")

    # Create a workflow serializer
    serializer = WorkflowSerializer()

    # Create a file path
    file_path = os.path.join(os.path.dirname(__file__), f"{title.lower().replace(' ', '_')}.json")

    # Save the workflow
    print(f"Saving workflow to {file_path}...")
    serializer.save_workflow_to_file(
        file_path,
        workflow,
        metadata={
            "name": title,
            "description": f"Example workflow for {title}",
            "author": "Example Script"
        }
    )

    # Load the workflow
    print(f"Loading workflow from {file_path}...")
    loaded = serializer.load_workflow_from_file(file_path)

    # Print information about the loaded workflow
    print(f"\nLoaded workflow: {loaded['metadata']['name']}")
    print(f"Description: {loaded['metadata']['description']}")
    print(f"Actions: {len(loaded['actions'])} actions")
    print(f"{'=' * 50}\n")


def main() -> None:
    """Main function"""
    print("Conditional Actions Example")
    print("==========================")

    # Create and run the if-then-else example
    if_then_else_workflow = create_if_then_else_example()
    run_workflow(if_then_else_workflow, "If-Then-Else Example")

    # Create and run the switch-case example
    switch_case_workflow = create_switch_case_example()
    run_workflow(switch_case_workflow, "Switch-Case Example")

    # Create and run the complex condition example
    complex_condition_workflow = create_complex_condition_example()
    run_workflow(complex_condition_workflow, "Complex Condition Example")

    # Save and load the workflows
    save_and_load_workflow(if_then_else_workflow, "If-Then-Else Example")
    save_and_load_workflow(switch_case_workflow, "Switch-Case Example")
    save_and_load_workflow(complex_condition_workflow, "Complex Condition Example")

    print("Conditional actions example completed successfully!")


if __name__ == "__main__":
    main()
