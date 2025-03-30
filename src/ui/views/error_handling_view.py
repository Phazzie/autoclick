"""
Error Handling View for configuring error recovery strategies.
SOLID: Single responsibility - UI for error handling configuration.
KISS: Simple interface for configuring error recovery.
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
    from ..presenters.error_handling_presenter import ErrorHandlingPresenter

class ErrorHandlingView(BaseView):
    """View for configuring error recovery strategies."""

    # Type hint for the presenter
    presenter: 'ErrorHandlingPresenter'

    def __init__(self, master, **kwargs):
        """Initialize the error handling view."""
        super().__init__(master, **kwargs)
        self.selected_strategy_id = None  # Currently selected strategy
        self.error_types = []  # List of error types
        self.recovery_strategies = {}  # Dictionary of recovery strategies

    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into strategy list and strategy details
        self.grid_columnconfigure(0, weight=1)  # Strategy list
        self.grid_columnconfigure(1, weight=2)  # Strategy details
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Main content

        # === Header ===
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.header_label = ctk.CTkLabel(
            self.header_frame, text="Error Handling & Recovery", font=get_header_font()
        )
        self.header_label.pack(pady=PAD_Y_INNER)

        # === Strategy List ===
        self.strategy_list_frame = ctk.CTkFrame(self)
        self.strategy_list_frame.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.strategy_list_frame.grid_columnconfigure(0, weight=1)
        self.strategy_list_frame.grid_rowconfigure(0, weight=0)
        self.strategy_list_frame.grid_rowconfigure(1, weight=1)
        self.strategy_list_frame.grid_rowconfigure(2, weight=0)

        self.strategy_list_label = ctk.CTkLabel(
            self.strategy_list_frame, text="Recovery Strategies", font=get_default_font()
        )
        self.strategy_list_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Strategy list treeview
        self.strategy_tree = StyledTreeview(
            self.strategy_list_frame,
            columns=("name", "type"),
            column_config={
                "name": {"width": 150, "heading": "Strategy Name"},
                "type": {"width": 100, "heading": "Error Type"}
            }
        )
        self.strategy_tree.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.strategy_tree.bind("<<TreeviewSelect>>", self._on_strategy_select)

        # Strategy list buttons
        self.strategy_buttons_frame = ctk.CTkFrame(self.strategy_list_frame)
        self.strategy_buttons_frame.grid(row=2, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.add_button = ctk.CTkButton(
            self.strategy_buttons_frame, text="Add", command=self._on_add_strategy
        )
        self.add_button.pack(side="left", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.delete_button = ctk.CTkButton(
            self.strategy_buttons_frame, text="Delete", command=self._on_delete_strategy
        )
        self.delete_button.pack(side="left", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # === Strategy Details ===
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=1, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_rowconfigure(0, weight=0)
        self.details_frame.grid_rowconfigure(1, weight=0)
        self.details_frame.grid_rowconfigure(2, weight=1)
        self.details_frame.grid_rowconfigure(3, weight=0)

        self.details_label = ctk.CTkLabel(
            self.details_frame, text="Strategy Details", font=get_default_font()
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

        # Error type field
        self.type_label = ctk.CTkLabel(
            self.basic_details_frame, text="Error Type:", font=get_default_font()
        )
        self.type_label.grid(row=1, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.type_var = tk.StringVar()
        self.type_dropdown = ctk.CTkOptionMenu(
            self.basic_details_frame,
            values=["Any", "Network", "Timeout", "Authentication", "Permission", "NotFound", "Validation"],
            variable=self.type_var
        )
        self.type_dropdown.grid(row=1, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Recovery action field
        self.action_label = ctk.CTkLabel(
            self.basic_details_frame, text="Action:", font=get_default_font()
        )
        self.action_label.grid(row=2, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.action_var = tk.StringVar()
        self.action_dropdown = ctk.CTkOptionMenu(
            self.basic_details_frame,
            values=["Retry", "Skip", "Abort", "Custom"],
            variable=self.action_var,
            command=self._on_action_changed
        )
        self.action_dropdown.grid(row=2, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Max retries field
        self.retries_label = ctk.CTkLabel(
            self.basic_details_frame, text="Max Retries:", font=get_default_font()
        )
        self.retries_label.grid(row=3, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.retries_var = tk.StringVar(value="3")
        self.retries_entry = ctk.CTkEntry(
            self.basic_details_frame, textvariable=self.retries_var, width=80
        )
        self.retries_entry.grid(row=3, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Retry delay field
        self.delay_label = ctk.CTkLabel(
            self.basic_details_frame, text="Retry Delay (ms):", font=get_default_font()
        )
        self.delay_label.grid(row=4, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.delay_var = tk.StringVar(value="1000")
        self.delay_entry = ctk.CTkEntry(
            self.basic_details_frame, textvariable=self.delay_var, width=80
        )
        self.delay_entry.grid(row=4, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Custom action frame
        self.custom_frame = ctk.CTkFrame(self.details_frame)
        self.custom_frame.grid(row=2, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.custom_frame.grid_columnconfigure(0, weight=1)
        self.custom_frame.grid_rowconfigure(0, weight=0)
        self.custom_frame.grid_rowconfigure(1, weight=1)

        self.custom_label = ctk.CTkLabel(
            self.custom_frame, text="Custom Action Script", font=get_default_font()
        )
        self.custom_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.custom_script = ctk.CTkTextbox(
            self.custom_frame, height=200
        )
        self.custom_script.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Buttons
        self.buttons_frame = ctk.CTkFrame(self.details_frame)
        self.buttons_frame.grid(row=3, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.save_button = ctk.CTkButton(
            self.buttons_frame, text="Save", command=self._on_save_strategy
        )
        self.save_button.pack(side="right", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Initially hide the custom frame and disable the details
        self.custom_frame.grid_remove()
        self._set_details_state(False)

    def _setup_layout(self):
        """Set up the layout grid."""
        # Main layout already set up in _create_widgets
        pass

    def update_strategy_list(self, strategies: List[Dict[str, Any]]):
        """
        Update the strategy list.

        Args:
            strategies: List of strategy dictionaries
        """
        # Clear existing items
        for item in self.strategy_tree.get_children():
            self.strategy_tree.delete(item)

        # Add strategies to the treeview
        for strategy in strategies:
            self.strategy_tree.insert(
                "", "end", iid=strategy["id"],
                values=(strategy["name"], strategy["error_type"])
            )

    def display_strategy_details(self, strategy: Optional[Dict[str, Any]]):
        """
        Display details for a strategy.

        Args:
            strategy: Strategy dictionary, or None to clear
        """
        if not strategy:
            self._set_details_state(False)
            self.name_var.set("")
            self.type_var.set("Any")
            self.action_var.set("Retry")
            self.retries_var.set("3")
            self.delay_var.set("1000")
            self.custom_script.delete("1.0", "end")
            self.custom_frame.grid_remove()
            return

        # Enable details
        self._set_details_state(True)

        # Set basic details
        self.name_var.set(strategy["name"])
        self.type_var.set(strategy["error_type"])
        self.action_var.set(strategy["action"])
        self.retries_var.set(str(strategy.get("max_retries", 3)))
        self.delay_var.set(str(strategy.get("retry_delay", 1000)))

        # Show/hide custom script based on action
        if strategy["action"] == "Custom":
            self.custom_frame.grid()
            self.custom_script.delete("1.0", "end")
            self.custom_script.insert("1.0", strategy.get("custom_script", ""))
        else:
            self.custom_frame.grid_remove()

        # Show/hide retry fields based on action
        if strategy["action"] == "Retry":
            self.retries_label.grid()
            self.retries_entry.grid()
            self.delay_label.grid()
            self.delay_entry.grid()
        else:
            self.retries_label.grid_remove()
            self.retries_entry.grid_remove()
            self.delay_label.grid_remove()
            self.delay_entry.grid_remove()

    def get_strategy_data(self) -> Dict[str, Any]:
        """
        Get the data from the strategy details form.

        Returns:
            Dictionary containing the strategy data
        """
        data = {
            "name": self.name_var.get(),
            "error_type": self.type_var.get(),
            "action": self.action_var.get(),
            "max_retries": int(self.retries_var.get() or 3),
            "retry_delay": int(self.delay_var.get() or 1000)
        }

        if data["action"] == "Custom":
            data["custom_script"] = self.custom_script.get("1.0", "end-1c")

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
        self.action_dropdown.configure(state=state)
        self.retries_entry.configure(state=state)
        self.delay_entry.configure(state=state)
        self.custom_script.configure(state=state)
        self.save_button.configure(state=state)

    # === Event Handlers ===

    def _on_strategy_select(self, event):
        """Handle strategy selection."""
        selected_items = self.strategy_tree.selection()
        if not selected_items:
            self.selected_strategy_id = None
            self.display_strategy_details(None)
            return

        self.selected_strategy_id = selected_items[0]
        if self.presenter:
            self.presenter.select_strategy(self.selected_strategy_id)

    def _on_add_strategy(self):
        """Handle add strategy button click."""
        if self.presenter:
            self.presenter.add_strategy()

    def _on_delete_strategy(self):
        """Handle delete strategy button click."""
        if not self.selected_strategy_id:
            messagebox.showinfo("Info", "Please select a strategy to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this strategy?"):
            if self.presenter:
                self.presenter.delete_strategy(self.selected_strategy_id)

    def _on_save_strategy(self):
        """Handle save strategy button click."""
        if not self.selected_strategy_id:
            messagebox.showinfo("Info", "Please select a strategy to save")
            return

        # Validate form
        if not self.name_var.get():
            messagebox.showerror("Error", "Name is required")
            return

        # Get strategy data
        strategy_data = self.get_strategy_data()

        # Save the strategy
        if self.presenter:
            self.presenter.update_strategy(self.selected_strategy_id, strategy_data)

    def _on_action_changed(self, value):
        """
        Handle action type change.

        Args:
            value: New action value
        """
        # Show/hide custom script based on action
        if value == "Custom":
            self.custom_frame.grid()
        else:
            self.custom_frame.grid_remove()

        # Show/hide retry fields based on action
        if value == "Retry":
            self.retries_label.grid()
            self.retries_entry.grid()
            self.delay_label.grid()
            self.delay_entry.grid()
        else:
            self.retries_label.grid_remove()
            self.retries_entry.grid_remove()
            self.delay_label.grid_remove()
            self.delay_entry.grid_remove()
