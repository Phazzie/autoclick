"""
Main Application class for AUTOCLICK.
SOLID: Coordinates views and presenters but delegates specific functionality.
KISS: Simple initialization and coordination.
"""
import os
import json
import customtkinter as ctk
from typing import Dict, Any, Optional

# Import views
from src.ui.views.sidebar_view import SidebarView
from src.ui.views.statusbar_view import StatusbarView
from src.ui.views.variable_view import VariableView
from src.ui.views.credential_view import CredentialView
from src.ui.views.condition_view import ConditionView
from src.ui.views.loop_view import LoopView
from src.ui.views.error_view import ErrorView

# Import presenters
from src.ui.presenters.sidebar_presenter import SidebarPresenter
from src.ui.presenters.variable_presenter import VariablePresenter
from src.ui.presenters.credential_presenter import CredentialPresenter
from src.ui.presenters.condition_presenter import ConditionPresenter
from src.ui.presenters.loop_presenter import LoopPresenter
from src.ui.presenters.error_presenter import ErrorPresenter

# Import backend components
from src.core.credentials.credential_manager import CredentialManager
from src.core.context.variable_storage import VariableStorage
from src.core.workflow.workflow_engine import WorkflowEngine
from src.core.conditions.condition_factory import ConditionFactory

# Import adapters
from src.ui.adapters.credential_adapter import CredentialAdapter
from src.ui.adapters.variable_adapter import VariableAdapter
from src.ui.adapters.workflow_adapter import WorkflowAdapter
from src.ui.adapters.error_adapter import ErrorAdapter
from src.ui.adapters.data_source_adapter import DataSourceAdapter
from src.ui.adapters.condition_adapter import ConditionAdapter
from src.ui.adapters.loop_adapter import LoopAdapter

# Import constants
from src.ui.utils.constants import (
    INITIAL_WIDTH, INITIAL_HEIGHT, MIN_WIDTH, MIN_HEIGHT,
    SETTINGS_FILE, PAD_X_OUTER, PAD_Y_OUTER
)
from src.ui.utils.ui_utils import get_app_path, configure_ttk_style

