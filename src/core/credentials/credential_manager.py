"""Credential management for tracking and filtering credentials"""
import csv
import json
import logging
import os
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple


class CredentialStatus(Enum):
    """Status of a credential"""

    UNUSED = auto()  # Credential has not been used yet
    SUCCESS = auto()  # Credential was used successfully
    FAILURE = auto()  # Credential failed to authenticate
    LOCKED = auto()  # Account is locked or requires additional verification
    EXPIRED = auto()  # Credential has expired
    INVALID = auto()  # Credential format is invalid
    BLACKLISTED = auto()  # Credential has been blacklisted


class CredentialRecord:
    """
    Record of a credential and its usage history

    This class tracks a credential and its usage history, including
    success/failure status, timestamps, and additional metadata.
    """

    def __init__(
        self,
        username: str,
        password: str,
        status: CredentialStatus = CredentialStatus.UNUSED,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the credential record

        Args:
            username: Username or identifier
            password: Password or secret
            status: Initial status of the credential
            metadata: Additional metadata for the credential
        """
        self.username = username
        self.password = password
        self.status = status
        self.metadata = metadata or {}
        self.attempts = 0
        self.last_used = None
        self.last_result = None
        self.history = []

    def record_attempt(
        self,
        success: bool,
        message: str,
        status: Optional[CredentialStatus] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record an authentication attempt

        Args:
            success: Whether the attempt was successful
            message: Result message
            status: New status for the credential (if None, will be set based on success)
            metadata: Additional metadata for the attempt
        """
        # Increment attempt counter
        self.attempts += 1

        # Set timestamp
        timestamp = datetime.now()
        self.last_used = timestamp

        # Set result
        self.last_result = {
            "success": success,
            "message": message,
            "timestamp": timestamp,
            "metadata": metadata or {},
        }

        # Add to history
        self.history.append(self.last_result)

        # Update status
        if status:
            self.status = status
        elif success:
            self.status = CredentialStatus.SUCCESS
        else:
            self.status = CredentialStatus.FAILURE

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the credential record to a dictionary

        Returns:
            Dictionary representation of the credential record
        """
        return {
            "username": self.username,
            "password": self.password,
            "status": self.status.name,
            "attempts": self.attempts,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "last_result": self.last_result,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CredentialRecord":
        """
        Create a credential record from a dictionary

        Args:
            data: Dictionary representation of the credential record

        Returns:
            Credential record
        """
        # Create the record
        record = cls(
            username=data["username"],
            password=data["password"],
            status=CredentialStatus[data["status"]]
            if "status" in data
            else CredentialStatus.UNUSED,
            metadata=data.get("metadata", {}),
        )

        # Set additional properties
        record.attempts = data.get("attempts", 0)

        if "last_used" in data and data["last_used"]:
            record.last_used = datetime.fromisoformat(data["last_used"])

        record.last_result = data.get("last_result")
        record.history = data.get("history", [])

        return record


class CredentialManager:
    """
    Manager for tracking and filtering credentials

    This class manages a set of credentials, tracks their usage,
    and provides methods for filtering and exporting them.
    """

    def __init__(self):
        """Initialize the credential manager"""
        self.credentials: Dict[str, CredentialRecord] = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_credential(
        self,
        username: str,
        password: str,
        status: CredentialStatus = CredentialStatus.UNUSED,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CredentialRecord:
        """
        Add a credential to the manager

        Args:
            username: Username or identifier
            password: Password or secret
            status: Initial status of the credential
            metadata: Additional metadata for the credential

        Returns:
            The credential record
        """
        # Create the credential record
        record = CredentialRecord(username, password, status, metadata)

        # Add to the credentials dictionary
        self.credentials[username] = record

        return record

    def get_credential(self, username: str) -> Optional[CredentialRecord]:
        """
        Get a credential by username

        Args:
            username: Username to look up

        Returns:
            Credential record, or None if not found
        """
        return self.credentials.get(username)

    def record_attempt(
        self,
        username: str,
        success: bool,
        message: str,
        status: Optional[CredentialStatus] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record an authentication attempt for a credential

        Args:
            username: Username of the credential
            success: Whether the attempt was successful
            message: Result message
            status: New status for the credential
            metadata: Additional metadata for the attempt

        Raises:
            KeyError: If the credential is not found
        """
        # Get the credential record
        record = self.get_credential(username)

        if not record:
            raise KeyError(f"Credential not found: {username}")

        # Record the attempt
        record.record_attempt(success, message, status, metadata)

    def get_credentials_by_status(
        self, status: CredentialStatus
    ) -> List[CredentialRecord]:
        """
        Get credentials by status

        Args:
            status: Status to filter by

        Returns:
            List of credential records with the specified status
        """
        return [
            record for record in self.credentials.values() if record.status == status
        ]

    def get_failed_credentials(self) -> List[CredentialRecord]:
        """
        Get credentials that have failed authentication

        Returns:
            List of credential records with failure status
        """
        return self.get_credentials_by_status(CredentialStatus.FAILURE)

    def get_successful_credentials(self) -> List[CredentialRecord]:
        """
        Get credentials that have successfully authenticated

        Returns:
            List of credential records with success status
        """
        return self.get_credentials_by_status(CredentialStatus.SUCCESS)

    def get_unused_credentials(self) -> List[CredentialRecord]:
        """
        Get credentials that have not been used

        Returns:
            List of credential records with unused status
        """
        return self.get_credentials_by_status(CredentialStatus.UNUSED)

    def remove_credential(self, username: str) -> bool:
        """
        Remove a credential from the manager

        Args:
            username: Username of the credential to remove

        Returns:
            True if the credential was removed, False if not found
        """
        if username in self.credentials:
            del self.credentials[username]
            return True
        return False

    def remove_credentials_by_status(self, status: CredentialStatus) -> int:
        """
        Remove credentials with a specific status

        Args:
            status: Status to filter by

        Returns:
            Number of credentials removed
        """
        # Get usernames to remove
        usernames = [
            record.username
            for record in self.credentials.values()
            if record.status == status
        ]

        # Remove the credentials
        for username in usernames:
            self.remove_credential(username)

        return len(usernames)

    def remove_failed_credentials(self) -> int:
        """
        Remove credentials that have failed authentication

        Returns:
            Number of credentials removed
        """
        return self.remove_credentials_by_status(CredentialStatus.FAILURE)

    def update_credential_status(self, username: str, status: CredentialStatus) -> bool:
        """
        Update the status of a credential

        Args:
            username: Username of the credential to update
            status: New status for the credential

        Returns:
            True if the credential was updated, False if not found
        """
        record = self.get_credential(username)
        if record:
            record.status = status
            return True
        return False

    def update_credentials_status(
        self, from_status: CredentialStatus, to_status: CredentialStatus
    ) -> int:
        """
        Update the status of all credentials with a specific status

        Args:
            from_status: Current status to match
            to_status: New status to set

        Returns:
            Number of credentials updated
        """
        # Get credentials with the specified status
        records = self.get_credentials_by_status(from_status)

        # Update their status
        for record in records:
            record.status = to_status

        return len(records)

    def load_from_csv(
        self,
        file_path: str,
        username_field: str = "username",
        password_field: str = "password",
        delimiter: str = ",",
    ) -> int:
        """
        Load credentials from a CSV file

        Args:
            file_path: Path to the CSV file
            username_field: Name of the username field
            password_field: Name of the password field
            delimiter: Field delimiter

        Returns:
            Number of credentials loaded

        Raises:
            FileNotFoundError: If the file does not exist
            IOError: If the file cannot be read
        """
        try:
            # Open the CSV file
            with open(file_path, "r", newline="") as file:
                # Create a CSV reader
                reader = csv.DictReader(file, delimiter=delimiter)

                # Check that the required fields are present
                if (
                    username_field not in reader.fieldnames
                    or password_field not in reader.fieldnames
                ):
                    raise ValueError(
                        f"CSV file must contain {username_field} and {password_field} fields"
                    )

                # Load the credentials
                count = 0
                for row in reader:
                    username = row[username_field]
                    password = row[password_field]

                    # Create metadata from other fields
                    metadata = {
                        key: value
                        for key, value in row.items()
                        if key not in [username_field, password_field]
                    }

                    # Add the credential
                    self.add_credential(username, password, metadata=metadata)
                    count += 1

                self.logger.info(f"Loaded {count} credentials from {file_path}")
                return count

        except (FileNotFoundError, IOError) as e:
            self.logger.error(f"Failed to load credentials from {file_path}: {str(e)}")
            raise

    def save_to_csv(
        self,
        file_path: str,
        username_field: str = "username",
        password_field: str = "password",
        include_status: bool = True,
        include_metadata: bool = True,
        delimiter: str = ",",
        filter_status: Optional[Set[CredentialStatus]] = None,
    ) -> int:
        """
        Save credentials to a CSV file

        Args:
            file_path: Path to the CSV file
            username_field: Name of the username field
            password_field: Name of the password field
            include_status: Whether to include the status field
            include_metadata: Whether to include metadata fields
            delimiter: Field delimiter
            filter_status: Set of statuses to include (None for all)

        Returns:
            Number of credentials saved

        Raises:
            IOError: If the file cannot be written
        """
        try:
            # Get the credentials to save
            if filter_status:
                credentials = [
                    record
                    for record in self.credentials.values()
                    if record.status in filter_status
                ]
            else:
                credentials = list(self.credentials.values())

            # If there are no credentials, don't create the file
            if not credentials:
                self.logger.warning(f"No credentials to save to {file_path}")
                return 0

            # Determine the fieldnames
            fieldnames = [username_field, password_field]

            if include_status:
                fieldnames.append("status")

            if include_metadata:
                # Get all metadata keys
                metadata_keys = set()
                for record in credentials:
                    metadata_keys.update(record.metadata.keys())

                # Add metadata fields
                fieldnames.extend(sorted(metadata_keys))

            # Open the CSV file
            with open(file_path, "w", newline="") as file:
                # Create a CSV writer
                writer = csv.DictWriter(
                    file, fieldnames=fieldnames, delimiter=delimiter
                )

                # Write the header
                writer.writeheader()

                # Write the credentials
                for record in credentials:
                    row = {
                        username_field: record.username,
                        password_field: record.password,
                    }

                    if include_status:
                        row["status"] = record.status.name

                    if include_metadata:
                        for key, value in record.metadata.items():
                            row[key] = value

                    writer.writerow(row)

                self.logger.info(f"Saved {len(credentials)} credentials to {file_path}")
                return len(credentials)

        except IOError as e:
            self.logger.error(f"Failed to save credentials to {file_path}: {str(e)}")
            raise

    def load_from_json(self, file_path: str) -> int:
        """
        Load credentials from a JSON file

        Args:
            file_path: Path to the JSON file

        Returns:
            Number of credentials loaded

        Raises:
            FileNotFoundError: If the file does not exist
            IOError: If the file cannot be read
            json.JSONDecodeError: If the file contains invalid JSON
        """
        try:
            # Open the JSON file
            with open(file_path, "r") as file:
                # Load the JSON data
                data = json.load(file)

                # Check that the data is a list
                if not isinstance(data, list):
                    raise ValueError("JSON file must contain a list of credentials")

                # Load the credentials
                count = 0
                for item in data:
                    # Check that the item is a dictionary
                    if not isinstance(item, dict):
                        continue

                    # Check that the required fields are present
                    if "username" not in item or "password" not in item:
                        continue

                    # Create the credential record
                    record = CredentialRecord.from_dict(item)

                    # Add to the credentials dictionary
                    self.credentials[record.username] = record
                    count += 1

                self.logger.info(f"Loaded {count} credentials from {file_path}")
                return count

        except (FileNotFoundError, IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to load credentials from {file_path}: {str(e)}")
            raise

    def save_to_json(
        self,
        file_path: str,
        include_history: bool = False,
        filter_status: Optional[Set[CredentialStatus]] = None,
    ) -> int:
        """
        Save credentials to a JSON file

        Args:
            file_path: Path to the JSON file
            include_history: Whether to include the attempt history
            filter_status: Set of statuses to include (None for all)

        Returns:
            Number of credentials saved

        Raises:
            IOError: If the file cannot be written
        """
        try:
            # Get the credentials to save
            if filter_status:
                credentials = [
                    record
                    for record in self.credentials.values()
                    if record.status in filter_status
                ]
            else:
                credentials = list(self.credentials.values())

            # If there are no credentials, don't create the file
            if not credentials:
                self.logger.warning(f"No credentials to save to {file_path}")
                return 0

            # Convert the credentials to dictionaries
            data = []
            for record in credentials:
                item = record.to_dict()

                if include_history:
                    item["history"] = record.history

                data.append(item)

            # Open the JSON file
            with open(file_path, "w") as file:
                # Write the JSON data
                json.dump(data, file, indent=2)

                self.logger.info(f"Saved {len(credentials)} credentials to {file_path}")
                return len(credentials)

        except IOError as e:
            self.logger.error(f"Failed to save credentials to {file_path}: {str(e)}")
            raise

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the credentials

        Returns:
            Dictionary of statistics
        """
        # Count credentials by status
        status_counts = {}
        for status in CredentialStatus:
            status_counts[status.name] = len(self.get_credentials_by_status(status))

        # Calculate success rate
        total_used = (
            status_counts[CredentialStatus.SUCCESS.name]
            + status_counts[CredentialStatus.FAILURE.name]
        )
        success_rate = (
            status_counts[CredentialStatus.SUCCESS.name] / total_used
            if total_used > 0
            else 0
        )

        return {
            "total": len(self.credentials),
            "status_counts": status_counts,
            "success_rate": success_rate,
        }
