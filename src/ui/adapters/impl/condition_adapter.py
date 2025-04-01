"""
Condition adapter implementation.

This module provides a concrete implementation of the condition adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.core.conditions.condition_factory_new import ConditionFactory
from src.core.conditions.condition_registry import ConditionRegistry
from src.core.conditions.standard_provider import StandardConditionProvider
from src.core.conditions.variable_provider import VariableConditionProvider
from src.ui.adapters.base.base_condition_adapter import BaseConditionAdapter


class ConditionAdapter(BaseConditionAdapter):
    """Concrete implementation of condition adapter."""
    
    def __init__(self, condition_factory: Optional[ConditionFactory] = None):
        """
        Initialize the adapter with a ConditionFactory instance.
        
        Args:
            condition_factory: Optional condition factory to use
        """
        if condition_factory is None:
            # Create a registry
            registry = ConditionRegistry()
            
            # Register providers
            registry.register_provider(StandardConditionProvider())
            registry.register_provider(VariableConditionProvider())
            
            # Create the factory
            condition_factory = ConditionFactory(registry)
        
        self._condition_factory = condition_factory
    
    def get_condition_types(self) -> List[Dict[str, Any]]:
        """
        Get all available condition types.
        
        Returns:
            List of condition types with metadata
        """
        # Get all condition types from the factory
        condition_types = self._condition_factory.get_condition_types()
        
        # Convert to UI format
        return [self._get_condition_type_metadata(condition_type) for condition_type in condition_types]
    
    def get_condition_schema(self, condition_type: str) -> Dict[str, Any]:
        """
        Get the schema for a condition type.
        
        Args:
            condition_type: Condition type
            
        Returns:
            Schema for the condition type
            
        Raises:
            ValueError: If the condition type is not supported
        """
        try:
            # Get the schema from the factory
            schema = self._condition_factory.get_condition_schema(condition_type)
            
            # Convert to UI format if needed
            return schema
        except Exception as e:
            raise ValueError(f"Error getting condition schema: {str(e)}")
    
    def create_condition(self, condition_type: str, condition_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a condition.
        
        Args:
            condition_type: Condition type
            condition_data: Condition data
            
        Returns:
            Created condition in the UI-expected format
            
        Raises:
            ValueError: If the condition data is invalid
        """
        # Validate the condition data
        errors = self.validate_condition(condition_type, condition_data)
        if errors:
            raise ValueError(f"Invalid condition data: {', '.join(errors)}")
        
        try:
            # Add the condition type to the data
            data_with_type = condition_data.copy()
            data_with_type["condition_type"] = condition_type
            
            # Create the condition
            condition = self._condition_factory.create_condition_from_definition(data_with_type)
            
            # Convert to UI format
            return self._convert_condition_to_ui_format(condition)
        except Exception as e:
            raise ValueError(f"Error creating condition: {str(e)}")
    
    def validate_condition(self, condition_type: str, condition_data: Dict[str, Any]) -> List[str]:
        """
        Validate a condition.
        
        Args:
            condition_type: Condition type
            condition_data: Condition data
            
        Returns:
            List of validation errors, empty if valid
        """
        try:
            # Add the condition type to the data
            data_with_type = condition_data.copy()
            data_with_type["condition_type"] = condition_type
            
            # Create the condition
            condition = self._condition_factory.create_condition_from_definition(data_with_type)
            
            # Validate the condition
            return condition.validate()
        except Exception as e:
            return [str(e)]
    
    def _get_condition_type_metadata(self, condition_type: str) -> Dict[str, Any]:
        """
        Get metadata for a condition type.
        
        Args:
            condition_type: Condition type
            
        Returns:
            Condition type metadata
        """
        # Define metadata for known condition types
        metadata = {
            "and": {
                "id": "and",
                "name": "AND",
                "description": "All conditions must be true",
                "icon": "and",
                "category": "logical"
            },
            "or": {
                "id": "or",
                "name": "OR",
                "description": "At least one condition must be true",
                "icon": "or",
                "category": "logical"
            },
            "not": {
                "id": "not",
                "name": "NOT",
                "description": "Condition must be false",
                "icon": "not",
                "category": "logical"
            },
            "true": {
                "id": "true",
                "name": "TRUE",
                "description": "Always true",
                "icon": "true",
                "category": "constant"
            },
            "false": {
                "id": "false",
                "name": "FALSE",
                "description": "Always false",
                "icon": "false",
                "category": "constant"
            },
            "variable_compare": {
                "id": "variable_compare",
                "name": "Compare Variable",
                "description": "Compare a variable with a value",
                "icon": "compare",
                "category": "variable"
            },
            "variable_exists": {
                "id": "variable_exists",
                "name": "Variable Exists",
                "description": "Check if a variable exists",
                "icon": "exists",
                "category": "variable"
            },
            "variable_empty": {
                "id": "variable_empty",
                "name": "Variable Empty",
                "description": "Check if a variable is empty",
                "icon": "empty",
                "category": "variable"
            },
            "variable_type": {
                "id": "variable_type",
                "name": "Variable Type",
                "description": "Check the type of a variable",
                "icon": "type",
                "category": "variable"
            }
        }
        
        # Return metadata for the condition type, or a default if not found
        return metadata.get(condition_type, {
            "id": condition_type,
            "name": condition_type.capitalize(),
            "description": f"{condition_type.capitalize()} condition",
            "icon": "condition",
            "category": "other"
        })
    
    def _convert_condition_to_ui_format(self, condition: Any) -> Dict[str, Any]:
        """
        Convert a condition to UI format.
        
        Args:
            condition: Condition object
            
        Returns:
            Condition in UI format
        """
        # Convert the condition to a dictionary
        condition_dict = condition.to_dict()
        
        # Add UI-specific fields
        condition_dict["id"] = condition_dict.get("condition_id", "")
        condition_dict["type"] = condition_dict.get("condition_type", "")
        
        # Remove redundant fields
        if "condition_id" in condition_dict:
            del condition_dict["condition_id"]
        if "condition_type" in condition_dict:
            del condition_dict["condition_type"]
        
        return condition_dict
