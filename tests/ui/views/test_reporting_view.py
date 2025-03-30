"""
Tests for the reporting view.
SOLID: Single responsibility - testing reporting view.
KISS: Simple tests for reporting view functionality.
"""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk

from src.ui.views.reporting_view import ReportingView

class TestReportingView(unittest.TestCase):
    """Tests for the reporting view."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a root window
        self.root = ctk.CTk()
        
        # Create the view
        self.view = ReportingView(self.root)
        
        # Create a mock presenter
        self.mock_presenter = MagicMock()
        self.view.set_presenter(self.mock_presenter)
        
        # Build the UI
        self.view.build_ui()
    
    def tearDown(self):
        """Clean up after the test."""
        self.root.destroy()
    
    def test_update_report_list(self):
        """Test updating the report list."""
        # Create test reports
        reports = [
            {
                "id": "1",
                "name": "Test Report 1",
                "type": "SummaryTable",
                "data_source_id": "test_source"
            },
            {
                "id": "2",
                "name": "Test Report 2",
                "type": "BarChart",
                "data_source_id": None
            }
        ]
        
        # Update the list
        self.view.update_report_list(reports)
        
        # Check that the tree has the correct number of items
        self.assertEqual(len(self.view.report_tree.get_children()), 2)
        
        # Check that the items have the correct values
        item1 = self.view.report_tree.item("1")
        self.assertEqual(item1["values"][0], "Test Report 1")
        self.assertEqual(item1["values"][1], "SummaryTable")
        self.assertEqual(item1["values"][2], "test_source")
        
        item2 = self.view.report_tree.item("2")
        self.assertEqual(item2["values"][0], "Test Report 2")
        self.assertEqual(item2["values"][1], "BarChart")
        self.assertEqual(item2["values"][2], "None")
    
    def test_display_report(self):
        """Test displaying a report in the editor."""
        # Create a test report
        report = {
            "id": "1",
            "name": "Test Report",
            "type": "SummaryTable",
            "data_source_id": "test_source",
            "content_options": {
                "title": "Test Title",
                "include_statistics": True
            },
            "style_options": {
                "theme": "default",
                "show_borders": True
            }
        }
        
        # Display the report
        self.view.display_report(report)
        
        # Check that the editor fields have the correct values
        self.assertEqual(self.view.name_entry.get(), "Test Report")
        self.assertEqual(self.view.type_var.get(), "SummaryTable")
        self.assertEqual(self.view.data_source_var.get(), "test_source")
        
        # Check that the content options were added
        self.assertTrue(hasattr(self.view.content_options_frame, "option_widgets"))
        self.assertEqual(len(self.view.content_options_frame.option_widgets), 2)
        self.assertIn("title", self.view.content_options_frame.option_widgets)
        self.assertIn("include_statistics", self.view.content_options_frame.option_widgets)
        
        # Check that the style options were added
        self.assertTrue(hasattr(self.view.style_options_frame, "option_widgets"))
        self.assertEqual(len(self.view.style_options_frame.option_widgets), 2)
        self.assertIn("theme", self.view.style_options_frame.option_widgets)
        self.assertIn("show_borders", self.view.style_options_frame.option_widgets)
    
    def test_update_type_options(self):
        """Test updating the type options."""
        # Create test options
        content_options = {
            "title": "Test Title",
            "include_statistics": True
        }
        style_options = {
            "theme": "default",
            "show_borders": True
        }
        
        # Update the options
        self.view.update_type_options("SummaryTable", content_options, style_options)
        
        # Check that the content options were added
        self.assertTrue(hasattr(self.view.content_options_frame, "option_widgets"))
        self.assertEqual(len(self.view.content_options_frame.option_widgets), 2)
        self.assertIn("title", self.view.content_options_frame.option_widgets)
        self.assertIn("include_statistics", self.view.content_options_frame.option_widgets)
        
        # Check that the style options were added
        self.assertTrue(hasattr(self.view.style_options_frame, "option_widgets"))
        self.assertEqual(len(self.view.style_options_frame.option_widgets), 2)
        self.assertIn("theme", self.view.style_options_frame.option_widgets)
        self.assertIn("show_borders", self.view.style_options_frame.option_widgets)
    
    def test_update_data_sources(self):
        """Test updating the data sources."""
        # Create test data sources
        data_sources = [
            {
                "id": "source1",
                "name": "Test Source 1",
                "type": "CSV"
            },
            {
                "id": "source2",
                "name": "Test Source 2",
                "type": "Database"
            }
        ]
        
        # Update the data sources
        self.view.update_data_sources(data_sources)
        
        # Check that the dropdown has the correct values
        expected_values = ["None", "source1", "source2"]
        self.assertEqual(self.view.data_source_dropdown.cget("values"), expected_values)
    
    def test_display_text_report(self):
        """Test displaying a text report."""
        # Display a text report
        self.view.display_text_report("Test content", "Test Title")
        
        # Check that the header was updated
        self.assertEqual(self.view.preview_header.cget("text"), "Report Preview: Test Title")
        
        # Check that the text preview has the correct content
        self.assertEqual(self.view.text_preview.get("1.0", tk.END).strip(), "Test content")
    
    def test_clear_viewer(self):
        """Test clearing the viewer."""
        # Set up the viewer with content
        self.view.display_text_report("Test content", "Test Title")
        
        # Clear the viewer
        self.view.clear_viewer()
        
        # Check that the header was reset
        self.assertEqual(self.view.preview_header.cget("text"), "Report Preview")
        
        # Check that the text preview was cleared
        self.assertEqual(self.view.text_preview.get("1.0", tk.END).strip(), "")
    
    def test_clear_editor(self):
        """Test clearing the editor."""
        # Set up the editor with data
        self.view.name_entry.insert(0, "Test Report")
        self.view.type_var.set("SummaryTable")
        self.view.data_source_var.set("test_source")
        
        # Clear the editor
        self.view.clear_editor()
        
        # Check that the fields were cleared
        self.assertEqual(self.view.name_entry.get(), "")
        self.assertEqual(self.view.type_var.get(), "")
        self.assertEqual(self.view.data_source_var.get(), "None")
    
    def test_set_editor_state(self):
        """Test setting the editor state."""
        # Disable the editor
        self.view.set_editor_state(False)
        
        # Check that the fields are disabled
        self.assertEqual(self.view.name_entry.cget("state"), "disabled")
        self.assertEqual(self.view.type_dropdown.cget("state"), "disabled")
        self.assertEqual(self.view.data_source_dropdown.cget("state"), "disabled")
        self.assertEqual(self.view.save_button.cget("state"), "disabled")
        self.assertEqual(self.view.delete_button.cget("state"), "disabled")
        self.assertEqual(self.view.generate_button.cget("state"), "disabled")
        
        # Enable the editor
        self.view.set_editor_state(True)
        
        # Check that the fields are enabled
        self.assertEqual(self.view.name_entry.cget("state"), "normal")
        self.assertEqual(self.view.type_dropdown.cget("state"), "normal")
        self.assertEqual(self.view.data_source_dropdown.cget("state"), "normal")
        self.assertEqual(self.view.save_button.cget("state"), "normal")
        self.assertEqual(self.view.delete_button.cget("state"), "normal")
        self.assertEqual(self.view.generate_button.cget("state"), "normal")
    
    def test_show_validation_error(self):
        """Test showing a validation error."""
        # Show a validation error
        self.view.show_validation_error("Test error")
        
        # Check that the validation label has the correct text
        self.assertEqual(self.view.validation_label.cget("text"), "Test error")
        
        # Clear the validation error
        self.view.show_validation_error("")
        
        # Check that the validation label is empty
        self.assertEqual(self.view.validation_label.cget("text"), "")
    
    def test_get_editor_data(self):
        """Test getting data from the editor."""
        # Set up the editor with data
        self.view.selected_report = "1"
        self.view.name_entry.insert(0, "Test Report")
        self.view.type_var.set("SummaryTable")
        self.view.data_source_var.set("test_source")
        
        # Add content options
        content_options = {
            "title": "Test Title",
            "include_statistics": True
        }
        style_options = {
            "theme": "default",
            "show_borders": True
        }
        self.view.update_type_options("SummaryTable", content_options, style_options)
        
        # Get the editor data
        data = self.view.get_editor_data()
        
        # Check that the data is correct
        self.assertEqual(data["id"], "1")
        self.assertEqual(data["name"], "Test Report")
        self.assertEqual(data["type"], "SummaryTable")
        self.assertEqual(data["data_source_id"], "test_source")
        self.assertEqual(len(data["content_options"]), 2)
        self.assertEqual(data["content_options"]["title"], "Test Title")
        self.assertEqual(data["content_options"]["include_statistics"], True)
        self.assertEqual(len(data["style_options"]), 2)
        self.assertEqual(data["style_options"]["theme"], "default")
        self.assertEqual(data["style_options"]["show_borders"], True)
    
    def test_on_report_selected(self):
        """Test the report selection handler."""
        # Set up the tree with an item
        self.view.report_tree.insert("", "end", "1", values=("Test Report", "SummaryTable", "test_source"))
        
        # Select the item
        self.view.report_tree.selection_set("1")
        
        # Call the handler
        self.view._on_report_selected(None)
        
        # Check that the presenter was called
        self.mock_presenter.select_report.assert_called_once_with("1")
    
    def test_on_add_clicked(self):
        """Test the add button click handler."""
        # Call the handler
        self.view._on_add_clicked()
        
        # Check that the presenter was called
        self.mock_presenter.create_new_report.assert_called_once()
    
    def test_on_refresh_clicked(self):
        """Test the refresh button click handler."""
        # Call the handler
        self.view._on_refresh_clicked()
        
        # Check that the presenter was called
        self.mock_presenter.load_reports.assert_called_once()
    
    def test_on_save_clicked(self):
        """Test the save button click handler."""
        # Set up the editor with data
        self.view.selected_report = "1"
        self.view.name_entry.insert(0, "Test Report")
        self.view.type_var.set("SummaryTable")
        self.view.data_source_var.set("test_source")
        
        # Call the handler
        self.view._on_save_clicked()
        
        # Check that the presenter was called
        self.mock_presenter.save_report.assert_called_once()
        
        # Check that the correct data was passed
        args, kwargs = self.mock_presenter.save_report.call_args
        data = args[0]
        self.assertEqual(data["id"], "1")
        self.assertEqual(data["name"], "Test Report")
        self.assertEqual(data["type"], "SummaryTable")
        self.assertEqual(data["data_source_id"], "test_source")
    
    def test_on_delete_clicked(self):
        """Test the delete button click handler."""
        # Set up the view
        self.view.selected_report = "1"
        
        # Call the handler
        self.view._on_delete_clicked()
        
        # Check that the presenter was called
        self.mock_presenter.delete_report.assert_called_once_with("1")
    
    def test_on_generate_clicked(self):
        """Test the generate button click handler."""
        # Set up the view
        self.view.selected_report = "1"
        self.view.format_var.set("html")
        
        # Call the handler
        self.view._on_generate_clicked()
        
        # Check that the presenter was called
        self.mock_presenter.generate_report.assert_called_once_with("1", "html")
    
    def test_on_clear_clicked(self):
        """Test the clear button click handler."""
        # Set up the view
        self.view.selected_report = "1"
        self.view.report_tree.insert("", "end", "1", values=("Test Report", "SummaryTable", "test_source"))
        self.view.report_tree.selection_set("1")
        
        # Call the handler
        self.view._on_clear_clicked()
        
        # Check that the view was updated
        self.assertIsNone(self.view.selected_report)
        self.assertEqual(len(self.view.report_tree.selection()), 0)
    
    def test_on_type_changed(self):
        """Test the type change handler."""
        # Call the handler
        self.view._on_type_changed("SummaryTable")
        
        # Check that the presenter was called
        self.mock_presenter.update_type_options.assert_called_once_with("SummaryTable")
    
    def test_on_data_source_changed(self):
        """Test the data source change handler."""
        # Call the handler
        self.view._on_data_source_changed("test_source")
        
        # Check that the presenter was called
        self.mock_presenter.update_data_source_options.assert_called_once_with("test_source")
    
    def test_on_format_changed(self):
        """Test the format change handler."""
        # Call the handler
        self.view._on_format_changed("pdf")
        
        # Check that the format was updated
        self.assertEqual(self.view.current_format, "pdf")

if __name__ == "__main__":
    unittest.main()
