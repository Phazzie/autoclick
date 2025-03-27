"""Common UI components"""
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, List, Optional, Tuple


class BrowserSelector:
    """Browser selector component"""
    
    def __init__(
        self,
        parent: Any,
        on_browser_change: Callable[[str], None],
        on_headless_change: Optional[Callable[[bool], None]] = None,
        include_headless: bool = True,
        initial_browser: str = "chrome",
        initial_headless: bool = False
    ) -> None:
        """
        Initialize the browser selector
        
        Args:
            parent: Parent widget
            on_browser_change: Callback for browser change
            on_headless_change: Callback for headless mode change
            include_headless: Whether to include headless mode checkbox
            initial_browser: Initial browser selection
            initial_headless: Initial headless mode
        """
        self.parent = parent
        self.on_browser_change = on_browser_change
        self.on_headless_change = on_headless_change
        self.include_headless = include_headless
        
        # Create frame
        self.frame = ttk.LabelFrame(parent, text="Browser")
        
        # Create browser selection
        self.browser_var = tk.StringVar(value=initial_browser)
        
        # Create radio buttons
        browsers = [
            ("Chrome", "chrome"),
            ("Firefox", "firefox"),
            ("Edge", "edge")
        ]
        
        for text, value in browsers:
            radio = ttk.Radiobutton(
                self.frame,
                text=text,
                variable=self.browser_var,
                value=value,
                command=self._on_browser_change
            )
            radio.pack(side=tk.LEFT, padx=5)
        
        # Create headless mode checkbox if needed
        if include_headless and on_headless_change:
            self.headless_frame = ttk.Frame(self.frame)
            self.headless_frame.pack(side=tk.LEFT, padx=10)
            
            self.headless_var = tk.BooleanVar(value=initial_headless)
            self.headless_check = ttk.Checkbutton(
                self.headless_frame,
                text="Headless Mode",
                variable=self.headless_var,
                command=self._on_headless_change
            )
            self.headless_check.pack(side=tk.LEFT)
    
    def pack(self, **kwargs: Any) -> None:
        """
        Pack the component
        
        Args:
            **kwargs: Pack options
        """
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs: Any) -> None:
        """
        Grid the component
        
        Args:
            **kwargs: Grid options
        """
        self.frame.grid(**kwargs)
    
    def get_browser(self) -> str:
        """
        Get the selected browser
        
        Returns:
            Selected browser
        """
        return self.browser_var.get()
    
    def get_headless(self) -> bool:
        """
        Get the headless mode
        
        Returns:
            Headless mode
        """
        if self.include_headless and hasattr(self, "headless_var"):
            return self.headless_var.get()
        return False
    
    def _on_browser_change(self) -> None:
        """Handle browser change"""
        if self.on_browser_change:
            self.on_browser_change(self.browser_var.get())
    
    def _on_headless_change(self) -> None:
        """Handle headless mode change"""
        if self.on_headless_change:
            self.on_headless_change(self.headless_var.get())


