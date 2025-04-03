"""Tests for the CredentialFormatter class."""
import unittest
from unittest.mock import MagicMock
from datetime import datetime

from src.core.credentials.credential_manager import CredentialStatus
from src.domain.credentials.impl.credential_formatter import CredentialFormatter


class TestCredentialFormatter(unittest.TestCase):
    """Test cases for the CredentialFormatter class."""
    
    def test_to_ui_format(self):
        """Test converting a credential to UI format."""
        # Arrange
        mock_credential = MagicMock()
        mock_credential.username = "user1"
        mock_credential.password = "password123"
        mock_credential.status = CredentialStatus.UNUSED
        mock_credential.last_used = datetime.now()
        mock_credential.metadata = {
            "name": "Test Credential",
            "category": "Test",
            "tags": ["test"],
            "notes": "Test notes",
            "type": "username_password"
        }
        
        # Act
        result = CredentialFormatter.to_ui_format(mock_credential)
        
        # Assert
        self.assertEqual(result["id"], "user1")
        self.assertEqual(result["name"], "Test Credential")
        self.assertEqual(result["username"], "user1")
        self.assertEqual(result["password"], "********")  # Password should be masked
        self.assertEqual(result["status"], "Active")
        self.assertEqual(result["category"], "Test")
        self.assertEqual(result["tags"], ["test"])
        self.assertEqual(result["notes"], "Test notes")
        self.assertEqual(result["type"], "username_password")
    
    def test_to_ui_format_minimal(self):
        """Test converting a credential with minimal metadata to UI format."""
        # Arrange
        mock_credential = MagicMock()
        mock_credential.username = "user1"
        mock_credential.password = "password123"
        mock_credential.status = CredentialStatus.UNUSED
        mock_credential.last_used = None
        mock_credential.metadata = None
        
        # Act
        result = CredentialFormatter.to_ui_format(mock_credential)
        
        # Assert
        self.assertEqual(result["id"], "user1")
        self.assertEqual(result["name"], "user1")  # Default to username
        self.assertEqual(result["username"], "user1")
        self.assertEqual(result["password"], "********")  # Password should be masked
        self.assertEqual(result["status"], "Active")
        self.assertEqual(result["category"], "Other")  # Default category
        self.assertEqual(result["tags"], [])  # Default empty tags
        self.assertEqual(result["notes"], "")  # Default empty notes
        self.assertEqual(result["type"], "username_password")  # Default type
    
    def test_get_credential_type_metadata_known(self):
        """Test getting metadata for a known credential type."""
        # Act
        result = CredentialFormatter.get_credential_type_metadata("username_password")
        
        # Assert
        self.assertEqual(result["id"], "username_password")
        self.assertEqual(result["name"], "Username/Password")
        self.assertEqual(result["category"], "basic")
        self.assertIn("schema", result)
    
    def test_get_credential_type_metadata_unknown(self):
        """Test getting metadata for an unknown credential type."""
        # Act
        result = CredentialFormatter.get_credential_type_metadata("unknown_type")
        
        # Assert
        self.assertEqual(result["id"], "unknown_type")
        self.assertEqual(result["name"], "Unknown_type")
        self.assertEqual(result["category"], "other")
        self.assertIn("schema", result)


if __name__ == "__main__":
    unittest.main()
