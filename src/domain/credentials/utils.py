"""
Credential utilities.

This module provides utility functions for credential management.
"""
from typing import Dict, Any, Optional

from src.core.credentials.credential_manager import CredentialStatus


def get_status_map() -> Dict[CredentialStatus, str]:
    """
    Get a mapping from CredentialStatus to string representation.
    
    Returns:
        Dictionary mapping CredentialStatus to string
    """
    return {
        CredentialStatus.UNUSED: "Active",
        CredentialStatus.SUCCESS: "Success",
        CredentialStatus.FAILURE: "Failure",
        CredentialStatus.LOCKED: "Inactive",
        CredentialStatus.EXPIRED: "Inactive",
        CredentialStatus.INVALID: "Inactive",
        CredentialStatus.BLACKLISTED: "Inactive"
    }


def get_status_from_string(status_str: str) -> CredentialStatus:
    """
    Convert a string status to CredentialStatus.
    
    Args:
        status_str: String representation of status
        
    Returns:
        CredentialStatus enum value
    """
    status_map = {
        "Active": CredentialStatus.UNUSED,
        "Success": CredentialStatus.SUCCESS,
        "Failure": CredentialStatus.FAILURE,
        "Inactive": CredentialStatus.BLACKLISTED
    }
    
    return status_map.get(status_str, CredentialStatus.UNUSED)


def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mask sensitive data in a dictionary.
    
    Args:
        data: Dictionary containing sensitive data
        
    Returns:
        Dictionary with sensitive data masked
    """
    # Create a copy of the data
    masked_data = data.copy()
    
    # Mask sensitive fields
    sensitive_fields = ["password", "secret", "key", "token", "access_token", "refresh_token", "private_key", "client_secret"]
    
    for field in sensitive_fields:
        if field in masked_data and masked_data[field]:
            masked_data[field] = "********"
    
    return masked_data


def extract_metadata(credential_data: Dict[str, Any], username: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract metadata from credential data.
    
    Args:
        credential_data: Credential data
        username: Optional username to use as default name
        
    Returns:
        Metadata dictionary
    """
    name = credential_data.get("name", username)
    category = credential_data.get("category", "Other")
    tags = credential_data.get("tags", [])
    notes = credential_data.get("notes", "")
    credential_type = credential_data.get("type", "username_password")
    
    return {
        "name": name,
        "category": category,
        "tags": tags,
        "notes": notes,
        "type": credential_type
    }
