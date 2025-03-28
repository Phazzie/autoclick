"""Tests for the CredentialFilterAction class"""
import unittest
from unittest.mock import MagicMock, patch

from src.core.actions.credential_filter_action import CredentialFilterAction
from src.core.actions.action_interface import ActionResult
from src.core.credentials.credential_manager import CredentialManager, CredentialStatus


class TestCredentialFilterAction(unittest.TestCase):
    """Test cases for the CredentialFilterAction class"""

    def setUp(self):
        """Set up test fixtures"""
        self.credential_manager = MagicMock(spec=CredentialManager)
        self.action = CredentialFilterAction(
            description="Test credential filter",
            credential_manager=self.credential_manager
        )

    def test_initialization(self):
        """Test initialization of the action"""
        # Assert default values
        self.assertEqual(self.action.username_variable, "username")
        self.assertEqual(self.action.success_variable, "success")
        self.assertEqual(self.action.message_variable, "message")
        self.assertEqual(self.action.inactive_status, CredentialStatus.BLACKLISTED)

        # Test with custom values
        custom_action = CredentialFilterAction(
            description="Custom filter",
            credential_manager=self.credential_manager,
            username_variable="user",
            success_variable="login_success",
            message_variable="login_message",
            inactive_status=CredentialStatus.EXPIRED,
            action_id="custom-id"
        )

        self.assertEqual(custom_action.username_variable, "user")
        self.assertEqual(custom_action.success_variable, "login_success")
        self.assertEqual(custom_action.message_variable, "login_message")
        self.assertEqual(custom_action.inactive_status, CredentialStatus.EXPIRED)
        self.assertEqual(custom_action.id, "custom-id")

    def test_execute_with_missing_username(self):
        """Test execution with missing username"""
        # Arrange
        context = {"variables": MagicMock()}
        context["variables"].get.return_value = None

        # Act
        result = self.action.execute(context)

        # Assert
        self.assertFalse(result.success)
        self.assertIn("Missing required variable", result.message)

    def test_execute_with_success_status(self):
        """Test execution with success status"""
        # Arrange
        context = {
            "username": "testuser",
            "success": True,
            "message": "Login successful"
        }

        self.credential_manager.get_statistics.return_value = {"total": 1}
        self.credential_manager.update_credentials_status.return_value = 0

        # Act
        result = self.action.execute(context)

        # Assert
        self.assertTrue(result.success)
        self.credential_manager.record_attempt.assert_called_once_with(
            "testuser", True, "Login successful", CredentialStatus.SUCCESS
        )
        self.credential_manager.update_credentials_status.assert_called_once_with(
            from_status=CredentialStatus.FAILURE,
            to_status=CredentialStatus.BLACKLISTED
        )

    def test_execute_with_failure_status(self):
        """Test execution with failure status"""
        # Arrange
        context = {
            "username": "testuser",
            "success": False,
            "message": "Login failed"
        }

        self.credential_manager.get_statistics.return_value = {"total": 0}
        self.credential_manager.update_credentials_status.return_value = 1

        # Act
        result = self.action.execute(context)

        # Assert
        self.assertTrue(result.success)
        self.credential_manager.record_attempt.assert_called_once_with(
            "testuser", False, "Login failed", CredentialStatus.FAILURE
        )
        self.credential_manager.update_credentials_status.assert_called_once_with(
            from_status=CredentialStatus.FAILURE,
            to_status=CredentialStatus.BLACKLISTED
        )
        self.assertEqual(result.data["updated_count"], 1)

    def test_execute_with_custom_inactive_status(self):
        """Test execution with custom inactive status"""
        # Arrange
        context = {"username": "testuser"}

        self.action.inactive_status = CredentialStatus.EXPIRED
        self.credential_manager.get_statistics.return_value = {"total": 0}
        self.credential_manager.update_credentials_status.return_value = 2

        # Act
        result = self.action.execute(context)

        # Assert
        self.assertTrue(result.success)
        self.credential_manager.update_credentials_status.assert_called_once_with(
            from_status=CredentialStatus.FAILURE,
            to_status=CredentialStatus.EXPIRED
        )
        self.assertEqual(result.data["updated_count"], 2)

    def test_to_dict(self):
        """Test converting the action to a dictionary"""
        # Arrange
        self.action.inactive_status = CredentialStatus.EXPIRED

        # Act
        data = self.action.to_dict()

        # Assert
        self.assertEqual(data["username_variable"], "username")
        self.assertEqual(data["success_variable"], "success")
        self.assertEqual(data["message_variable"], "message")
        self.assertEqual(data["inactive_status"], "EXPIRED")

    def test_from_dict(self):
        """Test creating an action from a dictionary"""
        # Arrange
        data = {
            "description": "Filter action",
            "username_variable": "user",
            "success_variable": "login_success",
            "message_variable": "login_message",
            "inactive_status": "EXPIRED",
            "id": "test-id"
        }

        # Act
        with patch("src.core.actions.credential_filter_action.CredentialManager") as mock_cm:
            action = CredentialFilterAction.from_dict(data)

        # Assert
        self.assertEqual(action.description, "Filter action")
        self.assertEqual(action.username_variable, "user")
        self.assertEqual(action.success_variable, "login_success")
        self.assertEqual(action.message_variable, "login_message")
        self.assertEqual(action.inactive_status, CredentialStatus.EXPIRED)
        self.assertEqual(action.id, "test-id")


if __name__ == "__main__":
    unittest.main()
