"""
Defines the Statusbar View component.
SOLID: Single responsibility - display status text.
KISS: Very simple widget and method.
"""
import customtkinter as ctk
from .base_view import BaseView
from ..utils.constants import PAD_X_OUTER as PAD_X, PAD_Y_INNER as INNER_PAD_Y
from ..utils.ui_utils import get_small_font

class StatusbarView(BaseView):
    """Status bar at the bottom of the application."""
    def __init__(self, master, **kwargs):
        super().__init__(master, presenter=None, height=30, corner_radius=0, fg_color=None, **kwargs) # Build UI immediately since no presenter needed for its own setup
        self.build_ui()
    
    def _create_widgets(self):
        self.status_label = ctk.CTkLabel(self, text="Initializing...", anchor="w", font=get_small_font())
    
    def _setup_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.status_label.grid(row=0, column=0, padx=PAD_X, pady=INNER_PAD_Y, sticky="ew")
    
    def update_status(self, message: str):
        """Updates the text displayed in the status bar."""
        # Check if widget exists before configuring
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
        else:
             print(f"STATUS (No Label): {message}")
