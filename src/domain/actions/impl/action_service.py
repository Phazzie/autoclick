"""
Action service implementation.

This module provides a concrete implementation of the action service interface.
"""
from typing import List, Dict, Any, Optional

from src.core.actions.action_factory import ActionFactory
from src.domain.actions.interfaces import IActionService
from src.domain.exceptions.domain_exceptions import DomainException


class ActionService(IActionService):
    """
    Implementation of the action service interface.
    
    This service provides action management functionality using the ActionFactory.
    """
    
    def __init__(self, action_factory: Optional[ActionFactory] = None):
        """
        Initialize the action service with an ActionFactory instance.
        
        Args:
            action_factory: Optional action factory to use
        """
        self._action_factory = action_factory or ActionFactory.get_instance()
        self._actions = {}  # In-memory store for actions
    
    def get_action_types(self) -> List[Dict[str, Any]]:
        """
        Get all available action types.
        
        Returns:
            List of action types with metadata
        """
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
        # Get the schema for the action type
        try:
            return self._get_action_schema(action_type)
        except Exception as e:
            raise DomainException(f"Error getting action schema for {action_type}: {str(e)}")
    
    def get_all_actions(self) -> List[Dict[str, Any]]:
        """
        Get all actions.
        
        Returns:
            List of actions in the UI-expected format
        """
        # Return all actions from the in-memory store
        return list(self._actions.values())
    
    def get_action(self, action_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an action by ID.
        
        Args:
            action_id: Action ID
            
        Returns:
            Action in the UI-expected format, or None if not found
        """
        # Return the action from the in-memory store
        return self._actions.get(action_id)
    
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
        # Validate the action data
        errors = self.validate_action(action_type, action_data)
        if errors:
            raise DomainException(f"Invalid action data: {', '.join(errors)}")
        
        try:
            # Create the action definition
            action_def = {
                "type": action_type,
                **action_data
            }
            
            # Create the action
            action = self._action_factory.create_from_dict(action_def)
            
            # Convert to UI format
            action_dict = action.to_dict()
            
            # Store the action
            self._actions[action_dict["id"]] = action_dict
            
            return action_dict
        except Exception as e:
            raise DomainException(f"Error creating action: {str(e)}")
    
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
        # Check if the action exists
        if action_id not in self._actions:
            return None
        
        # Get the action type
        action_type = self._actions[action_id].get("type")
        
        # Validate the action data
        errors = self.validate_action(action_type, action_data)
        if errors:
            raise DomainException(f"Invalid action data: {', '.join(errors)}")
        
        try:
            # Create the updated action definition
            action_def = {
                "id": action_id,
                "type": action_type,
                **action_data
            }
            
            # Create the action
            action = self._action_factory.create_from_dict(action_def)
            
            # Convert to UI format
            action_dict = action.to_dict()
            
            # Update the action
            self._actions[action_id] = action_dict
            
            return action_dict
        except Exception as e:
            raise DomainException(f"Error updating action: {str(e)}")
    
    def delete_action(self, action_id: str) -> bool:
        """
        Delete an action.
        
        Args:
            action_id: Action ID
            
        Returns:
            True if the action was deleted, False if not found
        """
        # Check if the action exists
        if action_id not in self._actions:
            return False
        
        # Delete the action
        del self._actions[action_id]
        
        return True
    
    def validate_action(self, action_type: str, action_data: Dict[str, Any]) -> List[str]:
        """
        Validate an action.
        
        Args:
            action_type: Action type
            action_data: Action data
            
        Returns:
            List of validation errors, empty if valid
        """
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
        elif action_type == "wait":
            if "duration" not in action_data:
                errors.append("Duration is required")
        
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
        # Check if the action exists
        if action_id not in self._actions:
            raise DomainException(f"Action not found: {action_id}")
        
        try:
            # Get the action definition
            action_def = self._actions[action_id]
            
            # Create the action
            action = self._action_factory.create_from_dict(action_def)
            
            # Execute the action
            result = action.execute(context)
            
            # Return the result
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            raise DomainException(f"Error executing action: {str(e)}")
    
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
            raise DomainException(f"Unsupported action type: {action_type}")
        
        return schemas[action_type]
