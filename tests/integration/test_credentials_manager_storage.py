"""Integration tests for credentials manager with actual storage"""
# pylint: disable=redefined-outer-name
import os
from pathlib import Path
import json
import pytest

from src.core.credentials_manager import CredentialsManager


@pytest.fixture
def storage_path(tmp_path) -> Path:
    """Create a temporary storage path"""
    return tmp_path / "credentials.json"


@pytest.fixture
def config(storage_path) -> dict:
    """Return a configuration for testing"""
    return {
        "storage_path": str(storage_path),
        "encryption_key": "test_encryption_key",
    }


@pytest.fixture
def credentials_manager(config) -> CredentialsManager:
    """Return a credentials manager instance"""
    return CredentialsManager(config)


@pytest.fixture
def test_credentials() -> dict:
    """Return test credentials"""
    return {
        "site1": {
            "username": "user1",
            "password": "pass1",
        },
        "site2": {
            "username": "user2",
            "password": "pass2",
        },
        "site3": {
            "username": "user3",
            "password": "pass3",
        },
    }


def test_credentials_manager_save_and_load(credentials_manager, test_credentials, storage_path):
    """Test that credentials manager can save and load credentials"""
    # Check that the storage file was created
    assert storage_path.exists()
    
    # Save credentials for each site
    for site, creds in test_credentials.items():
        credentials_manager.save(site, creds)
    
    # Check that the file is not empty
    assert storage_path.stat().st_size > 0
    
    # Check that the file content is encrypted (passwords should not be visible)
    content = storage_path.read_text()
    for site, creds in test_credentials.items():
        assert creds["password"] not in content
    
    # Load credentials for each site
    for site, expected_creds in test_credentials.items():
        loaded_creds = credentials_manager.load(site)
        assert loaded_creds == expected_creds


def test_credentials_manager_list_and_delete(credentials_manager, test_credentials):
    """Test that credentials manager can list and delete credentials"""
    # Save credentials for each site
    for site, creds in test_credentials.items():
        credentials_manager.save(site, creds)
    
    # List all keys
    keys = credentials_manager.list_keys()
    
    # Check that all sites are in the keys
    for site in test_credentials:
        assert site in keys
    
    # Delete credentials for one site
    site_to_delete = list(test_credentials.keys())[0]
    credentials_manager.delete(site_to_delete)
    
    # Check that the site was deleted
    keys = credentials_manager.list_keys()
    assert site_to_delete not in keys
    
    # Check that other sites are still there
    for site in test_credentials:
        if site != site_to_delete:
            assert site in keys


def test_credentials_manager_update(credentials_manager, test_credentials):
    """Test that credentials manager can update credentials"""
    # Save credentials for a site
    site = list(test_credentials.keys())[0]
    credentials_manager.save(site, test_credentials[site])
    
    # Update the credentials
    updated_creds = {
        "username": "updated_user",
        "password": "updated_pass",
    }
    credentials_manager.save(site, updated_creds)
    
    # Load the updated credentials
    loaded_creds = credentials_manager.load(site)
    
    # Check that the credentials were updated
    assert loaded_creds == updated_creds
    assert loaded_creds != test_credentials[site]


def test_credentials_manager_with_different_key(storage_path, test_credentials):
    """Test that credentials manager requires the correct encryption key"""
    # Create a credentials manager with one key
    config1 = {
        "storage_path": str(storage_path),
        "encryption_key": "key1",
    }
    manager1 = CredentialsManager(config1)
    
    # Save credentials
    site = list(test_credentials.keys())[0]
    manager1.save(site, test_credentials[site])
    
    # Create a credentials manager with a different key
    config2 = {
        "storage_path": str(storage_path),
        "encryption_key": "key2",
    }
    manager2 = CredentialsManager(config2)
    
    # Try to load the credentials
    loaded_creds = manager2.load(site)
    
    # Check that the credentials could not be loaded
    assert loaded_creds is None
