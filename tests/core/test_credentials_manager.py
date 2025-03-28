"""Tests for the credentials manager"""
# pylint: disable=redefined-outer-name
import os
from pathlib import Path
from typing import Dict, Any
from unittest.mock import MagicMock, patch

import pytest

from src.core.interfaces import StorageInterface


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Return a mock configuration for testing"""
    return {
        "storage_path": "credentials.json",
        "encryption_key": "test_key",
    }


@pytest.fixture
def mock_credentials() -> Dict[str, Dict[str, str]]:
    """Return mock credentials for testing"""
    return {
        "site1": {
            "username": "user1",
            "password": "pass1",
        },
        "site2": {
            "username": "user2",
            "password": "pass2",
        },
    }


def test_credentials_manager_implements_interface():
    """Test that CredentialsManager implements the StorageInterface"""
    # This will fail until we implement the CredentialsManager class
    from src.core.credentials_manager import CredentialsManager
    
    # Check that CredentialsManager is a subclass of StorageInterface
    assert issubclass(CredentialsManager, StorageInterface)


def test_credentials_manager_initialization(mock_config):
    """Test that CredentialsManager initializes correctly"""
    # This will fail until we implement the CredentialsManager class
    from src.core.credentials_manager import CredentialsManager
    
    # Create an instance of CredentialsManager
    manager = CredentialsManager(mock_config)
    
    # Check that the config was stored
    assert manager.config == mock_config
    
    # Check that the storage path was set correctly
    assert manager.storage_path == Path(mock_config["storage_path"])
    
    # Check that the encryption key was set correctly
    assert manager.encryption_key == mock_config["encryption_key"]


def test_credentials_manager_save_and_load(mock_config, mock_credentials, tmp_path):
    """Test that CredentialsManager can save and load credentials"""
    # This will fail until we implement the CredentialsManager class
    from src.core.credentials_manager import CredentialsManager
    
    # Update the config to use a temporary file
    config = mock_config.copy()
    config["storage_path"] = str(tmp_path / "credentials.json")
    
    # Create an instance of CredentialsManager
    manager = CredentialsManager(config)
    
    # Save credentials for each site
    for site, creds in mock_credentials.items():
        manager.save(site, creds)
    
    # Load credentials for each site
    for site, expected_creds in mock_credentials.items():
        loaded_creds = manager.load(site)
        assert loaded_creds == expected_creds


def test_credentials_manager_list_keys(mock_config, mock_credentials, tmp_path):
    """Test that CredentialsManager can list all keys"""
    # This will fail until we implement the CredentialsManager class
    from src.core.credentials_manager import CredentialsManager
    
    # Update the config to use a temporary file
    config = mock_config.copy()
    config["storage_path"] = str(tmp_path / "credentials.json")
    
    # Create an instance of CredentialsManager
    manager = CredentialsManager(config)
    
    # Save credentials for each site
    for site, creds in mock_credentials.items():
        manager.save(site, creds)
    
    # List all keys
    keys = manager.list_keys()
    
    # Check that all sites are in the keys
    for site in mock_credentials:
        assert site in keys


def test_credentials_manager_delete(mock_config, mock_credentials, tmp_path):
    """Test that CredentialsManager can delete credentials"""
    # This will fail until we implement the CredentialsManager class
    from src.core.credentials_manager import CredentialsManager
    
    # Update the config to use a temporary file
    config = mock_config.copy()
    config["storage_path"] = str(tmp_path / "credentials.json")
    
    # Create an instance of CredentialsManager
    manager = CredentialsManager(config)
    
    # Save credentials for each site
    for site, creds in mock_credentials.items():
        manager.save(site, creds)
    
    # Delete credentials for one site
    site_to_delete = list(mock_credentials.keys())[0]
    manager.delete(site_to_delete)
    
    # Check that the site was deleted
    keys = manager.list_keys()
    assert site_to_delete not in keys
    
    # Check that other sites are still there
    for site in mock_credentials:
        if site != site_to_delete:
            assert site in keys


def test_credentials_manager_encryption(mock_config, tmp_path):
    """Test that CredentialsManager encrypts credentials"""
    # This will fail until we implement the CredentialsManager class
    from src.core.credentials_manager import CredentialsManager
    
    # Update the config to use a temporary file
    config = mock_config.copy()
    config["storage_path"] = str(tmp_path / "credentials.json")
    
    # Create an instance of CredentialsManager
    manager = CredentialsManager(config)
    
    # Save credentials
    site = "test_site"
    creds = {"username": "test_user", "password": "test_pass"}
    manager.save(site, creds)
    
    # Check that the file exists
    assert Path(config["storage_path"]).exists()
    
    # Read the file content
    content = Path(config["storage_path"]).read_text()
    
    # Check that the password is not stored in plain text
    assert "test_pass" not in content
