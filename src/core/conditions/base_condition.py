"""Base class for conditions in the automation system"""
import uuid
from abc import abstractmethod
from typing import Dict, Any, Optional, TypeVar, Generic

from src.core.conditions.condition_interface import ConditionInterface, ConditionResult


T = TypeVar('T')


class BaseCondition(ConditionInterface[T], Generic[T]):
    """Base class for all conditions in the automation system"""

    def __init__(self, description: Optional[str] = None, condition_id: Optional[str] = None):
        """
        Initialize the base condition

        Args:
            description: Human-readable description of the condition
            condition_id: Optional unique identifier (generated if not provided)
        """
        self.id = condition_id or str(uuid.uuid4())
        self.description = description or self.__class__.__name__

    def evaluate(self, context: Dict[str, Any]) -> ConditionResult[T]:
        """
        Evaluate the condition with the given context

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the condition evaluation
        """
        try:
            return self._evaluate(context)
        except Exception as e:
            return ConditionResult.create_failure(f"Error evaluating condition: {str(e)}")

    @abstractmethod
    def _evaluate(self, context: Dict[str, Any]) -> ConditionResult[T]:
        """
        Internal method to evaluate the condition

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the condition evaluation
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the condition to a dictionary

        Returns:
            Dictionary representation of the condition
        """
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description
        }

    @property
    @abstractmethod
    def type(self) -> str:
        """
        Get the condition type

        Returns:
            String identifier for the condition type
        """
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseCondition':
        """
        Create a condition from a dictionary

        Args:
            data: Dictionary representation of the condition

        Returns:
            Instantiated condition
        """
        raise NotImplementedError(
            f"from_dict not implemented for {cls.__name__}. "
            "This method should be implemented by subclasses."
        )
