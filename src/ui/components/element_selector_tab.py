"""Element selector tab component"""
import logging
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional

from src.ui.components.base_component import BaseComponent
from src.ui.interfaces.view_interface import ElementSelectorViewInterface
from src.ui.presenters.element_presenter import ElementPresenter


class ElementSelectorTab(BaseComponent, ElementSelectorViewInterface):
    """Element selector tab component"""
    
    def __init__(self, parent: Any, presenter: ElementPresenter) -> None:
        """
        Initialize the element selector tab
        
        Args:
            parent: Parent widget
            presenter: Element presenter
        """
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.presenter = presenter
        self.presenter.set_view(self)
        
        # Create UI elements
        self._create_ui()
    
    def _create_ui(self) -> None:
        """Create the UI elements"""
        # Create header frame
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add title
        title_label = ttk.Label(header_frame, text="Element Selector", font=("Arial", 14, "bold"))
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Create URL frame
        url_frame = ttk.Frame(self.frame)
        url_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add URL entry
        url_label = ttk.Label(url_frame, text="URL:")
        url_label.pack(side=tk.LEFT, padx=5)
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        url_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Add browser selection
        browser_frame = ttk.LabelFrame(url_frame, text="Browser")
        browser_frame.pack(side=tk.LEFT, padx=5)
        
        self.browser_var = tk.StringVar(value="chrome")
        chrome_radio = ttk.Radiobutton(
            browser_frame,
            text="Chrome",
            variable=self.browser_var,
            value="chrome",
            command=lambda: self.presenter.set_browser_type("chrome")
        )
        firefox_radio = ttk.Radiobutton(
            browser_frame,
            text="Firefox",
            variable=self.browser_var,
            value="firefox",
            command=lambda: self.presenter.set_browser_type("firefox")
        )
        edge_radio = ttk.Radiobutton(
            browser_frame,
            text="Edge",
            variable=self.browser_var,
            value="edge",
            command=lambda: self.presenter.set_browser_type("edge")
        )
        
        chrome_radio.pack(side=tk.LEFT, padx=5)
        firefox_radio.pack(side=tk.LEFT, padx=5)
        edge_radio.pack(side=tk.LEFT, padx=5)
        
        # Add headless mode checkbox
        headless_frame = ttk.Frame(url_frame)
        headless_frame.pack(side=tk.LEFT, padx=5)
        
        self.headless_var = tk.BooleanVar(value=False)
        headless_check = ttk.Checkbutton(
            headless_frame,
            text="Headless Mode",
            variable=self.headless_var,
            command=lambda: self.presenter.set_headless(self.headless_var.get())
        )
        headless_check.pack(side=tk.LEFT, padx=5)
        
        # Add select button
        select_btn = ttk.Button(
            url_frame,
            text="Select Element",
            command=self.presenter.select_element
        )
        select_btn.pack(side=tk.LEFT, padx=5)
        
        # Create properties frame
        properties_frame = ttk.LabelFrame(self.frame, text="Element Properties")
        properties_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview for properties
        columns = ("Property", "Value")
        self.properties_tree = ttk.Treeview(properties_frame, columns=columns, show="headings")
        
        # Configure columns
        self.properties_tree.heading("Property", text="Property")
        self.properties_tree.heading("Value", text="Value")
        
        self.properties_tree.column("Property", width=150)
        self.properties_tree.column("Value", width=650)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(properties_frame, orient=tk.VERTICAL, command=self.properties_tree.yview)
        self.properties_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.properties_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create buttons frame
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add buttons
        add_to_workflow_btn = ttk.Button(
            buttons_frame,
            text="Add to Workflow",
            command=self._add_to_workflow
        )
        add_to_workflow_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            buttons_frame,
            text="Clear",
            command=self.presenter.clear_selected_element
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def display_element_properties(self, properties: Dict[str, Any]) -> None:
        """
        Display element properties
        
        Args:
            properties: Element properties to display
        """
        # Clear existing items
        for item in self.properties_tree.get_children():
            self.properties_tree.delete(item)
        
        # Add properties to treeview
        for key, value in properties.items():
            self.properties_tree.insert(
                "",
                tk.END,
                values=(key, str(value))
            )
    
    def get_url(self) -> str:
        """
        Get the URL entered by the user
        
        Returns:
            The URL
        """
        return self.url_var.get()
    
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
    
    def _add_to_workflow(self) -> None:
        """Add selected element to the workflow"""
        # This would be handled by an event or callback in a real implementation
        # For now, just show a message
        self.show_message("Add to workflow functionality not implemented yet")
