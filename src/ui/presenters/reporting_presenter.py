"""
Presenter for the reporting view.
SOLID: Single responsibility - handling reporting logic.
KISS: Simple delegation to adapter.
"""
from typing import Dict, List, Any, Optional, TYPE_CHECKING
import os
from datetime import datetime

from ..presenters.base_presenter import BasePresenter

if TYPE_CHECKING:
    from ..views.reporting_view import ReportingView
    from ..adapters.reporting_adapter import ReportingAdapter
    from ..adapters.data_source_adapter import DataSourceAdapter

class ReportingPresenter(BasePresenter):
    """Presenter for the reporting view."""

    def __init__(self, view: 'ReportingView', app, service: 'ReportingAdapter', data_source_service: Optional['DataSourceAdapter'] = None):
        """
        Initialize the presenter.

        Args:
            view: The view to present
            app: The main application
            service: The reporting adapter
            data_source_service: The data source adapter (optional)
        """
        super().__init__(view, app)
        self.service = service
        self.data_source_service = data_source_service
        self.reports = []
        self.data_sources = []
        self.report_types = []

    def initialize_view(self):
        """Initialize the view with data."""
        self.load_reports()
        self.load_data_sources()
        self.load_report_types()

    def load_reports(self):
        """Load reports from the service."""
        import logging
        try:
            # Get reports from the service
            logging.info("Loading reports from service")
            self.reports = self.service.get_all_reports()

            # Convert to view format
            report_data = []
            for report in self.reports:
                try:
                    report_data.append({
                        "id": report.id,
                        "name": report.name,
                        "type": report.type,
                        "data_source_id": report.data_source_id,
                        "content_options": report.content_options,
                        "style_options": report.style_options
                    })
                except AttributeError as attr_err:
                    # Log the specific attribute error
                    logging.error(f"Missing attribute in report {getattr(report, 'id', 'unknown')}: {str(attr_err)}")
                    # Continue with next report instead of failing completely
                    continue

            # Update the view
            self.view.update_report_list(report_data)

            # Log success
            logging.info(f"Successfully loaded {len(report_data)} reports")

            # Update status
            self.update_app_status(f"Loaded {len(report_data)} reports")
        except Exception as e:
            error_msg = f"Failed to load reports: {str(e)}"
            logging.error(error_msg)
            self.view.display_error("Error", error_msg)
            self._handle_error("loading reports", e)

    def load_data_sources(self):
        """Load data sources from the service."""
        try:
            # If we have a data source service, use it
            if self.data_source_service:
                self.data_sources = self.data_source_service.get_all_data_sources()

                # Convert to view format
                data_source_data = []
                for source in self.data_sources:
                    data_source_data.append({
                        "id": source.id,
                        "name": source.name,
                        "type": source.type
                    })

                # Update the view
                self.view.update_data_sources(data_source_data)
        except Exception as e:
            self.view.display_error("Error", f"Failed to load data sources: {str(e)}")
            self._handle_error("loading data sources", e)

    def load_report_types(self):
        """Load report types from the service."""
        try:
            # Get report types from the service
            self.report_types = self.service.get_report_types()
        except Exception as e:
            self.view.display_error("Error", f"Failed to load report types: {str(e)}")
            self._handle_error("loading report types", e)

    def select_report(self, report_id: str):
        """
        Select a report.

        Args:
            report_id: ID of the report to select
        """
        try:
            # Get the report from the service
            report = self.service.get_report(report_id)
            if not report:
                self.view.display_error("Error", f"Report not found: {report_id}")
                return

            # Convert to view format
            report_data = {
                "id": report.id,
                "name": report.name,
                "type": report.type,
                "data_source_id": report.data_source_id,
                "content_options": report.content_options,
                "style_options": report.style_options
            }

            # Display the report
            self.view.display_report(report_data)

            # Update status
            self.update_app_status(f"Selected report: {report.name}")
        except Exception as e:
            self.view.display_error("Error", f"Failed to select report: {str(e)}")
            self._handle_error(f"selecting report {report_id}", e)

    def create_new_report(self):
        """Create a new report."""
        try:
            # Clear the editor
            self.view.clear_editor()

            # Set default values
            default_type = "SummaryTable"

            # Get default options for the type
            default_content_options, default_style_options = self._get_default_options(default_type)

            # Update the view
            self.view.update_type_options(default_type, default_content_options, default_style_options)

            # Enable the editor
            self.view.set_editor_state(True)

            # Update status
            self.update_app_status("Creating new report")
        except Exception as e:
            self.view.display_error("Error", f"Failed to create new report: {str(e)}")
            self._handle_error("creating new report", e)

    def save_report(self, report_data: Dict[str, Any]):
        """
        Save a report.

        Args:
            report_data: Report data from the editor
        """
        try:
            # Validate the data
            if not report_data["name"]:
                self.view.show_validation_error("Name is required")
                return

            if not report_data["type"]:
                self.view.show_validation_error("Type is required")
                return

            # Clear validation message
            self.view.show_validation_error("")

            # Check if it's a new report or an update
            if report_data["id"]:
                # Update existing report
                self.service.update_report(
                    report_id=report_data["id"],
                    name=report_data["name"],
                    type_name=report_data["type"],
                    data_source_id=report_data["data_source_id"],
                    content_options=report_data["content_options"],
                    style_options=report_data["style_options"]
                )

                # Update status
                self.update_app_status(f"Updated report: {report_data['name']}")
            else:
                # Create new report
                report = self.service.add_report(
                    name=report_data["name"],
                    type_name=report_data["type"],
                    data_source_id=report_data["data_source_id"],
                    content_options=report_data["content_options"],
                    style_options=report_data["style_options"]
                )

                # Update status
                self.update_app_status(f"Created report: {report_data['name']}")

            # Reload reports
            self.load_reports()
        except Exception as e:
            self.view.display_error("Error", f"Failed to save report: {str(e)}")
            self._handle_error("saving report", e)

    def delete_report(self, report_id: str):
        """
        Delete a report.

        Args:
            report_id: ID of the report to delete
        """
        try:
            # Confirm deletion
            report = self.service.get_report(report_id)
            if not report:
                self.view.display_error("Error", f"Report not found: {report_id}")
                return

            if not self.view.ask_yes_no("Confirm Delete", f"Are you sure you want to delete the report '{report.name}'?"):
                return

            # Delete the report
            self.service.delete_report(report_id)

            # Clear the editor
            self.view.clear_editor()

            # Reload reports
            self.load_reports()

            # Update status
            self.update_app_status(f"Deleted report: {report.name}")
        except Exception as e:
            self.view.display_error("Error", f"Failed to delete report: {str(e)}")
            self._handle_error(f"deleting report {report_id}", e)

    def generate_report(self, report_id: str, format_type: str):
        """
        Generate a report.

        Args:
            report_id: ID of the report to generate
            format_type: Format to generate (html, pdf, csv, etc.)
        """
        import logging
        try:
            # Validate format type
            supported_formats = ["html", "pdf", "csv", "png"]
            if format_type not in supported_formats:
                error_msg = f"Unsupported format type: {format_type}. Supported formats are: {', '.join(supported_formats)}"
                logging.warning(error_msg)
                self.view.display_error("Error", error_msg)
                return

            # Log the generation attempt
            logging.info(f"Generating report {report_id} in {format_type} format")

            # Generate the report
            success, result = self.service.generate_report(report_id, format_type)

            if not success:
                error_msg = f"Failed to generate report: {result}"
                logging.error(error_msg)
                self.view.display_error("Error", error_msg)
                return

            # Get the report
            report = self.service.get_report(report_id)
            if not report:
                error_msg = f"Report not found: {report_id}"
                logging.error(error_msg)
                self.view.display_error("Error", error_msg)
                return

            # If it's a file path, check if it exists
            if os.path.exists(result):
                logging.info(f"Report generated as file: {result}")
                # If it's an HTML file, read it and display in the preview
                if format_type == "html":
                    try:
                        with open(result, "r", encoding="utf-8") as f:
                            content = f.read()
                        self.view.display_text_report(content, report.name)
                        logging.info(f"HTML report displayed in preview: {report.name}")
                    except (IOError, UnicodeDecodeError) as file_err:
                        error_msg = f"Error reading HTML report file: {str(file_err)}"
                        logging.error(error_msg)
                        self.view.display_error("Error", error_msg)
                        return
                else:
                    # For other formats, just show a message
                    self.view.display_info("Report Generated", f"Report generated successfully: {result}")
                    logging.info(f"Non-HTML report generated: {result}")
            else:
                # If it's not a file path, assume it's the content
                self.view.display_text_report(result, report.name)
                logging.info(f"Report content displayed directly: {report.name}")

            # Update status
            self.update_app_status(f"Generated report: {report.name} ({format_type})")
        except FileNotFoundError as fnf_err:
            error_msg = f"File not found: {str(fnf_err)}"
            logging.error(error_msg)
            self.view.display_error("Error", error_msg)
            self._handle_error(f"generating report {report_id} - file not found", fnf_err)
        except PermissionError as perm_err:
            error_msg = f"Permission denied: {str(perm_err)}"
            logging.error(error_msg)
            self.view.display_error("Error", error_msg)
            self._handle_error(f"generating report {report_id} - permission denied", perm_err)
        except Exception as e:
            error_msg = f"Failed to generate report: {str(e)}"
            logging.error(error_msg)
            self.view.display_error("Error", error_msg)
            self._handle_error(f"generating report {report_id}", e)

    def update_type_options(self, type_name: str):
        """
        Update the options based on the selected report type.

        Args:
            type_name: Report type name
        """
        try:
            # Get default options for the type
            content_options, style_options = self._get_default_options(type_name)

            # Update the view
            self.view.update_type_options(type_name, content_options, style_options)
        except Exception as e:
            self.view.display_error("Error", f"Failed to update type options: {str(e)}")
            self._handle_error(f"updating type options for {type_name}", e)

    def update_data_source_options(self, data_source_id: str):
        """
        Update the options based on the selected data source.

        Args:
            data_source_id: Data source ID
        """
        # This is a placeholder for future implementation
        # Currently, we don't update options based on data source
        pass

    def sort_reports(self, column: str, reverse: bool):
        """
        Sort reports by the given column.

        Args:
            column: Column to sort by
            reverse: Whether to sort in reverse order
        """
        try:
            # Sort the reports
            if column == "name":
                self.reports.sort(key=lambda r: r.name, reverse=reverse)
            elif column == "type":
                self.reports.sort(key=lambda r: r.type, reverse=reverse)
            elif column == "data_source":
                self.reports.sort(key=lambda r: r.data_source_id or "", reverse=reverse)

            # Convert to view format
            report_data = []
            for report in self.reports:
                report_data.append({
                    "id": report.id,
                    "name": report.name,
                    "type": report.type,
                    "data_source_id": report.data_source_id,
                    "content_options": report.content_options,
                    "style_options": report.style_options
                })

            # Update the view
            self.view.update_report_list(report_data)

            # Update status
            direction = "descending" if reverse else "ascending"
            self.update_app_status(f"Sorted reports by {column} ({direction})")
        except Exception as e:
            self.view.display_error("Error", f"Failed to sort reports: {str(e)}")
            self._handle_error(f"sorting reports by {column}", e)

    def _get_default_options(self, type_name: str):
        """
        Get default options for the given report type.

        Args:
            type_name: Report type name

        Returns:
            Tuple of (content_options, style_options)
        """
        # Find the report type
        report_type = next((rt for rt in self.report_types if rt["type"] == type_name), None)

        # Default options
        content_options = {}
        style_options = {}

        # Set default options based on type
        if type_name == "SummaryTable":
            content_options = {
                "title": "Summary Report",
                "include_statistics": True,
                "include_errors": True
            }
            style_options = {
                "theme": "default",
                "show_borders": True
            }
        elif type_name == "BarChart":
            content_options = {
                "title": "Bar Chart",
                "x_axis": "category",
                "y_axis": "value"
            }
            style_options = {
                "colors": ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],
                "show_legend": True
            }
        elif type_name == "LineChart":
            content_options = {
                "title": "Line Chart",
                "x_axis": "time",
                "y_axis": "value"
            }
            style_options = {
                "colors": ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],
                "show_legend": True,
                "show_markers": True
            }
        elif type_name == "PieChart":
            content_options = {
                "title": "Pie Chart",
                "labels": "category",
                "values": "value"
            }
            style_options = {
                "colors": ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],
                "show_legend": True,
                "show_percentages": True
            }
        elif type_name == "DetailedLog":
            content_options = {
                "title": "Detailed Log",
                "include_timestamps": True,
                "include_details": True,
                "max_entries": 100
            }
            style_options = {
                "theme": "default",
                "show_borders": True,
                "highlight_errors": True
            }

        return content_options, style_options

    def _handle_error(self, action: str, error: Exception):
        """
        Handle an error.

        Args:
            action: Action that caused the error
            error: The exception
        """
        import logging
        import traceback

        # Get the full stack trace
        stack_trace = traceback.format_exc()

        # Log the error with stack trace
        logging.error(f"Error {action}: {str(error)}\n{stack_trace}")

        # Update status
        self.update_app_status(f"Error {action}")

        # Log specific error types with appropriate severity
        if isinstance(error, (FileNotFoundError, PermissionError)):
            logging.error(f"File operation error {action}: {str(error)}")
        elif isinstance(error, ValueError):
            logging.warning(f"Validation error {action}: {str(error)}")
        elif isinstance(error, KeyError):
            logging.error(f"Missing key error {action}: {str(error)}")
        elif isinstance(error, TypeError):
            logging.error(f"Type error {action}: {str(error)}")
        elif isinstance(error, Exception):
            logging.error(f"Unexpected error {action}: {str(error)}")
