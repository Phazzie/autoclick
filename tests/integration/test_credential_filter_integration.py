"""Integration tests for the CredentialFilterAction"""
import unittest
from typing import Dict, Any, List

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.credential_filter_action import CredentialFilterAction
from src.core.credentials.credential_manager import CredentialManager, CredentialStatus
from src.core.workflow.workflow_engine import WorkflowEngine
from src.core.context.variable_storage import VariableStorage, VariableScope


class MockLoginAction(BaseAction):
    """Mock action that simulates a login attempt"""

    def __init__(
        self,
        description: str,
        username: str,
        password: str,
        success: bool,
        message: str,
        action_id: str = None,
    ):
        """Initialize the mock login action"""
        super().__init__(description, action_id)
        self.username = username
        self.password = password
        self.success = success
        self.message = message

    @property
    def type(self) -> str:
        """Get the action type"""
        return "mock_login"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        # Set variables directly in the context
        context["username"] = self.username
        context["password"] = self.password
        context["success"] = self.success
        context["message"] = self.message

        return ActionResult.create_success(
            f"Login {'succeeded' if self.success else 'failed'}: {self.message}",
            {
                "username": self.username,
                "success": self.success,
                "message": self.message,
            },
        )


class TestCredentialFilterIntegration(unittest.TestCase):
    """Integration tests for the CredentialFilterAction"""

    def setUp(self):
        """Set up test fixtures"""
        self.credential_manager = CredentialManager()
        self.workflow_engine = WorkflowEngine()
        self.variables = VariableStorage()

        # Add test credentials
        self.credential_manager.add_credential("user1", "pass1")
        self.credential_manager.add_credential("user2", "pass2")
        self.credential_manager.add_credential("user3", "pass3")

    def test_workflow_with_credential_filter(self):
        """Test a workflow that includes credential filtering"""
        # Create a workflow with login attempts and credential filtering
        workflow = [
            # Successful login
            MockLoginAction(
                description="Login with user1",
                username="user1",
                password="pass1",
                success=True,
                message="Login successful",
            ),
            CredentialFilterAction(
                description="Process successful login",
                credential_manager=self.credential_manager,
            ),
            # Failed login
            MockLoginAction(
                description="Login with user2",
                username="user2",
                password="wrong_password",
                success=False,
                message="Invalid password",
            ),
            CredentialFilterAction(
                description="Process failed login",
                credential_manager=self.credential_manager,
            ),
            # Locked account
            MockLoginAction(
                description="Login with user3",
                username="user3",
                password="pass3",
                success=False,
                message="Account locked",
            ),
            CredentialFilterAction(
                description="Process locked account",
                credential_manager=self.credential_manager,
                inactive_status=CredentialStatus.LOCKED,
            ),
        ]

        # Execute the workflow
        context = {}
        self.workflow_engine.execute_workflow(workflow, context)

        # Check the status of credentials
        user1 = self.credential_manager.get_credential("user1")
        user2 = self.credential_manager.get_credential("user2")
        user3 = self.credential_manager.get_credential("user3")

        self.assertEqual(user1.status, CredentialStatus.SUCCESS)
        self.assertEqual(user2.status, CredentialStatus.BLACKLISTED)
        self.assertEqual(user3.status, CredentialStatus.LOCKED)

        # Check attempt counts
        self.assertEqual(user1.attempts, 1)
        self.assertEqual(user2.attempts, 1)
        self.assertEqual(user3.attempts, 1)

        # Check statistics
        stats = self.credential_manager.get_statistics()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["status_counts"][CredentialStatus.SUCCESS.name], 1)
        self.assertEqual(stats["status_counts"][CredentialStatus.BLACKLISTED.name], 1)
        self.assertEqual(stats["status_counts"][CredentialStatus.LOCKED.name], 1)

    def test_multiple_login_attempts(self):
        """Test multiple login attempts with the same credentials"""
        # Create a workflow with multiple login attempts
        workflow = [
            # First attempt - success
            MockLoginAction(
                description="Login with user1 (success)",
                username="user1",
                password="pass1",
                success=True,
                message="Login successful",
            ),
            CredentialFilterAction(
                description="Process successful login",
                credential_manager=self.credential_manager,
            ),
            # Second attempt - failure
            MockLoginAction(
                description="Login with user1 (failure)",
                username="user1",
                password="wrong_password",
                success=False,
                message="Invalid password",
            ),
            CredentialFilterAction(
                description="Process failed login",
                credential_manager=self.credential_manager,
            ),
        ]

        # Execute the workflow
        context = {}
        self.workflow_engine.execute_workflow(workflow, context)

        # Check the status of the credential
        user1 = self.credential_manager.get_credential("user1")

        # The last status should be BLACKLISTED because the last attempt failed
        self.assertEqual(user1.status, CredentialStatus.BLACKLISTED)

        # Should have 2 attempts
        self.assertEqual(user1.attempts, 2)

        # Check the history
        self.assertEqual(len(user1.history), 2)
        self.assertTrue(user1.history[0]["success"])
        self.assertFalse(user1.history[1]["success"])


if __name__ == "__main__":
    unittest.main()
