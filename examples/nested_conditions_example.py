"""Example demonstrating nested conditional actions"""
import os
import sys
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.if_then_else_action import IfThenElseAction
from src.core.actions.switch_case_action import SwitchCaseAction, CaseBranch
from src.core.actions.set_variable_action import SetVariableAction
from src.core.conditions.comparison_condition import ComparisonCondition, ComparisonOperator
from src.core.conditions.composite_conditions import AndCondition, OrCondition, NotCondition
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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data["message"] = self.message
        return data


def create_nested_conditions_workflow() -> List[BaseAction]:
    """
    Create a workflow with nested conditional actions
    
    This example demonstrates a complex user registration flow with
    multiple nested conditions for validation and different paths.
    
    Returns:
        List of actions in the workflow
    """
    # Create the main workflow
    workflow = [
        # Initialize variables
        SetVariableAction(
            description="Initialize username",
            variable_name="username",
            value="john_doe"
        ),
        SetVariableAction(
            description="Initialize email",
            variable_name="email",
            value="john@example.com"
        ),
        SetVariableAction(
            description="Initialize age",
            variable_name="age",
            value=25
        ),
        SetVariableAction(
            description="Initialize country",
            variable_name="country",
            value="US"
        ),
        PrintAction(
            description="Start registration workflow",
            message="Starting user registration workflow..."
        ),
        
        # First level condition: Check if username is valid
        IfThenElseAction(
            description="Validate username",
            condition=ComparisonCondition(
                left_value="${username}",
                operator=ComparisonOperator.NOT_EQUALS,
                right_value="",
                description="Check if username is not empty"
            ),
            then_actions=[
                PrintAction(
                    description="Username valid",
                    message="Username '${username}' is valid."
                ),
                
                # Second level condition: Check if email is valid
                IfThenElseAction(
                    description="Validate email",
                    condition=AndCondition(
                        ComparisonCondition(
                            left_value="${email}",
                            operator=ComparisonOperator.NOT_EQUALS,
                            right_value="",
                            description="Check if email is not empty"
                        ),
                        ComparisonCondition(
                            left_value="${email}",
                            operator=ComparisonOperator.CONTAINS,
                            right_value="@",
                            description="Check if email contains @"
                        ),
                        description="Check if email is valid"
                    ),
                    then_actions=[
                        PrintAction(
                            description="Email valid",
                            message="Email '${email}' is valid."
                        ),
                        
                        # Third level condition: Check age requirements
                        SwitchCaseAction(
                            description="Validate age requirements",
                            cases=[
                                # Case 1: Age < 18
                                CaseBranch(
                                    condition=ComparisonCondition(
                                        left_value="${age}",
                                        operator=ComparisonOperator.LESS_THAN,
                                        right_value=18,
                                        description="Check if user is under 18"
                                    ),
                                    actions=[
                                        PrintAction(
                                            description="Under 18",
                                            message="Sorry, you must be 18 or older to register."
                                        ),
                                        SetVariableAction(
                                            description="Set registration status",
                                            variable_name="registration_status",
                                            value="rejected_age"
                                        )
                                    ],
                                    description="Under 18 Case"
                                ),
                                
                                # Case 2: Age between 18 and 65
                                CaseBranch(
                                    condition=AndCondition(
                                        ComparisonCondition(
                                            left_value="${age}",
                                            operator=ComparisonOperator.GREATER_THAN_OR_EQUAL,
                                            right_value=18,
                                            description="Check if user is 18 or older"
                                        ),
                                        ComparisonCondition(
                                            left_value="${age}",
                                            operator=ComparisonOperator.LESS_THAN,
                                            right_value=65,
                                            description="Check if user is under 65"
                                        ),
                                        description="Check if user is between 18 and 65"
                                    ),
                                    actions=[
                                        PrintAction(
                                            description="Standard registration",
                                            message="You qualify for standard registration."
                                        ),
                                        
                                        # Fourth level condition: Check country for terms
                                        IfThenElseAction(
                                            description="Check country-specific terms",
                                            condition=OrCondition(
                                                ComparisonCondition(
                                                    left_value="${country}",
                                                    operator=ComparisonOperator.EQUALS,
                                                    right_value="US",
                                                    description="Check if user is from US"
                                                ),
                                                ComparisonCondition(
                                                    left_value="${country}",
                                                    operator=ComparisonOperator.EQUALS,
                                                    right_value="CA",
                                                    description="Check if user is from Canada"
                                                ),
                                                description="Check if user is from US or Canada"
                                            ),
                                            then_actions=[
                                                PrintAction(
                                                    description="North America terms",
                                                    message="Showing North American terms and conditions."
                                                ),
                                                SetVariableAction(
                                                    description="Set terms version",
                                                    variable_name="terms_version",
                                                    value="north_america_v2"
                                                )
                                            ],
                                            else_actions=[
                                                PrintAction(
                                                    description="International terms",
                                                    message="Showing international terms and conditions."
                                                ),
                                                SetVariableAction(
                                                    description="Set terms version",
                                                    variable_name="terms_version",
                                                    value="international_v3"
                                                )
                                            ]
                                        ),
                                        
                                        SetVariableAction(
                                            description="Set registration status",
                                            variable_name="registration_status",
                                            value="approved_standard"
                                        )
                                    ],
                                    description="Standard Registration Case"
                                ),
                                
                                # Case 3: Age 65 or older
                                CaseBranch(
                                    condition=ComparisonCondition(
                                        left_value="${age}",
                                        operator=ComparisonOperator.GREATER_THAN_OR_EQUAL,
                                        right_value=65,
                                        description="Check if user is 65 or older"
                                    ),
                                    actions=[
                                        PrintAction(
                                            description="Senior registration",
                                            message="You qualify for senior registration with special benefits."
                                        ),
                                        SetVariableAction(
                                            description="Set registration status",
                                            variable_name="registration_status",
                                            value="approved_senior"
                                        )
                                    ],
                                    description="Senior Registration Case"
                                )
                            ],
                            default_actions=[
                                PrintAction(
                                    description="Invalid age",
                                    message="Invalid age value: ${age}"
                                ),
                                SetVariableAction(
                                    description="Set registration status",
                                    variable_name="registration_status",
                                    value="error_invalid_age"
                                )
                            ]
                        )
                    ],
                    else_actions=[
                        PrintAction(
                            description="Invalid email",
                            message="Email '${email}' is not valid. Please provide a valid email address."
                        ),
                        SetVariableAction(
                            description="Set registration status",
                            variable_name="registration_status",
                            value="error_invalid_email"
                        )
                    ]
                )
            ],
            else_actions=[
                PrintAction(
                    description="Invalid username",
                    message="Username cannot be empty. Please provide a valid username."
                ),
                SetVariableAction(
                    description="Set registration status",
                    variable_name="registration_status",
                    value="error_invalid_username"
                )
            ]
        ),
        
        # Final step: Show registration result
        PrintAction(
            description="Show registration result",
            message="Registration process completed with status: ${registration_status}"
        ),
        
        # Conditional message based on registration status
        IfThenElseAction(
            description="Show final message",
            condition=OrCondition(
                ComparisonCondition(
                    left_value="${registration_status}",
                    operator=ComparisonOperator.EQUALS,
                    right_value="approved_standard",
                    description="Check if standard registration was approved"
                ),
                ComparisonCondition(
                    left_value="${registration_status}",
                    operator=ComparisonOperator.EQUALS,
                    right_value="approved_senior",
                    description="Check if senior registration was approved"
                ),
                description="Check if registration was approved"
            ),
            then_actions=[
                PrintAction(
                    description="Success message",
                    message="Congratulations, ${username}! Your registration was successful."
                ),
                PrintAction(
                    description="Next steps",
                    message="Please check your email at ${email} for confirmation."
                )
            ],
            else_actions=[
                PrintAction(
                    description="Failure message",
                    message="Sorry, we couldn't complete your registration. Please correct the errors and try again."
                )
            ]
        )
    ]
    
    return workflow


