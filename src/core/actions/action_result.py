"""
Action result class.

This module defines the result of an action execution.
"""
from typing import Dict, Any, Optional
from enum import Enum, auto


class ActionResultStatus(Enum):
    """Enumeration of action result statuses."""
    
    SUCCESS = auto()
    FAILURE = auto()
    SKIPPED = auto()
    ABORTED = auto()


class ActionResult:
    """
    Result of an action execution.
    
    This class represents the result of executing an action,
    including the status, output data, and any error information.
    """
    
    def __init__(self, status: ActionResultStatus, data: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, error_details: Optional[Dict[str, Any]] = None):
        """
        Initialize an action result.
        
        Args:
            status: Status of the action execution
            data: Optional output data from the action
            error: Optional error message if the action failed
            error_details: Optional detailed error information
        """
        self.status = status
        self.data = data or {}
        self.error = error
        self.error_details = error_details or {}
    
    @property
    def is_success(self) -> bool:
        """Check if the action was successful."""
        return self.status == ActionResultStatus.SUCCESS
    
    @property
    def is_failure(self) -> bool:
        """Check if the action failed."""
        return self.status == ActionResultStatus.FAILURE
    
    @property
    def is_skipped(self) -> bool:
        """Check if the action was skipped."""
        return self.status == ActionResultStatus.SKIPPED
    
    @property
    def is_aborted(self) -> bool:
        """Check if the action was aborted."""
        return self.status == ActionResultStatus.ABORTED
    
    @classmethod
    def success(cls, data: Optional[Dict[str, Any]] = None) -> 'ActionResult':
        """
        Create a success result.
        
        Args:
            data: Optional output data from the action
            
        Returns:
            Success result
        """
        return cls(ActionResultStatus.SUCCESS, data)
    
    @classmethod
    def failure(cls, error: str, error_details: Optional[Dict[str, Any]] = None,
                data: Optional[Dict[str, Any]] = None) -> 'ActionResult':
        """
        Create a failure result.
        
        Args:
            error: Error message
            error_details: Optional detailed error information
            data: Optional output data from the action
            
        Returns:
            Failure result
        """
        return cls(ActionResultStatus.FAILURE, data, error, error_details)
    
    @classmethod
    def skipped(cls, reason: Optional[str] = None) -> 'ActionResult':
        """
        Create a skipped result.
        
        Args:
            reason: Optional reason for skipping the action
            
        Returns:
            Skipped result
        """
        data = {"reason": reason} if reason else {}
        return cls(ActionResultStatus.SKIPPED, data)
    
    @classmethod
    def aborted(cls, reason: Optional[str] = None) -> 'ActionResult':
        """
        Create an aborted result.
        
        Args:
            reason: Optional reason for aborting the action
            
        Returns:
            Aborted result
        """
        data = {"reason": reason} if reason else {}
        return cls(ActionResultStatus.ABORTED, data)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result to a dictionary.
        
        Returns:
            Dictionary representation of the result
        """
        return {
            "status": self.status.name,
            "data": self.data,
            "error": self.error,
            "error_details": self.error_details
        }
