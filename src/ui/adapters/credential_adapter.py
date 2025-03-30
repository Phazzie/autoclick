"""
Adapter for CredentialManager to provide the interface expected by the UI.
SOLID: Single responsibility - adapting credential operations.
KISS: Simple delegation to CredentialManager.
"""
import uuid
import base64
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.core.credentials.credential_manager import CredentialManager, CredentialStatus
from src.core.models import CredentialRecord as UICredentialRecord

class CredentialAdapter:
    """Adapter for CredentialManager to provide the interface expected by the UI."""

    def __init__(self, credential_manager: CredentialManager):
        """Initialize the adapter with a CredentialManager instance."""
        self.credential_manager = credential_manager

        # Initialize encryption key
        self._initialize_encryption()

    def _initialize_encryption(self):
        """Initialize encryption for secure password handling."""
        # Check if encryption key exists, if not create one
        key_file = os.path.join(os.path.dirname(__file__), '../../../.encryption_key')

        if os.path.exists(key_file):
            # Load existing key
            with open(key_file, 'rb') as f:
                self.key = f.read()
        else:
            # Generate a new key
            salt = os.urandom(16)
            # Use a default password for development - in production this should be more secure
            password = b"autoclick_default_password"

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            self.key = base64.urlsafe_b64encode(kdf.derive(password))

            # Save the key
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(self.key)

        # Create Fernet cipher for encryption/decryption
        self.cipher = Fernet(self.key)

    def _encrypt_password(self, password: str) -> str:
        """Encrypt a password."""
        return self.cipher.encrypt(password.encode()).decode()

    def _decrypt_password(self, encrypted_password: str) -> str:
        """Decrypt a password."""
        try:
            return self.cipher.decrypt(encrypted_password.encode()).decode()
        except Exception:
            # If decryption fails, return a placeholder
            return "[ENCRYPTED]"

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

        # Encrypt the password before storing
        encrypted_password = self._encrypt_password(password)

        # Add the credential to the backend
        record = self.credential_manager.add_credential(
            username=username,
            password=encrypted_password,  # Store encrypted password
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
        # Encrypt the password before storing
        record.password = self._encrypt_password(password)

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
        # Decrypt the password for display
        try:
            decrypted_password = self._decrypt_password(record.password)
        except Exception:
            # If decryption fails, it might not be encrypted yet
            decrypted_password = record.password

        return UICredentialRecord(
            id=username,
            name=name,
            username=username,
            password=decrypted_password,
            status=status_map.get(record.status, "Active"),
            last_used=record.last_used,
            category=category,
            tags=tags,
            notes=notes
        )

    def import_from_csv(self, file_path: str) -> int:
        """
        Import credentials from a CSV file.

        Args:
            file_path: Path to the CSV file

        Returns:
            Number of credentials imported
        """
        import csv

        count = 0
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Skip rows without required fields
                if 'username' not in row or 'password' not in row:
                    continue

                # Extract fields
                username = row['username']
                password = row['password']
                name = row.get('name', username)
                category = row.get('category', 'Other')
                notes = row.get('notes', '')

                # Extract tags if present
                tags = []
                if 'tags' in row:
                    tags = [tag.strip() for tag in row['tags'].split(',') if tag.strip()]

                # Add the credential
                self.add_credential(
                    name=name,
                    username=username,
                    password=password,
                    category=category,
                    tags=tags,
                    notes=notes
                )

                count += 1

        return count

    def import_from_json(self, file_path: str) -> int:
        """
        Import credentials from a JSON file.

        Args:
            file_path: Path to the JSON file

        Returns:
            Number of credentials imported
        """
        import json

        count = 0
        with open(file_path, 'r') as jsonfile:
            data = json.load(jsonfile)

            # Handle different JSON formats
            if isinstance(data, list):
                # List of credentials
                credentials = data
            elif isinstance(data, dict) and 'credentials' in data:
                # Object with credentials array
                credentials = data['credentials']
            else:
                # Single credential object
                credentials = [data]

            for cred in credentials:
                # Skip entries without required fields
                if 'username' not in cred or 'password' not in cred:
                    continue

                # Extract fields
                username = cred['username']
                password = cred['password']
                name = cred.get('name', username)
                category = cred.get('category', 'Other')
                notes = cred.get('notes', '')

                # Extract tags
                tags = cred.get('tags', [])

                # Add the credential
                self.add_credential(
                    name=name,
                    username=username,
                    password=password,
                    category=category,
                    tags=tags,
                    notes=notes
                )

                count += 1

        return count

    def export_to_csv(self, file_path: str) -> int:
        """
        Export credentials to a CSV file.

        Args:
            file_path: Path to the CSV file

        Returns:
            Number of credentials exported
        """
        import csv

        # Get all credentials
        credentials = self.get_all_credentials()

        # Write to CSV
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['name', 'username', 'password', 'status', 'category', 'tags', 'notes', 'last_used']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for cred in credentials:
                writer.writerow({
                    'name': cred.name,
                    'username': cred.username,
                    'password': cred.password,
                    'status': cred.status,
                    'category': cred.category,
                    'tags': ','.join(cred.tags),
                    'notes': cred.notes,
                    'last_used': cred.last_used.isoformat() if cred.last_used else ''
                })

        return len(credentials)

    def export_to_json(self, file_path: str) -> int:
        """
        Export credentials to a JSON file.

        Args:
            file_path: Path to the JSON file

        Returns:
            Number of credentials exported
        """
        import json

        # Get all credentials
        credentials = self.get_all_credentials()

        # Convert to serializable format
        cred_list = []
        for cred in credentials:
            cred_list.append({
                'name': cred.name,
                'username': cred.username,
                'password': cred.password,
                'status': cred.status,
                'category': cred.category,
                'tags': cred.tags,
                'notes': cred.notes,
                'last_used': cred.last_used.isoformat() if cred.last_used else None
            })

        # Write to JSON
        with open(file_path, 'w') as jsonfile:
            json.dump({'credentials': cred_list}, jsonfile, indent=2)

        return len(credentials)

    def update_credentials_status(self, target_status: str, new_status: str) -> int:
        """
        Update the status of credentials matching a target status.

        Args:
            target_status: Status to match
            new_status: New status to set

        Returns:
            Number of credentials updated
        """
        # Map UI status to backend status
        status_map = {
            "Active": CredentialStatus.UNUSED,
            "Success": CredentialStatus.SUCCESS,
            "Failure": CredentialStatus.FAILURE,
            "Inactive": CredentialStatus.LOCKED
        }

        # Get backend status values
        target_backend_status = status_map.get(target_status)
        new_backend_status = status_map.get(new_status)

        if not target_backend_status or not new_backend_status:
            return 0

        # Update credentials
        count = 0
        for username, record in list(self.credential_manager.credentials.items()):
            if record.status == target_backend_status:
                record.status = new_backend_status
                count += 1

        return count

    def delete_credentials_by_status(self, target_status: str) -> int:
        """
        Delete credentials matching a target status.

        Args:
            target_status: Status to match

        Returns:
            Number of credentials deleted
        """
        # Map UI status to backend status
        status_map = {
            "Active": CredentialStatus.UNUSED,
            "Success": CredentialStatus.SUCCESS,
            "Failure": CredentialStatus.FAILURE,
            "Inactive": CredentialStatus.LOCKED
        }

        # Get backend status value
        target_backend_status = status_map.get(target_status)

        if not target_backend_status:
            return 0

        # Delete credentials
        count = 0
        for username, record in list(self.credential_manager.credentials.items()):
            if record.status == target_backend_status:
                del self.credential_manager.credentials[username]
                count += 1

        return count