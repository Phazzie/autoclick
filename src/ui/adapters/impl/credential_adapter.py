"""
Credential adapter implementation.

This module provides a concrete implementation of the credential adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.core.credentials.credential_manager import CredentialManager
from src.ui.adapters.base.base_credential_adapter import BaseCredentialAdapter


class CredentialAdapter(BaseCredentialAdapter):
    """Concrete implementation of credential adapter."""
    
    def __init__(self, credential_manager: Optional[CredentialManager] = None):
        """
        Initialize the adapter with a CredentialManager instance.
        
        Args:
            credential_manager: Optional credential manager to use
        """
        self._credential_manager = credential_manager or CredentialManager()
    
    def get_credential_types(self) -> List[Dict[str, Any]]:
        """
        Get all available credential types.
        
        Returns:
            List of credential types with metadata
        """
        # Get all credential types from the manager
        credential_types = self._credential_manager.get_credential_types()
        
        # Convert to UI format
        return [self._get_credential_type_metadata(credential_type) for credential_type in credential_types]
    
    def get_all_credentials(self) -> List[Dict[str, Any]]:
        """
        Get all credentials.
        
        Returns:
            List of credentials in the UI-expected format (sensitive data masked)
        """
        # Get all credentials from the manager
        credentials = self._credential_manager.get_all_credentials()
        
        # Convert to UI format
        return [self._convert_credential_to_ui_format(credential) for credential in credentials]
    
    def get_credential(self, credential_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a credential by ID.
        
        Args:
            credential_id: Credential ID
            
        Returns:
            Credential in the UI-expected format (sensitive data masked), or None if not found
        """
        # Get the credential from the manager
        credential = self._credential_manager.get_credential(credential_id)
        
        # Return None if not found
        if credential is None:
            return None
        
        # Convert to UI format
        return self._convert_credential_to_ui_format(credential)
    
    def create_credential(self, credential_type: str, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a credential.
        
        Args:
            credential_type: Credential type
            credential_data: Credential data
            
        Returns:
            Created credential in the UI-expected format (sensitive data masked)
            
        Raises:
            ValueError: If the credential data is invalid
        """
        # Validate the credential data
        errors = self.validate_credential(credential_type, credential_data)
        if errors:
            raise ValueError(f"Invalid credential data: {', '.join(errors)}")
        
        try:
            # Create the credential
            credential = self._credential_manager.create_credential(credential_type, credential_data)
            
            # Convert to UI format
            return self._convert_credential_to_ui_format(credential)
        except Exception as e:
            raise ValueError(f"Error creating credential: {str(e)}")
    
    def update_credential(self, credential_id: str, credential_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a credential.
        
        Args:
            credential_id: Credential ID
            credential_data: Credential data
            
        Returns:
            Updated credential in the UI-expected format (sensitive data masked), or None if not found
            
        Raises:
            ValueError: If the credential data is invalid
        """
        # Validate the credential data
        credential = self._credential_manager.get_credential(credential_id)
        if credential is None:
            return None
        
        errors = self.validate_credential(credential.type, credential_data)
        if errors:
            raise ValueError(f"Invalid credential data: {', '.join(errors)}")
        
        try:
            # Update the credential
            credential = self._credential_manager.update_credential(credential_id, credential_data)
            
            # Return None if not found
            if credential is None:
                return None
            
            # Convert to UI format
            return self._convert_credential_to_ui_format(credential)
        except Exception as e:
            raise ValueError(f"Error updating credential: {str(e)}")
    
    def delete_credential(self, credential_id: str) -> bool:
        """
        Delete a credential.
        
        Args:
            credential_id: Credential ID
            
        Returns:
            True if the credential was deleted, False if not found
        """
        try:
            # Delete the credential
            return self._credential_manager.delete_credential(credential_id)
        except Exception as e:
            raise ValueError(f"Error deleting credential: {str(e)}")
    
    def validate_credential(self, credential_type: str, credential_data: Dict[str, Any]) -> List[str]:
        """
        Validate a credential.
        
        Args:
            credential_type: Credential type
            credential_data: Credential data
            
        Returns:
            List of validation errors, empty if valid
        """
        try:
            # Validate the credential
            return self._credential_manager.validate_credential(credential_type, credential_data)
        except Exception as e:
            return [str(e)]
    
    def test_credential(self, credential_id: str) -> Dict[str, Any]:
        """
        Test a credential.
        
        Args:
            credential_id: Credential ID
            
        Returns:
            Test result
            
        Raises:
            ValueError: If the credential is not found or cannot be tested
        """
        try:
            # Test the credential
            return self._credential_manager.test_credential(credential_id)
        except Exception as e:
            raise ValueError(f"Error testing credential: {str(e)}")
    
    def _get_credential_type_metadata(self, credential_type: str) -> Dict[str, Any]:
        """
        Get metadata for a credential type.
        
        Args:
            credential_type: Credential type
            
        Returns:
            Credential type metadata
        """
        # Define metadata for known credential types
        metadata = {
            "username_password": {
                "id": "username_password",
                "name": "Username/Password",
                "description": "Username and password credentials",
                "icon": "user-password",
                "category": "basic"
            },
            "api_key": {
                "id": "api_key",
                "name": "API Key",
                "description": "API key credentials",
                "icon": "api-key",
                "category": "api"
            },
            "oauth2": {
                "id": "oauth2",
                "name": "OAuth 2.0",
                "description": "OAuth 2.0 credentials",
                "icon": "oauth",
                "category": "oauth"
            },
            "certificate": {
                "id": "certificate",
                "name": "Certificate",
                "description": "Certificate credentials",
                "icon": "certificate",
                "category": "security"
            }
        }
        
        # Return metadata for the credential type, or a default if not found
        return metadata.get(credential_type, {
            "id": credential_type,
            "name": credential_type.capitalize(),
            "description": f"{credential_type.capitalize()} credentials",
            "icon": "credential",
            "category": "other"
        })
    
    def _convert_credential_to_ui_format(self, credential: Any) -> Dict[str, Any]:
        """
        Convert a credential to UI format.
        
        Args:
            credential: Credential object
            
        Returns:
            Credential in UI format (sensitive data masked)
        """
        # Create a copy of the credential data
        credential_data = credential.to_dict()
        
        # Mask sensitive data
        self._mask_sensitive_data(credential_data)
        
        return {
            "id": credential_data.get("id"),
            "type": credential_data.get("type"),
            "name": credential_data.get("name"),
            "description": credential_data.get("description"),
            "data": credential_data.get("data", {}),
            "createdAt": credential_data.get("created_at"),
            "updatedAt": credential_data.get("updated_at")
        }
    
    def _mask_sensitive_data(self, credential_data: Dict[str, Any]) -> None:
        """
        Mask sensitive data in credential data.
        
        Args:
            credential_data: Credential data to mask
        """
        # Get the credential data
        data = credential_data.get("data", {})
        
        # Mask sensitive fields
        sensitive_fields = ["password", "secret", "key", "token", "access_token", "refresh_token", "private_key"]
        
        for field in sensitive_fields:
            if field in data and data[field]:
                data[field] = "********"
