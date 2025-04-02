"""
Tests for Variable serialization.

This module contains tests for the serialization of Variable models.
Following TDD principles, these tests are written before implementing the actual code.

SRP-1: Tests variable serialization
"""
import unittest
from typing import Dict, Any
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.core.models import Variable
from src.core.utils.serialization import SerializableMixin


class TestVariableSerialization(unittest.TestCase):
    """Tests for Variable serialization."""

    def setUp(self):
        """Set up test fixtures."""
        # Create variables for testing
        self.string_var = Variable(
            name="string_var",
            value="test value",
            type="string"
        )

        self.number_var = Variable(
            name="number_var",
            value=42,
            type="number"
        )

        self.boolean_var = Variable(
            name="boolean_var",
            value=True,
            type="boolean"
        )

        self.list_var = Variable(
            name="list_var",
            value=["item1", "item2", "item3"],
            type="list"
        )

        self.dict_var = Variable(
            name="dict_var",
            value={"key1": "value1", "key2": "value2"},
            type="dict"
        )

        self.var_with_metadata = Variable(
            name="var_with_metadata",
            value="test",
            type="string",
            metadata={"description": "A test variable", "category": "test"}
        )

    def test_variable_is_serializable(self):
        """Test that Variable implements SerializableMixin."""
        self.assertIsInstance(self.string_var, SerializableMixin)

    def test_to_dict_basic(self):
        """Test basic to_dict functionality."""
        # Convert to dictionary
        result = self.string_var.to_dict()

        # Verify basic properties
        self.assertEqual(result["name"], "string_var")
        self.assertEqual(result["value"], "test value")
        self.assertEqual(result["var_type"], "string")
        self.assertEqual(result["metadata"], {})

    def test_to_dict_with_metadata(self):
        """Test to_dict with metadata."""
        # Convert to dictionary
        result = self.var_with_metadata.to_dict()

        # Verify metadata
        self.assertEqual(result["metadata"]["description"], "A test variable")
        self.assertEqual(result["metadata"]["category"], "test")

    def test_to_dict_with_complex_values(self):
        """Test to_dict with complex values."""
        # Convert list variable to dictionary
        list_result = self.list_var.to_dict()

        # Verify list value
        self.assertEqual(list_result["value"], ["item1", "item2", "item3"])

        # Convert dict variable to dictionary
        dict_result = self.dict_var.to_dict()

        # Verify dict value
        self.assertEqual(dict_result["value"], {"key1": "value1", "key2": "value2"})

    def test_from_dict_basic(self):
        """Test basic from_dict functionality."""
        # Create a dictionary
        data = {
            "name": "test_var",
            "value": "test value",
            "var_type": "string"
        }

        # Create a variable from the dictionary
        variable = Variable.from_dict(data)

        # Verify the variable
        self.assertEqual(variable.name, "test_var")
        self.assertEqual(variable.value, "test value")
        self.assertEqual(variable.type, "string")
        self.assertEqual(variable.metadata, {})

    def test_from_dict_with_metadata(self):
        """Test from_dict with metadata."""
        # Create a dictionary with metadata
        data = {
            "name": "test_var",
            "value": "test value",
            "var_type": "string",
            "metadata": {"description": "A test variable", "category": "test"}
        }

        # Create a variable from the dictionary
        variable = Variable.from_dict(data)

        # Verify the metadata
        self.assertEqual(variable.metadata["description"], "A test variable")
        self.assertEqual(variable.metadata["category"], "test")

    def test_from_dict_with_complex_values(self):
        """Test from_dict with complex values."""
        # Create a dictionary with a list value
        list_data = {
            "name": "list_var",
            "value": ["item1", "item2", "item3"],
            "var_type": "list"
        }

        # Create a variable from the dictionary
        list_var = Variable.from_dict(list_data)

        # Verify the list value
        self.assertEqual(list_var.value, ["item1", "item2", "item3"])

        # Create a dictionary with a dict value
        dict_data = {
            "name": "dict_var",
            "value": {"key1": "value1", "key2": "value2"},
            "var_type": "dict"
        }

        # Create a variable from the dictionary
        dict_var = Variable.from_dict(dict_data)

        # Verify the dict value
        self.assertEqual(dict_var.value, {"key1": "value1", "key2": "value2"})

    def test_from_dict_missing_required(self):
        """Test from_dict with missing required fields."""
        # Create dictionaries with missing required fields
        missing_name = {
            "value": "test value",
            "var_type": "string"
        }

        missing_value = {
            "name": "test_var",
            "var_type": "string"
        }

        missing_var_type = {
            "name": "test_var",
            "value": "test value"
        }

        # Verify that creating variables raises errors
        with self.assertRaises(ValueError):
            Variable.from_dict(missing_name)

        with self.assertRaises(ValueError):
            Variable.from_dict(missing_value)

        with self.assertRaises(ValueError):
            Variable.from_dict(missing_var_type)

    def test_round_trip(self):
        """Test round-trip serialization (to_dict -> from_dict)."""
        # Convert to dictionary and back
        data = self.var_with_metadata.to_dict()
        variable = Variable.from_dict(data)

        # Verify the variable
        self.assertEqual(variable.name, self.var_with_metadata.name)
        self.assertEqual(variable.value, self.var_with_metadata.value)
        self.assertEqual(variable.type, self.var_with_metadata.type)
        self.assertEqual(variable.metadata, self.var_with_metadata.metadata)

    def test_metadata_copy(self):
        """Test that metadata is copied, not referenced."""
        # Create a variable with metadata
        variable = Variable(
            name="test_var",
            value="test value",
            type="string",
            metadata={"key": "value"}
        )

        # Convert to dictionary
        data = variable.to_dict()

        # Modify the metadata in the dictionary
        data["metadata"]["key"] = "new-value"

        # Verify that the original variable's metadata is unchanged
        self.assertEqual(variable.metadata["key"], "value")

        # Create a new variable from the dictionary
        new_variable = Variable.from_dict(data)

        # Modify the new variable's metadata
        new_variable.metadata["key"] = "another-value"

        # Verify that the dictionary's metadata is unchanged
        self.assertEqual(data["metadata"]["key"], "new-value")


if __name__ == "__main__":
    unittest.main()
