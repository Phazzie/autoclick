"""Execution tab component"""
import logging
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Optional

from src.ui.components.base_component import BaseComponent
from src.ui.components.common import BrowserSelector
from src.ui.interfaces.view_interface import ExecutionViewInterface
from src.ui.presenters.execution_presenter import ExecutionPresenter


class ExecutionTab(BaseComponent, ExecutionViewInterface):
    """Execution tab component"""
    
    def __init__(self, parent: Any, presenter: ExecutionPresenter) -> None:
        """
        Initialize the execution tab
        
        Args:
            parent: Parent widget
            presenter: Execution presenter
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
        title_label = ttk.Label(
            header_frame,
            text="Workflow Execution",
            font=("Arial", 14, "bold")
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Create options frame
        options_frame = ttk.LabelFrame(self.frame, text="Execution Options")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add browser selector
        self.browser_selector = BrowserSelector(
            options_frame,
            on_browser_change=self.presenter.set_browser_type,
            on_headless_change=self.presenter.set_headless
        )
        self.browser_selector.pack(fill=tk.X, padx=5, pady=5)
        
        # Add timeout option
        timeout_frame = ttk.Frame(options_frame)
        timeout_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(timeout_frame, text="Timeout (seconds):").pack(side=tk.LEFT, padx=5)
        
        self.timeout_var = tk.IntVar(value=30)
        timeout_spinbox = ttk.Spinbox(
            timeout_frame,
            from_=1,
            to=300,
            textvariable=self.timeout_var,
            width=5
        )
        timeout_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Create control frame
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add run/stop buttons
        self.run_button = ttk.Button(
            control_frame,
            text="Run Workflow",
            command=self._run_workflow
        )
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            control_frame,
            text="Stop Execution",
            command=self.presenter.stop_execution,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Create log frame
        log_frame = ttk.LabelFrame(self.frame, text="Execution Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add log text widget
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, state=tk.DISABLED)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            log_frame,
            orient=tk.VERTICAL,
            command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Pack log text and scrollbar
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure tags
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("info", foreground="black")
    
    def display_execution_log(self, log_entries: List[Dict[str, Any]]) -> None:
        """
        Display execution log
        
        Args:
            log_entries: List of log entries to display
        """
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        
        for entry in log_entries:
            timestamp = entry.get("timestamp", "")
            level = entry.get("level", "info")
            message = entry.get("message", "")
            
            # Format based on level
            if level == "error":
                tag = "error"
                prefix = "ERROR: "
            elif level == "warning":
                tag = "warning"
                prefix = "WARNING: "
            else:
                tag = "info"
                prefix = ""
            
            # Add the log entry
            self.log_text.insert(tk.END, f"{timestamp} - {prefix}{message}\n", tag)
        
        # Scroll to the end
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def update_execution_status(self, is_running: bool) -> None:
        """
        Update execution status
        
        Args:
            is_running: Whether execution is running
        """
        if is_running:
            self.run_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.run_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def get_execution_options(self) -> Dict[str, Any]:
        """
        Get execution options
        
        Returns:
            Dictionary of execution options
        """
        return {
            "browser_type": self.browser_selector.get_browser(),
            "headless": self.browser_selector.get_headless(),
            "timeout": self.timeout_var.get()
        }
    
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
    
    def _run_workflow(self) -> None:
        """Run the current workflow"""
        # In a real implementation, this would get the workflow from the workflow builder
        # For now, we'll just create a simple workflow
        workflow = {
            "name": "Test Workflow",
            "actions": [
                {
                    "type": "click",
                    "selector": "#submit-button",
                    "description": "Click submit button"
                },
                {
                    "type": "input",
                    "selector": "#email-input",
                    "value": "test@example.com",
                    "description": "Enter email"
                }
            ]
        }
        
        self.presenter.run_workflow(workflow)
