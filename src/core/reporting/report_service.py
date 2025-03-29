"""
Report service with strict adherence to Single Responsibility Principle.
"""
from typing import Any, Dict, List, Optional

from src.core.reporting.report_interface import ReportInterface
from src.core.reporting.report_manager import ReportManager
from src.core.reporting.report_storage import ReportStorage
from src.core.reporting.report_formatter import ReportFormatter


class ReportService:
    """
    Service for coordinating report creation, storage, and formatting.
    
    This class has the single responsibility of coordinating the reporting process
    by delegating to specialized components for each specific task.
    """
    
    def __init__(self, report_dir: str = "reports"):
        """
        Initialize the report service.
        
        Args:
            report_dir: Directory for storing reports
        """
        self.report_manager = ReportManager()
        self.report_storage = ReportStorage(report_dir=report_dir)
        self.report_formatter = ReportFormatter()
    
    def generate_report(
        self,
        report_type: str,
        source: Any,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        save: bool = False,
        format_type: str = "json",
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Generate a report and optionally save it.
        
        Args:
            report_type: Type of report to create
            source: Data source for the report
            title: Optional report title
            description: Optional report description
            tags: Optional list of tags for categorization
            save: Whether to save the report to disk
            format_type: Format to save as (if save is True)
            **kwargs: Additional keyword arguments for specific report types
            
        Returns:
            Dictionary containing the report data and metadata
        """
        # Create report using manager
        report = self.report_manager.create_report(
            report_type=report_type,
            source=source,
            title=title,
            description=description,
            tags=tags,
            **kwargs
        )
        
        # Generate report data
        report_data = report.generate()
        
        # Save report if requested
        if save:
            file_path = self.report_storage.save_report(
                report=report,
                format_type=format_type
            )
            report_data["file_path"] = file_path
        
        return report_data
    
    def get_report_summary(self, report: ReportInterface) -> str:
        """
        Get a formatted summary of a report.
        
        Args:
            report: The report to summarize
            
        Returns:
            Formatted summary string
        """
        report_data = report.generate()
        return self.report_formatter.format_summary(report_data)
    
    def get_report_metrics(self, report: ReportInterface) -> Dict[str, Any]:
        """
        Get key metrics from a report.
        
        Args:
            report: The report to extract metrics from
            
        Returns:
            Dictionary of key metrics
        """
        report_data = report.generate()
        return self.report_formatter.extract_key_metrics(report_data)
    
    def save_all_reports(self, format_type: str = "json") -> List[str]:
        """
        Save all reports in the manager to disk.
        
        Args:
            format_type: Format to save as
            
        Returns:
            List of file paths for the saved reports
        """
        file_paths = []
        
        for report in self.report_manager.get_reports():
            file_path = self.report_storage.save_report(
                report=report,
                format_type=format_type
            )
            file_paths.append(file_path)
        
        return file_paths
    
    def clear_all(self) -> None:
        """
        Clear all reports from the manager and storage.
        """
        self.report_manager.clear_reports()
        self.report_storage.clear_storage()
