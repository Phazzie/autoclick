"""Handles logic for the SidebarView."""
from .base_presenter import BasePresenter
import customtkinter as ctk # Needed for get_appearance_mode
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..views.sidebar_view import SidebarView
    from app import AutoClickApp # Import App for type hint

class SidebarPresenter(BasePresenter): # Type hint view and app
    view: 'SidebarView'
    app: 'AutoClickApp'

    def __init__(self, view: 'SidebarView', app: 'AutoClickApp'): # Needs App reference
        super().__init__(view=view, app=app)
        # Initialization done via initialize_view called by App

    def initialize_view(self):
        """Populate nav items and set initial theme switch state."""
        if not self.view: return
        try:
            if hasattr(self.view, 'set_navigation_items'):
                 self.view.set_navigation_items(self._get_nav_items())
            if hasattr(self.view, 'set_theme_switch_state'):
                 self.view.set_theme_switch_state(ctk.get_appearance_mode())
        except Exception as e:
             self._handle_error("initializing sidebar view", e)

    def _get_nav_items(self) -> List[Tuple[str, str]]:
        """Returns the list of navigation items (text, tab_name)."""
        # Could be dynamic based on user role or config in future
        return [
            ("Workflow Builder", "Workflow Builder"), ("Action Execution", "Action Execution"),
            ("Variable Management", "Variable Management"), ("Credential Management", "Credential Management"),
            ("Condition Editor", "Condition Editor"), ("Loop Configuration", "Loop Configuration"),
            ("Error Handling", "Error Handling"), ("Reporting", "Reporting"),
            ("Data Sources", "Data Sources"), ("Settings", "Settings")
        ]

    def navigate_to(self, tab_name: str):
        """Instructs the main app to switch tabs."""
        if self.app and hasattr(self.app, 'navigate_to_tab'):
             self.app.navigate_to_tab(tab_name)
        else: print(f"Error: Cannot navigate. App reference missing or invalid.")

    def toggle_theme(self):
        """Instructs the main app to toggle the theme."""
        if self.app and hasattr(self.app, 'request_theme_toggle'):
             self.app.request_theme_toggle()
             # View state is updated by App calling apply_theme_change -> sidebar.set_theme_switch_state
        else: print("Error: Cannot toggle theme. App reference missing or invalid.")
