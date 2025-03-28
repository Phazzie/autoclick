"""Tests for the comparison condition"""
import unittest
import re
from typing import Dict, Any

from src.core.conditions.comparison_condition import ComparisonCondition, ComparisonOperator


class TestComparisonCondition(unittest.TestCase):
    """Test cases for the ComparisonCondition class"""

    def test_initialization(self):
        """Test initializing a comparison condition"""
        # Arrange & Act
        condition = ComparisonCondition(
            left_value=10,
            operator=ComparisonOperator.GREATER_THAN,
            right_value=5,
            description="Test comparison",
            condition_id="test-id"
        )

        # Assert
        self.assertEqual(condition.description, "Test comparison")
        self.assertEqual(condition.id, "test-id")
        self.assertEqual(condition.type, "comparison")
        self.assertEqual(condition.left_value, 10)
        self.assertEqual(condition.operator, ComparisonOperator.GREATER_THAN)
        self.assertEqual(condition.right_value, 5)

    def test_equal_operator(self):
        """Test the EQUAL operator"""
        # Arrange
        condition1 = ComparisonCondition(10, ComparisonOperator.EQUAL, 10)
        condition2 = ComparisonCondition(10, ComparisonOperator.EQUAL, 5)

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)

    def test_not_equal_operator(self):
        """Test the NOT_EQUAL operator"""
        # Arrange
        condition1 = ComparisonCondition(10, ComparisonOperator.NOT_EQUAL, 5)
        condition2 = ComparisonCondition(10, ComparisonOperator.NOT_EQUAL, 10)

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)

    def test_greater_than_operator(self):
        """Test the GREATER_THAN operator"""
        # Arrange
        condition1 = ComparisonCondition(10, ComparisonOperator.GREATER_THAN, 5)
        condition2 = ComparisonCondition(5, ComparisonOperator.GREATER_THAN, 10)
        condition3 = ComparisonCondition(10, ComparisonOperator.GREATER_THAN, 10)

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})
        result3 = condition3.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)
        self.assertFalse(result3.value)

    def test_greater_than_or_equal_operator(self):
        """Test the GREATER_THAN_OR_EQUAL operator"""
        # Arrange
        condition1 = ComparisonCondition(10, ComparisonOperator.GREATER_THAN_OR_EQUAL, 5)
        condition2 = ComparisonCondition(10, ComparisonOperator.GREATER_THAN_OR_EQUAL, 10)
        condition3 = ComparisonCondition(5, ComparisonOperator.GREATER_THAN_OR_EQUAL, 10)

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})
        result3 = condition3.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertTrue(result2.value)
        self.assertFalse(result3.value)

    def test_less_than_operator(self):
        """Test the LESS_THAN operator"""
        # Arrange
        condition1 = ComparisonCondition(5, ComparisonOperator.LESS_THAN, 10)
        condition2 = ComparisonCondition(10, ComparisonOperator.LESS_THAN, 5)
        condition3 = ComparisonCondition(10, ComparisonOperator.LESS_THAN, 10)

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})
        result3 = condition3.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)
        self.assertFalse(result3.value)

    def test_less_than_or_equal_operator(self):
        """Test the LESS_THAN_OR_EQUAL operator"""
        # Arrange
        condition1 = ComparisonCondition(5, ComparisonOperator.LESS_THAN_OR_EQUAL, 10)
        condition2 = ComparisonCondition(10, ComparisonOperator.LESS_THAN_OR_EQUAL, 10)
        condition3 = ComparisonCondition(10, ComparisonOperator.LESS_THAN_OR_EQUAL, 5)

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})
        result3 = condition3.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertTrue(result2.value)
        self.assertFalse(result3.value)

    def test_contains_operator(self):
        """Test the CONTAINS operator"""
        # Arrange
        condition1 = ComparisonCondition("hello world", ComparisonOperator.CONTAINS, "world")
        condition2 = ComparisonCondition("hello world", ComparisonOperator.CONTAINS, "universe")
        condition3 = ComparisonCondition([1, 2, 3], ComparisonOperator.CONTAINS, 2)
        condition4 = ComparisonCondition([1, 2, 3], ComparisonOperator.CONTAINS, 4)

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})
        result3 = condition3.evaluate({})
        result4 = condition4.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)
        self.assertTrue(result3.value)
        self.assertFalse(result4.value)

    def test_not_contains_operator(self):
        """Test the NOT_CONTAINS operator"""
        # Arrange
        condition1 = ComparisonCondition("hello world", ComparisonOperator.NOT_CONTAINS, "universe")
        condition2 = ComparisonCondition("hello world", ComparisonOperator.NOT_CONTAINS, "world")
        condition3 = ComparisonCondition([1, 2, 3], ComparisonOperator.NOT_CONTAINS, 4)
        condition4 = ComparisonCondition([1, 2, 3], ComparisonOperator.NOT_CONTAINS, 2)

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})
        result3 = condition3.evaluate({})
        result4 = condition4.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)
        self.assertTrue(result3.value)
        self.assertFalse(result4.value)

    def test_starts_with_operator(self):
        """Test the STARTS_WITH operator"""
        # Arrange
        condition1 = ComparisonCondition("hello world", ComparisonOperator.STARTS_WITH, "hello")
        condition2 = ComparisonCondition("hello world", ComparisonOperator.STARTS_WITH, "world")

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)

    def test_ends_with_operator(self):
        """Test the ENDS_WITH operator"""
        # Arrange
        condition1 = ComparisonCondition("hello world", ComparisonOperator.ENDS_WITH, "world")
        condition2 = ComparisonCondition("hello world", ComparisonOperator.ENDS_WITH, "hello")

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)

    def test_matches_regex_operator(self):
        """Test the MATCHES_REGEX operator"""
        # Arrange
        condition1 = ComparisonCondition("hello world", ComparisonOperator.MATCHES_REGEX, r"hello\s\w+")
        condition2 = ComparisonCondition("hello world", ComparisonOperator.MATCHES_REGEX, r"goodbye\s\w+")

        # Act
        result1 = condition1.evaluate({})
        result2 = condition2.evaluate({})

        # Assert
        self.assertTrue(result1.value)
        self.assertFalse(result2.value)

    def test_variable_resolution(self):
        """Test resolving variables in the context"""
        # Arrange
        context = {"x": 10, "y": 5}
        condition = ComparisonCondition("$x", ComparisonOperator.GREATER_THAN, "$y")

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertTrue(result.value)

    def test_variable_not_found(self):
        """Test handling of variables not found in the context"""
        # Arrange
        context = {"x": 10}
        condition = ComparisonCondition("$x", ComparisonOperator.GREATER_THAN, "$y")

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertFalse(result.success)
        self.assertIn("Variable not found", result.message)

    def test_invalid_operator(self):
        """Test handling of invalid operators"""
        # Arrange
        # Create a condition with an invalid operator (using a hack for testing)
        condition = ComparisonCondition(10, ComparisonOperator.EQUAL, 10)
        condition.operator = "INVALID"  # type: ignore

        # Act
        result = condition.evaluate({})

        # Assert
        self.assertFalse(result.success)
        self.assertIn("Unknown operator", result.message)

    def test_type_error(self):
        """Test handling of type errors"""
        # Arrange
        condition = ComparisonCondition(10, ComparisonOperator.STARTS_WITH, 5)

        # Act
        result = condition.evaluate({})

        # Assert
        self.assertFalse(result.success)
        self.assertIn("Cannot check if", result.message)

    def test_to_dict(self):
        """Test converting a comparison condition to a dictionary"""
        # Arrange
        condition = ComparisonCondition(
            left_value=10,
            operator=ComparisonOperator.GREATER_THAN,
            right_value=5,
            description="Test comparison",
            condition_id="test-id"
        )

        # Act
        data = condition.to_dict()

        # Assert
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "comparison")
        self.assertEqual(data["description"], "Test comparison")
        self.assertEqual(data["left_value"], 10)
        self.assertEqual(data["operator"], "GREATER_THAN")
        self.assertEqual(data["right_value"], 5)

    def test_from_dict(self):
        """Test creating a comparison condition from a dictionary"""
        # Arrange
        data = {
            "id": "test-id",
            "type": "comparison",
            "description": "Test comparison",
            "left_value": 10,
            "operator": "GREATER_THAN",
            "right_value": 5
        }

        # Act
        condition = ComparisonCondition.from_dict(data)

        # Assert
        self.assertEqual(condition.id, "test-id")
        self.assertEqual(condition.description, "Test comparison")
        self.assertEqual(condition.left_value, 10)
        self.assertEqual(condition.operator, ComparisonOperator.GREATER_THAN)
        self.assertEqual(condition.right_value, 5)


if __name__ == "__main__":
    unittest.main()
