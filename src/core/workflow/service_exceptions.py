"""
Workflow service exceptions.

This module defines exceptions specific to workflow service operations,
providing more detailed error information than generic exceptions.
"""


class WorkflowServiceError(Exception):
    """Base class for all workflow service-related exceptions."""
    pass


class WorkflowNotFoundError(WorkflowServiceError):
    """Exception raised when a workflow is not found."""
    
    def __init__(self, workflow_id: str):
        """
        Initialize a workflow not found error.
        
        Args:
            workflow_id: ID of the workflow that was not found
        """
        self.workflow_id = workflow_id
        super().__init__(f"Workflow '{workflow_id}' not found")


class WorkflowStepNotFoundError(WorkflowServiceError):
    """Exception raised when a workflow step is not found."""
    
    def __init__(self, step_id: str, workflow_id: str = None):
        """
        Initialize a workflow step not found error.
        
        Args:
            step_id: ID of the step that was not found
            workflow_id: Optional ID of the workflow
        """
        self.step_id = step_id
        self.workflow_id = workflow_id
        
        if workflow_id:
            message = f"Step '{step_id}' not found in workflow '{workflow_id}'"
        else:
            message = f"Step '{step_id}' not found"
            
        super().__init__(message)


class WorkflowValidationError(WorkflowServiceError):
    """Exception raised when a workflow validation fails."""
    
    def __init__(self, workflow_id: str, errors: list):
        """
        Initialize a workflow validation error.
        
        Args:
            workflow_id: ID of the workflow that failed validation
            errors: List of validation errors
        """
        self.workflow_id = workflow_id
        self.errors = errors
        
        message = f"Validation failed for workflow '{workflow_id}':\n" + "\n".join(f"- {error}" for error in errors)
        super().__init__(message)


class WorkflowExecutionError(WorkflowServiceError):
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
        
        full_message = f"Error executing workflow '{workflow_id}': {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
            
        super().__init__(full_message)


class WorkflowStepExecutionError(WorkflowServiceError):
    """Exception raised when a workflow step execution fails."""
    
    def __init__(self, step_id: str, workflow_id: str, message: str, cause: Exception = None):
        """
        Initialize a workflow step execution error.
        
        Args:
            step_id: ID of the step that failed execution
            workflow_id: ID of the workflow
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.step_id = step_id
        self.workflow_id = workflow_id
        self.cause = cause
        
        full_message = f"Error executing step '{step_id}' in workflow '{workflow_id}': {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
            
        super().__init__(full_message)


class WorkflowAlreadyExistsError(WorkflowServiceError):
    """Exception raised when a workflow already exists."""
    
    def __init__(self, workflow_id: str):
        """
        Initialize a workflow already exists error.
        
        Args:
            workflow_id: ID of the workflow that already exists
        """
        self.workflow_id = workflow_id
        super().__init__(f"Workflow '{workflow_id}' already exists")


class WorkflowRepositoryError(WorkflowServiceError):
    """Exception raised when there is an error with the workflow repository."""
    
    def __init__(self, message: str, cause: Exception = None):
        """
        Initialize a workflow repository error.
        
        Args:
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.cause = cause
        
        full_message = f"Workflow repository error: {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
            
        super().__init__(full_message)


class WorkflowSerializationError(WorkflowServiceError):
    """Exception raised when there is an error serializing a workflow."""
    
    def __init__(self, workflow_id: str, message: str, cause: Exception = None):
        """
        Initialize a workflow serialization error.
        
        Args:
            workflow_id: ID of the workflow that could not be serialized
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.workflow_id = workflow_id
        self.cause = cause
        
        full_message = f"Error serializing workflow '{workflow_id}': {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
            
        super().__init__(full_message)


class WorkflowDeserializationError(WorkflowServiceError):
    """Exception raised when there is an error deserializing a workflow."""
    
    def __init__(self, message: str, cause: Exception = None):
        """
        Initialize a workflow deserialization error.
        
        Args:
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.cause = cause
        
        full_message = f"Error deserializing workflow: {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
            
        super().__init__(full_message)


class WorkflowQueryError(WorkflowServiceError):
    """Exception raised when there is an error with a workflow query."""
    
    def __init__(self, message: str, query: dict = None):
        """
        Initialize a workflow query error.
        
        Args:
            message: Error message
            query: Optional query that caused the error
        """
        self.query = query
        
        if query:
            full_message = f"Query error: {message} (Query: {query})"
        else:
            full_message = f"Query error: {message}"
            
        super().__init__(full_message)
