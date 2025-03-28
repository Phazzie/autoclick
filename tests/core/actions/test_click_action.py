"""Tests for the ClickAction"""
import unittest
from unittest.mock import MagicMock
from typing import Dict, Any

from src.core.actions.click_action import ClickAction
from src.core.actions.action_factory import ActionFactory


class TestClickAction(unittest.TestCase):
    """Test cases for the ClickAction"""

    @classmethod
    def setUpClass(cls):
        """Set up the test class"""
        # Reset the action factory registry
        ActionFactory.reset_registry()
        # Register the ClickAction
        factory = ActionFactory.get_instance()
        factory.register_action_type("click", ClickAction)

    def test_click_action_initialization(self):
        """Test initializing a ClickAction"""
        # Arrange & Act
        action = ClickAction(description="Click submit button", selector="#submit")

        # Assert
        self.assertEqual(action.description, "Click submit button")
        self.assertEqual(action.selector, "#submit")
        self.assertEqual(action.type, "click")

    def test_click_action_validation(self):
        """Test ClickAction parameter validation"""
        # Arrange & Act & Assert
        with self.assertRaises(ValueError):
            ClickAction(description="Click button", selector="")  # Empty selector

    def test_click_action_serialization(self):
        """Test serializing a ClickAction to dict"""
        # Arrange
        action = ClickAction(description="Click submit button", selector="#submit", action_id="test-id")

        # Act
        serialized = action.to_dict()

        # Assert
        self.assertEqual(serialized["id"], "test-id")
        self.assertEqual(serialized["type"], "click")
        self.assertEqual(serialized["description"], "Click submit button")
        self.assertEqual(serialized["selector"], "#submit")

    def test_click_action_deserialization(self):
        """Test deserializing a dict to ClickAction"""
        # Arrange
        data = {
            "id": "test-id",
            "type": "click",
            "description": "Click submit button",
            "selector": "#submit"
        }

        # Act
        action = ClickAction.from_dict(data)

        # Assert
        self.assertEqual(action.id, "test-id")
        self.assertEqual(action.description, "Click submit button")
        self.assertEqual(action.selector, "#submit")

    def test_click_action_execution_success(self):
        """Test successful execution of ClickAction"""
        # Arrange
        action = ClickAction(description="Click submit button", selector="#submit")

        # Create mock driver and element
        mock_element = MagicMock()
        mock_driver = MagicMock()
        mock_driver.find_element_by_css_selector.return_value = mock_element

        context = {"driver": mock_driver}

        # Act
        result = action.execute(context)

        # Assert
        self.assertTrue(result.success)
        mock_driver.find_element_by_css_selector.assert_called_once_with("#submit")
        mock_element.click.assert_called_once()

    def test_click_action_execution_failure_no_driver(self):
        """Test ClickAction execution with no driver in context"""
        # Arrange
        action = ClickAction(description="Click submit button", selector="#submit")
        context = {}  # Empty context with no driver

        # Act
        result = action.execute(context)

        # Assert
        self.assertFalse(result.success)
        self.assertIn("No browser driver in context", result.message)

    def test_click_action_execution_failure_element_not_found(self):
        """Test ClickAction execution when element is not found"""
        # Arrange
        action = ClickAction(description="Click submit button", selector="#submit")

        # Create mock driver that raises exception
        mock_driver = MagicMock()
        mock_driver.find_element_by_css_selector.side_effect = Exception("Element not found")

        context = {"driver": mock_driver}

        # Act
        result = action.execute(context)

        # Assert
        self.assertFalse(result.success)
        self.assertIn("Failed to click element", result.message)

    def test_factory_registration(self):
        """Test that ClickAction is registered with the factory"""
        # Arrange
        factory = ActionFactory.get_instance()

        # Act & Assert
        self.assertIn("click", factory._registry)
        self.assertEqual(factory._registry["click"], ClickAction)

    def test_factory_creation(self):
        """Test creating a ClickAction from the factory"""
        # Arrange
        factory = ActionFactory.get_instance()

        # Act
        action_data = {
            "type": "click",
            "description": "Click submit button",
            "selector": "#submit",
            "id": "test-id"
        }
        action = factory.create_action(action_data)

        # Assert
        self.assertIsInstance(action, ClickAction)
        self.assertEqual(action.description, "Click submit button")
        self.assertEqual(action.selector, "#submit")
        self.assertEqual(action.id, "test-id")


if __name__ == "__main__":
    unittest.main()
