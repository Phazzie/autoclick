"""Tests for the LoopAdapter class."""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any, List

from src.core.actions.for_each_action import ForEachAction
from src.core.actions.while_loop_action import WhileLoopAction
from src.core.actions.action_factory import ActionFactory
from src.core.conditions.condition_factory import ConditionFactory
from src.ui.adapters.loop_adapter import LoopAdapter

class TestLoopAdapter(unittest.TestCase):
    """Test cases for the LoopAdapter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock action factory and condition factory
        self.mock_action_factory = MagicMock(spec=ActionFactory)
        self.mock_condition_factory = MagicMock(spec=ConditionFactory)
        
        # Create the adapter
        self.adapter = LoopAdapter(self.mock_action_factory, self.mock_condition_factory)
    
    def test_get_loop_types(self):
        """Test getting loop types."""
        # Call the method
        result = self.adapter.get_loop_types()
        
        # Verify the result
        self.assertEqual(len(result), 2)
        self.assertIn("for_each", [item["type"] for item in result])
        self.assertIn("while_loop", [item["type"] for item in result])
    
    def test_create_for_each_loop(self):
        """Test creating a for-each loop."""
        # Set up mock action factory
        mock_action = MagicMock(spec=ForEachAction)
        mock_action.id = "test_id"
        mock_action.description = "Test loop"
        mock_action.type = "for_each"
        self.mock_action_factory.create_action.return_value = mock_action
        
        # Call the method
        loop_data = {
            "type": "for_each",
            "description": "Test loop",
            "collection_variable": "items",
            "item_variable": "item",
            "actions": []
        }
        result = self.adapter.create_loop(loop_data)
        
        # Verify the result
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["description"], "Test loop")
        self.assertEqual(result["type"], "for_each")
        
        # Verify the action factory was called
        self.mock_action_factory.create_action.assert_called_once()
    
    def test_create_while_loop(self):
        """Test creating a while loop."""
        # Set up mock action factory
        mock_action = MagicMock(spec=WhileLoopAction)
        mock_action.id = "test_id"
        mock_action.description = "Test loop"
        mock_action.type = "while_loop"
        self.mock_action_factory.create_action.return_value = mock_action
        
        # Set up mock condition factory
        mock_condition = MagicMock()
        self.mock_condition_factory.create_condition.return_value = mock_condition
        
        # Call the method
        loop_data = {
            "type": "while_loop",
            "description": "Test loop",
            "condition": {
                "type": "comparison",
                "left_value": "x",
                "operator": "EQUAL",
                "right_value": "y"
            },
            "actions": [],
            "max_iterations": 10
        }
        result = self.adapter.create_loop(loop_data)
        
        # Verify the result
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["description"], "Test loop")
        self.assertEqual(result["type"], "while_loop")
        
        # Verify the action factory was called
        self.mock_action_factory.create_action.assert_called_once()
        
        # Verify the condition factory was called
        self.mock_condition_factory.create_condition.assert_called_once()
    
    def test_get_loop_by_id(self):
        """Test getting a loop by ID."""
        # Set up mock action factory
        mock_action = MagicMock()
        mock_action.id = "test_id"
        mock_action.description = "Test loop"
        mock_action.type = "for_each"
        mock_action.to_dict.return_value = {
            "id": "test_id",
            "description": "Test loop",
            "type": "for_each",
            "collection_variable": "items",
            "item_variable": "item",
            "actions": []
        }
        self.mock_action_factory.get_action_by_id.return_value = mock_action
        
        # Call the method
        result = self.adapter.get_loop_by_id("test_id")
        
        # Verify the result
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["description"], "Test loop")
        self.assertEqual(result["type"], "for_each")
        
        # Verify the action factory was called
        self.mock_action_factory.get_action_by_id.assert_called_once_with("test_id")
    
    def test_update_loop(self):
        """Test updating a loop."""
        # Set up mock action factory
        mock_action = MagicMock()
        mock_action.id = "test_id"
        mock_action.description = "Updated loop"
        mock_action.type = "for_each"
        mock_action.to_dict.return_value = {
            "id": "test_id",
            "description": "Updated loop",
            "type": "for_each",
            "collection_variable": "new_items",
            "item_variable": "new_item",
            "actions": []
        }
        self.mock_action_factory.update_action.return_value = mock_action
        
        # Call the method
        loop_data = {
            "id": "test_id",
            "description": "Updated loop",
            "type": "for_each",
            "collection_variable": "new_items",
            "item_variable": "new_item",
            "actions": []
        }
        result = self.adapter.update_loop(loop_data)
        
        # Verify the result
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["description"], "Updated loop")
        self.assertEqual(result["type"], "for_each")
        
        # Verify the action factory was called
        self.mock_action_factory.update_action.assert_called_once()
    
    def test_delete_loop(self):
        """Test deleting a loop."""
        # Set up mock action factory
        self.mock_action_factory.delete_action.return_value = True
        
        # Call the method
        result = self.adapter.delete_loop("test_id")
        
        # Verify the result
        self.assertTrue(result)
        
        # Verify the action factory was called
        self.mock_action_factory.delete_action.assert_called_once_with("test_id")

if __name__ == "__main__":
    unittest.main()
