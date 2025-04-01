"""
Tests for the compound condition implementations.

This module contains tests for the compound condition implementations.
"""
import unittest
from unittest.mock import Mock

from src.core.conditions.compound_condition_base import CompoundCondition
from src.core.conditions.compound_conditions import AndCondition, OrCondition, NotCondition
from src.core.conditions.exceptions import ConditionNotFoundError, ConditionEvaluationError


class TestCompoundCondition(unittest.TestCase):
    """Tests for the CompoundCondition class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a compound condition
        self.condition = TestCompoundCondition({
            "condition_id": "test-compound",
            "condition_type": "test-compound",
            "name": "Test Compound Condition"
        })
        
        # Create child conditions
        self.child1 = Mock()
        self.child1.condition_id = "child1"
        self.child1.validate.return_value = []
        self.child1.to_dict.return_value = {"condition_id": "child1"}
        
        self.child2 = Mock()
        self.child2.condition_id = "child2"
        self.child2.validate.return_value = []
        self.child2.to_dict.return_value = {"condition_id": "child2"}
        
        # Add child conditions
        self.condition.add_condition(self.child1)
        self.condition.add_condition(self.child2)
    
    def test_add_condition(self):
        """Test adding a condition."""
        # Create a new child condition
        child3 = Mock()
        child3.condition_id = "child3"
        
        # Add the condition
        self.condition.add_condition(child3)
        
        # Check that the condition was added
        self.assertEqual(self.condition.get_condition("child3"), child3)
    
    def test_remove_condition(self):
        """Test removing a condition."""
        # Remove a condition
        self.condition.remove_condition("child1")
        
        # Check that the condition was removed
        self.assertIsNone(self.condition.get_condition("child1"))
        
        # Try to remove a nonexistent condition
        with self.assertRaises(ConditionNotFoundError):
            self.condition.remove_condition("nonexistent")
    
    def test_get_conditions(self):
        """Test getting all conditions."""
        # Get all conditions
        conditions = self.condition.get_conditions()
        
        # Check the conditions
        self.assertEqual(len(conditions), 2)
        self.assertIn(self.child1, conditions)
        self.assertIn(self.child2, conditions)
    
    def test_get_condition(self):
        """Test getting a condition by ID."""
        # Get a condition
        condition = self.condition.get_condition("child1")
        
        # Check the condition
        self.assertEqual(condition, self.child1)
        
        # Get a nonexistent condition
        condition = self.condition.get_condition("nonexistent")
        
        # Check the condition
        self.assertIsNone(condition)
    
    def test_validate(self):
        """Test validating the compound condition."""
        # Validate the condition
        errors = self.condition.validate()
        
        # Check the errors
        self.assertEqual(errors, [])
        
        # Create a child condition with validation errors
        child3 = Mock()
        child3.condition_id = "child3"
        child3.validate.return_value = ["Error 1", "Error 2"]
        
        # Add the condition
        self.condition.add_condition(child3)
        
        # Validate the condition
        errors = self.condition.validate()
        
        # Check the errors
        self.assertEqual(len(errors), 3)
        self.assertIn("Errors in condition 'child3':", errors)
        self.assertIn("  - Error 1", errors)
        self.assertIn("  - Error 2", errors)
    
    def test_to_dict(self):
        """Test converting the compound condition to a dictionary."""
        # Convert to dictionary
        data = self.condition.to_dict()
        
        # Check the dictionary
        self.assertEqual(data["condition_id"], "test-compound")
        self.assertEqual(data["condition_type"], "test-compound")
        self.assertEqual(data["name"], "Test Compound Condition")
        self.assertEqual(len(data["conditions"]), 2)
        self.assertIn({"condition_id": "child1"}, data["conditions"])
        self.assertIn({"condition_id": "child2"}, data["conditions"])


class TestAndCondition(unittest.TestCase):
    """Tests for the AndCondition class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create an AND condition
        self.condition = AndCondition({
            "condition_id": "test-and",
            "name": "Test AND Condition"
        })
        
        # Create child conditions
        self.child1 = Mock()
        self.child1.condition_id = "child1"
        self.child1.evaluate.return_value = True
        
        self.child2 = Mock()
        self.child2.condition_id = "child2"
        self.child2.evaluate.return_value = True
        
        self.child3 = Mock()
        self.child3.condition_id = "child3"
        self.child3.evaluate.return_value = False
        
        # Create a mock context
        self.context = Mock()
    
    def test_evaluate_all_true(self):
        """Test evaluating the AND condition when all child conditions are true."""
        # Add child conditions
        self.condition.add_condition(self.child1)
        self.condition.add_condition(self.child2)
        
        # Evaluate the condition
        result = self.condition.evaluate(self.context)
        
        # Check the result
        self.assertTrue(result)
        
        # Check that the child conditions were evaluated
        self.child1.evaluate.assert_called_once_with(self.context)
        self.child2.evaluate.assert_called_once_with(self.context)
    
    def test_evaluate_one_false(self):
        """Test evaluating the AND condition when one child condition is false."""
        # Add child conditions
        self.condition.add_condition(self.child1)
        self.condition.add_condition(self.child3)
        
        # Evaluate the condition
        result = self.condition.evaluate(self.context)
        
        # Check the result
        self.assertFalse(result)
        
        # Check that the child conditions were evaluated
        self.child1.evaluate.assert_called_once_with(self.context)
        self.child3.evaluate.assert_called_once_with(self.context)
    
    def test_evaluate_no_conditions(self):
        """Test evaluating the AND condition when there are no child conditions."""
        # Evaluate the condition
        result = self.condition.evaluate(self.context)
        
        # Check the result
        self.assertTrue(result)


