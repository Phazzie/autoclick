"""
Condition Management View for displaying and editing conditions.
SOLID: Single responsibility - UI for condition management.
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
    from ..presenters.condition_presenter import ConditionPresenter

class ConditionView(BaseView):
    """View for managing conditions."""
    
    # Type hint for the presenter
    presenter: 'ConditionPresenter'
    
    def __init__(self, master, **kwargs):
        """Initialize the condition view."""
        super().__init__(master, **kwargs)
        self.current_category = "All"  # Default category filter
        self.selected_condition = None  # Currently selected condition
        self.selected_condition_type = None  # Currently selected condition type
        self.parameter_editors = {}  # Dictionary of parameter editors
    
    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into left (list) and right (editor) panels
        self.grid_columnconfigure(0, weight=3)  # List panel
        self.grid_columnconfigure(1, weight=2)  # Editor panel
        self.grid_rowconfigure(0, weight=1)
        
        # === Left Panel (Condition List) ===
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(1, weight=1)
        
        # Header with filter controls
        self.header_frame = ctk.CTkFrame(self.list_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, PAD_Y_INNER))
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, text="Conditions", font=get_header_font()
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Category filter
        self.category_frame = ctk.CTkFrame(self.header_frame)
        self.category_frame.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.category_label = ctk.CTkLabel(self.category_frame, text="Category:", font=get_default_font())
        self.category_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.category_var = tk.StringVar(value="All")
        self.category_dropdown = ctk.CTkOptionMenu(
            self.category_frame,
            values=["All", "Basic", "Web", "Composite", "Other"],
            variable=self.category_var,
            command=self._on_category_changed
        )
        self.category_dropdown.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Condition treeview
        self.condition_tree = StyledTreeview(
            self.list_frame,
            columns=(COL_ID_NAME, COL_ID_TYPE, COL_ID_DESCRIPTION),
            column_config={
                COL_ID_NAME: {"heading": "Name", "width": 150, "stretch": True},
                COL_ID_TYPE: {"heading": "Type", "width": 100, "stretch": False},
                COL_ID_DESCRIPTION: {"heading": "Description", "width": 200, "stretch": True}
            },
            show="headings"
        )
        self.condition_tree.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.condition_tree.bind("<<TreeviewSelect>>", self._on_condition_selected)
        
        # === Right Panel (Condition Editor) ===
        self.editor_frame = ctk.CTkFrame(self)
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(1, weight=1)
        
        # Editor header
        self.editor_header = ctk.CTkLabel(
            self.editor_frame, text="Condition Editor", font=get_header_font()
        )
        self.editor_header.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Editor form
        self.form_frame = ctk.CTkFrame(self.editor_frame)
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.form_frame.grid_columnconfigure(1, weight=1)
        
        # Condition type selector
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
        self.parameters_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=0, pady=PAD_Y_INNER)
        self.parameters_frame.grid_columnconfigure(1, weight=1)
        
        # Validation message
        self.validation_label = ctk.CTkLabel(
            self.form_frame, text="", font=get_small_font(), text_color="red"
        )
        self.validation_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Test section
        self.test_frame = ctk.CTkFrame(self.form_frame)
        self.test_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=0, pady=PAD_Y_INNER)
        self.test_frame.grid_columnconfigure(1, weight=1)
        
        self.test_label = ctk.CTkLabel(self.test_frame, text="Test Context:", font=get_default_font())
        self.test_label.grid(row=0, column=0, **GRID_ARGS_LABEL)
        
        self.test_context_text = ctk.CTkTextbox(self.test_frame, height=80)
        self.test_context_text.grid(row=0, column=1, **GRID_ARGS_WIDGET)
        self.test_context_text.insert("1.0", "{\n  \"variable1\": \"value1\"\n}")
        
        self.test_button = ctk.CTkButton(
            self.test_frame, text="Test Condition", command=self._on_test_clicked
        )
        self.test_button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.test_result_label = ctk.CTkLabel(
            self.test_frame, text="", font=get_default_font()
        )
        self.test_result_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
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
    
    def _on_category_changed(self, category: str):
        """Handle category filter change."""
        self.current_category = category
        self._filter_condition_list()
    
    def _on_condition_selected(self, event):
        """Handle condition selection in the tree."""
        selection = self.condition_tree.selection()
        if not selection:
            self.selected_condition = None
            self.set_editor_state(False)
            return
        
        item_id = selection[0]
        if self.presenter:
            self.presenter.select_condition(item_id)
    
    def _on_type_changed(self, condition_type: str):
        """Handle condition type selection."""
        if self.presenter:
            self.presenter.select_condition_type(condition_type)
    
    def _on_new_clicked(self):
        """Handle new condition button click."""
        self.clear_editor("Create a new condition")
        self.set_editor_state(True)
        self.selected_condition = None
        self.type_dropdown.focus_set()
    
    def _on_save_clicked(self):
        """Handle save button click."""
        if self.presenter:
            self.presenter.save_condition_from_editor()
    
    def _on_delete_clicked(self):
        """Handle delete button click."""
        if self.selected_condition and self.presenter:
            self.presenter.delete_condition(self.selected_condition)
    
    def _on_clear_clicked(self):
        """Handle clear button click."""
        self.clear_editor()
        self.set_editor_state(False)
        self.selected_condition = None
    
    def _on_test_clicked(self):
        """Handle test button click."""
        if not self.selected_condition:
            self.display_test_result(False, "No condition selected")
            return
        
        try:
            # Parse the test context
            context_text = self.test_context_text.get("1.0", "end").strip()
            if not context_text:
                context = {}
            else:
                context = json.loads(context_text)
            
            # Test the condition
            if self.presenter:
                self.presenter.test_condition(self.selected_condition, context)
        except json.JSONDecodeError:
            self.display_test_result(False, "Invalid JSON in test context")
        except Exception as e:
            self.display_test_result(False, f"Error: {str(e)}")
    
    # === Public Methods ===
    
    def update_condition_types(self, condition_types: List[Dict[str, Any]]):
        """
        Update the condition type dropdown with available types.
        
        Args:
            condition_types: List of condition types with metadata
        """
        # Group condition types by category
        categories = {}
        for ctype in condition_types:
            category = ctype.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append(ctype)
        
        # Create dropdown values with category headers
        dropdown_values = []
        for category in ["Basic", "Web", "Composite", "Other"]:
            if category in categories:
                for ctype in categories[category]:
                    dropdown_values.append(ctype["type"])
        
        # Update the dropdown
        self.type_dropdown.configure(values=dropdown_values)
        
        # Store the condition types for later use
        self.condition_types = condition_types
    
    def update_parameter_editors(self, condition_type: Dict[str, Any]):
        """
        Update the parameter editors for the selected condition type.
        
        Args:
            condition_type: Dictionary containing condition type metadata
        """
        # Clear existing parameter editors
        for widget in self.parameters_frame.winfo_children():
            widget.destroy()
        
        self.parameter_editors = {}
        
        # Create parameter editors
        parameters = condition_type.get("parameters", [])
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
            label.grid(row=i, column=0, **GRID_ARGS_LABEL)
            
            # Create editor based on parameter type
            if param_type == "string":
                editor = ctk.CTkEntry(self.parameters_frame)
                editor.grid(row=i, column=1, **GRID_ARGS_WIDGET)
                
                # Add tooltip
                tooltip = ctk.CTkLabel(
                    self.parameters_frame,
                    text=param_description,
                    font=get_small_font(),
                    text_color="gray"
                )
                tooltip.grid(row=i+1, column=1, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))
                
            elif param_type == "enum":
                options = param.get("options", [])
                var = tk.StringVar(value=options[0] if options else "")
                editor = ctk.CTkOptionMenu(
                    self.parameters_frame,
                    values=options,
                    variable=var
                )
                editor.grid(row=i, column=1, **GRID_ARGS_WIDGET)
                
                # Store the variable for later access
                self.parameter_editors[param_name + "_var"] = var
                
                # Add tooltip
                tooltip = ctk.CTkLabel(
                    self.parameters_frame,
                    text=param_description,
                    font=get_small_font(),
                    text_color="gray"
                )
                tooltip.grid(row=i+1, column=1, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))
                
            elif param_type == "boolean":
                var = tk.StringVar(value="False")
                editor = ctk.CTkOptionMenu(
                    self.parameters_frame,
                    values=["True", "False"],
                    variable=var
                )
                editor.grid(row=i, column=1, **GRID_ARGS_WIDGET)
                
                # Store the variable for later access
                self.parameter_editors[param_name + "_var"] = var
                
                # Add tooltip
                tooltip = ctk.CTkLabel(
                    self.parameters_frame,
                    text=param_description,
                    font=get_small_font(),
                    text_color="gray"
                )
                tooltip.grid(row=i+1, column=1, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))
                
            elif param_type == "array" or param_type == "object":
                editor = ctk.CTkTextbox(self.parameters_frame, height=100)
                editor.grid(row=i, column=1, **GRID_ARGS_WIDGET)
                editor.insert("1.0", "[]" if param_type == "array" else "{}")
                
                # Add tooltip
                tooltip = ctk.CTkLabel(
                    self.parameters_frame,
                    text=param_description + " (JSON format)",
                    font=get_small_font(),
                    text_color="gray"
                )
                tooltip.grid(row=i+1, column=1, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))
            
            # Store the editor for later access
            self.parameter_editors[param_name] = editor
        
        # Store the selected condition type
        self.selected_condition_type = condition_type
    
    def add_condition_to_list(self, condition: Dict[str, Any]):
        """
        Add a condition to the list.
        
        Args:
            condition: Dictionary containing condition data
        """
        # Insert the condition into the tree
        self.condition_tree.insert(
            "", "end", iid=condition["id"],
            values=(
                condition.get("description", ""),
                condition["type"],
                self._get_condition_description(condition)
            )
        )
        
        # Apply category filter
        self._filter_condition_list()
    
    def update_condition_in_list(self, condition: Dict[str, Any]):
        """
        Update a condition in the list.
        
        Args:
            condition: Dictionary containing updated condition data
        """
        # Update the condition in the tree
        self.condition_tree.item(
            condition["id"],
            values=(
                condition.get("description", ""),
                condition["type"],
                self._get_condition_description(condition)
            )
        )
        
        # Apply category filter
        self._filter_condition_list()
    
    def remove_condition_from_list(self, condition_id: str):
        """
        Remove a condition from the list.
        
        Args:
            condition_id: ID of the condition to remove
        """
        # Remove the condition from the tree
        self.condition_tree.delete(condition_id)
    
    def populate_editor(self, condition: Dict[str, Any]):
        """
        Populate the editor with condition data.
        
        Args:
            condition: Dictionary containing condition data
        """
        # Set the condition type
        condition_type = condition["type"]
        self.type_var.set(condition_type)
        
        # Find the condition type metadata
        selected_type = None
        for ctype in self.condition_types:
            if ctype["type"] == condition_type:
                selected_type = ctype
                break
        
        if selected_type:
            # Update parameter editors
            self.update_parameter_editors(selected_type)
            
            # Set description
            self.description_entry.delete(0, "end")
            self.description_entry.insert(0, condition.get("description", ""))
            
            # Set parameter values
            for param in selected_type.get("parameters", []):
                param_name = param["name"]
                param_type = param["type"]
                
                if param_name in self.parameter_editors:
                    editor = self.parameter_editors[param_name]
                    
                    if param_type == "string":
                        editor.delete(0, "end")
                        editor.insert(0, str(condition.get(param_name, "")))
                    elif param_type == "enum":
                        var = self.parameter_editors.get(param_name + "_var")
                        if var:
                            var.set(str(condition.get(param_name, "")))
                    elif param_type == "boolean":
                        var = self.parameter_editors.get(param_name + "_var")
                        if var:
                            var.set(str(condition.get(param_name, False)))
                    elif param_type == "array" or param_type == "object":
                        editor.delete("1.0", "end")
                        value = condition.get(param_name, [] if param_type == "array" else {})
                        editor.insert("1.0", json.dumps(value, indent=2))
        
        self.selected_condition = condition["id"]
        self.set_editor_state(True)
        self.validation_label.configure(text="")
        self.editor_header.configure(text=f"Edit Condition: {condition.get('description', condition['id'])}")
    
    def clear_editor(self, message: Optional[str] = None):
        """
        Clear the editor form.
        
        Args:
            message: Optional message to display in the editor header
        """
        # Clear condition type
        self.type_var.set("")
        
        # Clear description
        self.description_entry.delete(0, "end")
        
        # Clear parameter editors
        for widget in self.parameters_frame.winfo_children():
            widget.destroy()
        
        self.parameter_editors = {}
        self.selected_condition_type = None
        
        # Clear validation message
        self.validation_label.configure(text="")
        
        # Clear test result
        self.test_result_label.configure(text="")
        
        if message:
            self.editor_header.configure(text=message)
        else:
            self.editor_header.configure(text="Condition Editor")
    
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
            if not param_name.endswith("_var"):  # Skip variables
                if hasattr(editor, "configure"):
                    editor.configure(state=state)
        
        self.test_context_text.configure(state=state)
        self.test_button.configure(state=state)
        self.save_button.configure(state=state)
        self.delete_button.configure(state=state)
    
    def set_filter_category(self, category: str):
        """
        Set the category filter.
        
        Args:
            category: Category to filter by
        """
        self.category_var.set(category)
        self.current_category = category
        self._filter_condition_list()
    
    def get_editor_data(self) -> Dict[str, Any]:
        """
        Get the data from the editor form.
        
        Returns:
            Dictionary containing the condition data
        """
        if not self.selected_condition_type:
            return {}
        
        # Get basic data
        data = {
            "id": self.selected_condition or "",
            "type": self.type_var.get(),
            "description": self.description_entry.get()
        }
        
        # Get parameter values
        for param in self.selected_condition_type.get("parameters", []):
            param_name = param["name"]
            param_type = param["type"]
            
            if param_name in self.parameter_editors:
                editor = self.parameter_editors[param_name]
                
                if param_type == "string":
                    data[param_name] = editor.get()
                elif param_type == "enum":
                    var = self.parameter_editors.get(param_name + "_var")
                    if var:
                        data[param_name] = var.get()
                elif param_type == "boolean":
                    var = self.parameter_editors.get(param_name + "_var")
                    if var:
                        data[param_name] = var.get() == "True"
                elif param_type == "array" or param_type == "object":
                    try:
                        text = editor.get("1.0", "end").strip()
                        if text:
                            data[param_name] = json.loads(text)
                        else:
                            data[param_name] = [] if param_type == "array" else {}
                    except json.JSONDecodeError:
                        # Invalid JSON, use default value
                        data[param_name] = [] if param_type == "array" else {}
        
        return data
    
    def show_validation_error(self, message: str):
        """
        Show a validation error message.
        
        Args:
            message: Error message to display
        """
        self.validation_label.configure(text=message)
    
    def display_test_result(self, success: bool, message: str):
        """
        Display the result of testing a condition.
        
        Args:
            success: Whether the condition evaluated to true
            message: Message to display
        """
        if success:
            self.test_result_label.configure(
                text=f"Result: True - {message}",
                text_color="green"
            )
        else:
            self.test_result_label.configure(
                text=f"Result: False - {message}",
                text_color="red"
            )
    
    # === Helper Methods ===
    
    def _filter_condition_list(self):
        """Filter the condition list by category."""
        if self.current_category == "All":
            # Show all conditions
            for item in self.condition_tree.get_children():
                self.condition_tree.item(item, tags=())
        else:
            # Show only conditions in the selected category
            for item in self.condition_tree.get_children():
                condition_type = self.condition_tree.item(item, "values")[1]
                
                # Find the category for this condition type
                category = "Other"
                for ctype in self.condition_types:
                    if ctype["type"] == condition_type:
                        category = ctype.get("category", "Other")
                        break
                
                if category == self.current_category:
                    self.condition_tree.item(item, tags=())
                else:
                    self.condition_tree.item(item, tags=("hidden",))
    
    def _get_condition_description(self, condition: Dict[str, Any]) -> str:
        """
        Get a human-readable description of a condition.
        
        Args:
            condition: Dictionary containing condition data
            
        Returns:
            Human-readable description
        """
        condition_type = condition["type"]
        
        if condition_type == "comparison":
            return f"{condition.get('left_value', '')} {condition.get('operator', '')} {condition.get('right_value', '')}"
        elif condition_type == "element_exists":
            return f"Element exists: {condition.get('selector', '')}"
        elif condition_type == "text_contains":
            return f"Text contains: {condition.get('text', '')}"
        elif condition_type == "and":
            return f"AND ({len(condition.get('conditions', []))} conditions)"
        elif condition_type == "or":
            return f"OR ({len(condition.get('conditions', []))} conditions)"
        elif condition_type == "not":
            return f"NOT ({condition.get('condition', {}).get('type', '')})"
        else:
            return condition_type
