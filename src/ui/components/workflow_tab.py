"""Workflow tab component"""
import logging
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Optional

from src.ui.components.base_component import BaseComponent
from src.ui.components.tooltip import Tooltip
from src.ui.interfaces.view_interface import WorkflowViewInterface
from src.ui.presenters.workflow_presenter import WorkflowPresenter


class WorkflowTab(BaseComponent, WorkflowViewInterface):
    """Workflow tab component"""

    def __init__(self, parent: Any, presenter: WorkflowPresenter) -> None:
        """
        Initialize the workflow tab

        Args:
            parent: Parent widget
            presenter: Workflow presenter
        """
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.presenter = presenter
        self.presenter.set_view(self)

        # Create UI elements
        self._create_ui()

    def _create_ui(self) -> None:
        """Create the UI elements"""
        # Create header frame
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)

        # Add title
        title_label = ttk.Label(header_frame, text="Workflow Builder", font=("Arial", 14, "bold"))
        title_label.pack(side=tk.LEFT, padx=5)

        # Add buttons
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.pack(side=tk.RIGHT)

        add_btn = ttk.Button(buttons_frame, text="Add Action", command=self._add_action)
        add_btn.pack(side=tk.LEFT, padx=2)
        Tooltip(add_btn, "Add a new action to the workflow (Ctrl+N)")

        remove_btn = ttk.Button(buttons_frame, text="Remove Action", command=self.presenter.remove_action)
        remove_btn.pack(side=tk.LEFT, padx=2)
        Tooltip(remove_btn, "Remove the selected action (Delete)")

        move_up_btn = ttk.Button(buttons_frame, text="Move Up", command=self.presenter.move_action_up)
        move_up_btn.pack(side=tk.LEFT, padx=2)
        Tooltip(move_up_btn, "Move the selected action up (Ctrl+Up)")

        move_down_btn = ttk.Button(buttons_frame, text="Move Down", command=self.presenter.move_action_down)
        move_down_btn.pack(side=tk.LEFT, padx=2)
        Tooltip(move_down_btn, "Move the selected action down (Ctrl+Down)")

        # Create actions frame
        actions_frame = ttk.LabelFrame(self.frame, text="Workflow Actions")
        actions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create treeview for actions
        columns = ("ID", "Type", "Selector", "Value", "Description")
        self.actions_tree = ttk.Treeview(actions_frame, columns=columns, show="headings")

        # Configure columns
        self.actions_tree.heading("ID", text="ID")
        self.actions_tree.heading("Type", text="Type")
        self.actions_tree.heading("Selector", text="Selector")
        self.actions_tree.heading("Value", text="Value")
        self.actions_tree.heading("Description", text="Description")

        self.actions_tree.column("ID", width=50)
        self.actions_tree.column("Type", width=100)
        self.actions_tree.column("Selector", width=200)
        self.actions_tree.column("Value", width=200)
        self.actions_tree.column("Description", width=300)

        # Add tooltips to column headings
        for col, tooltip_text in [
            ("ID", "Unique identifier for the action"),
            ("Type", "Type of action (click, input, select, etc.)"),
            ("Selector", "CSS selector to identify the element"),
            ("Value", "Value to use for the action (e.g., text to input)"),
            ("Description", "Human-readable description of the action")
        ]:
            col_id = f"#{self.actions_tree.heading(col, 'id')}"
            col_widget = self.actions_tree.master.nametowidget(col_id)
            Tooltip(col_widget, tooltip_text)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(actions_frame, orient=tk.VERTICAL, command=self.actions_tree.yview)
        self.actions_tree.configure(yscrollcommand=scrollbar.set)

        # Pack treeview and scrollbar
        self.actions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add events for editing and drag-and-drop
        self.actions_tree.bind("<Double-1>", self._edit_action)
        self.actions_tree.bind("<ButtonPress-1>", self._on_drag_start)
        self.actions_tree.bind("<B1-Motion>", self._on_drag_motion)
        self.actions_tree.bind("<ButtonRelease-1>", self._on_drag_end)

        # Add keyboard shortcuts
        self.frame.bind("<Control-n>", lambda e: self._add_action())
        self.frame.bind("<Delete>", lambda e: self.presenter.remove_action())
        self.frame.bind("<Control-Up>", lambda e: self.presenter.move_action_up())
        self.frame.bind("<Control-Down>", lambda e: self.presenter.move_action_down())

        # Variables for drag-and-drop
        self.drag_source_item = None
        self.drag_source_index = None

    def display_actions(self, actions: List[Dict[str, Any]]) -> None:
        """
        Display workflow actions

        Args:
            actions: List of actions to display
        """
        # Clear existing items
        for item in self.actions_tree.get_children():
            self.actions_tree.delete(item)

        # Add actions to treeview
        for action in actions:
            self.actions_tree.insert(
                "",
                tk.END,
                values=(
                    action.get("id", ""),
                    action.get("type", ""),
                    action.get("selector", ""),
                    action.get("value", ""),
                    action.get("description", "")
                )
            )

    def get_selected_action_id(self) -> Optional[str]:
        """
        Get the ID of the selected action

        Returns:
            The ID of the selected action, or None if no action is selected
        """
        selected_items = self.actions_tree.selection()

        if not selected_items:
            return None

        # Get the ID from the first column
        values = self.actions_tree.item(selected_items[0], "values")
        return values[0] if values else None

    def show_message(self, message: str) -> None:
        """
        Show a message to the user

        Args:
            message: The message to show
        """
        # In a real implementation, this would update a status bar or show a toast
        self.logger.info(message)

        # For now, just print to console
        print(message)

    def _add_action(self) -> None:
        """Add a new action"""
        # Create a dialog to get action details
        dialog = tk.Toplevel(self.frame)
        dialog.title("Add Action")
        dialog.geometry("400x300")
        dialog.transient(self.frame)
        dialog.grab_set()

        # Create form
        ttk.Label(dialog, text="Action Type:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        type_var = tk.StringVar(value="click")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, values=["click", "input", "select", "wait", "navigate"])
        type_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        ttk.Label(dialog, text="Selector:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        selector_var = tk.StringVar()
        selector_entry = ttk.Entry(dialog, textvariable=selector_var)
        selector_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        ttk.Label(dialog, text="Value:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        value_var = tk.StringVar()
        value_entry = ttk.Entry(dialog, textvariable=value_var)
        value_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        ttk.Label(dialog, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        description_var = tk.StringVar()
        description_entry = ttk.Entry(dialog, textvariable=description_var)
        description_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        # Add buttons
        def add_action() -> None:
            action = {
                "type": type_var.get(),
                "selector": selector_var.get(),
                "value": value_var.get(),
                "description": description_var.get()
            }

            self.presenter.add_action(action)
            dialog.destroy()

        ttk.Button(dialog, text="Add", command=add_action).grid(row=4, column=0, padx=5, pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=4, column=1, padx=5, pady=10)

        # Configure grid
        dialog.columnconfigure(1, weight=1)

    def _edit_action(self, event: Any) -> None:
        """
        Edit the selected action

        Args:
            event: Event data
        """
        action_id = self.get_selected_action_id()

        if not action_id:
            return

        # Get the action from the model
        action = self.presenter.model.get_action(action_id)

        if not action:
            self.show_message("Failed to get action details")
            return

        # Create a dialog to edit action details
        dialog = tk.Toplevel(self.frame)
        dialog.title("Edit Action")
        dialog.geometry("400x300")
        dialog.transient(self.frame)
        dialog.grab_set()

        # Create form
        ttk.Label(dialog, text="Action Type:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        type_var = tk.StringVar(value=action.get("type", ""))
        type_combo = ttk.Combobox(dialog, textvariable=type_var, values=["click", "input", "select", "wait", "navigate"])
        type_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        ttk.Label(dialog, text="Selector:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        selector_var = tk.StringVar(value=action.get("selector", ""))
        selector_entry = ttk.Entry(dialog, textvariable=selector_var)
        selector_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        ttk.Label(dialog, text="Value:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        value_var = tk.StringVar(value=action.get("value", ""))
        value_entry = ttk.Entry(dialog, textvariable=value_var)
        value_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        ttk.Label(dialog, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        description_var = tk.StringVar(value=action.get("description", ""))
        description_entry = ttk.Entry(dialog, textvariable=description_var)
        description_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        # Add buttons
        def update_action() -> None:
            updated_action = {
                "type": type_var.get(),
                "selector": selector_var.get(),
                "value": value_var.get(),
                "description": description_var.get()
            }

            self.presenter.update_action(action_id, updated_action)
            dialog.destroy()

        ttk.Button(dialog, text="Update", command=update_action).grid(row=4, column=0, padx=5, pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=4, column=1, padx=5, pady=10)

        # Configure grid
        dialog.columnconfigure(1, weight=1)

    def _on_drag_start(self, event: Any) -> None:
        """
        Start dragging an item

        Args:
            event: Event data
        """
        # Get the item under the cursor
        item = self.actions_tree.identify_row(event.y)

        if not item:
            return

        # Save the item and its index
        self.drag_source_item = item

        # Get all items
        all_items = self.actions_tree.get_children()
        self.drag_source_index = all_items.index(item)

        # Select the item
        self.actions_tree.selection_set(item)

    def _on_drag_motion(self, event: Any) -> None:
        """
        Handle drag motion

        Args:
            event: Event data
        """
        if not self.drag_source_item:
            return

        # Get the item under the cursor
        target_item = self.actions_tree.identify_row(event.y)

        if not target_item:
            return

        # Get all items
        all_items = self.actions_tree.get_children()

        # Get the target index
        target_index = all_items.index(target_item)

        # Move the item if it's a different position
        if target_item != self.drag_source_item:
            # Get the target position (before or after)
            target_y = self.actions_tree.bbox(target_item)[1]
            target_height = self.actions_tree.bbox(target_item)[3]
            middle_y = target_y + target_height // 2

            if event.y < middle_y:  # Above middle, move before
                self.actions_tree.move(self.drag_source_item, "", target_index)
            else:  # Below middle, move after
                self.actions_tree.move(self.drag_source_item, "", target_index + 1)

            # Update the source index
            all_items = self.actions_tree.get_children()
            self.drag_source_index = all_items.index(self.drag_source_item)

    def _on_drag_end(self, event: Any) -> None:
        """
        End dragging an item

        Args:
            event: Event data
        """
        if not self.drag_source_item:
            return

        # Get all items in their new order
        all_items = self.actions_tree.get_children()

        # Get the action IDs in the new order
        action_ids = []
        for item in all_items:
            values = self.actions_tree.item(item, "values")
            action_ids.append(values[0])  # ID is the first column

        # Update the model with the new order
        self.presenter.model.reorder_actions(action_ids)

        # Reset drag variables
        self.drag_source_item = None
        self.drag_source_index = None
