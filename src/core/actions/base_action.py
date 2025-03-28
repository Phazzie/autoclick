"""Base implementation of the ActionInterface"""
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from src.core.actions.action_interface import ActionInterface, ActionResult


class BaseAction(ActionInterface, ABC):
    """Base class for all actions"""

    def __init__(self, description: str, action_id: Optional[str] = None) -> None:
        """
        Initialize the action

        Args:
            description: Human-readable description of the action
            action_id: Optional unique identifier (generated if not provided)

        Raises:
            ValueError: If description is empty
        """
        if not description:
            raise ValueError("Action description cannot be empty")

        self.description = description
        self.id = action_id or str(uuid.uuid4())
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    @property
    @abstractmethod
    def type(self) -> str:
        """
        Get the action type

        Returns:
            String identifier for the action type
        """
        pass

    def execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action with the given context

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the action execution
        """
        self.logger.info(f"Executing action: {self.description}")

        try:
            return self._execute(context)
        except Exception as e:
            self.logger.error(f"Action execution failed for action '{self.description}' (ID: {self.id}): {str(e)}", exc_info=True)
            return ActionResult.create_failure(f"Action '{self.description}' failed: {str(e)}")

    @abstractmethod
    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Implement the actual execution logic

        Args:
            context: Execution context

        Returns:
            Result of the action execution
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the action to a dictionary

        Returns:
            Dictionary representation of the action
        """
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseAction':
        """
        Create an action from a dictionary

        Args:
            data: Dictionary representation of the action

        Returns:
            Instantiated action
        """
        return cls(
            description=data.get("description", ""),
            action_id=data.get("id")
        )
