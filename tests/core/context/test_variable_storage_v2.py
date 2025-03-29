"""Tests for the enhanced variable storage"""
import unittest
from typing import Any, Dict, List, Set

from src.core.context.variable_storage import VariableScope, VariableChangeEvent
from src.core.context.variable_storage_v2 import VariableStorageV2
from src.core.variables.variable_interface import VariableType
from src.core.variables.variable import Variable
from src.core.variables.typed_variables import (
    StringVariable, NumberVariable, BooleanVariable, ListVariable, DictionaryVariable
)


class TestVariableStorageV2(unittest.TestCase):
    """Tests for the VariableStorageV2 class"""
    
    def setUp(self):
        """Set up the test"""
        self.storage = VariableStorageV2()
        
    def test_set_get(self):
        """Test setting and getting variables"""
        # Set a variable
        self.storage.set("test", "value")
        
        # Get the variable
        value = self.storage.get("test")
        
        # Assert
        self.assertEqual(value, "value")
        
    def test_get_variable(self):
        """Test getting variable objects"""
        # Set a variable
        self.storage.set("test", "value")
        
        # Get the variable object
        variable = self.storage.get_variable("test")
        
        # Assert
        self.assertIsNotNone(variable)
        self.assertEqual(variable.get_name(), "test")
        self.assertEqual(variable.get_value(), "value")
        self.assertEqual(variable.get_type(), VariableType.STRING)
        self.assertEqual(variable.get_scope(), VariableScope.WORKFLOW)
        
    def test_create_variable(self):
        """Test creating variables with specific types"""
        # Create variables of different types
        string_var = self.storage.create_variable("string", "value", VariableType.STRING)
        number_var = self.storage.create_variable("number", 42, VariableType.NUMBER)
        bool_var = self.storage.create_variable("bool", True, VariableType.BOOLEAN)
        list_var = self.storage.create_variable("list", [1, 2, 3], VariableType.LIST)
        dict_var = self.storage.create_variable("dict", {"key": "value"}, VariableType.DICTIONARY)
        
        # Assert
        self.assertEqual(string_var.get_value(), "value")
        self.assertEqual(number_var.get_value(), 42)
        self.assertEqual(bool_var.get_value(), True)
        self.assertEqual(list_var.get_value(), [1, 2, 3])
        self.assertEqual(dict_var.get_value(), {"key": "value"})
        
        self.assertEqual(string_var.get_type(), VariableType.STRING)
        self.assertEqual(number_var.get_type(), VariableType.NUMBER)
        self.assertEqual(bool_var.get_type(), VariableType.BOOLEAN)
        self.assertEqual(list_var.get_type(), VariableType.LIST)
        self.assertEqual(dict_var.get_type(), VariableType.DICTIONARY)
        
    def test_get_typed_variable(self):
        """Test getting typed variables"""
        # Create variables of different types
        self.storage.create_variable("string", "value", VariableType.STRING)
        self.storage.create_variable("number", 42, VariableType.NUMBER)
        
        # Get the variables with correct types
        string_var = self.storage.get_typed_variable("string", VariableType.STRING)
        number_var = self.storage.get_typed_variable("number", VariableType.NUMBER)
        
        # Assert
        self.assertIsNotNone(string_var)
        self.assertIsNotNone(number_var)
        self.assertEqual(string_var.get_value(), "value")
        self.assertEqual(number_var.get_value(), 42)
        
        # Try to get a variable with the wrong type
        with self.assertRaises(TypeError):
            self.storage.get_typed_variable("string", VariableType.NUMBER)
            
    def test_get_typed_values(self):
        """Test getting typed values"""
        # Create variables of different types
        self.storage.create_variable("string", "value", VariableType.STRING)
        self.storage.create_variable("number", 42, VariableType.NUMBER)
        self.storage.create_variable("bool", True, VariableType.BOOLEAN)
        self.storage.create_variable("list", [1, 2, 3], VariableType.LIST)
        self.storage.create_variable("dict", {"key": "value"}, VariableType.DICTIONARY)
        
        # Get the values with type-specific methods
        string_val = self.storage.get_string("string")
        number_val = self.storage.get_number("number")
        bool_val = self.storage.get_boolean("bool")
        list_val = self.storage.get_list("list")
        dict_val = self.storage.get_dictionary("dict")
        
        # Assert
        self.assertEqual(string_val, "value")
        self.assertEqual(number_val, 42)
        self.assertEqual(bool_val, True)
        self.assertEqual(list_val, [1, 2, 3])
        self.assertEqual(dict_val, {"key": "value"})
        
        # Try to get a value with the wrong type
        with self.assertRaises(TypeError):
            self.storage.get_string("number")
            
    def test_variable_scopes(self):
        """Test variable scopes"""
        # Create variables in different scopes
        self.storage.create_variable("global_var", "global", scope=VariableScope.GLOBAL)
        self.storage.create_variable("workflow_var", "workflow", scope=VariableScope.WORKFLOW)
        self.storage.create_variable("local_var", "local", scope=VariableScope.LOCAL)
        
        # Get the variables
        global_var = self.storage.get("global_var")
        workflow_var = self.storage.get("workflow_var")
        local_var = self.storage.get("local_var")
        
        # Assert
        self.assertEqual(global_var, "global")
        self.assertEqual(workflow_var, "workflow")
        self.assertEqual(local_var, "local")
        
        # Check scopes
        self.assertEqual(self.storage.get_scope("global_var"), VariableScope.GLOBAL)
        self.assertEqual(self.storage.get_scope("workflow_var"), VariableScope.WORKFLOW)
        self.assertEqual(self.storage.get_scope("local_var"), VariableScope.LOCAL)
        
    def test_variable_inheritance(self):
        """Test variable inheritance from parent storage"""
        # Create a parent storage with a variable
        parent = VariableStorageV2()
        parent.create_variable("parent_var", "parent_value")
        
        # Create a child storage
        child = VariableStorageV2(parent=parent)
        
        # Get the variable from the child
        value = child.get("parent_var")
        
        # Assert
        self.assertEqual(value, "parent_value")
        
        # Override the variable in the child
        child.create_variable("parent_var", "child_value")
        
        # Get the variable from the child
        value = child.get("parent_var")
        
        # Assert
        self.assertEqual(value, "child_value")
        
    def test_delete_variable(self):
        """Test deleting variables"""
        # Create a variable
        self.storage.create_variable("test", "value")
        
        # Check that it exists
        self.assertTrue(self.storage.has("test"))
        
        # Delete the variable
        result = self.storage.delete("test")
        
        # Assert
        self.assertTrue(result)
        self.assertFalse(self.storage.has("test"))
        self.assertIsNone(self.storage.get("test"))
        
    def test_clear_scope(self):
        """Test clearing a scope"""
        # Create variables in different scopes
        self.storage.create_variable("global_var", "global", scope=VariableScope.GLOBAL)
        self.storage.create_variable("workflow_var", "workflow", scope=VariableScope.WORKFLOW)
        self.storage.create_variable("local_var", "local", scope=VariableScope.LOCAL)
        
        # Clear the workflow scope
        self.storage.clear_scope(VariableScope.WORKFLOW)
        
        # Assert
        self.assertTrue(self.storage.has("global_var"))
        self.assertFalse(self.storage.has("workflow_var"))
        self.assertTrue(self.storage.has("local_var"))
        
    def test_clear_all(self):
        """Test clearing all scopes"""
        # Create variables in different scopes
        self.storage.create_variable("global_var", "global", scope=VariableScope.GLOBAL)
        self.storage.create_variable("workflow_var", "workflow", scope=VariableScope.WORKFLOW)
        self.storage.create_variable("local_var", "local", scope=VariableScope.LOCAL)
        
        # Clear all scopes
        self.storage.clear_all()
        
        # Assert
        self.assertFalse(self.storage.has("global_var"))
        self.assertFalse(self.storage.has("workflow_var"))
        self.assertFalse(self.storage.has("local_var"))
        
    def test_get_all(self):
        """Test getting all variables"""
        # Create variables in different scopes
        self.storage.create_variable("global_var", "global", scope=VariableScope.GLOBAL)
        self.storage.create_variable("workflow_var", "workflow", scope=VariableScope.WORKFLOW)
        self.storage.create_variable("local_var", "local", scope=VariableScope.LOCAL)
        
        # Get all variables
        all_vars = self.storage.get_all()
        
        # Assert
        self.assertEqual(len(all_vars), 3)
        self.assertEqual(all_vars["global_var"], "global")
        self.assertEqual(all_vars["workflow_var"], "workflow")
        self.assertEqual(all_vars["local_var"], "local")
        
        # Get variables from a specific scope
        workflow_vars = self.storage.get_all(scope=VariableScope.WORKFLOW)
        
        # Assert
        self.assertEqual(len(workflow_vars), 1)
        self.assertEqual(workflow_vars["workflow_var"], "workflow")
        
    def test_get_all_variables(self):
        """Test getting all variable objects"""
        # Create variables in different scopes
        self.storage.create_variable("global_var", "global", scope=VariableScope.GLOBAL)
        self.storage.create_variable("workflow_var", "workflow", scope=VariableScope.WORKFLOW)
        self.storage.create_variable("local_var", "local", scope=VariableScope.LOCAL)
        
        # Get all variable objects
        all_vars = self.storage.get_all_variables()
        
        # Assert
        self.assertEqual(len(all_vars), 3)
        self.assertEqual(all_vars["global_var"].get_value(), "global")
        self.assertEqual(all_vars["workflow_var"].get_value(), "workflow")
        self.assertEqual(all_vars["local_var"].get_value(), "local")
        
        # Get variable objects from a specific scope
        workflow_vars = self.storage.get_all_variables(scope=VariableScope.WORKFLOW)
        
        # Assert
        self.assertEqual(len(workflow_vars), 1)
        self.assertEqual(workflow_vars["workflow_var"].get_value(), "workflow")
        
    def test_get_names(self):
        """Test getting variable names"""
        # Create variables in different scopes
        self.storage.create_variable("global_var", "global", scope=VariableScope.GLOBAL)
        self.storage.create_variable("workflow_var", "workflow", scope=VariableScope.WORKFLOW)
        self.storage.create_variable("local_var", "local", scope=VariableScope.LOCAL)
        
        # Get all variable names
        all_names = self.storage.get_names()
        
        # Assert
        self.assertEqual(len(all_names), 3)
        self.assertIn("global_var", all_names)
        self.assertIn("workflow_var", all_names)
        self.assertIn("local_var", all_names)
        
        # Get variable names from a specific scope
        workflow_names = self.storage.get_names(scope=VariableScope.WORKFLOW)
        
        # Assert
        self.assertEqual(len(workflow_names), 1)
        self.assertIn("workflow_var", workflow_names)
        
    def test_has(self):
        """Test checking if a variable exists"""
        # Create a variable
        self.storage.create_variable("test", "value")
        
        # Check if it exists
        exists = self.storage.has("test")
        
        # Assert
        self.assertTrue(exists)
        
        # Check if a non-existent variable exists
        exists = self.storage.has("non_existent")
        
        # Assert
        self.assertFalse(exists)
        
    def test_variable_change_notification(self):
        """Test variable change notification"""
        # Create a variable
        variable = self.storage.create_variable("test", "value")
        
        # Create a listener
        changes = []
        
        def listener(event: VariableChangeEvent):
            changes.append((event.name, event.old_value, event.new_value))
            
        # Add the listener
        self.storage.add_variable_change_listener(listener)
        
        # Change the variable value
        variable.set_value("new_value")
        
        # Assert
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0], ("test", "value", "new_value"))
        
        # Remove the listener
        self.storage.remove_variable_change_listener(listener)
        
        # Change the variable value again
        variable.set_value("another_value")
        
        # Assert - no new changes recorded
        self.assertEqual(len(changes), 1)
        
    def test_clone(self):
        """Test cloning the variable storage"""
        # Create variables
        self.storage.create_variable("string", "value", VariableType.STRING)
        self.storage.create_variable("number", 42, VariableType.NUMBER)
        
        # Clone the storage
        clone = self.storage.clone()
        
        # Assert
        self.assertEqual(clone.get("string"), "value")
        self.assertEqual(clone.get("number"), 42)
        
        # Change a variable in the original
        self.storage.get_variable("string").set_value("new_value")
        
        # Assert - clone should not be affected
        self.assertEqual(self.storage.get("string"), "new_value")
        self.assertEqual(clone.get("string"), "value")
        
    def test_serialization(self):
        """Test serialization to and from dictionary"""
        # Create variables
        self.storage.create_variable("string", "value", VariableType.STRING)
        self.storage.create_variable("number", 42, VariableType.NUMBER)
        
        # Serialize to dictionary
        data = self.storage.to_dict()
        
        # Create a new storage from the dictionary
        new_storage = VariableStorageV2.from_dict(data)
        
        # Assert
        self.assertEqual(new_storage.get("string"), "value")
        self.assertEqual(new_storage.get("number"), 42)
        self.assertEqual(new_storage.get_variable("string").get_type(), VariableType.STRING)
        self.assertEqual(new_storage.get_variable("number").get_type(), VariableType.NUMBER)
        
    def test_invalid_variable_name(self):
        """Test validation of variable names"""
        # Try to create a variable with an invalid name
        with self.assertRaises(ValueError):
            self.storage.create_variable("", "value")
            
        with self.assertRaises(ValueError):
            self.storage.create_variable("123invalid", "value")
            
        with self.assertRaises(ValueError):
            self.storage.create_variable("invalid name", "value")
            
        # Valid names should work
        self.storage.create_variable("valid_name", "value")
        self.storage.create_variable("_valid_name", "value")
        self.storage.create_variable("validName123", "value")


if __name__ == "__main__":
    unittest.main()
