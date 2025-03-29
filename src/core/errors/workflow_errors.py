"""Workflow-related errors for the automation system"""
from typing import Dict, Any, Optional

from src.core.errors.error_types import Error, ErrorType, ErrorSeverity


class WorkflowError(Error):
    """Error raised when there's an issue with a workflow"""
    
    def __init__(
        self,
        workflow_id: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the workflow error
        
        Args:
            workflow_id: ID of the workflow
            message: Human-readable error message
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
        """
        # Add workflow ID to details
        details = details or {}
        details["workflow_id"] = workflow_id
        
        super().__init__(
            error_type=ErrorType.WORKFLOW_ERROR,
            message=message,
            severity=ErrorSeverity.ERROR,
            details=details,
            source=source,
            exception=exception
        )


class ActionError(Error):
    """Error raised when there's an issue with an action"""
    
    def __init__(
        self,
        action_id: str,
        action_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the action error
        
        Args:
            action_id: ID of the action
            action_type: Type of the action
            message: Human-readable error message
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
        """
        # Add action ID and type to details
        details = details or {}
        details["action_id"] = action_id
        details["action_type"] = action_type
        
        super().__init__(
            error_type=ErrorType.ACTION_ERROR,
            message=message,
            severity=ErrorSeverity.ERROR,
            details=details,
            source=source,
            exception=exception
        )


class ConditionError(Error):
    """Error raised when there's an issue with a condition"""
    
    def __init__(
        self,
        condition_id: str,
        condition_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the condition error
        
        Args:
            condition_id: ID of the condition
            condition_type: Type of the condition
            message: Human-readable error message
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
        """
        # Add condition ID and type to details
        details = details or {}
        details["condition_id"] = condition_id
        details["condition_type"] = condition_type
        
        super().__init__(
            error_type=ErrorType.CONDITION_ERROR,
            message=message,
            severity=ErrorSeverity.ERROR,
            details=details,
            source=source,
            exception=exception
        )
