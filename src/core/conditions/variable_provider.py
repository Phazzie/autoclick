"""
Variable condition provider implementation.

This module provides an implementation of the IConditionProvider interface,
for providing variable-related condition types.
"""
# No imports needed from typing

from .condition_provider import BaseConditionProvider
from .variable_conditions import (
    VariableCompareCondition, VariableExistsCondition,
    VariableEmptyCondition, VariableTypeCondition
)


class VariableConditionProvider(BaseConditionProvider):
    """
    Implementation of a variable condition provider.

    This class provides an implementation of the IConditionProvider interface,
    for providing variable-related condition types.
    """

    def __init__(self):
        """Initialize a variable condition provider."""
        super().__init__("variable", "Variable Conditions", "Provides variable-related condition types")

        # Register variable condition types
        self._register_variable_conditions()

    def _register_variable_conditions(self) -> None:
        """Register variable condition types."""
        # Register variable comparison condition
        self.register_condition_type("variable_compare", VariableCompareCondition, {
            "type": "object",
            "properties": {
                "condition_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "variable": {"type": "string"},
                "operator": {"type": "string", "enum": ["eq", "ne", "lt", "le", "gt", "ge", "contains", "not_contains", "starts_with", "ends_with", "matches"]},
                "value": {"type": ["string", "number", "boolean", "null"]}
            },
            "required": ["variable", "operator", "value"]
        })

        # Register variable exists condition
        self.register_condition_type("variable_exists", VariableExistsCondition, {
            "type": "object",
            "properties": {
                "condition_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "variable": {"type": "string"}
            },
            "required": ["variable"]
        })

        # Register variable empty condition
        self.register_condition_type("variable_empty", VariableEmptyCondition, {
            "type": "object",
            "properties": {
                "condition_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "variable": {"type": "string"}
            },
            "required": ["variable"]
        })

        # Register variable type condition
        self.register_condition_type("variable_type", VariableTypeCondition, {
            "type": "object",
            "properties": {
                "condition_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "variable": {"type": "string"},
                "type": {"type": "string", "enum": ["string", "number", "boolean", "list", "dict", "null"]}
            },
            "required": ["variable", "type"]
        })
