"""Example demonstrating data-driven testing features"""
import os
import sys
import csv
import json
from typing import Dict, Any, List, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.data_driven_action import DataDrivenAction
from src.core.actions.set_variable_action import SetVariableAction
from src.core.data.sources.base import DataSourceFactory
from src.core.data.mapping.variable_mapper import VariableMapper
from src.core.data.mapping.mapper import FieldMapping
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
        # Process variable expressions in the message
        processed_message = self.message
        if isinstance(self.message, str) and "${" in self.message and "}" in self.message:
            from src.core.expressions.expression_parser import parse_expression
            processed_message = parse_expression(self.message, context)
            
        # Print the message
        print(f"[PrintAction] {processed_message}")
        return ActionResult.create_success(f"Printed message: {processed_message}")


# Action that validates a value
class ValidateAction(BaseAction):
    """Action that validates a value"""

    def __init__(
        self,
        description: str,
        variable_name: str,
        validation_function: callable,
        error_message: str = "Validation failed",
        action_id: str = None
    ):
        """Initialize the validate action"""
        super().__init__(description, action_id)
        self.variable_name = variable_name
        self.validation_function = validation_function
        self.error_message = error_message

    @property
    def type(self) -> str:
        """Get the action type"""
        return "validate"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        # Get the value to validate
        value = context.get(self.variable_name)
        
        # Validate the value
        if self.validation_function(value):
            return ActionResult.create_success(f"Validation passed for {self.variable_name}")
        else:
            return ActionResult.create_failure(
                f"{self.error_message}: {self.variable_name}={value}"
            )


def create_csv_data_file(file_path: str) -> None:
    """
    Create a CSV data file for testing
    
    Args:
        file_path: Path to the CSV file to create
    """
    # Create the data
    data = [
        ["username", "password", "expected_result"],
        ["user1", "pass1", "success"],
        ["user2", "pass2", "success"],
        ["user3", "wrong", "failure"],
        ["", "pass4", "failure"],
        ["user5", "", "failure"]
    ]
    
    # Write the data to the file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        
    print(f"Created CSV data file: {file_path}")


def create_json_data_file(file_path: str) -> None:
    """
    Create a JSON data file for testing
    
    Args:
        file_path: Path to the JSON file to create
    """
    # Create the data
    data = {
        "test_data": {
            "login_tests": [
                {"username": "user1", "password": "pass1", "expected_result": "success"},
                {"username": "user2", "password": "pass2", "expected_result": "success"},
                {"username": "user3", "password": "wrong", "expected_result": "failure"},
                {"username": "", "password": "pass4", "expected_result": "failure"},
                {"username": "user5", "password": "", "expected_result": "failure"}
            ]
        }
    }
    
    # Write the data to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
        
    print(f"Created JSON data file: {file_path}")


def create_csv_data_driven_workflow() -> List[BaseAction]:
    """
    Create a workflow that uses a CSV data source
    
    Returns:
        List of actions in the workflow
    """
    # Create a CSV file
    csv_file = os.path.join(os.path.dirname(__file__), "login_data.csv")
    create_csv_data_file(csv_file)
    
    # Create a data source
    data_source = DataSourceFactory.create_csv_source(csv_file)
    
    # Create a data mapper
    data_mapper = VariableMapper()
    data_mapper.add_simple_mapping("username")
    data_mapper.add_simple_mapping("password")
    data_mapper.add_simple_mapping("expected_result")
    
    # Create actions to execute for each record
    actions = [
        PrintAction(
            description="Print login attempt",
            message="Attempting login with username=${username} and password=${password}"
        ),
        ValidateAction(
            description="Validate username",
            variable_name="username",
            validation_function=lambda x: x and len(x) > 0,
            error_message="Username cannot be empty"
        ),
        ValidateAction(
            description="Validate password",
            variable_name="password",
            validation_function=lambda x: x and len(x) > 0,
            error_message="Password cannot be empty"
        ),
        PrintAction(
            description="Print login result",
            message="Login ${expected_result == 'success' and 'succeeded' or 'failed'}"
        )
    ]
    
    # Create a data-driven action
    data_driven_action = DataDrivenAction(
        description="Login tests",
        data_source=data_source,
        actions=actions,
        data_mapper=data_mapper,
        continue_on_error=True,
        results_variable_name="login_results"
    )
    
    # Create the main workflow
    workflow = [
        PrintAction(
            description="Start workflow",
            message="Starting CSV data-driven workflow..."
        ),
        data_driven_action,
        PrintAction(
            description="End workflow",
            message="CSV data-driven workflow completed"
        )
    ]
    
    return workflow


