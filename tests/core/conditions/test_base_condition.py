"""Tests for the base condition"""
import unittest
from typing import Dict, Any

from src.core.conditions.condition_interface import ConditionResult
from src.core.conditions.base_condition import BaseCondition


# Concrete implementation of BaseCondition for testing
class TestCondition(BaseCondition[bool]):
    """Test condition for base condition tests"""

    def __init__(self, return_value: bool, raise_exception: bool = False, description: str = None, condition_id: str = None):
        """Initialize the test condition"""
        super().__init__(description, condition_id)
        self.return_value = return_value
        self.raise_exception = raise_exception

    @property
    def type(self) -> str:
        """Get the condition type"""
        return "test_condition"

    def _evaluate(self, context: Dict[str, Any]) -> ConditionResult[bool]:
        """Evaluate the condition"""
        if self.raise_exception:
            raise ValueError("Test exception")
        return ConditionResult.create_success(self.return_value, "Test message")


class TestBaseCondition(unittest.TestCase):
    """Test cases for the BaseCondition class"""

    def test_initialization(self):
        """Test initializing a base condition"""
        # Arrange & Act
        condition = TestCondition(True, description="Test description", condition_id="test-id")

        # Assert
        self.assertEqual(condition.description, "Test description")
        self.assertEqual(condition.id, "test-id")
        self.assertEqual(condition.type, "test_condition")

    def test_auto_generated_id(self):
        """Test that an ID is auto-generated if not provided"""
        # Arrange & Act
        condition = TestCondition(True)

        # Assert
        self.assertIsNotNone(condition.id)
        self.assertTrue(len(condition.id) > 0)

    def test_default_description(self):
        """Test that a default description is used if not provided"""
        # Arrange & Act
        condition = TestCondition(True)

        # Assert
        self.assertEqual(condition.description, "TestCondition")

    def test_evaluate_success(self):
        """Test evaluating a condition that succeeds"""
        # Arrange
        condition = TestCondition(True)

        # Act
        result = condition.evaluate({})

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(result.value)
        self.assertEqual(result.message, "Test message")

    def test_evaluate_exception(self):
        """Test evaluating a condition that raises an exception"""
        # Arrange
        condition = TestCondition(True, raise_exception=True)

        # Act
        result = condition.evaluate({})

        # Assert
        self.assertFalse(result.success)
        self.assertFalse(result.value)
        self.assertIn("Error evaluating condition", result.message)
        self.assertIn("Test exception", result.message)

    def test_to_dict(self):
        """Test converting a condition to a dictionary"""
        # Arrange
        condition = TestCondition(True, description="Test description", condition_id="test-id")

        # Act
        data = condition.to_dict()

        # Assert
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "test_condition")
        self.assertEqual(data["description"], "Test description")

    def test_from_dict_not_implemented(self):
        """Test that from_dict raises NotImplementedError"""
        # Arrange & Act & Assert
        with self.assertRaises(NotImplementedError):
            BaseCondition.from_dict({})


if __name__ == "__main__":
    unittest.main()
