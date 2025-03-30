"""
Error Handling Presenter for managing error configurations.
SOLID: Single responsibility - business logic for error handling.
KISS: Simple operations with clear error handling.
"""
from typing import Dict, List, Any, Optional, TYPE_CHECKING

from ..presenters.base_presenter import BasePresenter
from ..adapters.error_adapter import ErrorAdapter
from src.core.models import ErrorConfig

if TYPE_CHECKING:
    from ..views.error_view import ErrorView
    from app import AutoClickApp

class ErrorPresenter(BasePresenter[ErrorAdapter]):
    """Presenter for the Error Handling view."""
    
    # Type hints for view and app
    view: 'ErrorView'
    app: 'AutoClickApp'
    
    def __init__(self, view: 'ErrorView', app: 'AutoClickApp', service: ErrorAdapter):
        """
        Initialize the error presenter.
        
        Args:
            view: The error view
            app: The main application
            service: The error adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.error_configs = []  # Cache of error configurations
        self.current_severity = "All"  # Current severity filter
    
    def initialize_view(self):
        """Initialize the view with data."""
        try:
            self.load_error_configs()
            self.update_app_status("Error handling initialized")
        except Exception as e:
            self._handle_error("initializing error handling", e)
    
    def load_error_configs(self):
        """Load error configurations from the service and update the view."""
        try:
            # Get all error configurations from the service
            self.error_configs = self.service.get_all_error_configs()
            
            # Update the view
            self.view.update_error_list(self.error_configs)
            self.update_app_status("Error configurations loaded")
        except Exception as e:
            self._handle_error("loading error configurations", e)
    
    def filter_errors_by_severity(self, severity: str):
        """
        Filter errors by severity.
        
        Args:
            severity: Severity to filter by ("All", "Info", "Warning", "Error", "Critical", "Fatal")
        """
        try:
            if severity == "All":
                # Show all errors
                self.view.update_error_list(self.error_configs)
            else:
                # Show only errors with the selected severity
                filtered_errors = [
                    error for error in self.error_configs
                    if error.severity == severity
                ]
                self.view.update_error_list(filtered_errors)
            
            self.current_severity = severity
            self.update_app_status(f"Filtered errors by {severity} severity")
        except Exception as e:
            self._handle_error(f"filtering errors by {severity}", e)
    
    def select_error(self, error_type: str):
        """
        Handle error selection.
        
        Args:
            error_type: Type of the selected error
        """
        try:
            # Find the error in the cache
            error = None
            for config in self.error_configs:
                if config.error_type == error_type:
                    error = config
                    break
            
            if error:
                # Populate the editor with the error data
                self.view.populate_editor(error)
                self.update_app_status(f"Selected error: {error_type}")
            else:
                # Error not found
                self.view.clear_editor()
                self.view.set_editor_state(False)
                self.update_app_status(f"Error not found: {error_type}")
        except Exception as e:
            self._handle_error(f"selecting error {error_type}", e)
    
    def add_error_config(self, error_type: str, severity: str, action: str, custom_action: Optional[str] = None):
        """
        Add a new error configuration.
        
        Args:
            error_type: Error type identifier
            severity: Error severity (Info, Warning, Error, Critical, Fatal)
            action: Error action (Ignore, Log, Retry, Skip, Stop, Custom)
            custom_action: Custom action script or command
        """
        try:
            # Add the error configuration
            config = self.service.add_error_config(
                error_type=error_type,
                severity=severity,
                action=action,
                custom_action=custom_action
            )
            
            # Add the error to the list
            self.view.add_error_to_list(config)
            
            # Reload error configurations to refresh the cache
            self.load_error_configs()
            
            self.update_app_status(f"Added error configuration: {error_type}")
            
            return config
        except Exception as e:
            self._handle_error(f"adding error configuration {error_type}", e)
            return None
    
    def update_error_config(self, error_type: str, severity: str, action: str, custom_action: Optional[str] = None):
        """
        Update an existing error configuration.
        
        Args:
            error_type: Error type identifier
            severity: Error severity (Info, Warning, Error, Critical, Fatal)
            action: Error action (Ignore, Log, Retry, Skip, Stop, Custom)
            custom_action: Custom action script or command
        """
        try:
            # Update the error configuration
            config = self.service.update_error_config(
                error_type=error_type,
                severity=severity,
                action=action,
                custom_action=custom_action
            )
            
            if config:
                # Update the error in the list
                self.view.update_error_in_list(config)
                
                # Reload error configurations to refresh the cache
                self.load_error_configs()
                
                self.update_app_status(f"Updated error configuration: {error_type}")
            else:
                self.update_app_status(f"Error configuration not found: {error_type}")
            
            return config
        except Exception as e:
            self._handle_error(f"updating error configuration {error_type}", e)
            return None
    
    def save_error_from_editor(self):
        """Save the error configuration from the editor."""
        try:
            # Get the error data from the editor
            error_data = self.view.get_editor_data()
            
            error_type = error_data.get("error_type", "")
            severity = error_data.get("severity", "Warning")
            action = error_data.get("action", "Ignore")
            custom_action = error_data.get("custom_action")
            
            # Check if this is a new error or an update
            existing_error = None
            for config in self.error_configs:
                if config.error_type == error_type:
                    existing_error = config
                    break
            
            if existing_error:
                # Update an existing error
                config = self.update_error_config(
                    error_type=error_type,
                    severity=severity,
                    action=action,
                    custom_action=custom_action
                )
            else:
                # Add a new error
                config = self.add_error_config(
                    error_type=error_type,
                    severity=severity,
                    action=action,
                    custom_action=custom_action
                )
            
            if config:
                # Select the saved error
                self.select_error(error_type)
        except Exception as e:
            self._handle_error("saving error from editor", e)
    
    def get_error_hierarchy(self) -> Dict[str, Any]:
        """
        Get the error type hierarchy.
        
        Returns:
            Dictionary representing the error type hierarchy
        """
        try:
            return self.service.get_error_hierarchy()
        except Exception as e:
            self._handle_error("getting error hierarchy", e)
            return {}