def create_json_data_driven_workflow() -> List[BaseAction]:
    """
    Create a workflow that uses a JSON data source
    
    Returns:
        List of actions in the workflow
    """
    # Create a JSON file
    json_file = os.path.join(os.path.dirname(__file__), "login_data.json")
    create_json_data_file(json_file)
    
    # Create a data source
    data_source = DataSourceFactory.create_json_source(json_file, "test_data.login_tests")
    
    # Create a data mapper
    data_mapper = VariableMapper()
    data_mapper.add_simple_mapping("username")
    data_mapper.add_simple_mapping("password")
    data_mapper.add_simple_mapping("expected_result")
    
    # Create a transform function for the expected result
    def transform_expected_result(value: str) -> bool:
        return value == "success"
    
    # Add a mapping with a transform function
    data_mapper.add_mapping(
        FieldMapping(
            field_name="expected_result",
            variable_name="should_succeed",
            transform_function=transform_expected_result
        )
    )
    
    # Create actions to execute for each record
    actions = [
        PrintAction(
            description="Print login attempt",
            message="Attempting login with username=${username} and password=${password}"
        ),
        ValidateAction(
            description="Validate username",
            variable_name="username",
            validation_function=lambda x: x and len(x) > 0,
            error_message="Username cannot be empty"
        ),
        ValidateAction(
            description="Validate password",
            variable_name="password",
            validation_function=lambda x: x and len(x) > 0,
            error_message="Password cannot be empty"
        ),
        PrintAction(
            description="Print login result",
            message="Login ${should_succeed and 'should succeed' or 'should fail'}"
        )
    ]
    
    # Create a data-driven action
    data_driven_action = DataDrivenAction(
        description="Login tests",
        data_source=data_source,
        actions=actions,
        data_mapper=data_mapper,
        continue_on_error=True,
        results_variable_name="login_results"
    )
    
    # Create the main workflow
    workflow = [
        PrintAction(
            description="Start workflow",
            message="Starting JSON data-driven workflow..."
        ),
        data_driven_action,
        PrintAction(
            description="End workflow",
            message="JSON data-driven workflow completed"
        )
    ]
    
    return workflow


def create_memory_data_driven_workflow() -> List[BaseAction]:
    """
    Create a workflow that uses an in-memory data source
    
    Returns:
        List of actions in the workflow
    """
    # Create in-memory data
    data = [
        {"username": "user1", "password": "pass1", "expected_result": "success"},
        {"username": "user2", "password": "pass2", "expected_result": "success"},
        {"username": "user3", "password": "wrong", "expected_result": "failure"},
        {"username": "", "password": "pass4", "expected_result": "failure"},
        {"username": "user5", "password": "", "expected_result": "failure"}
    ]
    
    # Create a data source
    data_source = DataSourceFactory.create_memory_source(data)
    
    # Create a data mapper
    data_mapper = VariableMapper()
    data_mapper.add_simple_mapping("username")
    data_mapper.add_simple_mapping("password")
    data_mapper.add_simple_mapping("expected_result")
    
    # Create actions to execute for each record
    actions = [
        PrintAction(
            description="Print login attempt",
            message="Attempting login with username=${username} and password=${password}"
        ),
        ValidateAction(
            description="Validate username",
            variable_name="username",
            validation_function=lambda x: x and len(x) > 0,
            error_message="Username cannot be empty"
        ),
        ValidateAction(
            description="Validate password",
            variable_name="password",
            validation_function=lambda x: x and len(x) > 0,
            error_message="Password cannot be empty"
        ),
        PrintAction(
            description="Print login result",
            message="Login ${expected_result == 'success' and 'succeeded' or 'failed'}"
        )
    ]
    
    # Create a data-driven action
    data_driven_action = DataDrivenAction(
        description="Login tests",
        data_source=data_source,
        actions=actions,
        data_mapper=data_mapper,
        continue_on_error=True,
        results_variable_name="login_results"
    )
    
    # Create the main workflow
    workflow = [
        PrintAction(
            description="Start workflow",
            message="Starting in-memory data-driven workflow..."
        ),
        data_driven_action,
        PrintAction(
            description="End workflow",
            message="In-memory data-driven workflow completed"
        )
    ]
    
    return workflow


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
    
    # Print the results if available
    if "login_results" in context:
        login_results = context["login_results"]
        summary = login_results.get_summary()
        
        print("\nTest Results Summary:")
        print(f"Total tests: {summary['total']}")
        print(f"Successful tests: {summary['success']}")
        print(f"Failed tests: {summary['error']}")
        print(f"Success rate: {summary['success_rate'] * 100:.1f}%")
        
        print("\nFailed Tests:")
        for result in login_results.get_failed_results():
            print(f"  Record {result.record_index}: {result.message}")
    
    print("=" * 60)


def main() -> None:
    """Main function"""
    print("Data-Driven Testing Examples")
    print("===========================")
    
    # Run the CSV data-driven workflow
    csv_workflow = create_csv_data_driven_workflow()
    run_workflow(csv_workflow, "CSV Data-Driven Workflow")
    
    # Run the JSON data-driven workflow
    json_workflow = create_json_data_driven_workflow()
    run_workflow(json_workflow, "JSON Data-Driven Workflow")
    
    # Run the in-memory data-driven workflow
    memory_workflow = create_memory_data_driven_workflow()
    run_workflow(memory_workflow, "In-Memory Data-Driven Workflow")
    
    print("\nData-driven testing examples completed successfully!")


if __name__ == "__main__":
    main()
