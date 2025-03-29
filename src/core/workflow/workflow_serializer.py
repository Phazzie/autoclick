"""Workflow serialization functionality for saving and loading workflows"""
import os
import json
import logging
from typing import Dict, Any, List, Optional

from src.core.actions.base_action import BaseAction
from src.core.actions.action_factory import ActionFactory


class WorkflowSerializer:
    """
    Handles serialization and deserialization of workflows
    
    This class provides methods to save workflows to files and load them back,
    enabling workflow sharing, storage, and reuse.
    """
    
    def __init__(self):
        """Initialize the workflow serializer"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.schema_version = "1.0"
    
    def save_workflow_to_file(
        self,
        file_path: str,
        actions: List[BaseAction],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save a workflow to a file
        
        Args:
            file_path: Path to save the workflow file
            actions: List of actions in the workflow
            metadata: Optional metadata for the workflow
            
        Returns:
            Path to the saved file
            
        Raises:
            IOError: If the file cannot be saved
        """
        # Create the workflow data structure
        workflow_data = {
            "schema_version": self.schema_version,
            "metadata": metadata or {
                "name": "Unnamed Workflow",
                "description": "No description provided",
                "version": "1.0.0"
            },
            "actions": [action.to_dict() for action in actions]
        }
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Save the workflow to a file
        try:
            with open(file_path, 'w') as f:
                json.dump(workflow_data, f, indent=2)
                
            self.logger.info(f"Saved workflow to {file_path}")
            return file_path
        except Exception as e:
            self.logger.error(f"Error saving workflow to {file_path}: {str(e)}")
            raise IOError(f"Failed to save workflow: {str(e)}")
    
    def load_workflow_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load a workflow from a file
        
        Args:
            file_path: Path to the workflow file
            
        Returns:
            Dictionary containing the workflow data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is invalid
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Workflow file not found: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                workflow_data = json.load(f)
                
            # Validate the workflow data
            if "schema_version" not in workflow_data:
                raise ValueError("Invalid workflow file: missing schema_version")
                
            if "actions" not in workflow_data:
                raise ValueError("Invalid workflow file: missing actions")
                
            self.logger.info(f"Loaded workflow from {file_path}")
            return workflow_data
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing workflow file {file_path}: {str(e)}")
            raise ValueError(f"Invalid workflow file format: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error loading workflow from {file_path}: {str(e)}")
            raise
    
    def create_actions_from_workflow(self, workflow_data: Dict[str, Any]) -> List[BaseAction]:
        """
        Create action instances from workflow data
        
        Args:
            workflow_data: Workflow data loaded from a file
            
        Returns:
            List of instantiated actions
            
        Raises:
            ValueError: If the workflow data is invalid
        """
        if "actions" not in workflow_data:
            raise ValueError("Invalid workflow data: missing actions")
        
        actions = []
        action_factory = ActionFactory.get_instance()
        
        for action_data in workflow_data["actions"]:
            try:
                action = action_factory.create_from_dict(action_data)
                actions.append(action)
            except Exception as e:
                self.logger.error(f"Error creating action: {str(e)}")
                raise ValueError(f"Failed to create action: {str(e)}")
        
        return actions
    
    def save_workflow_to_string(
        self,
        actions: List[BaseAction],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save a workflow to a JSON string
        
        Args:
            actions: List of actions in the workflow
            metadata: Optional metadata for the workflow
            
        Returns:
            JSON string representation of the workflow
        """
        # Create the workflow data structure
        workflow_data = {
            "schema_version": self.schema_version,
            "metadata": metadata or {
                "name": "Unnamed Workflow",
                "description": "No description provided",
                "version": "1.0.0"
            },
            "actions": [action.to_dict() for action in actions]
        }
        
        # Convert to JSON string
        return json.dumps(workflow_data, indent=2)
    
    def load_workflow_from_string(self, json_string: str) -> Dict[str, Any]:
        """
        Load a workflow from a JSON string
        
        Args:
            json_string: JSON string representation of the workflow
            
        Returns:
            Dictionary containing the workflow data
            
        Raises:
            ValueError: If the string is invalid
        """
        try:
            workflow_data = json.loads(json_string)
            
            # Validate the workflow data
            if "schema_version" not in workflow_data:
                raise ValueError("Invalid workflow data: missing schema_version")
                
            if "actions" not in workflow_data:
                raise ValueError("Invalid workflow data: missing actions")
                
            return workflow_data
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing workflow JSON: {str(e)}")
            raise ValueError(f"Invalid workflow JSON format: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error loading workflow from string: {str(e)}")
            raise
