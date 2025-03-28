"""Conditional action for if-then-else logic"""
from typing import Dict, Any, List, Optional, Union

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.conditions.condition_interface import ConditionInterface
from src.core.conditions.condition_factory import ConditionFactory
from src.core.actions.action_factory import ActionFactory
from src.core.expressions.expression_parser import parse_expression


@ActionFactory.register("if_then_else")
class IfThenElseAction(BaseAction):
    """Action that executes different actions based on a condition"""

    def __init__(
        self,
        description: str,
        condition: ConditionInterface,
        then_actions: List[BaseAction],
        else_actions: Optional[List[BaseAction]] = None,
        action_id: Optional[str] = None
    ):
        """
        Initialize the if-then-else action

        Args:
            description: Human-readable description of the action
            condition: Condition to evaluate
            then_actions: Actions to execute if the condition is true
            else_actions: Actions to execute if the condition is false (optional)
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.condition = condition
        self.then_actions = then_actions
        self.else_actions = else_actions or []

    @property
    def type(self) -> str:
        """Get the action type"""
        return "if_then_else"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the action execution
        """
        # Process any variable expressions in the context
        processed_context = self._process_variable_expressions(context)

        # Evaluate the condition
        condition_result = self.condition.evaluate(processed_context)

        if condition_result:
            # Condition is true, execute then_actions
            return self._execute_branch(self.then_actions, processed_context, "then")
        else:
            # Condition is false, execute else_actions
            return self._execute_branch(self.else_actions, processed_context, "else")

    def _process_variable_expressions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process any variable expressions in the context

        Args:
            context: Original execution context

        Returns:
            Context with variable expressions processed
        """
        # Create a copy of the context to avoid modifying the original
        processed_context = context.copy()

        # Process string values that might contain variable expressions
        for key, value in processed_context.items():
            if isinstance(value, str) and "${" in value and "}" in value:
                processed_context[key] = parse_expression(value, context)

        return processed_context

    def _execute_branch(
        self,
        actions: List[BaseAction],
        context: Dict[str, Any],
        branch_name: str
    ) -> ActionResult:
        """
        Execute a branch of actions

        Args:
            actions: Actions to execute
            context: Execution context
            branch_name: Name of the branch (for logging)

        Returns:
            Result of the branch execution
        """
        results = []
        success = True
        error_message = None

        for i, action in enumerate(actions):
            try:
                result = action.execute(context)
                results.append(result)

                if not result.success:
                    # Action failed
                    success = False
                    error_message = f"Action {i+1} in {branch_name} branch failed: {result.message}"
                    break
            except Exception as e:
                # Handle unexpected exceptions
                success = False
                error_message = f"Error executing action {i+1} in {branch_name} branch: {str(e)}"
                break

        if success:
            return ActionResult.create_success(
                f"Executed {branch_name} branch successfully",
                {"branch": branch_name, "results": results}
            )
        else:
            return ActionResult.create_failure(
                error_message or f"Failed to execute {branch_name} branch",
                {"branch": branch_name, "results": results}
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data.update({
            "condition": self.condition.to_dict() if hasattr(self.condition, "to_dict") else {"type": "unknown"},
            "then_actions": [action.to_dict() for action in self.then_actions],
            "else_actions": [action.to_dict() for action in self.else_actions]
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IfThenElseAction':
        """
        Create an if-then-else action from a dictionary

        Args:
            data: Dictionary representation of the action

        Returns:
            Instantiated action
        """
        from src.core.actions.action_factory import ActionFactory
        from src.core.conditions.condition_factory import ConditionFactory

        action_factory = ActionFactory.get_instance()
        condition_factory = ConditionFactory.get_instance()

        # Create the condition
        condition_data = data.get("condition", {})
        condition = condition_factory.create_condition(condition_data)

        # Create the then actions
        then_actions_data = data.get("then_actions", [])
        then_actions = [
            action_factory.create_action(action_data)
            for action_data in then_actions_data
        ]

        # Create the else actions
        else_actions_data = data.get("else_actions", [])
        else_actions = [
            action_factory.create_action(action_data)
            for action_data in else_actions_data
        ]

        # Create the if-then-else action
        return cls(
            description=data.get("description", ""),
            condition=condition,
            then_actions=then_actions,
            else_actions=else_actions,
            action_id=data.get("id")
        )

    # End of class
