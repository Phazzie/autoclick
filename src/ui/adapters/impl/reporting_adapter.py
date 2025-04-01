"""
Reporting adapter implementation.

This module provides a concrete implementation of the reporting adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.core.reporting.reporting_service import ReportingService
from src.ui.adapters.base.base_reporting_adapter import BaseReportingAdapter


class ReportingAdapter(BaseReportingAdapter):
    """Concrete implementation of reporting adapter."""
    
    def __init__(self, reporting_service: Optional[ReportingService] = None):
        """
        Initialize the adapter with a ReportingService instance.
        
        Args:
            reporting_service: Optional reporting service to use
        """
        self._reporting_service = reporting_service or ReportingService()
    
    def get_report_types(self) -> List[Dict[str, Any]]:
        """
        Get all available report types.
        
        Returns:
            List of report types with metadata
        """
        # Get all report types from the service
        report_types = self._reporting_service.get_report_types()
        
        # Convert to UI format
        return [self._get_report_type_metadata(report_type) for report_type in report_types]
    
    def get_all_reports(self) -> List[Dict[str, Any]]:
        """
        Get all reports.
        
        Returns:
            List of reports in the UI-expected format
        """
        # Get all reports from the service
        reports = self._reporting_service.get_all_reports()
        
        # Convert to UI format
        return [self._convert_report_to_ui_format(report) for report in reports]
    
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a report by ID.
        
        Args:
            report_id: Report ID
            
        Returns:
            Report in the UI-expected format, or None if not found
        """
        # Get the report from the service
        report = self._reporting_service.get_report(report_id)
        
        # Return None if not found
        if report is None:
            return None
        
        # Convert to UI format
        return self._convert_report_to_ui_format(report)
    
    def create_report(self, report_type: str, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a report.
        
        Args:
            report_type: Report type
            report_data: Report data
            
        Returns:
            Created report in the UI-expected format
            
        Raises:
            ValueError: If the report data is invalid
        """
        try:
            # Create the report
            report = self._reporting_service.create_report(report_type, report_data)
            
            # Convert to UI format
            return self._convert_report_to_ui_format(report)
        except Exception as e:
            raise ValueError(f"Error creating report: {str(e)}")
    
    def update_report(self, report_id: str, report_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a report.
        
        Args:
            report_id: Report ID
            report_data: Report data
            
        Returns:
            Updated report in the UI-expected format, or None if not found
            
        Raises:
            ValueError: If the report data is invalid
        """
        try:
            # Update the report
            report = self._reporting_service.update_report(report_id, report_data)
            
            # Return None if not found
            if report is None:
                return None
            
            # Convert to UI format
            return self._convert_report_to_ui_format(report)
        except Exception as e:
            raise ValueError(f"Error updating report: {str(e)}")
    
    def delete_report(self, report_id: str) -> bool:
        """
        Delete a report.
        
        Args:
            report_id: Report ID
            
        Returns:
            True if the report was deleted, False if not found
        """
        try:
            # Delete the report
            return self._reporting_service.delete_report(report_id)
        except Exception as e:
            raise ValueError(f"Error deleting report: {str(e)}")
    
    def generate_report(self, report_id: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a report.
        
        Args:
            report_id: Report ID
            parameters: Optional report parameters
            
        Returns:
            Generated report data
            
        Raises:
            ValueError: If the report is not found or cannot be generated
        """
        try:
            # Generate the report
            report_data = self._reporting_service.generate_report(report_id, parameters)
            
            # Convert to UI format if needed
            return report_data
        except Exception as e:
            raise ValueError(f"Error generating report: {str(e)}")
    
    def _get_report_type_metadata(self, report_type: str) -> Dict[str, Any]:
        """
        Get metadata for a report type.
        
        Args:
            report_type: Report type
            
        Returns:
            Report type metadata
        """
        # Define metadata for known report types
        metadata = {
            "workflow_summary": {
                "id": "workflow_summary",
                "name": "Workflow Summary",
                "description": "Summary of workflow executions",
                "icon": "workflow-summary",
                "category": "workflow"
            },
            "execution_details": {
                "id": "execution_details",
                "name": "Execution Details",
                "description": "Detailed information about workflow executions",
                "icon": "execution-details",
                "category": "workflow"
            },
            "error_report": {
                "id": "error_report",
                "name": "Error Report",
                "description": "Report of errors that occurred during workflow executions",
                "icon": "error-report",
                "category": "error"
            },
            "performance_metrics": {
                "id": "performance_metrics",
                "name": "Performance Metrics",
                "description": "Performance metrics for workflow executions",
                "icon": "performance-metrics",
                "category": "performance"
            }
        }
        
        # Return metadata for the report type, or a default if not found
        return metadata.get(report_type, {
            "id": report_type,
            "name": report_type.capitalize(),
            "description": f"{report_type.capitalize()} report",
            "icon": "report",
            "category": "other"
        })
    
    def _convert_report_to_ui_format(self, report: Any) -> Dict[str, Any]:
        """
        Convert a report to UI format.
        
        Args:
            report: Report object
            
        Returns:
            Report in UI format
        """
        return {
            "id": report.id,
            "type": report.type,
            "name": report.name,
            "description": report.description,
            "config": report.config,
            "createdAt": report.created_at,
            "updatedAt": report.updated_at
        }
