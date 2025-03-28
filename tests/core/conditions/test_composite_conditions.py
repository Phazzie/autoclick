"""Tests for the composite conditions"""
import unittest
from typing import Dict, Any

from src.core.conditions.condition_interface import ConditionResult
from src.core.conditions.base_condition import BaseCondition
from src.core.conditions.composite_conditions import AndCondition, OrCondition, NotCondition


# Simple condition for testing
class TestCondition(BaseCondition[bool]):
    """Test condition for composite condition tests"""

    def __init__(self, return_value: bool, description: str = None, condition_id: str = None):
        """Initialize the test condition"""
        super().__init__(description, condition_id)
        self.return_value = return_value
        self.evaluated = False

    @property
    def type(self) -> str:
        """Get the condition type"""
        return "test_condition"

    def _evaluate(self, context: Dict[str, Any]) -> ConditionResult[bool]:
        """Evaluate the condition"""
        self.evaluated = True
        return ConditionResult.create_success(
            self.return_value,
            f"Test condition returned {self.return_value}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the condition to a dictionary"""
        data = super().to_dict()
        data["return_value"] = self.return_value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestCondition':
        """Create a condition from a dictionary"""
        return cls(
            return_value=data.get("return_value", False),
            description=data.get("description"),
            condition_id=data.get("id")
        )


class TestAndCondition(unittest.TestCase):
    """Test cases for the AndCondition class"""

    def test_initialization(self):
        """Test initializing an AND condition"""
        # Arrange
        condition1 = TestCondition(True)
        condition2 = TestCondition(False)

        # Act
        and_condition = AndCondition(condition1, condition2, description="Test AND")

        # Assert
        self.assertEqual(and_condition.description, "Test AND")
        self.assertEqual(and_condition.type, "and")
        self.assertEqual(len(and_condition.conditions), 2)
        self.assertEqual(and_condition.conditions[0], condition1)
        self.assertEqual(and_condition.conditions[1], condition2)

    def test_initialization_empty(self):
        """Test initializing an AND condition with no subconditions"""
        # Arrange & Act & Assert
        with self.assertRaises(ValueError):
            AndCondition()

    def test_evaluate_all_true(self):
        """Test evaluating an AND condition where all subconditions are true"""
        # Arrange
        condition1 = TestCondition(True)
        condition2 = TestCondition(True)
        and_condition = AndCondition(condition1, condition2)

        # Act
        result = and_condition.evaluate({})

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(result.value)
        self.assertTrue(condition1.evaluated)
        self.assertTrue(condition2.evaluated)

    def test_evaluate_one_false(self):
        """Test evaluating an AND condition where one subcondition is false"""
        # Arrange
        condition1 = TestCondition(True)
        condition2 = TestCondition(False)
        and_condition = AndCondition(condition1, condition2)

        # Act
        result = and_condition.evaluate({})

        # Assert
        self.assertTrue(result.success)
        self.assertFalse(result.value)
        self.assertTrue(condition1.evaluated)
        self.assertTrue(condition2.evaluated)

    def test_evaluate_short_circuit(self):
        """Test that AND short-circuits evaluation when a false condition is found"""
        # Arrange
        condition1 = TestCondition(False)
        condition2 = TestCondition(True)
        and_condition = AndCondition(condition1, condition2)

        # Act
        result = and_condition.evaluate({})

        # Assert
        self.assertTrue(result.success)
        self.assertFalse(result.value)
        self.assertTrue(condition1.evaluated)
        # condition2 should not be evaluated due to short-circuiting
        self.assertFalse(condition2.evaluated)

    def test_to_dict(self):
        """Test converting an AND condition to a dictionary"""
        # Arrange
        condition1 = TestCondition(True, description="Condition 1")
        condition2 = TestCondition(False, description="Condition 2")
        and_condition = AndCondition(condition1, condition2, description="Test AND", condition_id="test-id")

        # Act
        data = and_condition.to_dict()

        # Assert
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "and")
        self.assertEqual(data["description"], "Test AND")
        self.assertEqual(len(data["conditions"]), 2)
        self.assertEqual(data["conditions"][0]["description"], "Condition 1")
        self.assertEqual(data["conditions"][1]["description"], "Condition 2")


