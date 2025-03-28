"""Condition for checking if an element's text contains a specific string"""
from typing import Dict, Any, Optional

from src.core.conditions.condition_interface import ConditionResult
from src.core.conditions.base_condition import BaseCondition


class TextContainsCondition(BaseCondition[bool]):
    """Condition that checks if an element's text contains a specific string"""

    def __init__(
        self,
        selector: str,
        text: str,
        case_sensitive: bool = False,
        description: Optional[str] = None,
        condition_id: Optional[str] = None
    ):
        """
        Initialize the text contains condition

        Args:
            selector: CSS selector for the element
            text: Text to check for
            case_sensitive: Whether the comparison should be case-sensitive
            description: Human-readable description of the condition
            condition_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(
            description or f"Text contains: {text} in {selector}",
            condition_id
        )
        self.selector = selector
        self.text = text
        self.case_sensitive = case_sensitive

    @property
    def type(self) -> str:
        """Get the condition type"""
        return "text_contains"

    def _evaluate(self, context: Dict[str, Any]) -> ConditionResult[bool]:
        """
        Check if the element's text contains the specified string

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
            if not elements:
                return ConditionResult.create_success(
                    False,
                    f"Element not found: {self.selector}"
                )

            # Get the element's text
            element_text = elements[0].text

            # Check if the text contains the specified string
            if self.case_sensitive:
                contains = self.text in element_text
            else:
                contains = self.text.lower() in element_text.lower()

            if contains:
                return ConditionResult.create_success(
                    True,
                    f"Text found: '{self.text}' in '{element_text}'"
                )
            else:
                return ConditionResult.create_success(
                    False,
                    f"Text not found: '{self.text}' in '{element_text}'"
                )
        except Exception as e:
            return ConditionResult.create_failure(
                f"Error checking text: {str(e)}"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the condition to a dictionary"""
        data = super().to_dict()
        data.update({
            "selector": self.selector,
            "text": self.text,
            "case_sensitive": self.case_sensitive
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextContainsCondition':
        """
        Create a condition from a dictionary

        Args:
            data: Dictionary representation of the condition

        Returns:
            Instantiated condition
        """
        return cls(
            selector=data.get("selector", ""),
            text=data.get("text", ""),
            case_sensitive=data.get("case_sensitive", False),
            description=data.get("description"),
            condition_id=data.get("id")
        )
