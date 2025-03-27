"""Tests for the ElementPresenter class"""
import unittest
from unittest.mock import MagicMock

from src.ui.models.element_model import ElementModel
from src.ui.presenters.element_presenter import ElementPresenter


class TestElementPresenter(unittest.TestCase):
    """Test cases for the ElementPresenter class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.model = ElementModel()
        self.view = MagicMock()
        self.presenter = ElementPresenter(self.model, self.view)
        self.test_element = {
            "tag_name": "button",
            "id": "submit-button",
            "class": "btn btn-primary",
            "text": "Submit"
        }

    def test_select_element(self) -> None:
        """Test selecting an element"""
        # Mock the view to return a URL
        self.view.get_url.return_value = "https://example.com"
        
        # Select an element
        self.presenter.select_element()
        
        # Verify the model was updated
        self.assertEqual(self.model.url, "https://example.com")
        self.assertIsNotNone(self.model.selected_element)
        
        # Verify the view was updated
        self.view.display_element_properties.assert_called_once()
        self.view.show_message.assert_called_once_with("Element selected")

    def test_select_element_no_url(self) -> None:
        """Test selecting an element with no URL"""
        # Mock the view to return an empty URL
        self.view.get_url.return_value = ""
        
        # Select an element
        self.presenter.select_element()
        
        # Verify the model was not updated
        self.assertEqual(self.model.url, "")
        self.assertIsNone(self.model.selected_element)
        
        # Verify the view was updated
        self.view.show_message.assert_called_once_with("Please enter a URL")

    def test_clear_selected_element(self) -> None:
        """Test clearing selected element"""
        # Set selected element
        self.model.selected_element = self.test_element
        
        # Clear selected element
        self.presenter.clear_selected_element()
        
        # Verify the model was updated
        self.assertIsNone(self.model.selected_element)
        
        # Verify the view was updated
        self.view.display_element_properties.assert_called_once_with({})
        self.view.show_message.assert_called_once_with("Selected element cleared")

    def test_set_browser_type(self) -> None:
        """Test setting browser type"""
        # Set browser type
        self.presenter.set_browser_type("firefox")
        
        # Verify the model was updated
        self.assertEqual(self.model.browser_type, "firefox")
        
        # Verify the view was updated
        self.view.show_message.assert_called_once_with("Browser type set to firefox")

    def test_set_headless(self) -> None:
        """Test setting headless mode"""
        # Set headless mode
        self.presenter.set_headless(True)
        
        # Verify the model was updated
        self.assertTrue(self.model.headless)
        
        # Verify the view was updated
        self.view.show_message.assert_called_once_with("Headless mode enabled")

    def test_refresh_view_with_element(self) -> None:
        """Test refreshing the view with an element"""
        # Set selected element
        self.model.selected_element = self.test_element
        
        # Refresh the view
        self.presenter.refresh_view()
        
        # Verify the view was updated
        self.view.display_element_properties.assert_called_once()

    def test_refresh_view_without_element(self) -> None:
        """Test refreshing the view without an element"""
        # Refresh the view
        self.presenter.refresh_view()
        
        # Verify the view was updated
        self.view.display_element_properties.assert_called_once_with({})


if __name__ == "__main__":
    unittest.main()
