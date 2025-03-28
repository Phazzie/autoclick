"""Data-driven action implementation"""
from typing import Dict, Any, List, Optional
import logging

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.action_factory import ActionFactory
from src.core.data.sources.base import DataSource, DataSourceFactory
from src.core.data.mapping.mapper import DataMapper
from src.core.data.mapping.variable_mapper import VariableMapper
from src.core.data.iteration.iterator import DataIterator, DataIterationResult
from src.core.data.iteration.context import DataIterationContext


@ActionFactory.register("data_driven")
class DataDrivenAction(BaseAction):
    """
    Action that executes a sequence of actions for each record in a data source
    
    This action iterates through a data source, maps each record to the
    execution context, and executes a sequence of actions for each record.
    """
    
    def __init__(
        self,
        description: str,
        data_source: DataSource,
        actions: List[BaseAction],
        data_mapper: Optional[DataMapper] = None,
        continue_on_error: bool = True,
        max_errors: Optional[int] = None,
        results_variable_name: Optional[str] = None,
        action_id: Optional[str] = None
    ):
        """
        Initialize the data-driven action
        
        Args:
            description: Human-readable description of the action
            data_source: Data source to iterate through
            actions: Actions to execute for each record
            data_mapper: Mapper to map records to the execution context
            continue_on_error: Whether to continue iterating after an error
            max_errors: Maximum number of errors before stopping
            results_variable_name: Name of the variable to store results in
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.data_source = data_source
        self.actions = actions
        self.data_mapper = data_mapper or VariableMapper()
        self.continue_on_error = continue_on_error
        self.max_errors = max_errors
        self.results_variable_name = results_variable_name
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @property
    def type(self) -> str:
        """Get the action type"""
        return "data_driven"
        
    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action
        
        Args:
            context: Execution context containing variables, browser, etc.
            
        Returns:
            Result of the action execution
        """
        # Create a data iterator
        iterator = DataIterator(
            data_source=self.data_source,
            data_mapper=self.data_mapper,
            continue_on_error=self.continue_on_error,
            max_errors=self.max_errors
        )
        
        # Create an iteration context
        iteration_context = DataIterationContext()
        
        # Define the execute function
        def execute_record(record_context: Dict[str, Any]) -> Dict[str, Any]:
            # Execute each action in sequence
            for action in self.actions:
                result = action.execute(record_context)
                if not result.success:
                    return {
                        "success": False,
                        "message": f"Action '{action.description}' failed: {result.message}",
                        "action_result": result
                    }
            
            # All actions succeeded
            return {
                "success": True,
                "message": "All actions executed successfully",
                "context": record_context
            }
        
        # Iterate through the data source
        for result in iterator.iterate(execute_record, context):
            # Add the result to the iteration context
            iteration_context.add_result(result)
            
            # Log the result
            if result.success:
                self.logger.info(f"Record {result.record_index} succeeded: {result.message}")
            else:
                self.logger.warning(f"Record {result.record_index} failed: {result.message}")
        
        # Store the results in the context if requested
        if self.results_variable_name:
            if "variables" in context and hasattr(context["variables"], "set"):
                context["variables"].set(self.results_variable_name, iteration_context)
            else:
                context[self.results_variable_name] = iteration_context
        
        # Get a summary of the results
        summary = iteration_context.get_summary()
        
        # Determine the overall success of the action
        success = summary["error"] == 0
        
        # Create a result message
        message = (
            f"Executed {summary['total']} records: "
            f"{summary['success']} succeeded, {summary['error']} failed"
        )
        
        # Return the result
        if success:
            return ActionResult.create_success(message, {"summary": summary})
        else:
            return ActionResult.create_failure(message, {"summary": summary})
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        
        # We can't directly serialize the data source and mapper,
        # so we'll need to handle them specially in from_dict
        
        data.update({
            "actions": [action.to_dict() for action in self.actions],
            "continue_on_error": self.continue_on_error,
            "max_errors": self.max_errors,
            "results_variable_name": self.results_variable_name,
            "data_source_type": self.data_source.__class__.__name__,
            "data_mapper_type": self.data_mapper.__class__.__name__
        })
        
        return data
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataDrivenAction':
        """
        Create a data-driven action from a dictionary
        
        Args:
            data: Dictionary representation of the action
            
        Returns:
            Instantiated action
        """
        from src.core.actions.action_factory import ActionFactory
        
        # Create the actions
        actions_data = data.get("actions", [])
        actions = [
            ActionFactory.get_instance().create_action(action_data)
            for action_data in actions_data
        ]
        
        # Create a data source
        # This is a simplified implementation that assumes a CSV data source
        data_source = DataSourceFactory.create_csv_source(
            data.get("data_source_file", "data.csv")
        )
        
        # Create a data mapper
        # This is a simplified implementation that creates a default mapper
        data_mapper = VariableMapper()
        
        # Create the data-driven action
        return cls(
            description=data.get("description", ""),
            data_source=data_source,
            actions=actions,
            data_mapper=data_mapper,
            continue_on_error=data.get("continue_on_error", True),
            max_errors=data.get("max_errors"),
            results_variable_name=data.get("results_variable_name"),
            action_id=data.get("id")
        )