def run_workflow_with_different_inputs() -> None:
    """Run the nested conditions workflow with different inputs"""
    # Create the workflow
    workflow = create_nested_conditions_workflow()
    
    # Create a workflow engine
    engine = WorkflowEngine()
    
    # Test cases with different inputs
    test_cases = [
        {
            "name": "Valid Adult US User",
            "inputs": {
                "username": "john_doe",
                "email": "john@example.com",
                "age": 30,
                "country": "US"
            }
        },
        {
            "name": "Valid Senior International User",
            "inputs": {
                "username": "elder_smith",
                "email": "smith@example.co.uk",
                "age": 70,
                "country": "UK"
            }
        },
        {
            "name": "Underage User",
            "inputs": {
                "username": "young_user",
                "email": "young@example.com",
                "age": 16,
                "country": "CA"
            }
        },
        {
            "name": "Invalid Email",
            "inputs": {
                "username": "bad_email_user",
                "email": "not-an-email",
                "age": 25,
                "country": "US"
            }
        },
        {
            "name": "Empty Username",
            "inputs": {
                "username": "",
                "email": "nobody@example.com",
                "age": 40,
                "country": "FR"
            }
        }
    ]
    
    # Run each test case
    for test_case in test_cases:
        print(f"\n{'=' * 60}")
        print(f"Running test case: {test_case['name']}")
        print(f"{'=' * 60}")
        print(f"Inputs: {test_case['inputs']}")
        print(f"{'-' * 60}")
        
        # Create a context with the test inputs
        context = test_case["inputs"].copy()
        
        # Execute the workflow
        result = engine.execute_workflow(workflow, context)
        
        # Print the result
        print(f"{'-' * 60}")
        print(f"Workflow result: {'Success' if result['success'] else 'Failure'}")
        print(f"Final status: {context.get('registration_status', 'unknown')}")
        print(f"{'=' * 60}\n")


def main() -> None:
    """Main function"""
    print("Nested Conditional Actions Example")
    print("=================================")
    
    run_workflow_with_different_inputs()
    
    print("Nested conditional actions example completed successfully!")


if __name__ == "__main__":
    main()
