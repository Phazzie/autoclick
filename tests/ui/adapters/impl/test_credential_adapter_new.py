"""Tests for the new CredentialAdapter implementation."""
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.core.credentials.credential_manager import CredentialManager, CredentialStatus
from src.ui.adapters.impl.credential_adapter import CredentialAdapter
from src.domain.credentials.interfaces import ICredentialService


class TestCredentialAdapter(unittest.TestCase):
    """Test cases for the CredentialAdapter class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock service for clean architecture tests
        self.mock_service = MagicMock(spec=ICredentialService)

        # Create mock credential manager for legacy tests
        self.mock_credential_manager = MagicMock(spec=CredentialManager)

        # Create adapters for both modes
        self.service_adapter = CredentialAdapter(credential_service=self.mock_service)
        self.legacy_adapter = CredentialAdapter(credential_manager=self.mock_credential_manager)

    def test_get_credential_types_service_mode(self):
        """Test getting credential types in service mode."""
        # Arrange
        expected_types = [
            {
                "id": "username_password",
                "name": "Username/Password",
                "description": "Username and password credentials"
            }
        ]
        self.mock_service.get_credential_types.return_value = expected_types

        # Act
        result = self.service_adapter.get_credential_types()

        # Assert
        self.assertEqual(result, expected_types)
        self.mock_service.get_credential_types.assert_called_once()

    def test_get_credential_types_legacy_mode(self):
        """Test getting credential types in legacy mode."""
        # Arrange
        # In legacy mode, credential types are hardcoded in the adapter

        # Act
        result = self.legacy_adapter.get_credential_types()

        # Assert
        self.assertEqual(len(result), 4)  # username_password, api_key, oauth2, certificate
        self.assertEqual(result[0]["id"], "username_password")

    def test_get_all_credentials_service_mode(self):
        """Test getting all credentials in service mode."""
        # Arrange
        expected_credentials = [
            {
                "id": "user1",
                "name": "Test Credential",
                "username": "user1",
                "password": "********",
                "status": "Active"
            }
        ]
        self.mock_service.get_all_credentials.return_value = expected_credentials

        # Act
        result = self.service_adapter.get_all_credentials()

        # Assert
        self.assertEqual(result, expected_credentials)
        self.mock_service.get_all_credentials.assert_called_once()

    def test_get_all_credentials_legacy_mode(self):
        """Test getting all credentials in legacy mode."""
        # Arrange
        mock_record = MagicMock()
        mock_record.username = "user1"
        mock_record.password = "password123"
        mock_record.status = CredentialStatus.UNUSED
        mock_record.last_used = None
        mock_record.metadata = {"name": "Test Credential", "category": "Test", "tags": ["test"], "notes": "Test notes"}

        # In legacy mode, credentials are stored in a dictionary
        self.mock_credential_manager.credentials = {"user1": mock_record}

        # Act
        result = self.legacy_adapter.get_all_credentials()

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "user1")
        self.assertEqual(result[0]["name"], "Test Credential")

    def test_get_credential_service_mode(self):
        """Test getting a credential by ID in service mode."""
        # Arrange
        expected_credential = {
            "id": "user1",
            "name": "Test Credential",
            "username": "user1",
            "password": "********",
            "status": "Active"
        }
        self.mock_service.get_credential.return_value = expected_credential

        # Act
        result = self.service_adapter.get_credential("user1")

        # Assert
        self.assertEqual(result, expected_credential)
        self.mock_service.get_credential.assert_called_once_with("user1")

    def test_get_credential_legacy_mode(self):
        """Test getting a credential by ID in legacy mode."""
        # Arrange
        mock_record = MagicMock()
        mock_record.username = "user1"
        mock_record.password = "password123"
        mock_record.status = CredentialStatus.UNUSED
        mock_record.last_used = None
        mock_record.metadata = {"name": "Test Credential", "category": "Test", "tags": ["test"], "notes": "Test notes"}

        self.mock_credential_manager.get_credential.return_value = mock_record

        # Act
        result = self.legacy_adapter.get_credential("user1")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "user1")
        self.assertEqual(result["name"], "Test Credential")
        self.mock_credential_manager.get_credential.assert_called_once_with("user1")

    def test_create_credential_service_mode(self):
        """Test creating a credential in service mode."""
        # Arrange
        credential_type = "username_password"
        credential_data = {
            "name": "Test Credential",
            "username": "user1",
            "password": "password123",
            "category": "Test",
            "tags": ["test"],
            "notes": "Test notes"
        }

        expected_credential = {
            "id": "user1",
            "name": "Test Credential",
            "username": "user1",
            "password": "********",
            "status": "Active"
        }

        # Mock the validate_credential method to return empty list (no errors)
        self.mock_service.validate_credential.return_value = []
        self.mock_service.create_credential.return_value = expected_credential

        # Act
        result = self.service_adapter.create_credential(credential_type, credential_data)

        # Assert
        self.assertEqual(result, expected_credential)
        self.mock_service.create_credential.assert_called_once_with(credential_type, credential_data)

    def test_create_credential_legacy_mode(self):
        """Test creating a credential in legacy mode."""
        # Arrange
        credential_type = "username_password"
        credential_data = {
            "name": "Test Credential",
            "username": "user1",
            "password": "password123",
            "category": "Test",
            "tags": ["test"],
            "notes": "Test notes"
        }

        mock_record = MagicMock()
        mock_record.username = "user1"
        mock_record.password = "password123"
        mock_record.status = CredentialStatus.UNUSED
        mock_record.last_used = None
        mock_record.metadata = {"name": "Test Credential", "category": "Test", "tags": ["test"], "notes": "Test notes"}

        self.mock_credential_manager.add_credential.return_value = mock_record

        # Act
        result = self.legacy_adapter.create_credential(credential_type, credential_data)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "user1")
        self.assertEqual(result["name"], "Test Credential")
        self.mock_credential_manager.add_credential.assert_called_once()

    def test_update_credential_service_mode(self):
        """Test updating a credential in service mode."""
        # Arrange
        credential_id = "user1"
        credential_data = {
            "name": "Updated Credential",
            "username": "user1",
            "password": "newpassword",
            "category": "Updated",
            "tags": ["updated"],
            "notes": "Updated notes"
        }

        expected_credential = {
            "id": "user1",
            "name": "Updated Credential",
            "username": "user1",
            "password": "********",
            "status": "Active"
        }

        self.mock_service.update_credential.return_value = expected_credential

        # Act
        result = self.service_adapter.update_credential(credential_id, credential_data)

        # Assert
        self.assertEqual(result, expected_credential)
        self.mock_service.update_credential.assert_called_once_with(credential_id, credential_data)

    def test_update_credential_legacy_mode(self):
        """Test updating a credential in legacy mode."""
        # Arrange
        credential_id = "user1"
        credential_data = {
            "name": "Updated Credential",
            "username": "user1",
            "password": "newpassword",
            "status": "Active",
            "category": "Updated",
            "tags": ["updated"],
            "notes": "Updated notes"
        }

        mock_record = MagicMock()
        mock_record.username = "user1"
        mock_record.password = "password123"
        mock_record.status = CredentialStatus.UNUSED
        mock_record.last_used = None
        mock_record.metadata = {"name": "Test Credential", "category": "Test", "tags": ["test"], "notes": "Test notes"}

        self.mock_credential_manager.get_credential.return_value = mock_record

        # Act
        result = self.legacy_adapter.update_credential(credential_id, credential_data)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "user1")
        self.assertEqual(result["name"], "Updated Credential")

    def test_delete_credential_service_mode(self):
        """Test deleting a credential in service mode."""
        # Arrange
        credential_id = "user1"
        self.mock_service.delete_credential.return_value = True

        # Act
        result = self.service_adapter.delete_credential(credential_id)

        # Assert
        self.assertTrue(result)
        self.mock_service.delete_credential.assert_called_once_with(credential_id)

    def test_delete_credential_legacy_mode(self):
        """Test deleting a credential in legacy mode."""
        # Arrange
        credential_id = "user1"
        self.mock_credential_manager.remove_credential.return_value = True

        # Act
        result = self.legacy_adapter.delete_credential(credential_id)

        # Assert
        self.assertTrue(result)
        self.mock_credential_manager.remove_credential.assert_called_once_with(credential_id)

    def test_validate_credential_service_mode(self):
        """Test validating a credential in service mode."""
        # Arrange
        credential_type = "username_password"
        credential_data = {
            "name": "Test Credential",
            "username": "user1",
            "password": "password123"
        }

        self.mock_service.validate_credential.return_value = []

        # Act
        result = self.service_adapter.validate_credential(credential_type, credential_data)

        # Assert
        self.assertEqual(result, [])
        self.mock_service.validate_credential.assert_called_once_with(credential_type, credential_data)

    def test_validate_credential_legacy_mode(self):
        """Test validating a credential in legacy mode."""
        # Arrange
        credential_type = "username_password"
        credential_data = {
            "name": "Test Credential",
            "username": "user1",
            "password": "password123"
        }

        # Act
        result = self.legacy_adapter.validate_credential(credential_type, credential_data)

        # Assert
        self.assertEqual(result, [])

    def test_test_credential_service_mode(self):
        """Test testing a credential in service mode."""
        # Arrange
        credential_id = "user1"
        expected_result = {
            "success": True,
            "message": "Authentication successful"
        }

        self.mock_service.test_credential.return_value = expected_result

        # Act
        result = self.service_adapter.test_credential(credential_id)

        # Assert
        self.assertEqual(result, expected_result)
        self.mock_service.test_credential.assert_called_once_with(credential_id)

    def test_test_credential_legacy_mode(self):
        """Test testing a credential in legacy mode."""
        # Arrange
        credential_id = "user1"
        mock_record = MagicMock()
        mock_record.username = "user1"
        mock_record.password = "password123"
        mock_record.status = CredentialStatus.UNUSED

        self.mock_credential_manager.get_credential.return_value = mock_record

        # Act
        result = self.legacy_adapter.test_credential(credential_id)

        # Assert
        self.assertTrue("success" in result)
        self.assertTrue("message" in result)
        self.mock_credential_manager.get_credential.assert_called_once_with(credential_id)


if __name__ == "__main__":
    unittest.main()
