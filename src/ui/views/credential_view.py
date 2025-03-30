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

        # Status filter
        self.status_frame = ctk.CTkFrame(self.header_frame)
        self.status_frame.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.status_label = ctk.CTkLabel(self.status_frame, text="Status:", font=get_default_font())
        self.status_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.status_filter_var = tk.StringVar(value="All")
        self.status_dropdown = ctk.CTkOptionMenu(
            self.status_frame,
            values=["All", "Active", "Success", "Failure", "Inactive"],
            variable=self.status_filter_var,
            command=self._on_status_filter_changed
        )
        self.status_dropdown.grid(row=0, column=1, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)

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
        pass

    # === Event Handlers ===

    def _on_status_filter_changed(self, status: str):
        """Handle status filter change."""
        self.current_status = status
        if self.presenter:
            self.presenter.filter_credentials(status)

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
