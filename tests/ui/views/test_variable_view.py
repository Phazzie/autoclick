"""Tests for the VariableView class."""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk

# Import the class to test
from src.ui.views.variable_view import VariableView

class TestVariableView(unittest.TestCase):
    """Test cases for the VariableView class."""
    
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
        self.view = VariableView(self.root)
        self.view.set_presenter(self.mock_presenter)
        
        # Build the UI
        self.view.build_ui()
    
    def test_create_widgets(self):
        """Test that widgets are created correctly."""
        # Check that the main components exist
        self.assertIsNotNone(self.view.tree_frame)
        self.assertIsNotNone(self.view.editor_frame)
        self.assertIsNotNone(self.view.variable_tree)
        self.assertIsNotNone(self.view.scope_dropdown)
        self.assertIsNotNone(self.view.name_entry)
        self.assertIsNotNone(self.view.type_dropdown)
        self.assertIsNotNone(self.view.scope_editor_dropdown)
        self.assertIsNotNone(self.view.value_entry)
        self.assertIsNotNone(self.view.new_button)
        self.assertIsNotNone(self.view.save_button)
        self.assertIsNotNone(self.view.delete_button)
        self.assertIsNotNone(self.view.clear_button)
    
    def test_update_variable_list(self):
        """Test updating the variable list."""
        # Create test data
        variables = {
            "Global": [
                {"name": "global_var", "type": "String", "value": "global value", "scope": "Global"}
            ],
            "Workflow": [
                {"name": "workflow_var", "type": "Integer", "value": 42, "scope": "Workflow"}
            ],
            "Local": [
                {"name": "local_var", "type": "Boolean", "value": True, "scope": "Local"}
            ]
        }
        
        # Mock the treeview methods
        self.view.variable_tree.insert = MagicMock(return_value="item_id")
        self.view.variable_tree.delete = MagicMock()
        self.view.variable_tree.get_children = MagicMock(return_value=["item1", "item2"])
        self.view.variable_tree.item = MagicMock()
        
        # Call the method
        self.view.update_variable_list(variables)
        
        # Verify the treeview was cleared
        self.view.variable_tree.delete.assert_called()
        
        # Verify items were inserted
        self.assertEqual(self.view.variable_tree.insert.call_count, 6)  # 3 scopes + 3 variables
    
    def test_populate_editor(self):
        """Test populating the editor."""
        # Create test data
        variable = {
            "name": "test_var",
            "type": "String",
            "value": "test value",
            "scope": "Workflow"
        }
        
        # Call the method
        self.view.populate_editor(variable)
        
        # Verify the editor was populated
        self.assertEqual(self.view.name_entry.get(), "test_var")
        self.assertEqual(self.view.type_var.get(), "String")
        self.assertEqual(self.view.scope_editor_var.get(), "Workflow")
        self.assertEqual(self.view.value_entry.get(), "test value")
        self.assertEqual(self.view.selected_variable, "Workflow:test_var")
    
    def test_populate_editor_boolean(self):
        """Test populating the editor with a boolean variable."""
        # Create test data
        variable = {
            "name": "bool_var",
            "type": "Boolean",
            "value": True,
            "scope": "Global"
        }
        
        # Call the method
        self.view.populate_editor(variable)
        
        # Verify the editor was populated
        self.assertEqual(self.view.name_entry.get(), "bool_var")
        self.assertEqual(self.view.type_var.get(), "Boolean")
        self.assertEqual(self.view.scope_editor_var.get(), "Global")
        self.assertEqual(self.view.bool_var.get(), "True")
        self.assertEqual(self.view.selected_variable, "Global:bool_var")
    
    def test_populate_editor_complex(self):
        """Test populating the editor with a complex variable."""
        # Create test data
        variable = {
            "name": "list_var",
            "type": "List",
            "value": [1, 2, 3],
            "scope": "Local"
        }
        
        # Call the method
        self.view.populate_editor(variable)
        
        # Verify the editor was populated
        self.assertEqual(self.view.name_entry.get(), "list_var")
        self.assertEqual(self.view.type_var.get(), "List")
        self.assertEqual(self.view.scope_editor_var.get(), "Local")
        self.assertEqual(self.view.complex_value_text.get("1.0", "end").strip(), "[1, 2, 3]")
        self.assertEqual(self.view.selected_variable, "Local:list_var")
    
    def test_clear_editor(self):
        """Test clearing the editor."""
        # First populate the editor
        variable = {
            "name": "test_var",
            "type": "String",
            "value": "test value",
            "scope": "Workflow"
        }
        self.view.populate_editor(variable)
        
        # Call the method
        self.view.clear_editor()
        
        # Verify the editor was cleared
        self.assertEqual(self.view.name_entry.get(), "")
        self.assertEqual(self.view.type_var.get(), "String")
        self.assertEqual(self.view.scope_editor_var.get(), "Workflow")
        self.assertEqual(self.view.value_entry.get(), "")
    
    def test_set_editor_state_enabled(self):
        """Test enabling the editor."""
        # Call the method
        self.view.set_editor_state(True)
        
        # Verify the editor was enabled
        self.assertEqual(self.view.name_entry.cget("state"), "normal")
        self.assertEqual(self.view.type_dropdown.cget("state"), "normal")
        self.assertEqual(self.view.scope_editor_dropdown.cget("state"), "normal")
        self.assertEqual(self.view.value_entry.cget("state"), "normal")
        self.assertEqual(self.view.save_button.cget("state"), "normal")
        self.assertEqual(self.view.delete_button.cget("state"), "normal")
    
    def test_set_editor_state_disabled(self):
        """Test disabling the editor."""
        # Call the method
        self.view.set_editor_state(False)
        
        # Verify the editor was disabled
        self.assertEqual(self.view.name_entry.cget("state"), "disabled")
        self.assertEqual(self.view.type_dropdown.cget("state"), "disabled")
        self.assertEqual(self.view.scope_editor_dropdown.cget("state"), "disabled")
        self.assertEqual(self.view.value_entry.cget("state"), "disabled")
        self.assertEqual(self.view.save_button.cget("state"), "disabled")
        self.assertEqual(self.view.delete_button.cget("state"), "disabled")
    
    def test_set_filter_scope(self):
        """Test setting the filter scope."""
        # Call the method
        self.view.set_filter_scope("Global")
        
        # Verify the scope was set
        self.assertEqual(self.view.scope_var.get(), "Global")
        self.assertEqual(self.view.current_scope, "Global")
    
    def test_get_editor_data_string(self):
        """Test getting editor data for a string variable."""
        # Set up the editor
        self.view.name_entry.delete(0, "end")
        self.view.name_entry.insert(0, "string_var")
        self.view.type_var.set("String")
        self.view.scope_editor_var.set("Workflow")
        self.view.value_entry.delete(0, "end")
        self.view.value_entry.insert(0, "string value")
        
        # Call the method
        data = self.view.get_editor_data()
        
        # Verify the data
        self.assertEqual(data["name"], "string_var")
        self.assertEqual(data["type"], "String")
        self.assertEqual(data["value"], "string value")
        self.assertEqual(data["scope"], "Workflow")
    
    def test_get_editor_data_integer(self):
        """Test getting editor data for an integer variable."""
        # Set up the editor
        self.view.name_entry.delete(0, "end")
        self.view.name_entry.insert(0, "int_var")
        self.view.type_var.set("Integer")
        self.view.scope_editor_var.set("Global")
        self.view.value_entry.delete(0, "end")
        self.view.value_entry.insert(0, "42")
        
        # Call the method
        data = self.view.get_editor_data()
        
        # Verify the data
        self.assertEqual(data["name"], "int_var")
        self.assertEqual(data["type"], "Integer")
        self.assertEqual(data["value"], 42)
        self.assertEqual(data["scope"], "Global")
    
    def test_get_editor_data_boolean(self):
        """Test getting editor data for a boolean variable."""
        # Set up the editor
        self.view.name_entry.delete(0, "end")
        self.view.name_entry.insert(0, "bool_var")
        self.view.type_var.set("Boolean")
        self.view.scope_editor_var.set("Local")
        self.view.bool_var.set("True")
        
        # Call the method
        data = self.view.get_editor_data()
        
        # Verify the data
        self.assertEqual(data["name"], "bool_var")
        self.assertEqual(data["type"], "Boolean")
        self.assertEqual(data["value"], True)
        self.assertEqual(data["scope"], "Local")
    
    def test_show_validation_error(self):
        """Test showing a validation error."""
        # Call the method
        self.view.show_validation_error("Test error message")
        
        # Verify the error was shown
        self.assertEqual(self.view.validation_label.cget("text"), "Test error message")
    
    def test_on_scope_changed(self):
        """Test the scope changed event handler."""
        # Call the method
        self.view._on_scope_changed("Global")
        
        # Verify the presenter was called
        self.assertEqual(self.view.current_scope, "Global")
        self.mock_presenter.filter_variables.assert_called_once_with("Global")
    
    def test_on_new_clicked(self):
        """Test the new button click event handler."""
        # Call the method
        self.view._on_new_clicked()
        
        # Verify the editor was cleared and enabled
        self.assertEqual(self.view.name_entry.get(), "")
        self.assertEqual(self.view.selected_variable, None)
        self.assertEqual(self.view.editor_header.cget("text"), "Create a new variable")
    
    def test_on_save_clicked(self):
        """Test the save button click event handler."""
        # Set up the editor
        self.view.name_entry.delete(0, "end")
        self.view.name_entry.insert(0, "test_var")
        
        # Call the method
        self.view._on_save_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.save_variable.assert_called_once()
    
    def test_on_delete_clicked(self):
        """Test the delete button click event handler."""
        # Set up the view
        self.view.selected_variable = "Workflow:test_var"
        
        # Call the method
        self.view._on_delete_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.delete_variable.assert_called_once_with("Workflow:test_var")
    
    def test_on_clear_clicked(self):
        """Test the clear button click event handler."""
        # Set up the view
        self.view.selected_variable = "Workflow:test_var"
        
        # Call the method
        self.view._on_clear_clicked()
        
        # Verify the editor was cleared and disabled
        self.assertEqual(self.view.selected_variable, None)
        self.assertEqual(self.view.editor_header.cget("text"), "Variable Editor")

if __name__ == "__main__":
    unittest.main()
