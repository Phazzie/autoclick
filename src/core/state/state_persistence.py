"""State persistence functionality for saving and loading execution state"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from src.core.context.execution_context import ExecutionContext
from src.core.state.state_persistence_interface import StatePersistenceInterface


class StatePersistence(StatePersistenceInterface):
    """
    Handles saving and loading execution state

    This class provides methods to save the current execution state to a file
    and load it back later, enabling workflow pause and resume functionality.
    """

    def __init__(self, state_dir: str = "states"):
        """
        Initialize the state persistence

        Args:
            state_dir: Directory to store state files
        """
        self.state_dir = state_dir
        self.logger = logging.getLogger(self.__class__.__name__)

        # Create the state directory if it doesn't exist
        os.makedirs(self.state_dir, exist_ok=True)

    def save_state(self, workflow_id: str, context: ExecutionContext) -> str:
        """
        Save the current execution state to a file

        Args:
            workflow_id: ID of the workflow
            context: Execution context to save

        Returns:
            Path to the saved state file
        """
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

        # Create the filename
        filename = f"{workflow_id}_{timestamp}.state"
        file_path = os.path.join(self.state_dir, filename)

        # Create the state data
        state_data = {
            "workflow_id": workflow_id,
            "timestamp": datetime.now().isoformat(),
            "context": {
                "id": context.id,
                "state": context.state.to_dict(),
                "variables": {
                    "global": self._get_variables_by_scope(context, "GLOBAL"),
                    "workflow": self._get_variables_by_scope(context, "WORKFLOW"),
                    "local": self._get_variables_by_scope(context, "LOCAL")
                }
            }
        }

        # Save the state to a file
        try:
            with open(file_path, 'w') as f:
                json.dump(state_data, f, indent=2)

            self.logger.info(f"Saved state to {file_path}")
            return file_path
        except Exception as e:
            self.logger.error(f"Error saving state to {file_path}: {str(e)}")
            raise

    def load_state(self, file_path: str) -> ExecutionContext:
        """
        Load execution state from a file

        Args:
            file_path: Path to the state file

        Returns:
            Loaded execution context

        Raises:
            FileNotFoundError: If the state file doesn't exist
            ValueError: If the state file is invalid
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"State file not found: {file_path}")

        try:
            # Load the state data
            with open(file_path, 'r') as f:
                state_data = json.load(f)

            # Create a new execution context
            context = ExecutionContext(context_id=state_data["context"]["id"])

            # Restore the state
            context.state = context.state.from_dict(state_data["context"]["state"])

            # Restore the variables
            self._restore_variables(context, state_data["context"]["variables"])

            self.logger.info(f"Loaded state from {file_path}")
            return context
        except Exception as e:
            self.logger.error(f"Error loading state from {file_path}: {str(e)}")
            raise ValueError(f"Invalid state file: {str(e)}")

    def get_state_files(self, workflow_id: str) -> List[str]:
        """
        Get all state files for a workflow

        Args:
            workflow_id: ID of the workflow

        Returns:
            List of state file paths, sorted by timestamp (newest first)
        """
        # Get all state files for the workflow
        files = []
        for filename in os.listdir(self.state_dir):
            if filename.startswith(f"{workflow_id}_") and filename.endswith(".state"):
                files.append(os.path.join(self.state_dir, filename))

        # Sort by modification time (newest first)
        files.sort(key=os.path.getmtime, reverse=True)

        return files

    def get_latest_state_file(self, workflow_id: str) -> Optional[str]:
        """
        Get the latest state file for a workflow

        Args:
            workflow_id: ID of the workflow

        Returns:
            Path to the latest state file, or None if no state files exist
        """
        files = self.get_state_files(workflow_id)
        return files[0] if files else None

    def cleanup_old_states(self, workflow_id: str, max_states: int = 10) -> int:
        """
        Clean up old state files for a workflow

        Args:
            workflow_id: ID of the workflow
            max_states: Maximum number of state files to keep

        Returns:
            Number of state files removed
        """
        files = self.get_state_files(workflow_id)

        # If we have more files than the maximum, remove the oldest ones
        if len(files) > max_states:
            # Get the files to remove (oldest first)
            # Note: files are already sorted by modification time (newest first)
            to_remove = files[max_states:]

            # Remove the files
            removed_count = 0
            for file_path in to_remove:
                try:
                    os.remove(file_path)
                    removed_count += 1
                    self.logger.info(f"Removed old state file: {file_path}")
                except Exception as e:
                    self.logger.error(f"Error removing state file {file_path}: {str(e)}")

            return removed_count

        return 0

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
            # Convert scope name to uppercase to match enum member names
            scope = VariableScope[scope_name.upper()]
            for name, value in scope_vars.items():
                context.variables.set(name, value, scope)
