"""
Credential adapter interface.

This module defines the interface for credential adapters.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class ICredentialAdapter(ABC):
    """Interface for credential adapters."""
    
    @abstractmethod
    def get_credential_types(self) -> List[Dict[str, Any]]:
        """
        Get all available credential types.
        
        Returns:
            List of credential types with metadata
        """
        pass
    
    @abstractmethod
    def get_all_credentials(self) -> List[Dict[str, Any]]:
        """
        Get all credentials.
        
        Returns:
            List of credentials in the UI-expected format (sensitive data masked)
        """
        pass
    
    @abstractmethod
    def get_credential(self, credential_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a credential by ID.
        
        Args:
            credential_id: Credential ID
            
        Returns:
            Credential in the UI-expected format (sensitive data masked), or None if not found
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete_credential(self, credential_id: str) -> bool:
        """
        Delete a credential.
        
        Args:
            credential_id: Credential ID
            
        Returns:
            True if the credential was deleted, False if not found
        """
        pass
    
    @abstractmethod
    def validate_credential(self, credential_type: str, credential_data: Dict[str, Any]) -> List[str]:
        """
        Validate a credential.
        
        Args:
            credential_type: Credential type
            credential_data: Credential data
            
        Returns:
            List of validation errors, empty if valid
        """
        pass
    
    @abstractmethod
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
        pass
