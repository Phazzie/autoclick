"""
Adapter for loop operations to provide the interface expected by the UI.
SOLID: Single responsibility - adapting loop operations.
KISS: Simple delegation to ActionFactory and ConditionFactory.
"""
from typing import Dict, List, Any, Optional

from src.core.actions.action_factory import ActionFactory
from src.core.conditions.condition_factory import ConditionFactory


class LoopAdapter:
    """Adapter for loop operations to provide the interface expected by the UI."""
    
    def __init__(self, action_factory: ActionFactory, condition_factory: ConditionFactory):
        """
        Initialize the adapter with ActionFactory and ConditionFactory instances.
        
        Args:
            action_factory: Factory for creating and managing actions
            condition_factory: Factory for creating and managing conditions
        """
        self.action_factory = action_factory
        self.condition_factory = condition_factory
    
    def get_loop_types(self) -> List[Dict[str, Any]]:
        """
        Get all available loop types.
        
        Returns:
            List of loop types with metadata
        """
        # Define metadata for each loop type
        return [
            {
                "type": "for_each",
                "name": "For Each",
                "description": "Iterate over a collection of items",
                "parameters": [
                    {"name": "collection_variable", "type": "string", "description": "Name of the variable containing the collection"},
                    {"name": "item_variable", "type": "string", "description": "Name of the variable to store the current item"}
                ]
            },
            {
                "type": "while_loop",
                "name": "While Loop",
                "description": "Execute actions while a condition is true",
                "parameters": [
                    {"name": "condition", "type": "condition", "description": "Condition to evaluate for each iteration"},
                    {"name": "max_iterations", "type": "integer", "description": "Maximum number of iterations (optional)"}
                ]
            }
        ]
    
    def create_loop(self, loop_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a loop from the given data.
        
        Args:
            loop_data: Dictionary containing loop configuration
            
        Returns:
            Dictionary containing the created loop data
        """
        loop_type = loop_data.get("type")
        
        if loop_type == "while_loop":
            # Create the condition
            condition_data = loop_data.get("condition", {})
            condition = self.condition_factory.create_condition(condition_data)
            
            # Create the loop action
            action = self.action_factory.create_action(
                action_type=loop_type,
                description=loop_data.get("description", ""),
                condition=condition,
                actions=loop_data.get("actions", []),
                max_iterations=loop_data.get("max_iterations")
            )
        else:
            # Create the loop action
            action = self.action_factory.create_action(
                action_type=loop_type,
                description=loop_data.get("description", ""),
                collection_variable=loop_data.get("collection_variable", ""),
                item_variable=loop_data.get("item_variable", ""),
                actions=loop_data.get("actions", [])
            )
        
        # Convert the action to a dictionary
        if hasattr(action, "to_dict"):
            return action.to_dict()
        
        # Fallback for actions without to_dict method
        return {
            "id": action.id,
            "description": action.description,
            "type": action.type
        }
    
    def get_loop_by_id(self, loop_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a loop by ID.
        
        Args:
            loop_id: ID of the loop to get
            
        Returns:
            Dictionary containing the loop data, or None if not found
        """
        # Get the action from the factory
        action = self.action_factory.get_action_by_id(loop_id)
        
        if not action:
            return None
        
        # Convert the action to a dictionary
        if hasattr(action, "to_dict"):
            return action.to_dict()
        
        # Fallback for actions without to_dict method
        return {
            "id": action.id,
            "description": action.description,
            "type": action.type
        }
    
    def update_loop(self, loop_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a loop.
        
        Args:
            loop_data: Dictionary containing updated loop configuration
            
        Returns:
            Dictionary containing the updated loop data
        """
        loop_type = loop_data.get("type")
        loop_id = loop_data.get("id")
        
        if loop_type == "while_loop":
            # Create the condition
            condition_data = loop_data.get("condition", {})
            condition = self.condition_factory.create_condition(condition_data)
            
            # Update the loop action
            action = self.action_factory.update_action(
                action_id=loop_id,
                action_type=loop_type,
                description=loop_data.get("description", ""),
                condition=condition,
                actions=loop_data.get("actions", []),
                max_iterations=loop_data.get("max_iterations")
            )
        else:
            # Update the loop action
            action = self.action_factory.update_action(
                action_id=loop_id,
                action_type=loop_type,
                description=loop_data.get("description", ""),
                collection_variable=loop_data.get("collection_variable", ""),
                item_variable=loop_data.get("item_variable", ""),
                actions=loop_data.get("actions", [])
            )
        
        # Convert the action to a dictionary
        if hasattr(action, "to_dict"):
            return action.to_dict()
        
        # Fallback for actions without to_dict method
        return {
            "id": action.id,
            "description": action.description,
            "type": action.type
        }
    
    def delete_loop(self, loop_id: str) -> bool:
        """
        Delete a loop.
        
        Args:
            loop_id: ID of the loop to delete
            
        Returns:
            True if the loop was deleted, False otherwise
        """
        return self.action_factory.delete_action(loop_id)
