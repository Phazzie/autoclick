"""Tests for the text contains condition"""
import unittest
from unittest.mock import MagicMock

from src.core.conditions.text_contains_condition import TextContainsCondition


class TestTextContainsCondition(unittest.TestCase):
    """Test cases for the TextContainsCondition class"""

    def test_initialization(self):
        """Test initializing a text contains condition"""
        # Arrange & Act
        condition = TextContainsCondition(
            selector="#test-element",
            text="test text",
            case_sensitive=True,
            description="Test text contains",
            condition_id="test-id"
        )

        # Assert
        self.assertEqual(condition.description, "Test text contains")
        self.assertEqual(condition.id, "test-id")
        self.assertEqual(condition.type, "text_contains")
        self.assertEqual(condition.selector, "#test-element")
        self.assertEqual(condition.text, "test text")
        self.assertTrue(condition.case_sensitive)

    def test_default_description(self):
        """Test that a default description is generated if not provided"""
        # Arrange & Act
        condition = TextContainsCondition(selector="#test-element", text="test text")

        # Assert
        self.assertEqual(condition.description, "Text contains: test text in #test-element")

    def test_default_case_sensitivity(self):
        """Test that case sensitivity is False by default"""
        # Arrange & Act
        condition = TextContainsCondition(selector="#test-element", text="test text")

        # Assert
        self.assertFalse(condition.case_sensitive)

    def test_evaluate_text_contains_case_sensitive(self):
        """Test evaluating when the text contains the string (case sensitive)"""
        # Arrange
        condition = TextContainsCondition(
            selector="#test-element",
            text="Test Text",
            case_sensitive=True
        )
        
        # Create mock driver and element
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.text = "This is a Test Text example"
        mock_driver.find_elements_by_css_selector.return_value = [mock_element]
        
        context = {"driver": mock_driver}

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(result.value)
        mock_driver.find_elements_by_css_selector.assert_called_once_with("#test-element")

    def test_evaluate_text_contains_case_insensitive(self):
        """Test evaluating when the text contains the string (case insensitive)"""
        # Arrange
        condition = TextContainsCondition(
            selector="#test-element",
            text="test text",
            case_sensitive=False
        )
        
        # Create mock driver and element
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.text = "This is a TEST TEXT example"
        mock_driver.find_elements_by_css_selector.return_value = [mock_element]
        
        context = {"driver": mock_driver}

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(result.value)
        mock_driver.find_elements_by_css_selector.assert_called_once_with("#test-element")

    def test_evaluate_text_not_contains_case_sensitive(self):
        """Test evaluating when the text does not contain the string (case sensitive)"""
        # Arrange
        condition = TextContainsCondition(
            selector="#test-element",
            text="Test Text",
            case_sensitive=True
        )
        
        # Create mock driver and element
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.text = "This is a test text example"  # lowercase, won't match
        mock_driver.find_elements_by_css_selector.return_value = [mock_element]
        
        context = {"driver": mock_driver}

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertTrue(result.success)
        self.assertFalse(result.value)
        mock_driver.find_elements_by_css_selector.assert_called_once_with("#test-element")

    def test_evaluate_element_not_found(self):
        """Test evaluating when the element is not found"""
        # Arrange
        condition = TextContainsCondition(selector="#test-element", text="test text")
        
        # Create mock driver with no elements
        mock_driver = MagicMock()
        mock_driver.find_elements_by_css_selector.return_value = []
        
        context = {"driver": mock_driver}

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertTrue(result.success)
        self.assertFalse(result.value)
        self.assertIn("Element not found", result.message)
        mock_driver.find_elements_by_css_selector.assert_called_once_with("#test-element")

    def test_evaluate_no_driver(self):
        """Test evaluating with no driver in the context"""
        # Arrange
        condition = TextContainsCondition(selector="#test-element", text="test text")
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
        condition = TextContainsCondition(selector="#test-element", text="test text")
        
        # Create mock driver that raises an exception
        mock_driver = MagicMock()
        mock_driver.find_elements_by_css_selector.side_effect = Exception("Test exception")
        
        context = {"driver": mock_driver}

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertFalse(result.success)
        self.assertFalse(result.value)
        self.assertIn("Error checking text", result.message)
        self.assertIn("Test exception", result.message)

    def test_to_dict(self):
        """Test converting a text contains condition to a dictionary"""
        # Arrange
        condition = TextContainsCondition(
            selector="#test-element",
            text="test text",
            case_sensitive=True,
            description="Test text contains",
            condition_id="test-id"
        )

        # Act
        data = condition.to_dict()

        # Assert
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "text_contains")
        self.assertEqual(data["description"], "Test text contains")
        self.assertEqual(data["selector"], "#test-element")
        self.assertEqual(data["text"], "test text")
        self.assertTrue(data["case_sensitive"])

    def test_from_dict(self):
        """Test creating a text contains condition from a dictionary"""
        # Arrange
        data = {
            "id": "test-id",
            "type": "text_contains",
            "description": "Test text contains",
            "selector": "#test-element",
            "text": "test text",
            "case_sensitive": True
        }

        # Act
        condition = TextContainsCondition.from_dict(data)

        # Assert
        self.assertEqual(condition.id, "test-id")
        self.assertEqual(condition.description, "Test text contains")
        self.assertEqual(condition.selector, "#test-element")
        self.assertEqual(condition.text, "test text")
        self.assertTrue(condition.case_sensitive)


if __name__ == "__main__":
    unittest.main()
