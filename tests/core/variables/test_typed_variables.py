"""Tests for type-specific variable implementations"""
import unittest
from typing import Any, List, Dict

from src.core.context.variable_storage import VariableScope
from src.core.variables.variable_interface import VariableType
from src.core.variables.typed_variables import (
    StringVariable, NumberVariable, BooleanVariable, ListVariable, DictionaryVariable
)


class TestStringVariable(unittest.TestCase):
    """Tests for StringVariable"""
    
    def test_string_operations(self):
        """Test string-specific operations"""
        # Arrange
        var = StringVariable("name", "Hello World")
        
        # Act & Assert
        self.assertEqual(var.get_value(), "Hello World")
        self.assertEqual(var.to_upper(), "HELLO WORLD")
        self.assertEqual(var.to_lower(), "hello world")
        self.assertTrue(var.contains("World"))
        self.assertTrue(var.contains("world", case_sensitive=False))
        self.assertFalse(var.contains("world", case_sensitive=True))
        self.assertFalse(var.is_empty())
        
        # Act
        empty_var = StringVariable("empty", "")
        
        # Assert
        self.assertTrue(empty_var.is_empty())


class TestNumberVariable(unittest.TestCase):
    """Tests for NumberVariable"""
    
    def test_number_operations(self):
        """Test number-specific operations"""
        # Arrange
        var = NumberVariable("count", 42)
        
        # Act & Assert
        self.assertEqual(var.get_value(), 42)
        self.assertEqual(var.increment(), 43)
        self.assertEqual(var.get_value(), 43)
        self.assertEqual(var.increment(5), 48)
        self.assertEqual(var.decrement(), 47)
        self.assertEqual(var.decrement(7), 40)
        self.assertTrue(var.is_integer())
        self.assertEqual(var.to_int(), 40)
        self.assertEqual(var.to_float(), 40.0)
        
        # Act
        float_var = NumberVariable("price", 42.5)
        
        # Assert
        self.assertFalse(float_var.is_integer())
        self.assertEqual(float_var.to_int(), 42)
        self.assertEqual(float_var.to_float(), 42.5)


class TestBooleanVariable(unittest.TestCase):
    """Tests for BooleanVariable"""
    
    def test_boolean_operations(self):
        """Test boolean-specific operations"""
        # Arrange
        var = BooleanVariable("flag", True)
        
        # Act & Assert
        self.assertEqual(var.get_value(), True)
        self.assertEqual(var.toggle(), False)
        self.assertEqual(var.get_value(), False)
        self.assertEqual(var.toggle(), True)


class TestListVariable(unittest.TestCase):
    """Tests for ListVariable"""
    
    def test_list_operations(self):
        """Test list-specific operations"""
        # Arrange
        var = ListVariable("items", [1, 2, 3])
        
        # Act & Assert
        self.assertEqual(var.get_value(), [1, 2, 3])
        self.assertEqual(var.length(), 3)
        self.assertFalse(var.is_empty())
        self.assertTrue(var.contains(2))
        self.assertFalse(var.contains(4))
        
        # Act
        var.append(4)
        
        # Assert
        self.assertEqual(var.get_value(), [1, 2, 3, 4])
        self.assertEqual(var.length(), 4)
        
        # Act
        var.extend([5, 6])
        
        # Assert
        self.assertEqual(var.get_value(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(var.length(), 6)
        
        # Act
        var.remove(3)
        
        # Assert
        self.assertEqual(var.get_value(), [1, 2, 4, 5, 6])
        self.assertEqual(var.length(), 5)
        
        # Act
        var.set(1, 22)  # Replace index 1 (value 2) with 22
        
        # Assert
        self.assertEqual(var.get_value(), [1, 22, 4, 5, 6])
        self.assertEqual(var.get(1), 22)
        
        # Act
        var.clear()
        
        # Assert
        self.assertEqual(var.get_value(), [])
        self.assertEqual(var.length(), 0)
        self.assertTrue(var.is_empty())


class TestDictionaryVariable(unittest.TestCase):
    """Tests for DictionaryVariable"""
    
    def test_dictionary_operations(self):
        """Test dictionary-specific operations"""
        # Arrange
        var = DictionaryVariable("config", {"name": "test", "value": 42})
        
        # Act & Assert
        self.assertEqual(var.get_value(), {"name": "test", "value": 42})
        self.assertEqual(var.length(), 2)
        self.assertFalse(var.is_empty())
        self.assertTrue(var.has_key("name"))
        self.assertFalse(var.has_key("missing"))
        self.assertEqual(var.get("name"), "test")
        self.assertEqual(var.get("missing", "default"), "default")
        
        # Act
        var.set("new_key", "new_value")
        
        # Assert
        self.assertEqual(var.get_value(), {"name": "test", "value": 42, "new_key": "new_value"})
        self.assertEqual(var.length(), 3)
        
        # Act
        var.remove("name")
        
        # Assert
        self.assertEqual(var.get_value(), {"value": 42, "new_key": "new_value"})
        self.assertEqual(var.length(), 2)
        self.assertFalse(var.has_key("name"))
        
        # Act
        keys = var.keys()
        values = var.values()
        items = var.items()
        
        # Assert
        self.assertEqual(set(keys), {"value", "new_key"})
        self.assertEqual(set(values), {42, "new_value"})
        self.assertEqual(set(items), {("value", 42), ("new_key", "new_value")})
        
        # Act
        var.clear()
        
        # Assert
        self.assertEqual(var.get_value(), {})
        self.assertEqual(var.length(), 0)
        self.assertTrue(var.is_empty())


if __name__ == "__main__":
    unittest.main()
