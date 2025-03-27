"""Tests for the CredentialModel class"""
import unittest
from unittest.mock import MagicMock, patch

from src.ui.models.credential_model import CredentialModel


class TestCredentialModel(unittest.TestCase):
    """Test cases for the CredentialModel class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        # Mock the CredentialsManager
        with patch("src.ui.models.credential_model.CredentialsManager") as mock_manager:
            self.mock_manager_instance = mock_manager.return_value
            self.model = CredentialModel()
        
        self.test_site = "example.com"
        self.test_username = "testuser"
        self.test_password = "testpass"
        self.test_credentials = {
            "username": self.test_username,
            "password": self.test_password
        }

    def test_get_all_sites(self) -> None:
        """Test getting all sites"""
        # Mock the list_keys method
        self.mock_manager_instance.list_keys.return_value = [self.test_site]
        
        # Get all sites
        sites = self.model.get_all_sites()
        
        # Verify sites
        self.assertEqual(sites, [self.test_site])
        
        # Verify the list_keys method was called
        self.mock_manager_instance.list_keys.assert_called_once()

    def test_get_credentials(self) -> None:
        """Test getting credentials"""
        # Mock the load method
        self.mock_manager_instance.load.return_value = self.test_credentials
        
        # Get credentials
        credentials = self.model.get_credentials(self.test_site)
        
        # Verify credentials
        self.assertEqual(credentials, self.test_credentials)
        
        # Verify the load method was called with the correct site
        self.mock_manager_instance.load.assert_called_once_with(self.test_site)

    def test_add_credentials(self) -> None:
        """Test adding credentials"""
        # Add credentials
        result = self.model.add_credentials(
            self.test_site,
            self.test_username,
            self.test_password
        )
        
        # Verify result
        self.assertTrue(result)
        
        # Verify the save method was called with the correct arguments
        self.mock_manager_instance.save.assert_called_once_with(
            self.test_site,
            self.test_credentials
        )

    def test_add_credentials_exception(self) -> None:
        """Test adding credentials with exception"""
        # Mock the save method to raise an exception
        self.mock_manager_instance.save.side_effect = Exception("Test exception")
        
        # Add credentials
        result = self.model.add_credentials(
            self.test_site,
            self.test_username,
            self.test_password
        )
        
        # Verify result
        self.assertFalse(result)
        
        # Verify the save method was called with the correct arguments
        self.mock_manager_instance.save.assert_called_once_with(
            self.test_site,
            self.test_credentials
        )

    def test_update_credentials(self) -> None:
        """Test updating credentials"""
        # Update credentials
        result = self.model.update_credentials(
            self.test_site,
            self.test_username,
            self.test_password
        )
        
        # Verify result
        self.assertTrue(result)
        
        # Verify the save method was called with the correct arguments
        self.mock_manager_instance.save.assert_called_once_with(
            self.test_site,
            self.test_credentials
        )

    def test_remove_credentials(self) -> None:
        """Test removing credentials"""
        # Remove credentials
        result = self.model.remove_credentials(self.test_site)
        
        # Verify result
        self.assertTrue(result)
        
        # Verify the delete method was called with the correct site
        self.mock_manager_instance.delete.assert_called_once_with(self.test_site)

    def test_remove_credentials_exception(self) -> None:
        """Test removing credentials with exception"""
        # Mock the delete method to raise an exception
        self.mock_manager_instance.delete.side_effect = Exception("Test exception")
        
        # Remove credentials
        result = self.model.remove_credentials(self.test_site)
        
        # Verify result
        self.assertFalse(result)
        
        # Verify the delete method was called with the correct site
        self.mock_manager_instance.delete.assert_called_once_with(self.test_site)


if __name__ == "__main__":
    unittest.main()
