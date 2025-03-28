"""Action for filtering credentials based on login results"""
from typing import Any, Dict, Optional, Set

from src.core.actions.action_factory import ActionFactory
from src.core.actions.action_interface import ActionResult
from src.core.actions.base_action import BaseAction
from src.core.credentials.credential_manager import (CredentialManager,
                                                     CredentialStatus)


@ActionFactory.register("credential_filter")
class CredentialFilterAction(BaseAction):
    """
    Action that filters credentials based on login results

    This action works with the CredentialManager to identify failed login credentials
    and mark them as inactive rather than removing them.
    """

    def __init__(
        self,
        description: str,
        credential_manager: CredentialManager,
        username_variable: str = "username",
        success_variable: str = "success",
        message_variable: str = "message",
        inactive_status: CredentialStatus = CredentialStatus.BLACKLISTED,
        action_id: Optional[str] = None,
    ):
        """
        Initialize the credential filter action

        Args:
            description: Human-readable description of the action
            credential_manager: Credential manager to use
            username_variable: Name of the variable containing the username
            success_variable: Name of the variable containing the success flag
            message_variable: Name of the variable containing the result message
            inactive_status: Status to set for inactive credentials
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.credential_manager = credential_manager
        self.username_variable = username_variable
        self.success_variable = success_variable
        self.message_variable = message_variable
        self.inactive_status = inactive_status

    @property
    def type(self) -> str:
        """Get the action type"""
        return "credential_filter"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the action execution
        """
        # Get the variables from the context
        username = self._get_variable(context, self.username_variable)
        success = self._get_variable(context, self.success_variable)
        message = self._get_variable(
            context, self.message_variable, "No message provided"
        )

        # Check if the username is present
        if not username:
            return ActionResult.create_failure(
                f"Missing required variable: {self.username_variable}"
            )

        # Record the attempt if success status is available
        if success is not None:
            status = CredentialStatus.SUCCESS if success else CredentialStatus.FAILURE
            self.credential_manager.record_attempt(username, success, message, status)

        # Move failed credentials to inactive status
        updated_count = self.credential_manager.update_credentials_status(
            from_status=CredentialStatus.FAILURE, to_status=self.inactive_status
        )

        # Get statistics
        stats = self.credential_manager.get_statistics()

        # Return the result
        return ActionResult.create_success(
            f"Marked {updated_count} failed credentials as {self.inactive_status.name}",
            {"updated_count": updated_count, "statistics": stats},
        )

    def _get_variable(
        self, context: Dict[str, Any], variable_name: str, default: Any = None
    ) -> Any:
        """Get a variable from the context"""
        if "variables" in context and hasattr(context["variables"], "get"):
            return context["variables"].get(variable_name, default)
        return context.get(variable_name, default)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data.update(
            {
                "username_variable": self.username_variable,
                "success_variable": self.success_variable,
                "message_variable": self.message_variable,
                "inactive_status": self.inactive_status.name,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CredentialFilterAction":
        """Create a credential filter action from a dictionary"""
        # Parse inactive status
        inactive_status_name = data.get("inactive_status", "BLACKLISTED")
        inactive_status = (
            CredentialStatus[inactive_status_name]
            if inactive_status_name in CredentialStatus.__members__
            else CredentialStatus.BLACKLISTED
        )

        return cls(
            description=data.get("description", ""),
            credential_manager=CredentialManager(),
            username_variable=data.get("username_variable", "username"),
            success_variable=data.get("success_variable", "success"),
            message_variable=data.get("message_variable", "message"),
            inactive_status=inactive_status,
            action_id=data.get("id"),
        )
