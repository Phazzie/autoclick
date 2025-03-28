"""Tests for the refactored SimpleGUI class"""
import unittest
from unittest.mock import MagicMock, patch

from src.ui.simple_gui_refactored import SimpleGUI


class TestSimpleGUIRefactored(unittest.TestCase):
    """Test cases for the refactored SimpleGUI class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        # Mock Tkinter components to avoid actual GUI rendering
        with patch("tkinter.Tk"), \
             patch("src.ui.services.dialog_service.DialogService"), \
             patch("src.ui.services.file_service.FileService"), \
             patch("src.ui.services.theme_service.ThemeService"), \
             patch("src.ui.components.workflow_tab.WorkflowTab"):
            self.gui = SimpleGUI()
        
        # Mock the services
        self.gui.dialog_service = MagicMock()
        self.gui.file_service = MagicMock()
        self.gui.theme_service = MagicMock()
        
        # Mock the components
        self.gui.workflow_tab = MagicMock()

    def test_initialization(self) -> None:
        """Test initialization of the GUI"""
        self.assertIsNotNone(self.gui.workflow_model)
        self.assertIsNotNone(self.gui.dialog_service)
        self.assertIsNotNone(self.gui.file_service)
        self.assertIsNotNone(self.gui.theme_service)
        self.assertIsNotNone(self.gui.workflow_tab)

    def test_new_workflow(self) -> None:
        """Test creating a new workflow"""
        # Mock confirmation dialog to return True
        self.gui.dialog_service.show_confirmation.return_value = True
        
        # Call the method
        self.gui._new_workflow()
        
        # Verify the dialog was shown
        self.gui.dialog_service.show_confirmation.assert_called_once()
        
        # Verify the workflow was cleared
        self.gui.workflow_tab.presenter.refresh_view.assert_called_once()

    def test_open_workflow(self) -> None:
        """Test opening a workflow"""
        # Mock file dialog to return a path
        self.gui.dialog_service.open_file.return_value = "/path/to/workflow.json"
        
        # Mock file service to return workflow data
        workflow_data = {"name": "Test Workflow", "actions": []}
        self.gui.file_service.load_workflow.return_value = workflow_data
        
        # Call the method
        self.gui._open_workflow()
        
        # Verify the dialog was shown
        self.gui.dialog_service.open_file.assert_called_once()
        
        # Verify the file was loaded
        self.gui.file_service.load_workflow.assert_called_once_with("/path/to/workflow.json")
        
        # Verify the view was refreshed
        self.gui.workflow_tab.presenter.refresh_view.assert_called_once()

    def test_save_workflow(self) -> None:
        """Test saving a workflow"""
        # Set a file path
        self.gui.workflow_model.file_path = "/path/to/workflow.json"
        
        # Call the method
        self.gui._save_workflow()
        
        # Verify the file was saved
        self.gui.file_service.save_workflow.assert_called_once()

    def test_save_workflow_as(self) -> None:
        """Test saving a workflow as"""
        # Mock file dialog to return a path
        self.gui.dialog_service.save_file.return_value = "/path/to/new_workflow.json"
        
        # Call the method
        self.gui._save_workflow_as()
        
        # Verify the dialog was shown
        self.gui.dialog_service.save_file.assert_called_once()
        
        # Verify the file was saved
        self.gui.file_service.save_workflow.assert_called_once()

    def test_change_theme(self) -> None:
        """Test changing the theme"""
        # Call the method
        self.gui._change_theme("dark")
        
        # Verify the theme was set
        self.gui.theme_service.set_theme.assert_called_once_with("dark")


if __name__ == "__main__":
    unittest.main()
