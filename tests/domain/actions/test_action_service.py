"""Tests for the ActionService class."""
import unittest
from unittest.mock import MagicMock, patch

from src.core.actions.action_factory import ActionFactory
from src.domain.actions.impl.action_service import ActionService
from src.domain.exceptions.domain_exceptions import DomainException


class TestActionService(unittest.TestCase):
    """Test cases for the ActionService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_action_factory = MagicMock(spec=ActionFactory)
        self.service = ActionService(self.mock_action_factory)
    
    def test_get_action_types(self):
        """Test getting action types."""
        # Arrange
        self.mock_action_factory.get_action_types.return_value = ["click", "keyboard", "wait"]
        
        # Act
        result = self.service.get_action_types()
        
        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["id"], "click")
        self.assertEqual(result[1]["id"], "keyboard")
        self.assertEqual(result[2]["id"], "wait")
        self.mock_action_factory.get_action_types.assert_called_once()
    
    def test_get_action_schema_valid(self):
        """Test getting a valid action schema."""
        # Act
        result = self.service.get_action_schema("click")
        
        # Assert
        self.assertEqual(result["type"], "object")
        self.assertIn("x", result["properties"])
        self.assertIn("y", result["properties"])
    
    def test_get_action_schema_invalid(self):
        """Test getting an invalid action schema."""
        # Act/Assert
        with self.assertRaises(DomainException):
            self.service.get_action_schema("invalid_type")
    
    def test_get_all_actions_empty(self):
        """Test getting all actions when none exist."""
        # Act
        result = self.service.get_all_actions()
        
        # Assert
        self.assertEqual(result, [])
    
    def test_get_action_not_found(self):
        """Test getting an action that doesn't exist."""
        # Act
        result = self.service.get_action("non_existent_id")
        
        # Assert
        self.assertIsNone(result)
    
    def test_create_action(self):
        """Test creating an action."""
        # Arrange
        action_type = "click"
        action_data = {"x": 100, "y": 200}
        
        mock_action = MagicMock()
        mock_action.to_dict.return_value = {
            "id": "action1",
            "type": "click",
            "x": 100,
            "y": 200
        }
        
        self.mock_action_factory.create_from_dict.return_value = mock_action
        
        # Act
        result = self.service.create_action(action_type, action_data)
        
        # Assert
        self.assertEqual(result["id"], "action1")
        self.assertEqual(result["type"], "click")
        self.assertEqual(result["x"], 100)
        self.assertEqual(result["y"], 200)
        self.mock_action_factory.create_from_dict.assert_called_once()
    
    def test_create_action_invalid_data(self):
        """Test creating an action with invalid data."""
        # Arrange
        action_type = "click"
        action_data = {"y": 200}  # Missing x coordinate
        
        # Act/Assert
        with self.assertRaises(DomainException):
            self.service.create_action(action_type, action_data)
    
    def test_update_action(self):
        """Test updating an action."""
        # Arrange
        action_id = "action1"
        action_data = {"x": 150, "y": 250}
        
        # Create an action first
        mock_action = MagicMock()
        mock_action.to_dict.return_value = {
            "id": "action1",
            "type": "click",
            "x": 100,
            "y": 200
        }
        
        self.mock_action_factory.create_from_dict.return_value = mock_action
        self.service.create_action("click", {"x": 100, "y": 200})
        
        # Update the mock for the update operation
        mock_updated_action = MagicMock()
        mock_updated_action.to_dict.return_value = {
            "id": "action1",
            "type": "click",
            "x": 150,
            "y": 250
        }
        
        self.mock_action_factory.create_from_dict.return_value = mock_updated_action
        
        # Act
        result = self.service.update_action(action_id, action_data)
        
        # Assert
        self.assertEqual(result["id"], "action1")
        self.assertEqual(result["type"], "click")
        self.assertEqual(result["x"], 150)
        self.assertEqual(result["y"], 250)
    
    def test_update_action_not_found(self):
        """Test updating an action that doesn't exist."""
        # Arrange
        action_id = "non_existent_id"
        action_data = {"x": 150, "y": 250}
        
        # Act
        result = self.service.update_action(action_id, action_data)
        
        # Assert
        self.assertIsNone(result)
    
    def test_delete_action(self):
        """Test deleting an action."""
        # Arrange
        action_id = "action1"
        
        # Create an action first
        mock_action = MagicMock()
        mock_action.to_dict.return_value = {
            "id": "action1",
            "type": "click",
            "x": 100,
            "y": 200
        }
        
        self.mock_action_factory.create_from_dict.return_value = mock_action
        self.service.create_action("click", {"x": 100, "y": 200})
        
        # Act
        result = self.service.delete_action(action_id)
        
        # Assert
        self.assertTrue(result)
        self.assertIsNone(self.service.get_action(action_id))
    
    def test_delete_action_not_found(self):
        """Test deleting an action that doesn't exist."""
        # Arrange
        action_id = "non_existent_id"
        
        # Act
        result = self.service.delete_action(action_id)
        
        # Assert
        self.assertFalse(result)
    
    def test_validate_action_valid(self):
        """Test validating a valid action."""
        # Arrange
        action_type = "click"
        action_data = {"x": 100, "y": 200}
        
        # Act
        result = self.service.validate_action(action_type, action_data)
        
        # Assert
        self.assertEqual(result, [])
    
    def test_validate_action_invalid(self):
        """Test validating an invalid action."""
        # Arrange
        action_type = "click"
        action_data = {"y": 200}  # Missing x coordinate
        
        # Act
        result = self.service.validate_action(action_type, action_data)
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertIn("X coordinate is required", result)
    
    def test_execute_action(self):
        """Test executing an action."""
        # Arrange
        action_id = "action1"
        context = {"variable1": "value1"}
        
        # Create an action first
        mock_action = MagicMock()
        mock_action.to_dict.return_value = {
            "id": "action1",
            "type": "click",
            "x": 100,
            "y": 200
        }
        mock_action.execute.return_value = "Action executed"
        
        self.mock_action_factory.create_from_dict.return_value = mock_action
        self.service.create_action("click", {"x": 100, "y": 200})
        
        # Act
        result = self.service.execute_action(action_id, context)
        
        # Assert
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], "Action executed")
        mock_action.execute.assert_called_once_with(context)
    
    def test_execute_action_not_found(self):
        """Test executing an action that doesn't exist."""
        # Arrange
        action_id = "non_existent_id"
        context = {"variable1": "value1"}
        
        # Act/Assert
        with self.assertRaises(DomainException):
            self.service.execute_action(action_id, context)


if __name__ == "__main__":
    unittest.main()
