"""Record tab component"""
import logging
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Optional

from src.ui.components.base_component import BaseComponent
from src.ui.interfaces.view_interface import RecordViewInterface
from src.ui.presenters.record_presenter import RecordPresenter


class RecordTab(BaseComponent, RecordViewInterface):
    """Record tab component"""
    
    def __init__(self, parent: Any, presenter: RecordPresenter) -> None:
        """
        Initialize the record tab
        
        Args:
            parent: Parent widget
            presenter: Record presenter
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
        title_label = ttk.Label(header_frame, text="Record Browser Actions", font=("Arial", 14, "bold"))
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Create control frame
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add browser selection
        browser_frame = ttk.LabelFrame(control_frame, text="Browser")
        browser_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
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
        headless_frame = ttk.Frame(control_frame)
        headless_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.headless_var = tk.BooleanVar(value=False)
        headless_check = ttk.Checkbutton(
            headless_frame,
            text="Headless Mode",
            variable=self.headless_var,
            command=lambda: self.presenter.set_headless(self.headless_var.get())
        )
        headless_check.pack(side=tk.LEFT, padx=5)
        
        # Add record buttons
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.start_button = ttk.Button(
            buttons_frame,
            text="Start Recording",
            command=self._start_recording
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            buttons_frame,
            text="Stop Recording",
            command=self._stop_recording,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Create actions frame
        actions_frame = ttk.LabelFrame(self.frame, text="Recorded Actions")
        actions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview for actions
        columns = ("Type", "Selector", "Value", "Description")
        self.actions_tree = ttk.Treeview(actions_frame, columns=columns, show="headings")
        
        # Configure columns
        self.actions_tree.heading("Type", text="Type")
        self.actions_tree.heading("Selector", text="Selector")
        self.actions_tree.heading("Value", text="Value")
        self.actions_tree.heading("Description", text="Description")
        
        self.actions_tree.column("Type", width=100)
        self.actions_tree.column("Selector", width=200)
        self.actions_tree.column("Value", width=200)
        self.actions_tree.column("Description", width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(actions_frame, orient=tk.VERTICAL, command=self.actions_tree.yview)
        self.actions_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.actions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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
            command=self.presenter.clear_recorded_actions
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def display_recorded_actions(self, actions: List[Dict[str, Any]]) -> None:
        """
        Display recorded actions
        
        Args:
            actions: List of recorded actions to display
        """
        # Clear existing items
        for item in self.actions_tree.get_children():
            self.actions_tree.delete(item)
        
        # Add actions to treeview
        for action in actions:
            self.actions_tree.insert(
                "",
                tk.END,
                values=(
                    action.get("type", ""),
                    action.get("selector", ""),
                    action.get("value", ""),
                    action.get("description", "")
                )
            )
    
    def get_selected_recorded_action_indices(self) -> List[int]:
        """
        Get the indices of selected recorded actions
        
        Returns:
            List of indices of selected recorded actions
        """
        selected_items = self.actions_tree.selection()
        
        if not selected_items:
            return []
        
        # Get the indices of selected items
        indices = []
        for item in selected_items:
            index = self.actions_tree.index(item)
            indices.append(index)
        
        return indices
    
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
    
    def _start_recording(self) -> None:
        """Start recording browser actions"""
        self.presenter.start_recording()
        
        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
    
    def _stop_recording(self) -> None:
        """Stop recording browser actions"""
        self.presenter.stop_recording()
        
        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def _add_to_workflow(self) -> None:
        """Add selected actions to the workflow"""
        # This would be handled by an event or callback in a real implementation
        # For now, just show a message
        self.show_message("Add to workflow functionality not implemented yet")
