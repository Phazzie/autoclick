"""Tests for data mapping components"""
import unittest
from unittest.mock import MagicMock
from typing import Dict, Any

from src.core.data.mapping.mapper import FieldMapping
from src.core.data.mapping.variable_mapper import VariableMapper


class TestFieldMapping(unittest.TestCase):
    """Test cases for the FieldMapping class"""
    
    def test_apply_simple(self):
        """Test applying a simple field mapping"""
        # Create a field mapping
        mapping = FieldMapping("name", "username")
        
        # Create a record
        record = {"name": "Alice", "age": 30}
        
        # Apply the mapping
        value = mapping.apply(record)
        
        # Check the value
        self.assertEqual(value, "Alice")
        
    def test_apply_missing_field(self):
        """Test applying a mapping with a missing field"""
        # Create a field mapping
        mapping = FieldMapping("email", "user_email", default_value="no-email")
        
        # Create a record
        record = {"name": "Alice", "age": 30}
        
        # Apply the mapping
        value = mapping.apply(record)
        
        # Check the value
        self.assertEqual(value, "no-email")
        
    def test_apply_transform(self):
        """Test applying a mapping with a transform function"""
        # Create a transform function
        def transform(value):
            return value.upper()
            
        # Create a field mapping
        mapping = FieldMapping("name", "username", transform_function=transform)
        
        # Create a record
        record = {"name": "Alice", "age": 30}
        
        # Apply the mapping
        value = mapping.apply(record)
        
        # Check the value
        self.assertEqual(value, "ALICE")
        
    def test_apply_transform_error(self):
        """Test applying a mapping with a transform function that raises an error"""
        # Create a transform function
        def transform(value):
            raise ValueError("Test error")
            
        # Create a field mapping
        mapping = FieldMapping("name", "username", transform_function=transform, default_value="error")
        
        # Create a record
        record = {"name": "Alice", "age": 30}
        
        # Apply the mapping
        value = mapping.apply(record)
        
        # Check the value
        self.assertEqual(value, "error")


class TestVariableMapper(unittest.TestCase):
    """Test cases for the VariableMapper class"""
    
    def test_add_mapping(self):
        """Test adding a field mapping"""
        # Create a mapper
        mapper = VariableMapper()
        
        # Create a field mapping
        mapping = FieldMapping("name", "username")
        
        # Add the mapping
        mapper.add_mapping(mapping)
        
        # Check that the mapping was added
        self.assertEqual(len(mapper.mappings), 1)
        self.assertEqual(mapper.mappings[0], mapping)
        
    def test_add_simple_mapping(self):
        """Test adding a simple field mapping"""
        # Create a mapper
        mapper = VariableMapper()
        
        # Add a simple mapping
        mapper.add_simple_mapping("name", "username")
        
        # Check that the mapping was added
        self.assertEqual(len(mapper.mappings), 1)
        self.assertEqual(mapper.mappings[0].field_name, "name")
        self.assertEqual(mapper.mappings[0].variable_name, "username")
        
    def test_add_simple_mapping_default_variable_name(self):
        """Test adding a simple field mapping with default variable name"""
        # Create a mapper
        mapper = VariableMapper()
        
        # Add a simple mapping
        mapper.add_simple_mapping("name")
        
        # Check that the mapping was added
        self.assertEqual(len(mapper.mappings), 1)
        self.assertEqual(mapper.mappings[0].field_name, "name")
        self.assertEqual(mapper.mappings[0].variable_name, "name")
        
    def test_map_record(self):
        """Test mapping a record to the context"""
        # Create a mapper
        mapper = VariableMapper()
        
        # Add mappings
        mapper.add_simple_mapping("name", "username")
        mapper.add_simple_mapping("age", "user_age", transform_function=int)
        
        # Create a record
        record = {"name": "Alice", "age": "30", "city": "New York"}
        
        # Create a context
        context = {"existing": "value"}
        
        # Map the record
        result = mapper.map_record(record, context)
        
        # Check the result
        self.assertEqual(result["username"], "Alice")
        self.assertEqual(result["user_age"], 30)
        self.assertEqual(result["existing"], "value")
        
    def test_map_record_with_variables_object(self):
        """Test mapping a record to a context with a variables object"""
        # Create a mapper
        mapper = VariableMapper()
        
        # Add mappings
        mapper.add_simple_mapping("name", "username")
        mapper.add_simple_mapping("age", "user_age", transform_function=int)
        
        # Create a record
        record = {"name": "Alice", "age": "30", "city": "New York"}
        
        # Create a mock variables object
        variables = MagicMock()
        variables.set = MagicMock()
        
        # Create a context with the variables object
        context = {"variables": variables}
        
        # Map the record
        result = mapper.map_record(record, context)
        
        # Check that the variables.set method was called
        variables.set.assert_any_call("username", "Alice")
        variables.set.assert_any_call("user_age", 30)
        
    def test_get_field_mappings(self):
        """Test getting the field mappings"""
        # Create a mapper
        mapper = VariableMapper()
        
        # Add mappings
        mapper.add_simple_mapping("name", "username")
        mapper.add_simple_mapping("age", "user_age")
        
        # Get the field mappings
        mappings = mapper.get_field_mappings()
        
        # Check the mappings
        self.assertEqual(mappings, {"name": "username", "age": "user_age"})


if __name__ == "__main__":
    unittest.main()
