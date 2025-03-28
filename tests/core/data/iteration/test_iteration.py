"""Tests for data iteration components"""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any, List

from src.core.data.iteration.iterator import DataIterator, DataIterationResult
from src.core.data.iteration.context import DataIterationContext


class TestDataIterationResult(unittest.TestCase):
    """Test cases for the DataIterationResult class"""
    
    def test_create_result(self):
        """Test creating a data iteration result"""
        # Create a result
        result = DataIterationResult(
            record_index=0,
            record={"name": "Alice"},
            success=True,
            message="Test message",
            data={"test": "value"}
        )
        
        # Check the properties
        self.assertEqual(result.record_index, 0)
        self.assertEqual(result.record, {"name": "Alice"})
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Test message")
        self.assertEqual(result.data, {"test": "value"})
        
    def test_str(self):
        """Test the string representation of a result"""
        # Create a successful result
        success_result = DataIterationResult(
            record_index=0,
            record={"name": "Alice"},
            success=True,
            message="Test message"
        )
        
        # Check the string representation
        self.assertEqual(str(success_result), "Record 0: Success - Test message")
        
        # Create a failed result
        failed_result = DataIterationResult(
            record_index=1,
            record={"name": "Bob"},
            success=False,
            message="Test error"
        )
        
        # Check the string representation
        self.assertEqual(str(failed_result), "Record 1: Failure - Test error")


class TestDataIterator(unittest.TestCase):
    """Test cases for the DataIterator class"""
    
    def setUp(self):
        """Set up test environment"""
        # Create mock data source
        self.data_source = MagicMock()
        self.data_source.__enter__ = MagicMock(return_value=self.data_source)
        self.data_source.__exit__ = MagicMock(return_value=None)
        self.data_source.get_records = MagicMock(return_value=[
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35}
        ])
        
        # Create mock data mapper
        self.data_mapper = MagicMock()
        self.data_mapper.map_record = MagicMock(side_effect=lambda record, context: {
            **context,
            "name": record["name"],
            "age": record["age"]
        })
        
    def test_iterate_success(self):
        """Test iterating with successful executions"""
        # Create a data iterator
        iterator = DataIterator(self.data_source, self.data_mapper)
        
        # Create an execute function that always succeeds
        def execute_func(context):
            return {
                "success": True,
                "message": f"Processed {context['name']}",
                "context": context
            }
            
        # Iterate through the data
        results = list(iterator.iterate(execute_func))
        
        # Check the results
        self.assertEqual(len(results), 3)
        self.assertTrue(all(result.success for result in results))
        self.assertEqual(results[0].record["name"], "Alice")
        self.assertEqual(results[1].record["name"], "Bob")
        self.assertEqual(results[2].record["name"], "Charlie")
        
    def test_iterate_failure(self):
        """Test iterating with failed executions"""
        # Create a data iterator
        iterator = DataIterator(self.data_source, self.data_mapper)
        
        # Create an execute function that fails for Bob
        def execute_func(context):
            if context["name"] == "Bob":
                return {
                    "success": False,
                    "message": f"Failed to process {context['name']}",
                    "context": context
                }
            else:
                return {
                    "success": True,
                    "message": f"Processed {context['name']}",
                    "context": context
                }
                
        # Iterate through the data
        results = list(iterator.iterate(execute_func))
        
        # Check the results
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].success)
        self.assertFalse(results[1].success)
        self.assertTrue(results[2].success)
        
    def test_iterate_exception(self):
        """Test iterating with exceptions"""
        # Create a data iterator
        iterator = DataIterator(self.data_source, self.data_mapper)
        
        # Create an execute function that raises an exception for Bob
        def execute_func(context):
            if context["name"] == "Bob":
                raise ValueError("Test exception")
            else:
                return {
                    "success": True,
                    "message": f"Processed {context['name']}",
                    "context": context
                }
                
        # Iterate through the data
        results = list(iterator.iterate(execute_func))
        
        # Check the results
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].success)
        self.assertFalse(results[1].success)
        self.assertTrue(results[2].success)
        self.assertIn("Exception", results[1].message)
        
    def test_iterate_stop_on_error(self):
        """Test stopping iteration on error"""
        # Create a data iterator that stops on error
        iterator = DataIterator(self.data_source, self.data_mapper, continue_on_error=False)
        
        # Create an execute function that fails for Bob
        def execute_func(context):
            if context["name"] == "Bob":
                return {
                    "success": False,
                    "message": f"Failed to process {context['name']}",
                    "context": context
                }
            else:
                return {
                    "success": True,
                    "message": f"Processed {context['name']}",
                    "context": context
                }
                
        # Iterate through the data
        results = list(iterator.iterate(execute_func))
        
        # Check the results
        self.assertEqual(len(results), 2)  # Only Alice and Bob, not Charlie
        self.assertTrue(results[0].success)
        self.assertFalse(results[1].success)
        
    def test_iterate_max_errors(self):
        """Test stopping iteration after max errors"""
        # Create a data iterator with max_errors=1
        iterator = DataIterator(self.data_source, self.data_mapper, max_errors=1)
        
        # Create an execute function that fails for Bob and Charlie
        def execute_func(context):
            if context["name"] in ["Bob", "Charlie"]:
                return {
                    "success": False,
                    "message": f"Failed to process {context['name']}",
                    "context": context
                }
            else:
                return {
                    "success": True,
                    "message": f"Processed {context['name']}",
                    "context": context
                }
                
        # Iterate through the data
        results = list(iterator.iterate(execute_func))
        
        # Check the results
        self.assertEqual(len(results), 2)  # Only Alice and Bob, not Charlie
        self.assertTrue(results[0].success)
        self.assertFalse(results[1].success)


