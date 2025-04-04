"""Tests for the ActionAdapter class."""
import unittest
from unittest.mock import MagicMock, patch

from src.core.actions.action_factory import ActionFactory
from src.domain.actions.interfaces import IActionService
from src.ui.adapters.impl.action_adapter import ActionAdapter


class TestActionAdapter(unittest.TestCase):
    """Test cases for the ActionAdapter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock service for clean architecture tests
        self.mock_service = MagicMock(spec=IActionService)
        
        # Create mock action factory for legacy tests
        self.mock_action_factory = MagicMock(spec=ActionFactory)
        
        # Create adapters for both modes
        self.service_adapter = ActionAdapter(action_service=self.mock_service)
        self.legacy_adapter = ActionAdapter(action_factory=self.mock_action_factory)
    
    def test_get_action_types_service_mode(self):
        """Test getting action types in service mode."""
        # Arrange
        expected_types = [
            {
                "id": "click",
                "name": "Click",
                "description": "Click at a specific position"
            }
        ]
        self.mock_service.get_action_types.return_value = expected_types
        
        # Act
        result = self.service_adapter.get_action_types()
        
        # Assert
        self.assertEqual(result, expected_types)
        self.mock_service.get_action_types.assert_called_once()
    
    def test_get_action_types_legacy_mode(self):
        """Test getting action types in legacy mode."""
        # Arrange
        self.mock_action_factory.get_action_types.return_value = ["click", "keyboard"]
        
        # Act
        result = self.legacy_adapter.get_action_types()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "click")
        self.assertEqual(result[1]["id"], "keyboard")
        self.mock_action_factory.get_action_types.assert_called_once()
    
    def test_get_action_schema_service_mode(self):
        """Test getting an action schema in service mode."""
        # Arrange
        expected_schema = {
            "type": "object",
            "properties": {
                "x": {"type": "integer"},
                "y": {"type": "integer"}
            }
        }
        self.mock_service.get_action_schema.return_value = expected_schema
        
        # Act
        result = self.service_adapter.get_action_schema("click")
        
        # Assert
        self.assertEqual(result, expected_schema)
        self.mock_service.get_action_schema.assert_called_once_with("click")
    
    def test_get_action_schema_legacy_mode(self):
        """Test getting an action schema in legacy mode."""
        # Act
        result = self.legacy_adapter.get_action_schema("click")
        
        # Assert
        self.assertEqual(result["type"], "object")
        self.assertIn("x", result["properties"])
        self.assertIn("y", result["properties"])
    
    def test_get_all_actions_service_mode(self):
        """Test getting all actions in service mode."""
        # Arrange
        expected_actions = [
            {
                "id": "action1",
                "type": "click",
                "x": 100,
                "y": 200
            }
        ]
        self.mock_service.get_all_actions.return_value = expected_actions
        
        # Act
        result = self.service_adapter.get_all_actions()
        
        # Assert
        self.assertEqual(result, expected_actions)
        self.mock_service.get_all_actions.assert_called_once()
    
    def test_get_all_actions_legacy_mode(self):
        """Test getting all actions in legacy mode."""
        # Act
        result = self.legacy_adapter.get_all_actions()
        
        # Assert
        self.assertEqual(result, [])
    
    def test_get_action_service_mode(self):
        """Test getting an action by ID in service mode."""
        # Arrange
        expected_action = {
            "id": "action1",
            "type": "click",
            "x": 100,
            "y": 200
        }
        self.mock_service.get_action.return_value = expected_action
        
        # Act
        result = self.service_adapter.get_action("action1")
        
        # Assert
        self.assertEqual(result, expected_action)
        self.mock_service.get_action.assert_called_once_with("action1")
    
    def test_get_action_legacy_mode(self):
        """Test getting an action by ID in legacy mode."""
        # Act
        result = self.legacy_adapter.get_action("action1")
        
        # Assert
        self.assertIsNone(result)
    
    def test_create_action_service_mode(self):
        """Test creating an action in service mode."""
        # Arrange
        action_type = "click"
        action_data = {
            "x": 100,
            "y": 200
        }
        
        expected_action = {
            "id": "action1",
            "type": "click",
            "x": 100,
            "y": 200
        }
        
        # Mock the validate_action method to return empty list (no errors)
        self.mock_service.validate_action.return_value = []
        self.mock_service.create_action.return_value = expected_action
        
        # Act
        result = self.service_adapter.create_action(action_type, action_data)
        
        # Assert
        self.assertEqual(result, expected_action)
        self.mock_service.validate_action.assert_called_once_with(action_type, action_data)
        self.mock_service.create_action.assert_called_once_with(action_type, action_data)
    
    def test_create_action_legacy_mode(self):
        """Test creating an action in legacy mode."""
        # Arrange
        action_type = "click"
        action_data = {
            "x": 100,
            "y": 200
        }
        
        mock_action = MagicMock()
        mock_action.to_dict.return_value = {
            "id": "action1",
            "type": "click",
            "x": 100,
            "y": 200
        }
        
        self.mock_action_factory.create_from_dict.return_value = mock_action
        
        # Act
        result = self.legacy_adapter.create_action(action_type, action_data)
        
        # Assert
        self.assertEqual(result["id"], "action1")
        self.assertEqual(result["type"], "click")
        self.mock_action_factory.create_from_dict.assert_called_once()
    
    def test_update_action_service_mode(self):
        """Test updating an action in service mode."""
        # Arrange
        action_id = "action1"
        action_data = {
            "x": 150,
            "y": 250
        }
        
        expected_action = {
            "id": "action1",
            "type": "click",
            "x": 150,
            "y": 250
        }
        
        self.mock_service.update_action.return_value = expected_action
        
        # Act
        result = self.service_adapter.update_action(action_id, action_data)
        
        # Assert
        self.assertEqual(result, expected_action)
        self.mock_service.update_action.assert_called_once_with(action_id, action_data)
    
    def test_update_action_legacy_mode(self):
        """Test updating an action in legacy mode."""
        # Arrange
        action_id = "action1"
        action_data = {
            "x": 150,
            "y": 250
        }
        
        # Act/Assert
        with self.assertRaises(ValueError):
            self.legacy_adapter.update_action(action_id, action_data)
    
    def test_delete_action_service_mode(self):
        """Test deleting an action in service mode."""
        # Arrange
        action_id = "action1"
        self.mock_service.delete_action.return_value = True
        
        # Act
        result = self.service_adapter.delete_action(action_id)
        
        # Assert
        self.assertTrue(result)
        self.mock_service.delete_action.assert_called_once_with(action_id)
    
    def test_delete_action_legacy_mode(self):
        """Test deleting an action in legacy mode."""
        # Arrange
        action_id = "action1"
        
        # Act
        result = self.legacy_adapter.delete_action(action_id)
        
        # Assert
        self.assertFalse(result)
    
    def test_validate_action_service_mode(self):
        """Test validating an action in service mode."""
        # Arrange
        action_type = "click"
        action_data = {
            "x": 100,
            "y": 200
        }
        
        self.mock_service.validate_action.return_value = []
        
        # Act
        result = self.service_adapter.validate_action(action_type, action_data)
        
        # Assert
        self.assertEqual(result, [])
        self.mock_service.validate_action.assert_called_once_with(action_type, action_data)
    
    def test_validate_action_legacy_mode(self):
        """Test validating an action in legacy mode."""
        # Arrange
        action_type = "click"
        action_data = {
            "x": 100,
            "y": 200
        }
        
        # Act
        result = self.legacy_adapter.validate_action(action_type, action_data)
        
        # Assert
        self.assertEqual(result, [])
    
    def test_execute_action_service_mode(self):
        """Test executing an action in service mode."""
        # Arrange
        action_id = "action1"
        context = {"variable1": "value1"}
        
        expected_result = {
            "success": True,
            "result": "Action executed"
        }
        
        self.mock_service.execute_action.return_value = expected_result
        
        # Act
        result = self.service_adapter.execute_action(action_id, context)
        
        # Assert
        self.assertEqual(result, expected_result)
        self.mock_service.execute_action.assert_called_once_with(action_id, context)
    
    def test_execute_action_legacy_mode(self):
        """Test executing an action in legacy mode."""
        # Arrange
        action_id = "action1"
        context = {"variable1": "value1"}
        
        # Act/Assert
        with self.assertRaises(ValueError):
            self.legacy_adapter.execute_action(action_id, context)


if __name__ == "__main__":
    unittest.main()
