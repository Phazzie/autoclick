"""
Workflow-specific exceptions.

This module defines exceptions specific to workflow operations,
providing more detailed error information than generic exceptions.
"""


class WorkflowError(Exception):
    """Base class for all workflow-related exceptions."""
    pass


class WorkflowValidationError(WorkflowError):
    """Exception raised when a workflow fails validation."""
    
    def __init__(self, workflow_id: str, validation_errors: list):
        """
        Initialize a workflow validation error.
        
        Args:
            workflow_id: ID of the workflow that failed validation
            validation_errors: List of validation error messages
        """
        self.workflow_id = workflow_id
        self.validation_errors = validation_errors
        message = f"Workflow '{workflow_id}' failed validation with {len(validation_errors)} errors: {', '.join(validation_errors)}"
        super().__init__(message)


class WorkflowExecutionError(WorkflowError):
    """Exception raised when a workflow execution fails."""
    
    def __init__(self, workflow_id: str, message: str, cause: Exception = None):
        """
        Initialize a workflow execution error.
        
        Args:
            workflow_id: ID of the workflow that failed execution
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.workflow_id = workflow_id
        self.cause = cause
        full_message = f"Workflow '{workflow_id}' execution failed: {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
        super().__init__(full_message)


class ActionExecutionError(WorkflowError):
    """Exception raised when an action execution fails."""
    
    def __init__(self, workflow_id: str, action_id: str, action_type: str, message: str, cause: Exception = None):
        """
        Initialize an action execution error.
        
        Args:
            workflow_id: ID of the workflow containing the action
            action_id: ID of the action that failed
            action_type: Type of the action that failed
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.workflow_id = workflow_id
        self.action_id = action_id
        self.action_type = action_type
        self.cause = cause
        full_message = f"Action '{action_id}' (type: {action_type}) in workflow '{workflow_id}' failed: {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
        super().__init__(full_message)


class WorkflowNotFoundError(WorkflowError):
    """Exception raised when a workflow is not found."""
    
    def __init__(self, workflow_id: str):
        """
        Initialize a workflow not found error.
        
        Args:
            workflow_id: ID of the workflow that was not found
        """
        self.workflow_id = workflow_id
        super().__init__(f"Workflow '{workflow_id}' not found")


class InvalidWorkflowDefinitionError(WorkflowError):
    """Exception raised when a workflow definition is invalid."""
    
    def __init__(self, message: str):
        """
        Initialize an invalid workflow definition error.
        
        Args:
            message: Error message
        """
        super().__init__(f"Invalid workflow definition: {message}")


class CyclicDependencyError(WorkflowError):
    """Exception raised when a workflow contains a cyclic dependency."""
    
    def __init__(self, workflow_id: str, cycle_path: list):
        """
        Initialize a cyclic dependency error.
        
        Args:
            workflow_id: ID of the workflow containing the cycle
            cycle_path: List of action IDs forming the cycle
        """
        self.workflow_id = workflow_id
        self.cycle_path = cycle_path
        cycle_str = " -> ".join(cycle_path)
        super().__init__(f"Workflow '{workflow_id}' contains a cyclic dependency: {cycle_str}")


class MissingActionError(WorkflowError):
    """Exception raised when a required action is missing."""
    
    def __init__(self, workflow_id: str, action_id: str):
        """
        Initialize a missing action error.
        
        Args:
            workflow_id: ID of the workflow
            action_id: ID of the missing action
        """
        self.workflow_id = workflow_id
        self.action_id = action_id
        super().__init__(f"Workflow '{workflow_id}' references non-existent action '{action_id}'")


class InvalidConnectionError(WorkflowError):
    """Exception raised when a connection is invalid."""
    
    def __init__(self, workflow_id: str, source_id: str, target_id: str, message: str):
        """
        Initialize an invalid connection error.
        
        Args:
            workflow_id: ID of the workflow
            source_id: ID of the source action
            target_id: ID of the target action
            message: Error message
        """
        self.workflow_id = workflow_id
        self.source_id = source_id
        self.target_id = target_id
        super().__init__(f"Invalid connection in workflow '{workflow_id}' from '{source_id}' to '{target_id}': {message}")
