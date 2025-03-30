"""Tests for the CredentialAdapter class."""
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.core.credentials.credential_manager import CredentialManager, CredentialStatus
from src.ui.adapters.credential_adapter import CredentialAdapter
from src.core.models import CredentialRecord as UICredentialRecord

class TestCredentialAdapter(unittest.TestCase):
    """Test cases for the CredentialAdapter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_credential_manager = MagicMock(spec=CredentialManager)
        self.adapter = CredentialAdapter(self.mock_credential_manager)
    
    def test_get_all_credentials(self):
        """Test getting all credentials."""
        # Arrange
        mock_record = MagicMock()
        mock_record.password = "password123"
        mock_record.status = CredentialStatus.UNUSED
        mock_record.last_used = None
        mock_record.metadata = {"name": "Test Credential", "category": "Test", "tags": ["test"], "notes": "Test notes"}
        
        self.mock_credential_manager.credentials = {"user1": mock_record}
        
        # Act
        result = self.adapter.get_all_credentials()
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "user1")
        self.assertEqual(result[0].name, "Test Credential")
        self.assertEqual(result[0].username, "user1")
        self.assertEqual(result[0].password, "password123")
        self.assertEqual(result[0].status, "Active")
        self.assertEqual(result[0].category, "Test")
        self.assertEqual(result[0].tags, ["test"])
        self.assertEqual(result[0].notes, "Test notes")
    
    def test_get_credential_by_id(self):
        """Test getting a credential by ID."""
        # Arrange
        mock_record = MagicMock()
        mock_record.password = "password123"
        mock_record.status = CredentialStatus.UNUSED
        mock_record.last_used = None
        mock_record.metadata = {"name": "Test Credential", "category": "Test", "tags": ["test"], "notes": "Test notes"}
        
        self.mock_credential_manager.credentials = {"user1": mock_record}
        
        # Act
        result = self.adapter.get_credential_by_id("user1")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "user1")
        self.assertEqual(result.name, "Test Credential")
        self.assertEqual(result.username, "user1")
        self.assertEqual(result.password, "password123")
        self.assertEqual(result.status, "Active")
        self.assertEqual(result.category, "Test")
        self.assertEqual(result.tags, ["test"])
        self.assertEqual(result.notes, "Test notes")
    
    def test_get_credential_by_id_not_found(self):
        """Test getting a credential by ID when it doesn't exist."""
        # Arrange
        self.mock_credential_manager.credentials = {}
        
        # Act
        result = self.adapter.get_credential_by_id("user1")
        
        # Assert
        self.assertIsNone(result)
    
    def test_add_credential(self):
        """Test adding a credential."""
        # Arrange
        mock_record = MagicMock()
        mock_record.password = "password123"
        mock_record.status = CredentialStatus.UNUSED
        mock_record.last_used = None
        mock_record.metadata = {"name": "Test Credential", "category": "Test", "tags": ["test"], "notes": "Test notes"}
        
        self.mock_credential_manager.add_credential.return_value = mock_record
        
        # Act
        result = self.adapter.add_credential(
            name="Test Credential",
            username="user1",
            password="password123",
            category="Test",
            tags=["test"],
            notes="Test notes"
        )
        
        # Assert
        self.mock_credential_manager.add_credential.assert_called_once_with(
            username="user1",
            password="password123",
            status=CredentialStatus.UNUSED,
            metadata={"name": "Test Credential", "category": "Test", "tags": ["test"], "notes": "Test notes"}
        )
        
        self.assertEqual(result.id, "user1")
        self.assertEqual(result.name, "Test Credential")
        self.assertEqual(result.username, "user1")
        self.assertEqual(result.password, "password123")
        self.assertEqual(result.status, "Active")
        self.assertEqual(result.category, "Test")
        self.assertEqual(result.tags, ["test"])
        self.assertEqual(result.notes, "Test notes")
    
    def test_update_credential(self):
        """Test updating a credential."""
        # Arrange
        mock_record = MagicMock()
        mock_record.password = "password123"
        mock_record.status = CredentialStatus.UNUSED
        mock_record.last_used = None
        mock_record.metadata = {"name": "Test Credential", "category": "Test", "tags": ["test"], "notes": "Test notes"}
        
        self.mock_credential_manager.credentials = {"user1": mock_record}
        
        # Act
        result = self.adapter.update_credential(
            cid="user1",
            name="Updated Credential",
            username="user1",
            password="newpassword",
            status="Active",
            category="Updated",
            tags=["updated"],
            notes="Updated notes"
        )
        
        # Assert
        self.assertEqual(mock_record.password, "newpassword")
        self.assertEqual(mock_record.status, CredentialStatus.UNUSED)
        self.assertEqual(mock_record.metadata, {
            "name": "Updated Credential",
            "category": "Updated",
            "tags": ["updated"],
            "notes": "Updated notes"
        })
        
        self.assertEqual(result.id, "user1")
        self.assertEqual(result.name, "Updated Credential")
        self.assertEqual(result.username, "user1")
        self.assertEqual(result.password, "newpassword")
        self.assertEqual(result.status, "Active")
        self.assertEqual(result.category, "Updated")
        self.assertEqual(result.tags, ["updated"])
        self.assertEqual(result.notes, "Updated notes")
    
    def test_update_credential_not_found(self):
        """Test updating a credential that doesn't exist."""
        # Arrange
        self.mock_credential_manager.credentials = {}
        
        # Act
        result = self.adapter.update_credential(
            cid="user1",
            name="Updated Credential",
            username="user1",
            password="newpassword"
        )
        
        # Assert
        self.assertIsNone(result)
    
    def test_delete_credential(self):
        """Test deleting a credential."""
        # Arrange
        mock_record = MagicMock()
        self.mock_credential_manager.credentials = {"user1": mock_record}
        
        # Act
        result = self.adapter.delete_credential("user1")
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(self.mock_credential_manager.credentials, {})
    
    def test_delete_credential_not_found(self):
        """Test deleting a credential that doesn't exist."""
        # Arrange
        self.mock_credential_manager.credentials = {}
        
        # Act
        result = self.adapter.delete_credential("user1")
        
        # Assert
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
