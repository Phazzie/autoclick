"""
Tests for the base condition implementation.

This module contains tests for the base condition implementation.
"""
import unittest
from unittest.mock import Mock

from src.core.conditions.base_condition_new import BaseCondition
from src.core.conditions.exceptions import ConditionEvaluationError


class TestBaseCondition(unittest.TestCase):
    """Tests for the BaseCondition class."""
    
    def test_basic_properties(self):
        """Test basic condition properties."""
        # Create a condition with minimal configuration
        condition = TestCondition({
            "condition_type": "test"
        })
        
        # Check properties
        self.assertIsNotNone(condition.condition_id)
        self.assertEqual(condition.condition_type, "test")
        self.assertEqual(condition.name, "Test Condition")
        self.assertIsNone(condition.description)
        self.assertEqual(condition.config, {})
        
        # Create a condition with full configuration
        condition = TestCondition({
            "condition_id": "test-condition",
            "condition_type": "test",
            "name": "Test Condition",
            "description": "Test condition description",
            "param1": "value1",
            "param2": "value2"
        })
        
        # Check properties
        self.assertEqual(condition.condition_id, "test-condition")
        self.assertEqual(condition.condition_type, "test")
        self.assertEqual(condition.name, "Test Condition")
        self.assertEqual(condition.description, "Test condition description")
        self.assertEqual(condition.config, {
            "param1": "value1",
            "param2": "value2"
        })
    
    def test_evaluate(self):
        """Test condition evaluation."""
        # Create a condition that evaluates to True
        condition = TestCondition({
            "condition_type": "test",
            "result": True
        })
        
        # Create a mock context
        context = Mock()
        
        # Evaluate the condition
        result = condition.evaluate(context)
        
        # Check the result
        self.assertTrue(result)
        
        # Create a condition that evaluates to False
        condition = TestCondition({
            "condition_type": "test",
            "result": False
        })
        
        # Evaluate the condition
        result = condition.evaluate(context)
        
        # Check the result
        self.assertFalse(result)
        
        # Create a condition that raises an exception
        condition = TestCondition({
            "condition_type": "test",
            "raise_exception": True
        })
        
        # Evaluate the condition
        with self.assertRaises(ConditionEvaluationError):
            condition.evaluate(context)
    
    def test_validate(self):
        """Test condition validation."""
        # Create a valid condition
        condition = TestCondition({
            "condition_id": "test-condition",
            "condition_type": "test",
            "name": "Test Condition"
        })
        
        # Validate the condition
        errors = condition.validate()
        
        # Check the errors
        self.assertEqual(errors, [])
        
        # Create an invalid condition
        condition = TestCondition({
            "condition_type": "test",
            "name": "",
            "invalid": True
        })
        
        # Validate the condition
        errors = condition.validate()
        
        # Check the errors
        self.assertEqual(len(errors), 2)
        self.assertIn("Condition name is required", errors)
        self.assertIn("Invalid parameter", errors)
    
    def test_to_dict(self):
        """Test converting condition to dictionary."""
        # Create a condition
        condition = TestCondition({
            "condition_id": "test-condition",
            "condition_type": "test",
            "name": "Test Condition",
            "description": "Test condition description",
            "param1": "value1",
            "param2": "value2"
        })
        
        # Convert to dictionary
        data = condition.to_dict()
        
        # Check the dictionary
        self.assertEqual(data["condition_id"], "test-condition")
        self.assertEqual(data["condition_type"], "test")
        self.assertEqual(data["name"], "Test Condition")
        self.assertEqual(data["description"], "Test condition description")
        self.assertEqual(data["param1"], "value1")
        self.assertEqual(data["param2"], "value2")
        
        # Create a condition with None values
        condition = TestCondition({
            "condition_id": "test-condition",
            "condition_type": "test",
            "name": "Test Condition",
            "param1": None
        })
        
        # Convert to dictionary
        data = condition.to_dict()
        
        # Check the dictionary
        self.assertEqual(data["condition_id"], "test-condition")
        self.assertEqual(data["condition_type"], "test")
        self.assertEqual(data["name"], "Test Condition")
        self.assertNotIn("description", data)
        self.assertNotIn("param1", data)
    
    def test_string_representation(self):
        """Test string representation of condition."""
        # Create a condition
        condition = TestCondition({
            "condition_id": "test-condition",
            "condition_type": "test",
            "name": "Test Condition"
        })
        
        # Check string representation
        self.assertEqual(str(condition), "Test Condition (test)")
        self.assertEqual(repr(condition), "TestCondition(condition_id='test-condition', condition_type='test', name='Test Condition')")


class TestCondition(BaseCondition):
    """Test condition implementation."""
    
    def _evaluate(self, context):
        """Evaluate the condition."""
        if self._config.get("raise_exception"):
            raise Exception("Test exception")
        
        return self._config.get("result", False)
    
    def _validate(self):
        """Validate the condition."""
        errors = []
        
        if self._config.get("invalid"):
            errors.append("Invalid parameter")
        
        return errors


if __name__ == "__main__":
    unittest.main()
