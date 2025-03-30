"""
Presenter for the Data Mapping View.
SOLID: Single responsibility - handling data mapping logic.
KISS: Simple delegation to data mapping service.
"""
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING
import json
import os
import uuid
from tkinter import filedialog, messagebox

from ..presenters.base_presenter import BasePresenter
from src.core.data.mapping.mapper import FieldMapping
from src.core.data.mapping.variable_mapper import VariableMapper

if TYPE_CHECKING:
    from ..views.data_mapping_view import DataMappingView
    from ..app import AutoClickApp
    from ..adapters.data_source_adapter import DataSourceAdapter

class DataMappingPresenter(BasePresenter):
    """Presenter for the Data Mapping view."""
    
    # Type hints for view and app
    view: 'DataMappingView'
    app: 'AutoClickApp'
    
    def __init__(self, view: 'DataMappingView', app: 'AutoClickApp', service: 'DataSourceAdapter'):
        """
        Initialize the data mapping presenter.
        
        Args:
            view: The data mapping view
            app: The main application
            service: The data source adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.source_fields = []  # List of source fields
        self.target_variables = []  # List of target variables
        self.mappings = {}  # Dictionary of field mappings
        self.current_data_source_id = None  # ID of the current data source
    
    def initialize_view(self):
        """Initialize the view with data."""
        try:
            # Load source fields from the current data source
            self.load_source_fields()
            
            # Load target variables from the application
            self.load_target_variables()
            
            # Update the view
            self.view.update_source_fields(self.source_fields)
            self.view.update_target_variables(self.target_variables)
            self.view.update_mappings(self.mappings)
            
            self.update_app_status("Data mapping initialized")
        except Exception as e:
            self._handle_error("initializing data mapping", e)
    
    def load_source_fields(self, data_source_id: Optional[str] = None):
        """
        Load source fields from a data source.
        
        Args:
            data_source_id: ID of the data source to load fields from
        """
        try:
            # If no data source ID is provided, use the current one or the first available
            if not data_source_id:
                if self.current_data_source_id:
                    data_source_id = self.current_data_source_id
                elif self.service.data_sources:
                    data_source_id = next(iter(self.service.data_sources))
                else:
                    self.source_fields = []
                    return
            
            # Store the current data source ID
            self.current_data_source_id = data_source_id
            
            # Get the data source
            data_source = self.service.data_sources.get(data_source_id)
            if not data_source:
                self.source_fields = []
                return
            
            # Get a preview of the data to determine fields
            headers, rows = self.service.get_data_preview(data_source_id)
            
            # Create field list
            self.source_fields = []
            for header in headers:
                # Determine field type based on data
                field_type = "String"  # Default type
                if rows:
                    value = rows[0].get(header)
                    if isinstance(value, int):
                        field_type = "Integer"
                    elif isinstance(value, float):
                        field_type = "Float"
                    elif isinstance(value, bool):
                        field_type = "Boolean"
                
                self.source_fields.append({
                    "name": header,
                    "type": field_type
                })
            
            # Update the view
            self.view.update_source_fields(self.source_fields)
            
            self.update_app_status(f"Loaded {len(self.source_fields)} fields from {data_source.name}")
        except Exception as e:
            self._handle_error(f"loading source fields from {data_source_id}", e)
    
    def load_target_variables(self):
        """Load target variables from the application."""
        try:
            # In a real implementation, we would get variables from the application
            # For now, we'll create some example variables
            self.target_variables = [
                {"name": "username", "type": "String"},
                {"name": "password", "type": "String"},
                {"name": "age", "type": "Integer"},
                {"name": "email", "type": "String"},
                {"name": "is_active", "type": "Boolean"}
            ]
            
            # Update the view
            self.view.update_target_variables(self.target_variables)
            
            self.update_app_status(f"Loaded {len(self.target_variables)} target variables")
        except Exception as e:
            self._handle_error("loading target variables", e)
    
    def on_mapping_added(self, mapping_id: str, mapping: Dict[str, Any]):
        """
        Handle a mapping being added.
        
        Args:
            mapping_id: ID of the mapping
            mapping: Mapping data
        """
        try:
            # Store the mapping
            self.mappings[mapping_id] = mapping
            
            self.update_app_status(f"Added mapping from {mapping['source']} to {mapping['target']}")
        except Exception as e:
            self._handle_error(f"adding mapping {mapping_id}", e)
    
    def on_mapping_removed(self, mapping_id: str):
        """
        Handle a mapping being removed.
        
        Args:
            mapping_id: ID of the mapping to remove
        """
        try:
            # Get the mapping
            mapping = self.mappings.get(mapping_id)
            if not mapping:
                return
            
            # Remove the mapping
            del self.mappings[mapping_id]
            
            self.update_app_status(f"Removed mapping from {mapping['source']} to {mapping['target']}")
        except Exception as e:
            self._handle_error(f"removing mapping {mapping_id}", e)
    
    def on_mappings_cleared(self):
        """Handle all mappings being cleared."""
        try:
            # Clear the mappings
            self.mappings = {}
            
            self.update_app_status("Cleared all mappings")
        except Exception as e:
            self._handle_error("clearing mappings", e)
    
    def save_mappings(self):
        """Save the current mappings to a file."""
        try:
            # Ask for a file to save to
            file_path = filedialog.asksaveasfilename(
                title="Save Mappings",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
                defaultextension=".json"
            )
            
            if not file_path:
                return
            
            # Convert mappings to a serializable format
            serializable_mappings = {}
            for mapping_id, mapping in self.mappings.items():
                serializable_mappings[mapping_id] = {
                    "source": mapping["source"],
                    "target": mapping["target"],
                    "transform": str(mapping.get("transform", "None"))
                }
            
            # Save the mappings
            with open(file_path, "w") as f:
                json.dump(serializable_mappings, f, indent=4)
            
            self.update_app_status(f"Saved mappings to {file_path}")
        except Exception as e:
            self._handle_error("saving mappings", e)
    
    def load_mappings(self):
        """Load mappings from a file."""
        try:
            # Ask for a file to load from
            file_path = filedialog.askopenfilename(
                title="Load Mappings",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
            )
            
            if not file_path:
                return
            
            # Load the mappings
            with open(file_path, "r") as f:
                serializable_mappings = json.load(f)
            
            # Convert to mappings
            self.mappings = {}
            for mapping_id, mapping in serializable_mappings.items():
                # Skip mappings with missing fields
                if "source" not in mapping or "target" not in mapping:
                    continue
                
                # Skip mappings with invalid source fields
                if not any(f["name"] == mapping["source"] for f in self.source_fields):
                    continue
                
                # Skip mappings with invalid target variables
                if not any(v["name"] == mapping["target"] for v in self.target_variables):
                    continue
                
                # Add the mapping
                self.mappings[mapping_id] = {
                    "source": mapping["source"],
                    "target": mapping["target"],
                    "transform": None  # We can't deserialize functions
                }
            
            # Update the view
            self.view.update_mappings(self.mappings)
            
            self.update_app_status(f"Loaded {len(self.mappings)} mappings from {file_path}")
        except Exception as e:
            self._handle_error("loading mappings", e)
    
    def create_variable_mapper(self) -> VariableMapper:
        """
        Create a VariableMapper from the current mappings.
        
        Returns:
            VariableMapper instance
        """
        try:
            # Create a new variable mapper
            mapper = VariableMapper()
            
            # Add mappings
            for mapping in self.mappings.values():
                # Create a field mapping
                field_mapping = FieldMapping(
                    field_name=mapping["source"],
                    variable_name=mapping["target"],
                    transform_function=mapping.get("transform"),
                    default_value=None
                )
                
                # Add the mapping
                mapper.add_mapping(field_mapping)
            
            return mapper
        except Exception as e:
            self._handle_error("creating variable mapper", e)
            return VariableMapper()  # Return an empty mapper on error
