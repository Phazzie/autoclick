"""Credential presenter implementation"""
import logging
from typing import Dict, Optional, List

from src.ui.models.credential_model import CredentialModel
from src.ui.interfaces.view_interface import CredentialViewInterface


class CredentialPresenter:
    """Presenter for credential management"""
    
    def __init__(self, model: CredentialModel, view: Optional[CredentialViewInterface] = None) -> None:
        """
        Initialize the credential presenter
        
        Args:
            model: Credential model
            view: Credential view
        """
        self.logger = logging.getLogger(__name__)
        self.model = model
        self.view = view
    
    def set_view(self, view: CredentialViewInterface) -> None:
        """
        Set the view
        
        Args:
            view: Credential view
        """
        self.view = view
    
    def load_sites(self) -> None:
        """Load all sites with stored credentials"""
        self.logger.info("Loading sites")
        
        sites = self.model.get_all_sites()
        
        if self.view:
            self.view.display_sites(sites)
    
    def load_credentials(self, site: str) -> None:
        """
        Load credentials for a site
        
        Args:
            site: Site name
        """
        self.logger.info(f"Loading credentials for {site}")
        
        if not self.view:
            return
            
        credentials = self.model.get_credentials(site)
        
        if credentials:
            self.view.display_credentials(site, credentials)
        else:
            self.view.show_message(f"No credentials found for {site}")
    
    def add_credentials(self, site: str, username: str, password: str) -> None:
        """
        Add credentials for a site
        
        Args:
            site: Site name
            username: Username
            password: Password
        """
        self.logger.info(f"Adding credentials for {site}")
        
        if not self.view:
            return
            
        if not site:
            self.view.show_message("Site name cannot be empty")
            return
            
        if not username:
            self.view.show_message("Username cannot be empty")
            return
            
        if not password:
            self.view.show_message("Password cannot be empty")
            return
            
        # Check if site already exists
        existing_credentials = self.model.get_credentials(site)
        
        if existing_credentials:
            # Update existing credentials
            if self.model.update_credentials(site, username, password):
                self.view.show_message(f"Credentials updated for {site}")
                self.load_sites()
            else:
                self.view.show_message(f"Failed to update credentials for {site}")
        else:
            # Add new credentials
            if self.model.add_credentials(site, username, password):
                self.view.show_message(f"Credentials added for {site}")
                self.load_sites()
            else:
                self.view.show_message(f"Failed to add credentials for {site}")
    
    def remove_credentials(self, site: str) -> None:
        """
        Remove credentials for a site
        
        Args:
            site: Site name
        """
        self.logger.info(f"Removing credentials for {site}")
        
        if not self.view:
            return
            
        if not site:
            self.view.show_message("Site name cannot be empty")
            return
            
        if self.model.remove_credentials(site):
            self.view.show_message(f"Credentials removed for {site}")
            self.load_sites()
        else:
            self.view.show_message(f"Failed to remove credentials for {site}")
