"""Tests for the LoopPresenter class."""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.ui.presenters.loop_presenter import LoopPresenter
from src.ui.adapters.loop_adapter import LoopAdapter

class TestLoopPresenter(unittest.TestCase):
    """Test cases for the LoopPresenter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock objects
        self.mock_view = MagicMock()
        self.mock_app = MagicMock()
        self.mock_service = MagicMock(spec=LoopAdapter)
        
        # Create the presenter
        self.presenter = LoopPresenter(
            view=self.mock_view,
            app=self.mock_app,
            service=self.mock_service
        )
        
        # Set up mock data
        self.mock_loop_types = [
            {
                "type": "for_each",
                "name": "For Each",
                "description": "Iterate over a collection of items",
                "parameters": [
                    {"name": "collection_variable", "type": "string", "description": "Name of the variable containing the collection"},
                    {"name": "item_variable", "type": "string", "description": "Name of the variable to store the current item"}
                ]
            },
            {
                "type": "while_loop",
                "name": "While Loop",
                "description": "Execute actions while a condition is true",
                "parameters": [
                    {"name": "condition", "type": "condition", "description": "Condition to evaluate for each iteration"},
                    {"name": "max_iterations", "type": "integer", "description": "Maximum number of iterations (optional)"}
                ]
            }
        ]
        
        self.mock_loop = {
            "id": "test_id",
            "description": "Test loop",
            "type": "for_each",
            "collection_variable": "items",
            "item_variable": "item",
            "actions": []
        }
        
        # Configure mock service
        self.mock_service.get_loop_types.return_value = self.mock_loop_types
        self.mock_service.get_loop_by_id.return_value = self.mock_loop
    
    def test_initialize_view(self):
        """Test initializing the view."""
        # Call the method
        self.presenter.initialize_view()
        
        # Verify the service was called
        self.mock_service.get_loop_types.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_loop_types.assert_called_once_with(self.mock_loop_types)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_load_loop_types(self):
        """Test loading loop types."""
        # Call the method
        self.presenter.load_loop_types()
        
        # Verify the service was called
        self.mock_service.get_loop_types.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_loop_types.assert_called_once_with(self.mock_loop_types)
    
    def test_select_loop_type(self):
        """Test selecting a loop type."""
        # Call the method
        self.presenter.select_loop_type("for_each")
        
        # Verify the view was updated
        self.mock_view.update_parameter_editors.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_select_loop(self):
        """Test selecting a loop."""
        # Call the method
        self.presenter.select_loop("test_id")
        
        # Verify the service was called
        self.mock_service.get_loop_by_id.assert_called_once_with("test_id")
        
        # Verify the view was updated
        self.mock_view.populate_editor.assert_called_once_with(self.mock_loop)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_create_loop(self):
        """Test creating a loop."""
        # Set up mock service
        self.mock_service.create_loop.return_value = self.mock_loop
        
        # Call the method
        loop_data = {
            "type": "for_each",
            "description": "Test loop",
            "collection_variable": "items",
            "item_variable": "item",
            "actions": []
        }
        self.presenter.create_loop(loop_data)
        
        # Verify the service was called
        self.mock_service.create_loop.assert_called_once_with(loop_data)
        
        # Verify the view was updated
        self.mock_view.add_loop_to_list.assert_called_once_with(self.mock_loop)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_update_loop(self):
        """Test updating a loop."""
        # Set up mock service
        self.mock_service.update_loop.return_value = self.mock_loop
        
        # Call the method
        loop_data = {
            "id": "test_id",
            "type": "for_each",
            "description": "Test loop",
            "collection_variable": "items",
            "item_variable": "item",
            "actions": []
        }
        self.presenter.update_loop(loop_data)
        
        # Verify the service was called
        self.mock_service.update_loop.assert_called_once_with(loop_data)
        
        # Verify the view was updated
        self.mock_view.update_loop_in_list.assert_called_once_with(self.mock_loop)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_delete_loop(self):
        """Test deleting a loop."""
        # Set up mock service
        self.mock_service.delete_loop.return_value = True
        
        # Set up mock view
        self.mock_view.ask_yes_no.return_value = True
        
        # Call the method
        self.presenter.delete_loop("test_id")
        
        # Verify the service was called
        self.mock_service.delete_loop.assert_called_once_with("test_id")
        
        # Verify the view was updated
        self.mock_view.remove_loop_from_list.assert_called_once_with("test_id")
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_delete_loop_cancelled(self):
        """Test cancelling loop deletion."""
        # Set up mock view
        self.mock_view.ask_yes_no.return_value = False
        
        # Call the method
        self.presenter.delete_loop("test_id")
        
        # Verify the service was not called
        self.mock_service.delete_loop.assert_not_called()
    
    def test_save_loop_from_editor(self):
        """Test saving a loop from the editor."""
        # Set up mock view
        self.mock_view.get_editor_data.return_value = {
            "id": "test_id",
            "type": "for_each",
            "description": "Test loop",
            "collection_variable": "items",
            "item_variable": "item",
            "actions": []
        }
        
        # Set up mock service
        self.mock_service.update_loop.return_value = self.mock_loop
        
        # Call the method
        self.presenter.save_loop_from_editor()
        
        # Verify the view was called
        self.mock_view.get_editor_data.assert_called_once()
        
        # Verify the service was called
        self.mock_service.update_loop.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_loop_in_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_save_loop_from_editor_new(self):
        """Test saving a new loop from the editor."""
        # Set up mock view
        self.mock_view.get_editor_data.return_value = {
            "id": "",  # Empty ID indicates a new loop
            "type": "for_each",
            "description": "Test loop",
            "collection_variable": "items",
            "item_variable": "item",
            "actions": []
        }
        
        # Set up mock service
        self.mock_service.create_loop.return_value = self.mock_loop
        
        # Call the method
        self.presenter.save_loop_from_editor()
        
        # Verify the view was called
        self.mock_view.get_editor_data.assert_called_once()
        
        # Verify the service was called
        self.mock_service.create_loop.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.add_loop_to_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()

if __name__ == "__main__":
    unittest.main()
