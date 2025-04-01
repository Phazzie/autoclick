"""
Base error adapter implementation.

This module provides a base implementation of the error adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.ui.adapters.interfaces.ierror_adapter import IErrorAdapter


class BaseErrorAdapter(IErrorAdapter):
    """Base implementation of error adapter."""
    
    def get_all_errors(self) -> List[Dict[str, Any]]:
        """
        Get all errors.
        
        Returns:
            List of errors in the UI-expected format
        """
        raise NotImplementedError("Subclasses must implement get_all_errors")
    
    def get_error(self, error_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an error by ID.
        
        Args:
            error_id: Error ID
            
        Returns:
            Error in the UI-expected format, or None if not found
        """
        raise NotImplementedError("Subclasses must implement get_error")
    
    def get_errors_by_workflow(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Get errors for a workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            List of errors in the UI-expected format
        """
        raise NotImplementedError("Subclasses must implement get_errors_by_workflow")
    
    def get_errors_by_type(self, error_type: str) -> List[Dict[str, Any]]:
        """
        Get errors by type.
        
        Args:
            error_type: Error type
            
        Returns:
            List of errors in the UI-expected format
        """
        raise NotImplementedError("Subclasses must implement get_errors_by_type")
    
    def clear_error(self, error_id: str) -> bool:
        """
        Clear an error.
        
        Args:
            error_id: Error ID
            
        Returns:
            True if the error was cleared, False if not found
        """
        raise NotImplementedError("Subclasses must implement clear_error")
    
    def clear_all_errors(self) -> int:
        """
        Clear all errors.
        
        Returns:
            Number of errors cleared
        """
        raise NotImplementedError("Subclasses must implement clear_all_errors")
