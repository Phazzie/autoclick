"""
Data Mapping View for creating and editing data mappings.
SOLID: Single responsibility - UI for data mapping.
KISS: Simple drag-and-drop interface for mapping fields.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING
import uuid

from ..views.base_view import BaseView
from ..components.styled_treeview import StyledTreeview
from ..utils.constants import (
    GRID_ARGS_LABEL, GRID_ARGS_WIDGET, GRID_ARGS_FULL_SPAN_WIDGET,
    PAD_X_OUTER, PAD_Y_OUTER, PAD_X_INNER, PAD_Y_INNER
)
from ..utils.ui_utils import get_header_font, get_default_font, get_small_font

if TYPE_CHECKING:
    from ..presenters.data_mapping_presenter import DataMappingPresenter

class DataMappingView(BaseView):
    """View for creating and editing data mappings."""

    # Type hint for the presenter
    presenter: 'DataMappingPresenter'

    def __init__(self, master, **kwargs):
        """Initialize the data mapping view."""
        super().__init__(master, **kwargs)
        self.source_fields = []  # List of source fields
        self.target_variables = []  # List of target variables
        self.mappings = {}  # Dictionary of field mappings
        self.drag_data = {"item": None, "source": None}  # Data for dragging
        self.selected_mapping_id = None  # Currently selected mapping

    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into source fields, mapping area, and target variables
        self.grid_columnconfigure(0, weight=1)  # Source fields
        self.grid_columnconfigure(1, weight=0)  # Mapping controls
        self.grid_columnconfigure(2, weight=1)  # Target variables
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Main content
        self.grid_rowconfigure(2, weight=0)  # Buttons

        # === Header ===
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.header_label = ctk.CTkLabel(
            self.header_frame, text="Data Mapping", font=get_header_font()
        )
        self.header_label.pack(pady=PAD_Y_INNER)

        # === Source Fields ===
        self.source_frame = ctk.CTkFrame(self)
        self.source_frame.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.source_frame.grid_columnconfigure(0, weight=1)
        self.source_frame.grid_rowconfigure(0, weight=0)
        self.source_frame.grid_rowconfigure(1, weight=1)

        self.source_label = ctk.CTkLabel(
            self.source_frame, text="Source Fields", font=get_default_font()
        )
        self.source_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Source fields treeview
        self.source_tree = StyledTreeview(
            self.source_frame,
            columns=("name", "type"),
            column_config={
                "name": {"width": 150, "heading": "Field Name"},
                "type": {"width": 100, "heading": "Type"}
            }
        )
        self.source_tree.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Make source fields draggable
        self.source_tree.bind("<ButtonPress-1>", self._on_source_press)
        self.source_tree.bind("<B1-Motion>", self._on_source_drag)
        self.source_tree.bind("<ButtonRelease-1>", self._on_source_release)

        # === Mapping Controls ===
        self.mapping_frame = ctk.CTkFrame(self)
        self.mapping_frame.grid(row=1, column=1, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.mapping_label = ctk.CTkLabel(
            self.mapping_frame, text="Mappings", font=get_default_font()
        )
        self.mapping_label.pack(pady=PAD_Y_INNER)

        # Mapping buttons
        self.add_mapping_button = ctk.CTkButton(
            self.mapping_frame, text="Add →", command=self._on_add_mapping
        )
        self.add_mapping_button.pack(pady=PAD_Y_INNER)

        self.remove_mapping_button = ctk.CTkButton(
            self.mapping_frame, text="← Remove", command=self._on_remove_mapping
        )
        self.remove_mapping_button.pack(pady=PAD_Y_INNER)

        self.clear_mappings_button = ctk.CTkButton(
            self.mapping_frame, text="Clear All", command=self._on_clear_mappings
        )
        self.clear_mappings_button.pack(pady=PAD_Y_INNER)

        # === Target Variables ===
        self.target_frame = ctk.CTkFrame(self)
        self.target_frame.grid(row=1, column=2, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.target_frame.grid_columnconfigure(0, weight=1)
        self.target_frame.grid_rowconfigure(0, weight=0)
        self.target_frame.grid_rowconfigure(1, weight=1)

        self.target_label = ctk.CTkLabel(
            self.target_frame, text="Target Variables", font=get_default_font()
        )
        self.target_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Target variables treeview
        self.target_tree = StyledTreeview(
            self.target_frame,
            columns=("name", "type", "mapped"),
            column_config={
                "name": {"width": 150, "heading": "Variable Name"},
                "type": {"width": 100, "heading": "Type"},
                "mapped": {"width": 80, "heading": "Mapped"}
            }
        )
        self.target_tree.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Make target variables droppable
        self.target_tree.bind("<ButtonPress-1>", self._on_target_press)
        self.target_tree.bind("<ButtonRelease-1>", self._on_target_release)

        # === Mapping List ===
        self.mappings_frame = ctk.CTkFrame(self)
        self.mappings_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.mappings_frame.grid_columnconfigure(0, weight=1)
        self.mappings_frame.grid_rowconfigure(0, weight=0)
        self.mappings_frame.grid_rowconfigure(1, weight=1)

        self.mappings_label = ctk.CTkLabel(
            self.mappings_frame, text="Current Mappings", font=get_default_font()
        )
        self.mappings_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Mappings treeview
        self.mappings_tree = StyledTreeview(
            self.mappings_frame,
            columns=("source", "target", "transform"),
            column_config={
                "source": {"width": 150, "heading": "Source Field"},
                "target": {"width": 150, "heading": "Target Variable"},
                "transform": {"width": 150, "heading": "Transform"}
            }
        )
        self.mappings_tree.grid(row=1, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.mappings_tree.bind("<ButtonPress-1>", self._on_mapping_select)

        # === Action Buttons ===
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.save_button = ctk.CTkButton(
            self.buttons_frame, text="Save Mappings", command=self._on_save_mappings
        )
        self.save_button.pack(side="right", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.load_button = ctk.CTkButton(
            self.buttons_frame, text="Load Mappings", command=self._on_load_mappings
        )
        self.load_button.pack(side="right", padx=PAD_X_INNER, pady=PAD_Y_INNER)

    def _setup_layout(self):
        """Set up the layout grid."""
        # Main layout already set up in _create_widgets
        pass

    def update_source_fields(self, fields: List[Dict[str, Any]]):
        """
        Update the source fields list.

        Args:
            fields: List of field dictionaries with name and type
        """
        # Clear existing items
        for item in self.source_tree.get_children():
            self.source_tree.delete(item)

        # Store the fields
        self.source_fields = fields

        # Add fields to the treeview
        for field in fields:
            self.source_tree.insert(
                "", "end", iid=field["name"],
                values=(field["name"], field["type"])
            )

    def update_target_variables(self, variables: List[Dict[str, Any]]):
        """
        Update the target variables list.

        Args:
            variables: List of variable dictionaries with name and type
        """
        # Clear existing items
        for item in self.target_tree.get_children():
            self.target_tree.delete(item)

        # Store the variables
        self.target_variables = variables

        # Add variables to the treeview
        for variable in variables:
            # Check if the variable is mapped
            mapped = "Yes" if any(m["target"] == variable["name"] for m in self.mappings.values()) else "No"

            self.target_tree.insert(
                "", "end", iid=variable["name"],
                values=(variable["name"], variable["type"], mapped)
            )

    def update_mappings(self, mappings: Dict[str, Dict[str, Any]]):
        """
        Update the mappings list.

        Args:
            mappings: Dictionary of mapping dictionaries with source, target, and transform
        """
        # Clear existing items
        for item in self.mappings_tree.get_children():
            self.mappings_tree.delete(item)

        # Store the mappings
        self.mappings = mappings

        # Add mappings to the treeview
        for mapping_id, mapping in mappings.items():
            transform = mapping.get("transform", "None")
            if callable(transform):
                transform = transform.__name__

            self.mappings_tree.insert(
                "", "end", iid=mapping_id,
                values=(mapping["source"], mapping["target"], transform)
            )

        # Update the target variables to show which ones are mapped
        self.update_target_variables(self.target_variables)

    def add_mapping(self, source_field: str, target_variable: str):
        """
        Add a mapping between a source field and a target variable.

        Args:
            source_field: Name of the source field
            target_variable: Name of the target variable
        """
        if not source_field or not target_variable:
            return

        # Check if the source field exists
        if not any(f["name"] == source_field for f in self.source_fields):
            messagebox.showerror("Error", f"Source field '{source_field}' not found")
            return

        # Check if the target variable exists
        if not any(v["name"] == target_variable for v in self.target_variables):
            messagebox.showerror("Error", f"Target variable '{target_variable}' not found")
            return

        # Create a new mapping
        mapping_id = str(uuid.uuid4())
        mapping = {
            "source": source_field,
            "target": target_variable,
            "transform": None
        }

        # Add the mapping
        self.mappings[mapping_id] = mapping

        # Update the mappings list
        self.update_mappings(self.mappings)

        # Notify the presenter
        if self.presenter:
            self.presenter.on_mapping_added(mapping_id, mapping)

    def remove_mapping(self, mapping_id: str):
        """
        Remove a mapping.

        Args:
            mapping_id: ID of the mapping to remove
        """
        if mapping_id not in self.mappings:
            return

        # Remove the mapping
        del self.mappings[mapping_id]

        # Update the mappings list
        self.update_mappings(self.mappings)

        # Notify the presenter
        if self.presenter:
            self.presenter.on_mapping_removed(mapping_id)

    def clear_mappings(self):
        """Clear all mappings."""
        # Clear the mappings
        self.mappings = {}

        # Update the mappings list
        self.update_mappings(self.mappings)

        # Notify the presenter
        if self.presenter:
            self.presenter.on_mappings_cleared()

    # === Event Handlers ===

    def _on_source_press(self, event):
        """Handle source field press for dragging."""
        # Get the item under the cursor
        item = self.source_tree.identify_row(event.y)
        if not item:
            return

        # Store the item being dragged
        self.drag_data["item"] = item
        self.drag_data["source"] = "source"

    def _on_source_drag(self, event):
        """Handle source field drag."""
        # If we're not dragging anything, return
        if not self.drag_data["item"]:
            return

        # Create a drag icon or visual feedback
        pass  # Implement visual feedback for dragging

    def _on_source_release(self, event):
        """Handle source field release."""
        # If we're not dragging anything, return
        if not self.drag_data["item"] or self.drag_data["source"] != "source":
            return

        # Check if we're over the target tree
        target_tree_x = self.target_tree.winfo_rootx()
        target_tree_y = self.target_tree.winfo_rooty()
        target_tree_width = self.target_tree.winfo_width()
        target_tree_height = self.target_tree.winfo_height()

        if (target_tree_x <= event.x_root <= target_tree_x + target_tree_width and
            target_tree_y <= event.y_root <= target_tree_y + target_tree_height):
            # Convert to target tree coordinates
            x = event.x_root - target_tree_x
            y = event.y_root - target_tree_y

            # Get the target item
            target_item = self.target_tree.identify_row(y)
            if target_item:
                # Create a mapping
                self.add_mapping(self.drag_data["item"], target_item)

        # Reset drag data
        self.drag_data["item"] = None
        self.drag_data["source"] = None

    def _on_target_press(self, event):
        """Handle target variable press."""
        # Get the item under the cursor
        item = self.target_tree.identify_row(event.y)
        if not item:
            return

        # Store the selected item
        self.selected_target = item

    def _on_target_release(self, event):
        """Handle target variable release."""
        # Reset selected target
        self.selected_target = None

    def _on_mapping_select(self, event):
        """Handle mapping selection."""
        # Get the item under the cursor
        item = self.mappings_tree.identify_row(event.y)
        if not item:
            return

        # Store the selected mapping
        self.selected_mapping_id = item

    def _on_add_mapping(self):
        """Handle add mapping button click."""
        # Get the selected source field
        selected_source = self.source_tree.selection()
        if not selected_source:
            messagebox.showinfo("Info", "Please select a source field")
            return

        # Get the selected target variable
        selected_target = self.target_tree.selection()
        if not selected_target:
            messagebox.showinfo("Info", "Please select a target variable")
            return

        # Add the mapping
        self.add_mapping(selected_source[0], selected_target[0])

    def _on_remove_mapping(self):
        """Handle remove mapping button click."""
        # Get the selected mapping
        if not self.selected_mapping_id:
            messagebox.showinfo("Info", "Please select a mapping to remove")
            return

        # Remove the mapping
        self.remove_mapping(self.selected_mapping_id)
        self.selected_mapping_id = None

    def _on_clear_mappings(self):
        """Handle clear mappings button click."""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all mappings?"):
            self.clear_mappings()

    def _on_save_mappings(self):
        """Handle save mappings button click."""
        if self.presenter:
            self.presenter.save_mappings()

    def _on_load_mappings(self):
        """Handle load mappings button click."""
        if self.presenter:
            self.presenter.load_mappings()