class TreeviewWithScrollbar:
    """Treeview with scrollbar component"""
    
    def __init__(
        self,
        parent: Any,
        columns: List[Tuple[str, str, int]],
        on_select: Optional[Callable[[str], None]] = None,
        on_double_click: Optional[Callable[[str], None]] = None
    ) -> None:
        """
        Initialize the treeview with scrollbar
        
        Args:
            parent: Parent widget
            columns: List of column tuples (id, text, width)
            on_select: Callback for selection
            on_double_click: Callback for double click
        """
        self.parent = parent
        self.on_select = on_select
        self.on_double_click = on_double_click
        
        # Create frame
        self.frame = ttk.Frame(parent)
        
        # Create treeview
        column_ids = [col[0] for col in columns]
        self.treeview = ttk.Treeview(self.frame, columns=column_ids, show="headings")
        
        # Configure columns
        for col_id, col_text, col_width in columns:
            self.treeview.heading(col_id, text=col_text)
            self.treeview.column(col_id, width=col_width)
        
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.frame,
            orient=tk.VERTICAL,
            command=self.treeview.yview
        )
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack treeview and scrollbar
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        if on_select:
            self.treeview.bind("<<TreeviewSelect>>", self._on_select)
        
        if on_double_click:
            self.treeview.bind("<Double-1>", self._on_double_click)
    
    def pack(self, **kwargs: Any) -> None:
        """
        Pack the component
        
        Args:
            **kwargs: Pack options
        """
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs: Any) -> None:
        """
        Grid the component
        
        Args:
            **kwargs: Grid options
        """
        self.frame.grid(**kwargs)
    
    def clear(self) -> None:
        """Clear all items"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
    
    def add_item(self, values: List[Any], tags: Optional[List[str]] = None) -> str:
        """
        Add an item to the treeview
        
        Args:
            values: Values for each column
            tags: Tags for the item
            
        Returns:
            Item ID
        """
        return self.treeview.insert("", tk.END, values=values, tags=tags)
    
    def get_selected_item(self) -> Optional[str]:
        """
        Get the selected item ID
        
        Returns:
            Selected item ID, or None if no item is selected
        """
        selected_items = self.treeview.selection()
        
        if not selected_items:
            return None
        
        return selected_items[0]
    
    def get_selected_values(self) -> Optional[List[Any]]:
        """
        Get the values of the selected item
        
        Returns:
            Values of the selected item, or None if no item is selected
        """
        item_id = self.get_selected_item()
        
        if not item_id:
            return None
        
        return self.treeview.item(item_id, "values")
    
    def _on_select(self, event: Any) -> None:
        """Handle selection"""
        if self.on_select:
            item_id = self.get_selected_item()
            if item_id:
                self.on_select(item_id)
    
    def _on_double_click(self, event: Any) -> None:
        """Handle double click"""
        if self.on_double_click:
            item_id = self.get_selected_item()
            if item_id:
                self.on_double_click(item_id)


class ActionForm:
    """Action form component"""
    
    def __init__(
        self,
        parent: Any,
        on_submit: Callable[[Dict[str, Any]], None],
        on_cancel: Callable[[], None],
        initial_values: Optional[Dict[str, Any]] = None,
        title: str = "Action"
    ) -> None:
        """
        Initialize the action form
        
        Args:
            parent: Parent widget
            on_submit: Callback for form submission
            on_cancel: Callback for form cancellation
            initial_values: Initial form values
            title: Form title
        """
        self.parent = parent
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create form
        self._create_form(initial_values or {})
    
    def _create_form(self, initial_values: Dict[str, Any]) -> None:
        """
        Create the form
        
        Args:
            initial_values: Initial form values
        """
        # Action type
        ttk.Label(self.dialog, text="Action Type:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        
        self.type_var = tk.StringVar(value=initial_values.get("type", "click"))
        type_combo = ttk.Combobox(
            self.dialog,
            textvariable=self.type_var,
            values=["click", "input", "select", "wait", "navigate"]
        )
        type_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Selector
        ttk.Label(self.dialog, text="Selector:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )
        
        self.selector_var = tk.StringVar(value=initial_values.get("selector", ""))
        selector_entry = ttk.Entry(self.dialog, textvariable=self.selector_var)
        selector_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Value
        ttk.Label(self.dialog, text="Value:").grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W
        )
        
        self.value_var = tk.StringVar(value=initial_values.get("value", ""))
        value_entry = ttk.Entry(self.dialog, textvariable=self.value_var)
        value_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Description
        ttk.Label(self.dialog, text="Description:").grid(
            row=3, column=0, padx=5, pady=5, sticky=tk.W
        )
        
        self.description_var = tk.StringVar(value=initial_values.get("description", ""))
        description_entry = ttk.Entry(self.dialog, textvariable=self.description_var)
        description_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Buttons
        buttons_frame = ttk.Frame(self.dialog)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        submit_text = "Update" if initial_values else "Add"
        submit_btn = ttk.Button(buttons_frame, text=submit_text, command=self._on_submit)
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(buttons_frame, text="Cancel", command=self._on_cancel)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Configure grid
        self.dialog.columnconfigure(1, weight=1)
    
    def _on_submit(self) -> None:
        """Handle form submission"""
        action = {
            "type": self.type_var.get(),
            "selector": self.selector_var.get(),
            "value": self.value_var.get(),
            "description": self.description_var.get()
        }
        
        self.dialog.destroy()
        self.on_submit(action)
    
    def _on_cancel(self) -> None:
        """Handle form cancellation"""
        self.dialog.destroy()
        self.on_cancel()
