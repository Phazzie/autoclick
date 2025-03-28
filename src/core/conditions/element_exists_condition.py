"""Condition for checking if an element exists in the DOM"""
from typing import Dict, Any, Optional

from src.core.conditions.condition_interface import ConditionResult
from src.core.conditions.base_condition import BaseCondition


class ElementExistsCondition(BaseCondition[bool]):
    """Condition that checks if an element exists in the DOM"""

    def __init__(
        self,
        selector: str,
        description: Optional[str] = None,
        condition_id: Optional[str] = None
    ):
        """
        Initialize the element exists condition

        Args:
            selector: CSS selector for the element
            description: Human-readable description of the condition
            condition_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(
            description or f"Element exists: {selector}",
            condition_id
        )
        self.selector = selector

    @property
    def type(self) -> str:
        """Get the condition type"""
        return "element_exists"

    def _evaluate(self, context: Dict[str, Any]) -> ConditionResult[bool]:
        """
        Check if the element exists in the DOM

        Args:
            context: Execution context containing browser, etc.

        Returns:
            Result of the condition evaluation
        """
        # Get the browser driver from the context
        driver = context.get("driver")
        if not driver:
            return ConditionResult.create_failure("No browser driver in context")

        try:
            # Find the element
            elements = driver.find_elements_by_css_selector(self.selector)
            exists = len(elements) > 0

            if exists:
                return ConditionResult.create_success(
                    True,
                    f"Element found: {self.selector}"
                )
            else:
                return ConditionResult.create_success(
                    False,
                    f"Element not found: {self.selector}"
                )
        except Exception as e:
            return ConditionResult.create_failure(
                f"Error finding element: {str(e)}"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the condition to a dictionary"""
        data = super().to_dict()
        data["selector"] = self.selector
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ElementExistsCondition':
        """
        Create a condition from a dictionary

        Args:
            data: Dictionary representation of the condition

        Returns:
            Instantiated condition
        """
        return cls(
            selector=data.get("selector", ""),
            description=data.get("description"),
            condition_id=data.get("id")
        )
