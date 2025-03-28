"""Model for workflow data"""
import uuid
from typing import Dict, List, Any, Optional


class WorkflowModel:
    """Model for workflow data"""
    
    def __init__(self) -> None:
        """Initialize the workflow model"""
        self.actions: List[Dict[str, Any]] = []
        self.name: str = "New Workflow"
        self.file_path: Optional[str] = None
        
    def add_action(self, action: Dict[str, Any]) -> str:
        """
        Add an action to the workflow
        
        Args:
            action: The action to add
            
        Returns:
            The ID of the added action
        """
        # Generate a unique ID for the action
        action_id = str(uuid.uuid4())
        
        # Add the ID to the action
        action_with_id = action.copy()
        action_with_id["id"] = action_id
        
        # Add the action to the list
        self.actions.append(action_with_id)
        
        return action_id
        
    def remove_action(self, action_id: str) -> bool:
        """
        Remove an action from the workflow
        
        Args:
            action_id: The ID of the action to remove
            
        Returns:
            True if the action was removed, False otherwise
        """
        for i, action in enumerate(self.actions):
            if action.get("id") == action_id:
                self.actions.pop(i)
                return True
        return False
    
    def get_actions(self) -> List[Dict[str, Any]]:
        """
        Get all actions in the workflow
        
        Returns:
            A copy of the actions list
        """
        return self.actions.copy()
    
    def get_action(self, action_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an action by ID
        
        Args:
            action_id: The ID of the action to get
            
        Returns:
            The action, or None if not found
        """
        for action in self.actions:
            if action.get("id") == action_id:
                return action.copy()
        return None
    
    def update_action(self, action_id: str, updated_action: Dict[str, Any]) -> bool:
        """
        Update an action in the workflow
        
        Args:
            action_id: The ID of the action to update
            updated_action: The updated action data
            
        Returns:
            True if the action was updated, False otherwise
        """
        for i, action in enumerate(self.actions):
            if action.get("id") == action_id:
                # Preserve the ID
                updated_with_id = updated_action.copy()
                updated_with_id["id"] = action_id
                
                # Update the action
                self.actions[i] = updated_with_id
                return True
        return False
    
    def reorder_actions(self, action_ids: List[str]) -> bool:
        """
        Reorder actions in the workflow
        
        Args:
            action_ids: List of action IDs in the new order
            
        Returns:
            True if the actions were reordered, False otherwise
        """
        if len(action_ids) != len(self.actions):
            return False
            
        # Check if all IDs are valid
        action_dict = {action.get("id"): action for action in self.actions}
        if not all(action_id in action_dict for action_id in action_ids):
            return False
            
        # Reorder actions
        self.actions = [action_dict[action_id] for action_id in action_ids]
        return True
    
    def clear(self) -> None:
        """Clear all actions from the workflow"""
        self.actions = []
        self.name = "New Workflow"
        self.file_path = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the workflow to a dictionary
        
        Returns:
            Dictionary representation of the workflow
        """
        return {
            "name": self.name,
            "actions": self.actions
        }
    
    def from_dict(self, data: Dict[str, Any]) -> bool:
        """
        Load the workflow from a dictionary
        
        Args:
            data: Dictionary containing workflow data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.name = data.get("name", "Imported Workflow")
            
            # Ensure each action has an ID
            actions = data.get("actions", [])
            for action in actions:
                if "id" not in action:
                    action["id"] = str(uuid.uuid4())
            
            self.actions = actions
            return True
        except Exception:
            return False
