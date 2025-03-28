"""Tests for the ExecutionPresenter class"""
import unittest
from unittest.mock import MagicMock, patch

from src.ui.models.execution_model import ExecutionModel
from src.ui.services.execution_service import ExecutionService
from src.ui.presenters.execution_presenter import ExecutionPresenter


class TestExecutionPresenter(unittest.TestCase):
    """Test cases for the ExecutionPresenter class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.model = MagicMock(spec=ExecutionModel)
        self.service = MagicMock(spec=ExecutionService)
        self.view = MagicMock()
        self.presenter = ExecutionPresenter(self.model, self.service, self.view)
        
        self.test_workflow = {
            "name": "Test Workflow",
            "actions": [
                {
                    "type": "click",
                    "selector": "#test-button",
                    "description": "Click test button"
                }
            ]
        }
        
        self.test_options = {
            "browser_type": "chrome",
            "headless": False,
            "timeout": 30
        }

    def test_run_workflow(self) -> None:
        """Test running a workflow"""
        # Mock the model methods
        self.model.get_options.return_value = self.test_options
        
        # Run the workflow
        with patch("threading.Thread") as mock_thread:
            self.presenter.run_workflow(self.test_workflow)
            
            # Verify the model was updated
            self.model.start_execution.assert_called_once_with(self.test_workflow)
            
            # Verify the browser was initialized
            self.service.initialize_browser.assert_called_once_with(self.test_options)
            
            # Verify the view was updated
            self.view.display_execution_log.assert_called_once()
            self.view.update_execution_status.assert_called_once()
            self.view.show_message.assert_called_once_with("Workflow execution started")
            
            # Verify a thread was started
            mock_thread.assert_called_once()

    def test_run_workflow_no_actions(self) -> None:
        """Test running a workflow with no actions"""
        # Run the workflow
        self.presenter.run_workflow({"name": "Empty Workflow", "actions": []})
        
        # Verify the model was not updated
        self.model.start_execution.assert_not_called()
        
        # Verify the browser was not initialized
        self.service.initialize_browser.assert_not_called()
        
        # Verify the view was updated
        self.view.show_message.assert_called_once_with("Workflow has no actions")

    def test_run_workflow_exception(self) -> None:
        """Test running a workflow with an exception"""
        # Mock the model methods to raise an exception
        self.model.start_execution.side_effect = Exception("Test exception")
        
        # Run the workflow
        self.presenter.run_workflow(self.test_workflow)
        
        # Verify the model was updated
        self.model.start_execution.assert_called_once_with(self.test_workflow)
        
        # Verify the browser was not initialized
        self.service.initialize_browser.assert_not_called()
        
        # Verify the view was updated
        self.view.show_message.assert_called_once_with("Error starting workflow: Test exception")

    def test_stop_execution(self) -> None:
        """Test stopping execution"""
        # Stop execution
        self.presenter.stop_execution()
        
        # Verify the model was updated
        self.model.stop_execution.assert_called_once()
        
        # Verify the view was updated
        self.view.display_execution_log.assert_called_once()
        self.view.update_execution_status.assert_called_once()
        self.view.show_message.assert_called_once_with("Workflow execution stopped")

    def test_set_browser_type(self) -> None:
        """Test setting browser type"""
        # Set browser type
        self.presenter.set_browser_type("firefox")
        
        # Verify the model was updated
        self.model.set_option.assert_called_once_with("browser_type", "firefox")
        
        # Verify the view was updated
        self.view.show_message.assert_called_once_with("Browser type set to firefox")

    def test_set_headless(self) -> None:
        """Test setting headless mode"""
        # Set headless mode
        self.presenter.set_headless(True)
        
        # Verify the model was updated
        self.model.set_option.assert_called_once_with("headless", True)
        
        # Verify the view was updated
        self.view.show_message.assert_called_once_with("Headless mode enabled")

    def test_refresh_view(self) -> None:
        """Test refreshing the view"""
        # Mock the model methods
        self.model.get_log_entries.return_value = []
        self.model.is_execution_running.return_value = False
        
        # Refresh the view
        self.presenter.refresh_view()
        
        # Verify the view was updated
        self.view.display_execution_log.assert_called_once_with([])
        self.view.update_execution_status.assert_called_once_with(False)


if __name__ == "__main__":
    unittest.main()
