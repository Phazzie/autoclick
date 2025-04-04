"""
Script to update the application configuration to use clean architecture.

This script modifies the application initialization to use the CredentialAdapter
in clean architecture mode.
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.domain.credentials.impl.credential_service import CredentialService
from src.ui.adapters.impl.credential_adapter import CredentialAdapter


def update_app_config():
    """Update the application configuration to use clean architecture."""
    print("Updating application configuration to use clean architecture...")
    
    # Create a sample configuration file
    config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'app_config.py')
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    
    with open(config_file, 'w') as f:
        f.write("""\"\"\"
Application configuration for clean architecture.

This module provides configuration for the application to use clean architecture.
\"\"\"
from src.domain.credentials.impl.credential_service import CredentialService
from src.ui.adapters.impl.credential_adapter import CredentialAdapter


def configure_credential_adapter():
    \"\"\"
    Configure the credential adapter to use clean architecture.
    
    Returns:
        Configured credential adapter
    \"\"\"
    # Create the credential service
    credential_service = CredentialService()
    
    # Create the adapter with the service
    credential_adapter = CredentialAdapter(credential_service=credential_service)
    
    return credential_adapter
""")
    
    print(f"Configuration file created: {config_file}")
    print("To use clean architecture mode, update app.py to use this configuration.")
    print("Example:")
    print("```python")
    print("from config.app_config import configure_credential_adapter")
    print("")
    print("# In _init_services method:")
    print("self.credential_service = configure_credential_adapter()")
    print("```")


if __name__ == "__main__":
    update_app_config()
