"""
Reporting View for displaying and configuring reports.
SOLID: Single responsibility - UI for reporting.
KISS: Simple layout with list and configuration panels.
"""
import customtkinter as ctk
import tkinter as tk
from typing import Dict, List, Optional, Any, TYPE_CHECKING
from datetime import datetime

from ..views.base_view import BaseView
from ..components.styled_treeview import StyledTreeview
from ..utils.constants import (
    GRID_ARGS_LABEL, GRID_ARGS_WIDGET, GRID_ARGS_FULL_SPAN_WIDGET,
    PAD_X_OUTER, PAD_Y_OUTER, PAD_X_INNER, PAD_Y_INNER
)
from ..utils.ui_utils import get_header_font, get_default_font, get_small_font

if TYPE_CHECKING:
    from ..presenters.reporting_presenter import ReportingPresenter

class ReportingView(BaseView):
    """View for managing reports."""

    # Type hint for the presenter
    presenter: 'ReportingPresenter'

    def __init__(self, master, **kwargs):
        """Initialize the reporting view."""
        super().__init__(master, **kwargs)
        self.selected_report = None  # Currently selected report
        self.current_format = "html"  # Default export format
        self.sort_column = "name"  # Default sort column
        self.sort_reverse = False  # Default sort direction

    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into left (list) and right (config/viewer) panels
        self.grid_columnconfigure(0, weight=3)  # List panel
        self.grid_columnconfigure(1, weight=4)  # Config/viewer panel
        self.grid_rowconfigure(0, weight=1)

        # === Left Panel (Report List) ===
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(1, weight=1)

        # Header with controls
        self.header_frame = ctk.CTkFrame(self.list_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, PAD_Y_INNER))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.list_header = ctk.CTkLabel(
            self.header_frame, text="Reports", font=get_header_font()
        )
        self.list_header.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Button frame
        self.button_frame = ctk.CTkFrame(self.header_frame)
        self.button_frame.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.add_button = ctk.CTkButton(
            self.button_frame, text="Add", width=60, command=self._on_add_clicked
        )
        self.add_button.grid(row=0, column=0, padx=(0, PAD_X_INNER))

        self.refresh_button = ctk.CTkButton(
            self.button_frame, text="Refresh", width=60, command=self._on_refresh_clicked
        )
        self.refresh_button.grid(row=0, column=1)

        # Report treeview
        self.report_tree = StyledTreeview(
            self.list_frame,
            columns=("name", "type", "data_source"),
            column_config={
                "name": {"heading": "Name", "width": 150, "stretch": True},
                "type": {"heading": "Type", "width": 100, "stretch": False},
                "data_source": {"heading": "Data Source", "width": 120, "stretch": False}
            },
            show="headings"
        )
        self.report_tree.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.report_tree.bind("<<TreeviewSelect>>", self._on_report_selected)

        # Add column click handlers for sorting
        for col in ("name", "type", "data_source"):
            self.report_tree.heading(col, command=lambda c=col: self._on_column_click(c))

        # Scrollbar for the treeview
        self.tree_scrollbar = ctk.CTkScrollbar(
            self.list_frame, orientation="vertical", command=self.report_tree.yview
        )
        self.tree_scrollbar.grid(row=1, column=1, sticky="ns")
        self.report_tree.configure(yscrollcommand=self.tree_scrollbar.set)

        # === Right Panel (Configuration/Viewer) ===
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)

        # Notebook for tabs
        self.notebook = ctk.CTkTabview(self.right_panel)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Add tabs
        self.config_tab = self.notebook.add("Configuration")
        self.preview_tab = self.notebook.add("Preview")
        
        # Configure tabs
        for tab in (self.config_tab, self.preview_tab):
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)
        
        # === Configuration Tab ===
        self.config_tab.grid_rowconfigure(0, weight=0)  # Header
        self.config_tab.grid_rowconfigure(1, weight=1)  # Form
        
        # Header
        self.config_header = ctk.CTkLabel(
            self.config_tab, text="Report Configuration", font=get_header_font()
        )
        self.config_header.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Form frame
        self.form_frame = ctk.CTkFrame(self.config_tab)
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.form_frame.grid_columnconfigure(0, weight=0)  # Labels
        self.form_frame.grid_columnconfigure(1, weight=1)  # Inputs
        
        # Name field
        self.name_label = ctk.CTkLabel(self.form_frame, text="Name:", font=get_default_font())
        self.name_label.grid(row=0, column=0, **GRID_ARGS_LABEL)
        
        self.name_entry = ctk.CTkEntry(self.form_frame)
        self.name_entry.grid(row=0, column=1, **GRID_ARGS_WIDGET)
        
        # Type field
        self.type_label = ctk.CTkLabel(self.form_frame, text="Type:", font=get_default_font())
        self.type_label.grid(row=1, column=0, **GRID_ARGS_LABEL)
        
        self.type_var = tk.StringVar()
        self.type_dropdown = ctk.CTkOptionMenu(
            self.form_frame, variable=self.type_var, values=["SummaryTable", "BarChart", "LineChart", "PieChart"],
            command=self._on_type_changed
        )
        self.type_dropdown.grid(row=1, column=1, **GRID_ARGS_WIDGET)
        
        # Data source field
        self.data_source_label = ctk.CTkLabel(self.form_frame, text="Data Source:", font=get_default_font())
        self.data_source_label.grid(row=2, column=0, **GRID_ARGS_LABEL)
        
        self.data_source_var = tk.StringVar()
        self.data_source_dropdown = ctk.CTkOptionMenu(
            self.form_frame, variable=self.data_source_var, values=["None"],
            command=self._on_data_source_changed
        )
        self.data_source_dropdown.grid(row=2, column=1, **GRID_ARGS_WIDGET)
        
        # Content options frame
        self.content_options_label = ctk.CTkLabel(
            self.form_frame, text="Content Options:", font=get_default_font()
        )
        self.content_options_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.content_options_frame = ctk.CTkFrame(self.form_frame)
        self.content_options_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.content_options_frame.grid_columnconfigure(1, weight=1)
        
        # Dynamic content options will be added here based on report type
        
        # Style options frame
        self.style_options_label = ctk.CTkLabel(
            self.form_frame, text="Style Options:", font=get_default_font()
        )
        self.style_options_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.style_options_frame = ctk.CTkFrame(self.form_frame)
        self.style_options_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.style_options_frame.grid_columnconfigure(1, weight=1)
        
        # Dynamic style options will be added here based on report type
        
        # Validation message
        self.validation_label = ctk.CTkLabel(
            self.form_frame, text="", font=get_small_font(), text_color="red"
        )
        self.validation_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Action buttons
        self.action_frame = ctk.CTkFrame(self.form_frame)
        self.action_frame.grid(row=8, column=0, columnspan=2, sticky="ew", padx=0, pady=PAD_Y_INNER)
        self.action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.save_button = ctk.CTkButton(
            self.action_frame, text="Save", command=self._on_save_clicked
        )
        self.save_button.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.delete_button = ctk.CTkButton(
            self.action_frame, text="Delete", command=self._on_delete_clicked
        )
        self.delete_button.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.generate_button = ctk.CTkButton(
            self.action_frame, text="Generate", command=self._on_generate_clicked
        )
        self.generate_button.grid(row=0, column=2, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.clear_button = ctk.CTkButton(
            self.action_frame, text="Clear", command=self._on_clear_clicked
        )
        self.clear_button.grid(row=0, column=3, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Format selection
        self.format_frame = ctk.CTkFrame(self.form_frame)
        self.format_frame.grid(row=9, column=0, columnspan=2, sticky="ew", padx=0, pady=PAD_Y_INNER)
        self.format_frame.grid_columnconfigure(0, weight=0)
        self.format_frame.grid_columnconfigure(1, weight=1)
        
        self.format_label = ctk.CTkLabel(
            self.format_frame, text="Export Format:", font=get_default_font()
        )
        self.format_label.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.format_var = tk.StringVar(value="html")
        self.format_dropdown = ctk.CTkOptionMenu(
            self.format_frame, variable=self.format_var, values=["html", "pdf", "csv", "png"],
            command=self._on_format_changed
        )
        self.format_dropdown.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER, sticky="w")
        
        # === Preview Tab ===
        self.preview_tab.grid_rowconfigure(0, weight=0)  # Header
        self.preview_tab.grid_rowconfigure(1, weight=1)  # Content
        
        # Header
        self.preview_header = ctk.CTkLabel(
            self.preview_tab, text="Report Preview", font=get_header_font()
        )
        self.preview_header.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Preview frame
        self.preview_frame = ctk.CTkFrame(self.preview_tab)
        self.preview_frame.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(0, weight=1)
        
        # Text preview (for text-based reports)
        self.text_preview = ctk.CTkTextbox(self.preview_frame, wrap="word")
        self.text_preview.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Chart preview (for chart-based reports)
        self.chart_frame = ctk.CTkFrame(self.preview_frame)
        # Not adding to grid initially - will be shown when needed
        
        # Set initial state
        self.set_editor_state(False)

    def _setup_layout(self):
        """Set up the layout grid."""
        # Main layout already set up in _create_widgets
        pass

    # === Event Handlers ===

    def _on_column_click(self, column):
        """Handle column header click for sorting."""
        if self.presenter:
            # Toggle sort direction if clicking the same column
            if self.sort_column == column:
                self.sort_reverse = not self.sort_reverse
            else:
                self.sort_column = column
                self.sort_reverse = False
            
            self.presenter.sort_reports(column, self.sort_reverse)

    def _on_report_selected(self, event):
        """Handle report selection in the tree."""
        selection = self.report_tree.selection()
        if not selection:
            return
        
        self.selected_report = selection[0]
        if self.presenter:
            self.presenter.select_report(self.selected_report)

    def _on_add_clicked(self):
        """Handle add button click."""
        if self.presenter:
            self.presenter.create_new_report()

    def _on_refresh_clicked(self):
        """Handle refresh button click."""
        if self.presenter:
            self.presenter.load_reports()

    def _on_save_clicked(self):
        """Handle save button click."""
        if self.presenter:
            report_data = self.get_editor_data()
            self.presenter.save_report(report_data)

    def _on_delete_clicked(self):
        """Handle delete button click."""
        if self.presenter and self.selected_report:
            self.presenter.delete_report(self.selected_report)

    def _on_generate_clicked(self):
        """Handle generate button click."""
        if self.presenter and self.selected_report:
            self.presenter.generate_report(self.selected_report, self.format_var.get())

    def _on_clear_clicked(self):
        """Handle clear button click."""
        self.clear_editor()
        self.selected_report = None
        self.report_tree.selection_remove(self.report_tree.selection())
        self.set_editor_state(False)

    def _on_type_changed(self, type_name):
        """Handle report type change."""
        if self.presenter:
            self.presenter.update_type_options(type_name)

    def _on_data_source_changed(self, data_source_id):
        """Handle data source change."""
        if self.presenter:
            self.presenter.update_data_source_options(data_source_id)

    def _on_format_changed(self, format_type):
        """Handle format change."""
        self.current_format = format_type

    # === Public Methods ===

    def update_report_list(self, reports: List[Dict]):
        """
        Update the report list with the given reports.
        
        Args:
            reports: List of report data
        """
        # Clear the tree
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Add reports to the tree
        for report in reports:
            self.report_tree.insert(
                "", "end", report["id"],
                values=(
                    report["name"],
                    report["type"],
                    report.get("data_source_id", "None")
                )
            )

    def display_report(self, report: Dict):
        """
        Display a report in the editor.
        
        Args:
            report: Report data
        """
        # Set basic fields
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, report["name"])
        
        self.type_var.set(report["type"])
        
        data_source_id = report.get("data_source_id")
        if data_source_id:
            self.data_source_var.set(data_source_id)
        else:
            self.data_source_var.set("None")
        
        # Clear existing options
        self._clear_option_frames()
        
        # Add content options
        content_options = report.get("content_options", {})
        row = 0
        for key, value in content_options.items():
            self._add_option_field(self.content_options_frame, key, value, row)
            row += 1
        
        # Add style options
        style_options = report.get("style_options", {})
        row = 0
        for key, value in style_options.items():
            self._add_option_field(self.style_options_frame, key, value, row)
            row += 1
        
        # Select the configuration tab
        self.notebook.set("Configuration")
        
        # Enable the editor
        self.set_editor_state(True)

    def _add_option_field(self, parent, key, value, row):
        """Add an option field to the given parent frame."""
        # Create label
        label = ctk.CTkLabel(
            parent, text=f"{key.replace('_', ' ').title()}:", font=get_default_font()
        )
        label.grid(row=row, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Create input based on value type
        if isinstance(value, bool):
            var = tk.BooleanVar(value=value)
            input_widget = ctk.CTkCheckBox(
                parent, text="", variable=var, onvalue=True, offvalue=False
            )
            input_widget.var = var  # Store reference to var
        elif isinstance(value, (int, float)):
            var = tk.StringVar(value=str(value))
            input_widget = ctk.CTkEntry(parent, textvariable=var)
            input_widget.var = var
        elif isinstance(value, list):
            var = tk.StringVar(value=",".join(str(v) for v in value))
            input_widget = ctk.CTkEntry(parent, textvariable=var)
            input_widget.var = var
        else:
            var = tk.StringVar(value=str(value))
            input_widget = ctk.CTkEntry(parent, textvariable=var)
            input_widget.var = var
        
        input_widget.grid(row=row, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Store the widget with its key for later retrieval
        input_widget.option_key = key
        
        # Add to the parent's children dict if it doesn't exist
        if not hasattr(parent, "option_widgets"):
            parent.option_widgets = {}
        
        parent.option_widgets[key] = input_widget

    def _clear_option_frames(self):
        """Clear the content and style option frames."""
        # Clear content options
        for widget in self.content_options_frame.winfo_children():
            widget.destroy()
        
        # Clear style options
        for widget in self.style_options_frame.winfo_children():
            widget.destroy()
        
        # Reset option widgets
        self.content_options_frame.option_widgets = {}
        self.style_options_frame.option_widgets = {}

    def update_type_options(self, type_name: str, content_options: Dict, style_options: Dict):
        """
        Update the options based on the selected report type.
        
        Args:
            type_name: Report type name
            content_options: Default content options for the type
            style_options: Default style options for the type
        """
        # Clear existing options
        self._clear_option_frames()
        
        # Add content options
        row = 0
        for key, value in content_options.items():
            self._add_option_field(self.content_options_frame, key, value, row)
            row += 1
        
        # Add style options
        row = 0
        for key, value in style_options.items():
            self._add_option_field(self.style_options_frame, key, value, row)
            row += 1

    def update_data_sources(self, data_sources: List[Dict]):
        """
        Update the data source dropdown with the given sources.
        
        Args:
            data_sources: List of data source data
        """
        # Update the dropdown values
        values = ["None"] + [source["id"] for source in data_sources]
        self.data_source_dropdown.configure(values=values)

    def display_text_report(self, content: str, title: str):
        """
        Display a text report in the preview.
        
        Args:
            content: Report content
            title: Report title
        """
        # Clear the preview
        self.clear_viewer()
        
        # Update the header
        self.preview_header.configure(text=f"Report Preview: {title}")
        
        # Show the text preview
        self.text_preview.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Set the content
        self.text_preview.delete("1.0", tk.END)
        self.text_preview.insert("1.0", content)
        
        # Select the preview tab
        self.notebook.set("Preview")

    def clear_viewer(self):
        """Clear the report viewer."""
        # Clear text preview
        self.text_preview.delete("1.0", tk.END)
        
        # Hide chart frame
        self.chart_frame.grid_forget()
        
        # Reset header
        self.preview_header.configure(text="Report Preview")

    def clear_editor(self):
        """Clear the report editor."""
        # Clear basic fields
        self.name_entry.delete(0, tk.END)
        self.type_var.set("")
        self.data_source_var.set("None")
        
        # Clear options
        self._clear_option_frames()
        
        # Clear validation message
        self.validation_label.configure(text="")
        
        # Clear viewer
        self.clear_viewer()

    def set_editor_state(self, enabled: bool):
        """
        Set the editor state.
        
        Args:
            enabled: Whether the editor is enabled
        """
        state = "normal" if enabled else "disabled"
        
        # Set state for basic fields
        self.name_entry.configure(state=state)
        self.type_dropdown.configure(state=state)
        self.data_source_dropdown.configure(state=state)
        
        # Set state for buttons
        self.save_button.configure(state=state)
        self.delete_button.configure(state=state)
        self.generate_button.configure(state=state)
        self.format_dropdown.configure(state=state)
        
        # Set state for option widgets
        for frame in (self.content_options_frame, self.style_options_frame):
            if hasattr(frame, "option_widgets"):
                for widget in frame.option_widgets.values():
                    widget.configure(state=state)

    def show_validation_error(self, message: str):
        """
        Show a validation error message.
        
        Args:
            message: Error message
        """
        self.validation_label.configure(text=message)

    def get_editor_data(self) -> Dict[str, Any]:
        """
        Get the data from the editor.
        
        Returns:
            Dictionary with report data
        """
        data = {
            "id": self.selected_report,
            "name": self.name_entry.get(),
            "type": self.type_var.get(),
            "data_source_id": self.data_source_var.get() if self.data_source_var.get() != "None" else None,
            "content_options": {},
            "style_options": {}
        }
        
        # Get content options
        if hasattr(self.content_options_frame, "option_widgets"):
            for key, widget in self.content_options_frame.option_widgets.items():
                value = widget.var.get()
                
                # Convert value based on widget type
                if isinstance(widget, ctk.CTkCheckBox):
                    data["content_options"][key] = bool(value)
                elif isinstance(widget, ctk.CTkEntry):
                    # Try to convert to appropriate type
                    try:
                        if "," in value:
                            # Assume it's a list
                            data["content_options"][key] = [v.strip() for v in value.split(",")]
                        elif value.isdigit():
                            # Integer
                            data["content_options"][key] = int(value)
                        elif value.replace(".", "", 1).isdigit():
                            # Float
                            data["content_options"][key] = float(value)
                        else:
                            # String
                            data["content_options"][key] = value
                    except:
                        # Default to string if conversion fails
                        data["content_options"][key] = value
        
        # Get style options
        if hasattr(self.style_options_frame, "option_widgets"):
            for key, widget in self.style_options_frame.option_widgets.items():
                value = widget.var.get()
                
                # Convert value based on widget type
                if isinstance(widget, ctk.CTkCheckBox):
                    data["style_options"][key] = bool(value)
                elif isinstance(widget, ctk.CTkEntry):
                    # Try to convert to appropriate type
                    try:
                        if "," in value:
                            # Assume it's a list
                            data["style_options"][key] = [v.strip() for v in value.split(",")]
                        elif value.isdigit():
                            # Integer
                            data["style_options"][key] = int(value)
                        elif value.replace(".", "", 1).isdigit():
                            # Float
                            data["style_options"][key] = float(value)
                        else:
                            # String
                            data["style_options"][key] = value
                    except:
                        # Default to string if conversion fails
                        data["style_options"][key] = value
        
        return data
