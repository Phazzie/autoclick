"""Tests for the ConditionAdapter class."""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.core.conditions.condition_factory import ConditionFactory
from src.core.conditions.comparison_condition import ComparisonCondition, ComparisonOperator
from src.core.conditions.element_exists_condition import ElementExistsCondition
from src.core.conditions.text_contains_condition import TextContainsCondition
from src.core.conditions.composite_conditions import AndCondition, OrCondition, NotCondition
from src.ui.adapters.condition_adapter import ConditionAdapter

class TestConditionAdapter(unittest.TestCase):
    """Test cases for the ConditionAdapter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock condition factory
        self.mock_factory = MagicMock(spec=ConditionFactory)
        
        # Create the adapter
        self.adapter = ConditionAdapter(self.mock_factory)
    
    def test_get_condition_types(self):
        """Test getting condition types."""
        # Set up mock factory
        self.mock_factory.get_registered_condition_types.return_value = [
            "comparison", "element_exists", "text_contains", "and", "or", "not"
        ]
        
        # Call the method
        result = self.adapter.get_condition_types()
        
        # Verify the result
        self.assertEqual(len(result), 6)
        self.assertIn("comparison", [item["type"] for item in result])
        self.assertIn("element_exists", [item["type"] for item in result])
        self.assertIn("text_contains", [item["type"] for item in result])
        self.assertIn("and", [item["type"] for item in result])
        self.assertIn("or", [item["type"] for item in result])
        self.assertIn("not", [item["type"] for item in result])
    
    def test_create_comparison_condition(self):
        """Test creating a comparison condition."""
        # Set up mock factory
        mock_condition = MagicMock(spec=ComparisonCondition)
        mock_condition.id = "test_id"
        mock_condition.description = "Test condition"
        mock_condition.type = "comparison"
        self.mock_factory.create_condition.return_value = mock_condition
        
        # Call the method
        condition_data = {
            "type": "comparison",
            "left_value": "x",
            "operator": "EQUAL",
            "right_value": "y"
        }
        result = self.adapter.create_condition(condition_data)
        
        # Verify the result
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["description"], "Test condition")
        self.assertEqual(result["type"], "comparison")
        
        # Verify the factory was called
        self.mock_factory.create_condition.assert_called_once_with(condition_data)
    
    def test_create_element_exists_condition(self):
        """Test creating an element exists condition."""
        # Set up mock factory
        mock_condition = MagicMock(spec=ElementExistsCondition)
        mock_condition.id = "test_id"
        mock_condition.description = "Test condition"
        mock_condition.type = "element_exists"
        self.mock_factory.create_condition.return_value = mock_condition
        
        # Call the method
        condition_data = {
            "type": "element_exists",
            "selector": "#test"
        }
        result = self.adapter.create_condition(condition_data)
        
        # Verify the result
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["description"], "Test condition")
        self.assertEqual(result["type"], "element_exists")
        
        # Verify the factory was called
        self.mock_factory.create_condition.assert_called_once_with(condition_data)
    
    def test_create_text_contains_condition(self):
        """Test creating a text contains condition."""
        # Set up mock factory
        mock_condition = MagicMock(spec=TextContainsCondition)
        mock_condition.id = "test_id"
        mock_condition.description = "Test condition"
        mock_condition.type = "text_contains"
        self.mock_factory.create_condition.return_value = mock_condition
        
        # Call the method
        condition_data = {
            "type": "text_contains",
            "selector": "#test",
            "text": "test text",
            "case_sensitive": False
        }
        result = self.adapter.create_condition(condition_data)
        
        # Verify the result
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["description"], "Test condition")
        self.assertEqual(result["type"], "text_contains")
        
        # Verify the factory was called
        self.mock_factory.create_condition.assert_called_once_with(condition_data)
    
    def test_create_composite_condition(self):
        """Test creating a composite condition."""
        # Set up mock factory
        mock_condition = MagicMock(spec=AndCondition)
        mock_condition.id = "test_id"
        mock_condition.description = "Test condition"
        mock_condition.type = "and"
        self.mock_factory.create_condition.return_value = mock_condition
        
        # Call the method
        condition_data = {
            "type": "and",
            "conditions": [
                {
                    "type": "comparison",
                    "left_value": "x",
                    "operator": "EQUAL",
                    "right_value": "y"
                },
                {
                    "type": "element_exists",
                    "selector": "#test"
                }
            ]
        }
        result = self.adapter.create_condition(condition_data)
        
        # Verify the result
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["description"], "Test condition")
        self.assertEqual(result["type"], "and")
        
        # Verify the factory was called
        self.mock_factory.create_condition.assert_called_once_with(condition_data)
    
    def test_get_condition_by_id(self):
        """Test getting a condition by ID."""
        # Set up mock factory
        mock_condition = MagicMock()
        mock_condition.id = "test_id"
        mock_condition.description = "Test condition"
        mock_condition.type = "comparison"
        mock_condition.to_dict.return_value = {
            "id": "test_id",
            "description": "Test condition",
            "type": "comparison",
            "left_value": "x",
            "operator": "EQUAL",
            "right_value": "y"
        }
        self.mock_factory.get_condition_by_id.return_value = mock_condition
        
        # Call the method
        result = self.adapter.get_condition_by_id("test_id")
        
        # Verify the result
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["description"], "Test condition")
        self.assertEqual(result["type"], "comparison")
        self.assertEqual(result["left_value"], "x")
        self.assertEqual(result["operator"], "EQUAL")
        self.assertEqual(result["right_value"], "y")
        
        # Verify the factory was called
        self.mock_factory.get_condition_by_id.assert_called_once_with("test_id")
    
    def test_update_condition(self):
        """Test updating a condition."""
        # Set up mock factory
        mock_condition = MagicMock()
        mock_condition.id = "test_id"
        mock_condition.description = "Updated condition"
        mock_condition.type = "comparison"
        mock_condition.to_dict.return_value = {
            "id": "test_id",
            "description": "Updated condition",
            "type": "comparison",
            "left_value": "a",
            "operator": "EQUAL",
            "right_value": "b"
        }
        self.mock_factory.update_condition.return_value = mock_condition
        
        # Call the method
        condition_data = {
            "id": "test_id",
            "description": "Updated condition",
            "type": "comparison",
            "left_value": "a",
            "operator": "EQUAL",
            "right_value": "b"
        }
        result = self.adapter.update_condition(condition_data)
        
        # Verify the result
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["description"], "Updated condition")
        self.assertEqual(result["type"], "comparison")
        self.assertEqual(result["left_value"], "a")
        self.assertEqual(result["operator"], "EQUAL")
        self.assertEqual(result["right_value"], "b")
        
        # Verify the factory was called
        self.mock_factory.update_condition.assert_called_once_with(condition_data)
    
    def test_delete_condition(self):
        """Test deleting a condition."""
        # Set up mock factory
        self.mock_factory.delete_condition.return_value = True
        
        # Call the method
        result = self.adapter.delete_condition("test_id")
        
        # Verify the result
        self.assertTrue(result)
        
        # Verify the factory was called
        self.mock_factory.delete_condition.assert_called_once_with("test_id")
    
    def test_evaluate_condition(self):
        """Test evaluating a condition."""
        # Set up mock factory
        mock_condition = MagicMock()
        mock_condition.evaluate.return_value.success = True
        mock_condition.evaluate.return_value.value = True
        mock_condition.evaluate.return_value.message = "Condition evaluated successfully"
        self.mock_factory.get_condition_by_id.return_value = mock_condition
        
        # Call the method
        context = {"variable1": "value1"}
        result = self.adapter.evaluate_condition("test_id", context)
        
        # Verify the result
        self.assertTrue(result["success"])
        self.assertTrue(result["value"])
        self.assertEqual(result["message"], "Condition evaluated successfully")
        
        # Verify the factory was called
        self.mock_factory.get_condition_by_id.assert_called_once_with("test_id")
        mock_condition.evaluate.assert_called_once_with(context)

if __name__ == "__main__":
    unittest.main()
