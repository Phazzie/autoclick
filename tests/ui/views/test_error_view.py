"""Tests for the ErrorView class."""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk

from src.ui.views.error_view import ErrorView
from src.core.models import ErrorConfig

class TestErrorView(unittest.TestCase):
    """Test cases for the ErrorView class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are used by all tests."""
        # Initialize the root window
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide the window
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        # Destroy the root window
        cls.root.destroy()
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock presenter
        self.mock_presenter = MagicMock()
        
        # Create the view
        self.view = ErrorView(self.root)
        self.view.set_presenter(self.mock_presenter)
        
        # Build the UI
        self.view.build_ui()
        
        # Set up test data
        self.test_errors = [
            ErrorConfig(error_type="connection.timeout", severity="Warning", action="Retry"),
            ErrorConfig(error_type="connection.failed", severity="Error", action="Stop"),
            ErrorConfig(error_type="element.notfound", severity="Warning", action="Skip")
        ]
    
    def test_create_widgets(self):
        """Test that widgets are created correctly."""
        # Check that the main components exist
        self.assertIsNotNone(self.view.list_frame)
        self.assertIsNotNone(self.view.editor_frame)
        self.assertIsNotNone(self.view.error_tree)
        self.assertIsNotNone(self.view.severity_dropdown)
        self.assertIsNotNone(self.view.error_type_entry)
        self.assertIsNotNone(self.view.severity_var)
        self.assertIsNotNone(self.view.action_var)
        self.assertIsNotNone(self.view.custom_action_entry)
        self.assertIsNotNone(self.view.new_button)
        self.assertIsNotNone(self.view.save_button)
    
    def test_update_error_list(self):
        """Test updating the error list."""
        # Mock the treeview methods
        self.view.error_tree.insert = MagicMock(return_value="item_id")
        self.view.error_tree.delete = MagicMock()
        self.view.error_tree.get_children = MagicMock(return_value=["item1", "item2"])
        
        # Call the method
        self.view.update_error_list(self.test_errors)
        
        # Verify the treeview was cleared
        self.view.error_tree.delete.assert_called()
        
        # Verify items were inserted
        self.assertEqual(self.view.error_tree.insert.call_count, 3)  # 3 errors
    
    def test_add_error_to_list(self):
        """Test adding an error to the list."""
        # Mock the treeview methods
        self.view.error_tree.insert = MagicMock(return_value="item_id")
        
        # Call the method
        self.view.add_error_to_list(self.test_errors[0])
        
        # Verify the error was added
        self.view.error_tree.insert.assert_called_once()
    
    def test_update_error_in_list(self):
        """Test updating an error in the list."""
        # Mock the treeview methods
        self.view.error_tree.item = MagicMock()
        
        # Call the method
        self.view.update_error_in_list(self.test_errors[0])
        
        # Verify the error was updated
        self.view.error_tree.item.assert_called_once()
    
    def test_populate_editor(self):
        """Test populating the editor."""
        # Call the method
        self.view.populate_editor(self.test_errors[0])
        
        # Verify the editor was populated
        self.assertEqual(self.view.error_type_entry.get(), "connection.timeout")
        self.assertEqual(self.view.severity_var.get(), "Warning")
        self.assertEqual(self.view.action_var.get(), "Retry")
        self.assertEqual(self.view.selected_error, "connection.timeout")
    
    def test_clear_editor(self):
        """Test clearing the editor."""
        # First populate the editor
        self.view.populate_editor(self.test_errors[0])
        
        # Call the method
        self.view.clear_editor()
        
        # Verify the editor was cleared
        self.assertEqual(self.view.error_type_entry.get(), "")
        self.assertEqual(self.view.custom_action_entry.get(), "")
        self.assertIsNone(self.view.selected_error)
    
    def test_set_editor_state_enabled(self):
        """Test enabling the editor."""
        # Call the method
        self.view.set_editor_state(True)
        
        # Verify the editor was enabled
        self.assertEqual(self.view.error_type_entry.cget("state"), "normal")
        self.assertEqual(self.view.severity_dropdown.cget("state"), "normal")
        self.assertEqual(self.view.action_dropdown.cget("state"), "normal")
        self.assertEqual(self.view.custom_action_entry.cget("state"), "normal")
        self.assertEqual(self.view.save_button.cget("state"), "normal")
    
    def test_set_editor_state_disabled(self):
        """Test disabling the editor."""
        # Call the method
        self.view.set_editor_state(False)
        
        # Verify the editor was disabled
        self.assertEqual(self.view.error_type_entry.cget("state"), "disabled")
        self.assertEqual(self.view.severity_dropdown.cget("state"), "disabled")
        self.assertEqual(self.view.action_dropdown.cget("state"), "disabled")
        self.assertEqual(self.view.custom_action_entry.cget("state"), "disabled")
        self.assertEqual(self.view.save_button.cget("state"), "disabled")
    
    def test_get_editor_data(self):
        """Test getting editor data."""
        # Set up the editor
        self.view.error_type_entry.delete(0, "end")
        self.view.error_type_entry.insert(0, "connection.timeout")
        self.view.severity_var.set("Warning")
        self.view.action_var.set("Retry")
        self.view.custom_action_entry.delete(0, "end")
        self.view.custom_action_entry.insert(0, "")
        self.view.selected_error = "connection.timeout"
        
        # Call the method
        data = self.view.get_editor_data()
        
        # Verify the data
        self.assertEqual(data["error_type"], "connection.timeout")
        self.assertEqual(data["severity"], "Warning")
        self.assertEqual(data["action"], "Retry")
        self.assertEqual(data["custom_action"], "")
    
    def test_on_severity_filter_changed(self):
        """Test the severity filter changed event handler."""
        # Call the method
        self.view._on_severity_filter_changed("Warning")
        
        # Verify the presenter was called
        self.mock_presenter.filter_errors_by_severity.assert_called_once_with("Warning")
    
    def test_on_error_selected(self):
        """Test the error selected event handler."""
        # Mock the treeview selection
        self.view.error_tree.selection = MagicMock(return_value=["connection.timeout"])
        
        # Call the method
        self.view._on_error_selected(None)
        
        # Verify the presenter was called
        self.mock_presenter.select_error.assert_called_once_with("connection.timeout")
    
    def test_on_new_clicked(self):
        """Test the new button click event handler."""
        # Call the method
        self.view._on_new_clicked()
        
        # Verify the editor was cleared and enabled
        self.assertIsNone(self.view.selected_error)
        self.assertEqual(self.view.editor_header.cget("text"), "Create a new error configuration")
    
    def test_on_save_clicked(self):
        """Test the save button click event handler."""
        # Call the method
        self.view._on_save_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.save_error_from_editor.assert_called_once()
    
    def test_on_action_changed(self):
        """Test the action changed event handler."""
        # Call the method with non-Custom action
        self.view._on_action_changed("Retry")
        
        # Verify the custom action entry was disabled
        self.assertEqual(self.view.custom_action_entry.cget("state"), "disabled")
        
        # Call the method with Custom action
        self.view._on_action_changed("Custom")
        
        # Verify the custom action entry was enabled
        self.assertEqual(self.view.custom_action_entry.cget("state"), "normal")

if __name__ == "__main__":
    unittest.main()
