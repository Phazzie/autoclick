"""Example demonstrating error handling features"""
import os
import sys
import random
from typing import Dict, Any, List, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.try_catch_action import TryCatchAction
from src.core.actions.retry_action_impl import RetryAction
from src.core.actions.set_variable_action import SetVariableAction
from src.core.error.error_types import ErrorContext, ErrorCategory, ErrorSeverity
from src.core.error.error_handler import ErrorHandler, ErrorHandlerFactory
from src.core.error.recovery_strategy import RetryStrategy, FallbackStrategy, SkipStrategy
from src.core.workflow.workflow_engine import WorkflowEngine


# Simple action for printing messages
class PrintAction(BaseAction):
    """Action that prints a message"""

    def __init__(self, description: str, message: str, action_id: str = None):
        """Initialize the print action"""
        super().__init__(description, action_id)
        self.message = message

    @property
    def type(self) -> str:
        """Get the action type"""
        return "print"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        # Print the message
        print(f"[PrintAction] {self.message}")
        return ActionResult.create_success(f"Printed message: {self.message}")


# Action that randomly fails
class RandomFailAction(BaseAction):
    """Action that randomly fails"""

    def __init__(
        self,
        description: str,
        failure_rate: float = 0.5,
        error_message: str = "Random failure occurred",
        error_category: ErrorCategory = ErrorCategory.UNKNOWN,
        action_id: str = None
    ):
        """Initialize the random fail action"""
        super().__init__(description, action_id)
        self.failure_rate = failure_rate
        self.error_message = error_message
        self.error_category = error_category

    @property
    def type(self) -> str:
        """Get the action type"""
        return "random_fail"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        # Randomly decide whether to fail
        if random.random() < self.failure_rate:
            print(f"[RandomFailAction] Failed: {self.error_message}")
            return ActionResult.create_failure(self.error_message)
        else:
            print(f"[RandomFailAction] Succeeded")
            return ActionResult.create_success("Action succeeded")


# Action that always fails
class AlwaysFailAction(BaseAction):
    """Action that always fails"""

    def __init__(
        self,
        description: str,
        error_message: str = "Action failed",
        error_category: ErrorCategory = ErrorCategory.UNKNOWN,
        action_id: str = None
    ):
        """Initialize the always fail action"""
        super().__init__(description, action_id)
        self.error_message = error_message
        self.error_category = error_category

    @property
    def type(self) -> str:
        """Get the action type"""
        return "always_fail"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        print(f"[AlwaysFailAction] Failed: {self.error_message}")
        return ActionResult.create_failure(self.error_message)


def create_try_catch_example() -> List[BaseAction]:
    """
    Create an example workflow with try-catch actions
    
    Returns:
        List of actions in the workflow
    """
    # Create a workflow with a try-catch action
    workflow = [
        PrintAction(
            description="Start workflow",
            message="Starting try-catch example workflow..."
        ),
        
        # Initialize variables
        SetVariableAction(
            description="Initialize error variable",
            variable_name="last_error",
            value=None
        ),
        
        # Try-catch action
        TryCatchAction(
            description="Try-catch example",
            try_actions=[
                PrintAction(
                    description="Before potential failure",
                    message="Executing action that might fail..."
                ),
                RandomFailAction(
                    description="Random failure",
                    failure_rate=0.8,
                    error_message="Simulated random failure",
                    error_category=ErrorCategory.EXECUTION
                ),
                PrintAction(
                    description="After potential failure",
                    message="This will only execute if the previous action succeeded"
                )
            ],
            catch_actions=[
                PrintAction(
                    description="Error handler",
                    message="An error occurred, handling it gracefully"
                ),
                SetVariableAction(
                    description="Set recovery flag",
                    variable_name="recovery_attempted",
                    value=True
                )
            ],
            finally_actions=[
                PrintAction(
                    description="Cleanup",
                    message="This will execute regardless of success or failure"
                )
            ],
            error_variable_name="last_error"
        ),
        
        # Check the error variable
        PrintAction(
            description="End workflow",
            message="Try-catch example workflow completed"
        )
    ]
    
    return workflow


