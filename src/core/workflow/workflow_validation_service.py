"""
Workflow validation service.
SOLID: Single responsibility - workflow validation logic.
KISS: Simple validation methods.
"""
from typing import List, Dict, Set
from src.core.models import Workflow, WorkflowNode, WorkflowConnection

class WorkflowValidationError(Exception):
    """Exception raised when a workflow fails validation."""
    pass

class WorkflowValidationService:
    """Service for validating workflows."""

    def validate_workflow(self, workflow: Workflow) -> None:
        """
        Validate a workflow.

        Args:
            workflow: Workflow to validate

        Raises:
            WorkflowValidationError: If the workflow is invalid
        """
        errors = []

        # Check for required fields
        if not workflow.id:
            errors.append("Workflow ID is required")
        if not workflow.name:
            errors.append("Workflow name is required")

        # Check for start and end nodes
        start_nodes = [node for node in workflow.nodes.values() if node.type == "Start"]
        if not start_nodes:
            errors.append("Workflow must have at least one Start node")
        elif len(start_nodes) > 1:
            errors.append("Workflow must have only one Start node")

        # End node check is now a warning, not an error
        end_nodes = [node for node in workflow.nodes.values() if node.type == "End"]
        if not end_nodes:
            # Only warn about missing End node if there are more than just a Start node
            # This allows new workflows with just a Start node to be created
            if len(workflow.nodes) > 1:
                errors.append("Warning: Workflow should have at least one End node for proper execution")

        # Check for cycles
        try:
            self._detect_cycles(workflow)
        except WorkflowValidationError as e:
            errors.append(str(e))

        # Check for disconnected nodes
        disconnected = self._find_disconnected_nodes(workflow)
        if disconnected:
            node_names = ", ".join([f"{node.type} ({node.id})" for node in disconnected])
            errors.append(f"Workflow contains disconnected nodes: {node_names}")

        # Check for invalid connections
        for conn_id, conn in workflow.connections.items():
            # Check that source and target nodes exist
            if conn.source_node_id not in workflow.nodes:
                errors.append(f"Connection {conn_id} references non-existent source node {conn.source_node_id}")
            if conn.target_node_id not in workflow.nodes:
                errors.append(f"Connection {conn_id} references non-existent target node {conn.target_node_id}")

        # If there are any errors, raise an exception
        if errors:
            raise WorkflowValidationError("Workflow validation failed: " + "; ".join(errors))


    def _detect_cycles(self, workflow: Workflow) -> None:
        """
        Detect cycles in a workflow.

        Args:
            workflow: Workflow to check

        Raises:
            WorkflowValidationError: If a cycle is detected
        """
        # Build adjacency list
        adjacency: Dict[str, List[str]] = {node_id: [] for node_id in workflow.nodes}
        for conn in workflow.connections.values():
            if conn.source_node_id in adjacency:
                adjacency[conn.source_node_id].append(conn.target_node_id)

        # Track visited and recursion stack
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node_id: str) -> bool:
            """Depth-first search to detect cycles."""
            visited.add(node_id)

            rec_stack.add(node_id)

            for neighbor in adjacency.get(node_id, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node_id)
            return False
        # Check each node
        for node_id in workflow.nodes:
            if node_id not in visited:
                if dfs(node_id):
                    raise WorkflowValidationError("Workflow contains a cycle")


    def _find_disconnected_nodes(self, workflow: Workflow) -> List[WorkflowNode]:
        """
        Find nodes that are not reachable from any Start node.

        Args:
            workflow: Workflow to check

        Returns:
            List of disconnected nodes
        """
        if not workflow.nodes:
            return []

        start_nodes = [node.id for node in workflow.nodes.values() if node.type == "Start"]
        if not start_nodes:
            # If no start node, consider all nodes disconnected (though validation should catch this earlier)
            return list(workflow.nodes.values())

        # Build adjacency list (source -> list of targets)
        adjacency: Dict[str, List[str]] = {node_id: [] for node_id in workflow.nodes}
        for conn in workflow.connections.values():
            if conn.source_node_id in adjacency:
                adjacency[conn.source_node_id].append(conn.target_node_id)

        # Perform BFS from all start nodes to find reachable nodes
        reachable: Set[str] = set()
        queue: List[str] = start_nodes[:] # Start queue with all start nodes

        for start_node_id in start_nodes:
             reachable.add(start_node_id) # Start nodes are reachable

        head = 0
        while head < len(queue):
            current_node_id = queue[head]
            head += 1

            for neighbor_id in adjacency.get(current_node_id, []):
                if neighbor_id not in reachable:
                    reachable.add(neighbor_id)
                    queue.append(neighbor_id)

        # Return nodes that are not in the reachable set
        disconnected_nodes = [
            node for node_id, node in workflow.nodes.items() if node_id not in reachable
        ]
        return disconnected_nodes