"""
Credential Management Presenter for handling credential operations.
SOLID: Single responsibility - business logic for credential management.
KISS: Simple operations with clear error handling.
"""
from typing import Dict, List, Any, Optional, TYPE_CHECKING

from ..presenters.base_presenter import BasePresenter
from ..adapters.credential_adapter import CredentialAdapter

if TYPE_CHECKING:
    from ..views.credential_view import CredentialView
    from app import AutoClickApp

class CredentialPresenter(BasePresenter[CredentialAdapter]):
    """Presenter for the Credential Management view."""
    
    # Type hints for view and app
    view: 'CredentialView'
    app: 'AutoClickApp'
    
    def __init__(self, view: 'CredentialView', app: 'AutoClickApp', service: CredentialAdapter):
        """
        Initialize the credential presenter.
        
        Args:
            view: The credential view
            app: The main application
            service: The credential adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.credentials = []  # Cache of credentials
    
    def initialize_view(self):
        """Initialize the view with data."""
        try:
            self.load_credentials()
            self.update_app_status("Credential management initialized")
        except Exception as e:
            self._handle_error("initializing credential management", e)
    
    def load_credentials(self):
        """Load credentials from the service and update the view."""
        try:
            # Get all credentials from the service
            self.credentials = self.service.get_all_credentials()
            
            # Update the view
            self.view.update_credential_list(self.credentials)
            self.update_app_status("Credentials loaded")
        except Exception as e:
            self._handle_error("loading credentials", e)
    
    def filter_credentials(self, status: str):
        """
        Filter credentials by status.
        
        Args:
            status: Status to filter by ("All", "Active", "Success", "Failure", "Inactive")
        """
        try:
            if status == "All":
                # Show all credentials
                self.view.update_credential_list(self.credentials)
            else:
                # Show only credentials with the selected status
                filtered_credentials = [
                    cred for cred in self.credentials
                    if cred.status == status
                ]
                self.view.update_credential_list(filtered_credentials)
            
            self.update_app_status(f"Filtered credentials by {status} status")
        except Exception as e:
            self._handle_error(f"filtering credentials by {status}", e)
    
    def select_credential(self, credential_id: str):
        """
        Handle credential selection.
        
        Args:
            credential_id: ID of the selected credential
        """
        try:
            # Find the credential in the cache
            credential = None
            for cred in self.credentials:
                if cred.id == credential_id:
                    credential = cred
                    break
            
            if credential:
                # Populate the editor with the credential data
                self.view.populate_editor(credential)
                self.update_app_status(f"Selected credential: {credential.name}")
            else:
                # Credential not found
                self.view.clear_editor()
                self.view.set_editor_state(False)
                self.update_app_status(f"Credential not found: {credential_id}")
        except Exception as e:
            self._handle_error(f"selecting credential {credential_id}", e)
    
    def save_credential(self, credential_data: Dict[str, Any]):
        """
        Save a credential.
        
        Args:
            credential_data: Dictionary containing the credential data
        """
        try:
            # Validate the credential data
            username = credential_data.get("username", "").strip()
            if not username:
                self.view.show_validation_error("Username is required")
                return
            
            password = credential_data.get("password", "").strip()
            if not password:
                self.view.show_validation_error("Password is required")
                return
            
            name = credential_data.get("name", "").strip()
            if not name:
                # Use username as name if not provided
                name = username
            
            # Check if this is a new credential or an update
            credential_id = credential_data.get("id", "")
            
            # Prepare tags
            tags = credential_data.get("tags", [])
            
            # Save the credential
            if not credential_id:
                # Create a new credential
                self.service.add_credential(
                    name=name,
                    username=username,
                    password=password,
                    category=credential_data.get("category", "Other"),
                    tags=tags,
                    notes=credential_data.get("notes", "")
                )
                self.update_app_status(f"Created credential: {name}")
            else:
                # Update an existing credential
                self.service.update_credential(
                    cid=credential_id,
                    name=name,
                    username=username,
                    password=password,
                    status=credential_data.get("status", "Active"),
                    category=credential_data.get("category", "Other"),
                    tags=tags,
                    notes=credential_data.get("notes", "")
                )
                self.update_app_status(f"Updated credential: {name}")
            
            # Reload credentials to refresh the view
            self.load_credentials()
            
            # Select the saved credential
            if not credential_id:
                # For new credentials, find by username
                for cred in self.credentials:
                    if cred.username == username:
                        self.select_credential(cred.id)
                        break
            else:
                # For updates, use the existing ID
                self.select_credential(credential_id)
        except Exception as e:
            self._handle_error(f"saving credential {credential_data.get('name', '')}", e)
    
    def delete_credential(self, credential_id: str):
        """
        Delete a credential.
        
        Args:
            credential_id: ID of the credential to delete
        """
        try:
            # Find the credential in the cache
            credential_name = credential_id
            for cred in self.credentials:
                if cred.id == credential_id:
                    credential_name = cred.name
                    break
            
            # Confirm deletion
            if not self.view.ask_yes_no("Confirm Delete", f"Are you sure you want to delete the credential '{credential_name}'?"):
                return
            
            # Delete the credential
            success = self.service.delete_credential(credential_id)
            
            if success:
                self.update_app_status(f"Deleted credential: {credential_name}")
                
                # Reload credentials to refresh the view
                self.load_credentials()
                
                # Clear the editor
                self.view.clear_editor()
                self.view.set_editor_state(False)
            else:
                self.view.display_error("Delete Failed", f"Failed to delete credential: {credential_name}")
        except Exception as e:
            self._handle_error(f"deleting credential {credential_id}", e)
