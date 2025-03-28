"""Data mapping interfaces"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class DataMapper(ABC):
    """
    Interface for data mappers
    
    A data mapper maps fields from a data source to variables
    in the execution context.
    """
    
    @abstractmethod
    def map_record(self, record: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map a record to the execution context
        
        Args:
            record: Record to map
            context: Execution context to map to
            
        Returns:
            Updated execution context
        """
        pass
        
    @abstractmethod
    def get_field_mappings(self) -> Dict[str, str]:
        """
        Get the field mappings
        
        Returns:
            Dictionary mapping field names to variable names
        """
        pass


class FieldMapping:
    """
    Mapping between a data field and a context variable
    
    This class defines how a field from a data source is mapped
    to a variable in the execution context.
    """
    
    def __init__(
        self,
        field_name: str,
        variable_name: str,
        transform_function: Optional[callable] = None,
        default_value: Any = None
    ):
        """
        Initialize the field mapping
        
        Args:
            field_name: Name of the field in the data source
            variable_name: Name of the variable in the execution context
            transform_function: Optional function to transform the field value
            default_value: Default value to use if the field is missing
        """
        self.field_name = field_name
        self.variable_name = variable_name
        self.transform_function = transform_function
        self.default_value = default_value
        
    def apply(self, record: Dict[str, Any]) -> Any:
        """
        Apply the mapping to a record
        
        Args:
            record: Record to map
            
        Returns:
            Mapped value
        """
        # Get the field value, or use the default if missing
        value = record.get(self.field_name, self.default_value)
        
        # Apply the transform function if provided
        if self.transform_function and value is not None:
            try:
                value = self.transform_function(value)
            except Exception as e:
                # If the transform fails, use the default value
                value = self.default_value
                
        return value
