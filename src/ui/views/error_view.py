"""
Error Handling View for displaying and editing error configurations.
SOLID: Single responsibility - UI for error handling.
KISS: Simple layout with treeview and editor panel.
"""
import customtkinter as ctk
import tkinter as tk
from typing import Dict, List, Optional, Any, TYPE_CHECKING

from ..views.base_view import BaseView
from ..components.styled_treeview import StyledTreeview
from ..utils.constants import (
    COL_ID_TYPE, COL_ID_SEVERITY, COL_ID_ACTION,
    GRID_ARGS_LABEL, GRID_ARGS_WIDGET, GRID_ARGS_FULL_SPAN_WIDGET,
    PAD_X_OUTER, PAD_Y_OUTER, PAD_X_INNER, PAD_Y_INNER
)
from ..utils.ui_utils import get_header_font, get_default_font, get_small_font

if TYPE_CHECKING:
    from ..presenters.error_presenter import ErrorPresenter

class ErrorView(BaseView):
    """View for managing error configurations."""
    
    # Type hint for the presenter
    presenter: 'ErrorPresenter'
    
    def __init__(self, master, **kwargs):
        """Initialize the error view."""
        super().__init__(master, **kwargs)
        self.selected_error = None  # Currently selected error
    
    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into left (list) and right (editor) panels
        self.grid_columnconfigure(0, weight=3)  # List panel
        self.grid_columnconfigure(1, weight=2)  # Editor panel
        self.grid_rowconfigure(0, weight=1)
        
        # === Left Panel (Error List) ===
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(1, weight=1)
        
        # Header with filter controls
        self.header_frame = ctk.CTkFrame(self.list_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, PAD_Y_INNER))
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, text="Error Configurations", font=get_header_font()
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Severity filter
        self.severity_frame = ctk.CTkFrame(self.header_frame)
        self.severity_frame.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.severity_label = ctk.CTkLabel(self.severity_frame, text="Severity:", font=get_default_font())
        self.severity_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.severity_filter_var = tk.StringVar(value="All")
        self.severity_dropdown = ctk.CTkOptionMenu(
            self.severity_frame,
            values=["All", "Info", "Warning", "Error", "Critical", "Fatal"],
            variable=self.severity_filter_var,
            command=self._on_severity_filter_changed
        )
        self.severity_dropdown.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Error treeview
        self.error_tree = StyledTreeview(
            self.list_frame,
            columns=(COL_ID_TYPE, COL_ID_SEVERITY, COL_ID_ACTION),
            column_config={
                COL_ID_TYPE: {"heading": "Error Type", "width": 200, "stretch": True},
                COL_ID_SEVERITY: {"heading": "Severity", "width": 100, "stretch": False},
                COL_ID_ACTION: {"heading": "Action", "width": 100, "stretch": False}
            },
            show="headings"
        )
        self.error_tree.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.error_tree.bind("<<TreeviewSelect>>", self._on_error_selected)
        
        # === Right Panel (Error Editor) ===
        self.editor_frame = ctk.CTkFrame(self)
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(1, weight=1)
        
        # Editor header
        self.editor_header = ctk.CTkLabel(
            self.editor_frame, text="Error Configuration Editor", font=get_header_font()
        )
        self.editor_header.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Editor form
        self.form_frame = ctk.CTkFrame(self.editor_frame)
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.form_frame.grid_columnconfigure(1, weight=1)
        
        # Error type field
        self.error_type_label = ctk.CTkLabel(self.form_frame, text="Error Type:", font=get_default_font())
        self.error_type_label.grid(row=0, column=0, **GRID_ARGS_LABEL)
        
        self.error_type_entry = ctk.CTkEntry(self.form_frame)
        self.error_type_entry.grid(row=0, column=1, **GRID_ARGS_WIDGET)
        
        # Severity field
        self.severity_label = ctk.CTkLabel(self.form_frame, text="Severity:", font=get_default_font())
        self.severity_label.grid(row=1, column=0, **GRID_ARGS_LABEL)
        
        self.severity_var = tk.StringVar(value="Warning")
        self.severity_dropdown = ctk.CTkOptionMenu(
            self.form_frame,
            values=["Info", "Warning", "Error", "Critical", "Fatal"],
            variable=self.severity_var
        )
        self.severity_dropdown.grid(row=1, column=1, **GRID_ARGS_WIDGET)
        
        # Action field
        self.action_label = ctk.CTkLabel(self.form_frame, text="Action:", font=get_default_font())
        self.action_label.grid(row=2, column=0, **GRID_ARGS_LABEL)
        
        self.action_var = tk.StringVar(value="Ignore")
        self.action_dropdown = ctk.CTkOptionMenu(
            self.form_frame,
            values=["Ignore", "Log", "Retry", "Skip", "Stop", "Custom"],
            variable=self.action_var,
            command=self._on_action_changed
        )
        self.action_dropdown.grid(row=2, column=1, **GRID_ARGS_WIDGET)
        
        # Custom action field
        self.custom_action_label = ctk.CTkLabel(self.form_frame, text="Custom Action:", font=get_default_font())
        self.custom_action_label.grid(row=3, column=0, **GRID_ARGS_LABEL)
        
        self.custom_action_entry = ctk.CTkEntry(self.form_frame)
        self.custom_action_entry.grid(row=3, column=1, **GRID_ARGS_WIDGET)
        self.custom_action_entry.configure(state="disabled")  # Initially disabled
        
        # Description
        self.description_label = ctk.CTkLabel(
            self.form_frame,
            text="Configure how the application should handle different types of errors.",
            font=get_small_font(),
            wraplength=300
        )
        self.description_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Action buttons
        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=0, pady=PAD_Y_INNER)
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.new_button = ctk.CTkButton(
            self.button_frame, text="New", command=self._on_new_clicked
        )
        self.new_button.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.save_button = ctk.CTkButton(
            self.button_frame, text="Save", command=self._on_save_clicked
        )
        self.save_button.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Set initial state
        self.set_editor_state(False)
    
    def _setup_layout(self):
        """Set up the layout grid."""
        # Main layout already set up in _create_widgets
        pass
    
    # === Event Handlers ===
    
    def _on_severity_filter_changed(self, severity: str):
        """Handle severity filter change."""
        if self.presenter:
            self.presenter.filter_errors_by_severity(severity)
    
    def _on_error_selected(self, event):
        """Handle error selection in the tree."""
        selection = self.error_tree.selection()
        if not selection:
            self.selected_error = None
            self.set_editor_state(False)
            return
        
        item_id = selection[0]
        if self.presenter:
            self.presenter.select_error(item_id)
    
    def _on_new_clicked(self):
        """Handle new error button click."""
        self.clear_editor("Create a new error configuration")
        self.set_editor_state(True)
        self.selected_error = None
        self.error_type_entry.focus_set()
    
    def _on_save_clicked(self):
        """Handle save button click."""
        if self.presenter:
            self.presenter.save_error_from_editor()
    
    def _on_action_changed(self, action: str):
        """Handle action selection change."""
        if action == "Custom":
            self.custom_action_entry.configure(state="normal")
        else:
            self.custom_action_entry.configure(state="disabled")
            self.custom_action_entry.delete(0, "end")
    
    # === Public Methods ===
    
    def update_error_list(self, errors: List[Any]):
        """
        Update the error tree with new data.
        
        Args:
            errors: List of error configurations
        """
        # Clear existing items
        for item in self.error_tree.get_children():
            self.error_tree.delete(item)
        
        # Add errors
        for error in errors:
            # Format tags based on severity
            tags = []
            if error.severity == "Error":
                tags.append("error")
            elif error.severity == "Warning":
                tags.append("warning")
            elif error.severity == "Critical" or error.severity == "Fatal":
                tags.append("critical")
            
            # Insert error
            self.error_tree.insert(
                "", "end", iid=error.error_type,
                values=(
                    error.error_type,
                    error.severity,
                    error.action
                ),
                tags=tags
            )
    
    def add_error_to_list(self, error: Any):
        """
        Add an error to the list.
        
        Args:
            error: Error configuration to add
        """
        # Format tags based on severity
        tags = []
        if error.severity == "Error":
            tags.append("error")
        elif error.severity == "Warning":
            tags.append("warning")
        elif error.severity == "Critical" or error.severity == "Fatal":
            tags.append("critical")
        
        # Insert error
        self.error_tree.insert(
            "", "end", iid=error.error_type,
            values=(
                error.error_type,
                error.severity,
                error.action
            ),
            tags=tags
        )
    
    def update_error_in_list(self, error: Any):
        """
        Update an error in the list.
        
        Args:
            error: Updated error configuration
        """
        # Format tags based on severity
        tags = []
        if error.severity == "Error":
            tags.append("error")
        elif error.severity == "Warning":
            tags.append("warning")
        elif error.severity == "Critical" or error.severity == "Fatal":
            tags.append("critical")
        
        # Update error
        self.error_tree.item(
            error.error_type,
            values=(
                error.error_type,
                error.severity,
                error.action
            ),
            tags=tags
        )
    
    def populate_editor(self, error: Any):
        """
        Populate the editor with error data.
        
        Args:
            error: Error configuration to edit
        """
        # Set error type
        self.error_type_entry.delete(0, "end")
        self.error_type_entry.insert(0, error.error_type)
        
        # Set severity
        self.severity_var.set(error.severity)
        
        # Set action
        self.action_var.set(error.action)
        
        # Set custom action if applicable
        self.custom_action_entry.delete(0, "end")
        if error.action == "Custom" and error.custom_action:
            self.custom_action_entry.configure(state="normal")
            self.custom_action_entry.insert(0, error.custom_action)
        else:
            self.custom_action_entry.configure(state="disabled")
        
        self.selected_error = error.error_type
        self.set_editor_state(True)
        self.editor_header.configure(text=f"Edit Error: {error.error_type}")
    
    def clear_editor(self, message: Optional[str] = None):
        """
        Clear the editor form.
        
        Args:
            message: Optional message to display in the editor header
        """
        self.error_type_entry.delete(0, "end")
        self.severity_var.set("Warning")
        self.action_var.set("Ignore")
        self.custom_action_entry.delete(0, "end")
        self.custom_action_entry.configure(state="disabled")
        
        self.selected_error = None
        
        if message:
            self.editor_header.configure(text=message)
        else:
            self.editor_header.configure(text="Error Configuration Editor")
    
    def set_editor_state(self, enabled: bool):
        """
        Enable or disable the editor.
        
        Args:
            enabled: Whether the editor should be enabled
        """
        state = "normal" if enabled else "disabled"
        self.error_type_entry.configure(state=state)
        self.severity_dropdown.configure(state=state)
        self.action_dropdown.configure(state=state)
        
        # Custom action entry is only enabled if action is "Custom"
        if enabled and self.action_var.get() == "Custom":
            self.custom_action_entry.configure(state="normal")
        else:
            self.custom_action_entry.configure(state="disabled")
        
        self.save_button.configure(state=state)
    
    def get_editor_data(self) -> Dict[str, Any]:
        """
        Get the data from the editor form.
        
        Returns:
            Dictionary containing the error configuration data
        """
        action = self.action_var.get()
        custom_action = None
        
        if action == "Custom":
            custom_action = self.custom_action_entry.get()
        
        return {
            "error_type": self.error_type_entry.get(),
            "severity": self.severity_var.get(),
            "action": action,
            "custom_action": custom_action
        }
