"""
Data Source Presenter for managing data sources.
SOLID: Single responsibility - business logic for data source management.
KISS: Simple operations with clear error handling.
"""
from typing import Dict, List, Any, Optional, TYPE_CHECKING, Tuple

from ..presenters.base_presenter import BasePresenter
from ..adapters.data_source_adapter import DataSourceAdapter
from src.core.models import DataSourceConfig

if TYPE_CHECKING:
    from ..views.data_source_view import DataSourceView
    from app import AutoClickApp

class DataSourcePresenter(BasePresenter[DataSourceAdapter]):
    """Presenter for the Data Source view."""
    
    # Type hints for view and app
    view: 'DataSourceView'
    app: 'AutoClickApp'
    
    def __init__(self, view: 'DataSourceView', app: 'AutoClickApp', service: DataSourceAdapter):
        """
        Initialize the data source presenter.
        
        Args:
            view: The data source view
            app: The main application
            service: The data source adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.data_sources = []  # Cache of data sources
        self.current_type_filter = "All"  # Current type filter
    
    def initialize_view(self):
        """Initialize the view with data."""
        try:
            self.load_data_sources()
            self.update_app_status("Data source management initialized")
        except Exception as e:
            self._handle_error("initializing data source management", e)
    
    def load_data_sources(self):
        """Load data sources from the service and update the view."""
        try:
            # Get all data sources from the service
            self.data_sources = self.service.get_all_data_sources()
            
            # Update the view
            self.view.update_data_source_list(self.data_sources)
            self.update_app_status("Data sources loaded")
        except Exception as e:
            self._handle_error("loading data sources", e)
    
    def filter_data_sources_by_type(self, type_name: str):
        """
        Filter data sources by type.
        
        Args:
            type_name: Type to filter by ("All", "CSV File", "JSON File", "Database", "API Endpoint")
        """
        try:
            if type_name == "All":
                # Show all data sources
                self.view.update_data_source_list(self.data_sources)
            else:
                # Show only data sources with the selected type
                filtered_sources = [
                    source for source in self.data_sources
                    if source.type == type_name
                ]
                self.view.update_data_source_list(filtered_sources)
            
            self.current_type_filter = type_name
            self.update_app_status(f"Filtered data sources by {type_name} type")
        except Exception as e:
            self._handle_error(f"filtering data sources by {type_name}", e)
    
    def select_data_source(self, source_id: str):
        """
        Handle data source selection.
        
        Args:
            source_id: ID of the selected data source
        """
        try:
            # Get the data source from the service
            source = self.service.get_data_source(source_id)
            
            if source:
                # Populate the editor with the data source data
                self.view.populate_editor(source)
                self.update_app_status(f"Selected data source: {source.name}")
            else:
                # Data source not found
                self.view.clear_editor()
                self.view.set_editor_state(False)
                self.update_app_status(f"Data source not found: {source_id}")
        except Exception as e:
            self._handle_error(f"selecting data source {source_id}", e)
    
    def add_data_source(self, name: str, type_name: str, config_params: Dict[str, Any] = None):
        """
        Add a new data source.
        
        Args:
            name: Data source name
            type_name: Data source type (CSV File, JSON File, Database, API Endpoint)
            config_params: Configuration parameters
        """
        try:
            # Add the data source
            source = self.service.add_data_source(
                name=name,
                type_name=type_name,
                config_params=config_params
            )
            
            # Add the data source to the list
            self.view.add_data_source_to_list(source)
            
            # Reload data sources to refresh the cache
            self.load_data_sources()
            
            self.update_app_status(f"Added data source: {name}")
            
            return source
        except Exception as e:
            self._handle_error(f"adding data source {name}", e)
            return None
    
    def update_data_source(self, source_id: str, name: Optional[str] = None, type_name: Optional[str] = None, config_params: Optional[Dict[str, Any]] = None):
        """
        Update an existing data source.
        
        Args:
            source_id: Data source ID
            name: Data source name
            type_name: Data source type (CSV File, JSON File, Database, API Endpoint)
            config_params: Configuration parameters
        """
        try:
            # Update the data source
            source = self.service.update_data_source(
                source_id=source_id,
                name=name,
                type_name=type_name,
                config_params=config_params
            )
            
            if source:
                # Update the data source in the list
                self.view.update_data_source_in_list(source)
                
                # Reload data sources to refresh the cache
                self.load_data_sources()
                
                self.update_app_status(f"Updated data source: {source.name}")
            else:
                self.update_app_status(f"Data source not found: {source_id}")
            
            return source
        except Exception as e:
            self._handle_error(f"updating data source {source_id}", e)
            return None
    
    def delete_data_source(self, source_id: str):
        """
        Delete a data source.
        
        Args:
            source_id: ID of the data source to delete
        """
        try:
            # Get the data source for confirmation
            source = self.service.get_data_source(source_id)
            
            if not source:
                self.update_app_status(f"Data source not found: {source_id}")
                return False
            
            # Confirm deletion
            if not self.view.ask_yes_no("Confirm Delete", f"Are you sure you want to delete the data source '{source.name}'?"):
                return False
            
            # Delete the data source
            success = self.service.delete_data_source(source_id)
            
            if success:
                # Remove the data source from the list
                self.view.remove_data_source_from_list(source_id)
                
                # Clear the editor if the deleted data source was selected
                if self.view.selected_data_source == source_id:
                    self.view.clear_editor()
                    self.view.set_editor_state(False)
                
                # Reload data sources to refresh the cache
                self.load_data_sources()
                
                self.update_app_status(f"Deleted data source: {source.name}")
                return True
            else:
                self.view.display_error("Delete Failed", f"Failed to delete data source: {source.name}")
                return False
        except Exception as e:
            self._handle_error(f"deleting data source {source_id}", e)
            return False
    
    def get_data_preview(self, source_id: str, max_rows: int = 10):
        """
        Get a preview of the data from a data source.
        
        Args:
            source_id: ID of the data source
            max_rows: Maximum number of rows to return
        """
        try:
            # Get the data preview
            headers, rows = self.service.get_data_preview(source_id, max_rows)
            
            # Display the preview
            self.view.display_data_preview(headers, rows)
            
            self.update_app_status(f"Loaded data preview for {source_id}")
        except Exception as e:
            self._handle_error(f"getting data preview for {source_id}", e)
    
    def save_data_source_from_editor(self):
        """Save the data source from the editor."""
        try:
            # Get the data source data from the editor
            data = self.view.get_editor_data()
            
            source_id = data.get("id", "")
            name = data.get("name", "")
            type_name = data.get("type", "")
            config_params = data.get("config_params", {})
            
            # Check if this is a new data source or an update
            if not source_id:
                # Add a new data source
                source = self.add_data_source(
                    name=name,
                    type_name=type_name,
                    config_params=config_params
                )
                
                if source:
                    # Select the new data source
                    self.select_data_source(source.id)
            else:
                # Update an existing data source
                source = self.update_data_source(
                    source_id=source_id,
                    name=name,
                    type_name=type_name,
                    config_params=config_params
                )
                
                if source:
                    # Select the updated data source
                    self.select_data_source(source.id)
        except Exception as e:
            self._handle_error("saving data source from editor", e)
