"""Model for credential management"""
from typing import Dict, Any, Optional, List

from src.core.credentials_manager import CredentialsManager


class CredentialModel:
    """Model for credential management"""

    def __init__(self) -> None:
        """Initialize the credential model"""
        # In a real implementation, we would get the config from a config manager
        config = {
            "storage_path": "~/.autoclick/credentials.dat",
            "encryption_key": "autoclick_default_key"
        }
        self.credentials_manager = CredentialsManager(config)

    def get_all_sites(self) -> List[str]:
        """
        Get all sites with stored credentials

        Returns:
            List of site names
        """
        return self.credentials_manager.list_keys()

    def get_credentials(self, site: str) -> Optional[Dict[str, str]]:
        """
        Get credentials for a site

        Args:
            site: Site name

        Returns:
            Credentials dictionary, or None if not found
        """
        return self.credentials_manager.load(site)

    def add_credentials(self, site: str, username: str, password: str) -> bool:
        """
        Add credentials for a site

        Args:
            site: Site name
            username: Username
            password: Password

        Returns:
            True if successful, False otherwise
        """
        try:
            self.credentials_manager.save(site, {
                "username": username,
                "password": password
            })
            return True
        except Exception:
            return False

    def update_credentials(self, site: str, username: str, password: str) -> bool:
        """
        Update credentials for a site

        Args:
            site: Site name
            username: Username
            password: Password

        Returns:
            True if successful, False otherwise
        """
        return self.add_credentials(site, username, password)

    def remove_credentials(self, site: str) -> bool:
        """
        Remove credentials for a site

        Args:
            site: Site name

        Returns:
            True if successful, False otherwise
        """
        try:
            self.credentials_manager.delete(site)
            return True
        except Exception:
            return False
