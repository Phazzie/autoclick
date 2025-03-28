"""Service for managing keyboard shortcuts"""
import logging
import tkinter as tk
from typing import Any, Callable, Dict, Optional


class ShortcutService:
    """Service for managing keyboard shortcuts"""
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the shortcut service
        
        Args:
            root: Root Tkinter window
        """
        self.logger = logging.getLogger(__name__)
        self.root = root
        self.shortcuts: Dict[str, Dict[str, Any]] = {}
    
    def register_shortcut(
        self,
        key_sequence: str,
        callback: Callable[[], None],
        description: str
    ) -> None:
        """
        Register a keyboard shortcut
        
        Args:
            key_sequence: Key sequence (e.g., "Control-s", "Alt-F4")
            callback: Function to call when the shortcut is triggered
            description: Description of the shortcut
        """
        self.logger.debug(f"Registering shortcut: {key_sequence} - {description}")
        
        # Store shortcut information
        self.shortcuts[key_sequence] = {
            "callback": callback,
            "description": description
        }
        
        # Bind the shortcut to the root window
        self.root.bind(f"<{key_sequence}>", lambda event: callback())
    
    def unregister_shortcut(self, key_sequence: str) -> None:
        """
        Unregister a keyboard shortcut
        
        Args:
            key_sequence: Key sequence to unregister
        """
        self.logger.debug(f"Unregistering shortcut: {key_sequence}")
        
        if key_sequence in self.shortcuts:
            # Unbind the shortcut
            self.root.unbind(f"<{key_sequence}>")
            
            # Remove from shortcuts dictionary
            del self.shortcuts[key_sequence]
    
    def get_all_shortcuts(self) -> Dict[str, str]:
        """
        Get all registered shortcuts
        
        Returns:
            Dictionary mapping key sequences to descriptions
        """
        return {
            key: info["description"]
            for key, info in self.shortcuts.items()
        }
    
    def show_shortcuts_dialog(self) -> None:
        """Show a dialog with all registered shortcuts"""
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Keyboard Shortcuts")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create frame
        frame = tk.Frame(dialog, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add title
        title_label = tk.Label(
            frame,
            text="Keyboard Shortcuts",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Create listbox
        listbox = tk.Listbox(frame, width=50, height=15)
        listbox.pack(fill=tk.BOTH, expand=True)
        
        # Add shortcuts to listbox
        for key, description in self.get_all_shortcuts().items():
            listbox.insert(tk.END, f"{key:<15} - {description}")
        
        # Add close button
        close_button = tk.Button(
            frame,
            text="Close",
            command=dialog.destroy
        )
        close_button.pack(pady=10)
