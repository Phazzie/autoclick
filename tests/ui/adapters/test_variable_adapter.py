"""Tests for the VariableAdapter class."""
import unittest
from unittest.mock import MagicMock, patch

from src.core.variables.variable_storage import VariableStorage
from src.core.variables.variable_type import VariableType
from src.ui.adapters.impl.variable_adapter import VariableAdapter


class TestVariableAdapter(unittest.TestCase):
    """Test cases for the VariableAdapter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_variable_storage = MagicMock(spec=VariableStorage)
        self.adapter = VariableAdapter(self.mock_variable_storage)
    
    def test_get_variable_types(self):
        """Test getting variable types."""
        # Act
        result = self.adapter.get_variable_types()
        
        # Assert
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["id"], "string")
        self.assertEqual(result[1]["id"], "number")
        self.assertEqual(result[2]["id"], "boolean")
        self.assertEqual(result[3]["id"], "list")
        self.assertEqual(result[4]["id"], "dictionary")
    
    def test_get_all_variables(self):
        """Test getting all variables."""
        # Arrange
        variables = {
            "var1": ("value1", VariableType.STRING),
            "var2": (42, VariableType.NUMBER),
            "var3": (True, VariableType.BOOLEAN)
        }
        
        self.mock_variable_storage.get_all_variables.return_value = variables
        
        # Act
        result = self.adapter.get_all_variables()
        
        # Assert
        self.assertEqual(len(result), 3)
        
        # Check first variable
        self.assertEqual(result[0]["name"], "var1")
        self.assertEqual(result[0]["value"], "value1")
        self.assertEqual(result[0]["type"], "string")
        
        # Check second variable
        self.assertEqual(result[1]["name"], "var2")
        self.assertEqual(result[1]["value"], 42)
        self.assertEqual(result[1]["type"], "number")
        
        # Check third variable
        self.assertEqual(result[2]["name"], "var3")
        self.assertEqual(result[2]["value"], True)
        self.assertEqual(result[2]["type"], "boolean")
        
        # Verify storage was called
        self.mock_variable_storage.get_all_variables.assert_called_once()
    
    def test_get_variable(self):
        """Test getting a variable by name."""
        # Arrange
        self.mock_variable_storage.has_variable.return_value = True
        self.mock_variable_storage.get_variable.return_value = "value1"
        self.mock_variable_storage.get_variable_type.return_value = VariableType.STRING
        
        # Act
        result = self.adapter.get_variable("var1")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "var1")
        self.assertEqual(result["value"], "value1")
        self.assertEqual(result["type"], "string")
        
        # Verify storage was called
        self.mock_variable_storage.has_variable.assert_called_once_with("var1")
        self.mock_variable_storage.get_variable.assert_called_once_with("var1")
        self.mock_variable_storage.get_variable_type.assert_called_once_with("var1")
    
    def test_get_variable_not_found(self):
        """Test getting a variable that doesn't exist."""
        # Arrange
        self.mock_variable_storage.has_variable.return_value = False
        
        # Act
        result = self.adapter.get_variable("nonexistent")
        
        # Assert
        self.assertIsNone(result)
        
        # Verify storage was called
        self.mock_variable_storage.has_variable.assert_called_once_with("nonexistent")
        self.mock_variable_storage.get_variable.assert_not_called()
    
    def test_set_variable(self):
        """Test setting a variable."""
        # Arrange
        self.mock_variable_storage.set_variable.return_value = None
        
        # Act
        result = self.adapter.set_variable("var1", "value1", "string")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "var1")
        self.assertEqual(result["value"], "value1")
        self.assertEqual(result["type"], "string")
        
        # Verify storage was called
        self.mock_variable_storage.set_variable.assert_called_once_with("var1", "value1", VariableType.STRING)
    
    def test_set_variable_infer_type(self):
        """Test setting a variable with type inference."""
        # Arrange
        self.mock_variable_storage.set_variable.return_value = None
        
        # Act
        result = self.adapter.set_variable("var1", "value1")  # No type specified
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "var1")
        self.assertEqual(result["value"], "value1")
        self.assertEqual(result["type"], "string")
        
        # Verify storage was called
        self.mock_variable_storage.set_variable.assert_called_once_with("var1", "value1", VariableType.STRING)
    
    def test_set_variable_invalid(self):
        """Test setting a variable with invalid data."""
        # Act/Assert
        with self.assertRaises(ValueError) as context:
            self.adapter.set_variable("", "value1")  # Invalid: empty name
        
        # Verify error message
        self.assertIn("Invalid variable", str(context.exception))
        
        # Verify storage was not called
        self.mock_variable_storage.set_variable.assert_not_called()
    
    def test_delete_variable(self):
        """Test deleting a variable."""
        # Arrange
        self.mock_variable_storage.has_variable.return_value = True
        self.mock_variable_storage.delete_variable.return_value = None
        
        # Act
        result = self.adapter.delete_variable("var1")
        
        # Assert
        self.assertTrue(result)
        
        # Verify storage was called
        self.mock_variable_storage.has_variable.assert_called_once_with("var1")
        self.mock_variable_storage.delete_variable.assert_called_once_with("var1")
    
    def test_delete_variable_not_found(self):
        """Test deleting a variable that doesn't exist."""
        # Arrange
        self.mock_variable_storage.has_variable.return_value = False
        
        # Act
        result = self.adapter.delete_variable("nonexistent")
        
        # Assert
        self.assertFalse(result)
        
        # Verify storage was called
        self.mock_variable_storage.has_variable.assert_called_once_with("nonexistent")
        self.mock_variable_storage.delete_variable.assert_not_called()
    
    def test_validate_variable(self):
        """Test validating a variable."""
        # Act
        result = self.adapter.validate_variable("var1", "value1", "string")
        
        # Assert
        self.assertEqual(result, [])
    
    def test_validate_variable_invalid_name(self):
        """Test validating a variable with an invalid name."""
        # Act
        result = self.adapter.validate_variable("", "value1", "string")
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Variable name is required")
    
    def test_validate_variable_invalid_type(self):
        """Test validating a variable with an invalid type."""
        # Act
        result = self.adapter.validate_variable("var1", "value1", "invalid_type")
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertIn("Unsupported variable type", result[0])
    
    def test_validate_variable_type_mismatch(self):
        """Test validating a variable with a type mismatch."""
        # Act
        result = self.adapter.validate_variable("var1", "value1", "number")
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Number variable must be a number")
    
    def test_infer_variable_type(self):
        """Test inferring variable type from value."""
        # Test string
        self.assertEqual(self.adapter._infer_variable_type("value1"), "string")
        
        # Test number
        self.assertEqual(self.adapter._infer_variable_type(42), "number")
        self.assertEqual(self.adapter._infer_variable_type(3.14), "number")
        
        # Test boolean
        self.assertEqual(self.adapter._infer_variable_type(True), "boolean")
        self.assertEqual(self.adapter._infer_variable_type(False), "boolean")
        
        # Test list
        self.assertEqual(self.adapter._infer_variable_type([1, 2, 3]), "list")
        
        # Test dictionary
        self.assertEqual(self.adapter._infer_variable_type({"key": "value"}), "dictionary")
        
        # Test unknown (defaults to string)
        self.assertEqual(self.adapter._infer_variable_type(None), "string")


if __name__ == "__main__":
    unittest.main()