class TestOrCondition(unittest.TestCase):
    """Tests for the OrCondition class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create an OR condition
        self.condition = OrCondition({
            "condition_id": "test-or",
            "name": "Test OR Condition"
        })
        
        # Create child conditions
        self.child1 = Mock()
        self.child1.condition_id = "child1"
        self.child1.evaluate.return_value = True
        
        self.child2 = Mock()
        self.child2.condition_id = "child2"
        self.child2.evaluate.return_value = False
        
        self.child3 = Mock()
        self.child3.condition_id = "child3"
        self.child3.evaluate.return_value = False
        
        # Create a mock context
        self.context = Mock()
    
    def test_evaluate_one_true(self):
        """Test evaluating the OR condition when one child condition is true."""
        # Add child conditions
        self.condition.add_condition(self.child1)
        self.condition.add_condition(self.child2)
        
        # Evaluate the condition
        result = self.condition.evaluate(self.context)
        
        # Check the result
        self.assertTrue(result)
        
        # Check that the child conditions were evaluated
        self.child1.evaluate.assert_called_once_with(self.context)
    
    def test_evaluate_all_false(self):
        """Test evaluating the OR condition when all child conditions are false."""
        # Add child conditions
        self.condition.add_condition(self.child2)
        self.condition.add_condition(self.child3)
        
        # Evaluate the condition
        result = self.condition.evaluate(self.context)
        
        # Check the result
        self.assertFalse(result)
        
        # Check that the child conditions were evaluated
        self.child2.evaluate.assert_called_once_with(self.context)
        self.child3.evaluate.assert_called_once_with(self.context)
    
    def test_evaluate_no_conditions(self):
        """Test evaluating the OR condition when there are no child conditions."""
        # Evaluate the condition
        result = self.condition.evaluate(self.context)
        
        # Check the result
        self.assertFalse(result)


class TestNotCondition(unittest.TestCase):
    """Tests for the NotCondition class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a NOT condition
        self.condition = NotCondition({
            "condition_id": "test-not",
            "name": "Test NOT Condition"
        })
        
        # Create child conditions
        self.child1 = Mock()
        self.child1.condition_id = "child1"
        self.child1.evaluate.return_value = True
        self.child1.validate.return_value = []
        self.child1.to_dict.return_value = {"condition_id": "child1"}
        
        self.child2 = Mock()
        self.child2.condition_id = "child2"
        self.child2.evaluate.return_value = False
        self.child2.validate.return_value = []
        self.child2.to_dict.return_value = {"condition_id": "child2"}
        
        # Create a mock context
        self.context = Mock()
    
    def test_evaluate_child_true(self):
        """Test evaluating the NOT condition when the child condition is true."""
        # Set the child condition
        self.condition.condition = self.child1
        
        # Evaluate the condition
        result = self.condition.evaluate(self.context)
        
        # Check the result
        self.assertFalse(result)
        
        # Check that the child condition was evaluated
        self.child1.evaluate.assert_called_once_with(self.context)
    
    def test_evaluate_child_false(self):
        """Test evaluating the NOT condition when the child condition is false."""
        # Set the child condition
        self.condition.condition = self.child2
        
        # Evaluate the condition
        result = self.condition.evaluate(self.context)
        
        # Check the result
        self.assertTrue(result)
        
        # Check that the child condition was evaluated
        self.child2.evaluate.assert_called_once_with(self.context)
    
    def test_evaluate_no_child(self):
        """Test evaluating the NOT condition when there is no child condition."""
        # Evaluate the condition
        with self.assertRaises(ConditionEvaluationError):
            self.condition.evaluate(self.context)
    
    def test_validate(self):
        """Test validating the NOT condition."""
        # Validate the condition without a child
        errors = self.condition.validate()
        
        # Check the errors
        self.assertEqual(len(errors), 1)
        self.assertIn("Child condition is required", errors)
        
        # Set the child condition
        self.condition.condition = self.child1
        
        # Validate the condition
        errors = self.condition.validate()
        
        # Check the errors
        self.assertEqual(errors, [])
        
        # Create a child condition with validation errors
        child3 = Mock()
        child3.condition_id = "child3"
        child3.validate.return_value = ["Error 1", "Error 2"]
        
        # Set the child condition
        self.condition.condition = child3
        
        # Validate the condition
        errors = self.condition.validate()
        
        # Check the errors
        self.assertEqual(len(errors), 3)
        self.assertIn("Errors in child condition:", errors)
        self.assertIn("  - Error 1", errors)
        self.assertIn("  - Error 2", errors)
    
    def test_to_dict(self):
        """Test converting the NOT condition to a dictionary."""
        # Set the child condition
        self.condition.condition = self.child1
        
        # Convert to dictionary
        data = self.condition.to_dict()
        
        # Check the dictionary
        self.assertEqual(data["condition_id"], "test-not")
        self.assertEqual(data["condition_type"], "not")
        self.assertEqual(data["name"], "Test NOT Condition")
        self.assertEqual(data["condition"], {"condition_id": "child1"})
        
        # Create a NOT condition without a child
        condition = NotCondition({
            "condition_id": "test-not",
            "name": "Test NOT Condition"
        })
        
        # Convert to dictionary
        data = condition.to_dict()
        
        # Check the dictionary
        self.assertEqual(data["condition_id"], "test-not")
        self.assertEqual(data["condition_type"], "not")
        self.assertEqual(data["name"], "Test NOT Condition")
        self.assertNotIn("condition", data)


class TestCompoundCondition(CompoundCondition):
    """Test compound condition implementation."""
    
    def _evaluate(self, context):
        """Evaluate the condition."""
        return True


if __name__ == "__main__":
    unittest.main()
