"""Switch-case action for multiple conditional branches"""
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.conditions.condition_interface import ConditionInterface
from src.core.actions.action_factory import ActionFactory
from src.core.expressions.expression_parser import parse_expression


@dataclass
class CaseBranch:
    """A case branch in a switch-case action"""
    condition: ConditionInterface
    actions: List[BaseAction]
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the case branch to a dictionary"""
        return {
            "condition": self.condition.to_dict() if hasattr(self.condition, "to_dict") else {"type": "unknown"},
            "actions": [action.to_dict() for action in self.actions],
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], action_factory, condition_factory) -> 'CaseBranch':
        """
        Create a case branch from a dictionary

        Args:
            data: Dictionary representation of the case branch
            action_factory: Factory for creating actions
            condition_factory: Factory for creating conditions

        Returns:
            Instantiated case branch
        """
        # Create the condition
        condition_data = data.get("condition", {})
        condition = condition_factory.create_condition(condition_data)

        # Create the actions
        actions_data = data.get("actions", [])
        actions = [action_factory.create_action(action_data) for action_data in actions_data]

        # Create the case branch
        return cls(
            condition=condition,
            actions=actions,
            description=data.get("description")
        )


@ActionFactory.register("switch_case")
class SwitchCaseAction(BaseAction):
    """Action that executes different branches based on conditions"""

    def __init__(
        self,
        description: str,
        cases: List[CaseBranch],
        default_actions: Optional[List[BaseAction]] = None,
        action_id: Optional[str] = None
    ):
        """
        Initialize the switch-case action

        Args:
            description: Human-readable description of the action
            cases: List of case branches to evaluate
            default_actions: Actions to execute if no case matches (optional)
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.cases = cases
        self.default_actions = default_actions or []

    @property
    def type(self) -> str:
        """Get the action type"""
        return "switch_case"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the action execution
        """
        # Evaluate each case in order
        for i, case in enumerate(self.cases):
            # Evaluate the condition
            condition_result = case.condition.evaluate(context)

            if condition_result:
                # Condition is true, execute this case's actions
                case_description = case.description or f"Case {i+1}"
                return self._execute_branch(case.actions, context, case_description)

        # No case matched, execute default actions
        return self._execute_branch(self.default_actions, context, "default")

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
            "cases": [case.to_dict() for case in self.cases],
            "default_actions": [action.to_dict() for action in self.default_actions]
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SwitchCaseAction':
        """
        Create a switch-case action from a dictionary

        Args:
            data: Dictionary representation of the action

        Returns:
            Instantiated action
        """
        from src.core.actions.action_factory import ActionFactory
        from src.core.conditions.condition_factory import ConditionFactory

        action_factory = ActionFactory.get_instance()
        condition_factory = ConditionFactory.get_instance()

        # Create the case branches
        cases_data = data.get("cases", [])
        cases = [
            CaseBranch.from_dict(case_data, action_factory, condition_factory)
            for case_data in cases_data
        ]

        # Create the default actions
        default_actions_data = data.get("default_actions", [])
        default_actions = [
            action_factory.create_action(action_data)
            for action_data in default_actions_data
        ]

        # Create the switch-case action
        return cls(
            description=data.get("description", ""),
            cases=cases,
            default_actions=default_actions,
            action_id=data.get("id")
        )
