"""
Defines a base class for view components (Frames within Tabs).
SOLID: Provides a consistent interface for Views.
DRY: Common methods like presenter access, display_message.
KISS: Simple structure.
"""
import customtkinter as ctk
import tkinter as tk # For tk.Misc type hint
from typing import Optional, TYPE_CHECKING, Any, List, Dict # Added Any, List, Dict

# Prevent circular imports for type checking
if TYPE_CHECKING:
    from ..presenters.base_presenter import BasePresenter # Assume a base presenter exists

class BaseView(ctk.CTkFrame):
    """Base class for all view frames within the main tabs."""
    def __init__(self, master: tk.Misc, presenter: Optional['BasePresenter'] = None, **kwargs):
        kwargs.setdefault('fg_color', 'transparent') # Default to transparent background
        super().__init__(master, **kwargs)
        self._presenter = presenter
        self._initialized = False # Flag to ensure widgets created only once

    def build_ui(self):
        """Public method to trigger UI building AFTER presenter is set."""
        # Check if presenter is required but not set
        if self._presenter is None and self.__class__.__name__ != "StatusbarView":
             print(f"CRITICAL ERROR: build_ui called on {self.__class__.__name__} before presenter was set.")
             return # Cannot build without presenter

        if not self._initialized:
             print(f"Building UI for {self.__class__.__name__}...")
             self._create_widgets()
             self._setup_layout()
             self._initialized = True
             print(f"UI Built for {self.__class__.__name__}.")

    def set_presenter(self, presenter: 'BasePresenter'):
        """Links the presenter to this view."""
        self._presenter = presenter
        # If UI hasn't been built yet (e.g., if app builds views then presenters), build now
        # self.build_ui() # Decide on initialization order: build before or after presenter set? App handles this now.

    @property
    def presenter(self) -> 'BasePresenter':
        """Provides access to the presenter, ensuring it's set."""
        if not self._presenter and self.__class__.__name__ != "StatusbarView":
            raise AttributeError(f"Presenter not set for view {self.__class__.__name__}")
        return self._presenter

    # --- Template Methods (must be implemented by subclasses) ---
    def _create_widgets(self):
        raise NotImplementedError(f"{self.__class__.__name__} must implement _create_widgets")
    def _setup_layout(self):
        raise NotImplementedError(f"{self.__class__.__name__} must implement _setup_layout")

    # --- Common View Actions ---
    def update_status(self, message: str):
        """Requests the main app to update the global status bar."""
        if self.presenter and hasattr(self.presenter, 'update_app_status'):
             self.presenter.update_app_status(message)
        else: print(f"STATUS (View: {self.__class__.__name__}): {message}")

    def display_error(self, title: str, message: str):
        from ..utils.ui_utils import show_error; show_error(self, title, message)
    def display_info(self, title: str, message: str):
        from ..utils.ui_utils import show_message; show_message(self, title, message)
    def ask_yes_no(self, title: str, message: str) -> bool:
        from ..utils.ui_utils import ask_yes_no; return ask_yes_no(self, title, message)
    def get_input(self, title: str, prompt: str, initialvalue: str = "") -> Optional[str]:
         from ..utils.ui_utils import get_input; return get_input(self, title, prompt, initialvalue=initialvalue)
    def select_file(self, title: str = "Select File", filetypes: Optional[list] = None) -> Optional[str]:
         from ..utils.ui_utils import select_file; return select_file(self, title, filetypes)
    def select_directory(self, title: str = "Select Directory") -> Optional[str]:
         from ..utils.ui_utils import select_directory; return select_directory(self, title)

    # --- Placeholder methods needed by presenters (Subclasses implement or leave as pass) ---
    # Define common signatures expected by presenters, even if just `pass` here.
    # This acts as an informal interface definition.
    def load_settings(self, settings_dict: Dict): pass # Settings
    def update_variable_list(self, scope_map: Dict[str, List[Dict]]): pass # Variables
    def update_details(self, details_text: Optional[str], **kwargs): pass # Variables/Others - allow kwargs
    def set_action_buttons_state(self, enabled: bool): pass # Variables
    def set_filter_scope(self, scope: str): pass # Variables
    def update_error_tree(self, error_configs: Dict[str, Any]): pass # Errors
    def populate_editor(self, config: Any): pass # Errors, Credentials
    def clear_editor(self, message: Optional[str] = None): pass # Errors, Credentials
    def set_editor_state(self, enabled: bool): pass # Errors
    def get_editor_config(self) -> Dict: return {} # Errors
    def get_editor_data(self) -> Optional[Dict]: return {} # Credentials
    def set_editor_mode(self, mode: str): pass # Credentials
    def update_credential_list(self, data: list, page: int, total_pages: int, total_items: int): pass # Credentials
    def get_selected_credential_ids(self) -> List[str]: return [] # Credentials
    def get_source_config(self) -> Dict: return {} # Data Sources
    def set_source_config(self, config: Dict): pass # Data Sources
    def populate_source_selector(self, sources: List[Dict]): pass # Data Sources
    def set_selected_source(self, source_id: Optional[str], sources: List[Dict]): pass # Data Sources
    def reset_config_fields(self): pass # Data Sources
    def update_preview_grid(self, columns: List, data: List): pass # Data Sources
    def clear_preview(self): pass # Data Sources
    def populate_mapping_lists(self, source_fields: List, target_vars: List): pass # Data Sources
    def clear_mapping_lists(self): pass # Data Sources
    def update_report_list(self, reports: List[Dict]): pass # Reporting
    def display_text_report(self, content: str, title: str): pass # Reporting
    def display_chart(self, figure: Any): pass # Reporting
    def clear_viewer(self): pass # Reporting
    def update_toolbox(self, node_types: List[Dict]): pass # Workflow
    def clear_canvas(self): pass # Workflow
    def draw_node(self, node: Any): pass # Workflow
    def draw_connection(self, connection: Any): pass # Workflow
    def redraw_workflow(self, workflow: Optional[Any]): pass # Workflow
    def select_node_visual(self, node_id: Optional[str]): pass # Workflow
    def display_properties_for_node(self, node_data: Optional[Any]): pass # Workflow
    def get_workflow_name(self) -> str: return "Untitled" # Workflow
    def get_properties_data(self) -> Optional[Dict]: return None # Workflow
