"""
Tests for ErrorConfig serialization.

This module contains tests for the serialization of ErrorConfig models.
Following TDD principles, these tests are written before implementing the actual code.

SRP-1: Tests error config serialization
"""
import unittest
from typing import Dict, Any, Optional
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.core.models import ErrorConfig
from src.core.utils.serialization import SerializableMixin


class TestErrorConfigSerialization(unittest.TestCase):
    """Tests for ErrorConfig serialization."""

    def setUp(self):
        """Set up test fixtures."""
        # Create error configs for testing
        self.ignore_error = ErrorConfig(
            error_type="element.not.found",
            severity="Warning",
            action="Ignore"
        )
        
        self.retry_error = ErrorConfig(
            error_type="network.timeout",
            severity="Error",
            action="Retry"
        )
        
        self.custom_error = ErrorConfig(
            error_type="custom.error",
            severity="Critical",
            action="Custom",
            custom_action="log_and_notify"
        )

    def test_error_config_is_serializable(self):
        """Test that ErrorConfig implements SerializableMixin."""
        self.assertIsInstance(self.ignore_error, SerializableMixin)
        
    def test_to_dict_basic(self):
        """Test basic to_dict functionality."""
        # Convert to dictionary
        result = self.ignore_error.to_dict()
        
        # Verify basic properties
        self.assertEqual(result["error_type"], "element.not.found")
        self.assertEqual(result["severity"], "Warning")
        self.assertEqual(result["action"], "Ignore")
        self.assertIsNone(result["custom_action"])
        
    def test_to_dict_with_custom_action(self):
        """Test to_dict with custom action."""
        # Convert to dictionary
        result = self.custom_error.to_dict()
        
        # Verify custom action
        self.assertEqual(result["action"], "Custom")
        self.assertEqual(result["custom_action"], "log_and_notify")
        
    def test_from_dict_basic(self):
        """Test basic from_dict functionality."""
        # Create a dictionary
        data = {
            "error_type": "test.error",
            "severity": "Info",
            "action": "Log"
        }
        
        # Create an error config from the dictionary
        error_config = ErrorConfig.from_dict(data)
        
        # Verify the error config
        self.assertEqual(error_config.error_type, "test.error")
        self.assertEqual(error_config.severity, "Info")
        self.assertEqual(error_config.action, "Log")
        self.assertIsNone(error_config.custom_action)
        
    def test_from_dict_with_custom_action(self):
        """Test from_dict with custom action."""
        # Create a dictionary with a custom action
        data = {
            "error_type": "test.error",
            "severity": "Critical",
            "action": "Custom",
            "custom_action": "send_email"
        }
        
        # Create an error config from the dictionary
        error_config = ErrorConfig.from_dict(data)
        
        # Verify the custom action
        self.assertEqual(error_config.action, "Custom")
        self.assertEqual(error_config.custom_action, "send_email")
        
    def test_from_dict_missing_required(self):
        """Test from_dict with missing required fields."""
        # Create a dictionary with missing required fields
        missing_error_type = {
            "severity": "Warning",
            "action": "Ignore"
        }
        
        # Verify that creating an error config raises an error
        with self.assertRaises(ValueError):
            ErrorConfig.from_dict(missing_error_type)
            
    def test_from_dict_default_values(self):
        """Test from_dict with default values."""
        # Create a dictionary with only required fields
        data = {
            "error_type": "test.error"
        }
        
        # Create an error config from the dictionary
        error_config = ErrorConfig.from_dict(data)
        
        # Verify default values
        self.assertEqual(error_config.severity, "Warning")
        self.assertEqual(error_config.action, "Ignore")
        self.assertIsNone(error_config.custom_action)
        
    def test_round_trip(self):
        """Test round-trip serialization (to_dict -> from_dict)."""
        # Convert to dictionary and back
        data = self.custom_error.to_dict()
        error_config = ErrorConfig.from_dict(data)
        
        # Verify the error config
        self.assertEqual(error_config.error_type, self.custom_error.error_type)
        self.assertEqual(error_config.severity, self.custom_error.severity)
        self.assertEqual(error_config.action, self.custom_error.action)
        self.assertEqual(error_config.custom_action, self.custom_error.custom_action)


if __name__ == "__main__":
    unittest.main()
