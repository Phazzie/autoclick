"""
Action adapter interface.

This module defines the interface for action adapters.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IActionAdapter(ABC):
    """Interface for action adapters."""
    
    @abstractmethod
    def get_action_types(self) -> List[Dict[str, Any]]:
        """
        Get all available action types.
        
        Returns:
            List of action types with metadata
        """
        pass
    
    @abstractmethod
    def get_action_schema(self, action_type: str) -> Dict[str, Any]:
        """
        Get the schema for an action type.
        
        Args:
            action_type: Action type
            
        Returns:
            Schema for the action type
            
        Raises:
            ValueError: If the action type is not supported
        """
        pass
    
    @abstractmethod
    def get_all_actions(self) -> List[Dict[str, Any]]:
        """
        Get all actions.
        
        Returns:
            List of actions in the UI-expected format
        """
        pass
    
    @abstractmethod
    def get_action(self, action_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an action by ID.
        
        Args:
            action_id: Action ID
            
        Returns:
            Action in the UI-expected format, or None if not found
        """
        pass
    
    @abstractmethod
    def create_action(self, action_type: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an action.
        
        Args:
            action_type: Action type
            action_data: Action data
            
        Returns:
            Created action in the UI-expected format
            
        Raises:
            ValueError: If the action data is invalid
        """
        pass
    
    @abstractmethod
    def update_action(self, action_id: str, action_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an action.
        
        Args:
            action_id: Action ID
            action_data: Action data
            
        Returns:
            Updated action in the UI-expected format, or None if not found
            
        Raises:
            ValueError: If the action data is invalid
        """
        pass
    
    @abstractmethod
    def delete_action(self, action_id: str) -> bool:
        """
        Delete an action.
        
        Args:
            action_id: Action ID
            
        Returns:
            True if the action was deleted, False if not found
        """
        pass
    
    @abstractmethod
    def validate_action(self, action_type: str, action_data: Dict[str, Any]) -> List[str]:
        """
        Validate an action.
        
        Args:
            action_type: Action type
            action_data: Action data
            
        Returns:
            List of validation errors, empty if valid
        """
        pass
    
    @abstractmethod
    def execute_action(self, action_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an action.
        
        Args:
            action_id: Action ID
            context: Execution context
            
        Returns:
            Execution result
            
        Raises:
            ValueError: If the action is not found or cannot be executed
        """
        pass
