"""Tests for the condition interface"""
import unittest
from typing import Dict, Any

from src.core.conditions.condition_interface import ConditionInterface, ConditionResult, BooleanCondition


class TestConditionResult(unittest.TestCase):
    """Test cases for the ConditionResult class"""

    def test_create_success(self):
        """Test creating a successful result"""
        # Arrange & Act
        result = ConditionResult.create_success(True, "Success message")

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(result.value)
        self.assertEqual(result.message, "Success message")
        self.assertTrue(bool(result))

    def test_create_failure(self):
        """Test creating a failure result"""
        # Arrange & Act
        result = ConditionResult.create_failure("Failure message")

        # Assert
        self.assertFalse(result.success)
        self.assertFalse(result.value)
        self.assertEqual(result.message, "Failure message")
        self.assertFalse(bool(result))

    def test_boolean_conversion(self):
        """Test boolean conversion of results"""
        # Arrange & Act
        success_true = ConditionResult.create_success(True)
        success_false = ConditionResult.create_success(False)
        failure = ConditionResult.create_failure("Failure")

        # Assert
        self.assertTrue(bool(success_true))
        self.assertFalse(bool(success_false))
        self.assertFalse(bool(failure))

    def test_string_representation(self):
        """Test string representation of results"""
        # Arrange
        result = ConditionResult.create_success(True, "Success message")

        # Act
        result_str = str(result)

        # Assert
        self.assertIn("success=True", result_str)
        self.assertIn("value=True", result_str)
        self.assertIn("message='Success message'", result_str)


# Concrete implementation of ConditionInterface for testing
class TestCondition(BooleanCondition):
    """Test condition for interface tests"""

    def __init__(self, return_value: bool, success: bool = True, message: str = ""):
        """Initialize the test condition"""
        self.return_value = return_value
        self.success = success
        self.message = message

    def evaluate(self, context: Dict[str, Any]) -> ConditionResult[bool]:
        """Evaluate the condition"""
        if self.success:
            return ConditionResult.create_success(self.return_value, self.message)
        else:
            return ConditionResult.create_failure(self.message)


class TestConditionInterface(unittest.TestCase):
    """Test cases for the ConditionInterface"""

    def test_and_operator(self):
        """Test the AND operator"""
        # Arrange
        condition1 = TestCondition(True)
        condition2 = TestCondition(True)
        condition3 = TestCondition(False)

        # Act
        and_condition1 = condition1 & condition2
        and_condition2 = condition1 & condition3

        # Evaluate
        result1 = and_condition1.evaluate({})
        result2 = and_condition2.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)

    def test_or_operator(self):
        """Test the OR operator"""
        # Arrange
        condition1 = TestCondition(True)
        condition2 = TestCondition(False)
        condition3 = TestCondition(False)

        # Act
        or_condition1 = condition1 | condition2
        or_condition2 = condition2 | condition3

        # Evaluate
        result1 = or_condition1.evaluate({})
        result2 = or_condition2.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)

    def test_not_operator(self):
        """Test the NOT operator"""
        # Arrange
        condition1 = TestCondition(True)
        condition2 = TestCondition(False)

        # Act
        not_condition1 = ~condition1
        not_condition2 = ~condition2

        # Evaluate
        result1 = not_condition1.evaluate({})
        result2 = not_condition2.evaluate({})

        # Assert
        self.assertFalse(result1.value)
        self.assertTrue(result2.value)

    def test_complex_condition(self):
        """Test a complex condition with multiple operators"""
        # Arrange
        condition1 = TestCondition(True)
        condition2 = TestCondition(False)
        condition3 = TestCondition(True)

        # Act - (condition1 AND NOT condition2) OR condition3
        complex_condition = (condition1 & ~condition2) | condition3

        # Evaluate
        result = complex_condition.evaluate({})

        # Assert
        self.assertTrue(result.value)


if __name__ == "__main__":
    unittest.main()
