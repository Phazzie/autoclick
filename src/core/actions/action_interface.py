"""Interface for actions in the automation system"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import copy


class ActionResult:
    """Result of an action execution"""

    def __init__(self, success: bool, message: str, data: Optional[Dict[str, Any]] = None):
        """Initialize the action result"""
        self._success = success
        self._message = message
        self._data = copy.deepcopy(data or {})

    @property
    def success(self) -> bool:
        """Get the success status"""
        return self._success

    @property
    def message(self) -> str:
        """Get the message"""
        return self._message

    @property
    def data(self) -> Dict[str, Any]:
        """Get the data (copy to prevent modification)"""
        return copy.deepcopy(self._data)

    def __str__(self) -> str:
        """String representation"""
        return f"ActionResult(success={self._success}, message='{self._message}')"

    @classmethod
    def create_success(cls, message: str, data: Optional[Dict[str, Any]] = None) -> 'ActionResult':
        """
        Create a successful result

        Args:
            message: Success message
            data: Optional result data

        Returns:
            ActionResult with success=True
        """
        return cls(True, message, data)

    @classmethod
    def create_failure(cls, message: str, data: Optional[Dict[str, Any]] = None) -> 'ActionResult':
        """
        Create a failure result

        Args:
            message: Failure message
            data: Optional result data

        Returns:
            ActionResult with success=False
        """
        return cls(False, message, data)


class ActionInterface(ABC):
    """Interface for all actions in the automation system"""

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action with the given context

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the action execution
        """
        pass
