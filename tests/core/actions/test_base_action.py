"""Tests for the BaseAction class"""
import unittest
from unittest.mock import MagicMock
from typing import Dict, Any

from src.core.actions.action_interface import ActionResult
from src.core.actions.base_action import BaseAction


class TestBaseAction(unittest.TestCase):
    """Test cases for the BaseAction class"""

    def test_base_action_initialization(self):
        """Test initializing a BaseAction"""
        # Arrange & Act
        action = ConcreteAction(description="Test action")

        # Assert
        self.assertEqual(action.description, "Test action")
        self.assertIsNotNone(action.id)

    def test_base_action_with_id(self):
        """Test initializing a BaseAction with a specific ID"""
        # Arrange & Act
        action = ConcreteAction(description="Test action", action_id="test-id")

        # Assert
        self.assertEqual(action.id, "test-id")

    def test_base_action_validation(self):
        """Test BaseAction parameter validation"""
        # Arrange & Act & Assert
        with self.assertRaises(ValueError):
            ConcreteAction(description="")  # Empty description

    def test_base_action_serialization(self):
        """Test serializing a BaseAction to dict"""
        # Arrange
        action = ConcreteAction(description="Test action", action_id="test-id")

        # Act
        serialized = action.to_dict()

        # Assert
        self.assertEqual(serialized["id"], "test-id")
        self.assertEqual(serialized["type"], "concrete")
        self.assertEqual(serialized["description"], "Test action")

    def test_base_action_deserialization(self):
        """Test deserializing a dict to BaseAction"""
        # Arrange
        data = {
            "id": "test-id",
            "type": "concrete",
            "description": "Test action"
        }

        # Act
        action = ConcreteAction.from_dict(data)

        # Assert
        self.assertEqual(action.id, "test-id")
        self.assertEqual(action.description, "Test action")

    def test_base_action_logging(self):
        """Test BaseAction logging"""
        # Arrange
        action = ConcreteAction(description="Test action")
        mock_logger = MagicMock()
        action.logger = mock_logger
        context = {}

        # Act
        action.execute(context)

        # Assert
        mock_logger.info.assert_called_with("Executing action: Test action")


# Concrete implementation of BaseAction for testing
class ConcreteAction(BaseAction):
    """Concrete implementation of BaseAction for testing"""

    @property
    def type(self) -> str:
        return "concrete"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        # Unused context parameter is required by the interface
        return ActionResult.create_success("Concrete action executed")


if __name__ == "__main__":
    unittest.main()
