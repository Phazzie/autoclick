"""
Base loop adapter implementation.

This module provides a base implementation of the loop adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.ui.adapters.interfaces.iloop_adapter import ILoopAdapter


class BaseLoopAdapter(ILoopAdapter):
    """Base implementation of loop adapter."""
    
    def get_loop_types(self) -> List[Dict[str, Any]]:
        """
        Get all available loop types.
        
        Returns:
            List of loop types with metadata
        """
        raise NotImplementedError("Subclasses must implement get_loop_types")
    
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
        raise NotImplementedError("Subclasses must implement get_loop_schema")
    
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
        raise NotImplementedError("Subclasses must implement create_loop")
    
    def validate_loop(self, loop_type: str, loop_data: Dict[str, Any]) -> List[str]:
        """
        Validate a loop.
        
        Args:
            loop_type: Loop type
            loop_data: Loop data
            
        Returns:
            List of validation errors, empty if valid
        """
        raise NotImplementedError("Subclasses must implement validate_loop")
