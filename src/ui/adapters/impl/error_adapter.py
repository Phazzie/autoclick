"""
Error adapter implementation.

This module provides a concrete implementation of the error adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.core.errors.error_manager import ErrorManager
from src.ui.adapters.base.base_error_adapter import BaseErrorAdapter


class ErrorAdapter(BaseErrorAdapter):
    """Concrete implementation of error adapter."""
    
    def __init__(self, error_manager: Optional[ErrorManager] = None):
        """
        Initialize the adapter with an ErrorManager instance.
        
        Args:
            error_manager: Optional error manager to use
        """
        self._error_manager = error_manager or ErrorManager()
    
    def get_all_errors(self) -> List[Dict[str, Any]]:
        """
        Get all errors.
        
        Returns:
            List of errors in the UI-expected format
        """
        # Get all errors from the manager
        errors = self._error_manager.get_all_errors()
        
        # Convert to UI format
        return [self._convert_error_to_ui_format(error) for error in errors]
    
    def get_error(self, error_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an error by ID.
        
        Args:
            error_id: Error ID
            
        Returns:
            Error in the UI-expected format, or None if not found
        """
        # Get the error from the manager
        error = self._error_manager.get_error(error_id)
        
        # Return None if not found
        if error is None:
            return None
        
        # Convert to UI format
        return self._convert_error_to_ui_format(error)
    
    def get_errors_by_workflow(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Get errors for a workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            List of errors in the UI-expected format
        """
        # Get errors for the workflow from the manager
        errors = self._error_manager.get_errors_by_workflow(workflow_id)
        
        # Convert to UI format
        return [self._convert_error_to_ui_format(error) for error in errors]
    
    def get_errors_by_type(self, error_type: str) -> List[Dict[str, Any]]:
        """
        Get errors by type.
        
        Args:
            error_type: Error type
            
        Returns:
            List of errors in the UI-expected format
        """
        # Get errors by type from the manager
        errors = self._error_manager.get_errors_by_type(error_type)
        
        # Convert to UI format
        return [self._convert_error_to_ui_format(error) for error in errors]
    
    def clear_error(self, error_id: str) -> bool:
        """
        Clear an error.
        
        Args:
            error_id: Error ID
            
        Returns:
            True if the error was cleared, False if not found
        """
        # Clear the error
        return self._error_manager.clear_error(error_id)
    
    def clear_all_errors(self) -> int:
        """
        Clear all errors.
        
        Returns:
            Number of errors cleared
        """
        # Clear all errors
        return self._error_manager.clear_all_errors()
    
    def _convert_error_to_ui_format(self, error: Any) -> Dict[str, Any]:
        """
        Convert an error to UI format.
        
        Args:
            error: Error object
            
        Returns:
            Error in UI format
        """
        return {
            "id": error.id,
            "type": error.type,
            "message": error.message,
            "details": error.details,
            "timestamp": error.timestamp,
            "workflowId": error.workflow_id,
            "stepId": error.step_id,
            "severity": error.severity,
            "status": error.status
        }
