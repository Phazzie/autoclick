"""
Adapter for CredentialManager to provide the interface expected by the UI.
SOLID: Single responsibility - adapting credential operations.
KISS: Simple delegation to CredentialManager.
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.core.credentials.credential_manager import CredentialManager, CredentialStatus
from src.core.models import CredentialRecord as UICredentialRecord

class CredentialAdapter:
    """Adapter for CredentialManager to provide the interface expected by the UI."""
    
    def __init__(self, credential_manager: CredentialManager):
        """Initialize the adapter with a CredentialManager instance."""
        self.credential_manager = credential_manager
    
    def get_all_credentials(self) -> List[UICredentialRecord]:
        """
        Get all credentials.
        
        Returns:
            List of credential records in the UI-expected format.
        """
        # Convert backend CredentialRecord objects to UI CredentialRecord objects
        ui_credentials = []
        for username, record in self.credential_manager.credentials.items():
            ui_credentials.append(self._convert_to_ui_record(username, record))
        return ui_credentials
    
    def get_credential_by_id(self, cid: str) -> Optional[UICredentialRecord]:
        """
        Get a credential by ID.
        
        Args:
            cid: Credential ID (username in the backend)
            
        Returns:
            Credential record in the UI-expected format, or None if not found.
        """
        record = self.credential_manager.credentials.get(cid)
        if record:
            return self._convert_to_ui_record(cid, record)
        return None
    
    def add_credential(self, name: str, username: str, password: str, category: str = "Other", tags: List[str] = None, notes: str = "") -> UICredentialRecord:
        """
        Add a new credential.
        
        Args:
            name: Display name for the credential
            username: Username
            password: Password
            category: Category for grouping
            tags: List of tags
            notes: Additional notes
            
        Returns:
            The new credential record in the UI-expected format.
        """
        # Create metadata for UI-specific fields
        metadata = {
            "name": name,
            "category": category,
            "tags": tags or [],
            "notes": notes
        }
        
        # Add the credential to the backend
        record = self.credential_manager.add_credential(
            username=username,
            password=password,
            status=CredentialStatus.UNUSED,
            metadata=metadata
        )
        
        # Return the UI-expected format
        return self._convert_to_ui_record(username, record)
    
    def update_credential(self, cid: str, name: str, username: str, password: str, status: str = "Active", category: str = "Other", tags: List[str] = None, notes: str = "") -> Optional[UICredentialRecord]:
        """
        Update an existing credential.
        
        Args:
            cid: Credential ID (username in the backend)
            name: Display name for the credential
            username: Username
            password: Password
            status: Status string
            category: Category for grouping
            tags: List of tags
            notes: Additional notes
            
        Returns:
            The updated credential record in the UI-expected format, or None if not found.
        """
        # Check if the credential exists
        record = self.credential_manager.credentials.get(cid)
        if not record:
            return None
        
        # Update the credential in the backend
        record.username = username
        record.password = password
        
        # Map UI status to backend status
        if status == "Active":
            record.status = CredentialStatus.UNUSED
        elif status == "Inactive":
            record.status = CredentialStatus.BLACKLISTED
        elif status == "Success":
            record.status = CredentialStatus.SUCCESS
        elif status == "Failure":
            record.status = CredentialStatus.FAILURE
        
        # Update metadata for UI-specific fields
        record.metadata = {
            "name": name,
            "category": category,
            "tags": tags or [],
            "notes": notes
        }
        
        # If the ID (username) changed, we need to update the dictionary key
        if cid != username:
            self.credential_manager.credentials[username] = record
            del self.credential_manager.credentials[cid]
        
        # Return the UI-expected format
        return self._convert_to_ui_record(username, record)
    
    def delete_credential(self, cid: str) -> bool:
        """
        Delete a credential.
        
        Args:
            cid: Credential ID (username in the backend)
            
        Returns:
            True if the credential was deleted, False if not found.
        """
        if cid in self.credential_manager.credentials:
            del self.credential_manager.credentials[cid]
            return True
        return False
    
    def _convert_to_ui_record(self, username: str, record) -> UICredentialRecord:
        """
        Convert a backend CredentialRecord to a UI CredentialRecord.
        
        Args:
            username: Username (used as ID)
            record: Backend CredentialRecord
            
        Returns:
            UI CredentialRecord
        """
        # Map backend status to UI status
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
        metadata = record.metadata or {}
        name = metadata.get("name", username)
        category = metadata.get("category", "Other")
        tags = metadata.get("tags", [])
        notes = metadata.get("notes", "")
        
        # Create UI CredentialRecord
        return UICredentialRecord(
            id=username,
            name=name,
            username=username,
            password=record.password,
            status=status_map.get(record.status, "Active"),
            last_used=record.last_used,
            category=category,
            tags=tags,
            notes=notes
        )