class TestDataIterationContext(unittest.TestCase):
    """Test cases for the DataIterationContext class"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a context
        self.context = DataIterationContext()
        
        # Create some results
        self.result1 = DataIterationResult(
            record_index=0,
            record={"name": "Alice"},
            success=True,
            message="Success 1"
        )
        
        self.result2 = DataIterationResult(
            record_index=1,
            record={"name": "Bob"},
            success=False,
            message="Failure 1"
        )
        
        self.result3 = DataIterationResult(
            record_index=2,
            record={"name": "Charlie"},
            success=True,
            message="Success 2"
        )
        
    def test_start_iteration(self):
        """Test starting an iteration"""
        # Start an iteration
        self.context.start_iteration(0, {"name": "Alice"})
        
        # Check the properties
        self.assertEqual(self.context.current_index, 0)
        self.assertEqual(self.context.current_record, {"name": "Alice"})
        
    def test_add_result(self):
        """Test adding a result"""
        # Add a result
        self.context.add_result(self.result1)
        
        # Check the properties
        self.assertEqual(len(self.context.results), 1)
        self.assertEqual(self.context.success_count, 1)
        self.assertEqual(self.context.error_count, 0)
        
        # Add another result
        self.context.add_result(self.result2)
        
        # Check the properties
        self.assertEqual(len(self.context.results), 2)
        self.assertEqual(self.context.success_count, 1)
        self.assertEqual(self.context.error_count, 1)
        
    def test_get_summary(self):
        """Test getting a summary"""
        # Add some results
        self.context.add_result(self.result1)
        self.context.add_result(self.result2)
        self.context.add_result(self.result3)
        
        # Get the summary
        summary = self.context.get_summary()
        
        # Check the summary
        self.assertEqual(summary["total"], 3)
        self.assertEqual(summary["success"], 2)
        self.assertEqual(summary["error"], 1)
        self.assertEqual(summary["success_rate"], 2/3)
        
    def test_get_results(self):
        """Test getting all results"""
        # Add some results
        self.context.add_result(self.result1)
        self.context.add_result(self.result2)
        self.context.add_result(self.result3)
        
        # Get the results
        results = self.context.get_results()
        
        # Check the results
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], self.result1)
        self.assertEqual(results[1], self.result2)
        self.assertEqual(results[2], self.result3)
        
    def test_get_successful_results(self):
        """Test getting successful results"""
        # Add some results
        self.context.add_result(self.result1)
        self.context.add_result(self.result2)
        self.context.add_result(self.result3)
        
        # Get the successful results
        results = self.context.get_successful_results()
        
        # Check the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], self.result1)
        self.assertEqual(results[1], self.result3)
        
    def test_get_failed_results(self):
        """Test getting failed results"""
        # Add some results
        self.context.add_result(self.result1)
        self.context.add_result(self.result2)
        self.context.add_result(self.result3)
        
        # Get the failed results
        results = self.context.get_failed_results()
        
        # Check the results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.result2)


if __name__ == "__main__":
    unittest.main()
