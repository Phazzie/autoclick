"""
Reporting service.

This module provides a service for creating and managing reports.
"""
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime


class Report:
    """
    Report class.
    
    This class represents a report.
    """
    
    def __init__(self, report_id: Optional[str] = None, report_type: Optional[str] = None,
                 name: Optional[str] = None, description: Optional[str] = None,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize a report.
        
        Args:
            report_id: Optional ID for the report
            report_type: Optional type of report
            name: Optional name for the report
            description: Optional description for the report
            config: Optional configuration for the report
        """
        self.id = report_id or str(uuid.uuid4())
        self.type = report_type or "generic"
        self.name = name or f"{self.type.capitalize()} Report"
        self.description = description or ""
        self.config = config or {}
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the report to a dictionary.
        
        Returns:
            Dictionary representation of the report
        """
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "config": self.config,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class ReportingService:
    """
    Service for creating and managing reports.
    
    This class provides methods for creating, retrieving, and generating reports.
    """
    
    def __init__(self):
        """Initialize the reporting service."""
        self._reports: Dict[str, Report] = {}
        self._report_types = ["workflow_summary", "execution_details", "error_report", "performance_metrics"]
    
    def get_report_types(self) -> List[str]:
        """
        Get all available report types.
        
        Returns:
            List of report types
        """
        return self._report_types.copy()
    
    def get_all_reports(self) -> List[Report]:
        """
        Get all reports.
        
        Returns:
            List of reports
        """
        return list(self._reports.values())
    
    def get_report(self, report_id: str) -> Optional[Report]:
        """
        Get a report by ID.
        
        Args:
            report_id: Report ID
            
        Returns:
            Report or None if not found
        """
        return self._reports.get(report_id)
    
    def create_report(self, report_type: str, report_data: Dict[str, Any]) -> Report:
        """
        Create a report.
        
        Args:
            report_type: Report type
            report_data: Report data
            
        Returns:
            Created report
            
        Raises:
            ValueError: If the report type is not supported
        """
        # Validate report type
        if report_type not in self._report_types:
            raise ValueError(f"Unsupported report type: {report_type}")
        
        # Create a new report
        report = Report(
            report_type=report_type,
            name=report_data.get("name"),
            description=report_data.get("description"),
            config=report_data.get("config", {})
        )
        
        # Add the report to the service
        self._reports[report.id] = report
        
        return report
    
    def update_report(self, report_id: str, report_data: Dict[str, Any]) -> Optional[Report]:
        """
        Update a report.
        
        Args:
            report_id: Report ID
            report_data: Report data
            
        Returns:
            Updated report or None if not found
        """
        # Get the report
        report = self.get_report(report_id)
        
        # Return None if not found
        if report is None:
            return None
        
        # Update the report
        if "name" in report_data:
            report.name = report_data["name"]
        
        if "description" in report_data:
            report.description = report_data["description"]
        
        if "config" in report_data:
            report.config = report_data["config"]
        
        # Update the updated_at timestamp
        report.updated_at = datetime.now().isoformat()
        
        return report
    
    def delete_report(self, report_id: str) -> bool:
        """
        Delete a report.
        
        Args:
            report_id: Report ID
            
        Returns:
            True if the report was deleted, False if not found
        """
        # Check if the report exists
        if report_id not in self._reports:
            return False
        
        # Delete the report
        del self._reports[report_id]
        
        return True
    
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
        # Get the report
        report = self.get_report(report_id)
        
        # Raise an error if not found
        if report is None:
            raise ValueError(f"Report not found: {report_id}")
        
        # Generate the report based on its type
        if report.type == "workflow_summary":
            return self._generate_workflow_summary_report(report, parameters)
        elif report.type == "execution_details":
            return self._generate_execution_details_report(report, parameters)
        elif report.type == "error_report":
            return self._generate_error_report(report, parameters)
        elif report.type == "performance_metrics":
            return self._generate_performance_metrics_report(report, parameters)
        else:
            raise ValueError(f"Unsupported report type: {report.type}")
    
    def _generate_workflow_summary_report(self, report: Report, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a workflow summary report.
        
        Args:
            report: Report to generate
            parameters: Optional report parameters
            
        Returns:
            Generated report data
        """
        # Use default parameters if none are provided
        params = parameters or {}
        
        # Generate the report
        return {
            "report_id": report.id,
            "report_type": report.type,
            "report_name": report.name,
            "generated_at": datetime.now().isoformat(),
            "parameters": params,
            "data": {
                "workflows": [
                    {
                        "id": "workflow1",
                        "name": "Sample Workflow 1",
                        "executions": 10,
                        "success_rate": 80,
                        "average_duration": 5.2
                    },
                    {
                        "id": "workflow2",
                        "name": "Sample Workflow 2",
                        "executions": 5,
                        "success_rate": 100,
                        "average_duration": 3.7
                    }
                ],
                "total_executions": 15,
                "overall_success_rate": 86.7,
                "average_duration": 4.7
            }
        }
    
    def _generate_execution_details_report(self, report: Report, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate an execution details report.
        
        Args:
            report: Report to generate
            parameters: Optional report parameters
            
        Returns:
            Generated report data
        """
        # Use default parameters if none are provided
        params = parameters or {}
        
        # Generate the report
        return {
            "report_id": report.id,
            "report_type": report.type,
            "report_name": report.name,
            "generated_at": datetime.now().isoformat(),
            "parameters": params,
            "data": {
                "workflow_id": params.get("workflow_id", "workflow1"),
                "workflow_name": "Sample Workflow",
                "executions": [
                    {
                        "id": "execution1",
                        "start_time": "2023-01-01T10:00:00Z",
                        "end_time": "2023-01-01T10:05:00Z",
                        "status": "completed",
                        "duration": 300,
                        "steps_completed": 5,
                        "steps_failed": 0
                    },
                    {
                        "id": "execution2",
                        "start_time": "2023-01-02T10:00:00Z",
                        "end_time": "2023-01-02T10:04:00Z",
                        "status": "completed",
                        "duration": 240,
                        "steps_completed": 5,
                        "steps_failed": 0
                    }
                ]
            }
        }
    
    def _generate_error_report(self, report: Report, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate an error report.
        
        Args:
            report: Report to generate
            parameters: Optional report parameters
            
        Returns:
            Generated report data
        """
        # Use default parameters if none are provided
        params = parameters or {}
        
        # Generate the report
        return {
            "report_id": report.id,
            "report_type": report.type,
            "report_name": report.name,
            "generated_at": datetime.now().isoformat(),
            "parameters": params,
            "data": {
                "errors": [
                    {
                        "id": "error1",
                        "workflow_id": "workflow1",
                        "execution_id": "execution3",
                        "timestamp": "2023-01-03T10:02:00Z",
                        "error_type": "action_failed",
                        "error_message": "Failed to click element",
                        "step_id": "step2",
                        "action_id": "action3"
                    },
                    {
                        "id": "error2",
                        "workflow_id": "workflow2",
                        "execution_id": "execution2",
                        "timestamp": "2023-01-02T11:05:00Z",
                        "error_type": "timeout",
                        "error_message": "Timed out waiting for element",
                        "step_id": "step3",
                        "action_id": "action2"
                    }
                ],
                "total_errors": 2,
                "error_types": {
                    "action_failed": 1,
                    "timeout": 1
                }
            }
        }
    
    def _generate_performance_metrics_report(self, report: Report, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a performance metrics report.
        
        Args:
            report: Report to generate
            parameters: Optional report parameters
            
        Returns:
            Generated report data
        """
        # Use default parameters if none are provided
        params = parameters or {}
        
        # Generate the report
        return {
            "report_id": report.id,
            "report_type": report.type,
            "report_name": report.name,
            "generated_at": datetime.now().isoformat(),
            "parameters": params,
            "data": {
                "workflow_id": params.get("workflow_id", "workflow1"),
                "workflow_name": "Sample Workflow",
                "metrics": {
                    "average_execution_time": 270,
                    "min_execution_time": 240,
                    "max_execution_time": 300,
                    "average_step_time": 54,
                    "min_step_time": 30,
                    "max_step_time": 80,
                    "average_action_time": 18,
                    "min_action_time": 5,
                    "max_action_time": 40
                },
                "time_series": [
                    {
                        "date": "2023-01-01",
                        "executions": 5,
                        "average_time": 280
                    },
                    {
                        "date": "2023-01-02",
                        "executions": 10,
                        "average_time": 260
                    }
                ]
            }
        }
