"""Tests for the ErrorAdapter class."""
import unittest
from unittest.mock import MagicMock, patch

from src.ui.adapters.error_adapter import ErrorAdapter
from src.core.models import ErrorConfig as UIErrorConfig

class TestErrorAdapter(unittest.TestCase):
    """Test cases for the ErrorAdapter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.adapter = ErrorAdapter()
    
    def test_get_all_error_configs(self):
        """Test getting all error configurations."""
        # Act
        result = self.adapter.get_all_error_configs()
        
        # Assert
        self.assertEqual(len(result), 5)  # Default configs
        self.assertIsInstance(result[0], UIErrorConfig)
    
    def test_get_error_config(self):
        """Test getting an error configuration by type."""
        # Act
        result = self.adapter.get_error_config("connection.timeout")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, "connection.timeout")
        self.assertEqual(result.severity, "Warning")
        self.assertEqual(result.action, "Retry")
    
    def test_get_error_config_not_found(self):
        """Test getting an error configuration by type when it doesn't exist."""
        # Act
        result = self.adapter.get_error_config("nonexistent.error")
        
        # Assert
        self.assertIsNone(result)
    
    def test_add_error_config(self):
        """Test adding an error configuration."""
        # Act
        result = self.adapter.add_error_config(
            error_type="test.error",
            severity="Info",
            action="Log"
        )
        
        # Assert
        self.assertEqual(result.error_type, "test.error")
        self.assertEqual(result.severity, "Info")
        self.assertEqual(result.action, "Log")
        
        # Verify it was added to the dictionary
        self.assertIn("test.error", self.adapter.error_configs)
        self.assertEqual(self.adapter.error_configs["test.error"], result)
    
    def test_update_error_config(self):
        """Test updating an error configuration."""
        # Arrange
        self.adapter.add_error_config(
            error_type="test.error",
            severity="Info",
            action="Log"
        )
        
        # Act
        result = self.adapter.update_error_config(
            error_type="test.error",
            severity="Warning",
            action="Retry"
        )
        
        # Assert
        self.assertEqual(result.error_type, "test.error")
        self.assertEqual(result.severity, "Warning")
        self.assertEqual(result.action, "Retry")
        
        # Verify it was updated in the dictionary
        self.assertEqual(self.adapter.error_configs["test.error"].severity, "Warning")
        self.assertEqual(self.adapter.error_configs["test.error"].action, "Retry")
    
    def test_update_error_config_partial(self):
        """Test partially updating an error configuration."""
        # Arrange
        self.adapter.add_error_config(
            error_type="test.error",
            severity="Info",
            action="Log"
        )
        
        # Act
        result = self.adapter.update_error_config(
            error_type="test.error",
            severity="Warning"
        )
        
        # Assert
        self.assertEqual(result.error_type, "test.error")
        self.assertEqual(result.severity, "Warning")
        self.assertEqual(result.action, "Log")  # Unchanged
    
    def test_update_error_config_not_found(self):
        """Test updating an error configuration that doesn't exist."""
        # Act
        result = self.adapter.update_error_config(
            error_type="nonexistent.error",
            severity="Warning"
        )
        
        # Assert
        self.assertIsNone(result)
    
    def test_delete_error_config(self):
        """Test deleting an error configuration."""
        # Arrange
        self.adapter.add_error_config(
            error_type="test.error",
            severity="Info",
            action="Log"
        )
        
        # Act
        result = self.adapter.delete_error_config("test.error")
        
        # Assert
        self.assertTrue(result)
        self.assertNotIn("test.error", self.adapter.error_configs)
    
    def test_delete_error_config_not_found(self):
        """Test deleting an error configuration that doesn't exist."""
        # Act
        result = self.adapter.delete_error_config("nonexistent.error")
        
        # Assert
        self.assertFalse(result)
    
    def test_get_error_hierarchy(self):
        """Test getting the error type hierarchy."""
        # Arrange
        self.adapter.add_error_config("test.error.specific", "Info", "Log")
        self.adapter.add_error_config("test.error.another", "Warning", "Retry")
        self.adapter.add_error_config("other.category", "Error", "Stop")
        
        # Act
        result = self.adapter.get_error_hierarchy()
        
        # Assert
        self.assertIn("test", result)
        self.assertIn("error", result["test"])
        self.assertIn("specific", result["test"]["error"])
        self.assertIn("another", result["test"]["error"])
        self.assertIn("other", result)
        self.assertIn("category", result["other"])

if __name__ == "__main__":
    unittest.main()
