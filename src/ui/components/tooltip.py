"""Tooltip component for UI elements"""
import tkinter as tk
from typing import Any, Optional


class Tooltip:
    """Tooltip component for UI elements"""
    
    def __init__(
        self,
        widget: Any,
        text: str,
        delay: int = 500,
        wrap_length: int = 180,
        background: str = "#ffffe0",
        foreground: str = "black",
        font: Optional[tuple] = None
    ) -> None:
        """
        Initialize the tooltip
        
        Args:
            widget: Widget to attach the tooltip to
            text: Tooltip text
            delay: Delay in milliseconds before showing the tooltip
            wrap_length: Maximum line length for text wrapping
            background: Background color
            foreground: Text color
            font: Font tuple (family, size, style)
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.wrap_length = wrap_length
        self.background = background
        self.foreground = foreground
        self.font = font or ("TkDefaultFont", 9, "normal")
        
        self.tooltip_window = None
        self.scheduled_id = None
        
        # Bind events
        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)
        self.widget.bind("<ButtonPress>", self._on_leave)
    
    def _on_enter(self, event: Any = None) -> None:
        """
        Handle mouse enter event
        
        Args:
            event: Event data
        """
        # Cancel any scheduled tooltip
        self._cancel_scheduled()
        
        # Schedule tooltip display
        self.scheduled_id = self.widget.after(self.delay, self._show_tooltip)
    
    def _on_leave(self, event: Any = None) -> None:
        """
        Handle mouse leave event
        
        Args:
            event: Event data
        """
        # Cancel any scheduled tooltip
        self._cancel_scheduled()
        
        # Hide tooltip if visible
        self._hide_tooltip()
    
    def _cancel_scheduled(self) -> None:
        """Cancel any scheduled tooltip display"""
        if self.scheduled_id:
            self.widget.after_cancel(self.scheduled_id)
            self.scheduled_id = None
    
    def _show_tooltip(self) -> None:
        """Show the tooltip"""
        # Get widget position
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Create tooltip window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Remove window decorations
        
        # Position tooltip
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Create tooltip label
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            justify=tk.LEFT,
            background=self.background,
            foreground=self.foreground,
            relief=tk.SOLID,
            borderwidth=1,
            wraplength=self.wrap_length,
            font=self.font
        )
        label.pack(padx=3, pady=3)
    
    def _hide_tooltip(self) -> None:
        """Hide the tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
