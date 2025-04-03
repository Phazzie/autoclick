"""Tests for the CredentialValidator class."""
import unittest

from src.domain.credentials.impl.credential_validator import CredentialValidator


class TestCredentialValidator(unittest.TestCase):
    """Test cases for the CredentialValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = CredentialValidator()
    
    def test_validate_username_password_valid(self):
        """Test validating a valid username/password credential."""
        # Arrange
        credential_type = "username_password"
        credential_data = {
            "username": "user1",
            "password": "password123"
        }
        
        # Act
        result = self.validator.validate_credential(credential_type, credential_data)
        
        # Assert
        self.assertEqual(result, [])
    
    def test_validate_username_password_invalid(self):
        """Test validating an invalid username/password credential."""
        # Arrange
        credential_type = "username_password"
        credential_data = {
            # Missing username
            "password": "password123"
        }
        
        # Act
        result = self.validator.validate_credential(credential_type, credential_data)
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertIn("Username is required", result)
    
    def test_validate_api_key_valid(self):
        """Test validating a valid API key credential."""
        # Arrange
        credential_type = "api_key"
        credential_data = {
            "key": "api_key_123"
        }
        
        # Act
        result = self.validator.validate_credential(credential_type, credential_data)
        
        # Assert
        self.assertEqual(result, [])
    
    def test_validate_api_key_invalid(self):
        """Test validating an invalid API key credential."""
        # Arrange
        credential_type = "api_key"
        credential_data = {
            # Missing key
        }
        
        # Act
        result = self.validator.validate_credential(credential_type, credential_data)
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertIn("API key is required", result)
    
    def test_validate_oauth2_valid(self):
        """Test validating a valid OAuth2 credential."""
        # Arrange
        credential_type = "oauth2"
        credential_data = {
            "client_id": "client_id_123",
            "client_secret": "client_secret_123"
        }
        
        # Act
        result = self.validator.validate_credential(credential_type, credential_data)
        
        # Assert
        self.assertEqual(result, [])
    
    def test_validate_oauth2_invalid(self):
        """Test validating an invalid OAuth2 credential."""
        # Arrange
        credential_type = "oauth2"
        credential_data = {
            "client_id": "client_id_123"
            # Missing client_secret
        }
        
        # Act
        result = self.validator.validate_credential(credential_type, credential_data)
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertIn("Client secret is required", result)
    
    def test_validate_certificate_valid(self):
        """Test validating a valid certificate credential."""
        # Arrange
        credential_type = "certificate"
        credential_data = {
            "certificate_path": "/path/to/certificate.pem"
        }
        
        # Act
        result = self.validator.validate_credential(credential_type, credential_data)
        
        # Assert
        self.assertEqual(result, [])
    
    def test_validate_certificate_invalid(self):
        """Test validating an invalid certificate credential."""
        # Arrange
        credential_type = "certificate"
        credential_data = {
            # Missing certificate_path
        }
        
        # Act
        result = self.validator.validate_credential(credential_type, credential_data)
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertIn("Certificate path is required", result)
    
    def test_validate_unknown_type(self):
        """Test validating an unknown credential type."""
        # Arrange
        credential_type = "unknown"
        credential_data = {
            "field1": "value1"
        }
        
        # Act
        result = self.validator.validate_credential(credential_type, credential_data)
        
        # Assert
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
