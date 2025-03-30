"""
Workflow Builder Presenter for managing workflow creation and editing.
SOLID: Single responsibility - business logic for workflow building.
KISS: Simple operations with clear error handling.
"""
import uuid
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING

from ..presenters.base_presenter import BasePresenter
from ..adapters.workflow_adapter import WorkflowAdapter
from src.core.models import Workflow, WorkflowNode, WorkflowConnection

if TYPE_CHECKING:
    from ..views.workflow_view import WorkflowView
    from app import AutoClickApp

class WorkflowPresenter(BasePresenter[WorkflowAdapter]):
    """Presenter for the Workflow Builder view."""
    
    # Type hints for view and app
    view: 'WorkflowView'
    app: 'AutoClickApp'
    
    def __init__(self, view: 'WorkflowView', app: 'AutoClickApp', service: WorkflowAdapter):
        """
        Initialize the workflow presenter.
        
        Args:
            view: The workflow view
            app: The main application
            service: The workflow adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.current_workflow: Optional[Workflow] = None
        self.selected_node_id: Optional[str] = None
        self.node_types: List[Dict[str, Any]] = []
    
    def initialize_view(self):
        """Initialize the view with data."""
        try:
            # Get node types from the service
            self.node_types = self.service.get_node_types()
            
            # Initialize the canvas and toolbox
            self.view.initialize_canvas()
            self.view.initialize_toolbox(self.node_types)
            
            # Create a new empty workflow
            self.create_new_workflow("Untitled Workflow")
            
            self.update_app_status("Workflow builder initialized")
        except Exception as e:
            self._handle_error("initializing workflow builder", e)
    
    def load_workflow(self, workflow_id: str):
        """
        Load a workflow from the service.
        
        Args:
            workflow_id: ID of the workflow to load
        """
        try:
            # Get the workflow from the service
            workflow = self.service.get_workflow(workflow_id)
            
            if workflow:
                # Set the current workflow
                self.current_workflow = workflow
                
                # Clear the canvas and redraw the workflow
                self.view.clear_canvas()
                self.view.redraw_workflow(workflow)
                
                # Update the workflow name
                self.view.workflow_name_var.set(workflow.name)
                
                self.update_app_status(f"Loaded workflow: {workflow.name}")
            else:
                self.update_app_status(f"Workflow not found: {workflow_id}")
        except Exception as e:
            self._handle_error(f"loading workflow {workflow_id}", e)
    
    def create_new_workflow(self, name: str):
        """
        Create a new workflow.
        
        Args:
            name: Name of the new workflow
        """
        try:
            # Create a new workflow
            workflow_id = str(uuid.uuid4())
            workflow = Workflow(
                id=workflow_id,
                name=name,
                nodes={},
                connections={}
            )
            
            # Add a start node
            start_node_id = str(uuid.uuid4())
            start_node = WorkflowNode(
                id=start_node_id,
                type="Start",
                position=(100, 100),
                properties={},
                label="Start"
            )
            workflow.nodes[start_node_id] = start_node
            
            # Set the current workflow
            self.current_workflow = workflow
            
            # Save the workflow to the service
            self.service.create_workflow(workflow)
            
            # Clear the canvas and redraw the workflow
            self.view.clear_canvas()
            self.view.redraw_workflow(workflow)
            
            # Update the workflow name
            self.view.workflow_name_var.set(name)
            
            self.update_app_status(f"Created new workflow: {name}")
        except Exception as e:
            self._handle_error(f"creating new workflow {name}", e)
    
    def save_workflow(self):
        """Save the current workflow."""
        try:
            if not self.current_workflow:
                self.update_app_status("No workflow to save")
                return
            
            # Update the workflow name
            self.current_workflow.name = self.view.get_workflow_name()
            
            # Save the workflow to the service
            self.service.update_workflow(self.current_workflow)
            
            self.update_app_status(f"Saved workflow: {self.current_workflow.name}")
        except Exception as e:
            self._handle_error("saving workflow", e)
    
    def add_node(self, node_type: str, position: Tuple[int, int]):
        """
        Add a node to the current workflow.
        
        Args:
            node_type: Type of node to add
            position: Position (x, y) to place the node
        """
        try:
            if not self.current_workflow:
                self.create_new_workflow("Untitled Workflow")
            
            # Create a new node
            node_id = str(uuid.uuid4())
            node = WorkflowNode(
                id=node_id,
                type=node_type,
                position=position,
                properties={},
                label=node_type
            )
            
            # Add the node to the workflow
            self.current_workflow.nodes[node_id] = node
            
            # Draw the node on the canvas
            self.view.draw_node(node)
            
            self.update_app_status(f"Added {node_type} node")
            
            return node_id
        except Exception as e:
            self._handle_error(f"adding {node_type} node", e)
            return None
    
    def select_node(self, node_id: str):
        """
        Select a node in the workflow.
        
        Args:
            node_id: ID of the node to select
        """
        try:
            if not self.current_workflow or node_id not in self.current_workflow.nodes:
                self.update_app_status(f"Node not found: {node_id}")
                return
            
            # Set the selected node
            self.selected_node_id = node_id
            
            # Update the view
            self.view.select_node_visual(node_id)
            self.view.display_properties_for_node(self.current_workflow.nodes[node_id])
            
            self.update_app_status(f"Selected {self.current_workflow.nodes[node_id].type} node")
        except Exception as e:
            self._handle_error(f"selecting node {node_id}", e)
    
    def update_node_properties(self):
        """Update the properties of the selected node."""
        try:
            if not self.current_workflow or not self.selected_node_id:
                self.update_app_status("No node selected")
                return
            
            # Get the properties from the view
            properties = self.view.get_properties_data()
            
            if not properties:
                self.update_app_status("No properties to update")
                return
            
            # Update the node properties
            node = self.current_workflow.nodes[self.selected_node_id]
            node.properties.update(properties)
            
            # Update the node label if provided
            if "label" in properties:
                node.label = properties["label"]
            
            # Redraw the workflow
            self.view.redraw_workflow(self.current_workflow)
            
            self.update_app_status(f"Updated {node.type} node properties")
        except Exception as e:
            self._handle_error("updating node properties", e)
    
    def delete_node(self):
        """Delete the selected node."""
        try:
            if not self.current_workflow or not self.selected_node_id:
                self.update_app_status("No node selected")
                return
            
            # Get the node
            node = self.current_workflow.nodes[self.selected_node_id]
            
            # Find connections to/from this node
            connections_to_delete = []
            for conn_id, conn in self.current_workflow.connections.items():
                if conn.source_node_id == self.selected_node_id or conn.target_node_id == self.selected_node_id:
                    connections_to_delete.append(conn_id)
            
            # Delete the connections
            for conn_id in connections_to_delete:
                del self.current_workflow.connections[conn_id]
            
            # Delete the node
            del self.current_workflow.nodes[self.selected_node_id]
            
            # Clear the selection
            self.selected_node_id = None
            
            # Redraw the workflow
            self.view.redraw_workflow(self.current_workflow)
            
            self.update_app_status(f"Deleted {node.type} node")
        except Exception as e:
            self._handle_error("deleting node", e)
    
    def add_connection(self, source_node_id: str, source_port: str, target_node_id: str, target_port: str):
        """
        Add a connection between nodes.
        
        Args:
            source_node_id: ID of the source node
            source_port: Port on the source node
            target_node_id: ID of the target node
            target_port: Port on the target node
        """
        try:
            if not self.current_workflow:
                self.update_app_status("No workflow to add connection to")
                return
            
            # Check if the nodes exist
            if source_node_id not in self.current_workflow.nodes:
                self.update_app_status(f"Source node not found: {source_node_id}")
                return
            
            if target_node_id not in self.current_workflow.nodes:
                self.update_app_status(f"Target node not found: {target_node_id}")
                return
            
            # Create a new connection
            conn_id = str(uuid.uuid4())
            connection = WorkflowConnection(
                id=conn_id,
                source_node_id=source_node_id,
                source_port=source_port,
                target_node_id=target_node_id,
                target_port=target_port
            )
            
            # Add the connection to the workflow
            self.current_workflow.connections[conn_id] = connection
            
            # Draw the connection on the canvas
            self.view.draw_connection(connection)
            
            self.update_app_status("Added connection")
            
            return conn_id
        except Exception as e:
            self._handle_error("adding connection", e)
            return None
    
    def delete_connection(self, connection_id: str):
        """
        Delete a connection.
        
        Args:
            connection_id: ID of the connection to delete
        """
        try:
            if not self.current_workflow or connection_id not in self.current_workflow.connections:
                self.update_app_status(f"Connection not found: {connection_id}")
                return
            
            # Delete the connection
            del self.current_workflow.connections[connection_id]
            
            # Redraw the workflow
            self.view.redraw_workflow(self.current_workflow)
            
            self.update_app_status("Deleted connection")
        except Exception as e:
            self._handle_error(f"deleting connection {connection_id}", e)
    
    def execute_workflow(self):
        """
        Execute the current workflow.
        
        Returns:
            Dictionary containing execution results
        """
        try:
            if not self.current_workflow:
                self.update_app_status("No workflow to execute")
                return {"success": False, "message": "No workflow to execute"}
            
            # Save the workflow first
            self.save_workflow()
            
            # Execute the workflow
            result = self.service.execute_workflow(self.current_workflow)
            
            if result["success"]:
                self.update_app_status("Workflow executed successfully")
            else:
                self.update_app_status(f"Workflow execution failed: {result['message']}")
            
            return result
        except Exception as e:
            self._handle_error("executing workflow", e)
            return {"success": False, "message": str(e)}
    
    def validate_workflow(self):
        """
        Validate the current workflow.
        
        Returns:
            Dictionary containing validation results
        """
        try:
            if not self.current_workflow:
                self.update_app_status("No workflow to validate")
                return {"valid": False, "errors": ["No workflow to validate"]}
            
            # Initialize validation results
            result = {"valid": True, "errors": []}
            
            # Check if there's a Start node
            has_start = False
            for node in self.current_workflow.nodes.values():
                if node.type == "Start":
                    has_start = True
                    break
            
            if not has_start:
                result["valid"] = False
                result["errors"].append("No Start node found")
            
            # Check if there's an End node
            has_end = False
            for node in self.current_workflow.nodes.values():
                if node.type == "End":
                    has_end = True
                    break
            
            if not has_end:
                result["valid"] = False
                result["errors"].append("No End node found")
            
            # Check if all nodes are connected
            connected_nodes = set()
            for conn in self.current_workflow.connections.values():
                connected_nodes.add(conn.source_node_id)
                connected_nodes.add(conn.target_node_id)
            
            for node_id in self.current_workflow.nodes:
                if node_id not in connected_nodes and len(self.current_workflow.nodes) > 1:
                    result["valid"] = False
                    result["errors"].append(f"Node {node_id} is not connected")
            
            # Update status
            if result["valid"]:
                self.update_app_status("Workflow is valid")
            else:
                self.update_app_status(f"Workflow validation failed: {', '.join(result['errors'])}")
            
            return result
        except Exception as e:
            self._handle_error("validating workflow", e)
            return {"valid": False, "errors": [str(e)]}
