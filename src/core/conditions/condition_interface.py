"""Interface for conditions in the automation system"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, TypeVar, Generic, Callable

# Type variable for the result of condition evaluation
T = TypeVar('T')


class ConditionResult(Generic[T]):
    """Result of a condition evaluation"""

    def __init__(self, success: bool, value: T, message: Optional[str] = None):
        """
        Initialize the condition result

        Args:
            success: Whether the condition evaluation was successful
            value: The value of the condition evaluation
            message: Optional message describing the result
        """
        self._success = success
        self._value = value
        self._message = message or ""

    @property
    def success(self) -> bool:
        """Get whether the condition evaluation was successful"""
        return self._success

    @property
    def value(self) -> T:
        """Get the value of the condition evaluation"""
        return self._value

    @property
    def message(self) -> str:
        """Get the message describing the result"""
        return self._message

    def __bool__(self) -> bool:
        """
        Boolean conversion for the result

        Returns:
            True if the condition evaluation was successful and the value is truthy,
            False otherwise
        """
        return self._success and bool(self._value)

    def __str__(self) -> str:
        """String representation of the result"""
        return f"ConditionResult(success={self._success}, value={self._value}, message='{self._message}')"

    @classmethod
    def create_success(cls, value: T, message: Optional[str] = None) -> 'ConditionResult[T]':
        """
        Create a successful result

        Args:
            value: The value of the condition evaluation
            message: Optional message describing the result

        Returns:
            ConditionResult with success=True
        """
        return cls(True, value, message)

    @classmethod
    def create_failure(cls, message: str, value: Optional[T] = None) -> 'ConditionResult[T]':
        """
        Create a failure result

        Args:
            message: Message describing the failure
            value: Optional value (defaults to None or False for boolean results)

        Returns:
            ConditionResult with success=False
        """
        # Use None or False as the default value for failures
        default_value = None
        if isinstance(value, bool) or value is None:
            default_value = False  # type: ignore

        return cls(False, value if value is not None else default_value, message)  # type: ignore


class ConditionInterface(ABC, Generic[T]):
    """Interface for all conditions in the automation system"""

    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> ConditionResult[T]:
        """
        Evaluate the condition with the given context

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the condition evaluation
        """
        pass

    def __and__(self, other: 'ConditionInterface') -> 'ConditionInterface':
        """
        Combine this condition with another using AND logic

        Args:
            other: Another condition to combine with

        Returns:
            A new condition that evaluates to True only if both conditions are True
        """
        # Import here to avoid circular dependency
        from src.core.conditions.composite_conditions import AndCondition
        return AndCondition(self, other)

    def __or__(self, other: 'ConditionInterface') -> 'ConditionInterface':
        """
        Combine this condition with another using OR logic

        Args:
            other: Another condition to combine with

        Returns:
            A new condition that evaluates to True if either condition is True
        """
        # Import here to avoid circular dependency
        from src.core.conditions.composite_conditions import OrCondition
        return OrCondition(self, other)

    def __invert__(self) -> 'ConditionInterface':
        """
        Negate this condition using NOT logic

        Returns:
            A new condition that evaluates to True only if this condition is False
        """
        # Import here to avoid circular dependency
        from src.core.conditions.composite_conditions import NotCondition
        return NotCondition(self)


# Type alias for boolean conditions (most common case)
BooleanCondition = ConditionInterface[bool]


# Function type for condition factories
ConditionFactory = Callable[..., ConditionInterface]
