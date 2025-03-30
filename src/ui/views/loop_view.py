"""
Loop Configuration View for displaying and editing loops.
SOLID: Single responsibility - UI for loop configuration.
KISS: Simple layout with treeview and editor panel.
"""
import customtkinter as ctk
import tkinter as tk
from typing import Dict, List, Optional, Any, TYPE_CHECKING
import json

from ..views.base_view import BaseView
from ..components.styled_treeview import StyledTreeview
from ..utils.constants import (
    COL_ID_NAME, COL_ID_TYPE, COL_ID_DESCRIPTION,
    GRID_ARGS_LABEL, GRID_ARGS_WIDGET, GRID_ARGS_FULL_SPAN_WIDGET,
    PAD_X_OUTER, PAD_Y_OUTER, PAD_X_INNER, PAD_Y_INNER
)
from ..utils.ui_utils import get_header_font, get_default_font, get_small_font

if TYPE_CHECKING:
    from ..presenters.loop_presenter import LoopPresenter

class LoopView(BaseView):
    """View for configuring loops."""
    
    # Type hint for the presenter
    presenter: 'LoopPresenter'
    
    def __init__(self, master, **kwargs):
        """Initialize the loop view."""
        super().__init__(master, **kwargs)
        self.selected_loop = None  # Currently selected loop
        self.selected_loop_type = None  # Currently selected loop type
        self.parameter_editors = {}  # Dictionary of parameter editors
        self.loop_types = []  # Available loop types
    
    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into left (list) and right (editor) panels
        self.grid_columnconfigure(0, weight=3)  # List panel
        self.grid_columnconfigure(1, weight=2)  # Editor panel
        self.grid_rowconfigure(0, weight=1)
        
        # === Left Panel (Loop List) ===
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self.list_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, PAD_Y_INNER))
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, text="Loops", font=get_header_font()
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Loop treeview
        self.loop_tree = StyledTreeview(
            self.list_frame,
            columns=(COL_ID_NAME, COL_ID_TYPE, COL_ID_DESCRIPTION),
            column_config={
                COL_ID_NAME: {"heading": "Name", "width": 150, "stretch": True},
                COL_ID_TYPE: {"heading": "Type", "width": 100, "stretch": False},
                COL_ID_DESCRIPTION: {"heading": "Description", "width": 200, "stretch": True}
            },
            show="headings"
        )
        self.loop_tree.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.loop_tree.bind("<<TreeviewSelect>>", self._on_loop_selected)
        
        # === Right Panel (Loop Editor) ===
        self.editor_frame = ctk.CTkFrame(self)
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(2, weight=1)
        
        # Editor header
        self.editor_header = ctk.CTkLabel(
            self.editor_frame, text="Loop Editor", font=get_header_font()
        )
        self.editor_header.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Editor form
        self.form_frame = ctk.CTkFrame(self.editor_frame)
        self.form_frame.grid(row=1, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.form_frame.grid_columnconfigure(1, weight=1)
        
        # Loop type selector
        self.type_label = ctk.CTkLabel(self.form_frame, text="Type:", font=get_default_font())
        self.type_label.grid(row=0, column=0, **GRID_ARGS_LABEL)
        
        self.type_var = tk.StringVar(value="")
        self.type_dropdown = ctk.CTkOptionMenu(
            self.form_frame,
            values=[],
            variable=self.type_var,
            command=self._on_type_changed
        )
        self.type_dropdown.grid(row=0, column=1, **GRID_ARGS_WIDGET)
        
        # Description field
        self.description_label = ctk.CTkLabel(self.form_frame, text="Description:", font=get_default_font())
        self.description_label.grid(row=1, column=0, **GRID_ARGS_LABEL)
        
        self.description_entry = ctk.CTkEntry(self.form_frame)
        self.description_entry.grid(row=1, column=1, **GRID_ARGS_WIDGET)
        
        # Parameter editors container
        self.parameters_frame = ctk.CTkFrame(self.form_frame)
        self.parameters_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=PAD_Y_INNER)
        self.parameters_frame.grid_columnconfigure(1, weight=1)
        
        # Validation message
        self.validation_label = ctk.CTkLabel(
            self.form_frame, text="", font=get_small_font(), text_color="red"
        )
        self.validation_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Actions section
        self.actions_label = ctk.CTkLabel(
            self.editor_frame, text="Actions", font=get_default_font()
        )
        self.actions_label.grid(row=2, column=0, sticky="nw", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.actions_frame = ctk.CTkFrame(self.editor_frame)
        self.actions_frame.grid(row=3, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.actions_frame.grid_columnconfigure(0, weight=1)
        
        # Action buttons
        self.button_frame = ctk.CTkFrame(self.editor_frame)
        self.button_frame.grid(row=4, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.new_button = ctk.CTkButton(
            self.button_frame, text="New", command=self._on_new_clicked
        )
        self.new_button.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.save_button = ctk.CTkButton(
            self.button_frame, text="Save", command=self._on_save_clicked
        )
        self.save_button.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.delete_button = ctk.CTkButton(
            self.button_frame, text="Delete", command=self._on_delete_clicked
        )
        self.delete_button.grid(row=0, column=2, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.clear_button = ctk.CTkButton(
            self.button_frame, text="Clear", command=self._on_clear_clicked
        )
        self.clear_button.grid(row=0, column=3, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Set initial state
        self.set_editor_state(False)
    
    def _setup_layout(self):
        """Set up the layout grid."""
        # Main layout already set up in _create_widgets
        pass
    
    # === Event Handlers ===
    
    def _on_loop_selected(self, event):
        """Handle loop selection in the tree."""
        selection = self.loop_tree.selection()
        if not selection:
            self.selected_loop = None
            self.set_editor_state(False)
            return
        
        item_id = selection[0]
        if self.presenter:
            self.presenter.select_loop(item_id)
    
    def _on_type_changed(self, loop_type: str):
        """Handle loop type selection."""
        if self.presenter:
            self.presenter.select_loop_type(loop_type)
    
    def _on_new_clicked(self):
        """Handle new loop button click."""
        self.clear_editor("Create a new loop")
        self.set_editor_state(True)
        self.selected_loop = None
        self.type_dropdown.focus_set()
    
    def _on_save_clicked(self):
        """Handle save button click."""
        if self.presenter:
            self.presenter.save_loop_from_editor()
    
    def _on_delete_clicked(self):
        """Handle delete button click."""
        if self.selected_loop and self.presenter:
            self.presenter.delete_loop(self.selected_loop)
    
    def _on_clear_clicked(self):
        """Handle clear button click."""
        self.clear_editor()
        self.set_editor_state(False)
        self.selected_loop = None
    
    # === Public Methods ===
    
    def update_loop_types(self, loop_types: List[Dict[str, Any]]):
        """
        Update the loop type dropdown with available types.
        
        Args:
            loop_types: List of loop types with metadata
        """
        # Create dropdown values
        dropdown_values = [ltype["type"] for ltype in loop_types]
        
        # Update the dropdown
        self.type_dropdown.configure(values=dropdown_values)
        
        # Store the loop types for later use
        self.loop_types = loop_types
    
    def update_parameter_editors(self, loop_type: Dict[str, Any]):
        """
        Update the parameter editors for the selected loop type.
        
        Args:
            loop_type: Dictionary containing loop type metadata
        """
        # Clear existing parameter editors
        for widget in self.parameters_frame.winfo_children():
            widget.destroy()
        
        self.parameter_editors = {}
        
        # Create parameter editors
        parameters = loop_type.get("parameters", [])
        for i, param in enumerate(parameters):
            param_name = param["name"]
            param_type = param["type"]
            param_description = param.get("description", "")
            
            # Create label
            label = ctk.CTkLabel(
                self.parameters_frame,
                text=f"{param_name.replace('_', ' ').title()}:",
                font=get_default_font()
            )
            label.grid(row=i*2, column=0, **GRID_ARGS_LABEL)
            
            # Create editor based on parameter type
            if param_type == "string":
                editor = ctk.CTkEntry(self.parameters_frame)
                editor.grid(row=i*2, column=1, **GRID_ARGS_WIDGET)
                
                # Add tooltip
                tooltip = ctk.CTkLabel(
                    self.parameters_frame,
                    text=param_description,
                    font=get_small_font(),
                    text_color="gray"
                )
                tooltip.grid(row=i*2+1, column=1, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))
                
            elif param_type == "integer":
                editor = ctk.CTkEntry(self.parameters_frame)
                editor.grid(row=i*2, column=1, **GRID_ARGS_WIDGET)
                
                # Add tooltip
                tooltip = ctk.CTkLabel(
                    self.parameters_frame,
                    text=param_description,
                    font=get_small_font(),
                    text_color="gray"
                )
                tooltip.grid(row=i*2+1, column=1, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))
                
            elif param_type == "condition":
                # For conditions, we'll use a button to open a condition editor
                editor = ctk.CTkButton(
                    self.parameters_frame,
                    text="Edit Condition",
                    command=lambda: self._open_condition_editor(param_name)
                )
                editor.grid(row=i*2, column=1, **GRID_ARGS_WIDGET)
                
                # Add tooltip
                tooltip = ctk.CTkLabel(
                    self.parameters_frame,
                    text=param_description,
                    font=get_small_font(),
                    text_color="gray"
                )
                tooltip.grid(row=i*2+1, column=1, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))
                
                # Add a hidden field to store the condition data
                condition_data = ctk.CTkTextbox(self.parameters_frame, height=1)
                condition_data.grid_forget()  # Hide the widget
                self.parameter_editors[param_name + "_data"] = condition_data
            
            # Store the editor for later access
            self.parameter_editors[param_name] = editor
        
        # Store the selected loop type
        self.selected_loop_type = loop_type
    
    def add_loop_to_list(self, loop: Dict[str, Any]):
        """
        Add a loop to the list.
        
        Args:
            loop: Dictionary containing loop data
        """
        # Insert the loop into the tree
        self.loop_tree.insert(
            "", "end", iid=loop["id"],
            values=(
                loop.get("description", ""),
                loop["type"],
                self._get_loop_description(loop)
            )
        )
    
    def update_loop_in_list(self, loop: Dict[str, Any]):
        """
        Update a loop in the list.
        
        Args:
            loop: Dictionary containing updated loop data
        """
        # Update the loop in the tree
        self.loop_tree.item(
            loop["id"],
            values=(
                loop.get("description", ""),
                loop["type"],
                self._get_loop_description(loop)
            )
        )
    
    def remove_loop_from_list(self, loop_id: str):
        """
        Remove a loop from the list.
        
        Args:
            loop_id: ID of the loop to remove
        """
        # Remove the loop from the tree
        self.loop_tree.delete(loop_id)
    
    def populate_editor(self, loop: Dict[str, Any]):
        """
        Populate the editor with loop data.
        
        Args:
            loop: Dictionary containing loop data
        """
        # Set the loop type
        loop_type = loop["type"]
        self.type_var.set(loop_type)
        
        # Find the loop type metadata
        selected_type = None
        for ltype in self.loop_types:
            if ltype["type"] == loop_type:
                selected_type = ltype
                break
        
        if selected_type:
            # Update parameter editors
            self.update_parameter_editors(selected_type)
            
            # Set description
            self.description_entry.delete(0, "end")
            self.description_entry.insert(0, loop.get("description", ""))
            
            # Set parameter values
            for param in selected_type.get("parameters", []):
                param_name = param["name"]
                param_type = param["type"]
                
                if param_name in self.parameter_editors:
                    editor = self.parameter_editors[param_name]
                    
                    if param_type == "string":
                        editor.delete(0, "end")
                        editor.insert(0, str(loop.get(param_name, "")))
                    elif param_type == "integer":
                        editor.delete(0, "end")
                        editor.insert(0, str(loop.get(param_name, "")))
                    elif param_type == "condition":
                        # Store the condition data
                        condition_data = self.parameter_editors.get(param_name + "_data")
                        if condition_data:
                            condition_data.delete("1.0", "end")
                            condition_json = json.dumps(loop.get(param_name, {}))
                            condition_data.insert("1.0", condition_json)
        
        self.selected_loop = loop["id"]
        self.set_editor_state(True)
        self.validation_label.configure(text="")
        self.editor_header.configure(text=f"Edit Loop: {loop.get('description', loop['id'])}")
    
    def clear_editor(self, message: Optional[str] = None):
        """
        Clear the editor form.
        
        Args:
            message: Optional message to display in the editor header
        """
        # Clear loop type
        self.type_var.set("")
        
        # Clear description
        self.description_entry.delete(0, "end")
        
        # Clear parameter editors
        for widget in self.parameters_frame.winfo_children():
            widget.destroy()
        
        self.parameter_editors = {}
        self.selected_loop_type = None
        
        # Clear validation message
        self.validation_label.configure(text="")
        
        if message:
            self.editor_header.configure(text=message)
        else:
            self.editor_header.configure(text="Loop Editor")
    
    def set_editor_state(self, enabled: bool):
        """
        Enable or disable the editor.
        
        Args:
            enabled: Whether the editor should be enabled
        """
        state = "normal" if enabled else "disabled"
        self.type_dropdown.configure(state=state)
        self.description_entry.configure(state=state)
        
        # Enable/disable parameter editors
        for param_name, editor in self.parameter_editors.items():
            if not param_name.endswith("_data"):  # Skip hidden data fields
                if hasattr(editor, "configure"):
                    editor.configure(state=state)
        
        self.save_button.configure(state=state)
        self.delete_button.configure(state=state)
    
    def get_editor_data(self) -> Dict[str, Any]:
        """
        Get the data from the editor form.
        
        Returns:
            Dictionary containing the loop data
        """
        if not self.selected_loop_type:
            return {}
        
        # Get basic data
        data = {
            "id": self.selected_loop or "",
            "type": self.type_var.get(),
            "description": self.description_entry.get()
        }
        
        # Get parameter values
        for param in self.selected_loop_type.get("parameters", []):
            param_name = param["name"]
            param_type = param["type"]
            
            if param_name in self.parameter_editors:
                editor = self.parameter_editors[param_name]
                
                if param_type == "string":
                    data[param_name] = editor.get()
                elif param_type == "integer":
                    try:
                        data[param_name] = int(editor.get())
                    except ValueError:
                        data[param_name] = None
                elif param_type == "condition":
                    # Get the condition data
                    condition_data = self.parameter_editors.get(param_name + "_data")
                    if condition_data:
                        try:
                            condition_json = condition_data.get("1.0", "end").strip()
                            if condition_json:
                                data[param_name] = json.loads(condition_json)
                            else:
                                data[param_name] = {}
                        except json.JSONDecodeError:
                            data[param_name] = {}
        
        return data
    
    def show_validation_error(self, message: str):
        """
        Show a validation error message.
        
        Args:
            message: Error message to display
        """
        self.validation_label.configure(text=message)
    
    # === Helper Methods ===
    
    def _get_loop_description(self, loop: Dict[str, Any]) -> str:
        """
        Get a human-readable description of a loop.
        
        Args:
            loop: Dictionary containing loop data
            
        Returns:
            Human-readable description
        """
        loop_type = loop["type"]
        
        if loop_type == "for_each":
            return f"For each {loop.get('item_variable', '')} in {loop.get('collection_variable', '')}"
        elif loop_type == "while_loop":
            return f"While condition is true (max: {loop.get('max_iterations', 'unlimited')})"
        else:
            return loop_type
    
    def _open_condition_editor(self, param_name: str):
        """
        Open a condition editor for the given parameter.
        
        Args:
            param_name: Name of the parameter to edit
        """
        # This would open a dialog to edit the condition
        # For now, we'll just show a message
        self.show_validation_error("Condition editor not implemented yet")
