"""Try-catch action for error handling in workflows"""
from typing import Dict, Any, List, Optional
import logging

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.action_factory import ActionFactory
from src.core.error.error_types import ErrorContext, ErrorCategory, ErrorSeverity
from src.core.error.error_handler import ErrorHandler, ErrorHandlerFactory


@ActionFactory.register("try_catch")
class TryCatchAction(BaseAction):
    """
    Action that executes a sequence of actions with error handling
    
    This action is similar to a try-catch block in programming languages.
    It executes a sequence of "try" actions, and if any of them fail,
    it executes a sequence of "catch" actions.
    """
    
    def __init__(
        self,
        description: str,
        try_actions: List[BaseAction],
        catch_actions: List[BaseAction],
        finally_actions: Optional[List[BaseAction]] = None,
        error_variable_name: Optional[str] = None,
        action_id: Optional[str] = None
    ):
        """
        Initialize the try-catch action
        
        Args:
            description: Human-readable description of the action
            try_actions: Actions to execute in the "try" block
            catch_actions: Actions to execute if an error occurs
            finally_actions: Actions to execute regardless of success or failure
            error_variable_name: Name of the variable to store the error in
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.try_actions = try_actions
        self.catch_actions = catch_actions
        self.finally_actions = finally_actions or []
        self.error_variable_name = error_variable_name
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @property
    def type(self) -> str:
        """Get the action type"""
        return "try_catch"
        
    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action
        
        Args:
            context: Execution context containing variables, browser, etc.
            
        Returns:
            Result of the action execution
        """
        error_occurred = False
        error_context = None
        try_results = []
        catch_results = []
        finally_results = []
        
        # Execute the "try" actions
        for i, action in enumerate(self.try_actions):
            try:
                result = action.execute(context)
                try_results.append(result)
                
                if not result.success:
                    # Action failed, break out of the try block
                    error_occurred = True
                    error_context = ErrorContext(
                        message=f"Action {i+1} in try block failed: {result.message}",
                        category=ErrorCategory.EXECUTION,
                        severity=ErrorSeverity.ERROR,
                        context={"action_index": i, "action_type": action.type}
                    )
                    break
                    
            except Exception as e:
                # Unexpected exception, break out of the try block
                error_occurred = True
                error_context = ErrorContext.from_exception(
                    e,
                    category=ErrorCategory.EXECUTION,
                    severity=ErrorSeverity.ERROR,
                    context={"action_index": i, "action_type": action.type}
                )
                break
                
        # If an error occurred, store it in the context if requested
        if error_occurred and self.error_variable_name:
            if "variables" in context and hasattr(context["variables"], "set"):
                # Use the variables object if available
                context["variables"].set(self.error_variable_name, error_context.to_dict())
            else:
                # Otherwise, store directly in the context
                context[self.error_variable_name] = error_context.to_dict()
                
        # Execute the "catch" actions if an error occurred
        if error_occurred:
            self.logger.info(f"Error occurred in try block, executing catch actions: {error_context}")
            
            for i, action in enumerate(self.catch_actions):
                try:
                    result = action.execute(context)
                    catch_results.append(result)
                    
                    if not result.success:
                        self.logger.warning(
                            f"Action {i+1} in catch block failed: {result.message}"
                        )
                        
                except Exception as e:
                    self.logger.error(
                        f"Unexpected error in catch block: {str(e)}",
                        exc_info=True
                    )
                    
        # Execute the "finally" actions regardless of success or failure
        for i, action in enumerate(self.finally_actions):
            try:
                result = action.execute(context)
                finally_results.append(result)
                
                if not result.success:
                    self.logger.warning(
                        f"Action {i+1} in finally block failed: {result.message}"
                    )
                    
            except Exception as e:
                self.logger.error(
                    f"Unexpected error in finally block: {str(e)}",
                    exc_info=True
                )
                
        # Determine the overall success of the action
        if error_occurred:
            # If all catch actions succeeded, consider the action successful
            catch_success = all(result.success for result in catch_results) if catch_results else True
            
            if catch_success:
                return ActionResult.create_success(
                    "Error occurred but was handled successfully",
                    {
                        "error": error_context.to_dict() if error_context else None,
                        "try_results": try_results,
                        "catch_results": catch_results,
                        "finally_results": finally_results
                    }
                )
            else:
                return ActionResult.create_failure(
                    "Error occurred and catch actions failed",
                    {
                        "error": error_context.to_dict() if error_context else None,
                        "try_results": try_results,
                        "catch_results": catch_results,
                        "finally_results": finally_results
                    }
                )
        else:
            # No error occurred, action is successful
            return ActionResult.create_success(
                "Try block executed successfully",
                {
                    "try_results": try_results,
                    "finally_results": finally_results
                }
            )
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data.update({
            "try_actions": [action.to_dict() for action in self.try_actions],
            "catch_actions": [action.to_dict() for action in self.catch_actions],
            "finally_actions": [action.to_dict() for action in self.finally_actions],
            "error_variable_name": self.error_variable_name
        })
        return data
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TryCatchAction':
        """
        Create a try-catch action from a dictionary
        
        Args:
            data: Dictionary representation of the action
            
        Returns:
            Instantiated action
        """
        from src.core.actions.action_factory import ActionFactory
        
        action_factory = ActionFactory.get_instance()
        
        # Create the try actions
        try_actions_data = data.get("try_actions", [])
        try_actions = [
            action_factory.create_action(action_data)
            for action_data in try_actions_data
        ]
        
        # Create the catch actions
        catch_actions_data = data.get("catch_actions", [])
        catch_actions = [
            action_factory.create_action(action_data)
            for action_data in catch_actions_data
        ]
        
        # Create the finally actions
        finally_actions_data = data.get("finally_actions", [])
        finally_actions = [
            action_factory.create_action(action_data)
            for action_data in finally_actions_data
        ]
        
        # Create the try-catch action
        return cls(
            description=data.get("description", ""),
            try_actions=try_actions,
            catch_actions=catch_actions,
            finally_actions=finally_actions,
            error_variable_name=data.get("error_variable_name"),
            action_id=data.get("id")
        )
