"""Tests for the ActionFactory"""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.core.actions.action_interface import ActionInterface, ActionResult
from src.core.actions.base_action import BaseAction
from src.core.actions.action_factory import ActionFactory


class TestActionFactory(unittest.TestCase):
    """Test cases for the ActionFactory"""

    def setUp(self):
        """Set up test environment"""
        # Clear the registry before each test
        ActionFactory._instance = None
        ActionFactory._registry = {}

    def test_singleton_pattern(self):
        """Test that ActionFactory follows singleton pattern"""
        # Arrange & Act
        factory1 = ActionFactory.get_instance()
        factory2 = ActionFactory.get_instance()

        # Assert
        self.assertIs(factory1, factory2)

    def test_register_action_type(self):
        """Test registering an action type"""
        # Arrange
        factory = ActionFactory.get_instance()

        # Create a mock action class
        class MockAction(BaseAction):
            @property
            def type(self) -> str:
                return "mock_action"

            def _execute(self, context: Dict[str, Any]) -> ActionResult:
                return ActionResult.create_success("Mock executed")

        # Act
        factory.register_action_type("mock_action", MockAction)

        # Assert
        self.assertIn("mock_action", factory._registry)
        self.assertEqual(factory._registry["mock_action"], MockAction)

    def test_create_action(self):
        """Test creating an action from the factory"""
        # Arrange
        factory = ActionFactory.get_instance()

        # Create a mock action class
        class MockAction(BaseAction):
            @property
            def type(self) -> str:
                return "mock_action"

            def _execute(self, context: Dict[str, Any]) -> ActionResult:
                return ActionResult.create_success("Mock executed")

        factory.register_action_type("mock_action", MockAction)

        # Act
        action_data = {
            "type": "mock_action",
            "description": "Test mock action",
            "id": "test-id"
        }
        action = factory.create_action(action_data)

        # Assert
        self.assertIsInstance(action, MockAction)
        self.assertEqual(action.description, "Test mock action")
        self.assertEqual(action.id, "test-id")

    def test_create_action_unknown_type(self):
        """Test creating an action with unknown type"""
        # Arrange
        factory = ActionFactory.get_instance()

        # Act & Assert
        with self.assertRaises(ValueError):
            factory.create_action({"type": "unknown_type", "description": "Test"})

    def test_register_with_decorator(self):
        """Test registering an action using the decorator"""
        # Arrange
        factory = ActionFactory.get_instance()

        # Define a decorated action class
        @ActionFactory.register("decorated_action")
        class DecoratedAction(BaseAction):
            @property
            def type(self) -> str:
                return "decorated_action"

            def _execute(self, context: Dict[str, Any]) -> ActionResult:
                return ActionResult.create_success("Decorated executed")

        # Act & Assert
        self.assertIn("decorated_action", factory._registry)
        self.assertEqual(factory._registry["decorated_action"], DecoratedAction)

    def test_create_from_dict(self):
        """Test creating an action from a dictionary"""
        # Arrange
        factory = ActionFactory.get_instance()

        # Create a mock action class
        class MockAction(BaseAction):
            @property
            def type(self) -> str:
                return "mock_action"

            def _execute(self, context: Dict[str, Any]) -> ActionResult:
                return ActionResult.create_success("Mock executed")

        factory.register_action_type("mock_action", MockAction)

        # Act
        action_data = {
            "type": "mock_action",
            "description": "Test mock action",
            "id": "test-id"
        }
        action = factory.create_from_dict(action_data)

        # Assert
        self.assertIsInstance(action, MockAction)
        self.assertEqual(action.description, "Test mock action")
        self.assertEqual(action.id, "test-id")

    def test_validation_on_registration(self):
        """Test validation when registering an action type"""
        # Arrange
        factory = ActionFactory.get_instance()

        # Create an invalid action class (not inheriting from BaseAction)
        class InvalidAction:
            def execute(self, context: Dict[str, Any]) -> ActionResult:
                return ActionResult.create_success("Invalid executed")

        # Act & Assert
        with self.assertRaises(TypeError):
            factory.register_action_type("invalid_action", InvalidAction)

    @patch("importlib.import_module")
    def test_load_actions_from_module(self, mock_import_module):
        """Test loading actions from a module"""
        # Arrange
        factory = ActionFactory.get_instance()
        
        # Create mock module with actions
        mock_module = MagicMock()
        
        # Create mock action classes
        class MockAction1(BaseAction):
            @property
            def type(self) -> str:
                return "mock_action1"
                
            def _execute(self, context: Dict[str, Any]) -> ActionResult:
                return ActionResult.create_success("Mock1 executed")
                
        class MockAction2(BaseAction):
            @property
            def type(self) -> str:
                return "mock_action2"
                
            def _execute(self, context: Dict[str, Any]) -> ActionResult:
                return ActionResult.create_success("Mock2 executed")
        
        # Add mock actions to the mock module
        mock_module.MockAction1 = MockAction1
        mock_module.MockAction2 = MockAction2
        mock_module.__all__ = ["MockAction1", "MockAction2"]
        
        # Configure the mock import_module to return our mock module
        mock_import_module.return_value = mock_module
        
        # Act
        factory.load_actions_from_module("mock_module")
        
        # Assert
        self.assertIn("mock_action1", factory._registry)
        self.assertIn("mock_action2", factory._registry)
        self.assertEqual(factory._registry["mock_action1"], MockAction1)
        self.assertEqual(factory._registry["mock_action2"], MockAction2)


if __name__ == "__main__":
    unittest.main()
