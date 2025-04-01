"""
Tests for the new condition factory implementation.

This module contains tests for the new condition factory implementation.
"""
import unittest
from unittest.mock import Mock, patch

from src.core.conditions.condition_factory_new import ConditionFactory
from src.core.conditions.exceptions import ConditionFactoryError, ConditionTypeNotFoundError


class TestConditionFactory(unittest.TestCase):
    """Tests for the ConditionFactory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock registry
        self.registry = Mock()
        
        # Create a mock provider
        self.provider = Mock()
        self.provider.provider_id = "test-provider"
        self.provider.get_condition_types.return_value = ["test-condition"]
        self.provider.get_condition_schema.return_value = {"type": "object"}
        
        # Configure the registry
        self.registry.get_provider_for_condition_type.return_value = self.provider
        self.registry.get_condition_types.return_value = ["test-condition"]
        
        # Create a mock resolver
        self.resolver = Mock()
        
        # Create the factory
        self.factory = ConditionFactory(self.registry)
        self.factory._resolver = self.resolver
    
    def test_create_condition(self):
        """Test creating a condition."""
        # Create a mock condition
        condition = Mock()
        
        # Configure the provider
        self.provider.create_condition.return_value = condition
        
        # Create a condition
        result = self.factory.create_condition("test-condition", {"param": "value"})
        
        # Check the result
        self.assertEqual(result, condition)
        
        # Check that the provider was called
        self.registry.get_provider_for_condition_type.assert_called_once_with("test-condition")
        self.provider.create_condition.assert_called_once_with("test-condition", {"param": "value"})
    
    def test_create_condition_unknown_type(self):
        """Test creating a condition with an unknown type."""
        # Configure the registry
        self.registry.get_provider_for_condition_type.return_value = None
        
        # Create a condition
        with self.assertRaises(ConditionFactoryError):
            self.factory.create_condition("unknown-condition", {"param": "value"})
        
        # Check that the registry was called
        self.registry.get_provider_for_condition_type.assert_called_once_with("unknown-condition")
    
    def test_create_condition_provider_error(self):
        """Test creating a condition when the provider raises an error."""
        # Configure the provider
        self.provider.create_condition.side_effect = Exception("Test error")
        
        # Create a condition
        with self.assertRaises(ConditionFactoryError):
            self.factory.create_condition("test-condition", {"param": "value"})
        
        # Check that the provider was called
        self.registry.get_provider_for_condition_type.assert_called_once_with("test-condition")
        self.provider.create_condition.assert_called_once_with("test-condition", {"param": "value"})
    
    def test_get_condition_types(self):
        """Test getting all condition types."""
        # Get condition types
        result = self.factory.get_condition_types()
        
        # Check the result
        self.assertEqual(result, ["test-condition"])
        
        # Check that the registry was called
        self.registry.get_condition_types.assert_called_once()
    
    def test_get_condition_schema(self):
        """Test getting the schema for a condition type."""
        # Get the schema
        result = self.factory.get_condition_schema("test-condition")
        
        # Check the result
        self.assertEqual(result, {"type": "object"})
        
        # Check that the provider was called
        self.registry.get_provider_for_condition_type.assert_called_once_with("test-condition")
        self.provider.get_condition_schema.assert_called_once_with("test-condition")
    
    def test_get_condition_schema_unknown_type(self):
        """Test getting the schema for an unknown condition type."""
        # Configure the registry
        self.registry.get_provider_for_condition_type.return_value = None
        
        # Get the schema
        with self.assertRaises(ConditionFactoryError):
            self.factory.get_condition_schema("unknown-condition")
        
        # Check that the registry was called
        self.registry.get_provider_for_condition_type.assert_called_once_with("unknown-condition")
    
    def test_get_condition_schema_provider_error(self):
        """Test getting the schema when the provider raises an error."""
        # Configure the provider
        self.provider.get_condition_schema.side_effect = Exception("Test error")
        
        # Get the schema
        with self.assertRaises(ConditionFactoryError):
            self.factory.get_condition_schema("test-condition")
        
        # Check that the provider was called
        self.registry.get_provider_for_condition_type.assert_called_once_with("test-condition")
        self.provider.get_condition_schema.assert_called_once_with("test-condition")
    
    def test_create_condition_from_definition(self):
        """Test creating a condition from a definition."""
        # Create a mock condition
        condition = Mock()
        
        # Configure the resolver
        self.resolver.resolve_condition.return_value = condition
        
        # Create a condition
        result = self.factory.create_condition_from_definition({"condition_type": "test-condition"})
        
        # Check the result
        self.assertEqual(result, condition)
        
        # Check that the resolver was called
        self.resolver.resolve_condition.assert_called_once_with({"condition_type": "test-condition"})
    
    def test_create_condition_from_definition_resolver_error(self):
        """Test creating a condition from a definition when the resolver raises an error."""
        # Configure the resolver
        self.resolver.resolve_condition.side_effect = Exception("Test error")
        
        # Create a condition
        with self.assertRaises(ConditionFactoryError):
            self.factory.create_condition_from_definition({"condition_type": "test-condition"})
        
        # Check that the resolver was called
        self.resolver.resolve_condition.assert_called_once_with({"condition_type": "test-condition"})


if __name__ == "__main__":
    unittest.main()
