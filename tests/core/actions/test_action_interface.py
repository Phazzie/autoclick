"""Tests for the ActionInterface"""
import unittest
from typing import Dict, Any

from src.core.actions.action_interface import ActionInterface, ActionResult


class TestActionInterface(unittest.TestCase):
    """Test cases for the ActionInterface"""

    def test_action_result_success(self):
        """Test creating a successful ActionResult"""
        # Arrange & Act
        result = ActionResult.create_success("Operation completed")

        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Operation completed")
        self.assertEqual(result.data, {})

    def test_action_result_failure(self):
        """Test creating a failed ActionResult"""
        # Arrange & Act
        result = ActionResult.create_failure("Operation failed")

        # Assert
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Operation failed")
        self.assertEqual(result.data, {})

    def test_action_result_with_data(self):
        """Test creating an ActionResult with data"""
        # Arrange
        data = {"key": "value"}

        # Act
        result = ActionResult.create_success("Operation with data", data)

        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Operation with data")
        self.assertEqual(result.data, data)

    def test_action_result_immutable(self):
        """Test that ActionResult data is immutable"""
        # Arrange
        data = {"key": "value"}
        result = ActionResult.create_success("Operation with data", data)

        # Act
        data["key"] = "modified"

        # Assert - The result's data should not be modified
        self.assertEqual(result.data["key"], "value")

    def test_mock_action_implementation(self):
        """Test a mock implementation of ActionInterface"""
        # Arrange
        class MockAction(ActionInterface):
            def execute(self, context: Dict[str, Any]) -> ActionResult:
                # Unused context parameter is required by the interface
                return ActionResult.create_success("Mock executed")

        action = MockAction()
        context = {}

        # Act
        result = action.execute(context)

        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Mock executed")


if __name__ == "__main__":
    unittest.main()
