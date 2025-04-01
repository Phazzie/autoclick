"""
Dialog for batch operations on credentials.
SOLID: Single responsibility - UI for batch operations.
KISS: Simple dialog with clear options.
"""
import customtkinter as ctk
import tkinter as tk
from typing import Optional, Dict, Any

from ..utils.constants import PAD_X_INNER, PAD_Y_INNER
from ..utils.ui_utils import get_header_font, get_default_font

class BatchOperationsDialog:
    """Dialog for batch operations on credentials."""

    def __init__(self, parent):
        """
        Initialize the batch operations dialog.

        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.result = False
        self.operation = None
        self.target_status = None
        self.new_status = None

        # Create the dialog
        self._create_dialog()

    def _create_dialog(self):
        """Create the dialog window."""
        # Create a new top-level window
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Batch Operations")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()  # Make the dialog modal

        # Configure the grid
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(3, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(
            self.dialog, text="Batch Operations", font=get_header_font()
        )
        self.header_label.grid(row=0, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Operation selection
        self.operation_frame = ctk.CTkFrame(self.dialog)
        self.operation_frame.grid(row=1, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.operation_label = ctk.CTkLabel(
            self.operation_frame, text="Operation:", font=get_default_font()
        )
        self.operation_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.operation_var = tk.StringVar(value="update_status")

        self.update_radio = ctk.CTkRadioButton(
            self.operation_frame, text="Update Status", variable=self.operation_var, value="update_status",
            command=self._on_operation_changed
        )
        self.update_radio.grid(row=0, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.delete_radio = ctk.CTkRadioButton(
            self.operation_frame, text="Delete Credentials", variable=self.operation_var, value="delete",
            command=self._on_operation_changed
        )
        self.delete_radio.grid(row=0, column=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Status selection
        self.status_frame = ctk.CTkFrame(self.dialog)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Target status
        self.target_label = ctk.CTkLabel(
            self.status_frame, text="Target Status:", font=get_default_font()
        )
        self.target_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.target_var = tk.StringVar(value="Inactive")
        self.target_dropdown = ctk.CTkOptionMenu(
            self.status_frame,
            values=["Active", "Success", "Failure", "Inactive"],
            variable=self.target_var
        )
        self.target_dropdown.grid(row=0, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # New status (for update operation)
        self.new_label = ctk.CTkLabel(
            self.status_frame, text="New Status:", font=get_default_font()
        )
        self.new_label.grid(row=1, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.new_var = tk.StringVar(value="Active")
        self.new_dropdown = ctk.CTkOptionMenu(
            self.status_frame,
            values=["Active", "Success", "Failure", "Inactive"],
            variable=self.new_var
        )
        self.new_dropdown.grid(row=1, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Warning message
        self.warning_frame = ctk.CTkFrame(self.dialog)
        self.warning_frame.grid(row=3, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.warning_label = ctk.CTkLabel(
            self.warning_frame,
            text="Warning: This operation will affect all credentials with the selected status.",
            font=get_default_font(),
            text_color="red",
            wraplength=350
        )
        self.warning_label.pack(padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Buttons
        self.button_frame = ctk.CTkFrame(self.dialog)
        self.button_frame.grid(row=4, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.cancel_button = ctk.CTkButton(
            self.button_frame, text="Cancel", command=self._on_cancel
        )
        self.cancel_button.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.ok_button = ctk.CTkButton(
            self.button_frame, text="OK", command=self._on_ok
        )
        self.ok_button.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Update UI based on initial operation
        self._on_operation_changed()

        # Wait for the dialog to be closed
        self.parent.wait_window(self.dialog)

    def _on_operation_changed(self, *args):
        """Handle operation change."""
        operation = self.operation_var.get()

        if operation == "update_status":
            # Show new status field
            self.new_label.grid()
            self.new_dropdown.grid()

            # Update warning message
            self.warning_label.configure(
                text="Warning: This operation will update the status of all credentials with the selected status."
            )
        else:  # delete
            # Hide new status field
            self.new_label.grid_remove()
            self.new_dropdown.grid_remove()

            # Update warning message
            self.warning_label.configure(
                text="Warning: This operation will permanently delete all credentials with the selected status. This cannot be undone!"
            )

    def _on_cancel(self):
        """Handle cancel button click."""
        self.result = False
        self.dialog.destroy()

    def _on_ok(self):
        """Handle OK button click."""
        try:
            # Store the selected values
            self.operation = self.operation_var.get() if hasattr(self, 'operation_var') else None
            self.target_status = self.target_var.get() if hasattr(self, 'target_var') else None
            self.new_status = self.new_var.get() if hasattr(self, 'new_var') else None

            # Validate required fields
            if not self.operation:
                raise ValueError("Operation type is required")
            if not self.target_status:
                raise ValueError("Target status is required")
            if self.operation == "update_status" and not self.new_status:
                raise ValueError("New status is required for update operation")

            # Set result to True
            self.result = True

            # Close the dialog
            self.dialog.destroy()
        except Exception as e:
            # Show error and keep dialog open
            from ..utils.ui_utils import show_error
            show_error(self.dialog, "Operation Error", str(e))
