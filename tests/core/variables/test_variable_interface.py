"""Tests for the variable interface system"""
import unittest
from typing import Any, List, Dict
from datetime import datetime

from src.core.context.variable_storage import VariableScope
from src.core.variables.variable_interface import (
    IValueHolder, ITyped, IObservable, ISerializable, VariableType, VariableChangeEvent
)
from src.core.variables.variable import Variable


class TestVariableInterface(unittest.TestCase):
    """Tests for the variable interface components"""
    
    def test_value_holder_interface(self):
        """Test the IValueHolder interface"""
        # Arrange
        var = Variable("test", "value", VariableType.STRING)
        
        # Act & Assert
        self.assertEqual(var.get_value(), "value")
        
        # Act
        var.set_value("new value")
        
        # Assert
        self.assertEqual(var.get_value(), "new value")
    
    def test_typed_interface(self):
        """Test the ITyped interface"""
        # Arrange
        var = Variable("test", "value", VariableType.STRING)
        
        # Act & Assert
        self.assertEqual(var.get_type(), VariableType.STRING)
        self.assertTrue(var.is_valid_value("another string"))
        self.assertFalse(var.is_valid_value(123))
    
    def test_observable_interface(self):
        """Test the IObservable interface"""
        # Arrange
        var = Variable("test", "value", VariableType.STRING)
        changes: List[VariableChangeEvent] = []
        
        def listener(event: VariableChangeEvent) -> None:
            changes.append(event)
        
        # Act
        var.add_change_listener(listener)
        var.set_value("new value")
        
        # Assert
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].variable_name, "test")
        self.assertEqual(changes[0].old_value, "value")
        self.assertEqual(changes[0].new_value, "new value")
        
        # Act
        var.remove_change_listener(listener)
        var.set_value("another value")
        
        # Assert - no new changes recorded
        self.assertEqual(len(changes), 1)
    
    def test_serializable_interface(self):
        """Test the ISerializable interface"""
        # Arrange
        var = Variable("test", 123, VariableType.NUMBER, VariableScope.GLOBAL)
        
        # Act
        data = var.to_dict()
        new_var = Variable.from_dict(data)
        
        # Assert
        self.assertEqual(new_var.get_name(), "test")
        self.assertEqual(new_var.get_type(), VariableType.NUMBER)
        self.assertEqual(new_var.get_value(), 123)
        self.assertEqual(new_var.get_scope(), VariableScope.GLOBAL)


class TestVariableCreation(unittest.TestCase):
    """Tests for variable creation and validation"""
    
    def test_create_string_variable(self):
        """Test creating a string variable"""
        # Arrange & Act
        var = Variable("name", "value", VariableType.STRING)
        
        # Assert
        self.assertEqual(var.get_name(), "name")
        self.assertEqual(var.get_value(), "value")
        self.assertEqual(var.get_type(), VariableType.STRING)
        self.assertEqual(var.get_scope(), VariableScope.WORKFLOW)  # Default scope
    
    def test_create_number_variable(self):
        """Test creating a number variable"""
        # Arrange & Act
        var = Variable("count", 42, VariableType.NUMBER)
        
        # Assert
        self.assertEqual(var.get_value(), 42)
        self.assertEqual(var.get_type(), VariableType.NUMBER)
    
    def test_create_boolean_variable(self):
        """Test creating a boolean variable"""
        # Arrange & Act
        var = Variable("flag", True, VariableType.BOOLEAN)
        
        # Assert
        self.assertEqual(var.get_value(), True)
        self.assertEqual(var.get_type(), VariableType.BOOLEAN)
    
    def test_create_list_variable(self):
        """Test creating a list variable"""
        # Arrange & Act
        var = Variable("items", [1, 2, 3], VariableType.LIST)
        
        # Assert
        self.assertEqual(var.get_value(), [1, 2, 3])
        self.assertEqual(var.get_type(), VariableType.LIST)
    
    def test_create_dict_variable(self):
        """Test creating a dictionary variable"""
        # Arrange & Act
        var = Variable("config", {"key": "value"}, VariableType.DICTIONARY)
        
        # Assert
        self.assertEqual(var.get_value(), {"key": "value"})
        self.assertEqual(var.get_type(), VariableType.DICTIONARY)


class TestTypeConversion(unittest.TestCase):
    """Tests for type conversion"""
    
    def test_string_to_number_conversion(self):
        """Test converting string to number"""
        # Arrange & Act
        var = Variable("count", "42", VariableType.NUMBER)
        
        # Assert
        self.assertEqual(var.get_value(), 42)
        self.assertEqual(var.get_type(), VariableType.NUMBER)
    
    def test_string_to_boolean_conversion(self):
        """Test converting string to boolean"""
        # Arrange & Act
        var1 = Variable("flag1", "true", VariableType.BOOLEAN)
        var2 = Variable("flag2", "false", VariableType.BOOLEAN)
        var3 = Variable("flag3", "1", VariableType.BOOLEAN)
        var4 = Variable("flag4", "0", VariableType.BOOLEAN)
        
        # Assert
        self.assertEqual(var1.get_value(), True)
        self.assertEqual(var2.get_value(), False)
        self.assertEqual(var3.get_value(), True)
        self.assertEqual(var4.get_value(), False)
    
    def test_number_to_boolean_conversion(self):
        """Test converting number to boolean"""
        # Arrange & Act
        var1 = Variable("flag1", 1, VariableType.BOOLEAN)
        var2 = Variable("flag2", 0, VariableType.BOOLEAN)
        
        # Assert
        self.assertEqual(var1.get_value(), True)
        self.assertEqual(var2.get_value(), False)
    
    def test_invalid_conversion(self):
        """Test invalid type conversion"""
        # Arrange & Act & Assert
        with self.assertRaises(ValueError):
            Variable("invalid", "not a valid number", VariableType.NUMBER)
        
        with self.assertRaises(ValueError):
            Variable("invalid", "not a valid boolean", VariableType.BOOLEAN)
        
        with self.assertRaises(ValueError):
            Variable("invalid", "not valid json", VariableType.DICTIONARY)


class TestMetadata(unittest.TestCase):
    """Tests for variable metadata"""
    
    def test_metadata_operations(self):
        """Test metadata operations"""
        # Arrange
        var = Variable("test", "value", VariableType.STRING)
        
        # Act & Assert - initially empty
        self.assertEqual(var.get_metadata(), {})
        
        # Act
        var.set_metadata("description", "A test variable")
        
        # Assert
        self.assertEqual(var.get_metadata(), {"description": "A test variable"})
        self.assertEqual(var.get_metadata_value("description"), "A test variable")
        self.assertIsNone(var.get_metadata_value("non_existent"))
        self.assertEqual(var.get_metadata_value("non_existent", "default"), "default")
        
        # Act
        var.set_metadata("category", "test")
        
        # Assert
        self.assertEqual(var.get_metadata(), {
            "description": "A test variable",
            "category": "test"
        })


if __name__ == "__main__":
    unittest.main()
