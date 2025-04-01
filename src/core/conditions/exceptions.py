"""
Condition exceptions.

This module defines exceptions specific to condition operations,
providing more detailed error information than generic exceptions.
"""


class ConditionError(Exception):
    """Base class for all condition-related exceptions."""
    pass


class ConditionNotFoundError(ConditionError):
    """Exception raised when a condition is not found."""
    
    def __init__(self, condition_id: str):
        """
        Initialize a condition not found error.
        
        Args:
            condition_id: ID of the condition that was not found
        """
        self.condition_id = condition_id
        super().__init__(f"Condition '{condition_id}' not found")


class ConditionTypeNotFoundError(ConditionError):
    """Exception raised when a condition type is not found."""
    
    def __init__(self, condition_type: str):
        """
        Initialize a condition type not found error.
        
        Args:
            condition_type: Type of condition that was not found
        """
        self.condition_type = condition_type
        super().__init__(f"Condition type '{condition_type}' not found")


class ConditionValidationError(ConditionError):
    """Exception raised when a condition validation fails."""
    
    def __init__(self, condition_id: str, errors: list):
        """
        Initialize a condition validation error.
        
        Args:
            condition_id: ID of the condition that failed validation
            errors: List of validation errors
        """
        self.condition_id = condition_id
        self.errors = errors
        
        message = f"Validation failed for condition '{condition_id}':\n" + "\n".join(f"- {error}" for error in errors)
        super().__init__(message)


class ConditionEvaluationError(ConditionError):
    """Exception raised when a condition evaluation fails."""
    
    def __init__(self, condition_id: str, message: str, cause: Exception = None):
        """
        Initialize a condition evaluation error.
        
        Args:
            condition_id: ID of the condition that failed evaluation
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.condition_id = condition_id
        self.cause = cause
        
        full_message = f"Error evaluating condition '{condition_id}': {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
            
        super().__init__(full_message)


class ConditionProviderError(ConditionError):
    """Exception raised when there is an error with a condition provider."""
    
    def __init__(self, provider_id: str, message: str, cause: Exception = None):
        """
        Initialize a condition provider error.
        
        Args:
            provider_id: ID of the provider that encountered an error
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.provider_id = provider_id
        self.cause = cause
        
        full_message = f"Error in condition provider '{provider_id}': {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
            
        super().__init__(full_message)


class ConditionRegistryError(ConditionError):
    """Exception raised when there is an error with the condition registry."""
    
    def __init__(self, message: str, cause: Exception = None):
        """
        Initialize a condition registry error.
        
        Args:
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.cause = cause
        
        full_message = f"Condition registry error: {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
            
        super().__init__(full_message)


class ConditionResolverError(ConditionError):
    """Exception raised when there is an error resolving a condition."""
    
    def __init__(self, message: str, cause: Exception = None):
        """
        Initialize a condition resolver error.
        
        Args:
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.cause = cause
        
        full_message = f"Condition resolver error: {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
            
        super().__init__(full_message)


class ConditionFactoryError(ConditionError):
    """Exception raised when there is an error creating a condition."""
    
    def __init__(self, condition_type: str, message: str, cause: Exception = None):
        """
        Initialize a condition factory error.
        
        Args:
            condition_type: Type of condition that could not be created
            message: Error message
            cause: Optional underlying exception that caused the failure
        """
        self.condition_type = condition_type
        self.cause = cause
        
        full_message = f"Error creating condition of type '{condition_type}': {message}"
        if cause:
            full_message += f" (Caused by: {type(cause).__name__}: {str(cause)})"
            
        super().__init__(full_message)
