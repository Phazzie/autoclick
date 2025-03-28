"""Data iteration context"""
from typing import Dict, Any, List, Optional
import logging

from src.core.data.iteration.iterator import DataIterationResult


class DataIterationContext:
    """
    Context for data iteration
    
    This class holds the context for a data iteration, including
    the current record, iteration index, and results of previous
    iterations.
    """
    
    def __init__(self):
        """Initialize the data iteration context"""
        self.current_index = -1
        self.current_record = None
        self.results = []
        self.success_count = 0
        self.error_count = 0
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def start_iteration(self, index: int, record: Dict[str, Any]) -> None:
        """
        Start a new iteration
        
        Args:
            index: Index of the record in the data source
            record: The data record
        """
        self.current_index = index
        self.current_record = record
        
    def add_result(self, result: DataIterationResult) -> None:
        """
        Add a result to the context
        
        Args:
            result: Result of the iteration
        """
        self.results.append(result)
        
        if result.success:
            self.success_count += 1
        else:
            self.error_count += 1
            
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the iteration results
        
        Returns:
            Summary dictionary
        """
        return {
            "total": len(self.results),
            "success": self.success_count,
            "error": self.error_count,
            "success_rate": self.success_count / len(self.results) if self.results else 0
        }
        
    def get_results(self) -> List[DataIterationResult]:
        """
        Get all iteration results
        
        Returns:
            List of iteration results
        """
        return self.results.copy()
        
    def get_successful_results(self) -> List[DataIterationResult]:
        """
        Get successful iteration results
        
        Returns:
            List of successful iteration results
        """
        return [result for result in self.results if result.success]
        
    def get_failed_results(self) -> List[DataIterationResult]:
        """
        Get failed iteration results
        
        Returns:
            List of failed iteration results
        """
        return [result for result in self.results if not result.success]
