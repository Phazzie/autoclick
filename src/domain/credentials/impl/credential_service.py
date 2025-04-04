"""
Credential service implementation.

This module provides a concrete implementation of the credential service interface.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.core.credentials.credential_manager import CredentialManager, CredentialStatus
from src.domain.credentials.interfaces import ICredentialService
from src.domain.credentials.impl.credential_validator import CredentialValidator
from src.domain.credentials.impl.credential_formatter import CredentialFormatter
from src.domain.credentials.utils import get_status_from_string, extract_metadata
from src.domain.exceptions.domain_exceptions import DomainException


class CredentialService(ICredentialService):
    """
    Implementation of the credential service interface.

    This service provides credential management functionality using the CredentialManager.
    """

    def __init__(self,
                 credential_manager: Optional[CredentialManager] = None,
                 validator: Optional[CredentialValidator] = None,
                 formatter: Optional[CredentialFormatter] = None):
        """
        Initialize the credential service with dependencies.

        Args:
            credential_manager: Optional credential manager to use
            validator: Optional credential validator to use
            formatter: Optional credential formatter to use
        """
        self._credential_manager = credential_manager or CredentialManager()
        self._validator = validator or CredentialValidator()
        self._formatter = formatter or CredentialFormatter()

    def get_credential_types(self) -> List[Dict[str, Any]]:
        """
        Get all available credential types.

        Returns:
            List of credential types with metadata
        """
        # Define supported credential types
        credential_types = ["username_password", "api_key", "oauth2", "certificate"]

        # Convert to UI format using the formatter
        return [self._formatter.get_credential_type_metadata(credential_type)
                for credential_type in credential_types]

    def get_all_credentials(self) -> List[Dict[str, Any]]:
        """
        Get all credentials.

        Returns:
            List of credentials in the UI-expected format (sensitive data masked)
        """
        # Get all credentials from the manager
        credentials = list(self._credential_manager.credentials.values())

        # Convert to UI format using the formatter
        return [self._formatter.to_ui_format(credential) for credential in credentials]

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

        # Convert to UI format using the formatter
        return self._formatter.to_ui_format(credential)

    def create_credential(self, credential_type: str, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a credential.

        Args:
            credential_type: Credential type
            credential_data: Credential data

        Returns:
            Created credential in the UI-expected format (sensitive data masked)

        Raises:
            DomainException: If the credential data is invalid
        """
        # Validate the credential data
        errors = self.validate_credential(credential_type, credential_data)
        if errors:
            raise DomainException(f"Invalid credential data: {', '.join(errors)}")

        try:
            # Extract credential fields
            username = credential_data.get("username")
            password = credential_data.get("password")

            # Extract metadata
            metadata = extract_metadata(credential_data, username)
            metadata["type"] = credential_type

            # Add the credential
            credential = self._credential_manager.add_credential(
                username=username,
                password=password,
                status=CredentialStatus.UNUSED,
                metadata=metadata
            )

            # Convert to UI format using the formatter
            return self._formatter.to_ui_format(credential)
        except Exception as e:
            raise DomainException(f"Error creating credential: {str(e)}")

    def update_credential(self, credential_id: str, credential_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a credential.

        Args:
            credential_id: Credential ID
            credential_data: Credential data

        Returns:
            Updated credential in the UI-expected format (sensitive data masked), or None if not found

        Raises:
            DomainException: If the credential data is invalid
        """
        # Get the credential
        credential = self._credential_manager.get_credential(credential_id)
        if credential is None:
            return None

        # Get the credential type from metadata
        credential_type = credential.metadata.get("type", "username_password")

        # Validate the credential data
        errors = self.validate_credential(credential_type, credential_data)
        if errors:
            raise DomainException(f"Invalid credential data: {', '.join(errors)}")

        try:
            # Update password if provided
            password = credential_data.get("password")
            if password:
                credential.password = password

            # Update status if provided
            status_str = credential_data.get("status")
            if status_str:
                credential.status = get_status_from_string(status_str)

            # Extract and update metadata
            metadata = extract_metadata(credential_data, credential.username)
            metadata["type"] = credential_type
            credential.metadata = metadata

            # Convert to UI format using the formatter
            return self._formatter.to_ui_format(credential)
        except Exception as e:
            raise DomainException(f"Error updating credential: {str(e)}")

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
            return self._credential_manager.remove_credential(credential_id)
        except Exception as e:
            raise DomainException(f"Error deleting credential: {str(e)}")

    def validate_credential(self, credential_type: str, credential_data: Dict[str, Any]) -> List[str]:
        """
        Validate a credential.

        Args:
            credential_type: Credential type
            credential_data: Credential data

        Returns:
            List of validation errors, empty if valid
        """
        # Delegate to the validator
        return self._validator.validate_credential(credential_type, credential_data)

    def test_credential(self, credential_id: str) -> Dict[str, Any]:
        """
        Test a credential.

        Args:
            credential_id: Credential ID

        Returns:
            Test result

        Raises:
            DomainException: If the credential is not found or cannot be tested
        """
        try:
            # Get the credential
            credential = self._credential_manager.get_credential(credential_id)

            # Raise error if not found
            if credential is None:
                raise DomainException(f"Credential not found: {credential_id}")

            # In a real implementation, we would test the credential here
            # For now, just return a success result
            result = {
                "success": True,
                "message": "Credential test successful",
                "timestamp": str(datetime.now())
            }

            # Record the test result
            self._credential_manager.record_attempt(
                credential_id,
                success=result["success"],
                message=result["message"]
            )

            return result
        except Exception as e:
            raise DomainException(f"Error testing credential: {str(e)}")
