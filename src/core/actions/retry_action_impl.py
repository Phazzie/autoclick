"""Retry action for automatically retrying failed actions"""
from typing import Dict, Any, List, Optional
import logging
import time

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.action_factory import ActionFactory
from src.core.error.error_types import ErrorContext, ErrorCategory, ErrorSeverity


@ActionFactory.register("retry")
class RetryAction(BaseAction):
    """
    Action that retries another action multiple times until it succeeds
    
    This action wraps another action and retries it a specified number
    of times if it fails, with an optional delay between retries.
    """
    
    def __init__(
        self,
        description: str,
        action: BaseAction,
        max_retries: int = 3,
        delay_seconds: float = 1.0,
        backoff_factor: float = 2.0,
        success_variable_name: Optional[str] = None,
        attempts_variable_name: Optional[str] = None,
        action_id: Optional[str] = None
    ):
        """
        Initialize the retry action
        
        Args:
            description: Human-readable description of the action
            action: The action to retry
            max_retries: Maximum number of retry attempts
            delay_seconds: Delay between retries in seconds
            backoff_factor: Factor to increase delay by after each retry
            success_variable_name: Name of the variable to store success status in
            attempts_variable_name: Name of the variable to store attempt count in
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.action = action
        self.max_retries = max_retries
        self.delay_seconds = delay_seconds
        self.backoff_factor = backoff_factor
        self.success_variable_name = success_variable_name
        self.attempts_variable_name = attempts_variable_name
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @property
    def type(self) -> str:
        """Get the action type"""
        return "retry"
        
    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action
        
        Args:
            context: Execution context containing variables, browser, etc.
            
        Returns:
            Result of the action execution
        """
        current_delay = self.delay_seconds
        last_result = None
        success = False
        
        # Try to execute the action with retries
        for attempt in range(self.max_retries + 1):  # +1 for the initial attempt
            # Update the attempts variable if specified
            if self.attempts_variable_name:
                if "variables" in context and hasattr(context["variables"], "set"):
                    context["variables"].set(self.attempts_variable_name, attempt + 1)
                else:
                    context[self.attempts_variable_name] = attempt + 1
                    
            # Wait before retrying (except for the first attempt)
            if attempt > 0:
                self.logger.info(
                    f"Retrying action (attempt {attempt+1}/{self.max_retries+1}) "
                    f"after {current_delay:.2f}s delay"
                )
                time.sleep(current_delay)
                current_delay *= self.backoff_factor
                
            try:
                # Execute the action
                result = self.action.execute(context)
                last_result = result
                
                # If the action succeeded, we're done
                if result.success:
                    success = True
                    break
                    
                self.logger.warning(
                    f"Action failed (attempt {attempt+1}/{self.max_retries+1}): {result.message}"
                )
                
            except Exception as e:
                self.logger.error(
                    f"Unexpected error (attempt {attempt+1}/{self.max_retries+1}): {str(e)}",
                    exc_info=True
                )
                
                # Create a failure result for the exception
                last_result = ActionResult.create_failure(
                    f"Exception occurred: {str(e)}",
                    {"exception": str(e)}
                )
                
        # Update the success variable if specified
        if self.success_variable_name:
            if "variables" in context and hasattr(context["variables"], "set"):
                context["variables"].set(self.success_variable_name, success)
            else:
                context[self.success_variable_name] = success
                
        # Return the final result
        if success:
            return ActionResult.create_success(
                f"Action succeeded after {attempt+1} attempts",
                {
                    "attempts": attempt+1,
                    "action_result": last_result.data if last_result else None
                }
            )
        else:
            return ActionResult.create_failure(
                f"Action failed after {self.max_retries+1} attempts",
                {
                    "attempts": attempt+1,
                    "action_result": last_result.data if last_result else None,
                    "last_error": last_result.message if last_result else "Unknown error"
                }
            )
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data.update({
            "action": self.action.to_dict(),
            "max_retries": self.max_retries,
            "delay_seconds": self.delay_seconds,
            "backoff_factor": self.backoff_factor,
            "success_variable_name": self.success_variable_name,
            "attempts_variable_name": self.attempts_variable_name
        })
        return data
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RetryAction':
        """
        Create a retry action from a dictionary
        
        Args:
            data: Dictionary representation of the action
            
        Returns:
            Instantiated action
        """
        from src.core.actions.action_factory import ActionFactory
        
        action_factory = ActionFactory.get_instance()
        
        # Create the action to retry
        action_data = data.get("action", {})
        action = action_factory.create_action(action_data)
        
        # Create the retry action
        return cls(
            description=data.get("description", ""),
            action=action,
            max_retries=data.get("max_retries", 3),
            delay_seconds=data.get("delay_seconds", 1.0),
            backoff_factor=data.get("backoff_factor", 2.0),
            success_variable_name=data.get("success_variable_name"),
            attempts_variable_name=data.get("attempts_variable_name"),
            action_id=data.get("id")
        )
