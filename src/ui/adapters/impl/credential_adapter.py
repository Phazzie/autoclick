"""
Credential adapter implementation.

This module provides a concrete implementation of the credential adapter interface.
It supports both clean architecture (through ICredentialService) and legacy mode
(through CredentialManager).
"""
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.core.credentials.credential_manager import CredentialManager, CredentialStatus
from src.domain.credentials.interfaces import ICredentialService
from src.ui.adapters.base.base_credential_adapter import BaseCredentialAdapter


class CredentialAdapter(BaseCredentialAdapter):
    """
    Concrete implementation of credential adapter.

    This adapter uses the clean architecture components through a credential service
    or falls back to the legacy credential manager.
    """

    def __init__(self, credential_service: Optional[ICredentialService] = None, credential_manager: Optional[CredentialManager] = None):
        """
        Initialize the adapter with a credential service or manager.

        Args:
            credential_service: Optional credential service to use (clean architecture)
            credential_manager: Optional credential manager to use (legacy)
        """
        if credential_service:
            self._service = credential_service
            self._use_service = True
        else:
            self._use_service = False
            self._credential_manager = credential_manager or CredentialManager()

    def get_credential_types(self) -> List[Dict[str, Any]]:
        """
        Get all available credential types.

        Returns:
            List of credential types with metadata
        """
        if self._use_service:
            try:
                return self._service.get_credential_types()
            except Exception as e:
                raise ValueError(f"Error getting credential types: {str(e)}")
        else:
            # Legacy implementation
            # In legacy mode, we hardcode the credential types
            credential_types = ["username_password", "api_key", "oauth2", "certificate"]

            # Convert to UI format
            return [self._get_credential_type_metadata(credential_type) for credential_type in credential_types]

    def get_all_credentials(self) -> List[Dict[str, Any]]:
        """
        Get all credentials.

        Returns:
            List of credentials in the UI-expected format (sensitive data masked)
        """
        if self._use_service:
            try:
                return self._service.get_all_credentials()
            except Exception as e:
                raise ValueError(f"Error getting all credentials: {str(e)}")
        else:
            # Legacy implementation
            # Get all credentials from the manager's credentials dictionary
            credentials = list(self._credential_manager.credentials.values())

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
        if self._use_service:
            try:
                return self._service.get_credential(credential_id)
            except Exception as e:
                raise ValueError(f"Error getting credential {credential_id}: {str(e)}")
        else:
            # Legacy implementation
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
        if self._use_service:
            try:
                # Validate the credential data first
                errors = self.validate_credential(credential_type, credential_data)
                if errors:
                    raise ValueError(f"Invalid credential data: {', '.join(errors)}")

                # Create the credential
                return self._service.create_credential(credential_type, credential_data)
            except Exception as e:
                raise ValueError(f"Error creating credential: {str(e)}")
        else:
            # Legacy implementation
            # Validate the credential data
            errors = self.validate_credential(credential_type, credential_data)
            if errors:
                raise ValueError(f"Invalid credential data: {', '.join(errors)}")

            try:
                # Extract credential fields
                username = credential_data.get("username")
                password = credential_data.get("password")
                name = credential_data.get("name", username)
                category = credential_data.get("category", "Other")
                tags = credential_data.get("tags", [])
                notes = credential_data.get("notes", "")

                # Create metadata
                metadata = {
                    "name": name,
                    "category": category,
                    "tags": tags,
                    "notes": notes
                }

                # Add the credential
                credential = self._credential_manager.add_credential(
                    username=username,
                    password=password,
                    status=CredentialStatus.UNUSED,
                    metadata=metadata
                )

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
        if self._use_service:
            try:
                return self._service.update_credential(credential_id, credential_data)
            except Exception as e:
                raise ValueError(f"Error updating credential {credential_id}: {str(e)}")
        else:
            # Legacy implementation
            # Get the credential
            credential = self._credential_manager.get_credential(credential_id)
            if credential is None:
                return None

            # Validate the credential data
            errors = self.validate_credential("username_password", credential_data)
            if errors:
                raise ValueError(f"Invalid credential data: {', '.join(errors)}")

            try:
                # Extract credential fields
                username = credential_data.get("username", credential.username)
                password = credential_data.get("password")
                name = credential_data.get("name", username)
                status_str = credential_data.get("status", "Active")
                category = credential_data.get("category", "Other")
                tags = credential_data.get("tags", [])
                notes = credential_data.get("notes", "")

                # Update the credential
                if password:
                    credential.password = password

                # Map UI status to backend status
                if status_str == "Active":
                    credential.status = CredentialStatus.UNUSED
                elif status_str == "Inactive":
                    credential.status = CredentialStatus.BLACKLISTED
                elif status_str == "Success":
                    credential.status = CredentialStatus.SUCCESS
                elif status_str == "Failure":
                    credential.status = CredentialStatus.FAILURE

                # Update metadata
                credential.metadata = {
                    "name": name,
                    "category": category,
                    "tags": tags,
                    "notes": notes
                }

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
        if self._use_service:
            try:
                return self._service.delete_credential(credential_id)
            except Exception as e:
                raise ValueError(f"Error deleting credential {credential_id}: {str(e)}")
        else:
            # Legacy implementation
            try:
                # Delete the credential
                return self._credential_manager.remove_credential(credential_id)
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
        if self._use_service:
            try:
                return self._service.validate_credential(credential_type, credential_data)
            except Exception as e:
                # Return the error as a validation error
                return [f"Error validating credential: {str(e)}"]
        else:
            # Legacy implementation
            errors = []

            # Validate required fields based on credential type
            if credential_type == "username_password":
                if not credential_data.get("username"):
                    errors.append("Username is required")

                # Only require password for new credentials (not updates)
                if "password" in credential_data and not credential_data.get("password"):
                    errors.append("Password is required")
            elif credential_type == "api_key":
                if not credential_data.get("key"):
                    errors.append("API key is required")
            elif credential_type == "oauth2":
                if not credential_data.get("client_id"):
                    errors.append("Client ID is required")
                if not credential_data.get("client_secret"):
                    errors.append("Client secret is required")

            return errors

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
        if self._use_service:
            try:
                return self._service.test_credential(credential_id)
            except Exception as e:
                raise ValueError(f"Error testing credential {credential_id}: {str(e)}")
        else:
            # Legacy implementation
            try:
                # Get the credential
                credential = self._credential_manager.get_credential(credential_id)

                # Raise error if not found
                if credential is None:
                    raise ValueError(f"Credential not found: {credential_id}")

                # In a real implementation, we would test the credential here
                # For now, just return a success result
                return {
                    "success": True,
                    "message": "Credential test successful",
                    "timestamp": str(datetime.now())
                }
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
        # Map status to UI status
        status_map = {
            CredentialStatus.UNUSED: "Active",
            CredentialStatus.SUCCESS: "Success",
            CredentialStatus.FAILURE: "Failure",
            CredentialStatus.LOCKED: "Inactive",
            CredentialStatus.EXPIRED: "Inactive",
            CredentialStatus.INVALID: "Inactive",
            CredentialStatus.BLACKLISTED: "Inactive"
        }

        # Get UI-specific fields from metadata
        metadata = credential.metadata or {}
        name = metadata.get("name", credential.username)
        category = metadata.get("category", "Other")
        tags = metadata.get("tags", [])
        notes = metadata.get("notes", "")

        # Create UI format
        return {
            "id": credential.username,
            "name": name,
            "username": credential.username,
            "password": "********",  # Mask password
            "status": status_map.get(credential.status, "Active"),
            "last_used": credential.last_used,
            "category": category,
            "tags": tags,
            "notes": notes
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

    def _get_status_string(self, status: CredentialStatus) -> str:
        """
        Convert a CredentialStatus to a string.

        Args:
            status: CredentialStatus enum value

        Returns:
            String representation of the status
        """
        status_map = {
            CredentialStatus.UNUSED: "Active",
            CredentialStatus.SUCCESS: "Success",
            CredentialStatus.FAILURE: "Failure",
            CredentialStatus.LOCKED: "Inactive",
            CredentialStatus.EXPIRED: "Inactive",
            CredentialStatus.INVALID: "Inactive",
            CredentialStatus.BLACKLISTED: "Inactive"
        }

        return status_map.get(status, "Active")
