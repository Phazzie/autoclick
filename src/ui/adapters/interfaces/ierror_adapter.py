"""
Error adapter interface.

This module defines the interface for error adapters.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IErrorAdapter(ABC):
    """Interface for error adapters."""
    
    @abstractmethod
    def get_all_errors(self) -> List[Dict[str, Any]]:
        """
        Get all errors.
        
        Returns:
            List of errors in the UI-expected format
        """
        pass
    
    @abstractmethod
    def get_error(self, error_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an error by ID.
        
        Args:
            error_id: Error ID
            
        Returns:
            Error in the UI-expected format, or None if not found
        """
        pass
    
    @abstractmethod
    def get_errors_by_workflow(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Get errors for a workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            List of errors in the UI-expected format
        """
        pass
    
    @abstractmethod
    def get_errors_by_type(self, error_type: str) -> List[Dict[str, Any]]:
        """
        Get errors by type.
        
        Args:
            error_type: Error type
            
        Returns:
            List of errors in the UI-expected format
        """
        pass
    
    @abstractmethod
    def clear_error(self, error_id: str) -> bool:
        """
        Clear an error.
        
        Args:
            error_id: Error ID
            
        Returns:
            True if the error was cleared, False if not found
        """
        pass
    
    @abstractmethod
    def clear_all_errors(self) -> int:
        """
        Clear all errors.
        
        Returns:
            Number of errors cleared
        """
        pass
