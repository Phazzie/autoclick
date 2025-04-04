"""
Credential formatter implementation.

This module provides utilities for formatting credentials.
"""
from typing import Dict, Any

from src.core.credentials.credential_manager import CredentialStatus
from src.domain.credentials.utils import get_status_map, mask_sensitive_data


class CredentialFormatter:
    """
    Formatter for credentials.
    
    This class provides methods for converting credentials to UI format.
    """
    
    @staticmethod
    def to_ui_format(credential: Any) -> Dict[str, Any]:
        """
        Convert a credential to UI format.
        
        Args:
            credential: Credential object
            
        Returns:
            Credential in UI format (sensitive data masked)
        """
        # Get status mapping
        status_map = get_status_map()
        
        # Get UI-specific fields from metadata
        metadata = credential.metadata or {}
        name = metadata.get("name", credential.username)
        category = metadata.get("category", "Other")
        tags = metadata.get("tags", [])
        notes = metadata.get("notes", "")
        credential_type = metadata.get("type", "username_password")
        
        # Create UI format
        credential_data = {
            "id": credential.username,
            "type": credential_type,
            "name": name,
            "username": credential.username,
            "password": credential.password,  # Will be masked later
            "status": status_map.get(credential.status, "Active"),
            "last_used": credential.last_used,
            "category": category,
            "tags": tags,
            "notes": notes
        }
        
        # Mask sensitive data
        return mask_sensitive_data(credential_data)
    
    @staticmethod
    def get_credential_type_metadata(credential_type: str) -> Dict[str, Any]:
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
                "category": "basic",
                "schema": {
                    "type": "object",
                    "required": ["username", "password"],
                    "properties": {
                        "username": {"type": "string", "title": "Username"},
                        "password": {"type": "string", "title": "Password", "format": "password"}
                    }
                }
            },
            "api_key": {
                "id": "api_key",
                "name": "API Key",
                "description": "API key credentials",
                "icon": "api-key",
                "category": "api",
                "schema": {
                    "type": "object",
                    "required": ["key"],
                    "properties": {
                        "key": {"type": "string", "title": "API Key"},
                        "header_name": {"type": "string", "title": "Header Name", "default": "X-API-Key"}
                    }
                }
            },
            "oauth2": {
                "id": "oauth2",
                "name": "OAuth 2.0",
                "description": "OAuth 2.0 credentials",
                "icon": "oauth",
                "category": "oauth",
                "schema": {
                    "type": "object",
                    "required": ["client_id", "client_secret"],
                    "properties": {
                        "client_id": {"type": "string", "title": "Client ID"},
                        "client_secret": {"type": "string", "title": "Client Secret", "format": "password"},
                        "token_url": {"type": "string", "title": "Token URL"},
                        "scope": {"type": "string", "title": "Scope"}
                    }
                }
            },
            "certificate": {
                "id": "certificate",
                "name": "Certificate",
                "description": "Certificate credentials",
                "icon": "certificate",
                "category": "security",
                "schema": {
                    "type": "object",
                    "required": ["certificate_path"],
                    "properties": {
                        "certificate_path": {"type": "string", "title": "Certificate Path"},
                        "private_key_path": {"type": "string", "title": "Private Key Path"},
                        "passphrase": {"type": "string", "title": "Passphrase", "format": "password"}
                    }
                }
            }
        }
        
        # Return metadata for the credential type, or a default if not found
        return metadata.get(credential_type, {
            "id": credential_type,
            "name": credential_type.capitalize(),
            "description": f"{credential_type.capitalize()} credentials",
            "icon": "credential",
            "category": "other",
            "schema": {
                "type": "object",
                "properties": {}
            }
        })
