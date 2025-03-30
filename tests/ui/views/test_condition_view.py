"""Tests for the ConditionView class."""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk
import json

# Import the class to test
from src.ui.views.condition_view import ConditionView

class TestConditionView(unittest.TestCase):
    """Test cases for the ConditionView class."""
    
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
        self.view = ConditionView(self.root)
        self.view.set_presenter(self.mock_presenter)
        
        # Build the UI
        self.view.build_ui()
        
        # Set up test data
        self.condition_types = [
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
        
        self.test_condition = {
            "id": "test_id",
            "description": "Test condition",
            "type": "comparison",
            "left_value": "x",
            "operator": "EQUAL",
            "right_value": "y"
        }
    
    def test_create_widgets(self):
        """Test that widgets are created correctly."""
        # Check that the main components exist
        self.assertIsNotNone(self.view.list_frame)
        self.assertIsNotNone(self.view.editor_frame)
        self.assertIsNotNone(self.view.condition_tree)
        self.assertIsNotNone(self.view.category_dropdown)
        self.assertIsNotNone(self.view.type_dropdown)
        self.assertIsNotNone(self.view.description_entry)
        self.assertIsNotNone(self.view.parameters_frame)
        self.assertIsNotNone(self.view.test_context_text)
        self.assertIsNotNone(self.view.test_button)
        self.assertIsNotNone(self.view.new_button)
        self.assertIsNotNone(self.view.save_button)
        self.assertIsNotNone(self.view.delete_button)
        self.assertIsNotNone(self.view.clear_button)
    
    def test_update_condition_types(self):
        """Test updating condition types."""
        # Call the method
        self.view.update_condition_types(self.condition_types)
        
        # Verify the condition types were stored
        self.assertEqual(self.view.condition_types, self.condition_types)
        
        # Verify the dropdown was updated
        self.assertEqual(len(self.view.type_dropdown.cget("values")), 2)
    
    def test_update_parameter_editors(self):
        """Test updating parameter editors."""
        # Call the method
        self.view.update_parameter_editors(self.condition_types[0])
        
        # Verify parameter editors were created
        self.assertEqual(len(self.view.parameter_editors), 4)  # 3 parameters + 1 variable
        self.assertIn("left_value", self.view.parameter_editors)
        self.assertIn("operator", self.view.parameter_editors)
        self.assertIn("operator_var", self.view.parameter_editors)
        self.assertIn("right_value", self.view.parameter_editors)
        
        # Verify the selected condition type was stored
        self.assertEqual(self.view.selected_condition_type, self.condition_types[0])
    
    def test_add_condition_to_list(self):
        """Test adding a condition to the list."""
        # Mock the treeview methods
        self.view.condition_tree.insert = MagicMock(return_value="item_id")
        self.view.condition_tree.get_children = MagicMock(return_value=[])
        
        # Call the method
        self.view.add_condition_to_list(self.test_condition)
        
        # Verify the condition was added
        self.view.condition_tree.insert.assert_called_once()
    
    def test_update_condition_in_list(self):
        """Test updating a condition in the list."""
        # Mock the treeview methods
        self.view.condition_tree.item = MagicMock()
        self.view.condition_tree.get_children = MagicMock(return_value=[])
        
        # Call the method
        self.view.update_condition_in_list(self.test_condition)
        
        # Verify the condition was updated
        self.view.condition_tree.item.assert_called_once()
    
    def test_remove_condition_from_list(self):
        """Test removing a condition from the list."""
        # Mock the treeview methods
        self.view.condition_tree.delete = MagicMock()
        
        # Call the method
        self.view.remove_condition_from_list("test_id")
        
        # Verify the condition was removed
        self.view.condition_tree.delete.assert_called_once_with("test_id")
    
    def test_populate_editor(self):
        """Test populating the editor."""
        # Set up the view
        self.view.update_condition_types(self.condition_types)
        
        # Call the method
        self.view.populate_editor(self.test_condition)
        
        # Verify the editor was populated
        self.assertEqual(self.view.type_var.get(), "comparison")
        self.assertEqual(self.view.description_entry.get(), "Test condition")
        self.assertEqual(self.view.selected_condition, "test_id")
        
        # Verify parameter editors were created and populated
        self.assertIn("left_value", self.view.parameter_editors)
        self.assertIn("operator", self.view.parameter_editors)
        self.assertIn("right_value", self.view.parameter_editors)
    
    def test_clear_editor(self):
        """Test clearing the editor."""
        # First populate the editor
        self.view.update_condition_types(self.condition_types)
        self.view.populate_editor(self.test_condition)
        
        # Call the method
        self.view.clear_editor()
        
        # Verify the editor was cleared
        self.assertEqual(self.view.type_var.get(), "")
        self.assertEqual(self.view.description_entry.get(), "")
        self.assertEqual(self.view.parameter_editors, {})
        self.assertIsNone(self.view.selected_condition_type)
    
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
    
    def test_set_filter_category(self):
        """Test setting the filter category."""
        # Call the method
        self.view.set_filter_category("Basic")
        
        # Verify the category was set
        self.assertEqual(self.view.category_var.get(), "Basic")
        self.assertEqual(self.view.current_category, "Basic")
    
    def test_get_editor_data(self):
        """Test getting editor data."""
        # Set up the view
        self.view.update_condition_types(self.condition_types)
        self.view.populate_editor(self.test_condition)
        
        # Call the method
        data = self.view.get_editor_data()
        
        # Verify the data
        self.assertEqual(data["id"], "test_id")
        self.assertEqual(data["type"], "comparison")
        self.assertEqual(data["description"], "Test condition")
    
    def test_show_validation_error(self):
        """Test showing a validation error."""
        # Call the method
        self.view.show_validation_error("Test error message")
        
        # Verify the error was shown
        self.assertEqual(self.view.validation_label.cget("text"), "Test error message")
    
    def test_display_test_result_success(self):
        """Test displaying a successful test result."""
        # Call the method
        self.view.display_test_result(True, "Condition evaluated successfully")
        
        # Verify the result was displayed
        self.assertEqual(self.view.test_result_label.cget("text"), "Result: True - Condition evaluated successfully")
        self.assertEqual(self.view.test_result_label.cget("text_color"), "green")
    
    def test_display_test_result_failure(self):
        """Test displaying a failed test result."""
        # Call the method
        self.view.display_test_result(False, "Condition evaluation failed")
        
        # Verify the result was displayed
        self.assertEqual(self.view.test_result_label.cget("text"), "Result: False - Condition evaluation failed")
        self.assertEqual(self.view.test_result_label.cget("text_color"), "red")
    
    def test_on_category_changed(self):
        """Test the category changed event handler."""
        # Mock the filter method
        self.view._filter_condition_list = MagicMock()
        
        # Call the method
        self.view._on_category_changed("Basic")
        
        # Verify the category was set and filter was called
        self.assertEqual(self.view.current_category, "Basic")
        self.view._filter_condition_list.assert_called_once()
    
    def test_on_condition_selected(self):
        """Test the condition selected event handler."""
        # Mock the treeview selection
        self.view.condition_tree.selection = MagicMock(return_value=["test_id"])
        
        # Call the method
        self.view._on_condition_selected(None)
        
        # Verify the presenter was called
        self.mock_presenter.select_condition.assert_called_once_with("test_id")
    
    def test_on_type_changed(self):
        """Test the type changed event handler."""
        # Call the method
        self.view._on_type_changed("comparison")
        
        # Verify the presenter was called
        self.mock_presenter.select_condition_type.assert_called_once_with("comparison")
    
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
        self.assertIsNone(self.view.selected_condition)
    
    def test_on_save_clicked(self):
        """Test the save button click event handler."""
        # Call the method
        self.view._on_save_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.save_condition_from_editor.assert_called_once()
    
    def test_on_delete_clicked(self):
        """Test the delete button click event handler."""
        # Set up the view
        self.view.selected_condition = "test_id"
        
        # Call the method
        self.view._on_delete_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.delete_condition.assert_called_once_with("test_id")
    
    def test_on_clear_clicked(self):
        """Test the clear button click event handler."""
        # Mock the clear method
        self.view.clear_editor = MagicMock()
        self.view.set_editor_state = MagicMock()
        
        # Set up the view
        self.view.selected_condition = "test_id"
        
        # Call the method
        self.view._on_clear_clicked()
        
        # Verify the methods were called
        self.view.clear_editor.assert_called_once()
        self.view.set_editor_state.assert_called_once_with(False)
        self.assertIsNone(self.view.selected_condition)
    
    def test_on_test_clicked(self):
        """Test the test button click event handler."""
        # Set up the view
        self.view.selected_condition = "test_id"
        self.view.test_context_text.delete("1.0", "end")
        self.view.test_context_text.insert("1.0", '{"variable1": "value1"}')
        
        # Call the method
        self.view._on_test_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.test_condition.assert_called_once_with("test_id", {"variable1": "value1"})

if __name__ == "__main__":
    unittest.main()
