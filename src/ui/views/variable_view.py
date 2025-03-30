"""
Variable Management View for displaying and editing variables.
SOLID: Single responsibility - UI for variable management.
KISS: Simple layout with treeview and editor panel.
"""
import customtkinter as ctk
import tkinter as tk
from typing import Dict, List, Optional, Any, TYPE_CHECKING

from ..views.base_view import BaseView
from ..components.styled_treeview import StyledTreeview
from ..utils.constants import (
    COL_ID_NAME, COL_ID_TYPE, COL_ID_VALUE, COL_ID_SCOPE,
    GRID_ARGS_LABEL, GRID_ARGS_WIDGET, GRID_ARGS_FULL_SPAN_WIDGET,
    PAD_X_OUTER, PAD_Y_OUTER, PAD_X_INNER, PAD_Y_INNER
)
from ..utils.ui_utils import get_header_font, get_default_font, get_small_font

if TYPE_CHECKING:
    from ..presenters.variable_presenter import VariablePresenter

class VariableView(BaseView):
    """View for managing variables across different scopes."""
    
    # Type hint for the presenter
    presenter: 'VariablePresenter'
    
    def __init__(self, master, **kwargs):
        """Initialize the variable view."""
        super().__init__(master, **kwargs)
        self.current_scope = "All"  # Default scope filter
        self.selected_variable = None  # Currently selected variable
    
    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into left (tree) and right (editor) panels
        self.grid_columnconfigure(0, weight=3)  # Tree panel
        self.grid_columnconfigure(1, weight=2)  # Editor panel
        self.grid_rowconfigure(0, weight=1)
        
        # === Left Panel (Variable Tree) ===
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=0, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(1, weight=1)
        
        # Header with filter controls
        self.header_frame = ctk.CTkFrame(self.tree_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, PAD_Y_INNER))
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, text="Variables", font=get_header_font()
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Scope filter
        self.scope_frame = ctk.CTkFrame(self.header_frame)
        self.scope_frame.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.scope_label = ctk.CTkLabel(self.scope_frame, text="Scope:", font=get_default_font())
        self.scope_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.scope_var = tk.StringVar(value="All")
        self.scope_dropdown = ctk.CTkOptionMenu(
            self.scope_frame,
            values=["All", "Global", "Workflow", "Local"],
            variable=self.scope_var,
            command=self._on_scope_changed
        )
        self.scope_dropdown.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Variable treeview
        self.variable_tree = StyledTreeview(
            self.tree_frame,
            columns=(COL_ID_NAME, COL_ID_TYPE, COL_ID_VALUE),
            column_config={
                COL_ID_SCOPE: {"heading": "Scope", "width": 120, "stretch": False},
                COL_ID_NAME: {"heading": "Name", "width": 150, "stretch": True},
                COL_ID_TYPE: {"heading": "Type", "width": 100, "stretch": False},
                COL_ID_VALUE: {"heading": "Value", "width": 200, "stretch": True}
            },
            show="tree headings"
        )
        self.variable_tree.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.variable_tree.bind("<<TreeviewSelect>>", self._on_variable_selected)
        
        # === Right Panel (Variable Editor) ===
        self.editor_frame = ctk.CTkFrame(self)
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(1, weight=1)
        
        # Editor header
        self.editor_header = ctk.CTkLabel(
            self.editor_frame, text="Variable Editor", font=get_header_font()
        )
        self.editor_header.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Editor form
        self.form_frame = ctk.CTkFrame(self.editor_frame)
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.form_frame.grid_columnconfigure(1, weight=1)
        
        # Name field
        self.name_label = ctk.CTkLabel(self.form_frame, text="Name:", font=get_default_font())
        self.name_label.grid(row=0, column=0, **GRID_ARGS_LABEL)
        
        self.name_entry = ctk.CTkEntry(self.form_frame)
        self.name_entry.grid(row=0, column=1, **GRID_ARGS_WIDGET)
        
        # Type field
        self.type_label = ctk.CTkLabel(self.form_frame, text="Type:", font=get_default_font())
        self.type_label.grid(row=1, column=0, **GRID_ARGS_LABEL)
        
        self.type_var = tk.StringVar(value="String")
        self.type_dropdown = ctk.CTkOptionMenu(
            self.form_frame,
            values=["String", "Integer", "Float", "Boolean", "List", "Dictionary"],
            variable=self.type_var,
            command=self._on_type_changed
        )
        self.type_dropdown.grid(row=1, column=1, **GRID_ARGS_WIDGET)
        
        # Scope field
        self.scope_editor_label = ctk.CTkLabel(self.form_frame, text="Scope:", font=get_default_font())
        self.scope_editor_label.grid(row=2, column=0, **GRID_ARGS_LABEL)
        
        self.scope_editor_var = tk.StringVar(value="Workflow")
        self.scope_editor_dropdown = ctk.CTkOptionMenu(
            self.form_frame,
            values=["Global", "Workflow", "Local"],
            variable=self.scope_editor_var
        )
        self.scope_editor_dropdown.grid(row=2, column=1, **GRID_ARGS_WIDGET)
        
        # Value field
        self.value_label = ctk.CTkLabel(self.form_frame, text="Value:", font=get_default_font())
        self.value_label.grid(row=3, column=0, **GRID_ARGS_LABEL)
        
        # Default to string entry
        self.value_entry = ctk.CTkEntry(self.form_frame)
        self.value_entry.grid(row=3, column=1, **GRID_ARGS_WIDGET)
        
        # Boolean value option (hidden by default)
        self.bool_var = tk.StringVar(value="False")
        self.bool_dropdown = ctk.CTkOptionMenu(
            self.form_frame,
            values=["True", "False"],
            variable=self.bool_var
        )
        
        # Complex value editor (hidden by default)
        self.complex_value_frame = ctk.CTkFrame(self.form_frame)
        self.complex_value_text = ctk.CTkTextbox(self.complex_value_frame, height=100)
        self.complex_value_text.pack(fill="both", expand=True, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Validation message
        self.validation_label = ctk.CTkLabel(
            self.form_frame, text="", font=get_small_font(), text_color="red"
        )
        self.validation_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Action buttons
        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=0, pady=PAD_Y_INNER)
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
    
    def _on_scope_changed(self, scope: str):
        """Handle scope filter change."""
        self.current_scope = scope
        if self.presenter:
            self.presenter.filter_variables(scope)
    
    def _on_variable_selected(self, event):
        """Handle variable selection in the tree."""
        selection = self.variable_tree.selection()
        if not selection:
            self.selected_variable = None
            self.set_editor_state(False)
            return
        
        item_id = selection[0]
        if self.presenter:
            self.presenter.select_variable(item_id)
    
    def _on_type_changed(self, type_name: str):
        """Handle type selection change."""
        self._update_value_editor(type_name)
    
    def _on_new_clicked(self):
        """Handle new variable button click."""
        self.clear_editor("Create a new variable")
        self.set_editor_state(True)
        self.selected_variable = None
        self.name_entry.focus_set()
    
    def _on_save_clicked(self):
        """Handle save button click."""
        if self.presenter:
            self.presenter.save_variable(self.get_editor_data())
    
    def _on_delete_clicked(self):
        """Handle delete button click."""
        if self.selected_variable and self.presenter:
            self.presenter.delete_variable(self.selected_variable)
    
    def _on_clear_clicked(self):
        """Handle clear button click."""
        self.clear_editor()
        self.set_editor_state(False)
        self.selected_variable = None
    
    # === Public Methods ===
    
    def update_variable_list(self, scope_map: Dict[str, List[Dict]]):
        """
        Update the variable tree with new data.
        
        Args:
            scope_map: Dictionary mapping scope names to lists of variables
        """
        # Clear existing items
        for item in self.variable_tree.get_children():
            self.variable_tree.delete(item)
        
        # Add scope nodes
        for scope, variables in scope_map.items():
            # Skip empty scopes if filtering is active
            if not variables and self.current_scope != "All":
                continue
            
            # Create scope node
            scope_node = self.variable_tree.insert(
                "", "end", text=scope, values=("", "", "")
            )
            
            # Add variables under scope node
            for var in variables:
                var_id = f"{scope}:{var['name']}"
                self.variable_tree.insert(
                    scope_node, "end", iid=var_id,
                    text="", 
                    values=(var["name"], var["type"], str(var["value"]))
                )
        
        # Expand all scope nodes
        for item in self.variable_tree.get_children():
            self.variable_tree.item(item, open=True)
    
    def populate_editor(self, variable_data: Dict[str, Any]):
        """
        Populate the editor with variable data.
        
        Args:
            variable_data: Dictionary containing variable data
        """
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, variable_data.get("name", ""))
        
        var_type = variable_data.get("type", "String")
        self.type_var.set(var_type)
        
        scope = variable_data.get("scope", "Workflow")
        self.scope_editor_var.set(scope)
        
        # Update value editor based on type
        self._update_value_editor(var_type)
        
        # Set value based on type
        value = variable_data.get("value", "")
        if var_type == "Boolean":
            self.bool_var.set("True" if value else "False")
        elif var_type in ["List", "Dictionary"]:
            import json
            try:
                formatted_value = json.dumps(value, indent=2)
            except:
                formatted_value = str(value)
            self.complex_value_text.delete("1.0", "end")
            self.complex_value_text.insert("1.0", formatted_value)
        else:
            self.value_entry.delete(0, "end")
            self.value_entry.insert(0, str(value))
        
        self.selected_variable = f"{scope}:{variable_data.get('name', '')}"
        self.set_editor_state(True)
        self.validation_label.configure(text="")
    
    def clear_editor(self, message: Optional[str] = None):
        """
        Clear the editor form.
        
        Args:
            message: Optional message to display in the editor header
        """
        self.name_entry.delete(0, "end")
        self.type_var.set("String")
        self.scope_editor_var.set("Workflow")
        self.value_entry.delete(0, "end")
        self.bool_var.set("False")
        self.complex_value_text.delete("1.0", "end")
        self.validation_label.configure(text="")
        
        if message:
            self.editor_header.configure(text=message)
        else:
            self.editor_header.configure(text="Variable Editor")
        
        self._update_value_editor("String")
    
    def set_editor_state(self, enabled: bool):
        """
        Enable or disable the editor.
        
        Args:
            enabled: Whether the editor should be enabled
        """
        state = "normal" if enabled else "disabled"
        self.name_entry.configure(state=state)
        self.type_dropdown.configure(state=state)
        self.scope_editor_dropdown.configure(state=state)
        self.value_entry.configure(state=state)
        self.bool_dropdown.configure(state=state)
        self.complex_value_text.configure(state=state)
        self.save_button.configure(state=state)
        self.delete_button.configure(state=state)
    
    def set_filter_scope(self, scope: str):
        """
        Set the scope filter.
        
        Args:
            scope: Scope to filter by
        """
        self.scope_var.set(scope)
        self.current_scope = scope
    
    def get_editor_data(self) -> Dict[str, Any]:
        """
        Get the data from the editor form.
        
        Returns:
            Dictionary containing the variable data
        """
        var_type = self.type_var.get()
        
        # Get value based on type
        if var_type == "Boolean":
            value = self.bool_var.get() == "True"
        elif var_type == "Integer":
            try:
                value = int(self.value_entry.get())
            except ValueError:
                value = 0
        elif var_type == "Float":
            try:
                value = float(self.value_entry.get())
            except ValueError:
                value = 0.0
        elif var_type in ["List", "Dictionary"]:
            import json
            try:
                value = json.loads(self.complex_value_text.get("1.0", "end"))
            except json.JSONDecodeError:
                value = [] if var_type == "List" else {}
        else:  # String or other
            value = self.value_entry.get()
        
        return {
            "name": self.name_entry.get(),
            "type": var_type,
            "value": value,
            "scope": self.scope_editor_var.get()
        }
    
    def show_validation_error(self, message: str):
        """
        Show a validation error message.
        
        Args:
            message: Error message to display
        """
        self.validation_label.configure(text=message)
    
    # === Helper Methods ===
    
    def _update_value_editor(self, var_type: str):
        """
        Update the value editor based on the variable type.
        
        Args:
            var_type: Variable type
        """
        # Hide all value editors first
        self.value_entry.grid_forget()
        self.bool_dropdown.grid_forget()
        self.complex_value_frame.grid_forget()
        
        # Show the appropriate editor
        if var_type == "Boolean":
            self.bool_dropdown.grid(row=3, column=1, **GRID_ARGS_WIDGET)
        elif var_type in ["List", "Dictionary"]:
            self.complex_value_frame.grid(row=3, column=1, **GRID_ARGS_WIDGET)
        else:  # String, Integer, Float
            self.value_entry.grid(row=3, column=1, **GRID_ARGS_WIDGET)
