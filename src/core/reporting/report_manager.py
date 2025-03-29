"""
Report manager for handling report generation and storage.
"""
import os
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from src.core.reporting.report_interface import ReportInterface
from src.core.reporting.report_factory import ReportFactory


class ReportManager:
    """
    Manager for report generation and storage.
    
    This class provides methods for creating, storing, and retrieving reports.
    It follows the Single Responsibility Principle by focusing only on report management.
    """
    
    def __init__(self, report_dir: str = "reports"):
        """
        Initialize the report manager.
        
        Args:
            report_dir: Directory for storing reports
        """
        self.report_dir = report_dir
        self.reports: List[ReportInterface] = []
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Create report directory if it doesn't exist
        os.makedirs(report_dir, exist_ok=True)
    
    def create_report(
        self,
        report_type: str,
        source: Any,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any
    ) -> ReportInterface:
        """
        Create and populate a new report.
        
        Args:
            report_type: Type of report to create
            source: Data source for the report
            title: Optional report title
            description: Optional report description
            tags: Optional list of tags for categorization
            **kwargs: Additional keyword arguments for specific report types
            
        Returns:
            The created report instance
            
        Raises:
            ValueError: If the report type is not registered
        """
        # Create report using factory
        report = ReportFactory.create_report(
            report_type=report_type,
            title=title,
            description=description,
            tags=tags,
            **kwargs
        )
        
        # Collect data from source
        report.collect_data(source)
        
        # Add to reports list
        self.reports.append(report)
        
        return report
    
    def save_report(
        self,
        report: ReportInterface,
        format_type: str = "json",
        filename: Optional[str] = None
    ) -> str:
        """
        Save a report to disk.
        
        Args:
            report: The report to save
            format_type: Format to save as (e.g., 'json', 'html', 'csv', 'txt')
            filename: Optional filename (generated if not provided)
            
        Returns:
            Path to the saved report file
        """
        # Generate filename if not provided
        if filename is None:
            metadata = report.get_metadata()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_type = metadata.get("report_type", "report")
            filename = f"{report_type}_{timestamp}.{format_type}"
        
        # Ensure correct extension
        if not filename.endswith(f".{format_type}"):
            filename = f"{filename}.{format_type}"
        
        # Create full path
        file_path = os.path.join(self.report_dir, filename)
        
        # Export report to file
        report.export(format_type=format_type, destination=file_path)
        
        self.logger.info(f"Report saved to {file_path}")
        
        return file_path
    
    def get_reports(self, report_type: Optional[str] = None) -> List[ReportInterface]:
        """
        Get reports, optionally filtered by type.
        
        Args:
            report_type: Optional report type to filter by
            
        Returns:
            List of reports
        """
        if report_type is None:
            return self.reports
        
        return [
            report for report in self.reports
            if report.get_metadata().get("report_type") == report_type
        ]
    
    def clear_reports(self) -> None:
        """
        Clear the reports list.
        """
        self.reports = []
