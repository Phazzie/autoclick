"""
Standard condition provider implementation.

This module provides an implementation of the IConditionProvider interface,
for providing standard condition types.
"""

from .condition_provider import BaseConditionProvider
from .compound_conditions import AndCondition, OrCondition, NotCondition
from .standard_conditions import TrueCondition, FalseCondition


class StandardConditionProvider(BaseConditionProvider):
    """
    Implementation of a standard condition provider.

    This class provides an implementation of the IConditionProvider interface,
    for providing standard condition types such as AND, OR, and NOT.
    """

    def __init__(self):
        """Initialize a standard condition provider."""
        super().__init__("standard", "Standard Conditions", "Provides standard condition types")

        # Register standard condition types
        self._register_standard_conditions()

    def _register_standard_conditions(self) -> None:
        """Register standard condition types."""
        # Register AND condition
        self.register_condition_type("and", AndCondition, {
            "type": "object",
            "properties": {
                "condition_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "conditions": {
                    "type": "array",
                    "items": {"type": "object"}
                }
            }
        })

        # Register OR condition
        self.register_condition_type("or", OrCondition, {
            "type": "object",
            "properties": {
                "condition_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "conditions": {
                    "type": "array",
                    "items": {"type": "object"}
                }
            }
        })

        # Register NOT condition
        self.register_condition_type("not", NotCondition, {
            "type": "object",
            "properties": {
                "condition_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "condition": {"type": "object"}
            },
            "required": ["condition"]
        })

        # Register TRUE condition
        self.register_condition_factory("true", lambda config: TrueCondition(config), {
            "type": "object",
            "properties": {
                "condition_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"}
            }
        })

        # Register FALSE condition
        self.register_condition_factory("false", lambda config: FalseCondition(config), {
            "type": "object",
            "properties": {
                "condition_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"}
            }
        })
