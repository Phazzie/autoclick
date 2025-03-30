"""
Adapter for reporting operations to provide the interface expected by the UI.
SOLID: Single responsibility - adapting reporting operations.
KISS: Simple delegation to reporting engine.
"""
from typing import Dict, List, Any, Optional, Tuple
import uuid
import os
import json

from src.core.models import ReportConfig


class ReportingAdapter:
    """Adapter for reporting operations to provide the interface expected by the UI."""
    
    def __init__(self, reporting_engine=None):
        """
        Initialize the adapter with a reporting engine.
        
        Args:
            reporting_engine: The reporting engine to use (optional)
        """
        self.reporting_engine = reporting_engine
        self.reports: Dict[str, ReportConfig] = {}
        self._load_default_reports()
    
    def _load_default_reports(self):
        """Load default reports."""
        default_reports = [
            ReportConfig(
                id="summary_report",
                name="Summary Report",
                type="SummaryTable",
                data_source_id="csv_example",
                content_options={
                    "title": "Execution Summary",
                    "include_statistics": True,
                    "include_errors": True
                },
                style_options={
                    "theme": "default",
                    "show_borders": True
                }
            ),
            ReportConfig(
                id="error_chart",
                name="Error Distribution",
                type="BarChart",
                data_source_id="csv_example",
                content_options={
                    "title": "Error Distribution by Type",
                    "x_axis": "error_type",
                    "y_axis": "count"
                },
                style_options={
                    "colors": ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],
                    "show_legend": True
                }
            )
        ]
        
        for report in default_reports:
            self.reports[report.id] = report
    
    def get_all_reports(self) -> List[ReportConfig]:
        """
        Get all reports.
        
        Returns:
            List of all reports
        """
        return list(self.reports.values())
    
    def get_report(self, report_id: str) -> Optional[ReportConfig]:
        """
        Get a report by ID.
        
        Args:
            report_id: ID of the report to get
            
        Returns:
            The report, or None if not found
        """
        return self.reports.get(report_id)
    
    def add_report(self, name: str, type_name: str, data_source_id: Optional[str] = None,
                  content_options: Optional[Dict[str, Any]] = None,
                  style_options: Optional[Dict[str, Any]] = None) -> ReportConfig:
        """
        Add a new report.
        
        Args:
            name: Report name
            type_name: Report type (SummaryTable, BarChart, LineChart, etc.)
            data_source_id: ID of the data source to use
            content_options: Content options for the report
            style_options: Style options for the report
            
        Returns:
            The new report
        """
        report_id = str(uuid.uuid4())
        report = ReportConfig(
            id=report_id,
            name=name,
            type=type_name,
            data_source_id=data_source_id,
            content_options=content_options or {},
            style_options=style_options or {}
        )
        
        self.reports[report_id] = report
        return report
    
    def update_report(self, report_id: str, name: Optional[str] = None, 
                     type_name: Optional[str] = None, data_source_id: Optional[str] = None,
                     content_options: Optional[Dict[str, Any]] = None,
                     style_options: Optional[Dict[str, Any]] = None) -> Optional[ReportConfig]:
        """
        Update a report.
        
        Args:
            report_id: ID of the report to update
            name: New report name
            type_name: New report type
            data_source_id: New data source ID
            content_options: New content options
            style_options: New style options
            
        Returns:
            The updated report, or None if not found
        """
        report = self.reports.get(report_id)
        if not report:
            return None
        
        if name is not None:
            report.name = name
        
        if type_name is not None:
            report.type = type_name
        
        if data_source_id is not None:
            report.data_source_id = data_source_id
        
        if content_options is not None:
            report.content_options = content_options
        
        if style_options is not None:
            report.style_options = style_options
        
        return report
    
    def delete_report(self, report_id: str) -> bool:
        """
        Delete a report.
        
        Args:
            report_id: ID of the report to delete
            
        Returns:
            True if the report was deleted, False otherwise
        """
        if report_id in self.reports:
            del self.reports[report_id]
            return True
        return False
    
    def generate_report(self, report_id: str, format_type: str = "html") -> Tuple[bool, str]:
        """
        Generate a report.
        
        Args:
            report_id: ID of the report to generate
            format_type: Format to generate (html, pdf, csv, etc.)
            
        Returns:
            Tuple of (success, result)
            - success: True if the report was generated successfully
            - result: Path to the generated report or error message
        """
        report = self.reports.get(report_id)
        if not report:
            return False, f"Report not found: {report_id}"
        
        # If we have a reporting engine, use it
        if self.reporting_engine:
            try:
                result = self.reporting_engine.generate_report(report, format_type)
                return True, result
            except Exception as e:
                return False, f"Error generating report: {str(e)}"
        
        # Otherwise, return a dummy result for demonstration
        dummy_path = f"reports/{report.name.lower().replace(' ', '_')}.{format_type}"
        return True, dummy_path
    
    def get_report_types(self) -> List[Dict[str, Any]]:
        """
        Get all available report types.
        
        Returns:
            List of report types with metadata
        """
        return [
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
            },
            {
                "type": "LineChart",
                "name": "Line Chart",
                "description": "A line chart for visualizing trends",
                "supported_formats": ["html", "pdf", "png"]
            },
            {
                "type": "PieChart",
                "name": "Pie Chart",
                "description": "A pie chart for visualizing proportions",
                "supported_formats": ["html", "pdf", "png"]
            },
            {
                "type": "DetailedLog",
                "name": "Detailed Log",
                "description": "A detailed log of all actions and results",
                "supported_formats": ["html", "pdf", "txt"]
            }
        ]
