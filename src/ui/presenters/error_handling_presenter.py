"""
Presenter for the Error Handling View.
SOLID: Single responsibility - handling error recovery logic.
KISS: Simple delegation to error handling service.
"""
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING
import uuid
from tkinter import messagebox

from ..presenters.base_presenter import BasePresenter

if TYPE_CHECKING:
    from ..views.error_handling_view import ErrorHandlingView
    from app import AutoClickApp
    from ..adapters.error_adapter import ErrorAdapter

class ErrorHandlingPresenter(BasePresenter):
    """Presenter for the Error Handling view."""
    
    # Type hints for view and app
    view: 'ErrorHandlingView'
    app: 'AutoClickApp'
    
    def __init__(self, view: 'ErrorHandlingView', app: 'AutoClickApp', service: 'ErrorAdapter'):
        """
        Initialize the error handling presenter.
        
        Args:
            view: The error handling view
            app: The main application
            service: The error adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.strategies = []  # List of recovery strategies
    
    def initialize_view(self):
        """Initialize the view with data."""
        try:
            # Load recovery strategies
            self.load_strategies()
            
            self.update_app_status("Error handling initialized")
        except Exception as e:
            self._handle_error("initializing error handling", e)
    
    def load_strategies(self):
        """Load recovery strategies from the service."""
        try:
            # Get all strategies from the service
            self.strategies = self.service.get_recovery_strategies()
            
            # Update the view
            self.view.update_strategy_list(self.strategies)
            
            self.update_app_status("Recovery strategies loaded")
        except Exception as e:
            self._handle_error("loading recovery strategies", e)
    
    def select_strategy(self, strategy_id: str):
        """
        Select a recovery strategy.
        
        Args:
            strategy_id: ID of the strategy to select
        """
        try:
            # Find the strategy
            strategy = next((s for s in self.strategies if s["id"] == strategy_id), None)
            
            if not strategy:
                self.view.display_strategy_details(None)
                return
            
            # Display the strategy details
            self.view.display_strategy_details(strategy)
            
            self.update_app_status(f"Selected strategy: {strategy['name']}")
        except Exception as e:
            self._handle_error(f"selecting strategy {strategy_id}", e)
    
    def add_strategy(self):
        """Add a new recovery strategy."""
        try:
            # Create a new strategy with default values
            strategy_id = str(uuid.uuid4())
            strategy = {
                "id": strategy_id,
                "name": "New Strategy",
                "error_type": "Any",
                "action": "Retry",
                "max_retries": 3,
                "retry_delay": 1000
            }
            
            # Add the strategy to the service
            self.service.add_recovery_strategy(strategy)
            
            # Add the strategy to the list
            self.strategies.append(strategy)
            
            # Update the view
            self.view.update_strategy_list(self.strategies)
            
            # Select the new strategy
            self.view.strategy_tree.selection_set(strategy_id)
            self.select_strategy(strategy_id)
            
            self.update_app_status(f"Added new strategy: {strategy['name']}")
        except Exception as e:
            self._handle_error("adding strategy", e)
    
    def update_strategy(self, strategy_id: str, strategy_data: Dict[str, Any]):
        """
        Update a recovery strategy.
        
        Args:
            strategy_id: ID of the strategy to update
            strategy_data: New data for the strategy
        """
        try:
            # Find the strategy
            strategy_index = next((i for i, s in enumerate(self.strategies) if s["id"] == strategy_id), -1)
            
            if strategy_index == -1:
                messagebox.showerror("Error", f"Strategy {strategy_id} not found")
                return
            
            # Update the strategy
            strategy_data["id"] = strategy_id
            self.strategies[strategy_index] = strategy_data
            
            # Update the strategy in the service
            self.service.update_recovery_strategy(strategy_id, strategy_data)
            
            # Update the view
            self.view.update_strategy_list(self.strategies)
            
            # Re-select the strategy
            self.view.strategy_tree.selection_set(strategy_id)
            self.select_strategy(strategy_id)
            
            self.update_app_status(f"Updated strategy: {strategy_data['name']}")
        except Exception as e:
            self._handle_error(f"updating strategy {strategy_id}", e)
    
    def delete_strategy(self, strategy_id: str):
        """
        Delete a recovery strategy.
        
        Args:
            strategy_id: ID of the strategy to delete
        """
        try:
            # Find the strategy
            strategy_index = next((i for i, s in enumerate(self.strategies) if s["id"] == strategy_id), -1)
            
            if strategy_index == -1:
                messagebox.showerror("Error", f"Strategy {strategy_id} not found")
                return
            
            # Get the strategy name
            strategy_name = self.strategies[strategy_index]["name"]
            
            # Delete the strategy from the service
            self.service.delete_recovery_strategy(strategy_id)
            
            # Delete the strategy from the list
            del self.strategies[strategy_index]
            
            # Update the view
            self.view.update_strategy_list(self.strategies)
            
            # Clear the details
            self.view.display_strategy_details(None)
            
            self.update_app_status(f"Deleted strategy: {strategy_name}")
        except Exception as e:
            self._handle_error(f"deleting strategy {strategy_id}", e)
