"""Tests for the variable factory"""
import unittest
from typing import Any, Dict

from src.core.context.variable_storage import VariableScope
from src.core.variables.variable_interface import VariableType
from src.core.variables.variable_factory import VariableFactory
from src.core.variables.typed_variables import (
    StringVariable, NumberVariable, BooleanVariable, ListVariable, DictionaryVariable
)


class TestVariableFactory(unittest.TestCase):
    """Tests for the VariableFactory"""
    
    def setUp(self):
        """Set up the test"""
        self.factory = VariableFactory()
    
    def test_create_variable_by_type(self):
        """Test creating variables by explicit type"""
        # Arrange & Act
        string_var = self.factory.create_variable("name", "value", VariableType.STRING)
        number_var = self.factory.create_variable("count", 42, VariableType.NUMBER)
        bool_var = self.factory.create_variable("flag", True, VariableType.BOOLEAN)
        list_var = self.factory.create_variable("items", [1, 2, 3], VariableType.LIST)
        dict_var = self.factory.create_variable("config", {"key": "value"}, VariableType.DICTIONARY)
        
        # Assert
        self.assertIsInstance(string_var, StringVariable)
        self.assertIsInstance(number_var, NumberVariable)
        self.assertIsInstance(bool_var, BooleanVariable)
        self.assertIsInstance(list_var, ListVariable)
        self.assertIsInstance(dict_var, DictionaryVariable)
    
    def test_create_variable_by_value(self):
        """Test creating variables by inferring type from value"""
        # Arrange & Act
        string_var = self.factory.create_variable("name", "value")
        number_var = self.factory.create_variable("count", 42)
        bool_var = self.factory.create_variable("flag", True)
        list_var = self.factory.create_variable("items", [1, 2, 3])
        dict_var = self.factory.create_variable("config", {"key": "value"})
        
        # Assert
        self.assertIsInstance(string_var, StringVariable)
        self.assertIsInstance(number_var, NumberVariable)
        self.assertIsInstance(bool_var, BooleanVariable)
        self.assertIsInstance(list_var, ListVariable)
        self.assertIsInstance(dict_var, DictionaryVariable)
    
    def test_create_from_dict(self):
        """Test creating variables from dictionary"""
        # Arrange
        data = {
            "name": "test",
            "type": "STRING",
            "value": "value",
            "scope": "GLOBAL",
            "metadata": {"description": "A test variable"}
        }
        
        # Act
        var = self.factory.create_from_dict(data)
        
        # Assert
        self.assertIsInstance(var, StringVariable)
        self.assertEqual(var.get_name(), "test")
        self.assertEqual(var.get_value(), "value")
        self.assertEqual(var.get_type(), VariableType.STRING)
        self.assertEqual(var.get_scope(), VariableScope.GLOBAL)
        self.assertEqual(var.get_metadata(), {"description": "A test variable"})
    
    def test_register_custom_type(self):
        """Test registering a custom variable type"""
        # Arrange
        class CustomVariable(StringVariable):
            """Custom variable type for testing"""
            
            @classmethod
            def get_variable_type(cls) -> VariableType:
                return VariableType.OBJECT
        
        # Act
        self.factory.register_variable_class(VariableType.OBJECT, CustomVariable)
        var = self.factory.create_variable("custom", "value", VariableType.OBJECT)
        
        # Assert
        self.assertIsInstance(var, CustomVariable)


if __name__ == "__main__":
    unittest.main()
