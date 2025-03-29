"""Execution presenter implementation"""
import logging
import threading
import time
from typing import Any, Dict, Optional

from src.ui.models.execution_model import ExecutionModel
from src.ui.services.execution_service import ExecutionService
from src.ui.interfaces.view_interface import ExecutionViewInterface


class ExecutionPresenter:
    """Presenter for execution tab"""
    
    def __init__(
        self,
        model: ExecutionModel,
        service: ExecutionService,
        view: Optional[ExecutionViewInterface] = None
    ) -> None:
        """
        Initialize the execution presenter
        
        Args:
            model: Execution model
            service: Execution service
            view: Execution view
        """
        self.logger = logging.getLogger(__name__)
        self.model = model
        self.service = service
        self.view = view
    
    def set_view(self, view: ExecutionViewInterface) -> None:
        """
        Set the view
        
        Args:
            view: Execution view
        """
        self.view = view
    
    def run_workflow(self, workflow: Dict[str, Any]) -> None:
        """
        Run a workflow
        
        Args:
            workflow: Workflow to run
        """
        self.logger.info("Running workflow")
        
        if not self.view:
            return
        
        if not workflow.get("actions"):
            self.view.show_message("Workflow has no actions")
            return
        
        try:
            # Start execution
            self.model.start_execution(workflow)
            
            # Initialize browser
            options = self.model.get_options()
            self.service.initialize_browser(options)
            
            # Update view
            self.refresh_view()
            
            # Execute actions in a separate thread
            threading.Thread(
                target=self._execute_workflow,
                args=(workflow,),
                daemon=True
            ).start()
            
            self.view.show_message("Workflow execution started")
        except Exception as e:
            self.logger.error(f"Error starting workflow: {str(e)}")
            self.model.add_log_entry("error", f"Error starting workflow: {str(e)}")
            self.refresh_view()
            self.view.show_message(f"Error starting workflow: {str(e)}")
    
    def _execute_workflow(self, workflow: Dict[str, Any]) -> None:
        """
        Execute a workflow
        
        Args:
            workflow: Workflow to execute
        """
        try:
            for i, action in enumerate(workflow.get("actions", [])):
                if not self.model.is_execution_running():
                    break
                
                self.model.add_log_entry(
                    "info",
                    f"Executing action {i+1}: {action.get('description', action.get('type'))}"
                )
                self.refresh_view()
                
                result = self.service.execute_action(action)
                
                if result.get("success"):
                    self.model.add_log_entry("info", result.get("message", "Action completed"))
                else:
                    self.model.add_log_entry("error", result.get("message", "Action failed"))
                
                self.refresh_view()
                
                # Small delay between actions
                time.sleep(0.5)
            
            self.model.add_log_entry("info", "Workflow execution completed")
        except Exception as e:
            self.model.add_log_entry("error", f"Error executing workflow: {str(e)}")
        finally:
            self.service.close_browser()
            self.model.stop_execution()
            self.refresh_view()
    
    def stop_execution(self) -> None:
        """Stop workflow execution"""
        self.logger.info("Stopping workflow execution")
        
        self.model.stop_execution()
        self.refresh_view()
        
        if self.view:
            self.view.show_message("Workflow execution stopped")
    
    def set_browser_type(self, browser_type: str) -> None:
        """
        Set the browser type
        
        Args:
            browser_type: Browser type
        """
        self.logger.info(f"Setting browser type to {browser_type}")
        
        self.model.set_option("browser_type", browser_type)
        
        if self.view:
            self.view.show_message(f"Browser type set to {browser_type}")
    
    def set_headless(self, headless: bool) -> None:
        """
        Set headless mode
        
        Args:
            headless: Whether to use headless mode
        """
        self.logger.info(f"Setting headless mode to {headless}")
        
        self.model.set_option("headless", headless)
        
        if self.view:
            self.view.show_message(f"Headless mode {'enabled' if headless else 'disabled'}")
    
    def refresh_view(self) -> None:
        """Refresh the view with current model data"""
        self.logger.debug("Refreshing execution view")
        
        if self.view:
            self.view.display_execution_log(self.model.get_log_entries())
            self.view.update_execution_status(self.model.is_execution_running())
