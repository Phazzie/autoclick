"""
Report interface for defining the contract for all report types.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


class ReportInterface(ABC):
    """
    Interface for report generation and customization.
    
    This interface defines the contract that all report implementations must follow.
    It provides methods for data collection, report generation, and export.
    """
    
    @abstractmethod
    def collect_data(self, source: Any) -> None:
        """
        Collect data from the specified source for the report.
        
        Args:
            source: The data source to collect from (workflow, execution context, etc.)
        """
        pass
    
    @abstractmethod
    def generate(self) -> Dict[str, Any]:
        """
        Generate the report based on collected data.
        
        Returns:
            A dictionary containing the report data
        """
        pass
    
    @abstractmethod
    def export(self, format_type: str, destination: Optional[str] = None) -> Union[str, bytes]:
        """
        Export the report in the specified format.
        
        Args:
            format_type: The format to export (e.g., 'html', 'pdf', 'json', 'csv')
            destination: Optional file path to save the report
            
        Returns:
            The report content as string or bytes depending on the format
        """
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the report.
        
        Returns:
            A dictionary containing report metadata (creation time, type, etc.)
        """
        pass


class ReportMetadata:
    """
    Class for storing report metadata.
    """
    
    def __init__(
        self,
        report_type: str,
        title: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize report metadata.
        
        Args:
            report_type: Type of the report
            title: Report title
            description: Optional report description
            tags: Optional list of tags for categorization
        """
        self.report_type = report_type
        self.title = title
        self.description = description or ""
        self.tags = tags or []
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metadata to dictionary.
        
        Returns:
            Dictionary representation of metadata
        """
        return {
            "report_type": self.report_type,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def update(self) -> None:
        """
        Update the 'updated_at' timestamp to current time.
        """
        self.updated_at = datetime.now()
