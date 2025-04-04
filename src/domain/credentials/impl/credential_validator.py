"""
Credential validator implementation.

This module provides a concrete implementation of the credential validator interface.
"""
from typing import List, Dict, Any

from src.domain.credentials.interfaces import ICredentialValidator


class CredentialValidator(ICredentialValidator):
    """
    Implementation of the credential validator interface.
    
    This validator provides validation for different credential types.
    """
    
    def validate_credential(self, credential_type: str, credential_data: Dict[str, Any]) -> List[str]:
        """
        Validate a credential.
        
        Args:
            credential_type: Credential type
            credential_data: Credential data
            
        Returns:
            List of validation errors, empty if valid
        """
        # Get the appropriate validator method based on credential type
        validator_method = getattr(self, f"_validate_{credential_type}", self._validate_default)
        
        # Call the validator method
        return validator_method(credential_data)
    
    def _validate_username_password(self, credential_data: Dict[str, Any]) -> List[str]:
        """
        Validate a username/password credential.
        
        Args:
            credential_data: Credential data
            
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate required fields
        if not credential_data.get("username"):
            errors.append("Username is required")
        
        # Only require password for new credentials (not updates)
        if "password" in credential_data and not credential_data.get("password"):
            errors.append("Password is required")
        
        return errors
    
    def _validate_api_key(self, credential_data: Dict[str, Any]) -> List[str]:
        """
        Validate an API key credential.
        
        Args:
            credential_data: Credential data
            
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate required fields
        if not credential_data.get("key"):
            errors.append("API key is required")
        
        return errors
    
    def _validate_oauth2(self, credential_data: Dict[str, Any]) -> List[str]:
        """
        Validate an OAuth2 credential.
        
        Args:
            credential_data: Credential data
            
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate required fields
        if not credential_data.get("client_id"):
            errors.append("Client ID is required")
        if not credential_data.get("client_secret"):
            errors.append("Client secret is required")
        
        return errors
    
    def _validate_certificate(self, credential_data: Dict[str, Any]) -> List[str]:
        """
        Validate a certificate credential.
        
        Args:
            credential_data: Credential data
            
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate required fields
        if not credential_data.get("certificate_path"):
            errors.append("Certificate path is required")
        
        return errors
    
    def _validate_default(self, credential_data: Dict[str, Any]) -> List[str]:
        """
        Default validator for unknown credential types.
        
        Args:
            credential_data: Credential data
            
        Returns:
            List of validation errors, empty if valid
        """
        # No specific validation for unknown types
        return []
