"""
Action Execution Presenter for managing workflow execution.
SOLID: Single responsibility - business logic for action execution.
KISS: Simple operations with clear error handling.
"""
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING
import time
import threading

from ..presenters.base_presenter import BasePresenter
from ..adapters.workflow_adapter import WorkflowAdapter
from src.core.models import Workflow

if TYPE_CHECKING:
    from ..views.action_execution_view import ActionExecutionView
    from app import AutoClickApp

class ActionExecutionPresenter(BasePresenter[WorkflowAdapter]):
    """Presenter for the Action Execution view."""
    
    # Type hints for view and app
    view: 'ActionExecutionView'
    app: 'AutoClickApp'
    
    def __init__(self, view: 'ActionExecutionView', app: 'AutoClickApp', service: WorkflowAdapter):
        """
        Initialize the action execution presenter.
        
        Args:
            view: The action execution view
            app: The main application
            service: The workflow adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.current_workflow: Optional[Workflow] = None
        self.execution_thread: Optional[threading.Thread] = None
        self.is_executing = False
        self.execution_paused = False
        self.execution_results = []
        self.current_step = 0
        self.total_steps = 0
    
    def initialize_view(self):
        """Initialize the view with data."""
        try:
            # Get all workflows from the service
            workflows = self.service.get_all_workflows()
            
            # Update the view with the workflows
            self.view.update_workflow_list(workflows)
            
            self.update_app_status("Action execution initialized")
        except Exception as e:
            self._handle_error("initializing action execution", e)
    
    def load_workflows(self):
        """Load workflows from the service."""
        try:
            # Get all workflows from the service
            workflows = self.service.get_all_workflows()
            
            # Update the view with the workflows
            self.view.update_workflow_list(workflows)
            
            self.update_app_status("Workflows loaded")
        except Exception as e:
            self._handle_error("loading workflows", e)
    
    def select_workflow(self, workflow_id: str):
        """
        Select a workflow for execution.
        
        Args:
            workflow_id: ID of the workflow to select
        """
        try:
            # Get the workflow from the service
            workflow = self.service.get_workflow(workflow_id)
            
            if workflow:
                # Set the current workflow
                self.current_workflow = workflow
                
                # Update the view
                self.view.display_workflow_details(workflow)
                
                # Enable execution controls
                self.view.set_execution_controls_state(True)
                
                self.update_app_status(f"Selected workflow: {workflow.name}")
            else:
                self.update_app_status(f"Workflow not found: {workflow_id}")
        except Exception as e:
            self._handle_error(f"selecting workflow {workflow_id}", e)
    
    def execute_workflow(self):
        """Execute the current workflow."""
        try:
            if not self.current_workflow:
                self.update_app_status("No workflow selected")
                return
            
            if self.is_executing:
                self.update_app_status("Workflow already executing")
                return
            
            # Reset execution state
            self.is_executing = True
            self.execution_paused = False
            self.execution_results = []
            self.current_step = 0
            
            # Count total steps (nodes)
            self.total_steps = len(self.current_workflow.nodes)
            
            # Update the view
            self.view.reset_execution_display()
            self.view.update_progress(0, self.total_steps)
            self.view.set_execution_controls_state(False)
            self.view.set_pause_resume_button_state(True, "Pause")
            self.view.set_stop_button_state(True)
            
            # Start execution in a separate thread
            self.execution_thread = threading.Thread(target=self._execute_workflow_thread)
            self.execution_thread.daemon = True
            self.execution_thread.start()
            
            self.update_app_status(f"Executing workflow: {self.current_workflow.name}")
        except Exception as e:
            self.is_executing = False
            self._handle_error("executing workflow", e)
    
    def _execute_workflow_thread(self):
        """Execute the workflow in a separate thread."""
        try:
            # Execute the workflow
            result = self.service.execute_workflow(self.current_workflow)
            
            # Simulate execution for demonstration
            self._simulate_execution()
            
            # Update the view with the results
            self.app.after(0, lambda: self.view.display_execution_results(result))
            
            # Reset execution state
            self.is_executing = False
            
            # Update the view
            self.app.after(0, lambda: self.view.set_execution_controls_state(True))
            self.app.after(0, lambda: self.view.set_pause_resume_button_state(False, "Pause"))
            self.app.after(0, lambda: self.view.set_stop_button_state(False))
            
            self.app.after(0, lambda: self.update_app_status(f"Workflow execution completed: {self.current_workflow.name}"))
        except Exception as e:
            self.is_executing = False
            self.app.after(0, lambda: self._handle_error("executing workflow thread", e))
    
    def _simulate_execution(self):
        """Simulate workflow execution for demonstration."""
        # Simulate execution of each node
        for i, (node_id, node) in enumerate(self.current_workflow.nodes.items()):
            # Check if execution was stopped
            if not self.is_executing:
                break
            
            # Check if execution is paused
            while self.execution_paused and self.is_executing:
                time.sleep(0.1)
            
            # Update current step
            self.current_step = i + 1
            
            # Update the view
            self.app.after(0, lambda step=self.current_step: self.view.update_progress(step, self.total_steps))
            self.app.after(0, lambda node=node: self.view.highlight_current_node(node.id))
            
            # Simulate action execution
            result = {
                "node_id": node_id,
                "node_type": node.type,
                "node_label": node.label,
                "success": True,
                "message": f"Executed {node.type} node: {node.label}",
                "timestamp": time.time()
            }
            
            # Add result to execution results
            self.execution_results.append(result)
            
            # Update the view with the result
            self.app.after(0, lambda r=result: self.view.add_execution_result(r))
            
            # Simulate execution time
            time.sleep(1)
    
    def pause_resume_execution(self):
        """Pause or resume workflow execution."""
        try:
            if not self.is_executing:
                self.update_app_status("No workflow executing")
                return
            
            if self.execution_paused:
                # Resume execution
                self.execution_paused = False
                self.view.set_pause_resume_button_state(True, "Pause")
                self.update_app_status("Workflow execution resumed")
            else:
                # Pause execution
                self.execution_paused = True
                self.view.set_pause_resume_button_state(True, "Resume")
                self.update_app_status("Workflow execution paused")
        except Exception as e:
            self._handle_error("pausing/resuming workflow execution", e)
    
    def stop_execution(self):
        """Stop workflow execution."""
        try:
            if not self.is_executing:
                self.update_app_status("No workflow executing")
                return
            
            # Stop execution
            self.is_executing = False
            self.execution_paused = False
            
            # Update the view
            self.view.set_execution_controls_state(True)
            self.view.set_pause_resume_button_state(False, "Pause")
            self.view.set_stop_button_state(False)
            
            self.update_app_status("Workflow execution stopped")
        except Exception as e:
            self._handle_error("stopping workflow execution", e)
    
    def save_execution_results(self, file_path: str):
        """
        Save execution results to a file.
        
        Args:
            file_path: Path to save the results
        """
        try:
            if not self.execution_results:
                self.update_app_status("No execution results to save")
                return
            
            # Save the results
            self.view.save_results_to_file(self.execution_results, file_path)
            
            self.update_app_status(f"Execution results saved to: {file_path}")
        except Exception as e:
            self._handle_error(f"saving execution results to {file_path}", e)
