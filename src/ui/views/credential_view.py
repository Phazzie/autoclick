"""
Credential Management View for displaying and editing credentials.
SOLID: Single responsibility - UI for credential management.
KISS: Simple layout with treeview and editor panel.
"""
import customtkinter as ctk
import tkinter as tk
from typing import Dict, List, Optional, Any, TYPE_CHECKING
from datetime import datetime

from ..views.base_view import BaseView
from ..components.styled_treeview import StyledTreeview
from ..utils.constants import (
    COL_ID_NAME, COL_ID_USERNAME, COL_ID_STATUS, COL_ID_CATEGORY, COL_ID_LAST_USED,
    GRID_ARGS_LABEL, GRID_ARGS_WIDGET, GRID_ARGS_FULL_SPAN_WIDGET,
    PAD_X_OUTER, PAD_Y_OUTER, PAD_X_INNER, PAD_Y_INNER
)
from ..utils.ui_utils import get_header_font, get_default_font, get_small_font
from ..components.context_menu import ContextMenu

if TYPE_CHECKING:
    from ..presenters.credential_presenter import CredentialPresenter

class CredentialView(BaseView):
    """View for managing credentials."""

    # Type hint for the presenter
    presenter: 'CredentialPresenter'

    def __init__(self, master, **kwargs):
        """Initialize the credential view."""
        super().__init__(master, **kwargs)
        self.current_status = "All"  # Default status filter
        self.selected_credential = None  # Currently selected credential

    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into left (list) and right (editor) panels
        self.grid_columnconfigure(0, weight=3)  # List panel
        self.grid_columnconfigure(1, weight=2)  # Editor panel
        self.grid_rowconfigure(0, weight=1)

        # === Left Panel (Credential List) ===
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(1, weight=1)

        # Header with filter controls
        self.header_frame = ctk.CTkFrame(self.list_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, PAD_Y_INNER))
        self.header_frame.grid_columnconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_frame, text="Credentials", font=get_header_font()
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Filter and search frame
        self.filter_frame = ctk.CTkFrame(self.header_frame)
        self.filter_frame.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Status filter
        self.status_label = ctk.CTkLabel(self.filter_frame, text="Status:", font=get_default_font())
        self.status_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.status_filter_var = tk.StringVar(value="All")
        self.status_dropdown = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["All", "Active", "Success", "Failure", "Inactive"],
            variable=self.status_filter_var,
            command=self._on_status_filter_changed,
            width=100
        )
        self.status_dropdown.grid(row=0, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Category filter
        self.category_label = ctk.CTkLabel(self.filter_frame, text="Category:", font=get_default_font())
        self.category_label.grid(row=0, column=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.category_var = tk.StringVar(value="All")
        self.category_dropdown = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["All", "Other", "Email", "Social", "Banking", "Shopping", "Work"],
            variable=self.category_var,
            command=self._on_category_filter_changed,
            width=100
        )
        self.category_dropdown.grid(row=0, column=3, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Search field
        self.search_label = ctk.CTkLabel(self.filter_frame, text="Search:", font=get_default_font())
        self.search_label.grid(row=0, column=4, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search_changed)
        self.search_entry = ctk.CTkEntry(
            self.filter_frame,
            textvariable=self.search_var,
            placeholder_text="Search credentials...",
            width=200
        )
        self.search_entry.grid(row=0, column=5, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Clear search button
        self.clear_search_button = ctk.CTkButton(
            self.filter_frame,
            text="Clear",
            command=self._on_clear_search,
            width=60
        )
        self.clear_search_button.grid(row=0, column=6, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Credential treeview
        self.credential_tree = StyledTreeview(
            self.list_frame,
            columns=(COL_ID_NAME, COL_ID_USERNAME, COL_ID_STATUS, COL_ID_CATEGORY, COL_ID_LAST_USED),
            column_config={
                COL_ID_NAME: {"heading": "Name", "width": 150, "stretch": True},
                COL_ID_USERNAME: {"heading": "Username", "width": 120, "stretch": True},
                COL_ID_STATUS: {"heading": "Status", "width": 80, "stretch": False},
                COL_ID_CATEGORY: {"heading": "Category", "width": 100, "stretch": False},
                COL_ID_LAST_USED: {"heading": "Last Used", "width": 150, "stretch": False}
            },
            show="headings"
        )
        self.credential_tree.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.credential_tree.bind("<<TreeviewSelect>>", self._on_credential_selected)
        self.credential_tree.bind("<Button-3>", self._on_credential_right_click)  # Right-click for context menu

        # Add sorting by clicking on column headers
        for col in (COL_ID_NAME, COL_ID_USERNAME, COL_ID_STATUS, COL_ID_CATEGORY, COL_ID_LAST_USED):
            self.credential_tree.heading(col, command=lambda c=col: self._on_column_click(c))

        # Initialize sorting state
        self.sort_column = COL_ID_NAME  # Default sort column
        self.sort_reverse = False  # Default sort direction

        # Import/Export buttons
        self.import_export_frame = ctk.CTkFrame(self.list_frame)
        self.import_export_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=PAD_Y_INNER)

        self.import_button = ctk.CTkButton(self.import_export_frame, text="Import", command=self._on_import_clicked)
        self.import_button.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.export_button = ctk.CTkButton(self.import_export_frame, text="Export", command=self._on_export_clicked)
        self.export_button.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Batch operations button
        self.batch_button = ctk.CTkButton(self.import_export_frame, text="Batch Operations", command=self._on_batch_operations_clicked)
        self.batch_button.grid(row=0, column=2, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # === Right Panel (Credential Editor) ===
        self.editor_frame = ctk.CTkFrame(self)
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(1, weight=1)

        # Editor header
        self.editor_header = ctk.CTkLabel(
            self.editor_frame, text="Credential Editor", font=get_header_font()
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

        # Username field
        self.username_label = ctk.CTkLabel(self.form_frame, text="Username:", font=get_default_font())
        self.username_label.grid(row=1, column=0, **GRID_ARGS_LABEL)

        self.username_entry = ctk.CTkEntry(self.form_frame)
        self.username_entry.grid(row=1, column=1, **GRID_ARGS_WIDGET)

        # Password field
        self.password_label = ctk.CTkLabel(self.form_frame, text="Password:", font=get_default_font())
        self.password_label.grid(row=2, column=0, **GRID_ARGS_LABEL)

        self.password_entry = ctk.CTkEntry(self.form_frame, show="•")
        self.password_entry.grid(row=2, column=1, **GRID_ARGS_WIDGET)

        # Status field
        self.status_editor_label = ctk.CTkLabel(self.form_frame, text="Status:", font=get_default_font())
        self.status_editor_label.grid(row=3, column=0, **GRID_ARGS_LABEL)

        self.status_var = tk.StringVar(value="Active")
        self.status_dropdown = ctk.CTkOptionMenu(
            self.form_frame,
            values=["Active", "Success", "Failure", "Inactive"],
            variable=self.status_var
        )
        self.status_dropdown.grid(row=3, column=1, **GRID_ARGS_WIDGET)

        # Category field
        self.category_label = ctk.CTkLabel(self.form_frame, text="Category:", font=get_default_font())
        self.category_label.grid(row=4, column=0, **GRID_ARGS_LABEL)

        self.category_entry = ctk.CTkEntry(self.form_frame)
        self.category_entry.grid(row=4, column=1, **GRID_ARGS_WIDGET)

        # Tags field
        self.tags_label = ctk.CTkLabel(self.form_frame, text="Tags:", font=get_default_font())
        self.tags_label.grid(row=5, column=0, **GRID_ARGS_LABEL)

        self.tags_entry = ctk.CTkEntry(self.form_frame)
        self.tags_entry.grid(row=5, column=1, **GRID_ARGS_WIDGET)

        # Notes field
        self.notes_label = ctk.CTkLabel(self.form_frame, text="Notes:", font=get_default_font())
        self.notes_label.grid(row=6, column=0, **GRID_ARGS_LABEL)

        self.notes_text = ctk.CTkTextbox(self.form_frame, height=100)
        self.notes_text.grid(row=6, column=1, **GRID_ARGS_WIDGET)

        # Validation message
        self.validation_label = ctk.CTkLabel(
            self.form_frame, text="", font=get_small_font(), text_color="red"
        )
        self.validation_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Action buttons
        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.grid(row=8, column=0, columnspan=2, sticky="ew", padx=0, pady=PAD_Y_INNER)
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

        # Create context menus
        self._create_context_menus()

    # === Event Handlers ===

    def _on_status_filter_changed(self, status: str):
        """Handle status filter change."""
        self.current_status = status
        if self.presenter:
            self.presenter.filter_credentials(status, self.category_var.get(), self.search_var.get())

    def _on_category_filter_changed(self, category: str):
        """Handle category filter change."""
        if self.presenter:
            self.presenter.filter_credentials(self.status_var.get(), category, self.search_var.get())

    def _on_search_changed(self, *args):
        """Handle search text change."""
        if self.presenter:
            self.presenter.filter_credentials(self.status_var.get(), self.category_var.get(), self.search_var.get())

    def _on_clear_search(self):
        """Handle clear search button click."""
        self.search_var.set("")

    def _on_column_click(self, column):
        """Handle column header click for sorting."""
        # If clicking the same column, reverse the sort order
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            # Otherwise, sort by the new column in ascending order
            self.sort_reverse = False
            self.sort_column = column

        # Apply the sort
        if self.presenter:
            self.presenter.sort_credentials(self.sort_column, self.sort_reverse)

    def _on_credential_selected(self, event):
        """Handle credential selection in the tree."""
        selection = self.credential_tree.selection()
        if not selection:
            self.selected_credential = None
            self.set_editor_state(False)
            return

        item_id = selection[0]
        if self.presenter:
            self.presenter.select_credential(item_id)

    def _on_new_clicked(self):
        """Handle new credential button click."""
        self.clear_editor("Create a new credential")
        self.set_editor_state(True)
        self.selected_credential = None
        self.name_entry.focus_set()

    def _on_save_clicked(self):
        """Handle save button click."""
        if self.presenter:
            self.presenter.save_credential(self.get_editor_data())

    def _on_delete_clicked(self):
        """Handle delete button click."""
        if self.selected_credential and self.presenter:
            self.presenter.delete_credential(self.selected_credential)

    def _on_clear_clicked(self):
        """Handle clear button click."""
        self.clear_editor()
        self.set_editor_state(False)
        self.selected_credential = None

    def _on_import_clicked(self):
        """Handle import button click."""
        if self.presenter:
            self.presenter.import_credentials()

    def _on_export_clicked(self):
        """Handle export button click."""
        if self.presenter:
            self.presenter.export_credentials()

    def _on_batch_operations_clicked(self):
        """Handle batch operations button click."""
        if self.presenter:
            self.presenter.show_batch_operations()

    # === Context Menu Methods ===

    def _create_context_menus(self):
        """Create context menus for the credential view."""
        # Credential context menu (when right-clicking on a credential)
        self.credential_context_menu = ContextMenu(self.credential_tree)
        self.credential_context_menu.add_command("Edit", self._on_edit_from_context_menu)
        self.credential_context_menu.add_command("Delete", self._on_delete_from_context_menu)
        self.credential_context_menu.add_separator()
        self.credential_context_menu.add_command("Copy Username", self._on_copy_username)
        self.credential_context_menu.add_command("Copy Password", self._on_copy_password)
        self.credential_context_menu.add_separator()
        self.credential_context_menu.add_command("Change Status", self._on_change_status)

        # List context menu (when right-clicking on empty space in the list)
        self.list_context_menu = ContextMenu(self.credential_tree)
        self.list_context_menu.add_command("Add New Credential", self._on_add_clicked)
        self.list_context_menu.add_separator()
        self.list_context_menu.add_command("Import Credentials", self._on_import_clicked)
        self.list_context_menu.add_command("Export Credentials", self._on_export_clicked)
        self.list_context_menu.add_separator()
        self.list_context_menu.add_command("Batch Operations", self._on_batch_operations_clicked)
        self.list_context_menu.add_command("Refresh List", self._on_refresh_list)

    def _on_credential_right_click(self, event):
        """Handle right-click on a credential."""
        # Get the item that was clicked
        item_id = self.credential_tree.identify_row(event.y)

        if item_id:  # If an item was clicked
            # Select the item
            self.credential_tree.selection_set(item_id)
            self.selected_credential = item_id

            # Show the credential context menu
            self.credential_context_menu.show(event.x_root, event.y_root)
        else:  # If empty space was clicked
            # Show the list context menu
            self.list_context_menu.show(event.x_root, event.y_root)

    def _on_edit_from_context_menu(self):
        """Handle edit from context menu."""
        if self.selected_credential and self.presenter:
            self.presenter.select_credential(self.selected_credential)

    def _on_delete_from_context_menu(self):
        """Handle delete from context menu."""
        if self.selected_credential and self.presenter:
            self.presenter.delete_credential(self.selected_credential)

    def _on_copy_username(self):
        """Handle copy username from context menu."""
        if self.selected_credential and self.presenter:
            self.presenter.copy_username(self.selected_credential)

    def _on_copy_password(self):
        """Handle copy password from context menu."""
        if self.selected_credential and self.presenter:
            self.presenter.copy_password(self.selected_credential)

    def _on_change_status(self):
        """Handle change status from context menu."""
        if self.selected_credential and self.presenter:
            self.presenter.show_change_status_dialog(self.selected_credential)

    def _on_refresh_list(self):
        """Handle refresh list from context menu."""
        if self.presenter:
            self.presenter.load_credentials()

    # === Public Methods ===

    def update_credential_list(self, credentials: List[Dict]):
        """
        Update the credential tree with new data.

        Args:
            credentials: List of credential records
        """
        # Clear existing items
        for item in self.credential_tree.get_children():
            self.credential_tree.delete(item)

        # Add credentials
        for cred in credentials:
            # Get credential attributes, handling both dict and object access
            is_dict = hasattr(cred, "get")

            # Get ID
            cred_id = cred.get("id", "") if is_dict else cred.id

            # Get name
            name = cred.get("name", "") if is_dict else cred.name

            # Get username
            username = cred.get("username", "") if is_dict else cred.username

            # Get status
            status = cred.get("status", "Active") if is_dict else cred.status

            # Get category
            category = cred.get("category", "") if is_dict else cred.category

            # Format last used date
            last_used = ""
            last_used_value = cred.get("last_used", None) if is_dict else cred.last_used
            if last_used_value:
                if isinstance(last_used_value, datetime):
                    last_used = last_used_value.strftime("%Y-%m-%d %H:%M")
                else:
                    last_used = str(last_used_value)

            # Format tags
            tags = []
            if status == "Success":
                tags.append("success")
            elif status == "Failure":
                tags.append("failure")
            elif status == "Inactive":
                tags.append("inactive")

            # Insert credential
            self.credential_tree.insert(
                "", "end", iid=cred_id,
                values=(
                    name,
                    username,
                    status,
                    category,
                    last_used
                ),
                tags=tags
            )

    def populate_editor(self, credential: Dict):
        """
        Populate the editor with credential data.

        Args:
            credential: Dictionary containing credential data
        """
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, credential.get("name", "") if hasattr(credential, "get") else credential.name)

        self.username_entry.delete(0, "end")
        self.username_entry.insert(0, credential.get("username", "") if hasattr(credential, "get") else credential.username)

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, credential.get("password", "") if hasattr(credential, "get") else credential.password)

        status = credential.get("status", "Active") if hasattr(credential, "get") else credential.status
        self.status_var.set(status)

        category = credential.get("category", "") if hasattr(credential, "get") else credential.category
        self.category_entry.delete(0, "end")
        self.category_entry.insert(0, category or "")

        tags = credential.get("tags", []) if hasattr(credential, "get") else credential.tags
        self.tags_entry.delete(0, "end")
        if tags:
            self.tags_entry.insert(0, ", ".join(tags))

        notes = credential.get("notes", "") if hasattr(credential, "get") else credential.notes
        self.notes_text.delete("1.0", "end")
        if notes:
            self.notes_text.insert("1.0", notes)

        cred_id = credential.get("id", "") if hasattr(credential, "get") else credential.id
        self.selected_credential = cred_id
        self.set_editor_state(True)
        self.validation_label.configure(text="")

        name = credential.get("name", "") if hasattr(credential, "get") else credential.name
        self.editor_header.configure(text=f"Edit Credential: {name}")

    def clear_editor(self, message: Optional[str] = None):
        """
        Clear the editor form.

        Args:
            message: Optional message to display in the editor header
        """
        self.name_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.status_var.set("Active")
        self.category_entry.delete(0, "end")
        self.tags_entry.delete(0, "end")
        self.notes_text.delete("1.0", "end")
        self.validation_label.configure(text="")

        if message:
            self.editor_header.configure(text=message)
        else:
            self.editor_header.configure(text="Credential Editor")

    def set_editor_state(self, enabled: bool):
        """
        Enable or disable the editor.

        Args:
            enabled: Whether the editor should be enabled
        """
        state = "normal" if enabled else "disabled"
        self.name_entry.configure(state=state)
        self.username_entry.configure(state=state)
        self.password_entry.configure(state=state)
        self.status_dropdown.configure(state=state)
        self.category_entry.configure(state=state)
        self.tags_entry.configure(state=state)

        # CTkTextbox doesn't support state parameter in configure
        # Instead, use the configure_state method
        if enabled:
            self.notes_text.configure(state="normal")
        else:
            self.notes_text.configure(state="disabled")

        self.save_button.configure(state=state)
        self.delete_button.configure(state=state)

    def set_filter_status(self, status: str):
        """
        Set the status filter.

        Args:
            status: Status to filter by
        """
        self.status_filter_var.set(status)
        self.current_status = status

    def get_editor_data(self) -> Dict[str, Any]:
        """
        Get the data from the editor form.

        Returns:
            Dictionary containing the credential data
        """
        # Parse tags
        tags_text = self.tags_entry.get().strip()
        tags = []
        if tags_text:
            tags = [tag.strip() for tag in tags_text.split(",")]

        return {
            "id": self.selected_credential or "",
            "name": self.name_entry.get(),
            "username": self.username_entry.get(),
            "password": self.password_entry.get(),
            "status": self.status_var.get(),
            "category": self.category_entry.get(),
            "tags": tags,
            "notes": self.notes_text.get("1.0", "end").strip()
        }

    def show_validation_error(self, message: str):
        """
        Show a validation error message.

        Args:
            message: Error message to display
        """
        self.validation_label.configure(text=message)

    def copy_to_clipboard(self, text: str):
        """Copy text to the clipboard."""
        self.clipboard_clear()
        self.clipboard_append(text)

    def show_status_selection_dialog(self, current_status: str) -> str:
        """Show a dialog to select a new status."""
        # Create a simple dialog
        dialog = tk.Toplevel(self)
        dialog.title("Change Status")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make the dialog modal

        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Add a label
        label = ctk.CTkLabel(
            dialog,
            text=f"Current status: {current_status}\nSelect new status:",
            font=get_default_font()
        )
        label.pack(pady=10)

        # Add radio buttons for status options
        status_var = tk.StringVar(value=current_status)

        for status in ["Active", "Success", "Failure", "Inactive"]:
            radio = ctk.CTkRadioButton(
                dialog,
                text=status,
                variable=status_var,
                value=status,
                font=get_default_font()
            )
            radio.pack(anchor="w", padx=20, pady=5)

        # Add buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(side="bottom", fill="x", pady=10)

        # Result variable
        result = [None]  # Use a list to store the result (to allow modification from inner functions)

        # Cancel button
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=lambda: [result.clear(), result.append(None), dialog.destroy()]
        )
        cancel_button.pack(side="left", padx=10, pady=10, expand=True)

        # OK button
        ok_button = ctk.CTkButton(
            button_frame,
            text="OK",
            command=lambda: [result.clear(), result.append(status_var.get()), dialog.destroy()]
        )
        ok_button.pack(side="right", padx=10, pady=10, expand=True)

        # Wait for the dialog to be closed
        self.wait_window(dialog)

        # Return the selected status
        return result[0]
