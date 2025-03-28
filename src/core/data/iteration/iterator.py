"""Data iteration components"""
from typing import Dict, Any, List, Optional, Iterator, Callable
import logging

from src.core.data.sources.base import DataSource
from src.core.data.mapping.mapper import DataMapper


class DataIterationResult:
    """
    Result of a data iteration
    
    This class holds the results of executing a workflow with
    a specific data record.
    """
    
    def __init__(
        self,
        record_index: int,
        record: Dict[str, Any],
        success: bool,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the data iteration result
        
        Args:
            record_index: Index of the record in the data source
            record: The data record
            success: Whether the iteration was successful
            message: Result message
            data: Additional result data
        """
        self.record_index = record_index
        self.record = record
        self.success = success
        self.message = message
        self.data = data or {}
        
    def __str__(self) -> str:
        """String representation of the result"""
        status = "Success" if self.success else "Failure"
        return f"Record {self.record_index}: {status} - {self.message}"


class DataIterator:
    """
    Iterates through data records and executes a workflow for each
    
    This class handles the iteration through a data source, mapping
    each record to the execution context, and executing a workflow
    for each record.
    """
    
    def __init__(
        self,
        data_source: DataSource,
        data_mapper: DataMapper,
        continue_on_error: bool = True,
        max_errors: Optional[int] = None
    ):
        """
        Initialize the data iterator
        
        Args:
            data_source: Data source to iterate through
            data_mapper: Mapper to map records to the execution context
            continue_on_error: Whether to continue iterating after an error
            max_errors: Maximum number of errors before stopping
        """
        self.data_source = data_source
        self.data_mapper = data_mapper
        self.continue_on_error = continue_on_error
        self.max_errors = max_errors
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def iterate(
        self,
        execute_func: Callable[[Dict[str, Any]], Dict[str, Any]],
        base_context: Optional[Dict[str, Any]] = None
    ) -> Iterator[DataIterationResult]:
        """
        Iterate through the data source and execute a function for each record
        
        Args:
            execute_func: Function to execute for each record
            base_context: Base execution context
            
        Returns:
            Iterator over iteration results
        """
        base_context = base_context or {}
        error_count = 0
        
        # Open the data source
        with self.data_source:
            # Iterate through the records
            for i, record in enumerate(self.data_source.get_records()):
                # Map the record to the context
                context = self.data_mapper.map_record(record, base_context)
                
                try:
                    # Execute the function
                    result = execute_func(context)
                    
                    # Create a result object
                    success = result.get("success", False)
                    message = result.get("message", "")
                    
                    iteration_result = DataIterationResult(
                        record_index=i,
                        record=record,
                        success=success,
                        message=message,
                        data=result
                    )
                    
                    # Count errors
                    if not success:
                        error_count += 1
                        
                    # Yield the result
                    yield iteration_result
                    
                    # Check if we should stop due to errors
                    if not success and not self.continue_on_error:
                        self.logger.warning(f"Stopping iteration due to error: {message}")
                        break
                        
                    if self.max_errors is not None and error_count >= self.max_errors:
                        self.logger.warning(f"Stopping iteration after {error_count} errors")
                        break
                        
                except Exception as e:
                    # Handle exceptions during execution
                    error_count += 1
                    
                    # Create a result object for the exception
                    iteration_result = DataIterationResult(
                        record_index=i,
                        record=record,
                        success=False,
                        message=f"Exception: {str(e)}",
                        data={"exception": str(e)}
                    )
                    
                    # Log the exception
                    self.logger.error(f"Exception during iteration for record {i}: {str(e)}", exc_info=True)
                    
                    # Yield the result
                    yield iteration_result
                    
                    # Check if we should stop due to errors
                    if not self.continue_on_error:
                        self.logger.warning("Stopping iteration due to exception")
                        break
                        
                    if self.max_errors is not None and error_count >= self.max_errors:
                        self.logger.warning(f"Stopping iteration after {error_count} errors")
                        break
