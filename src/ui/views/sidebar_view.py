"""
Defines the Sidebar View component.
SOLID: Responsibility is UI construction and exposing interaction points.
KISS: Simple layout and widget creation.
"""
import customtkinter as ctk
from typing import List, Tuple, Optional, TYPE_CHECKING
from .base_view import BaseView
from ..utils.constants import PAD_X_OUTER as PAD_X, PAD_Y_OUTER as PAD_Y, PAD_Y_INNER as INNER_PAD_Y, CORNER_RADIUS

if TYPE_CHECKING:
    from ..presenters.sidebar_presenter import SidebarPresenter

class SidebarView(BaseView):
    """Sidebar navigation panel.""" # Type hint presenter
    presenter: 'SidebarPresenter'
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=None, width=200, corner_radius=0, **kwargs)
    
    def _create_widgets(self):
        """Creates sidebar widgets. Called by build_ui."""
        self.logo_label = ctk.CTkLabel(self, text="AUTOCLICK", font=ctk.CTkFont(size=20, weight="bold"))
        self.nav_buttons: dict[str, ctk.CTkButton] = {}
        self.theme_switch = ctk.CTkSwitch(self, text="Dark Mode",
                                          command=self._on_theme_toggle,
                                          onvalue="Dark", offvalue="Light")
    
    def _setup_layout(self):
        """Sets up the grid layout. Called by build_ui."""
        self.logo_label.grid(row=0, column=0, padx=PAD_X, pady=(PAD_Y * 2, PAD_Y), sticky="ew")
        # Button layout and theme switch placement happens in set_navigation_items
    
    def set_navigation_items(self, nav_items: List[Tuple[str, str]]):
         """Creates/updates navigation buttons based on data from the presenter."""
         for button in self.nav_buttons.values(): button.destroy()
         self.nav_buttons = {}
         
         row_idx = 1
         for text, tab_name in nav_items:
             if not self.presenter: command = lambda: print(f"Navigate (No Presenter!)")
             else: command = lambda tn=tab_name: self.presenter.navigate_to(tn)
             button = ctk.CTkButton(self, text=text, corner_radius=CORNER_RADIUS, anchor="w", command=command)
             button.grid(row=row_idx, column=0, padx=PAD_X, pady=INNER_PAD_Y, sticky="ew")
             self.nav_buttons[tab_name] = button
             row_idx += 1
         
         self.grid_rowconfigure(row_idx, weight=1) # Push theme switch down
         self.theme_switch.grid(row=row_idx + 1, column=0, padx=PAD_X, pady=(PAD_Y, PAD_Y * 2), sticky="sew")
    
    def _on_theme_toggle(self):
         """Internal handler that safely calls the presenter's method."""
         if self.presenter: self.presenter.toggle_theme()
         else: print("Error: Sidebar presenter not set for theme toggle.")
    
    def set_theme_switch_state(self, mode: str):
        """Updates the theme switch based on the current mode ('Light' or 'Dark')."""
        if hasattr(self, 'theme_switch'): # Ensure widget exists
            if mode == "Dark": self.theme_switch.select()
            else: self.theme_switch.deselect()
