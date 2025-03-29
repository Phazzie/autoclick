"""Action for setting variables in the context"""
from typing import Dict, Any, Optional, Union

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.action_factory import ActionFactory
from src.core.expressions.expression_parser import parse_expression


@ActionFactory.register("set_variable")
class SetVariableAction(BaseAction):
    """Action that sets a variable in the context"""

    def __init__(
        self,
        description: str,
        variable_name: str,
        variable_value: Any,
        evaluate_expression: bool = True,
        action_id: Optional[str] = None
    ):
        """
        Initialize the set variable action

        Args:
            description: Human-readable description of the action
            variable_name: Name of the variable to set
            variable_value: Value to set (can be a literal or an expression)
            evaluate_expression: Whether to evaluate the value as an expression
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.variable_name = variable_name
        self.variable_value = variable_value
        self.evaluate_expression = evaluate_expression

    @property
    def type(self) -> str:
        """Get the action type"""
        return "set_variable"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the action execution
        """
        try:
            # Evaluate the variable name if it contains expressions
            variable_name = parse_expression(self.variable_name, context) if isinstance(self.variable_name, str) else self.variable_name
            
            # Evaluate the value if needed
            if self.evaluate_expression and isinstance(self.variable_value, str):
                value = parse_expression(self.variable_value, context)
            else:
                value = self.variable_value

            # Set the variable in the context
            context[variable_name] = value
            
            return ActionResult.create_success(
                f"Variable '{variable_name}' set to '{value}'",
                {variable_name: value}
            )
        except Exception as e:
            return ActionResult.create_failure(
                f"Failed to set variable: {str(e)}"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data.update({
            "variable_name": self.variable_name,
            "variable_value": self.variable_value,
            "evaluate_expression": self.evaluate_expression
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SetVariableAction':
        """
        Create an action from a dictionary

        Args:
            data: Dictionary representation of the action

        Returns:
            Instantiated action
        """
        return cls(
            description=data.get("description", ""),
            variable_name=data.get("variable_name", ""),
            variable_value=data.get("variable_value"),
            evaluate_expression=data.get("evaluate_expression", True),
            action_id=data.get("id")
        )