class TestOrCondition(unittest.TestCase):
    """Test cases for the OrCondition class"""

    def test_initialization(self):
        """Test initializing an OR condition"""
        # Arrange
        condition1 = TestCondition(True)
        condition2 = TestCondition(False)

        # Act
        or_condition = OrCondition(condition1, condition2, description="Test OR")

        # Assert
        self.assertEqual(or_condition.description, "Test OR")
        self.assertEqual(or_condition.type, "or")
        self.assertEqual(len(or_condition.conditions), 2)
        self.assertEqual(or_condition.conditions[0], condition1)
        self.assertEqual(or_condition.conditions[1], condition2)

    def test_initialization_empty(self):
        """Test initializing an OR condition with no subconditions"""
        # Arrange & Act & Assert
        with self.assertRaises(ValueError):
            OrCondition()

    def test_evaluate_one_true(self):
        """Test evaluating an OR condition where one subcondition is true"""
        # Arrange
        condition1 = TestCondition(True)
        condition2 = TestCondition(False)
        or_condition = OrCondition(condition1, condition2)

        # Act
        result = or_condition.evaluate({})

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(result.value)
        self.assertTrue(condition1.evaluated)
        # condition2 should not be evaluated due to short-circuiting
        self.assertFalse(condition2.evaluated)

    def test_evaluate_all_false(self):
        """Test evaluating an OR condition where all subconditions are false"""
        # Arrange
        condition1 = TestCondition(False)
        condition2 = TestCondition(False)
        or_condition = OrCondition(condition1, condition2)

        # Act
        result = or_condition.evaluate({})

        # Assert
        self.assertTrue(result.success)
        self.assertFalse(result.value)
        self.assertTrue(condition1.evaluated)
        self.assertTrue(condition2.evaluated)

    def test_evaluate_short_circuit(self):
        """Test that OR short-circuits evaluation when a true condition is found"""
        # Arrange
        condition1 = TestCondition(True)
        condition2 = TestCondition(False)
        or_condition = OrCondition(condition1, condition2)

        # Act
        result = or_condition.evaluate({})

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(result.value)
        self.assertTrue(condition1.evaluated)
        # condition2 should not be evaluated due to short-circuiting
        self.assertFalse(condition2.evaluated)

    def test_to_dict(self):
        """Test converting an OR condition to a dictionary"""
        # Arrange
        condition1 = TestCondition(True, description="Condition 1")
        condition2 = TestCondition(False, description="Condition 2")
        or_condition = OrCondition(condition1, condition2, description="Test OR", condition_id="test-id")

        # Act
        data = or_condition.to_dict()

        # Assert
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "or")
        self.assertEqual(data["description"], "Test OR")
        self.assertEqual(len(data["conditions"]), 2)
        self.assertEqual(data["conditions"][0]["description"], "Condition 1")
        self.assertEqual(data["conditions"][1]["description"], "Condition 2")


class TestNotCondition(unittest.TestCase):
    """Test cases for the NotCondition class"""

    def test_initialization(self):
        """Test initializing a NOT condition"""
        # Arrange
        condition = TestCondition(True, description="Test condition")

        # Act
        not_condition = NotCondition(condition, description="Test NOT")

        # Assert
        self.assertEqual(not_condition.description, "Test NOT")
        self.assertEqual(not_condition.type, "not")
        self.assertEqual(not_condition.condition, condition)

    def test_evaluate_true_to_false(self):
        """Test evaluating a NOT condition that negates a true condition"""
        # Arrange
        condition = TestCondition(True)
        not_condition = NotCondition(condition)

        # Act
        result = not_condition.evaluate({})

        # Assert
        self.assertTrue(result.success)
        self.assertFalse(result.value)
        self.assertTrue(condition.evaluated)

    def test_evaluate_false_to_true(self):
        """Test evaluating a NOT condition that negates a false condition"""
        # Arrange
        condition = TestCondition(False)
        not_condition = NotCondition(condition)

        # Act
        result = not_condition.evaluate({})

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(result.value)
        self.assertTrue(condition.evaluated)

    def test_to_dict(self):
        """Test converting a NOT condition to a dictionary"""
        # Arrange
        condition = TestCondition(True, description="Test condition")
        not_condition = NotCondition(condition, description="Test NOT", condition_id="test-id")

        # Act
        data = not_condition.to_dict()

        # Assert
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "not")
        self.assertEqual(data["description"], "Test NOT")
        self.assertEqual(data["condition"]["description"], "Test condition")


if __name__ == "__main__":
    unittest.main()
