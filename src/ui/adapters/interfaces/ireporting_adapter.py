"""
Reporting adapter interface.

This module defines the interface for reporting adapters.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IReportingAdapter(ABC):
    """Interface for reporting adapters."""
    
    @abstractmethod
    def get_report_types(self) -> List[Dict[str, Any]]:
        """
        Get all available report types.
        
        Returns:
            List of report types with metadata
        """
        pass
    
    @abstractmethod
    def get_all_reports(self) -> List[Dict[str, Any]]:
        """
        Get all reports.
        
        Returns:
            List of reports in the UI-expected format
        """
        pass
    
    @abstractmethod
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a report by ID.
        
        Args:
            report_id: Report ID
            
        Returns:
            Report in the UI-expected format, or None if not found
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete_report(self, report_id: str) -> bool:
        """
        Delete a report.
        
        Args:
            report_id: Report ID
            
        Returns:
            True if the report was deleted, False if not found
        """
        pass
    
    @abstractmethod
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
        pass
