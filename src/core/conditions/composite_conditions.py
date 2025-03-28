"""Composite conditions for combining multiple conditions"""
from typing import Dict, Any, List, Optional

from src.core.conditions.condition_interface import ConditionInterface, ConditionResult, BooleanCondition
from src.core.conditions.base_condition import BaseCondition


class AndCondition(BaseCondition[bool]):
    """Condition that evaluates to True only if all subconditions are True"""

    def __init__(
        self,
        *conditions: ConditionInterface,
        description: Optional[str] = None,
        condition_id: Optional[str] = None
    ):
        """
        Initialize the AND condition

        Args:
            *conditions: Subconditions to combine with AND logic
            description: Human-readable description of the condition
            condition_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(
            description or "AND condition",
            condition_id
        )
        if not conditions:
            raise ValueError("AND condition requires at least one subcondition")
        self.conditions = list(conditions)

    @property
    def type(self) -> str:
        """Get the condition type"""
        return "and"

    def _evaluate(self, context: Dict[str, Any]) -> ConditionResult[bool]:
        """
        Evaluate all subconditions with AND logic

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the condition evaluation
        """
        results = []
        for condition in self.conditions:
            result = condition.evaluate(context)
            results.append(result)
            
            # Short-circuit evaluation: if any condition is False, the AND is False
            if not result:
                return ConditionResult.create_success(
                    False,
                    f"AND condition failed: {result.message}"
                )

        # All conditions are True
        return ConditionResult.create_success(
            True,
            "All conditions in AND are True"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the condition to a dictionary"""
        data = super().to_dict()
        data["conditions"] = [
            condition.to_dict() if hasattr(condition, "to_dict") else {"type": "unknown"}
            for condition in self.conditions
        ]
        return data


class OrCondition(BaseCondition[bool]):
    """Condition that evaluates to True if any subcondition is True"""

    def __init__(
        self,
        *conditions: ConditionInterface,
        description: Optional[str] = None,
        condition_id: Optional[str] = None
    ):
        """
        Initialize the OR condition

        Args:
            *conditions: Subconditions to combine with OR logic
            description: Human-readable description of the condition
            condition_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(
            description or "OR condition",
            condition_id
        )
        if not conditions:
            raise ValueError("OR condition requires at least one subcondition")
        self.conditions = list(conditions)

    @property
    def type(self) -> str:
        """Get the condition type"""
        return "or"

    def _evaluate(self, context: Dict[str, Any]) -> ConditionResult[bool]:
        """
        Evaluate all subconditions with OR logic

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the condition evaluation
        """
        failure_messages = []
        for condition in self.conditions:
            result = condition.evaluate(context)
            
            # Short-circuit evaluation: if any condition is True, the OR is True
            if result:
                return ConditionResult.create_success(
                    True,
                    f"OR condition succeeded: {result.message}"
                )
            
            failure_messages.append(result.message)

        # All conditions are False
        return ConditionResult.create_success(
            False,
            f"All conditions in OR are False: {'; '.join(failure_messages)}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the condition to a dictionary"""
        data = super().to_dict()
        data["conditions"] = [
            condition.to_dict() if hasattr(condition, "to_dict") else {"type": "unknown"}
            for condition in self.conditions
        ]
        return data


class NotCondition(BaseCondition[bool]):
    """Condition that negates another condition"""

    def __init__(
        self,
        condition: ConditionInterface,
        description: Optional[str] = None,
        condition_id: Optional[str] = None
    ):
        """
        Initialize the NOT condition

        Args:
            condition: Subcondition to negate
            description: Human-readable description of the condition
            condition_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(
            description or f"NOT ({getattr(condition, 'description', 'condition')})",
            condition_id
        )
        self.condition = condition

    @property
    def type(self) -> str:
        """Get the condition type"""
        return "not"

    def _evaluate(self, context: Dict[str, Any]) -> ConditionResult[bool]:
        """
        Evaluate the subcondition and negate the result

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the condition evaluation
        """
        result = self.condition.evaluate(context)
        
        # Negate the result
        return ConditionResult.create_success(
            not bool(result),
            f"NOT condition: {result.message}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the condition to a dictionary"""
        data = super().to_dict()
        data["condition"] = (
            self.condition.to_dict() 
            if hasattr(self.condition, "to_dict") 
            else {"type": "unknown"}
        )
        return data
