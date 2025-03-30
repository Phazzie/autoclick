"""Tests for the DataSourceView class."""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk

from src.ui.views.data_source_view import DataSourceView
from src.core.models import DataSourceConfig

class TestDataSourceView(unittest.TestCase):
    """Test cases for the DataSourceView class."""
    
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
        self.view = DataSourceView(self.root)
        self.view.set_presenter(self.mock_presenter)
        
        # Build the UI
        self.view.build_ui()
        
        # Set up test data
        self.test_data_sources = [
            DataSourceConfig(
                id="csv_example",
                name="Example CSV",
                type="CSV File",
                config_params={
                    "file_path": "data/example.csv",
                    "has_header": True,
                    "delimiter": ","
                }
            ),
            DataSourceConfig(
                id="json_example",
                name="Example JSON",
                type="JSON File",
                config_params={
                    "file_path": "data/example.json",
                    "root_element": "items"
                }
            )
        ]
    
    def test_create_widgets(self):
        """Test that widgets are created correctly."""
        # Check that the main components exist
        self.assertIsNotNone(self.view.list_frame)
        self.assertIsNotNone(self.view.editor_frame)
        self.assertIsNotNone(self.view.data_source_tree)
        self.assertIsNotNone(self.view.type_dropdown)
        self.assertIsNotNone(self.view.name_entry)
        self.assertIsNotNone(self.view.type_var)
        self.assertIsNotNone(self.view.config_frame)
        self.assertIsNotNone(self.view.preview_frame)
        self.assertIsNotNone(self.view.new_button)
        self.assertIsNotNone(self.view.save_button)
        self.assertIsNotNone(self.view.delete_button)
        self.assertIsNotNone(self.view.preview_button)
    
    def test_update_data_source_list(self):
        """Test updating the data source list."""
        # Mock the treeview methods
        self.view.data_source_tree.insert = MagicMock(return_value="item_id")
        self.view.data_source_tree.delete = MagicMock()
        self.view.data_source_tree.get_children = MagicMock(return_value=["item1", "item2"])
        
        # Call the method
        self.view.update_data_source_list(self.test_data_sources)
        
        # Verify the treeview was cleared
        self.view.data_source_tree.delete.assert_called()
        
        # Verify items were inserted
        self.assertEqual(self.view.data_source_tree.insert.call_count, 2)  # 2 data sources
    
    def test_add_data_source_to_list(self):
        """Test adding a data source to the list."""
        # Mock the treeview methods
        self.view.data_source_tree.insert = MagicMock(return_value="item_id")
        
        # Call the method
        self.view.add_data_source_to_list(self.test_data_sources[0])
        
        # Verify the data source was added
        self.view.data_source_tree.insert.assert_called_once()
    
    def test_update_data_source_in_list(self):
        """Test updating a data source in the list."""
        # Mock the treeview methods
        self.view.data_source_tree.item = MagicMock()
        
        # Call the method
        self.view.update_data_source_in_list(self.test_data_sources[0])
        
        # Verify the data source was updated
        self.view.data_source_tree.item.assert_called_once()
    
    def test_remove_data_source_from_list(self):
        """Test removing a data source from the list."""
        # Mock the treeview methods
        self.view.data_source_tree.delete = MagicMock()
        
        # Call the method
        self.view.remove_data_source_from_list("csv_example")
        
        # Verify the data source was removed
        self.view.data_source_tree.delete.assert_called_once_with("csv_example")
    
    def test_populate_editor_csv(self):
        """Test populating the editor with a CSV data source."""
        # Call the method
        self.view.populate_editor(self.test_data_sources[0])
        
        # Verify the editor was populated
        self.assertEqual(self.view.name_entry.get(), "Example CSV")
        self.assertEqual(self.view.type_var.get(), "CSV File")
        self.assertEqual(self.view.selected_data_source, "csv_example")
        
        # Verify CSV-specific fields were created
        self.assertIn("file_path", self.view.config_editors)
        self.assertIn("has_header", self.view.config_editors)
        self.assertIn("delimiter", self.view.config_editors)
    
    def test_populate_editor_json(self):
        """Test populating the editor with a JSON data source."""
        # Call the method
        self.view.populate_editor(self.test_data_sources[1])
        
        # Verify the editor was populated
        self.assertEqual(self.view.name_entry.get(), "Example JSON")
        self.assertEqual(self.view.type_var.get(), "JSON File")
        self.assertEqual(self.view.selected_data_source, "json_example")
        
        # Verify JSON-specific fields were created
        self.assertIn("file_path", self.view.config_editors)
        self.assertIn("root_element", self.view.config_editors)
    
    def test_clear_editor(self):
        """Test clearing the editor."""
        # First populate the editor
        self.view.populate_editor(self.test_data_sources[0])
        
        # Call the method
        self.view.clear_editor()
        
        # Verify the editor was cleared
        self.assertEqual(self.view.name_entry.get(), "")
        self.assertEqual(self.view.config_editors, {})
        self.assertIsNone(self.view.selected_data_source)
    
    def test_set_editor_state_enabled(self):
        """Test enabling the editor."""
        # Call the method
        self.view.set_editor_state(True)
        
        # Verify the editor was enabled
        self.assertEqual(self.view.name_entry.cget("state"), "normal")
        self.assertEqual(self.view.type_dropdown.cget("state"), "normal")
        self.assertEqual(self.view.save_button.cget("state"), "normal")
        self.assertEqual(self.view.delete_button.cget("state"), "normal")
        self.assertEqual(self.view.preview_button.cget("state"), "normal")
    
    def test_set_editor_state_disabled(self):
        """Test disabling the editor."""
        # Call the method
        self.view.set_editor_state(False)
        
        # Verify the editor was disabled
        self.assertEqual(self.view.name_entry.cget("state"), "disabled")
        self.assertEqual(self.view.type_dropdown.cget("state"), "disabled")
        self.assertEqual(self.view.save_button.cget("state"), "disabled")
        self.assertEqual(self.view.delete_button.cget("state"), "disabled")
        self.assertEqual(self.view.preview_button.cget("state"), "disabled")
    
    def test_get_editor_data_csv(self):
        """Test getting editor data for a CSV data source."""
        # Set up the editor
        self.view.name_entry.delete(0, "end")
        self.view.name_entry.insert(0, "Example CSV")
        self.view.type_var.set("CSV File")
        self.view.selected_data_source = "csv_example"
        
        # Create mock config editors
        self.view.config_editors = {
            "file_path": MagicMock(),
            "has_header": MagicMock(),
            "delimiter": MagicMock()
        }
        self.view.config_editors["file_path"].get.return_value = "data/example.csv"
        self.view.config_editors["has_header"].get.return_value = "True"
        self.view.config_editors["delimiter"].get.return_value = ","
        
        # Call the method
        data = self.view.get_editor_data()
        
        # Verify the data
        self.assertEqual(data["id"], "csv_example")
        self.assertEqual(data["name"], "Example CSV")
        self.assertEqual(data["type"], "CSV File")
        self.assertEqual(data["config_params"]["file_path"], "data/example.csv")
        self.assertEqual(data["config_params"]["has_header"], True)
        self.assertEqual(data["config_params"]["delimiter"], ",")
    
    def test_display_data_preview(self):
        """Test displaying a data preview."""
        # Set up test data
        headers = ["Column1", "Column2", "Column3"]
        rows = [
            ["Value1", "Value2", "Value3"],
            ["Value4", "Value5", "Value6"]
        ]
        
        # Mock the preview table
        self.view.preview_table = MagicMock()
        
        # Call the method
        self.view.display_data_preview(headers, rows)
        
        # Verify the preview was displayed
        self.view.preview_table.delete_all.assert_called_once()
        self.assertEqual(self.view.preview_table.add_column.call_count, 3)  # 3 columns
        self.assertEqual(self.view.preview_table.add_row.call_count, 2)  # 2 rows
    
    def test_on_type_filter_changed(self):
        """Test the type filter changed event handler."""
        # Call the method
        self.view._on_type_filter_changed("CSV File")
        
        # Verify the presenter was called
        self.mock_presenter.filter_data_sources_by_type.assert_called_once_with("CSV File")
    
    def test_on_data_source_selected(self):
        """Test the data source selected event handler."""
        # Mock the treeview selection
        self.view.data_source_tree.selection = MagicMock(return_value=["csv_example"])
        
        # Call the method
        self.view._on_data_source_selected(None)
        
        # Verify the presenter was called
        self.mock_presenter.select_data_source.assert_called_once_with("csv_example")
    
    def test_on_type_changed(self):
        """Test the type changed event handler."""
        # Call the method
        self.view._on_type_changed("CSV File")
        
        # Verify the config editors were updated
        self.assertIn("file_path", self.view.config_editors)
        self.assertIn("has_header", self.view.config_editors)
        self.assertIn("delimiter", self.view.config_editors)
    
    def test_on_new_clicked(self):
        """Test the new button click event handler."""
        # Call the method
        self.view._on_new_clicked()
        
        # Verify the editor was cleared and enabled
        self.assertIsNone(self.view.selected_data_source)
        self.assertEqual(self.view.editor_header.cget("text"), "Create a new data source")
    
    def test_on_save_clicked(self):
        """Test the save button click event handler."""
        # Call the method
        self.view._on_save_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.save_data_source_from_editor.assert_called_once()
    
    def test_on_delete_clicked(self):
        """Test the delete button click event handler."""
        # Set up the view
        self.view.selected_data_source = "csv_example"
        
        # Call the method
        self.view._on_delete_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.delete_data_source.assert_called_once_with("csv_example")
    
    def test_on_preview_clicked(self):
        """Test the preview button click event handler."""
        # Set up the view
        self.view.selected_data_source = "csv_example"
        
        # Call the method
        self.view._on_preview_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.get_data_preview.assert_called_once_with("csv_example")

if __name__ == "__main__":
    unittest.main()
