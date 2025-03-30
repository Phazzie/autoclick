"""
Context menu component for the UI.
SOLID: Single responsibility - providing context menus.
KISS: Simple implementation with minimal dependencies.
DRY: Reusable component for all context menus in the application.
"""
import tkinter as tk
from typing import Dict, List, Callable, Any, Optional, Tuple, Union


class ContextMenu:
    """
    Reusable context menu component.
    
    This class provides a simple way to create and show context menus
    in any part of the application.
    """
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the context menu.
        
        Args:
            parent: The parent widget for the context menu
        """
        self.parent = parent
        self.menu = tk.Menu(parent, tearoff=0)
        self.items: List[Dict[str, Any]] = []
        
    def add_command(self, label: str, command: Callable, 
                   enabled: bool = True, icon: Optional[tk.PhotoImage] = None) -> None:
        """
        Add a command to the context menu.
        
        Args:
            label: The label for the menu item
            command: The function to call when the item is selected
            enabled: Whether the item is enabled
            icon: Optional icon for the menu item
        """
        self.items.append({
            "type": "command",
            "label": label,
            "command": command,
            "enabled": enabled,
            "icon": icon
        })
        
    def add_separator(self) -> None:
        """Add a separator to the context menu."""
        self.items.append({"type": "separator"})
        
    def add_submenu(self, label: str, submenu: 'ContextMenu', 
                   enabled: bool = True, icon: Optional[tk.PhotoImage] = None) -> None:
        """
        Add a submenu to the context menu.
        
        Args:
            label: The label for the submenu
            submenu: The submenu to add
            enabled: Whether the submenu is enabled
            icon: Optional icon for the submenu
        """
        self.items.append({
            "type": "submenu",
            "label": label,
            "submenu": submenu,
            "enabled": enabled,
            "icon": icon
        })
        
    def show(self, x: int, y: int) -> None:
        """
        Show the context menu at the specified position.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        # Clear the menu
        self.menu.delete(0, tk.END)
        
        # Add items to the menu
        for item in self.items:
            if item["type"] == "command":
                state = tk.NORMAL if item["enabled"] else tk.DISABLED
                if item["icon"]:
                    self.menu.add_command(
                        label=item["label"],
                        command=item["command"],
                        state=state,
                        image=item["icon"],
                        compound=tk.LEFT
                    )
                else:
                    self.menu.add_command(
                        label=item["label"],
                        command=item["command"],
                        state=state
                    )
            elif item["type"] == "separator":
                self.menu.add_separator()
            elif item["type"] == "submenu":
                state = tk.NORMAL if item["enabled"] else tk.DISABLED
                submenu = item["submenu"]
                
                # Create a new menu for the submenu
                submenu_widget = tk.Menu(self.menu, tearoff=0)
                
                # Add items to the submenu
                for subitem in submenu.items:
                    if subitem["type"] == "command":
                        substate = tk.NORMAL if subitem["enabled"] else tk.DISABLED
                        if subitem["icon"]:
                            submenu_widget.add_command(
                                label=subitem["label"],
                                command=subitem["command"],
                                state=substate,
                                image=subitem["icon"],
                                compound=tk.LEFT
                            )
                        else:
                            submenu_widget.add_command(
                                label=subitem["label"],
                                command=subitem["command"],
                                state=substate
                            )
                    elif subitem["type"] == "separator":
                        submenu_widget.add_separator()
                
                # Add the submenu to the menu
                if item["icon"]:
                    self.menu.add_cascade(
                        label=item["label"],
                        menu=submenu_widget,
                        state=state,
                        image=item["icon"],
                        compound=tk.LEFT
                    )
                else:
                    self.menu.add_cascade(
                        label=item["label"],
                        menu=submenu_widget,
                        state=state
                    )
        
        # Show the menu
        try:
            self.menu.tk_popup(x, y)
        finally:
            # Make sure to release the grab
            self.menu.grab_release()
            
    def clear(self) -> None:
        """Clear all items from the context menu."""
        self.items = []
