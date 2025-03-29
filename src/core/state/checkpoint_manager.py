"""Checkpoint management functionality for saving and restoring workflow execution points"""
import os
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from src.core.context.execution_context import ExecutionContext
from src.core.state.state_persistence import StatePersistence
from src.core.state.checkpoint_interface import CheckpointInterface
from src.core.state.checkpoint import Checkpoint
from src.core.state.checkpoint_manager_interface import CheckpointManagerInterface


class CheckpointManager(CheckpointManagerInterface):
    """
    Manages checkpoints for workflow execution

    This class provides methods to create checkpoints during workflow execution
    and restore from them later, enabling advanced pause/resume functionality.
    """

    def __init__(self, checkpoint_dir: str = "checkpoints"):
        """
        Initialize the checkpoint manager

        Args:
            checkpoint_dir: Directory to store checkpoint files
        """
        self.checkpoint_dir = checkpoint_dir
        self.logger = logging.getLogger(self.__class__.__name__)

        # Create the checkpoint directory if it doesn't exist
        os.makedirs(self.checkpoint_dir, exist_ok=True)

        # Create a state persistence instance for handling context serialization
        self.state_persistence = StatePersistence(checkpoint_dir)

    def create_checkpoint(
        self,
        workflow_id: str,
        context: ExecutionContext,
        data: Dict[str, Any],
        name: Optional[str] = None
    ) -> str:
        """
        Create a checkpoint

        Args:
            workflow_id: ID of the workflow
            context: Execution context to save
            data: Additional data to save with the checkpoint (e.g., action index)
            name: Optional name for the checkpoint

        Returns:
            ID of the created checkpoint
        """
        # Generate a unique ID for the checkpoint
        checkpoint_id = str(uuid.uuid4())

        # Create a timestamp
        timestamp = datetime.now().isoformat()

        # Create the checkpoint data
        checkpoint_data = {
            "id": checkpoint_id,
            "workflow_id": workflow_id,
            "timestamp": timestamp,
            "name": name,
            "data": data
        }

        # Create the filename
        filename = f"{checkpoint_id}.checkpoint"
        file_path = os.path.join(self.checkpoint_dir, filename)

        try:
            # Save the checkpoint data
            with open(file_path, 'w') as f:
                json.dump(checkpoint_data, f, indent=2)

            # Save the context state
            context_file = os.path.join(self.checkpoint_dir, f"{checkpoint_id}.context")
            self._save_context(context_file, context)

            self.logger.info(f"Created checkpoint {checkpoint_id}")
            return checkpoint_id
        except Exception as e:
            self.logger.error(f"Error creating checkpoint: {str(e)}")
            raise

    def restore_from_checkpoint(self, checkpoint_id: str) -> Tuple[ExecutionContext, Dict[str, Any]]:
        """
        Restore from a checkpoint

        Args:
            checkpoint_id: ID of the checkpoint

        Returns:
            Tuple of (restored context, checkpoint data)

        Raises:
            FileNotFoundError: If the checkpoint doesn't exist
            ValueError: If the checkpoint is invalid
        """
        # Get the checkpoint file path
        checkpoint_file = self.get_checkpoint_file(checkpoint_id)
        if not os.path.exists(checkpoint_file):
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")

        # Get the context file path
        context_file = os.path.join(self.checkpoint_dir, f"{checkpoint_id}.context")
        if not os.path.exists(context_file):
            raise FileNotFoundError(f"Context file not found for checkpoint: {checkpoint_id}")

        try:
            # Load the checkpoint data
            with open(checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)

            # Load the context
            context = self._load_context(context_file)

            self.logger.info(f"Restored from checkpoint {checkpoint_id}")
            return context, checkpoint_data["data"]
        except Exception as e:
            self.logger.error(f"Error restoring from checkpoint: {str(e)}")
            raise ValueError(f"Invalid checkpoint: {str(e)}")

    def get_checkpoints_for_workflow(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Get all checkpoints for a workflow

        Args:
            workflow_id: ID of the workflow

        Returns:
            List of checkpoint data dictionaries
        """
        checkpoints = []

        # Iterate through all checkpoint files
        for filename in os.listdir(self.checkpoint_dir):
            if not filename.endswith(".checkpoint"):
                continue

            file_path = os.path.join(self.checkpoint_dir, filename)
            try:
                # Load the checkpoint data
                with open(file_path, 'r') as f:
                    checkpoint_data = json.load(f)

                # Check if it's for the specified workflow
                if checkpoint_data["workflow_id"] == workflow_id:
                    checkpoints.append(checkpoint_data)
            except Exception as e:
                self.logger.error(f"Error loading checkpoint {filename}: {str(e)}")

        # Sort by timestamp (newest first)
        checkpoints.sort(key=lambda x: x["timestamp"], reverse=True)

        return checkpoints

    def get_checkpoint_by_name(self, workflow_id: str, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a checkpoint by name

        Args:
            workflow_id: ID of the workflow
            name: Name of the checkpoint

        Returns:
            Checkpoint data dictionary, or None if not found
        """
        checkpoints = self.get_checkpoints_for_workflow(workflow_id)

        # Find the checkpoint with the specified name
        for checkpoint in checkpoints:
            if checkpoint["name"] == name:
                return checkpoint

        return None

    def get_checkpoint(self, checkpoint_id: str) -> Optional[CheckpointInterface]:
        """
        Get a checkpoint by ID

        Args:
            checkpoint_id: ID of the checkpoint

        Returns:
            Checkpoint, or None if not found
        """
        # Get the checkpoint file path
        checkpoint_file = self.get_checkpoint_file(checkpoint_id)
        if not os.path.exists(checkpoint_file):
            return None

        # Get the context file path
        context_file = os.path.join(self.checkpoint_dir, f"{checkpoint_id}.context")
        if not os.path.exists(context_file):
            return None

        try:
            # Load the checkpoint data
            with open(checkpoint_file, 'r') as f:
                data = json.load(f)

            # Load the context
            context = self._load_context(context_file)

            # Create and return the checkpoint
            return Checkpoint(
                checkpoint_id=data["id"],
                workflow_id=data["workflow_id"],
                timestamp=data.get("timestamp", ""),
                name=data.get("name"),
                data=data.get("data", {}),
                context=context
            )
        except Exception as e:
            self.logger.error(f"Error loading checkpoint {checkpoint_id}: {str(e)}")
            return None

    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Delete a checkpoint

        Args:
            checkpoint_id: ID of the checkpoint

        Returns:
            True if the checkpoint was deleted, False otherwise
        """
        # Get the checkpoint file path
        checkpoint_file = self.get_checkpoint_file(checkpoint_id)
        if not os.path.exists(checkpoint_file):
            return False

        # Get the context file path
        context_file = os.path.join(self.checkpoint_dir, f"{checkpoint_id}.context")

        try:
            # Delete the checkpoint file
            os.remove(checkpoint_file)

            # Delete the context file if it exists
            if os.path.exists(context_file):
                os.remove(context_file)

            self.logger.info(f"Deleted checkpoint {checkpoint_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting checkpoint {checkpoint_id}: {str(e)}")
            return False

    def get_checkpoint_file(self, checkpoint_id: str) -> str:
        """
        Get the file path for a checkpoint

        Args:
            checkpoint_id: ID of the checkpoint

        Returns:
            Path to the checkpoint file
        """
        return os.path.join(self.checkpoint_dir, f"{checkpoint_id}.checkpoint")

    def _save_context(self, file_path: str, context: ExecutionContext) -> None:
        """
        Save an execution context to a file

        Args:
            file_path: Path to save the context to
            context: Execution context to save
        """
        # Create the context data
        context_data = {
            "id": context.id,
            "state": context.state.to_dict(),
            "variables": {
                "global": self._get_variables_by_scope(context, "GLOBAL"),
                "workflow": self._get_variables_by_scope(context, "WORKFLOW"),
                "local": self._get_variables_by_scope(context, "LOCAL")
            }
        }

        # Save the context data
        with open(file_path, 'w') as f:
            json.dump(context_data, f, indent=2)

    def _load_context(self, file_path: str) -> ExecutionContext:
        """
        Load an execution context from a file

        Args:
            file_path: Path to load the context from

        Returns:
            Loaded execution context
        """
        # Load the context data
        with open(file_path, 'r') as f:
            context_data = json.load(f)

        # Create a new execution context
        context = ExecutionContext(context_id=context_data["id"])

        # Restore the state
        context.state = context.state.from_dict(context_data["state"])

        # Restore the variables
        self._restore_variables(context, context_data["variables"])

        return context

    def _get_variables_by_scope(self, context: ExecutionContext, scope_name: str) -> Dict[str, Any]:
        """
        Get variables by scope

        Args:
            context: Execution context
            scope_name: Name of the scope (GLOBAL, WORKFLOW, LOCAL)

        Returns:
            Dictionary of variables in the specified scope
        """
        from src.core.context.variable_storage import VariableScope

        # Get the scope enum
        scope = VariableScope[scope_name]

        # Get the variables for the scope
        return context.variables._variables[scope]

    def _restore_variables(self, context: ExecutionContext, variables: Dict[str, Dict[str, Any]]) -> None:
        """
        Restore variables to an execution context

        Args:
            context: Execution context
            variables: Dictionary of variables by scope
        """
        from src.core.context.variable_storage import VariableScope

        # Restore variables for each scope
        for scope_name, scope_vars in variables.items():
            scope = VariableScope[scope_name]
            for name, value in scope_vars.items():
                context.variables.set(name, value, scope)
