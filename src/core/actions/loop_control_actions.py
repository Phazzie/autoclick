"""Loop control actions for breaking and continuing loops"""
from typing import Dict, Any, Optional

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.action_factory import ActionFactory


@ActionFactory.register("break")
class BreakAction(BaseAction):
    """Action that breaks out of the current loop"""

    def __init__(
        self,
        description: str = "Break out of the current loop",
        action_id: Optional[str] = None
    ):
        """
        Initialize the break action

        Args:
            description: Human-readable description of the action
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)

    @property
    def type(self) -> str:
        """Get the action type"""
        return "break"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the action execution
        """
        # Set the loop_break flag in the context
        context["loop_break"] = True
        
        return ActionResult.create_success(
            "Break action executed",
            {"loop_break": True}
        )


@ActionFactory.register("continue")
class ContinueAction(BaseAction):
    """Action that continues to the next iteration of the current loop"""

    def __init__(
        self,
        description: str = "Continue to the next iteration of the current loop",
        action_id: Optional[str] = None
    ):
        """
        Initialize the continue action

        Args:
            description: Human-readable description of the action
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)

    @property
    def type(self) -> str:
        """Get the action type"""
        return "continue"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the action execution
        """
        # Set the loop_continue flag in the context
        context["loop_continue"] = True
        
        return ActionResult.create_success(
            "Continue action executed",
            {"loop_continue": True}
        )