class AutoClickApp:
    """Main application class that coordinates views and presenters."""

    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("AUTOCLICK")
        self.root.geometry(f"{INITIAL_WIDTH}x{INITIAL_HEIGHT}")
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)

        # Initialize settings
        self.settings = self._load_settings()

        # Set appearance mode based on settings
        self._apply_theme(self.settings.get("theme", "Dark"))

        # Initialize services
        self._init_services()

        # Create main window
        self.window = ctk.CTkToplevel(self.root)
        self.window.title("AUTOCLICK")
        self.window.geometry(f"{INITIAL_WIDTH}x{INITIAL_HEIGHT}")
        self.window.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create UI components
        self._create_ui_components()

        # Initialize views and presenters
        self._init_views_and_presenters()

        # Set up layout
        self._setup_layout()

        # Show initial tab
        self.navigate_to_tab("Workflow Builder")

        # Update status
        self.update_status("Application initialized successfully.")

    def _load_settings(self) -> Dict[str, Any]:
        """Load application settings from file."""
        settings_path = get_app_path(SETTINGS_FILE)
        default_settings = {
            "theme": "Dark",
            "last_tab": "Workflow Builder",
            "workflows_dir": "workflows",
            "auto_save": True,
            "save_interval": 300,  # seconds
        }

        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**default_settings, **loaded_settings}
            except Exception as e:
                print(f"Error loading settings: {e}")

        return default_settings

    def _save_settings(self):
        """Save application settings to file."""
        settings_path = get_app_path(SETTINGS_FILE)
        try:
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def _init_services(self):
        """Initialize service instances."""
        # Create backend service instances
        self.credential_manager = CredentialManager()
        self.variable_storage = VariableStorage()
        self.workflow_engine = WorkflowEngine()
        self.condition_factory = ConditionFactory  # This is already an instance, not a class

        # Create adapter services that bridge between UI expectations and backend interfaces
        self.credential_service = CredentialAdapter(self.credential_manager)
        self.variable_service = VariableAdapter(self.variable_storage)
        self.workflow_service = WorkflowAdapter(self.workflow_engine)
        self.error_service = ErrorAdapter()
        self.condition_service = ConditionAdapter(self.condition_factory)
        self.loop_service = LoopAdapter(self.workflow_engine, self.condition_factory)

        # TODO: Create additional adapter services as needed
        self.datasource_service = None  # To be implemented
        self.reporting_service = None  # To be implemented

    def _create_ui_components(self):
        """Create the main UI components."""
        # Configure grid
        self.window.grid_columnconfigure(1, weight=1)  # Content area expands
        self.window.grid_rowconfigure(1, weight=1)     # Content area expands

        # Create sidebar
        self.sidebar_frame = SidebarView(self.window)

        # Create main content area with tabs
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.grid_rowconfigure(0, weight=1)
        self.tabview.grid_columnconfigure(0, weight=1)

        # Create tabs
        self.tabs = {}
        tab_names = [
            "Workflow Builder", "Variable Management", "Credential Management",
            "Condition Editor", "Loop Configuration", "Error Handling", "Reporting", "Data Sources", "Settings"
        ]
        for tab_name in tab_names:
            tab = self.tabview.add(tab_name)
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)
            self.tabs[tab_name] = tab

        # Hide the tab bar - we'll use the sidebar for navigation
        self.tabview._segmented_button.grid_forget()

        # Create status bar
        self.statusbar = StatusbarView(self.window)

    def _init_views_and_presenters(self):
        """Initialize all views and presenters."""
        # Create view instances for tabs
        self.variable_view = VariableView(self.tabs["Variable Management"])
        self.credential_view = CredentialView(self.tabs["Credential Management"])
        self.condition_view = ConditionView(self.tabs["Condition Editor"])
        self.loop_view = LoopView(self.tabs["Loop Configuration"])
        self.error_view = ErrorView(self.tabs["Error Handling"])

        # Create presenter instances
        self.sidebar_presenter = SidebarPresenter(self.sidebar_frame, self)
        self.variable_presenter = VariablePresenter(
            view=self.variable_view,
            app=self,
            service=self.variable_service
        )
        self.credential_presenter = CredentialPresenter(
            view=self.credential_view,
            app=self,
            service=self.credential_service
        )
        self.condition_presenter = ConditionPresenter(
            view=self.condition_view,
            app=self,
            service=self.condition_service
        )
        self.loop_presenter = LoopPresenter(
            view=self.loop_view,
            app=self,
            service=self.loop_service
        )
        self.error_presenter = ErrorPresenter(
            view=self.error_view,
            app=self,
            service=self.error_service
        )

        # Link views to presenters
        self.sidebar_frame.set_presenter(self.sidebar_presenter)
        self.variable_view.set_presenter(self.variable_presenter)
        self.credential_view.set_presenter(self.credential_presenter)
        self.condition_view.set_presenter(self.condition_presenter)
        self.loop_view.set_presenter(self.loop_presenter)
        self.error_view.set_presenter(self.error_presenter)

        # Build UI for each view
        self.sidebar_frame.build_ui()
        self.variable_view.build_ui()
        self.credential_view.build_ui()
        self.condition_view.build_ui()
        self.loop_view.build_ui()
        self.error_view.build_ui()

        # Initialize presenters
        self.sidebar_presenter.initialize_view()
        self.variable_presenter.initialize_view()
        self.credential_presenter.initialize_view()
        self.condition_presenter.initialize_view()
        self.loop_presenter.initialize_view()
        self.error_presenter.initialize_view()

    def _setup_layout(self):
        """Set up the main application layout."""
        # Place components in the grid
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(PAD_X_OUTER, 0), pady=PAD_Y_OUTER)
        self.tabview.grid(row=0, column=1, sticky="nsew", padx=PAD_X_OUTER, pady=PAD_Y_OUTER)
        self.statusbar.grid(row=1, column=1, sticky="ew", padx=PAD_X_OUTER, pady=(0, PAD_Y_OUTER))

    def navigate_to_tab(self, tab_name: str):
        """Switch to the specified tab."""
        if tab_name in self.tabs:
            self.tabview.set(tab_name)
            self.update_status(f"Navigated to {tab_name}")
            # Update settings
            self.settings["last_tab"] = tab_name
            self._save_settings()

    def update_status(self, message: str):
        """Update the status bar message."""
        if hasattr(self, 'statusbar'):
            self.statusbar.update_status(message)

    def request_theme_toggle(self):
        """Toggle between light and dark themes."""
        current_theme = ctk.get_appearance_mode()
        new_theme = "Light" if current_theme == "Dark" else "Dark"
        self._apply_theme(new_theme)
        self.settings["theme"] = new_theme
        self._save_settings()
        self.update_status(f"Theme changed to {new_theme} mode")

    def _apply_theme(self, theme: str):
        """Apply the specified theme."""
        ctk.set_appearance_mode(theme)
        configure_ttk_style(theme)

        # Update sidebar theme switch if it exists
        if hasattr(self, 'sidebar_frame'):
            self.sidebar_frame.set_theme_switch_state(theme)

    def on_close(self):
        """Handle application close event."""
        # Save settings
        self._save_settings()

        # Close the application
        self.window.destroy()
        self.root.destroy()

    def run(self):
        """Run the application main loop."""
        # Show the main window
        self.window.deiconify()

        # Start the main loop
        self.root.mainloop()
