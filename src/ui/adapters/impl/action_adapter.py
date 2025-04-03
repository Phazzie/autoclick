"""
Action adapter implementation.

This module provides a concrete implementation of the action adapter interface.
It supports both clean architecture (through IActionService) and legacy mode
(through ActionFactory).
"""
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.core.actions.action_factory import ActionFactory
from src.domain.actions.interfaces import IActionService
from src.ui.adapters.base.base_action_adapter import BaseActionAdapter


class ActionAdapter(BaseActionAdapter):
    """
    Concrete implementation of action adapter.
    
    This adapter uses the clean architecture components through an action service
    or falls back to the legacy action factory.
    """
    
    def __init__(self, action_service: Optional[IActionService] = None, action_factory: Optional[ActionFactory] = None):
        """
        Initialize the adapter with an action service or factory.
        
        Args:
            action_service: Optional action service to use (clean architecture)
            action_factory: Optional action factory to use (legacy)
        """
        if action_service:
            self._service = action_service
            self._use_service = True
        else:
            self._use_service = False
            self._action_factory = action_factory or ActionFactory.get_instance()
    
    def get_action_types(self) -> List[Dict[str, Any]]:
        """
        Get all available action types.
        
        Returns:
            List of action types with metadata
        """
        if self._use_service:
            try:
                return self._service.get_action_types()
            except Exception as e:
                raise ValueError(f"Error getting action types: {str(e)}")
        else:
            # Legacy implementation
            # Get all action types from the factory
            action_types = self._action_factory.get_action_types()
            
            # Convert to UI format
            return [self._get_action_type_metadata(action_type) for action_type in action_types]
    
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
        if self._use_service:
            try:
                return self._service.get_action_schema(action_type)
            except Exception as e:
                raise ValueError(f"Error getting action schema for {action_type}: {str(e)}")
        else:
            # Legacy implementation
            # Get the schema from the factory
            try:
                # In the legacy implementation, we don't have a direct way to get the schema
                # So we'll return a basic schema based on the action type
                return self._get_action_schema(action_type)
            except Exception as e:
                raise ValueError(f"Error getting action schema for {action_type}: {str(e)}")
    
    def get_all_actions(self) -> List[Dict[str, Any]]:
        """
        Get all actions.
        
        Returns:
            List of actions in the UI-expected format
        """
        if self._use_service:
            try:
                return self._service.get_all_actions()
            except Exception as e:
                raise ValueError(f"Error getting all actions: {str(e)}")
        else:
            # Legacy implementation
            # Get all actions from the factory
            try:
                # In the legacy implementation, we don't have a direct way to get all actions
                # So we'll return an empty list for now
                return []
            except Exception as e:
                raise ValueError(f"Error getting all actions: {str(e)}")
    
    def get_action(self, action_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an action by ID.
        
        Args:
            action_id: Action ID
            
        Returns:
            Action in the UI-expected format, or None if not found
        """
        if self._use_service:
            try:
                return self._service.get_action(action_id)
            except Exception as e:
                raise ValueError(f"Error getting action {action_id}: {str(e)}")
        else:
            # Legacy implementation
            # Get the action from the factory
            try:
                # In the legacy implementation, we don't have a direct way to get an action by ID
                # So we'll return None for now
                return None
            except Exception as e:
                raise ValueError(f"Error getting action {action_id}: {str(e)}")
    
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
        if self._use_service:
            try:
                # Validate the action data first
                errors = self.validate_action(action_type, action_data)
                if errors:
                    raise ValueError(f"Invalid action data: {', '.join(errors)}")
                
                # Create the action
                return self._service.create_action(action_type, action_data)
            except Exception as e:
                raise ValueError(f"Error creating action: {str(e)}")
        else:
            # Legacy implementation
            # Validate the action data
            errors = self.validate_action(action_type, action_data)
            if errors:
                raise ValueError(f"Invalid action data: {', '.join(errors)}")
            
            try:
                # Create the action definition
                action_def = {
                    "type": action_type,
                    **action_data
                }
                
                # Create the action
                action = self._action_factory.create_from_dict(action_def)
                
                # Convert to UI format
                return action.to_dict()
            except Exception as e:
                raise ValueError(f"Error creating action: {str(e)}")
    
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
        if self._use_service:
            try:
                return self._service.update_action(action_id, action_data)
            except Exception as e:
                raise ValueError(f"Error updating action {action_id}: {str(e)}")
        else:
            # Legacy implementation
            # In the legacy implementation, we don't have a direct way to update an action
            # So we'll raise an error for now
            raise ValueError("Action update not supported in legacy mode")
    
    def delete_action(self, action_id: str) -> bool:
        """
        Delete an action.
        
        Args:
            action_id: Action ID
            
        Returns:
            True if the action was deleted, False if not found
        """
        if self._use_service:
            try:
                return self._service.delete_action(action_id)
            except Exception as e:
                raise ValueError(f"Error deleting action {action_id}: {str(e)}")
        else:
            # Legacy implementation
            try:
                # In the legacy implementation, we don't have a direct way to delete an action
                # So we'll return False for now
                return False
            except Exception as e:
                raise ValueError(f"Error deleting action: {str(e)}")
    
    def validate_action(self, action_type: str, action_data: Dict[str, Any]) -> List[str]:
        """
        Validate an action.
        
        Args:
            action_type: Action type
            action_data: Action data
            
        Returns:
            List of validation errors, empty if valid
        """
        if self._use_service:
            try:
                return self._service.validate_action(action_type, action_data)
            except Exception as e:
                # Return the error as a validation error
                return [f"Error validating action: {str(e)}"]
        else:
            # Legacy implementation
            # Basic validation based on action type
            errors = []
            
            # Validate required fields based on action type
            if action_type == "click":
                if "x" not in action_data:
                    errors.append("X coordinate is required")
                if "y" not in action_data:
                    errors.append("Y coordinate is required")
            elif action_type == "keyboard":
                if "text" not in action_data:
                    errors.append("Text is required")
            
            return errors
    
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
        if self._use_service:
            try:
                return self._service.execute_action(action_id, context)
            except Exception as e:
                raise ValueError(f"Error executing action {action_id}: {str(e)}")
        else:
            # Legacy implementation
            try:
                # In the legacy implementation, we don't have a direct way to execute an action by ID
                # So we'll raise an error for now
                raise ValueError("Action execution by ID not supported in legacy mode")
            except Exception as e:
                raise ValueError(f"Error executing action: {str(e)}")
    
    def _get_action_type_metadata(self, action_type: str) -> Dict[str, Any]:
        """
        Get metadata for an action type.
        
        Args:
            action_type: Action type
            
        Returns:
            Action type metadata
        """
        # Define metadata for known action types
        metadata = {
            "click": {
                "id": "click",
                "name": "Click",
                "description": "Click at a specific position",
                "icon": "mouse-pointer",
                "category": "mouse"
            },
            "keyboard": {
                "id": "keyboard",
                "name": "Keyboard",
                "description": "Type text or press keys",
                "icon": "keyboard",
                "category": "input"
            },
            "wait": {
                "id": "wait",
                "name": "Wait",
                "description": "Wait for a specified time",
                "icon": "clock",
                "category": "utility"
            },
            "screenshot": {
                "id": "screenshot",
                "name": "Screenshot",
                "description": "Take a screenshot",
                "icon": "camera",
                "category": "utility"
            }
        }
        
        # Return metadata for the action type, or a default if not found
        return metadata.get(action_type, {
            "id": action_type,
            "name": action_type.capitalize(),
            "description": f"{action_type.capitalize()} action",
            "icon": "action",
            "category": "other"
        })
    
    def _get_action_schema(self, action_type: str) -> Dict[str, Any]:
        """
        Get schema for an action type.
        
        Args:
            action_type: Action type
            
        Returns:
            Schema for the action type
            
        Raises:
            ValueError: If the action type is not supported
        """
        # Define schemas for known action types
        schemas = {
            "click": {
                "type": "object",
                "required": ["x", "y"],
                "properties": {
                    "x": {"type": "integer", "title": "X Coordinate"},
                    "y": {"type": "integer", "title": "Y Coordinate"},
                    "button": {"type": "string", "title": "Mouse Button", "enum": ["left", "right", "middle"], "default": "left"},
                    "double": {"type": "boolean", "title": "Double Click", "default": False}
                }
            },
            "keyboard": {
                "type": "object",
                "required": ["text"],
                "properties": {
                    "text": {"type": "string", "title": "Text to Type"},
                    "delay": {"type": "integer", "title": "Delay between keystrokes (ms)", "default": 0}
                }
            },
            "wait": {
                "type": "object",
                "required": ["duration"],
                "properties": {
                    "duration": {"type": "integer", "title": "Duration (ms)", "default": 1000}
                }
            },
            "screenshot": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "title": "Filename"},
                    "region": {
                        "type": "object",
                        "title": "Region",
                        "properties": {
                            "x": {"type": "integer", "title": "X"},
                            "y": {"type": "integer", "title": "Y"},
                            "width": {"type": "integer", "title": "Width"},
                            "height": {"type": "integer", "title": "Height"}
                        }
                    }
                }
            }
        }
        
        # Return schema for the action type, or raise an error if not found
        if action_type not in schemas:
            raise ValueError(f"Unsupported action type: {action_type}")
        
        return schemas[action_type]
