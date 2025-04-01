"""
Condition adapter interface.

This module defines the interface for condition adapters.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IConditionAdapter(ABC):
    """Interface for condition adapters."""
    
    @abstractmethod
    def get_condition_types(self) -> List[Dict[str, Any]]:
        """
        Get all available condition types.
        
        Returns:
            List of condition types with metadata
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def validate_condition(self, condition_type: str, condition_data: Dict[str, Any]) -> List[str]:
        """
        Validate a condition.
        
        Args:
            condition_type: Condition type
            condition_data: Condition data
            
        Returns:
            List of validation errors, empty if valid
        """
        pass
