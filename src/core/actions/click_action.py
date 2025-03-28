"""Click action implementation"""
from typing import Dict, Any, Optional

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.action_factory import ActionFactory


@ActionFactory.register("click")
class ClickAction(BaseAction):
    """Action to click on an element"""

    def __init__(self, description: str, selector: str, action_id: Optional[str] = None) -> None:
        """
        Initialize the click action

        Args:
            description: Human-readable description of the action
            selector: CSS selector for the element to click
            action_id: Optional unique identifier (generated if not provided)

        Raises:
            ValueError: If description or selector is empty
        """
        super().__init__(description, action_id)
        if not selector:
            raise ValueError("Selector cannot be empty")
        self.selector = selector

    @property
    def type(self) -> str:
        """
        Get the action type

        Returns:
            String identifier for the action type
        """
        return "click"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the click action

        Args:
            context: Execution context containing browser, etc.

        Returns:
            Result of the action execution
        """
        # Get the browser driver from the context
        driver = context.get("driver")
        if not driver:
            return ActionResult.create_failure("No browser driver in context")

        try:
            # Find the element and click it
            element = driver.find_element_by_css_selector(self.selector)
            element.click()
            return ActionResult.create_success(f"Clicked element: {self.selector}")
        except Exception as e:
            return ActionResult.create_failure(f"Failed to click element: {str(e)}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the action to a dictionary

        Returns:
            Dictionary representation of the action
        """
        data = super().to_dict()
        data["selector"] = self.selector
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClickAction':
        """
        Create an action from a dictionary

        Args:
            data: Dictionary representation of the action

        Returns:
            Instantiated action
        """
        return cls(
            description=data.get("description", ""),
            selector=data.get("selector", ""),
            action_id=data.get("id")
        )
