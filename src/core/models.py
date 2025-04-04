"""
Defines the core data structures (models) used in the application.
SOLID: Each class represents a single data entity.
KISS: Uses simple dataclasses for structure.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.core.utils.serialization import SerializableMixin

@dataclass
class CredentialRecord:
    id: str
    name: str
    username: str
    password: str  # Encrypted by CredentialAdapter using Fernet symmetric encryption
    status: str  # "Active", "Inactive" primarily for edit; others for display/history
    last_used: Optional[datetime] = None
    category: str = "Other"
    tags: List[str] = field(default_factory=list)
    notes: str = ""

@dataclass
class Variable(SerializableMixin):
    name: str
    type: str = "String" # Default type
    value: Any = ""
    scope: str = "Local" # Default scope
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the variable to a dictionary.

        Returns:
            Dictionary representation of the variable
        """
        # Create a dictionary with all variable properties
        # Use var_type instead of type to match test expectations
        return {
            "name": self.name,
            "value": self.value,
            "var_type": self.type,
            "scope": self.scope,
            "metadata": self.metadata.copy() if self.metadata else {}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Variable':
        """
        Create a variable from a dictionary.

        Args:
            data: Dictionary representation of the variable

        Returns:
            New variable instance

        Raises:
            ValueError: If required fields are missing
        """
        # Validate required fields
        required_fields = ["name", "value", "var_type"]
        cls.validate_required_fields(data, required_fields)

        # Extract properties with defaults
        name = data["name"]
        value = data["value"]
        var_type = data["var_type"]  # Map var_type to type
        scope = data.get("scope", "Local")
        metadata = data.get("metadata", {}).copy()

        # Create and return the variable
        return cls(
            name=name,
            value=value,
            type=var_type,
            scope=scope,
            metadata=metadata
        )

@dataclass
class ErrorConfig(SerializableMixin):
    error_type: str # Key (hierarchical path)
    severity: str = "Warning"
    action: str = "Ignore"
    custom_action: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the error config to a dictionary.

        Returns:
            Dictionary representation of the error config
        """
        # Create a dictionary with all error config properties
        return {
            "error_type": self.error_type,
            "severity": self.severity,
            "action": self.action,
            "custom_action": self.custom_action
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ErrorConfig':
        """
        Create an error config from a dictionary.

        Args:
            data: Dictionary representation of the error config

        Returns:
            New error config instance

        Raises:
            ValueError: If required fields are missing
        """
        # Validate required fields
        cls.validate_required_fields(data, ["error_type"])

        # Extract properties with defaults
        error_type = data["error_type"]
        severity = data.get("severity", "Warning")
        action = data.get("action", "Ignore")
        custom_action = data.get("custom_action")

        # Create and return the error config
        return cls(
            error_type=error_type,
            severity=severity,
            action=action,
            custom_action=custom_action
        )

@dataclass
class DataSourceConfig:
    id: str
    name: str
    type: str # e.g., 'CSV File', 'Database', 'API Endpoint'
    config_params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReportConfig:
    id: str
    name: str
    type: str # e.g., 'BarChart', 'SummaryTable'
    data_source_id: Optional[str] = None # Link to data source
    content_options: Dict[str, Any] = field(default_factory=dict)
    style_options: Dict[str, Any] = field(default_factory=dict)

# --- Workflow Models ---

@dataclass
class WorkflowNode(SerializableMixin):
    id: str
    type: str # e.g., 'Start', 'Click', 'Type', 'Condition', 'Loop', 'End'
    position: tuple[int, int] # (x, y) on canvas
    properties: Dict[str, Any] = field(default_factory=dict) # Node-specific settings
    label: str = "" # Store display label derived from properties?

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the node to a dictionary.

        Returns:
            Dictionary representation of the node
        """
        # Create a dictionary with all node properties
        return {
            "id": self.id,
            "type": self.type,
            "position": self.position,
            "properties": self.properties.copy() if self.properties else {},
            "label": self.label
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowNode':
        """
        Create a node from a dictionary.

        Args:
            data: Dictionary representation of the node

        Returns:
            New node instance

        Raises:
            ValueError: If required fields are missing
        """
        # Validate required fields
        cls.validate_required_fields(data, ["id", "type", "position"])

        # Extract properties with defaults
        node_id = data["id"]
        node_type = data["type"]
        position = data["position"]
        properties = data.get("properties", {}).copy()
        label = data.get("label", "")

        # Create and return the node
        return cls(
            id=node_id,
            type=node_type,
            position=position,
            properties=properties,
            label=label
        )

@dataclass
class WorkflowConnection(SerializableMixin):
    id: str
    source_node_id: str
    source_port: str # e.g., 'output', 'true_branch', 'loop_body'
    target_node_id: str
    target_port: str # e.g., 'input'

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the connection to a dictionary.

        Returns:
            Dictionary representation of the connection
        """
        # Create a dictionary with all connection properties
        return {
            "id": self.id,
            "source_node_id": self.source_node_id,
            "source_port": self.source_port,
            "target_node_id": self.target_node_id,
            "target_port": self.target_port
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowConnection':
        """
        Create a connection from a dictionary.

        Args:
            data: Dictionary representation of the connection

        Returns:
            New connection instance

        Raises:
            ValueError: If required fields are missing
        """
        # Validate required fields
        required_fields = ["id", "source_node_id", "source_port", "target_node_id", "target_port"]
        cls.validate_required_fields(data, required_fields)

        # Create and return the connection
        return cls(
            id=data["id"],
            source_node_id=data["source_node_id"],
            source_port=data["source_port"],
            target_node_id=data["target_node_id"],
            target_port=data["target_port"]
        )

@dataclass
class Workflow(SerializableMixin):
    id: str
    name: str
    nodes: Dict[str, WorkflowNode] = field(default_factory=dict)
    connections: Dict[str, WorkflowConnection] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict) # e.g., description, creation_date

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the workflow to a dictionary.

        Returns:
            Dictionary representation of the workflow
        """
        # Create a base dictionary with the workflow properties
        result = {
            "id": self.id,
            "name": self.name,
            "metadata": self.metadata.copy() if self.metadata else {}
        }

        # Add nodes and connections
        result["nodes"] = [node.to_dict() for node in self.nodes.values()]
        result["connections"] = [connection.to_dict() for connection in self.connections.values()]

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workflow':
        """
        Create a workflow from a dictionary.

        Args:
            data: Dictionary representation of the workflow

        Returns:
            New workflow instance

        Raises:
            ValueError: If required fields are missing
        """
        # Validate required fields
        cls.validate_required_fields(data, ["id", "name"])

        # Create the workflow with basic properties
        workflow = cls(
            id=data["id"],
            name=data["name"],
            metadata=data.get("metadata", {}).copy()
        )

        # Process nodes and connections
        cls._process_nodes(workflow, data.get("nodes", []))
        cls._process_connections(workflow, data.get("connections", []))

        return workflow

    @classmethod
    def _process_nodes(cls, workflow: 'Workflow', nodes_data: List[Dict[str, Any]]) -> None:
        """
        Process node data and add nodes to the workflow.

        Args:
            workflow: Workflow to add nodes to
            nodes_data: List of node data dictionaries
        """
        for node_data in nodes_data:
            node = WorkflowNode.from_dict(node_data)
            workflow.nodes[node.id] = node

    @classmethod
    def _process_connections(cls, workflow: 'Workflow', connections_data: List[Dict[str, Any]]) -> None:
        """
        Process connection data and add connections to the workflow.

        Args:
            workflow: Workflow to add connections to
            connections_data: List of connection data dictionaries
        """
        for connection_data in connections_data:
            connection = WorkflowConnection.from_dict(connection_data)
            workflow.connections[connection.id] = connection

    def add_node(self, node: WorkflowNode) -> None:
        """
        Add a node to the workflow.

        Args:
            node: Node to add
        """
        self.nodes[node.id] = node

    def add_connection(self, connection: WorkflowConnection) -> None:
        """
        Add a connection to the workflow.

        Args:
            connection: Connection to add
        """
        self.connections[connection.id] = connection
