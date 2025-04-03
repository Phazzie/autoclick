"""
Domain action interfaces.

This module defines the interfaces for the domain action components.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class IActionReader(Protocol):
    """Interface for reading action information."""
    
    def get_action_types(self) -> List[Dict[str, Any]]:
        """
        Get all available action types.
        
        Returns:
            List of action types with metadata
        """
        ...
    
    def get_all_actions(self) -> List[Dict[str, Any]]:
        """
        Get all actions.
        
        Returns:
            List of actions in the UI-expected format
        """
        ...
    
    def get_action(self, action_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an action by ID.
        
        Args:
            action_id: Action ID
            
        Returns:
            Action in the UI-expected format, or None if not found
        """
        ...
    
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
        ...


@runtime_checkable
class IActionWriter(Protocol):
    """Interface for writing action information."""
    
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
        ...
    
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
        ...
    
    def delete_action(self, action_id: str) -> bool:
        """
        Delete an action.
        
        Args:
            action_id: Action ID
            
        Returns:
            True if the action was deleted, False if not found
        """
        ...


@runtime_checkable
class IActionValidator(Protocol):
    """Interface for validating actions."""
    
    def validate_action(self, action_type: str, action_data: Dict[str, Any]) -> List[str]:
        """
        Validate an action.
        
        Args:
            action_type: Action type
            action_data: Action data
            
        Returns:
            List of validation errors, empty if valid
        """
        ...


@runtime_checkable
class IActionExecutor(Protocol):
    """Interface for executing actions."""
    
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
        ...


@runtime_checkable
class IActionService(IActionReader, IActionWriter, IActionValidator, IActionExecutor, Protocol):
    """Comprehensive interface for action services."""
    pass
