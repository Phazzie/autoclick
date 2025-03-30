"""Tests for the LoopView class."""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk
import json

# Import the class to test
from src.ui.views.loop_view import LoopView

class TestLoopView(unittest.TestCase):
    """Test cases for the LoopView class."""
    
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
        self.view = LoopView(self.root)
        self.view.set_presenter(self.mock_presenter)
        
        # Build the UI
        self.view.build_ui()
        
        # Set up test data
        self.loop_types = [
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
        
        self.test_loop = {
            "id": "test_id",
            "description": "Test loop",
            "type": "for_each",
            "collection_variable": "items",
            "item_variable": "item",
            "actions": []
        }
    
    def test_create_widgets(self):
        """Test that widgets are created correctly."""
        # Check that the main components exist
        self.assertIsNotNone(self.view.list_frame)
        self.assertIsNotNone(self.view.editor_frame)
        self.assertIsNotNone(self.view.loop_tree)
        self.assertIsNotNone(self.view.type_dropdown)
        self.assertIsNotNone(self.view.description_entry)
        self.assertIsNotNone(self.view.parameters_frame)
        self.assertIsNotNone(self.view.actions_frame)
        self.assertIsNotNone(self.view.new_button)
        self.assertIsNotNone(self.view.save_button)
        self.assertIsNotNone(self.view.delete_button)
        self.assertIsNotNone(self.view.clear_button)
    
    def test_update_loop_types(self):
        """Test updating loop types."""
        # Call the method
        self.view.update_loop_types(self.loop_types)
        
        # Verify the loop types were stored
        self.assertEqual(self.view.loop_types, self.loop_types)
        
        # Verify the dropdown was updated
        self.assertEqual(len(self.view.type_dropdown.cget("values")), 2)
    
    def test_update_parameter_editors(self):
        """Test updating parameter editors."""
        # Call the method
        self.view.update_parameter_editors(self.loop_types[0])
        
        # Verify parameter editors were created
        self.assertEqual(len(self.view.parameter_editors), 2)
        self.assertIn("collection_variable", self.view.parameter_editors)
        self.assertIn("item_variable", self.view.parameter_editors)
        
        # Verify the selected loop type was stored
        self.assertEqual(self.view.selected_loop_type, self.loop_types[0])
    
    def test_add_loop_to_list(self):
        """Test adding a loop to the list."""
        # Mock the treeview methods
        self.view.loop_tree.insert = MagicMock(return_value="item_id")
        
        # Call the method
        self.view.add_loop_to_list(self.test_loop)
        
        # Verify the loop was added
        self.view.loop_tree.insert.assert_called_once()
    
    def test_update_loop_in_list(self):
        """Test updating a loop in the list."""
        # Mock the treeview methods
        self.view.loop_tree.item = MagicMock()
        
        # Call the method
        self.view.update_loop_in_list(self.test_loop)
        
        # Verify the loop was updated
        self.view.loop_tree.item.assert_called_once()
    
    def test_remove_loop_from_list(self):
        """Test removing a loop from the list."""
        # Mock the treeview methods
        self.view.loop_tree.delete = MagicMock()
        
        # Call the method
        self.view.remove_loop_from_list("test_id")
        
        # Verify the loop was removed
        self.view.loop_tree.delete.assert_called_once_with("test_id")
    
    def test_populate_editor(self):
        """Test populating the editor."""
        # Set up the view
        self.view.update_loop_types(self.loop_types)
        
        # Call the method
        self.view.populate_editor(self.test_loop)
        
        # Verify the editor was populated
        self.assertEqual(self.view.type_var.get(), "for_each")
        self.assertEqual(self.view.description_entry.get(), "Test loop")
        self.assertEqual(self.view.selected_loop, "test_id")
    
    def test_clear_editor(self):
        """Test clearing the editor."""
        # First populate the editor
        self.view.update_loop_types(self.loop_types)
        self.view.populate_editor(self.test_loop)
        
        # Call the method
        self.view.clear_editor()
        
        # Verify the editor was cleared
        self.assertEqual(self.view.type_var.get(), "")
        self.assertEqual(self.view.description_entry.get(), "")
        self.assertEqual(self.view.parameter_editors, {})
        self.assertIsNone(self.view.selected_loop_type)
    
    def test_set_editor_state_enabled(self):
        """Test enabling the editor."""
        # Call the method
        self.view.set_editor_state(True)
        
        # Verify the editor was enabled
        self.assertEqual(self.view.type_dropdown.cget("state"), "normal")
        self.assertEqual(self.view.description_entry.cget("state"), "normal")
        self.assertEqual(self.view.save_button.cget("state"), "normal")
        self.assertEqual(self.view.delete_button.cget("state"), "normal")
    
    def test_set_editor_state_disabled(self):
        """Test disabling the editor."""
        # Call the method
        self.view.set_editor_state(False)
        
        # Verify the editor was disabled
        self.assertEqual(self.view.type_dropdown.cget("state"), "disabled")
        self.assertEqual(self.view.description_entry.cget("state"), "disabled")
        self.assertEqual(self.view.save_button.cget("state"), "disabled")
        self.assertEqual(self.view.delete_button.cget("state"), "disabled")
    
    def test_get_editor_data(self):
        """Test getting editor data."""
        # Set up the view
        self.view.update_loop_types(self.loop_types)
        self.view.populate_editor(self.test_loop)
        
        # Mock the parameter editors
        self.view.parameter_editors["collection_variable"] = MagicMock()
        self.view.parameter_editors["collection_variable"].get.return_value = "items"
        self.view.parameter_editors["item_variable"] = MagicMock()
        self.view.parameter_editors["item_variable"].get.return_value = "item"
        
        # Call the method
        data = self.view.get_editor_data()
        
        # Verify the data
        self.assertEqual(data["id"], "test_id")
        self.assertEqual(data["type"], "for_each")
        self.assertEqual(data["description"], "Test loop")
        self.assertEqual(data["collection_variable"], "items")
        self.assertEqual(data["item_variable"], "item")
    
    def test_show_validation_error(self):
        """Test showing a validation error."""
        # Call the method
        self.view.show_validation_error("Test error message")
        
        # Verify the error was shown
        self.assertEqual(self.view.validation_label.cget("text"), "Test error message")
    
    def test_on_loop_selected(self):
        """Test the loop selected event handler."""
        # Mock the treeview selection
        self.view.loop_tree.selection = MagicMock(return_value=["test_id"])
        
        # Call the method
        self.view._on_loop_selected(None)
        
        # Verify the presenter was called
        self.mock_presenter.select_loop.assert_called_once_with("test_id")
    
    def test_on_type_changed(self):
        """Test the type changed event handler."""
        # Call the method
        self.view._on_type_changed("for_each")
        
        # Verify the presenter was called
        self.mock_presenter.select_loop_type.assert_called_once_with("for_each")
    
    def test_on_new_clicked(self):
        """Test the new button click event handler."""
        # Mock the clear method
        self.view.clear_editor = MagicMock()
        self.view.set_editor_state = MagicMock()
        
        # Call the method
        self.view._on_new_clicked()
        
        # Verify the methods were called
        self.view.clear_editor.assert_called_once()
        self.view.set_editor_state.assert_called_once_with(True)
        self.assertIsNone(self.view.selected_loop)
    
    def test_on_save_clicked(self):
        """Test the save button click event handler."""
        # Call the method
        self.view._on_save_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.save_loop_from_editor.assert_called_once()
    
    def test_on_delete_clicked(self):
        """Test the delete button click event handler."""
        # Set up the view
        self.view.selected_loop = "test_id"
        
        # Call the method
        self.view._on_delete_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.delete_loop.assert_called_once_with("test_id")
    
    def test_on_clear_clicked(self):
        """Test the clear button click event handler."""
        # Mock the clear method
        self.view.clear_editor = MagicMock()
        self.view.set_editor_state = MagicMock()
        
        # Set up the view
        self.view.selected_loop = "test_id"
        
        # Call the method
        self.view._on_clear_clicked()
        
        # Verify the methods were called
        self.view.clear_editor.assert_called_once()
        self.view.set_editor_state.assert_called_once_with(False)
        self.assertIsNone(self.view.selected_loop)

if __name__ == "__main__":
    unittest.main()
