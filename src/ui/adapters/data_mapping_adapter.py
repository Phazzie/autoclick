"""
Adapter for data mapping to provide the interface expected by the UI.
SOLID: Single responsibility - adapting data mapping operations.
KISS: Simple delegation to data mapping components.
"""
from typing import Dict, List, Any, Optional, Tuple
import uuid
import json
import os

from src.core.data.mapping.mapper import FieldMapping
from src.core.data.mapping.variable_mapper import VariableMapper

class DataMappingAdapter:
    """Adapter for data mapping to provide the interface expected by the UI."""
    
    def __init__(self, data_source_adapter=None):
        """
        Initialize the adapter.
        
        Args:
            data_source_adapter: The data source adapter to use (optional)
        """
        self.data_source_adapter = data_source_adapter
        self.mappings: Dict[str, Dict[str, Any]] = {}
        self.mappers: Dict[str, VariableMapper] = {}
    
    def get_field_mappings(self, data_source_id: str) -> Dict[str, Dict[str, Any]]:
        """
        Get the field mappings for a data source.
        
        Args:
            data_source_id: ID of the data source
            
        Returns:
            Dictionary of field mappings
        """
        return self.mappings.get(data_source_id, {})
    
    def add_field_mapping(
        self,
        data_source_id: str,
        field_name: str,
        variable_name: str,
        transform_function: Optional[callable] = None,
        default_value: Any = None
    ) -> str:
        """
        Add a field mapping.
        
        Args:
            data_source_id: ID of the data source
            field_name: Name of the field in the data source
            variable_name: Name of the variable in the execution context
            transform_function: Optional function to transform the field value
            default_value: Default value to use if the field is missing
            
        Returns:
            ID of the new mapping
        """
        # Create the mapping ID
        mapping_id = str(uuid.uuid4())
        
        # Create the mapping
        mapping = {
            "source": field_name,
            "target": variable_name,
            "transform": transform_function,
            "default_value": default_value
        }
        
        # Add the mapping to the dictionary
        if data_source_id not in self.mappings:
            self.mappings[data_source_id] = {}
        
        self.mappings[data_source_id][mapping_id] = mapping
        
        # Invalidate the mapper for this data source
        if data_source_id in self.mappers:
            del self.mappers[data_source_id]
        
        return mapping_id
    
    def remove_field_mapping(self, data_source_id: str, mapping_id: str) -> bool:
        """
        Remove a field mapping.
        
        Args:
            data_source_id: ID of the data source
            mapping_id: ID of the mapping to remove
            
        Returns:
            True if the mapping was removed, False otherwise
        """
        # Check if the data source exists
        if data_source_id not in self.mappings:
            return False
        
        # Check if the mapping exists
        if mapping_id not in self.mappings[data_source_id]:
            return False
        
        # Remove the mapping
        del self.mappings[data_source_id][mapping_id]
        
        # Invalidate the mapper for this data source
        if data_source_id in self.mappers:
            del self.mappers[data_source_id]
        
        return True
    
    def clear_field_mappings(self, data_source_id: str) -> bool:
        """
        Clear all field mappings for a data source.
        
        Args:
            data_source_id: ID of the data source
            
        Returns:
            True if the mappings were cleared, False otherwise
        """
        # Check if the data source exists
        if data_source_id not in self.mappings:
            return False
        
        # Clear the mappings
        self.mappings[data_source_id] = {}
        
        # Invalidate the mapper for this data source
        if data_source_id in self.mappers:
            del self.mappers[data_source_id]
        
        return True
    
    def get_variable_mapper(self, data_source_id: str) -> VariableMapper:
        """
        Get a variable mapper for a data source.
        
        Args:
            data_source_id: ID of the data source
            
        Returns:
            VariableMapper instance
        """
        # Check if we already have a mapper for this data source
        if data_source_id in self.mappers:
            return self.mappers[data_source_id]
        
        # Create a new mapper
        mapper = VariableMapper()
        
        # Add mappings
        if data_source_id in self.mappings:
            for mapping in self.mappings[data_source_id].values():
                # Create a field mapping
                field_mapping = FieldMapping(
                    field_name=mapping["source"],
                    variable_name=mapping["target"],
                    transform_function=mapping.get("transform"),
                    default_value=mapping.get("default_value")
                )
                
                # Add the mapping
                mapper.add_mapping(field_mapping)
        
        # Store the mapper
        self.mappers[data_source_id] = mapper
        
        return mapper
    
    def save_mappings_to_file(self, data_source_id: str, file_path: str) -> bool:
        """
        Save mappings to a file.
        
        Args:
            data_source_id: ID of the data source
            file_path: Path to save the mappings to
            
        Returns:
            True if the mappings were saved, False otherwise
        """
        try:
            # Check if the data source exists
            if data_source_id not in self.mappings:
                return False
            
            # Convert mappings to a serializable format
            serializable_mappings = {}
            for mapping_id, mapping in self.mappings[data_source_id].items():
                serializable_mappings[mapping_id] = {
                    "source": mapping["source"],
                    "target": mapping["target"],
                    "transform": str(mapping.get("transform", "None")),
                    "default_value": mapping.get("default_value")
                }
            
            # Save the mappings
            with open(file_path, "w") as f:
                json.dump(serializable_mappings, f, indent=4)
            
            return True
        except Exception:
            return False
    
    def load_mappings_from_file(self, data_source_id: str, file_path: str) -> bool:
        """
        Load mappings from a file.
        
        Args:
            data_source_id: ID of the data source
            file_path: Path to load the mappings from
            
        Returns:
            True if the mappings were loaded, False otherwise
        """
        try:
            # Load the mappings
            with open(file_path, "r") as f:
                serializable_mappings = json.load(f)
            
            # Convert to mappings
            mappings = {}
            for mapping_id, mapping in serializable_mappings.items():
                # Skip mappings with missing fields
                if "source" not in mapping or "target" not in mapping:
                    continue
                
                # Add the mapping
                mappings[mapping_id] = {
                    "source": mapping["source"],
                    "target": mapping["target"],
                    "transform": None,  # We can't deserialize functions
                    "default_value": mapping.get("default_value")
                }
            
            # Store the mappings
            self.mappings[data_source_id] = mappings
            
            # Invalidate the mapper for this data source
            if data_source_id in self.mappers:
                del self.mappers[data_source_id]
            
            return True
        except Exception:
            return False
