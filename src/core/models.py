"""
Defines the core data structures (models) used in the application.
SOLID: Each class represents a single data entity.
KISS: Uses simple dataclasses for structure.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class CredentialRecord:
    id: str
    name: str
    username: str
    password: str # INSECURE STORAGE - For demo only
    status: str # "Active", "Inactive" primarily for edit; others for display/history
    last_used: Optional[datetime] = None
    category: str = "Other"
    tags: List[str] = field(default_factory=list)
    notes: str = ""

@dataclass
class Variable:
    name: str
    type: str = "String" # Default type
    value: Any = ""
    scope: str = "Local" # Default scope
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ErrorConfig:
    error_type: str # Key (hierarchical path)
    severity: str = "Warning"
    action: str = "Ignore"
    custom_action: Optional[str] = None

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
class WorkflowNode:
    id: str
    type: str # e.g., 'Start', 'Click', 'Type', 'Condition', 'Loop', 'End'
    position: tuple[int, int] # (x, y) on canvas
    properties: Dict[str, Any] = field(default_factory=dict) # Node-specific settings
    label: str = "" # Store display label derived from properties?

@dataclass
class WorkflowConnection:
    id: str
    source_node_id: str
    source_port: str # e.g., 'output', 'true_branch', 'loop_body'
    target_node_id: str
    target_port: str # e.g., 'input'

@dataclass
class Workflow:
    id: str
    name: str
    nodes: Dict[str, WorkflowNode] = field(default_factory=dict)
    connections: Dict[str, WorkflowConnection] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict) # e.g., description, creation_date
