"""Tests for the condition factory"""
import unittest
from unittest.mock import patch, MagicMock

from src.core.conditions.condition_factory import ConditionFactoryClass, ConditionFactory
from src.core.conditions.base_condition import BaseCondition
from src.core.conditions.condition_interface import ConditionResult


# Test condition for factory tests
class TestCondition(BaseCondition[bool]):
    """Test condition for factory tests"""

    def __init__(self, test_param: str = "", description: str = None, condition_id: str = None):
        """Initialize the test condition"""
        super().__init__(description, condition_id)
        self.test_param = test_param

    @property
    def type(self) -> str:
        """Get the condition type"""
        return "test_condition"

    def _evaluate(self, context):
        """Evaluate the condition"""
        return ConditionResult.create_success(True, "Test condition")

    def to_dict(self):
        """Convert the condition to a dictionary"""
        data = super().to_dict()
        data["test_param"] = self.test_param
        return data

    @classmethod
    def from_dict(cls, data):
        """Create a condition from a dictionary"""
        return cls(
            test_param=data.get("test_param", ""),
            description=data.get("description"),
            condition_id=data.get("id")
        )


class TestConditionFactory(unittest.TestCase):
    """Test cases for the ConditionFactory class"""

    def setUp(self):
        """Set up test environment"""
        # Create a new factory instance for each test
        self.factory = ConditionFactoryClass()
        
        # Clear the registry
        self.factory._registry = {}

    def test_singleton_pattern(self):
        """Test that the factory uses the singleton pattern"""
        # Arrange & Act
        factory1 = ConditionFactoryClass()
        factory2 = ConditionFactoryClass()
        factory3 = ConditionFactoryClass.get_instance()

        # Assert
        self.assertIs(factory1, factory2)
        self.assertIs(factory1, factory3)
        self.assertIs(factory2, factory3)

    def test_register_condition_type(self):
        """Test registering a condition type"""
        # Arrange & Act
        self.factory.register_condition_type("test_condition", TestCondition)

        # Assert
        self.assertIn("test_condition", self.factory._registry)
        self.assertEqual(self.factory._registry["test_condition"], TestCondition)

    def test_register_invalid_condition_type(self):
        """Test registering an invalid condition type"""
        # Arrange & Act & Assert
        with self.assertRaises(TypeError):
            self.factory.register_condition_type("invalid", str)  # str is not a BaseCondition

    def test_create_condition(self):
        """Test creating a condition from data"""
        # Arrange
        self.factory.register_condition_type("test_condition", TestCondition)
        condition_data = {
            "type": "test_condition",
            "test_param": "test value",
            "description": "Test description",
            "id": "test-id"
        }

        # Act
        condition = self.factory.create_condition(condition_data)

        # Assert
        self.assertIsInstance(condition, TestCondition)
        self.assertEqual(condition.test_param, "test value")
        self.assertEqual(condition.description, "Test description")
        self.assertEqual(condition.id, "test-id")

    def test_create_unknown_condition_type(self):
        """Test creating a condition with an unknown type"""
        # Arrange
        condition_data = {
            "type": "unknown_condition",
            "test_param": "test value"
        }

        # Act & Assert
        with self.assertRaises(ValueError):
            self.factory.create_condition(condition_data)

    def test_get_available_condition_types(self):
        """Test getting available condition types"""
        # Arrange
        self.factory.register_condition_type("test_condition1", TestCondition)
        self.factory.register_condition_type("test_condition2", TestCondition)

        # Act
        types = self.factory.get_available_condition_types()

        # Assert
        self.assertEqual(len(types), 2)
        self.assertIn("test_condition1", types)
        self.assertIn("test_condition2", types)

    @patch("importlib.import_module")
    def test_load_conditions_from_module(self, mock_import_module):
        """Test loading conditions from a module"""
        # Arrange
        # Create a mock module with a condition class
        mock_module = MagicMock()
        mock_module.__all__ = ["TestCondition"]
        mock_module.TestCondition = TestCondition
        mock_import_module.return_value = mock_module

        # Act
        self.factory.load_conditions_from_module("test_module")

        # Assert
        mock_import_module.assert_called_once_with("test_module")
        self.assertIn("test_condition", self.factory._registry)
        self.assertEqual(self.factory._registry["test_condition"], TestCondition)

    def test_register_decorator(self):
        """Test the register decorator"""
        # Arrange & Act
        @ConditionFactoryClass.register("decorated_condition")
        class DecoratedCondition(TestCondition):
            pass

        # Assert
        factory = ConditionFactoryClass.get_instance()
        self.assertIn("decorated_condition", factory._registry)
        self.assertEqual(factory._registry["decorated_condition"], DecoratedCondition)

    def test_register_decorator_invalid_class(self):
        """Test the register decorator with an invalid class"""
        # Arrange & Act & Assert
        with self.assertRaises(TypeError):
            @ConditionFactoryClass.register("invalid_condition")
            class InvalidCondition:  # Not a BaseCondition
                pass

    def test_global_factory_instance(self):
        """Test the global factory instance"""
        # Arrange & Act
        factory = ConditionFactory

        # Assert
        self.assertIsInstance(factory, ConditionFactoryClass)
        self.assertIs(factory, ConditionFactoryClass.get_instance())


if __name__ == "__main__":
    unittest.main()
