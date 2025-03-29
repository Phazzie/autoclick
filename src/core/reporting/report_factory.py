"""
Factory for creating different types of reports.
"""
from typing import Any, Dict, List, Optional, Type

from src.core.reporting.report_interface import ReportInterface
from src.core.reporting.base_report import BaseReport
from src.core.reporting.execution_report import ExecutionReport
from src.core.reporting.test_case_report import TestCaseReport
from src.core.reporting.summary_report import SummaryReport


class ReportFactory:
    """
    Factory for creating different types of reports.
    
    This factory provides methods for creating various report types
    and manages report type registration.
    """
    
    _report_types: Dict[str, Type[ReportInterface]] = {
        "execution": ExecutionReport,
        "test_case": TestCaseReport,
        "summary": SummaryReport
    }
    
    @classmethod
    def create_report(
        cls,
        report_type: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any
    ) -> ReportInterface:
        """
        Create a report of the specified type.
        
        Args:
            report_type: Type of report to create
            title: Optional report title
            description: Optional report description
            tags: Optional list of tags for categorization
            **kwargs: Additional keyword arguments for specific report types
            
        Returns:
            A report instance of the specified type
            
        Raises:
            ValueError: If the report type is not registered
        """
        if report_type not in cls._report_types:
            raise ValueError(f"Unknown report type: {report_type}")
        
        report_class = cls._report_types[report_type]
        
        # Create report with provided parameters
        report_args = {}
        if title is not None:
            report_args["title"] = title
        if description is not None:
            report_args["description"] = description
        if tags is not None:
            report_args["tags"] = tags
        
        # Add any additional kwargs
        report_args.update(kwargs)
        
        return report_class(**report_args)
    
    @classmethod
    def register_report_type(cls, report_type: str, report_class: Type[ReportInterface]) -> None:
        """
        Register a new report type.
        
        Args:
            report_type: Type identifier for the report
            report_class: Report class to register
            
        Raises:
            TypeError: If the report class does not implement ReportInterface
        """
        if not issubclass(report_class, ReportInterface):
            raise TypeError(f"Report class must implement ReportInterface: {report_class}")
        
        cls._report_types[report_type] = report_class
    
    @classmethod
    def get_available_report_types(cls) -> List[str]:
        """
        Get a list of available report types.
        
        Returns:
            List of registered report type identifiers
        """
        return list(cls._report_types.keys())
