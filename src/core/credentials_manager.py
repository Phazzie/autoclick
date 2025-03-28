"""Credentials manager for securely storing and retrieving credentials"""
import base64
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.core.interfaces import StorageInterface


class CredentialsManager(StorageInterface):
    """Manages secure storage and retrieval of credentials"""

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize the credentials manager
        
        Args:
            config: Configuration dictionary with storage_path and encryption_key
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.storage_path = Path(config["storage_path"])
        self.encryption_key = config["encryption_key"]
        self.cipher = self._create_cipher()
        self._ensure_storage_exists()
    
    def _create_cipher(self) -> Fernet:
        """
        Create a cipher for encryption/decryption
        
        Returns:
            Fernet cipher
        """
        # Derive a key from the encryption key
        salt = b"autoclick_salt"  # In a real app, this would be stored securely
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.encryption_key.encode()))
        return Fernet(key)
    
    def _ensure_storage_exists(self) -> None:
        """Ensure the storage file exists"""
        if not self.storage_path.exists():
            self.logger.info(f"Creating credentials storage at {self.storage_path}")
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            self._write_data({})
    
    def _read_data(self) -> Dict[str, Any]:
        """
        Read and decrypt data from storage
        
        Returns:
            Dictionary of stored data
        """
        if not self.storage_path.exists():
            return {}
        
        try:
            encrypted_data = self.storage_path.read_bytes()
            if not encrypted_data:
                return {}
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except Exception as e:
            self.logger.error(f"Error reading credentials: {str(e)}")
            return {}
    
    def _write_data(self, data: Dict[str, Any]) -> None:
        """
        Encrypt and write data to storage
        
        Args:
            data: Dictionary of data to store
        """
        try:
            json_data = json.dumps(data)
            encrypted_data = self.cipher.encrypt(json_data.encode())
            self.storage_path.write_bytes(encrypted_data)
        except Exception as e:
            self.logger.error(f"Error writing credentials: {str(e)}")
    
    def save(self, key: str, data: Any) -> None:
        """
        Save data with the given key
        
        Args:
            key: Key to store the data under
            data: Data to store
        """
        self.logger.info(f"Saving credentials for {key}")
        all_data = self._read_data()
        all_data[key] = data
        self._write_data(all_data)
    
    def load(self, key: str) -> Any:
        """
        Load data for the given key
        
        Args:
            key: Key to load data for
            
        Returns:
            Stored data, or None if not found
        """
        self.logger.info(f"Loading credentials for {key}")
        all_data = self._read_data()
        return all_data.get(key)
    
    def delete(self, key: str) -> None:
        """
        Delete data for the given key
        
        Args:
            key: Key to delete data for
        """
        self.logger.info(f"Deleting credentials for {key}")
        all_data = self._read_data()
        if key in all_data:
            del all_data[key]
            self._write_data(all_data)
    
    def list_keys(self) -> List[str]:
        """
        List all available keys
        
        Returns:
            List of keys
        """
        self.logger.info("Listing all credential keys")
        all_data = self._read_data()
        return list(all_data.keys())
