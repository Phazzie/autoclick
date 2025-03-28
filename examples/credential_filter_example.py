"""Example of using the CredentialFilterAction"""
import logging
from typing import Dict, Any, List

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.credential_filter_action import CredentialFilterAction
from src.core.credentials.credential_manager import CredentialManager, CredentialStatus
from src.core.workflow.workflow_engine import WorkflowEngine
# No need for variable storage imports


class PrintAction(BaseAction):
    """Simple action for printing messages"""

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
        print(f"[PrintAction] {self.message}")
        return ActionResult.create_success(f"Printed message: {self.message}")


class DisplayCredentialsAction(BaseAction):
    """Action to display the current credentials and their statuses"""

    def __init__(self, description: str, credential_manager: CredentialManager, action_id: str = None):
        """Initialize the display credentials action"""
        super().__init__(description, action_id)
        self.credential_manager = credential_manager

    @property
    def type(self) -> str:
        """Get the action type"""
        return "display_credentials"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        # Get all credentials
        all_credentials = self.credential_manager.credentials.values()

        # Print header
        print("\n----- Current Credentials -----")
        print(f"{'Username':<15} {'Status':<15} {'Attempts':<10}")
        print("-" * 40)

        # Print each credential
        for cred in all_credentials:
            print(f"{cred.username:<15} {cred.status.name:<15} {cred.attempts:<10}")

        print("-" * 40)

        return ActionResult.create_success("Displayed credentials")


def create_workflow() -> List[BaseAction]:
    """Create a workflow that demonstrates credential filtering"""
    # Create a credential manager
    credential_manager = CredentialManager()

    # Add some test credentials
    credential_manager.add_credential("user1", "pass1")
    credential_manager.add_credential("user2", "pass2")
    credential_manager.add_credential("user3", "pass3")

    # Create a workflow
    return [
        PrintAction(
            description="Start workflow",
            message="Starting credential filter workflow..."
        ),

        DisplayCredentialsAction(
            description="Display initial credentials",
            credential_manager=credential_manager
        ),

        # Simulate a successful login
        PrintAction(
            description="Simulate successful login",
            message="Attempting login with user1..."
        ),
        CredentialFilterAction(
            description="Record successful login",
            credential_manager=credential_manager
        ),

        DisplayCredentialsAction(
            description="Display credentials after successful login",
            credential_manager=credential_manager
        ),

        # Simulate a failed login
        PrintAction(
            description="Simulate failed login",
            message="Attempting login with user2..."
        ),
        CredentialFilterAction(
            description="Record failed login and mark as inactive",
            credential_manager=credential_manager,
            inactive_status=CredentialStatus.BLACKLISTED
        ),

        DisplayCredentialsAction(
            description="Display credentials after failed login",
            credential_manager=credential_manager
        ),

        # Simulate a locked account
        PrintAction(
            description="Simulate locked account",
            message="Attempting login with user3..."
        ),
        CredentialFilterAction(
            description="Record locked account and mark as inactive",
            credential_manager=credential_manager,
            inactive_status=CredentialStatus.LOCKED
        ),

        DisplayCredentialsAction(
            description="Display credentials after locked account",
            credential_manager=credential_manager
        ),

        # Print final statistics
        PrintAction(
            description="End workflow",
            message="Credential filter workflow completed"
        )
    ]


def main():
    """Run the example"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create the workflow engine
    engine = WorkflowEngine()

    # Create the context with initial variables
    context = {
        "username": "user1",
        "success": True,
        "message": "Login successful"
    }

    # Create and run the workflow
    workflow = create_workflow()
    engine.execute_workflow(workflow, context)

    # Update context for the second credential
    context["username"] = "user2"
    context["success"] = False
    context["message"] = "Invalid password"

    # Run the workflow again
    engine.execute_workflow(workflow, context)

    # Update context for the third credential
    context["username"] = "user3"
    context["success"] = False
    context["message"] = "Account locked"

    # Run the workflow again
    engine.execute_workflow(workflow, context)


if __name__ == "__main__":
    main()
