"""
Data Source View for managing data sources.
SOLID: Single responsibility - UI for data source management.
KISS: Simple interface for configuring data sources.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
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
    from ..presenters.data_source_presenter import DataSourcePresenter

class DataSourceView(BaseView):
    """View for managing data sources."""

    # Type hint for the presenter
    presenter: 'DataSourcePresenter'

    def __init__(self, master, **kwargs):
        """Initialize the data source view."""
        super().__init__(master, **kwargs)
        self.selected_source_id = None  # Currently selected data source
        self.config_widgets = {}  # Dictionary of configuration widgets

    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into source list and source details
        self.grid_columnconfigure(0, weight=1)  # Source list
        self.grid_columnconfigure(1, weight=2)  # Source details
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Main content

        # === Header ===
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.header_label = ctk.CTkLabel(
            self.header_frame, text="Data Source Management", font=get_header_font()
        )
        self.header_label.pack(pady=PAD_Y_INNER)

        # === Source List ===
        self.source_list_frame = ctk.CTkFrame(self)
        self.source_list_frame.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.source_list_frame.grid_columnconfigure(0, weight=1)
        self.source_list_frame.grid_rowconfigure(0, weight=0)
        self.source_list_frame.grid_rowconfigure(1, weight=1)
        self.source_list_frame.grid_rowconfigure(2, weight=0)

        self.source_list_label = ctk.CTkLabel(
            self.source_list_frame, text="Data Sources", font=get_default_font()
        )
        self.source_list_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Source list treeview
        self.source_tree = StyledTreeview(
            self.source_list_frame,
            columns=("name", "type"),
            column_config={
                "name": {"width": 150, "heading": "Name"},
                "type": {"width": 100, "heading": "Type"}
            }
        )
        self.source_tree.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.source_tree.bind("<<TreeviewSelect>>", self._on_source_select)

        # Source list buttons
        self.source_buttons_frame = ctk.CTkFrame(self.source_list_frame)
        self.source_buttons_frame.grid(row=2, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.add_button = ctk.CTkButton(
            self.source_buttons_frame, text="Add", command=self._on_add_source
        )
        self.add_button.pack(side="left", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.delete_button = ctk.CTkButton(
            self.source_buttons_frame, text="Delete", command=self._on_delete_source
        )
        self.delete_button.pack(side="left", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # === Source Details ===
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=1, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_rowconfigure(0, weight=0)
        self.details_frame.grid_rowconfigure(1, weight=0)
        self.details_frame.grid_rowconfigure(2, weight=1)
        self.details_frame.grid_rowconfigure(3, weight=0)

        self.details_label = ctk.CTkLabel(
            self.details_frame, text="Data Source Details", font=get_default_font()
        )
        self.details_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Basic details
        self.basic_details_frame = ctk.CTkFrame(self.details_frame)
        self.basic_details_frame.grid(row=1, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.basic_details_frame.grid_columnconfigure(1, weight=1)

        # Name field
        self.name_label = ctk.CTkLabel(
            self.basic_details_frame, text="Name:", font=get_default_font()
        )
        self.name_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.name_var = tk.StringVar()
        self.name_entry = ctk.CTkEntry(
            self.basic_details_frame, textvariable=self.name_var
        )
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Type field
        self.type_label = ctk.CTkLabel(
            self.basic_details_frame, text="Type:", font=get_default_font()
        )
        self.type_label.grid(row=1, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.type_var = tk.StringVar()
        self.type_dropdown = ctk.CTkOptionMenu(
            self.basic_details_frame,
            values=["CSV File", "JSON File", "Database", "API Endpoint"],
            variable=self.type_var,
            command=self._on_type_changed
        )
        self.type_dropdown.grid(row=1, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Configuration frame
        self.config_frame = ctk.CTkScrollableFrame(self.details_frame)
        self.config_frame.grid(row=2, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.config_frame.grid_columnconfigure(1, weight=1)

        # Preview frame
        self.preview_frame = ctk.CTkFrame(self.details_frame)
        self.preview_frame.grid(row=3, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(1, weight=1)

        self.preview_label = ctk.CTkLabel(
            self.preview_frame, text="Data Preview", font=get_default_font()
        )
        self.preview_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.preview_button = ctk.CTkButton(
            self.preview_frame, text="Preview Data", command=self._on_preview_data
        )
        self.preview_button.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.save_button = ctk.CTkButton(
            self.preview_frame, text="Save", command=self._on_save_source
        )
        self.save_button.grid(row=0, column=2, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Preview treeview
        self.preview_tree = StyledTreeview(
            self.preview_frame,
            columns=(),  # Will be set dynamically
            column_config={}  # Will be set dynamically
        )
        self.preview_tree.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Disable details initially
        self._set_details_state(False)

    def _setup_layout(self):
        """Set up the layout grid."""
        # Main layout already set up in _create_widgets
        pass

    def update_source_list(self, sources: List[Dict[str, Any]]):
        """
        Update the source list.

        Args:
            sources: List of data source dictionaries
        """
        # Clear existing items
        for item in self.source_tree.get_children():
            self.source_tree.delete(item)

        # Add sources to the treeview
        for source in sources:
            self.source_tree.insert(
                "", "end", iid=source.id,
                values=(source.name, source.type)
            )

    def display_source_details(self, source: Optional[Dict[str, Any]]):
        """
        Display details for a data source.

        Args:
            source: Data source dictionary, or None to clear
        """
        if not source:
            self._set_details_state(False)
            self.name_var.set("")
            self.type_var.set("")
            self._clear_config_widgets()
            return

        # Enable details
        self._set_details_state(True)

        # Set basic details
        self.name_var.set(source.name)
        self.type_var.set(source.type)

        # Create configuration widgets based on type
        self._create_config_widgets(source.type, source.config_params)

    def display_data_preview(self, headers: List[str], rows: List[Dict[str, Any]]):
        """
        Display a preview of the data.

        Args:
            headers: List of column headers
            rows: List of data rows
        """
        # Clear existing columns
        self.preview_tree.configure(columns=headers)

        # Configure columns
        column_config = {}
        for header in headers:
            column_config[header] = {"width": 100, "heading": header}
        self.preview_tree.configure(column_config=column_config)

        # Clear existing items
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)

        # Add rows to the treeview
        for i, row in enumerate(rows):
            self.preview_tree.insert(
                "", "end", iid=str(i),
                values=row
            )

    def get_source_data(self) -> Dict[str, Any]:
        """
        Get the data from the source details form.

        Returns:
            Dictionary containing the source data
        """
        data = {
            "name": self.name_var.get(),
            "type": self.type_var.get(),
            "config_params": {}
        }

        # Get configuration parameters
        for param_name, widget in self.config_widgets.items():
            if isinstance(widget, ctk.CTkEntry):
                data["config_params"][param_name] = widget.get()
            elif isinstance(widget, ctk.CTkCheckBox):
                data["config_params"][param_name] = bool(widget.get())
            elif isinstance(widget, ctk.CTkOptionMenu):
                data["config_params"][param_name] = widget.get()

        return data

    def _set_details_state(self, enabled: bool):
        """
        Set the state of the details form.

        Args:
            enabled: Whether the form should be enabled
        """
        state = "normal" if enabled else "disabled"
        self.name_entry.configure(state=state)
        self.type_dropdown.configure(state=state)
        self.preview_button.configure(state=state)
        self.save_button.configure(state=state)

    def _clear_config_widgets(self):
        """Clear the configuration widgets."""
        for widget in self.config_frame.winfo_children():
            widget.destroy()
        self.config_widgets = {}

    def _create_config_widgets(self, source_type: str, config_params: Dict[str, Any]):
        """
        Create configuration widgets based on the source type.

        Args:
            source_type: Type of data source
            config_params: Configuration parameters
        """
        # Clear existing widgets
        self._clear_config_widgets()

        # Create widgets based on type
        if source_type == "CSV File":
            self._create_csv_config_widgets(config_params)
        elif source_type == "JSON File":
            self._create_json_config_widgets(config_params)
        elif source_type == "Database":
            self._create_database_config_widgets(config_params)
        elif source_type == "API Endpoint":
            self._create_api_config_widgets(config_params)

    def _create_csv_config_widgets(self, config_params: Dict[str, Any]):
        """
        Create configuration widgets for CSV files.

        Args:
            config_params: Configuration parameters
        """
        # File path
        file_path_label = ctk.CTkLabel(
            self.config_frame, text="File Path:", font=get_default_font()
        )
        file_path_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        file_path_frame = ctk.CTkFrame(self.config_frame)
        file_path_frame.grid(row=0, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        file_path_frame.grid_columnconfigure(0, weight=1)

        file_path_entry = ctk.CTkEntry(file_path_frame)
        file_path_entry.grid(row=0, column=0, sticky="ew", padx=(0, PAD_X_INNER))
        file_path_entry.insert(0, config_params.get("file_path", ""))
        self.config_widgets["file_path"] = file_path_entry

        file_path_button = ctk.CTkButton(
            file_path_frame, text="Browse", width=80, command=self._on_browse_csv
        )
        file_path_button.grid(row=0, column=1, sticky="e")

        # Has header
        has_header_label = ctk.CTkLabel(
            self.config_frame, text="Has Header:", font=get_default_font()
        )
        has_header_label.grid(row=1, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        has_header_var = tk.IntVar(value=int(config_params.get("has_header", True)))
        has_header_checkbox = ctk.CTkCheckBox(
            self.config_frame, text="", variable=has_header_var
        )
        has_header_checkbox.grid(row=1, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.config_widgets["has_header"] = has_header_checkbox

        # Delimiter
        delimiter_label = ctk.CTkLabel(
            self.config_frame, text="Delimiter:", font=get_default_font()
        )
        delimiter_label.grid(row=2, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        delimiter_entry = ctk.CTkEntry(self.config_frame, width=50)
        delimiter_entry.grid(row=2, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        delimiter_entry.insert(0, config_params.get("delimiter", ","))
        self.config_widgets["delimiter"] = delimiter_entry

    def _create_json_config_widgets(self, config_params: Dict[str, Any]):
        """
        Create configuration widgets for JSON files.

        Args:
            config_params: Configuration parameters
        """
        # File path
        file_path_label = ctk.CTkLabel(
            self.config_frame, text="File Path:", font=get_default_font()
        )
        file_path_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        file_path_frame = ctk.CTkFrame(self.config_frame)
        file_path_frame.grid(row=0, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        file_path_frame.grid_columnconfigure(0, weight=1)

        file_path_entry = ctk.CTkEntry(file_path_frame)
        file_path_entry.grid(row=0, column=0, sticky="ew", padx=(0, PAD_X_INNER))
        file_path_entry.insert(0, config_params.get("file_path", ""))
        self.config_widgets["file_path"] = file_path_entry

        file_path_button = ctk.CTkButton(
            file_path_frame, text="Browse", width=80, command=self._on_browse_json
        )
        file_path_button.grid(row=0, column=1, sticky="e")

        # Root element
        root_element_label = ctk.CTkLabel(
            self.config_frame, text="Root Element:", font=get_default_font()
        )
        root_element_label.grid(row=1, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        root_element_entry = ctk.CTkEntry(self.config_frame)
        root_element_entry.grid(row=1, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        root_element_entry.insert(0, config_params.get("root_element", ""))
        self.config_widgets["root_element"] = root_element_entry

    def _create_database_config_widgets(self, config_params: Dict[str, Any]):
        """
        Create configuration widgets for databases.

        Args:
            config_params: Configuration parameters
        """
        # Connection string
        conn_string_label = ctk.CTkLabel(
            self.config_frame, text="Connection String:", font=get_default_font()
        )
        conn_string_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        conn_string_entry = ctk.CTkEntry(self.config_frame)
        conn_string_entry.grid(row=0, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        conn_string_entry.insert(0, config_params.get("connection_string", ""))
        self.config_widgets["connection_string"] = conn_string_entry

        # Query
        query_label = ctk.CTkLabel(
            self.config_frame, text="Query:", font=get_default_font()
        )
        query_label.grid(row=1, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        query_entry = ctk.CTkTextbox(self.config_frame, height=100)
        query_entry.grid(row=1, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        query_entry.insert("1.0", config_params.get("query", ""))
        self.config_widgets["query"] = query_entry

    def _create_api_config_widgets(self, config_params: Dict[str, Any]):
        """
        Create configuration widgets for API endpoints.

        Args:
            config_params: Configuration parameters
        """
        # URL
        url_label = ctk.CTkLabel(
            self.config_frame, text="URL:", font=get_default_font()
        )
        url_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        url_entry = ctk.CTkEntry(self.config_frame)
        url_entry.grid(row=0, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        url_entry.insert(0, config_params.get("url", ""))
        self.config_widgets["url"] = url_entry

        # Method
        method_label = ctk.CTkLabel(
            self.config_frame, text="Method:", font=get_default_font()
        )
        method_label.grid(row=1, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        method_var = tk.StringVar(value=config_params.get("method", "GET"))
        method_dropdown = ctk.CTkOptionMenu(
            self.config_frame,
            values=["GET", "POST", "PUT", "DELETE"],
            variable=method_var
        )
        method_dropdown.grid(row=1, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.config_widgets["method"] = method_dropdown

        # Headers
        headers_label = ctk.CTkLabel(
            self.config_frame, text="Headers:", font=get_default_font()
        )
        headers_label.grid(row=2, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        headers_entry = ctk.CTkTextbox(self.config_frame, height=50)
        headers_entry.grid(row=2, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        headers_entry.insert("1.0", config_params.get("headers", ""))
        self.config_widgets["headers"] = headers_entry

        # Body
        body_label = ctk.CTkLabel(
            self.config_frame, text="Body:", font=get_default_font()
        )
        body_label.grid(row=3, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        body_entry = ctk.CTkTextbox(self.config_frame, height=100)
        body_entry.grid(row=3, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        body_entry.insert("1.0", config_params.get("body", ""))
        self.config_widgets["body"] = body_entry

    # === Event Handlers ===

    def _on_source_select(self, event):
        """Handle source selection."""
        selected_items = self.source_tree.selection()
        if not selected_items:
            self.selected_source_id = None
            self.display_source_details(None)
            return

        self.selected_source_id = selected_items[0]
        if self.presenter:
            self.presenter.select_data_source(self.selected_source_id)

    def _on_add_source(self):
        """Handle add source button click."""
        if self.presenter:
            self.presenter.add_data_source()

    def _on_delete_source(self):
        """Handle delete source button click."""
        if not self.selected_source_id:
            messagebox.showinfo("Info", "Please select a data source to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this data source?"):
            if self.presenter:
                self.presenter.delete_data_source(self.selected_source_id)

    def _on_save_source(self):
        """Handle save source button click."""
        if not self.selected_source_id:
            messagebox.showinfo("Info", "Please select a data source to save")
            return

        # Validate form
        if not self.name_var.get():
            messagebox.showerror("Error", "Name is required")
            return

        if not self.type_var.get():
            messagebox.showerror("Error", "Type is required")
            return

        # Get source data
        source_data = self.get_source_data()

        # Save the source
        if self.presenter:
            self.presenter.update_data_source(self.selected_source_id, source_data)

    def _on_preview_data(self):
        """Handle preview data button click."""
        if not self.selected_source_id:
            messagebox.showinfo("Info", "Please select a data source to preview")
            return

        # Get source data
        source_data = self.get_source_data()

        # Preview the data
        if self.presenter:
            self.presenter.preview_data_source(self.selected_source_id, source_data)

    def _on_type_changed(self, value):
        """
        Handle data source type change.

        Args:
            value: New type value
        """
        # Create configuration widgets based on the new type
        self._create_config_widgets(value, {})

    def _on_browse_csv(self):
        """Handle browse button click for CSV files."""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.config_widgets["file_path"].delete(0, "end")
            self.config_widgets["file_path"].insert(0, file_path)

    def _on_browse_json(self):
        """Handle browse button click for JSON files."""
        file_path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            self.config_widgets["file_path"].delete(0, "end")
            self.config_widgets["file_path"].insert(0, file_path)
