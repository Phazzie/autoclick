"""
Tests for the reporting presenter.
SOLID: Single responsibility - testing reporting presenter.
KISS: Simple tests for reporting presenter functionality.
"""
import unittest
from unittest.mock import MagicMock, patch
import os
from datetime import datetime

from src.ui.presenters.reporting_presenter import ReportingPresenter
from src.core.models import ReportConfig, DataSourceConfig

class TestReportingPresenter(unittest.TestCase):
    """Tests for the reporting presenter."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create mock view
        self.mock_view = MagicMock()
        
        # Create mock app
        self.mock_app = MagicMock()
        
        # Create mock service
        self.mock_service = MagicMock()
        
        # Create mock data source service
        self.mock_data_source_service = MagicMock()
        
        # Create the presenter
        self.presenter = ReportingPresenter(
            view=self.mock_view,
            app=self.mock_app,
            service=self.mock_service,
            data_source_service=self.mock_data_source_service
        )
        
        # Create test reports
        self.test_reports = [
            ReportConfig(
                id="1",
                name="Test Report 1",
                type="SummaryTable",
                data_source_id="test_source",
                content_options={
                    "title": "Test Title 1",
                    "include_statistics": True
                },
                style_options={
                    "theme": "default",
                    "show_borders": True
                }
            ),
            ReportConfig(
                id="2",
                name="Test Report 2",
                type="BarChart",
                data_source_id=None,
                content_options={
                    "title": "Test Title 2",
                    "x_axis": "category",
                    "y_axis": "value"
                },
                style_options={
                    "colors": ["#ff9999", "#66b3ff"],
                    "show_legend": True
                }
            )
        ]
        
        # Create test data sources
        self.test_data_sources = [
            DataSourceConfig(
                id="test_source",
                name="Test Source",
                type="CSV",
                config_params={
                    "file_path": "test.csv",
                    "delimiter": ","
                }
            ),
            DataSourceConfig(
                id="another_source",
                name="Another Source",
                type="Database",
                config_params={
                    "connection_string": "test_connection",
                    "query": "SELECT * FROM test"
                }
            )
        ]
        
        # Create test report types
        self.test_report_types = [
            {
                "type": "SummaryTable",
                "name": "Summary Table",
                "description": "A table summarizing execution results",
                "supported_formats": ["html", "pdf", "csv"]
            },
            {
                "type": "BarChart",
                "name": "Bar Chart",
                "description": "A bar chart for visualizing data",
                "supported_formats": ["html", "pdf", "png"]
            }
        ]
        
        # Set up the mock service to return the test reports
        self.mock_service.get_all_reports.return_value = self.test_reports
        self.mock_service.get_report_types.return_value = self.test_report_types
        
        # Set up the mock data source service to return the test data sources
        self.mock_data_source_service.get_all_data_sources.return_value = self.test_data_sources
    
    def test_initialize_view(self):
        """Test initializing the view."""
        # Call the method
        self.presenter.initialize_view()
        
        # Verify the services were called
        self.mock_service.get_all_reports.assert_called_once()
        self.mock_data_source_service.get_all_data_sources.assert_called_once()
        self.mock_service.get_report_types.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_report_list.assert_called_once()
        self.mock_view.update_data_sources.assert_called_once()
        
        # Verify the app status was updated
        self.mock_app.update_status.assert_called_once()
    
    def test_load_reports(self):
        """Test loading reports."""
        # Call the method
        self.presenter.load_reports()
        
        # Verify the service was called
        self.mock_service.get_all_reports.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_report_list.assert_called_once()
        
        # Verify the app status was updated
        self.mock_app.update_status.assert_called_once_with("Loaded 2 reports")
        
        # Verify the correct data was passed to the view
        args, kwargs = self.mock_view.update_report_list.call_args
        report_data = args[0]
        self.assertEqual(len(report_data), 2)
        self.assertEqual(report_data[0]["id"], "1")
        self.assertEqual(report_data[0]["name"], "Test Report 1")
        self.assertEqual(report_data[0]["type"], "SummaryTable")
        self.assertEqual(report_data[0]["data_source_id"], "test_source")
        self.assertEqual(report_data[1]["id"], "2")
        self.assertEqual(report_data[1]["name"], "Test Report 2")
        self.assertEqual(report_data[1]["type"], "BarChart")
        self.assertIsNone(report_data[1]["data_source_id"])
    
    def test_load_data_sources(self):
        """Test loading data sources."""
        # Call the method
        self.presenter.load_data_sources()
        
        # Verify the service was called
        self.mock_data_source_service.get_all_data_sources.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_data_sources.assert_called_once()
        
        # Verify the correct data was passed to the view
        args, kwargs = self.mock_view.update_data_sources.call_args
        data_source_data = args[0]
        self.assertEqual(len(data_source_data), 2)
        self.assertEqual(data_source_data[0]["id"], "test_source")
        self.assertEqual(data_source_data[0]["name"], "Test Source")
        self.assertEqual(data_source_data[0]["type"], "CSV")
        self.assertEqual(data_source_data[1]["id"], "another_source")
        self.assertEqual(data_source_data[1]["name"], "Another Source")
        self.assertEqual(data_source_data[1]["type"], "Database")
    
    def test_load_report_types(self):
        """Test loading report types."""
        # Call the method
        self.presenter.load_report_types()
        
        # Verify the service was called
        self.mock_service.get_report_types.assert_called_once()
        
        # Verify the report types were stored
        self.assertEqual(self.presenter.report_types, self.test_report_types)
    
    def test_select_report(self):
        """Test selecting a report."""
        # Set up the mock service to return a specific report
        self.mock_service.get_report.return_value = self.test_reports[0]
        
        # Call the method
        self.presenter.select_report("1")
        
        # Verify the service was called
        self.mock_service.get_report.assert_called_once_with("1")
        
        # Verify the view was updated
        self.mock_view.display_report.assert_called_once()
        
        # Verify the app status was updated
        self.mock_app.update_status.assert_called_once_with("Selected report: Test Report 1")
        
        # Verify the correct data was passed to the view
        args, kwargs = self.mock_view.display_report.call_args
        report_data = args[0]
        self.assertEqual(report_data["id"], "1")
        self.assertEqual(report_data["name"], "Test Report 1")
        self.assertEqual(report_data["type"], "SummaryTable")
        self.assertEqual(report_data["data_source_id"], "test_source")
        self.assertEqual(report_data["content_options"]["title"], "Test Title 1")
        self.assertEqual(report_data["content_options"]["include_statistics"], True)
        self.assertEqual(report_data["style_options"]["theme"], "default")
        self.assertEqual(report_data["style_options"]["show_borders"], True)
    
    def test_create_new_report(self):
        """Test creating a new report."""
        # Call the method
        self.presenter.create_new_report()
        
        # Verify the view was updated
        self.mock_view.clear_editor.assert_called_once()
        self.mock_view.update_type_options.assert_called_once()
        self.mock_view.set_editor_state.assert_called_once_with(True)
        
        # Verify the app status was updated
        self.mock_app.update_status.assert_called_once_with("Creating new report")
        
        # Verify the correct data was passed to the view
        args, kwargs = self.mock_view.update_type_options.call_args
        type_name, content_options, style_options = args
        self.assertEqual(type_name, "SummaryTable")
        self.assertEqual(content_options["title"], "Summary Report")
        self.assertEqual(content_options["include_statistics"], True)
        self.assertEqual(content_options["include_errors"], True)
        self.assertEqual(style_options["theme"], "default")
        self.assertEqual(style_options["show_borders"], True)
    
    def test_save_report_new(self):
        """Test saving a new report."""
        # Create test data
        report_data = {
            "id": None,
            "name": "New Report",
            "type": "SummaryTable",
            "data_source_id": "test_source",
            "content_options": {
                "title": "New Title",
                "include_statistics": True
            },
            "style_options": {
                "theme": "default",
                "show_borders": True
            }
        }
        
        # Set up the mock service
        self.mock_service.add_report.return_value = ReportConfig(
            id="3",
            name="New Report",
            type="SummaryTable",
            data_source_id="test_source",
            content_options={
                "title": "New Title",
                "include_statistics": True
            },
            style_options={
                "theme": "default",
                "show_borders": True
            }
        )
        
        # Call the method
        self.presenter.save_report(report_data)
        
        # Verify the service was called
        self.mock_service.add_report.assert_called_once_with(
            name="New Report",
            type_name="SummaryTable",
            data_source_id="test_source",
            content_options={
                "title": "New Title",
                "include_statistics": True
            },
            style_options={
                "theme": "default",
                "show_borders": True
            }
        )
        
        # Verify the reports were reloaded
        self.mock_service.get_all_reports.assert_called_once()
        
        # Verify the app status was updated
        self.mock_app.update_status.assert_called_once_with("Created report: New Report")
    
    def test_save_report_existing(self):
        """Test saving an existing report."""
        # Create test data
        report_data = {
            "id": "1",
            "name": "Updated Report",
            "type": "SummaryTable",
            "data_source_id": "test_source",
            "content_options": {
                "title": "Updated Title",
                "include_statistics": True
            },
            "style_options": {
                "theme": "default",
                "show_borders": True
            }
        }
        
        # Call the method
        self.presenter.save_report(report_data)
        
        # Verify the service was called
        self.mock_service.update_report.assert_called_once_with(
            report_id="1",
            name="Updated Report",
            type_name="SummaryTable",
            data_source_id="test_source",
            content_options={
                "title": "Updated Title",
                "include_statistics": True
            },
            style_options={
                "theme": "default",
                "show_borders": True
            }
        )
        
        # Verify the reports were reloaded
        self.mock_service.get_all_reports.assert_called_once()
        
        # Verify the app status was updated
        self.mock_app.update_status.assert_called_once_with("Updated report: Updated Report")
    
    def test_save_report_validation_error(self):
        """Test saving a report with validation errors."""
        # Create test data with missing name
        report_data = {
            "id": "1",
            "name": "",
            "type": "SummaryTable",
            "data_source_id": "test_source",
            "content_options": {},
            "style_options": {}
        }
        
        # Call the method
        self.presenter.save_report(report_data)
        
        # Verify the validation error was shown
        self.mock_view.show_validation_error.assert_called_once_with("Name is required")
        
        # Verify the service was not called
        self.mock_service.update_report.assert_not_called()
        self.mock_service.add_report.assert_not_called()
    
    def test_delete_report(self):
        """Test deleting a report."""
        # Set up the mock service
        self.mock_service.get_report.return_value = self.test_reports[0]
        self.mock_view.ask_yes_no.return_value = True
        
        # Call the method
        self.presenter.delete_report("1")
        
        # Verify the service was called
        self.mock_service.get_report.assert_called_once_with("1")
        self.mock_service.delete_report.assert_called_once_with("1")
        
        # Verify the view was updated
        self.mock_view.clear_editor.assert_called_once()
        
        # Verify the reports were reloaded
        self.mock_service.get_all_reports.assert_called_once()
        
        # Verify the app status was updated
        self.mock_app.update_status.assert_called_once_with("Deleted report: Test Report 1")
    
    def test_delete_report_cancelled(self):
        """Test cancelling report deletion."""
        # Set up the mock service
        self.mock_service.get_report.return_value = self.test_reports[0]
        self.mock_view.ask_yes_no.return_value = False
        
        # Call the method
        self.presenter.delete_report("1")
        
        # Verify the service was called to get the report
        self.mock_service.get_report.assert_called_once_with("1")
        
        # Verify the delete service was not called
        self.mock_service.delete_report.assert_not_called()
        
        # Verify the view was not updated
        self.mock_view.clear_editor.assert_not_called()
        
        # Verify the reports were not reloaded
        self.mock_service.get_all_reports.assert_not_called()
    
    @patch("os.path.exists")
    def test_generate_report_html(self, mock_exists):
        """Test generating an HTML report."""
        # Set up the mock service
        self.mock_service.get_report.return_value = self.test_reports[0]
        self.mock_service.generate_report.return_value = (True, "reports/test_report_1.html")
        mock_exists.return_value = True
        
        # Mock the file open
        mock_open = unittest.mock.mock_open(read_data="<html>Test content</html>")
        with patch("builtins.open", mock_open):
            # Call the method
            self.presenter.generate_report("1", "html")
        
        # Verify the service was called
        self.mock_service.generate_report.assert_called_once_with("1", "html")
        self.mock_service.get_report.assert_called_once_with("1")
        
        # Verify the view was updated
        self.mock_view.display_text_report.assert_called_once_with("<html>Test content</html>", "Test Report 1")
        
        # Verify the app status was updated
        self.mock_app.update_status.assert_called_once_with("Generated report: Test Report 1 (html)")
    
    @patch("os.path.exists")
    def test_generate_report_pdf(self, mock_exists):
        """Test generating a PDF report."""
        # Set up the mock service
        self.mock_service.get_report.return_value = self.test_reports[0]
        self.mock_service.generate_report.return_value = (True, "reports/test_report_1.pdf")
        mock_exists.return_value = True
        
        # Call the method
        self.presenter.generate_report("1", "pdf")
        
        # Verify the service was called
        self.mock_service.generate_report.assert_called_once_with("1", "pdf")
        self.mock_service.get_report.assert_called_once_with("1")
        
        # Verify the view was updated
        self.mock_view.display_info.assert_called_once()
        
        # Verify the app status was updated
        self.mock_app.update_status.assert_called_once_with("Generated report: Test Report 1 (pdf)")
    
    def test_generate_report_error(self):
        """Test generating a report with an error."""
        # Set up the mock service
        self.mock_service.generate_report.return_value = (False, "Error generating report")
        
        # Call the method
        self.presenter.generate_report("1", "html")
        
        # Verify the service was called
        self.mock_service.generate_report.assert_called_once_with("1", "html")
        
        # Verify the error was displayed
        self.mock_view.display_error.assert_called_once_with("Error", "Failed to generate report: Error generating report")
    
    def test_update_type_options(self):
        """Test updating type options."""
        # Call the method
        self.presenter.update_type_options("BarChart")
        
        # Verify the view was updated
        self.mock_view.update_type_options.assert_called_once()
        
        # Verify the correct data was passed to the view
        args, kwargs = self.mock_view.update_type_options.call_args
        type_name, content_options, style_options = args
        self.assertEqual(type_name, "BarChart")
        self.assertEqual(content_options["title"], "Bar Chart")
        self.assertEqual(content_options["x_axis"], "category")
        self.assertEqual(content_options["y_axis"], "value")
        self.assertEqual(style_options["colors"], ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])
        self.assertEqual(style_options["show_legend"], True)
    
    def test_sort_reports(self):
        """Test sorting reports."""
        # Set up the presenter with reports
        self.presenter.reports = self.test_reports.copy()
        
        # Call the method
        self.presenter.sort_reports("name", True)
        
        # Verify the view was updated
        self.mock_view.update_report_list.assert_called_once()
        
        # Verify the app status was updated
        self.mock_app.update_status.assert_called_once_with("Sorted reports by name (descending)")
        
        # Verify the reports were sorted correctly
        args, kwargs = self.mock_view.update_report_list.call_args
        report_data = args[0]
        self.assertEqual(report_data[0]["name"], "Test Report 2")
        self.assertEqual(report_data[1]["name"], "Test Report 1")

if __name__ == "__main__":
    unittest.main()
