"""Tests for the element exists condition"""
import unittest
from unittest.mock import MagicMock

from src.core.conditions.element_exists_condition import ElementExistsCondition


class TestElementExistsCondition(unittest.TestCase):
    """Test cases for the ElementExistsCondition class"""

    def test_initialization(self):
        """Test initializing an element exists condition"""
        # Arrange & Act
        condition = ElementExistsCondition(
            selector="#test-element",
            description="Test element exists",
            condition_id="test-id"
        )

        # Assert
        self.assertEqual(condition.description, "Test element exists")
        self.assertEqual(condition.id, "test-id")
        self.assertEqual(condition.type, "element_exists")
        self.assertEqual(condition.selector, "#test-element")

    def test_default_description(self):
        """Test that a default description is generated if not provided"""
        # Arrange & Act
        condition = ElementExistsCondition(selector="#test-element")

        # Assert
        self.assertEqual(condition.description, "Element exists: #test-element")

    def test_evaluate_element_exists(self):
        """Test evaluating when the element exists"""
        # Arrange
        condition = ElementExistsCondition(selector="#test-element")
        
        # Create mock driver and elements
        mock_driver = MagicMock()
        mock_elements = [MagicMock()]
        mock_driver.find_elements_by_css_selector.return_value = mock_elements
        
        context = {"driver": mock_driver}

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(result.value)
        mock_driver.find_elements_by_css_selector.assert_called_once_with("#test-element")

    def test_evaluate_element_not_exists(self):
        """Test evaluating when the element does not exist"""
        # Arrange
        condition = ElementExistsCondition(selector="#test-element")
        
        # Create mock driver with no elements
        mock_driver = MagicMock()
        mock_driver.find_elements_by_css_selector.return_value = []
        
        context = {"driver": mock_driver}

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertTrue(result.success)
        self.assertFalse(result.value)
        mock_driver.find_elements_by_css_selector.assert_called_once_with("#test-element")

    def test_evaluate_no_driver(self):
        """Test evaluating with no driver in the context"""
        # Arrange
        condition = ElementExistsCondition(selector="#test-element")
        context = {}  # Empty context with no driver

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertFalse(result.success)
        self.assertFalse(result.value)
        self.assertIn("No browser driver in context", result.message)

    def test_evaluate_driver_exception(self):
        """Test evaluating when the driver raises an exception"""
        # Arrange
        condition = ElementExistsCondition(selector="#test-element")
        
        # Create mock driver that raises an exception
        mock_driver = MagicMock()
        mock_driver.find_elements_by_css_selector.side_effect = Exception("Test exception")
        
        context = {"driver": mock_driver}

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertFalse(result.success)
        self.assertFalse(result.value)
        self.assertIn("Error finding element", result.message)
        self.assertIn("Test exception", result.message)

    def test_to_dict(self):
        """Test converting an element exists condition to a dictionary"""
        # Arrange
        condition = ElementExistsCondition(
            selector="#test-element",
            description="Test element exists",
            condition_id="test-id"
        )

        # Act
        data = condition.to_dict()

        # Assert
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "element_exists")
        self.assertEqual(data["description"], "Test element exists")
        self.assertEqual(data["selector"], "#test-element")

    def test_from_dict(self):
        """Test creating an element exists condition from a dictionary"""
        # Arrange
        data = {
            "id": "test-id",
            "type": "element_exists",
            "description": "Test element exists",
            "selector": "#test-element"
        }

        # Act
        condition = ElementExistsCondition.from_dict(data)

        # Assert
        self.assertEqual(condition.id, "test-id")
        self.assertEqual(condition.description, "Test element exists")
        self.assertEqual(condition.selector, "#test-element")


if __name__ == "__main__":
    unittest.main()
