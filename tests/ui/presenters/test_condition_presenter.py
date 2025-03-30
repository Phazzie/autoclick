"""Tests for the ConditionPresenter class."""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.ui.presenters.condition_presenter import ConditionPresenter
from src.ui.adapters.condition_adapter import ConditionAdapter

class TestConditionPresenter(unittest.TestCase):
    """Test cases for the ConditionPresenter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock objects
        self.mock_view = MagicMock()
        self.mock_app = MagicMock()
        self.mock_service = MagicMock(spec=ConditionAdapter)
        
        # Create the presenter
        self.presenter = ConditionPresenter(
            view=self.mock_view,
            app=self.mock_app,
            service=self.mock_service
        )
        
        # Set up mock data
        self.mock_condition_types = [
            {
                "type": "comparison",
                "name": "Comparison",
                "description": "Compare two values",
                "category": "Basic",
                "parameters": [
                    {"name": "left_value", "type": "string", "description": "Left value or variable name"},
                    {"name": "operator", "type": "enum", "description": "Comparison operator", 
                     "options": ["EQUAL", "NOT_EQUAL", "GREATER_THAN", "GREATER_THAN_OR_EQUAL", 
                                "LESS_THAN", "LESS_THAN_OR_EQUAL", "CONTAINS", "NOT_CONTAINS", 
                                "STARTS_WITH", "ENDS_WITH", "MATCHES_REGEX"]},
                    {"name": "right_value", "type": "string", "description": "Right value or variable name"}
                ]
            },
            {
                "type": "element_exists",
                "name": "Element Exists",
                "description": "Check if an element exists in the DOM",
                "category": "Web",
                "parameters": [
                    {"name": "selector", "type": "string", "description": "CSS selector for the element"}
                ]
            }
        ]
        
        self.mock_condition = {
            "id": "test_id",
            "description": "Test condition",
            "type": "comparison",
            "left_value": "x",
            "operator": "EQUAL",
            "right_value": "y"
        }
        
        # Configure mock service
        self.mock_service.get_condition_types.return_value = self.mock_condition_types
        self.mock_service.get_condition_by_id.return_value = self.mock_condition
    
    def test_initialize_view(self):
        """Test initializing the view."""
        # Call the method
        self.presenter.initialize_view()
        
        # Verify the service was called
        self.mock_service.get_condition_types.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_condition_types.assert_called_once_with(self.mock_condition_types)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_load_condition_types(self):
        """Test loading condition types."""
        # Call the method
        self.presenter.load_condition_types()
        
        # Verify the service was called
        self.mock_service.get_condition_types.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_condition_types.assert_called_once_with(self.mock_condition_types)
    
    def test_select_condition_type(self):
        """Test selecting a condition type."""
        # Call the method
        self.presenter.select_condition_type("comparison")
        
        # Verify the view was updated
        self.mock_view.update_parameter_editors.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_select_condition(self):
        """Test selecting a condition."""
        # Call the method
        self.presenter.select_condition("test_id")
        
        # Verify the service was called
        self.mock_service.get_condition_by_id.assert_called_once_with("test_id")
        
        # Verify the view was updated
        self.mock_view.populate_editor.assert_called_once_with(self.mock_condition)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_create_condition(self):
        """Test creating a condition."""
        # Set up mock service
        self.mock_service.create_condition.return_value = self.mock_condition
        
        # Call the method
        condition_data = {
            "type": "comparison",
            "left_value": "x",
            "operator": "EQUAL",
            "right_value": "y"
        }
        self.presenter.create_condition(condition_data)
        
        # Verify the service was called
        self.mock_service.create_condition.assert_called_once_with(condition_data)
        
        # Verify the view was updated
        self.mock_view.add_condition_to_list.assert_called_once_with(self.mock_condition)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_update_condition(self):
        """Test updating a condition."""
        # Set up mock service
        self.mock_service.update_condition.return_value = self.mock_condition
        
        # Call the method
        condition_data = {
            "id": "test_id",
            "type": "comparison",
            "left_value": "x",
            "operator": "EQUAL",
            "right_value": "y"
        }
        self.presenter.update_condition(condition_data)
        
        # Verify the service was called
        self.mock_service.update_condition.assert_called_once_with(condition_data)
        
        # Verify the view was updated
        self.mock_view.update_condition_in_list.assert_called_once_with(self.mock_condition)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_delete_condition(self):
        """Test deleting a condition."""
        # Set up mock service
        self.mock_service.delete_condition.return_value = True
        
        # Set up mock view
        self.mock_view.ask_yes_no.return_value = True
        
        # Call the method
        self.presenter.delete_condition("test_id")
        
        # Verify the service was called
        self.mock_service.delete_condition.assert_called_once_with("test_id")
        
        # Verify the view was updated
        self.mock_view.remove_condition_from_list.assert_called_once_with("test_id")
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_delete_condition_cancelled(self):
        """Test cancelling condition deletion."""
        # Set up mock view
        self.mock_view.ask_yes_no.return_value = False
        
        # Call the method
        self.presenter.delete_condition("test_id")
        
        # Verify the service was not called
        self.mock_service.delete_condition.assert_not_called()
    
    def test_test_condition(self):
        """Test testing a condition."""
        # Set up mock service
        self.mock_service.evaluate_condition.return_value = {
            "success": True,
            "value": True,
            "message": "Condition evaluated successfully"
        }
        
        # Call the method
        context = {"variable1": "value1"}
        self.presenter.test_condition("test_id", context)
        
        # Verify the service was called
        self.mock_service.evaluate_condition.assert_called_once_with("test_id", context)
        
        # Verify the view was updated
        self.mock_view.display_test_result.assert_called_once_with(
            True, "Condition evaluated successfully"
        )
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_save_condition_from_editor(self):
        """Test saving a condition from the editor."""
        # Set up mock view
        self.mock_view.get_editor_data.return_value = {
            "id": "test_id",
            "type": "comparison",
            "left_value": "x",
            "operator": "EQUAL",
            "right_value": "y"
        }
        
        # Set up mock service
        self.mock_service.update_condition.return_value = self.mock_condition
        
        # Call the method
        self.presenter.save_condition_from_editor()
        
        # Verify the view was called
        self.mock_view.get_editor_data.assert_called_once()
        
        # Verify the service was called
        self.mock_service.update_condition.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_condition_in_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_save_condition_from_editor_new(self):
        """Test saving a new condition from the editor."""
        # Set up mock view
        self.mock_view.get_editor_data.return_value = {
            "id": "",  # Empty ID indicates a new condition
            "type": "comparison",
            "left_value": "x",
            "operator": "EQUAL",
            "right_value": "y"
        }
        
        # Set up mock service
        self.mock_service.create_condition.return_value = self.mock_condition
        
        # Call the method
        self.presenter.save_condition_from_editor()
        
        # Verify the view was called
        self.mock_view.get_editor_data.assert_called_once()
        
        # Verify the service was called
        self.mock_service.create_condition.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.add_condition_to_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()

if __name__ == "__main__":
    unittest.main()
