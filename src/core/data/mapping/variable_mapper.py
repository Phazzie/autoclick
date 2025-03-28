"""Variable mapper implementation"""
from typing import Dict, Any, List, Optional
import logging

from src.core.data.mapping.mapper import DataMapper, FieldMapping


class VariableMapper(DataMapper):
    """
    Maps data fields to variables in the execution context
    
    This mapper applies a set of field mappings to map data fields
    to variables in the execution context.
    """
    
    def __init__(self, mappings: List[FieldMapping] = None):
        """
        Initialize the variable mapper
        
        Args:
            mappings: List of field mappings
        """
        self.mappings = mappings or []
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def add_mapping(self, mapping: FieldMapping) -> None:
        """
        Add a field mapping
        
        Args:
            mapping: Field mapping to add
        """
        self.mappings.append(mapping)
        
    def add_simple_mapping(
        self,
        field_name: str,
        variable_name: Optional[str] = None,
        transform_function: Optional[callable] = None,
        default_value: Any = None
    ) -> None:
        """
        Add a simple field mapping
        
        Args:
            field_name: Name of the field in the data source
            variable_name: Name of the variable in the execution context
                           (defaults to the field name if not provided)
            transform_function: Optional function to transform the field value
            default_value: Default value to use if the field is missing
        """
        variable_name = variable_name or field_name
        mapping = FieldMapping(field_name, variable_name, transform_function, default_value)
        self.add_mapping(mapping)
        
    def map_record(self, record: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map a record to the execution context
        
        Args:
            record: Record to map
            context: Execution context to map to
            
        Returns:
            Updated execution context
        """
        # Create a copy of the context to avoid modifying the original
        updated_context = context.copy()
        
        # Apply each mapping
        for mapping in self.mappings:
            value = mapping.apply(record)
            
            # Update the context
            if "variables" in updated_context and hasattr(updated_context["variables"], "set"):
                # Use the variables object if available
                updated_context["variables"].set(mapping.variable_name, value)
            else:
                # Otherwise, store directly in the context
                updated_context[mapping.variable_name] = value
                
        return updated_context
        
    def get_field_mappings(self) -> Dict[str, str]:
        """
        Get the field mappings
        
        Returns:
            Dictionary mapping field names to variable names
        """
        return {mapping.field_name: mapping.variable_name for mapping in self.mappings}
