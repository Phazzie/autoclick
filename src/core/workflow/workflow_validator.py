"""
Workflow validator for validating workflow definitions.

This module provides a validator for workflow definitions, ensuring they
meet the required structure and constraints before execution.
"""
from typing import List, Dict, Any, Set
from .interfaces import IWorkflowValidator, WorkflowDefinition
from .exceptions import InvalidWorkflowDefinitionError


class WorkflowValidator(IWorkflowValidator):
    """
    Validator for workflow definitions.

    This class validates workflow definitions to ensure they meet the required
    structure and constraints before execution.
    """

    def validate(self, workflow: WorkflowDefinition) -> List[str]:
        """
        Validate a workflow definition.

        Args:
            workflow: Workflow definition to validate

        Returns:
            List of validation errors, empty if valid
        """
        errors = []

        # Basic validation
        self._validate_basic_properties(workflow, errors)

        # Validate actions
        self._validate_actions(workflow, errors)

        # Validate connections
        self._validate_connections(workflow, errors)

        # Validate for cycles
        self._validate_no_cycles(workflow, errors)

        return errors

    def _validate_basic_properties(self, workflow: WorkflowDefinition, errors: List[str]) -> None:
        """
        Validate basic workflow properties.

        Args:
            workflow: Workflow definition to validate
            errors: List to append errors to
        """
        if not workflow.workflow_id:
            errors.append("Workflow ID is required")

        if not workflow.name:
            errors.append("Workflow name is required")

    def _validate_actions(self, workflow: WorkflowDefinition, errors: List[str]) -> None:
        """
        Validate workflow actions.

        Args:
            workflow: Workflow definition to validate
            errors: List to append errors to
        """
        # Check if actions attribute exists
        if not hasattr(workflow, 'actions') or not workflow.actions:
            # Try to use nodes instead if available
            if hasattr(workflow, 'nodes') and workflow.nodes:
                # Convert nodes to actions format for validation
                actions = []
                for node_id, node in workflow.nodes.items():
                    if isinstance(node, dict):
                        actions.append({
                            'id': node_id,
                            'type': node.get('type', 'Unknown'),
                            'properties': node.get('properties', {})
                        })
                    else:
                        actions.append({
                            'id': node_id,
                            'type': getattr(node, 'type', 'Unknown'),
                            'properties': getattr(node, 'properties', {})
                        })
                # Set actions for validation
                workflow.actions = actions
            else:
                errors.append("Workflow must contain at least one action or node")
                return

        action_ids = set()

        for i, action in enumerate(workflow.actions):
            # Check required fields
            if 'id' not in action:
                errors.append(f"Action at index {i} is missing an ID")
                continue

            action_id = action['id']

            if action_id in action_ids:
                errors.append(f"Duplicate action ID: {action_id}")
            else:
                action_ids.add(action_id)

            if 'type' not in action:
                errors.append(f"Action '{action_id}' is missing a type")

            # Additional action-specific validation could be added here

    def _validate_connections(self, workflow: WorkflowDefinition, errors: List[str]) -> None:
        """
        Validate workflow connections.

        Args:
            workflow: Workflow definition to validate
            errors: List to append errors to
        """
        # Check if connections attribute exists and is not empty
        if not hasattr(workflow, 'connections') or not workflow.connections:
            return  # No connections is valid for single-action workflows

        # Get action IDs from actions or nodes
        if hasattr(workflow, 'actions') and workflow.actions:
            action_ids = {action['id'] for action in workflow.actions if 'id' in action}
        elif hasattr(workflow, 'nodes') and workflow.nodes:
            action_ids = set(workflow.nodes.keys())
        else:
            action_ids = set()

        for i, connection in enumerate(workflow.connections):
            # Check required fields
            source_field = 'source' if 'source' in connection else 'source_node_id'
            target_field = 'target' if 'target' in connection else 'target_node_id'

            if source_field not in connection:
                errors.append(f"Connection at index {i} is missing a source")
                continue

            if target_field not in connection:
                errors.append(f"Connection at index {i} is missing a target")
                continue

            source = connection[source_field]
            target = connection[target_field]

            # Check that source and target exist
            if source not in action_ids:
                errors.append(f"Connection source '{source}' does not exist")

            if target not in action_ids:
                errors.append(f"Connection target '{target}' does not exist")

            # Check for self-connections
            if source == target:
                errors.append(f"Self-connection detected for action '{source}'")

    def _validate_no_cycles(self, workflow: WorkflowDefinition, errors: List[str]) -> None:
        """
        Validate that the workflow has no cycles.

        Args:
            workflow: Workflow definition to validate
            errors: List to append errors to
        """
        # Build adjacency list
        adjacency_list: Dict[str, List[str]] = {}

        # Get nodes from actions or nodes attribute
        if hasattr(workflow, 'actions') and workflow.actions:
            for action in workflow.actions:
                if 'id' in action:
                    adjacency_list[action['id']] = []
        elif hasattr(workflow, 'nodes') and workflow.nodes:
            for node_id in workflow.nodes:
                adjacency_list[node_id] = []

        # Get connections
        if hasattr(workflow, 'connections') and workflow.connections:
            for connection in workflow.connections:
                source_field = 'source' if 'source' in connection else 'source_node_id'
                target_field = 'target' if 'target' in connection else 'target_node_id'

                if source_field in connection and target_field in connection:
                    source = connection[source_field]
                    target = connection[target_field]

                    if source in adjacency_list:
                        adjacency_list[source].append(target)

        # If no connections, no need to check for cycles
        if not any(adjacency_list.values()):
            return

        # Check for cycles using DFS
        visited: Set[str] = set()
        path: Set[str] = set()

        def dfs(node: str) -> bool:
            """
            Depth-first search to detect cycles.

            Args:
                node: Current node

            Returns:
                True if a cycle is detected, False otherwise
            """
            if node in path:
                errors.append(f"Cycle detected involving action '{node}'")
                return True

            if node in visited:
                return False

            visited.add(node)
            path.add(node)

            for neighbor in adjacency_list.get(node, []):
                if dfs(neighbor):
                    return True

            path.remove(node)
            return False

        # Start DFS from each node
        for node in adjacency_list:
            if node not in visited:
                dfs(node)