def create_retry_example() -> List[BaseAction]:
    """
    Create an example workflow with retry actions
    
    Returns:
        List of actions in the workflow
    """
    # Create a workflow with a retry action
    workflow = [
        PrintAction(
            description="Start workflow",
            message="Starting retry example workflow..."
        ),
        
        # Initialize variables
        SetVariableAction(
            description="Initialize attempts variable",
            variable_name="attempts",
            value=0
        ),
        SetVariableAction(
            description="Initialize success variable",
            variable_name="success",
            value=False
        ),
        
        # Retry action
        RetryAction(
            description="Retry example",
            action=RandomFailAction(
                description="Random failure",
                failure_rate=0.7,
                error_message="Simulated random failure",
                error_category=ErrorCategory.EXECUTION
            ),
            max_retries=5,
            delay_seconds=0.5,
            backoff_factor=1.5,
            success_variable_name="success",
            attempts_variable_name="attempts"
        ),
        
        # Check the variables
        PrintAction(
            description="Show results",
            message="Retry example completed. Attempts: ${attempts}, Success: ${success}"
        ),
        
        # End workflow
        PrintAction(
            description="End workflow",
            message="Retry example workflow completed"
        )
    ]
    
    return workflow


def create_error_handler_example() -> None:
    """
    Create an example that demonstrates the ErrorHandler class
    """
    print("\n" + "=" * 60)
    print("Error Handler Example")
    print("=" * 60)
    
    # Create an error handler
    handler = ErrorHandler()
    
    # Add recovery strategies
    handler.add_strategy(RetryStrategy(max_retries=3, delay_seconds=0.5))
    handler.add_strategy(FallbackStrategy(fallback_value="Default Value"))
    handler.add_strategy(SkipStrategy())
    
    # Create some error contexts
    network_error = ErrorContext(
        message="Failed to connect to server",
        category=ErrorCategory.NETWORK,
        severity=ErrorSeverity.ERROR,
        context={"url": "https://example.com"}
    )
    
    validation_error = ErrorContext(
        message="Invalid input value",
        category=ErrorCategory.VALIDATION,
        severity=ErrorSeverity.WARNING,
        context={"field": "email", "value": "not-an-email"}
    )
    
    critical_error = ErrorContext(
        message="Database connection failed",
        category=ErrorCategory.DATABASE,
        severity=ErrorSeverity.CRITICAL,
        recoverable=False,
        context={"database": "users"}
    )
    
    # Handle the errors
    print("Handling network error...")
    network_result = handler.handle_error(network_error, {
        "args": [],
        "kwargs": {}
    })
    print(f"Result: {network_result.success}, Message: {network_result.message}")
    print()
    
    print("Handling validation error...")
    validation_result = handler.handle_error(validation_error, {})
    print(f"Result: {validation_result.success}, Message: {validation_result.message}")
    print()
    
    print("Handling critical error...")
    critical_result = handler.handle_error(critical_error, {})
    print(f"Result: {critical_result.success}, Message: {critical_result.message}")
    print()
    
    # Show error history
    print("Error History:")
    for i, error in enumerate(handler.get_error_history()):
        print(f"{i+1}. {error}")
    
    print("=" * 60)


def run_workflow(workflow: List[BaseAction], title: str) -> None:
    """
    Run a workflow with the workflow engine
    
    Args:
        workflow: List of actions to execute
        title: Title of the workflow
    """
    print("\n" + "=" * 60)
    print(f"Running {title}")
    print("=" * 60)
    
    # Create a workflow engine
    engine = WorkflowEngine()
    
    # Create an execution context
    context = {}
    
    # Execute the workflow
    result = engine.execute_workflow(workflow, context)
    
    # Print the result
    print(f"\nWorkflow result: {'Success' if result['success'] else 'Failure'}")
    print(f"Message: {result['message']}")
    
    # Print the context variables
    print("\nContext variables:")
    for key, value in context.items():
        if key != "variables" and not key.startswith("_"):
            print(f"  {key}: {value}")
    
    print("=" * 60)


def main() -> None:
    """Main function"""
    print("Error Handling Examples")
    print("======================")
    
    # Set a fixed seed for reproducible results
    random.seed(42)
    
    # Run the try-catch example
    try_catch_workflow = create_try_catch_example()
    run_workflow(try_catch_workflow, "Try-Catch Example")
    
    # Run the retry example
    retry_workflow = create_retry_example()
    run_workflow(retry_workflow, "Retry Example")
    
    # Run the error handler example
    create_error_handler_example()
    
    print("\nError handling examples completed successfully!")


if __name__ == "__main__":
    main()
