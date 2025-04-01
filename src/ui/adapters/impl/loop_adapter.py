"""
Loop adapter implementation.

This module provides a concrete implementation of the loop adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.core.loops.loop_factory import LoopFactory
from src.ui.adapters.base.base_loop_adapter import BaseLoopAdapter


class LoopAdapter(BaseLoopAdapter):
    """Concrete implementation of loop adapter."""
    
    def __init__(self, loop_factory: Optional[LoopFactory] = None):
        """
        Initialize the adapter with a LoopFactory instance.
        
        Args:
            loop_factory: Optional loop factory to use
        """
        self._loop_factory = loop_factory or LoopFactory()
    
    def get_loop_types(self) -> List[Dict[str, Any]]:
        """
        Get all available loop types.
        
        Returns:
            List of loop types with metadata
        """
        # Get all loop types from the factory
        loop_types = self._loop_factory.get_loop_types()
        
        # Convert to UI format
        return [self._get_loop_type_metadata(loop_type) for loop_type in loop_types]
    
    def get_loop_schema(self, loop_type: str) -> Dict[str, Any]:
        """
        Get the schema for a loop type.
        
        Args:
            loop_type: Loop type
            
        Returns:
            Schema for the loop type
            
        Raises:
            ValueError: If the loop type is not supported
        """
        try:
            # Get the schema from the factory
            schema = self._loop_factory.get_loop_schema(loop_type)
            
            # Convert to UI format if needed
            return schema
        except Exception as e:
            raise ValueError(f"Error getting loop schema: {str(e)}")
    
    def create_loop(self, loop_type: str, loop_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a loop.
        
        Args:
            loop_type: Loop type
            loop_data: Loop data
            
        Returns:
            Created loop in the UI-expected format
            
        Raises:
            ValueError: If the loop data is invalid
        """
        # Validate the loop data
        errors = self.validate_loop(loop_type, loop_data)
        if errors:
            raise ValueError(f"Invalid loop data: {', '.join(errors)}")
        
        try:
            # Create the loop
            loop = self._loop_factory.create_loop(loop_type, loop_data)
            
            # Convert to UI format
            return self._convert_loop_to_ui_format(loop)
        except Exception as e:
            raise ValueError(f"Error creating loop: {str(e)}")
    
    def validate_loop(self, loop_type: str, loop_data: Dict[str, Any]) -> List[str]:
        """
        Validate a loop.
        
        Args:
            loop_type: Loop type
            loop_data: Loop data
            
        Returns:
            List of validation errors, empty if valid
        """
        try:
            # Create the loop
            loop = self._loop_factory.create_loop(loop_type, loop_data)
            
            # Validate the loop
            return loop.validate()
        except Exception as e:
            return [str(e)]
    
    def _get_loop_type_metadata(self, loop_type: str) -> Dict[str, Any]:
        """
        Get metadata for a loop type.
        
        Args:
            loop_type: Loop type
            
        Returns:
            Loop type metadata
        """
        # Define metadata for known loop types
        metadata = {
            "count": {
                "id": "count",
                "name": "Count Loop",
                "description": "Loop a fixed number of times",
                "icon": "count",
                "category": "basic"
            },
            "while": {
                "id": "while",
                "name": "While Loop",
                "description": "Loop while a condition is true",
                "icon": "while",
                "category": "conditional"
            },
            "for_each": {
                "id": "for_each",
                "name": "For Each Loop",
                "description": "Loop over items in a collection",
                "icon": "for-each",
                "category": "collection"
            },
            "until": {
                "id": "until",
                "name": "Until Loop",
                "description": "Loop until a condition is true",
                "icon": "until",
                "category": "conditional"
            }
        }
        
        # Return metadata for the loop type, or a default if not found
        return metadata.get(loop_type, {
            "id": loop_type,
            "name": loop_type.capitalize(),
            "description": f"{loop_type.capitalize()} loop",
            "icon": "loop",
            "category": "other"
        })
    
    def _convert_loop_to_ui_format(self, loop: Any) -> Dict[str, Any]:
        """
        Convert a loop to UI format.
        
        Args:
            loop: Loop object
            
        Returns:
            Loop in UI format
        """
        return {
            "id": loop.loop_id,
            "type": loop.loop_type,
            "name": loop.name,
            "description": loop.description,
            "config": loop.config
        }
