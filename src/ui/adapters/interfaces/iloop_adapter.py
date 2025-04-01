"""
Loop adapter interface.

This module defines the interface for loop adapters.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class ILoopAdapter(ABC):
    """Interface for loop adapters."""
    
    @abstractmethod
    def get_loop_types(self) -> List[Dict[str, Any]]:
        """
        Get all available loop types.
        
        Returns:
            List of loop types with metadata
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def validate_loop(self, loop_type: str, loop_data: Dict[str, Any]) -> List[str]:
        """
        Validate a loop.
        
        Args:
            loop_type: Loop type
            loop_data: Loop data
            
        Returns:
            List of validation errors, empty if valid
        """
        pass
