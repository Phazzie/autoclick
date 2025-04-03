"""Tests for the credential utilities."""
import unittest

from src.core.credentials.credential_manager import CredentialStatus
from src.domain.credentials.utils import (
    get_status_map,
    get_status_from_string,
    mask_sensitive_data,
    extract_metadata
)


class TestCredentialUtils(unittest.TestCase):
    """Test cases for the credential utilities."""
    
    def test_get_status_map(self):
        """Test getting the status map."""
        # Act
        result = get_status_map()
        
        # Assert
        self.assertEqual(result[CredentialStatus.UNUSED], "Active")
        self.assertEqual(result[CredentialStatus.SUCCESS], "Success")
        self.assertEqual(result[CredentialStatus.FAILURE], "Failure")
        self.assertEqual(result[CredentialStatus.LOCKED], "Inactive")
        self.assertEqual(result[CredentialStatus.EXPIRED], "Inactive")
        self.assertEqual(result[CredentialStatus.INVALID], "Inactive")
        self.assertEqual(result[CredentialStatus.BLACKLISTED], "Inactive")
    
    def test_get_status_from_string(self):
        """Test converting a string status to CredentialStatus."""
        # Act
        active_result = get_status_from_string("Active")
        success_result = get_status_from_string("Success")
        failure_result = get_status_from_string("Failure")
        inactive_result = get_status_from_string("Inactive")
        unknown_result = get_status_from_string("Unknown")
        
        # Assert
        self.assertEqual(active_result, CredentialStatus.UNUSED)
        self.assertEqual(success_result, CredentialStatus.SUCCESS)
        self.assertEqual(failure_result, CredentialStatus.FAILURE)
        self.assertEqual(inactive_result, CredentialStatus.BLACKLISTED)
        self.assertEqual(unknown_result, CredentialStatus.UNUSED)  # Default
    
    def test_mask_sensitive_data(self):
        """Test masking sensitive data."""
        # Arrange
        data = {
            "username": "user1",
            "password": "password123",
            "key": "api_key_123",
            "token": "token_123",
            "client_secret": "secret_123",
            "non_sensitive": "value"
        }
        
        # Act
        result = mask_sensitive_data(data)
        
        # Assert
        self.assertEqual(result["username"], "user1")  # Not masked
        self.assertEqual(result["password"], "********")  # Masked
        self.assertEqual(result["key"], "********")  # Masked
        self.assertEqual(result["token"], "********")  # Masked
        self.assertEqual(result["client_secret"], "********")  # Masked
        self.assertEqual(result["non_sensitive"], "value")  # Not masked
    
    def test_extract_metadata(self):
        """Test extracting metadata from credential data."""
        # Arrange
        credential_data = {
            "name": "Test Credential",
            "category": "Test",
            "tags": ["test"],
            "notes": "Test notes",
            "type": "username_password"
        }
        
        # Act
        result = extract_metadata(credential_data)
        
        # Assert
        self.assertEqual(result["name"], "Test Credential")
        self.assertEqual(result["category"], "Test")
        self.assertEqual(result["tags"], ["test"])
        self.assertEqual(result["notes"], "Test notes")
        self.assertEqual(result["type"], "username_password")
    
    def test_extract_metadata_defaults(self):
        """Test extracting metadata with defaults."""
        # Arrange
        credential_data = {}
        username = "user1"
        
        # Act
        result = extract_metadata(credential_data, username)
        
        # Assert
        self.assertEqual(result["name"], "user1")  # Default to username
        self.assertEqual(result["category"], "Other")  # Default
        self.assertEqual(result["tags"], [])  # Default
        self.assertEqual(result["notes"], "")  # Default
        self.assertEqual(result["type"], "username_password")  # Default


if __name__ == "__main__":
    unittest.main()
