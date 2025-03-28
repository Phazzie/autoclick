"""Credential tab component"""
import logging
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Optional

from src.ui.components.base_component import BaseComponent
from src.ui.components.common import TreeviewWithScrollbar
from src.ui.interfaces.view_interface import CredentialViewInterface
from src.ui.presenters.credential_presenter import CredentialPresenter


class CredentialTab(BaseComponent, CredentialViewInterface):
    """Credential tab component"""
    
    def __init__(self, parent: Any, presenter: CredentialPresenter) -> None:
        """
        Initialize the credential tab
        
        Args:
            parent: Parent widget
            presenter: Credential presenter
        """
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.presenter = presenter
        self.presenter.set_view(self)
        
        # Create UI elements
        self._create_ui()
        
        # Load sites
        self.presenter.load_sites()
    
    def _create_ui(self) -> None:
        """Create the UI elements"""
        # Create header frame
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add title
        title_label = ttk.Label(
            header_frame,
            text="Credential Management",
            font=("Arial", 14, "bold")
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Create main content frame
        content_frame = ttk.Frame(self.frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create sites frame
        sites_frame = ttk.LabelFrame(content_frame, text="Sites")
        sites_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Create sites listbox
        self.sites_listbox = tk.Listbox(sites_frame, width=30)
        self.sites_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        sites_scrollbar = ttk.Scrollbar(
            sites_frame,
            orient=tk.VERTICAL,
            command=self.sites_listbox.yview
        )
        self.sites_listbox.configure(yscrollcommand=sites_scrollbar.set)
        sites_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.sites_listbox.bind("<<ListboxSelect>>", self._on_site_selected)
        
        # Create credentials frame
        credentials_frame = ttk.LabelFrame(content_frame, text="Credentials")
        credentials_frame.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )
        
        # Create form
        form_frame = ttk.Frame(credentials_frame)
        form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Site
        ttk.Label(form_frame, text="Site:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        
        self.site_var = tk.StringVar()
        site_entry = ttk.Entry(form_frame, textvariable=self.site_var)
        site_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Username
        ttk.Label(form_frame, text="Username:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )
        
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=self.username_var)
        username_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Password
        ttk.Label(form_frame, text="Password:").grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W
        )
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.password_var, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Configure grid
        form_frame.columnconfigure(1, weight=1)
        
        # Create buttons frame
        buttons_frame = ttk.Frame(credentials_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add buttons
        save_btn = ttk.Button(
            buttons_frame,
            text="Save",
            command=self._save_credentials
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = ttk.Button(
            buttons_frame,
            text="Remove",
            command=self._remove_credentials
        )
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            buttons_frame,
            text="Clear",
            command=self._clear_form
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def display_sites(self, sites: List[str]) -> None:
        """
        Display sites with stored credentials
        
        Args:
            sites: List of site names
        """
        # Clear listbox
        self.sites_listbox.delete(0, tk.END)
        
        # Add sites
        for site in sites:
            self.sites_listbox.insert(tk.END, site)
    
    def display_credentials(self, site: str, credentials: Dict[str, str]) -> None:
        """
        Display credentials for a site
        
        Args:
            site: Site name
            credentials: Credentials dictionary
        """
        self.site_var.set(site)
        self.username_var.set(credentials.get("username", ""))
        self.password_var.set(credentials.get("password", ""))
    
    def show_message(self, message: str) -> None:
        """
        Show a message to the user
        
        Args:
            message: The message to show
        """
        # In a real implementation, this would update a status bar or show a toast
        self.logger.info(message)
        
        # For now, just print to console
        print(message)
    
    def _on_site_selected(self, event: Any) -> None:
        """
        Handle site selection
        
        Args:
            event: Event data
        """
        # Get selected site
        selection = self.sites_listbox.curselection()
        
        if not selection:
            return
        
        site = self.sites_listbox.get(selection[0])
        
        # Load credentials
        self.presenter.load_credentials(site)
    
    def _save_credentials(self) -> None:
        """Save credentials"""
        site = self.site_var.get()
        username = self.username_var.get()
        password = self.password_var.get()
        
        self.presenter.add_credentials(site, username, password)
    
    def _remove_credentials(self) -> None:
        """Remove credentials"""
        site = self.site_var.get()
        
        self.presenter.remove_credentials(site)
    
    def _clear_form(self) -> None:
        """Clear the form"""
        self.site_var.set("")
        self.username_var.set("")
        self.password_var.set("")
