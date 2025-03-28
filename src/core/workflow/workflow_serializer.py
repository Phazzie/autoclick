"""Workflow serialization utilities"""
import json
import os
from typing import Dict, Any, List, Optional, Union, Type
import logging
from datetime import datetime

from src.core.actions.base_action import BaseAction
from src.core.actions.action_factory import ActionFactory
from src.core.conditions.base_condition import BaseCondition
from src.core.conditions.condition_factory import ConditionFactory
from src.core.context.execution_context import ExecutionContext


class WorkflowSerializer:
    """Class for serializing and deserializing workflows"""

    # Current serialization format version
    CURRENT_VERSION = "1.0.0"

    def __init__(self) -> None:
        """Initialize the workflow serializer"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.action_factory = ActionFactory.get_instance()
        self.condition_factory = ConditionFactory.get_instance()

    def serialize_workflow(
        self,
        actions: List[BaseAction],
        context: Optional[ExecutionContext] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Serialize a workflow to a dictionary

        Args:
            actions: List of actions in the workflow
            context: Optional execution context
            metadata: Optional metadata about the workflow

        Returns:
            Dictionary representation of the workflow
        """
        self.logger.debug(f"Serializing workflow with {len(actions)} actions")

        # Create metadata if not provided
        if metadata is None:
            metadata = {}

        # Add default metadata
        metadata.update({
            "version": self.CURRENT_VERSION,
            "created_at": datetime.now().isoformat(),
            "action_count": len(actions)
        })

        # Create the workflow dictionary
        workflow_dict = {
            "metadata": metadata,
            "actions": [action.to_dict() for action in actions]
        }

        # Add context if provided
        if context:
            workflow_dict["context"] = context.to_dict(include_children=True)

        return workflow_dict

    def deserialize_workflow(
        self,
        workflow_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Deserialize a workflow from a dictionary

        Args:
            workflow_dict: Dictionary representation of the workflow

        Returns:
            Dictionary containing the deserialized workflow components
            {
                "actions": List of deserialized actions,
                "context": Deserialized execution context (if present),
                "metadata": Workflow metadata
            }

        Raises:
            ValueError: If the workflow dictionary is invalid
        """
        self.logger.debug("Deserializing workflow")

        # Validate the workflow dictionary
        if not isinstance(workflow_dict, dict):
            raise ValueError("Workflow must be a dictionary")

        if "actions" not in workflow_dict:
            raise ValueError("Workflow must contain an 'actions' key")

        if not isinstance(workflow_dict["actions"], list):
            raise ValueError("Workflow actions must be a list")

        # Get metadata
        metadata = workflow_dict.get("metadata", {})
        version = metadata.get("version", "unknown")

        self.logger.debug(f"Deserializing workflow version {version}")

        # Deserialize actions
        actions_data = workflow_dict["actions"]
        actions = []

        for action_data in actions_data:
            action_type = action_data.get("type")
            if not action_type:
                self.logger.warning(f"Skipping action without type: {action_data}")
                continue

            try:
                action = self.action_factory.create_action(action_data)
                actions.append(action)
            except Exception as e:
                self.logger.error(f"Error deserializing action of type {action_type}: {str(e)}")
                raise ValueError(f"Failed to deserialize action of type {action_type}: {str(e)}")

        # Deserialize context if present
        context = None
        if "context" in workflow_dict:
            try:
                context = ExecutionContext.from_dict(workflow_dict["context"])
            except Exception as e:
                self.logger.error(f"Error deserializing context: {str(e)}")
                raise ValueError(f"Failed to deserialize context: {str(e)}")

        return {
            "actions": actions,
            "context": context,
            "metadata": metadata
        }

    def save_workflow_to_file(
        self,
        file_path: str,
        actions: List[BaseAction],
        context: Optional[ExecutionContext] = None,
        metadata: Optional[Dict[str, Any]] = None,
        pretty_print: bool = True
    ) -> None:
        """
        Save a workflow to a file

        Args:
            file_path: Path to save the workflow to
            actions: List of actions in the workflow
            context: Optional execution context
            metadata: Optional metadata about the workflow
            pretty_print: Whether to format the JSON with indentation

        Raises:
            IOError: If the file cannot be written
        """
        self.logger.info(f"Saving workflow to {file_path}")

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

        # Serialize the workflow
        workflow_dict = self.serialize_workflow(actions, context, metadata)

        # Write to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if pretty_print:
                    json.dump(workflow_dict, f, indent=2)
                else:
                    json.dump(workflow_dict, f)
            self.logger.debug(f"Workflow saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving workflow to {file_path}: {str(e)}")
            raise IOError(f"Failed to save workflow to {file_path}: {str(e)}")

    def load_workflow_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load a workflow from a file

        Args:
            file_path: Path to load the workflow from

        Returns:
            Dictionary containing the deserialized workflow components
            {
                "actions": List of deserialized actions,
                "context": Deserialized execution context (if present),
                "metadata": Workflow metadata
            }

        Raises:
            IOError: If the file cannot be read
            ValueError: If the workflow is invalid
        """
        self.logger.info(f"Loading workflow from {file_path}")

        # Read from file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                workflow_dict = json.load(f)
            self.logger.debug(f"Workflow loaded from {file_path}")
        except Exception as e:
            self.logger.error(f"Error loading workflow from {file_path}: {str(e)}")
            raise IOError(f"Failed to load workflow from {file_path}: {str(e)}")

        # Deserialize the workflow
        return self.deserialize_workflow(workflow_dict)
