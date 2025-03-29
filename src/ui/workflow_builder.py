"""Workflow builder for creating automation workflows"""
import json
import logging
import uuid
from typing import Any, Dict, List, Optional

from src.ui.interfaces import WorkflowBuilderInterface


class WorkflowBuilder(WorkflowBuilderInterface):
    """Builds and manages automation workflows"""
    
    def __init__(self) -> None:
        """Initialize the workflow builder"""
        self.logger = logging.getLogger(__name__)
        self.actions: List[Dict[str, Any]] = []
        self.action_ids: Dict[str, int] = {}  # Maps action IDs to indices
    
    def add_action(self, action: Dict[str, Any]) -> str:
        """
        Add an action to the workflow and return its ID
        
        Args:
            action: Action to add
            
        Returns:
            Unique ID for the action
        """
        self.logger.info("Adding action to workflow")
        
        # Generate a unique ID for the action
        action_id = str(uuid.uuid4())
        
        # Add the ID to the action
        action_with_id = action.copy()
        action_with_id["id"] = action_id
        
        # Add the action to the list
        self.actions.append(action_with_id)
        self.action_ids[action_id] = len(self.actions) - 1
        
        self.logger.debug(f"Added action with ID {action_id}")
        return action_id
    
    def remove_action(self, action_id: str) -> bool:
        """
        Remove an action from the workflow
        
        Args:
            action_id: ID of the action to remove
            
        Returns:
            True if the action was removed, False otherwise
        """
        self.logger.info(f"Removing action {action_id} from workflow")
        
        if action_id not in self.action_ids:
            self.logger.warning(f"Action {action_id} not found in workflow")
            return False
        
        # Get the index of the action
        index = self.action_ids[action_id]
        
        # Remove the action from the list
        self.actions.pop(index)
        
        # Update the action_ids dictionary
        del self.action_ids[action_id]
        
        # Update indices for actions after the removed one
        for aid, idx in list(self.action_ids.items()):
            if idx > index:
                self.action_ids[aid] = idx - 1
        
        self.logger.debug(f"Removed action {action_id}")
        return True
    
    def reorder_actions(self, action_ids: List[str]) -> bool:
        """
        Reorder actions in the workflow
        
        Args:
            action_ids: List of action IDs in the new order
            
        Returns:
            True if the actions were reordered, False otherwise
        """
        self.logger.info("Reordering workflow actions")
        
        # Check if all action IDs are valid
        if not all(aid in self.action_ids for aid in action_ids):
            self.logger.warning("Invalid action IDs in reorder request")
            return False
        
        # Check if all actions are included
        if len(action_ids) != len(self.actions):
            self.logger.warning("Not all actions included in reorder request")
            return False
        
        # Create a new action list in the specified order
        new_actions = []
        for aid in action_ids:
            index = self.action_ids[aid]
            new_actions.append(self.actions[index])
        
        # Update the action list
        self.actions = new_actions
        
        # Update the action_ids dictionary
        self.action_ids = {action["id"]: i for i, action in enumerate(self.actions)}
        
        self.logger.debug("Actions reordered successfully")
        return True
    
    def export_workflow(self) -> Dict[str, Any]:
        """
        Export the workflow as a configuration
        
        Returns:
            Dictionary containing the workflow configuration
        """
        self.logger.info("Exporting workflow configuration")
        
        # Create a configuration dictionary
        config = {
            "name": "Exported Workflow",
            "description": "Workflow exported from the workflow builder",
            "version": "1.0.0",
            "actions": self.actions,
        }
        
        self.logger.debug(f"Exported workflow with {len(self.actions)} actions")
        return config
    
    def import_workflow(self, config: Dict[str, Any]) -> bool:
        """
        Import a workflow from a configuration
        
        Args:
            config: Workflow configuration
            
        Returns:
            True if the workflow was imported, False otherwise
        """
        self.logger.info("Importing workflow configuration")
        
        try:
            # Clear existing actions
            self.actions = []
            self.action_ids = {}
            
            # Import actions from the configuration
            for action in config.get("actions", []):
                # Ensure each action has an ID
                if "id" not in action:
                    action["id"] = str(uuid.uuid4())
                
                self.actions.append(action)
                self.action_ids[action["id"]] = len(self.actions) - 1
            
            self.logger.debug(f"Imported workflow with {len(self.actions)} actions")
            return True
        except Exception as e:
            self.logger.error(f"Error importing workflow: {str(e)}")
            return False
    
    def save_workflow(self, file_path: str) -> bool:
        """
        Save the workflow to a file
        
        Args:
            file_path: Path to save the workflow
            
        Returns:
            True if the workflow was saved, False otherwise
        """
        self.logger.info(f"Saving workflow to {file_path}")
        
        try:
            # Export the workflow
            config = self.export_workflow()
            
            # Save to file
            with open(file_path, "w") as f:
                json.dump(config, f, indent=2)
            
            self.logger.debug(f"Workflow saved to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving workflow: {str(e)}")
            return False
    
    def load_workflow(self, file_path: str) -> bool:
        """
        Load a workflow from a file
        
        Args:
            file_path: Path to load the workflow from
            
        Returns:
            True if the workflow was loaded, False otherwise
        """
        self.logger.info(f"Loading workflow from {file_path}")
        
        try:
            # Load from file
            with open(file_path, "r") as f:
                config = json.load(f)
            
            # Import the workflow
            result = self.import_workflow(config)
            
            if result:
                self.logger.debug(f"Workflow loaded from {file_path}")
            else:
                self.logger.warning(f"Failed to import workflow from {file_path}")
            
            return result
        except Exception as e:
            self.logger.error(f"Error loading workflow: {str(e)}")
            return False
    
    def get_actions(self) -> List[Dict[str, Any]]:
        """
        Get all actions in the workflow
        
        Returns:
            List of actions
        """
        return self.actions.copy()
    
    def get_action(self, action_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an action by ID
        
        Args:
            action_id: ID of the action to get
            
        Returns:
            Action dictionary or None if not found
        """
        if action_id not in self.action_ids:
            return None
        
        index = self.action_ids[action_id]
        return self.actions[index].copy()
    
    def update_action(self, action_id: str, action: Dict[str, Any]) -> bool:
        """
        Update an action in the workflow
        
        Args:
            action_id: ID of the action to update
            action: New action data
            
        Returns:
            True if the action was updated, False otherwise
        """
        self.logger.info(f"Updating action {action_id}")
        
        if action_id not in self.action_ids:
            self.logger.warning(f"Action {action_id} not found in workflow")
            return False
        
        # Get the index of the action
        index = self.action_ids[action_id]
        
        # Update the action
        updated_action = action.copy()
        updated_action["id"] = action_id  # Ensure ID is preserved
        self.actions[index] = updated_action
        
        self.logger.debug(f"Updated action {action_id}")
        return True
