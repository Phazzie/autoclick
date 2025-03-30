"""Tests for the ErrorPresenter class."""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.ui.presenters.error_presenter import ErrorPresenter
from src.ui.adapters.error_adapter import ErrorAdapter
from src.core.models import ErrorConfig

class TestErrorPresenter(unittest.TestCase):
    """Test cases for the ErrorPresenter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock objects
        self.mock_view = MagicMock()
        self.mock_app = MagicMock()
        self.mock_service = MagicMock(spec=ErrorAdapter)
        
        # Create the presenter
        self.presenter = ErrorPresenter(
            view=self.mock_view,
            app=self.mock_app,
            service=self.mock_service
        )
        
        # Set up mock data
        self.mock_error_configs = [
            ErrorConfig(error_type="connection.timeout", severity="Warning", action="Retry"),
            ErrorConfig(error_type="connection.failed", severity="Error", action="Stop"),
            ErrorConfig(error_type="element.notfound", severity="Warning", action="Skip")
        ]
        
        # Configure mock service
        self.mock_service.get_all_error_configs.return_value = self.mock_error_configs
        self.mock_service.get_error_hierarchy.return_value = {
            "connection": {
                "timeout": {},
                "failed": {}
            },
            "element": {
                "notfound": {}
            }
        }
    
    def test_initialize_view(self):
        """Test initializing the view."""
        # Call the method
        self.presenter.initialize_view()
        
        # Verify the service was called
        self.mock_service.get_all_error_configs.assert_called_once()
        self.mock_service.get_error_hierarchy.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_error_tree.assert_called_once()
        self.mock_view.update_error_list.assert_called_once_with(self.mock_error_configs)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_load_error_configs(self):
        """Test loading error configurations."""
        # Call the method
        self.presenter.load_error_configs()
        
        # Verify the service was called
        self.mock_service.get_all_error_configs.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_error_list.assert_called_once_with(self.mock_error_configs)
    
    def test_select_error_config(self):
        """Test selecting an error configuration."""
        # Set up mock service
        self.mock_service.get_error_config.return_value = self.mock_error_configs[0]
        
        # Call the method
        self.presenter.select_error_config("connection.timeout")
        
        # Verify the service was called
        self.mock_service.get_error_config.assert_called_once_with("connection.timeout")
        
        # Verify the view was updated
        self.mock_view.populate_editor.assert_called_once_with(self.mock_error_configs[0])
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_add_error_config(self):
        """Test adding an error configuration."""
        # Set up mock service
        self.mock_service.add_error_config.return_value = ErrorConfig(
            error_type="test.error",
            severity="Warning",
            action="Log"
        )
        
        # Call the method
        self.presenter.add_error_config("test.error", "Warning", "Log")
        
        # Verify the service was called
        self.mock_service.add_error_config.assert_called_once_with(
            error_type="test.error",
            severity="Warning",
            action="Log",
            custom_action=None
        )
        
        # Verify the view was updated
        self.mock_view.update_error_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_update_error_config(self):
        """Test updating an error configuration."""
        # Set up mock service
        self.mock_service.update_error_config.return_value = ErrorConfig(
            error_type="connection.timeout",
            severity="Error",
            action="Stop"
        )
        
        # Call the method
        self.presenter.update_error_config("connection.timeout", "Error", "Stop")
        
        # Verify the service was called
        self.mock_service.update_error_config.assert_called_once_with(
            error_type="connection.timeout",
            severity="Error",
            action="Stop",
            custom_action=None
        )
        
        # Verify the view was updated
        self.mock_view.update_error_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_delete_error_config(self):
        """Test deleting an error configuration."""
        # Set up mock service
        self.mock_service.delete_error_config.return_value = True
        
        # Set up mock view
        self.mock_view.ask_yes_no.return_value = True
        
        # Call the method
        self.presenter.delete_error_config("connection.timeout")
        
        # Verify the service was called
        self.mock_service.delete_error_config.assert_called_once_with("connection.timeout")
        
        # Verify the view was updated
        self.mock_view.update_error_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_delete_error_config_cancelled(self):
        """Test cancelling error configuration deletion."""
        # Set up mock view
        self.mock_view.ask_yes_no.return_value = False
        
        # Call the method
        self.presenter.delete_error_config("connection.timeout")
        
        # Verify the service was not called
        self.mock_service.delete_error_config.assert_not_called()
    
    def test_save_error_config_from_editor(self):
        """Test saving an error configuration from the editor."""
        # Set up mock view
        self.mock_view.get_editor_data.return_value = {
            "error_type": "connection.timeout",
            "severity": "Error",
            "action": "Stop",
            "custom_action": None
        }
        
        # Set up mock service
        self.mock_service.update_error_config.return_value = ErrorConfig(
            error_type="connection.timeout",
            severity="Error",
            action="Stop"
        )
        
        # Call the method
        self.presenter.save_error_config_from_editor()
        
        # Verify the view was called
        self.mock_view.get_editor_data.assert_called_once()
        
        # Verify the service was called
        self.mock_service.update_error_config.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_error_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_save_error_config_from_editor_new(self):
        """Test saving a new error configuration from the editor."""
        # Set up mock view
        self.mock_view.get_editor_data.return_value = {
            "error_type": "test.error",
            "severity": "Warning",
            "action": "Log",
            "custom_action": None
        }
        
        # Set up mock service
        self.mock_service.get_error_config.return_value = None
        self.mock_service.add_error_config.return_value = ErrorConfig(
            error_type="test.error",
            severity="Warning",
            action="Log"
        )
        
        # Call the method
        self.presenter.save_error_config_from_editor()
        
        # Verify the view was called
        self.mock_view.get_editor_data.assert_called_once()
        
        # Verify the service was called
        self.mock_service.get_error_config.assert_called_once()
        self.mock_service.add_error_config.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_error_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()

if __name__ == "__main__":
    unittest.main()
