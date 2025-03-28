"""Comparison conditions for comparing values"""
from enum import Enum, auto
from typing import Dict, Any, Optional, Union, TypeVar, Generic, cast

from src.core.conditions.condition_interface import ConditionResult
from src.core.conditions.base_condition import BaseCondition


T = TypeVar('T')


class ComparisonOperator(Enum):
    """Operators for comparing values"""
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_THAN_OR_EQUAL = auto()
    LESS_THAN = auto()
    LESS_THAN_OR_EQUAL = auto()
    CONTAINS = auto()
    NOT_CONTAINS = auto()
    STARTS_WITH = auto()
    ENDS_WITH = auto()
    MATCHES_REGEX = auto()


class ComparisonCondition(BaseCondition[bool], Generic[T]):
    """Condition that compares two values"""

    def __init__(
        self,
        left_value: Union[T, str],
        operator: ComparisonOperator,
        right_value: Union[T, str],
        description: Optional[str] = None,
        condition_id: Optional[str] = None
    ):
        """
        Initialize the comparison condition

        Args:
            left_value: Left value or variable name to compare
            operator: Comparison operator
            right_value: Right value or variable name to compare
            description: Human-readable description of the condition
            condition_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(
            description or f"Compare {left_value} {operator.name} {right_value}",
            condition_id
        )
        self.left_value = left_value
        self.operator = operator
        self.right_value = right_value

    @property
    def type(self) -> str:
        """Get the condition type"""
        return "comparison"

    def _evaluate(self, context: Dict[str, Any]) -> ConditionResult[bool]:
        """
        Evaluate the comparison with the given context

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the condition evaluation
        """
        # Resolve values (if they are variable names)
        left = self._resolve_value(self.left_value, context)
        right = self._resolve_value(self.right_value, context)

        # Perform the comparison
        try:
            result = self._compare(left, right)
            return ConditionResult.create_success(
                result,
                f"Comparison {left} {self.operator.name} {right} is {result}"
            )
        except Exception as e:
            return ConditionResult.create_failure(
                f"Error comparing values: {str(e)}"
            )

    def _resolve_value(self, value: Union[T, str], context: Dict[str, Any]) -> Any:
        """
        Resolve a value or variable name to its actual value

        Args:
            value: Value or variable name
            context: Execution context

        Returns:
            Resolved value
        """
        if isinstance(value, str) and value.startswith("$"):
            # It's a variable reference
            var_name = value[1:]
            if var_name in context:
                return context[var_name]
            else:
                raise ValueError(f"Variable not found: {var_name}")
        return value

    def _compare(self, left: Any, right: Any) -> bool:
        """
        Compare two values using the specified operator

        Args:
            left: Left value
            right: Right value

        Returns:
            Result of the comparison
        """
        if self.operator == ComparisonOperator.EQUAL:
            return left == right
        elif self.operator == ComparisonOperator.NOT_EQUAL:
            return left != right
        elif self.operator == ComparisonOperator.GREATER_THAN:
            return left > right
        elif self.operator == ComparisonOperator.GREATER_THAN_OR_EQUAL:
            return left >= right
        elif self.operator == ComparisonOperator.LESS_THAN:
            return left < right
        elif self.operator == ComparisonOperator.LESS_THAN_OR_EQUAL:
            return left <= right
        elif self.operator == ComparisonOperator.CONTAINS:
            if isinstance(left, str) and isinstance(right, str):
                return right in left
            elif hasattr(left, "__contains__"):
                return right in left
            else:
                raise TypeError(f"Cannot check if {type(left)} contains {type(right)}")
        elif self.operator == ComparisonOperator.NOT_CONTAINS:
            if isinstance(left, str) and isinstance(right, str):
                return right not in left
            elif hasattr(left, "__contains__"):
                return right not in left
            else:
                raise TypeError(f"Cannot check if {type(left)} contains {type(right)}")
        elif self.operator == ComparisonOperator.STARTS_WITH:
            if isinstance(left, str) and isinstance(right, str):
                return left.startswith(right)
            else:
                raise TypeError(f"Cannot check if {type(left)} starts with {type(right)}")
        elif self.operator == ComparisonOperator.ENDS_WITH:
            if isinstance(left, str) and isinstance(right, str):
                return left.endswith(right)
            else:
                raise TypeError(f"Cannot check if {type(left)} ends with {type(right)}")
        elif self.operator == ComparisonOperator.MATCHES_REGEX:
            import re
            if isinstance(left, str) and isinstance(right, str):
                return bool(re.search(right, left))
            else:
                raise TypeError(f"Cannot match regex {type(right)} against {type(left)}")
        else:
            raise ValueError(f"Unknown operator: {self.operator}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the condition to a dictionary"""
        data = super().to_dict()
        data.update({
            "left_value": self.left_value,
            "operator": self.operator.name,
            "right_value": self.right_value
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ComparisonCondition':
        """
        Create a condition from a dictionary

        Args:
            data: Dictionary representation of the condition

        Returns:
            Instantiated condition
        """
        return cls(
            left_value=data.get("left_value"),
            operator=ComparisonOperator[data.get("operator", "EQUAL")],
            right_value=data.get("right_value"),
            description=data.get("description"),
            condition_id=data.get("id")
        )
