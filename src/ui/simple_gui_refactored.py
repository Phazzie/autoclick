"""Simple GUI for AUTOCLICK (Refactored)"""
import logging
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional

from src.ui.models.workflow_model import WorkflowModel
from src.ui.models.record_model import RecordModel
from src.ui.models.element_model import ElementModel
from src.ui.models.execution_model import ExecutionModel
from src.ui.models.credential_model import CredentialModel

from src.ui.presenters.workflow_presenter import WorkflowPresenter
from src.ui.presenters.record_presenter import RecordPresenter
from src.ui.presenters.element_presenter import ElementPresenter
from src.ui.presenters.execution_presenter import ExecutionPresenter
from src.ui.presenters.credential_presenter import CredentialPresenter

from src.ui.components.workflow_tab import WorkflowTab
from src.ui.components.record_tab import RecordTab
from src.ui.components.element_selector_tab import ElementSelectorTab
from src.ui.components.execution_tab import ExecutionTab
from src.ui.components.credential_tab import CredentialTab

from src.ui.services.dialog_service import DialogService
from src.ui.services.file_service import FileService
from src.ui.services.theme_service import ThemeService
from src.ui.services.execution_service import ExecutionService


class SimpleGUI:
    """Simple GUI for AUTOCLICK"""

    def __init__(self, theme: str = "system") -> None:
        """
        Initialize the GUI

        Args:
            theme: GUI theme to use (system, dark, light)
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing AUTOCLICK GUI")

        # Create services
        self.dialog_service = DialogService()
        self.file_service = FileService()
        self.theme_service = ThemeService(theme)

        # Create models
        self.workflow_model = WorkflowModel()
        self.record_model = RecordModel()
        self.element_model = ElementModel()
        self.execution_model = ExecutionModel()
        self.credential_model = CredentialModel()

        # Create services
        self.execution_service = ExecutionService()

        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("AUTOCLICK - Web Automation")
        self.root.geometry("1024x768")

        # Apply theme
        self._apply_theme()

        # Create the main UI
        self._create_ui()

        self.logger.info("GUI initialized")

    def _apply_theme(self) -> None:
        """Apply the current theme"""
        # In a real implementation with CustomTkinter, we would use:
        # import customtkinter as ctk
        # ctk.set_appearance_mode(self.theme_service.get_theme())
        # ctk.set_default_color_theme("blue")

        # For now, we'll just use ttk styles
        style = ttk.Style()

        if self.theme_service.get_theme() == "dark":
            # Dark theme (approximation with ttk)
            self.root.configure(bg="#2E3440")
            style.configure("TFrame", background="#2E3440")
            style.configure("TLabel", background="#2E3440", foreground="#ECEFF4")
            style.configure("TButton", background="#4C566A", foreground="#ECEFF4")
            style.configure("TNotebook", background="#2E3440", foreground="#ECEFF4")
            style.configure("TNotebook.Tab", background="#3B4252", foreground="#ECEFF4", padding=[10, 2])
            style.map("TNotebook.Tab", background=[("selected", "#5E81AC")], foreground=[("selected", "#ECEFF4")])
        elif self.theme_service.get_theme() == "light":
            # Light theme (approximation with ttk)
            self.root.configure(bg="#ECEFF4")
            style.configure("TFrame", background="#ECEFF4")
            style.configure("TLabel", background="#ECEFF4", foreground="#2E3440")
            style.configure("TButton", background="#D8DEE9", foreground="#2E3440")
            style.configure("TNotebook", background="#ECEFF4", foreground="#2E3440")
            style.configure("TNotebook.Tab", background="#E5E9F0", foreground="#2E3440", padding=[10, 2])
            style.map("TNotebook.Tab", background=[("selected", "#81A1C1")], foreground=[("selected", "#ECEFF4")])

    def _create_ui(self) -> None:
        """Create the main UI components"""
        self.logger.debug("Creating UI components")

        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tab frames
        self.record_tab_frame = ttk.Frame(self.notebook)
        self.element_tab_frame = ttk.Frame(self.notebook)
        self.workflow_tab_frame = ttk.Frame(self.notebook)
        self.execution_tab_frame = ttk.Frame(self.notebook)
        self.credential_tab_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.record_tab_frame, text="Record")
        self.notebook.add(self.element_tab_frame, text="Element Selector")
        self.notebook.add(self.workflow_tab_frame, text="Workflow Builder")
        self.notebook.add(self.execution_tab_frame, text="Execution")
        self.notebook.add(self.credential_tab_frame, text="Credentials")

        # Create presenters
        record_presenter = RecordPresenter(self.record_model)
        element_presenter = ElementPresenter(self.element_model)
        workflow_presenter = WorkflowPresenter(self.workflow_model)
        execution_presenter = ExecutionPresenter(
            self.execution_model,
            self.execution_service
        )
        credential_presenter = CredentialPresenter(self.credential_model)

        # Create tab components
        self.record_tab = RecordTab(self.record_tab_frame, record_presenter)
        self.record_tab.pack(fill=tk.BOTH, expand=True)

        self.element_tab = ElementSelectorTab(self.element_tab_frame, element_presenter)
        self.element_tab.pack(fill=tk.BOTH, expand=True)

        self.workflow_tab = WorkflowTab(self.workflow_tab_frame, workflow_presenter)
        self.workflow_tab.pack(fill=tk.BOTH, expand=True)

        self.execution_tab = ExecutionTab(self.execution_tab_frame, execution_presenter)
        self.execution_tab.pack(fill=tk.BOTH, expand=True)

        self.credential_tab = CredentialTab(self.credential_tab_frame, credential_presenter)
        self.credential_tab.pack(fill=tk.BOTH, expand=True)

        # Create menu
        self._create_menu()

        # Create status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # TODO: Create other tab components

    def _create_menu(self) -> None:
        """Create the menu bar"""
        self.logger.debug("Creating menu bar")

        # Create menu bar
        self.menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Workflow", command=self._new_workflow)
        file_menu.add_command(label="Open Workflow...", command=self._open_workflow)
        file_menu.add_command(label="Save Workflow", command=self._save_workflow)
        file_menu.add_command(label="Save Workflow As...", command=self._save_workflow_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: self.root.focus_get().event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.root.focus_get().event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.root.focus_get().event_generate("<<Paste>>"))

        # View menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="System Theme", command=lambda: self._change_theme("system"))
        view_menu.add_command(label="Dark Theme", command=lambda: self._change_theme("dark"))
        view_menu.add_command(label="Light Theme", command=lambda: self._change_theme("light"))

        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self._show_documentation)
        help_menu.add_command(label="About", command=self._show_about)

        # Add menus to menu bar
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Set menu bar
        self.root.config(menu=self.menu_bar)

    def _new_workflow(self) -> None:
        """Create a new workflow"""
        if self.dialog_service.show_confirmation("New Workflow", "Create a new workflow? Any unsaved changes will be lost."):
            self.workflow_model.clear()
            self.workflow_tab.presenter.refresh_view()
            self.status_var.set("New workflow created")

    def _open_workflow(self) -> None:
        """Open a workflow from a file"""
        file_path = self.dialog_service.open_file([("JSON Files", "*.json"), ("All Files", "*.*")])

        if file_path:
            try:
                workflow_data = self.file_service.load_workflow(file_path)
                if self.workflow_model.from_dict(workflow_data):
                    self.workflow_model.file_path = file_path
                    self.workflow_tab.presenter.refresh_view()
                    self.status_var.set(f"Workflow loaded from {file_path}")
                else:
                    self.dialog_service.show_error("Error", "Failed to import workflow data")
            except Exception as e:
                self.dialog_service.show_error("Error", f"Failed to load workflow: {str(e)}")

    def _save_workflow(self) -> None:
        """Save the current workflow"""
        if self.workflow_model.file_path:
            try:
                self.file_service.save_workflow(self.workflow_model.to_dict(), self.workflow_model.file_path)
                self.status_var.set(f"Workflow saved to {self.workflow_model.file_path}")
            except Exception as e:
                self.dialog_service.show_error("Error", f"Failed to save workflow: {str(e)}")
        else:
            self._save_workflow_as()

    def _save_workflow_as(self) -> None:
        """Save the current workflow to a new file"""
        file_path = self.dialog_service.save_file([("JSON Files", "*.json")], ".json")

        if file_path:
            try:
                self.file_service.save_workflow(self.workflow_model.to_dict(), file_path)
                self.workflow_model.file_path = file_path
                self.status_var.set(f"Workflow saved to {file_path}")
            except Exception as e:
                self.dialog_service.show_error("Error", f"Failed to save workflow: {str(e)}")

    def _change_theme(self, theme: str) -> None:
        """
        Change the GUI theme

        Args:
            theme: Theme name
        """
        self.theme_service.set_theme(theme)
        self._apply_theme()
        self.status_var.set(f"Theme changed to {theme}")

    def _show_documentation(self) -> None:
        """Show documentation"""
        self.dialog_service.show_info("Documentation", "Documentation is not yet available.")

    def _show_about(self) -> None:
        """Show about dialog"""
        self.dialog_service.show_info(
            "About AUTOCLICK",
            "AUTOCLICK - Web Automation Tool\n\n"
            "A streamlined, maintainable, and easily extensible web automation application.\n\n"
            "© 2023 Phazzie"
        )

    def start(self) -> None:
        """Start the GUI"""
        self.logger.info("Starting GUI main loop")
        self.root.mainloop()
